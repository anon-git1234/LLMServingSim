import os
import subprocess
import math
from time import time
import argparse

from inference_serving.scheduler import *
from inference_serving.request import *
from inference_serving.utils import *
from inference_serving.control import *
from inference_serving.kv_manage import *
from inference_serving.generate_graph import *
from inference_serving.generate_text import *
from inference_serving.pim import *


def main():
    cwd = os.getcwd()
    cwd = os.path.join(cwd, "astra-sim")
    os.chdir(cwd)
    parser = argparse.ArgumentParser(description='LLM-Sim') 

    parser.add_argument('--model_name', type=str, help='Name of the model', default='gpt2')
    parser.add_argument('--npu_num', type=int, help='# of NPUs', default=16)
    parser.add_argument('--max_batch', type=int, help='maximum size of the batch', default=0)
    parser.add_argument('--batch_delay', type=int, help='batch delay', default=0)
    parser.add_argument('--scheduling', type=str, help='scheduling of the system', default='orca')
    parser.add_argument('--parallel', type=str, help='parallelism', default='hybrid')
    parser.add_argument('--npu_group', type=int, help='npu_group', default=1)
    parser.add_argument('--npu_mem', type=int, help='npu memory', default=40)
    parser.add_argument('--kv_manage', type=str, help='kv cache management', default='vllm')
    parser.add_argument('--block_size', type=int, help='kv cache block size', default=8)
    parser.add_argument('--pim_type', type=str, help='PIM attached type', default=None)
    parser.add_argument('--sub_batch', action='store_true', default=False, help='PIM sub-batch interleaving')
    parser.add_argument('--dataset', type=str, help='dataset path', default=None)

    args = parser.parse_args()

    ################################################################################################

    model=args.model_name
    npu_num=args.npu_num
    max_batch=args.max_batch if args.max_batch != 0 else float('inf')       # 0 means infinite batch size
    batch_delay=args.batch_delay                                            # tick, not used in orca
    scheduling=args.scheduling if args.scheduling=='orca' else None         # None or orca                  *vLLM is always orca
    parallel=args.parallel                                                  # tensor, pipeline, hybrid      *orca is uses hybrid as default, if npu_num == npu_group: pipeline
    npu_group=args.npu_group                                                # used in hybrid                *if not hybrid, it should be 1
    npu_mem=args.npu_mem                                                    # npu local mem (hbm) in GB     *if pim pool mode, it is size of pim and kv cache is in pim
    kv_manage=args.kv_manage                                                # max, pow2, oracle, vllm
    block_size=args.block_size                                              # kv block size of vLLM  
    pim_type=args.pim_type if args.pim_type in ['local', 'pool'] else None  # None, local, pool             *pim mode for tensor parallelism
    sub_batch=args.sub_batch                                                # True, False                   *used in local pim mode
    dataset=args.dataset
    if pim_type == 'pool':
        npu_num += npu_num

    ### Should change network configuration for npu_groups ###
    ### Need same dim for npu_groups in network json file  ###
    ### Currently it has 1 ~ 128 NPU json file, you can add manually ###
    network_dim = int(math.log2(npu_group))+1
    if npu_group == npu_num: # means pipeline
        network_dim = 1
    if pim_type != 'pool':
        network=cwd+f"/inputs/network/analytical/fully_connected_{network_dim}d_{npu_num}.json"
    else:
        network=cwd+f"/inputs/network/analytical/pim_pool_{npu_num}.json"
    binary=cwd+"/build/astra_analytical/build/AnalyticalAstra/bin/AnalyticalAstra"
    system=cwd+"/inputs/system/sample_fully_connected_sys.txt"
    memory=cwd+"/inputs/remote_memory/analytical/per_npu_memory_expansion.json"

    ### You need to add model reference file in request/model_reference/ ###
    ### This will caculate the model weight size to manage memory constraint ###
    ################################################################################################

    start = time()
    # Calculating Simulator Runtime Latency
    astra_time = 0
    graph_time = 0
    compile_time = 0
    simulate_time = 0
    orca_time = 0
    vllm_time = 0
    pim_time = 0
    subbatch_time = 0

    scheduler = Scheduler(model, max_batch, batch_delay, scheduling, parallel, npu_num, npu_group, npu_mem, kv_manage, block_size, pim_type)

    if dataset != None:
        # generate possion
        scheduler.generate(dataset, isInit=True)

    else:
        # Manually adding request
        for i in range(16):      # model, seq_len, end_len, arrival_time
            scheduler.addRequest([model, 128, 129, 0])

    # Simulator start
    current = 0 # current tick of the system
    sys = 0 # current system id (NPU id)
    id = 0 # id of the request

    # get first request
    first = scheduler.getRequest(current, [i for i in range(npu_num)])
    if sub_batch:
        sb_st = time()
        bats = subbatchInt(first)
        sb_ed = time()
        subbatch_time += sb_ed - sb_st
    else:
        bats = [first]

    for bat in bats:
        # Compile with codelet and generate full request txt with genesys
        comp, sim = generateText(bat, parallel, npu_group)
        compile_time += comp
        simulate_time += sim

        # PIM activate
        if pim_type != None:
            # call the pim simulator and get the result
            # pim_times of gen pahse GEMV
            pim_st = time()
            addPIMtime(bat, npu_group, estimate_mha_latency(bat), pim_type)
            pim_ed = time()
            pim_time += pim_ed - pim_st

    # Schedule the subbatches
    if sub_batch:
        sb_st = time()
        mergeText(first, bats, npu_num, npu_group)
        sb_ed = time()
        subbatch_time += sb_ed - sb_st

    # Make Chakra Grapth
    graph = generateGraph(first, parallel, npu_group, npu_num)
    graph_time += graph

    # set first workload file
    workload=getWorkload(first, parallel, npu_group)
    # run subprocess
    args = [binary, "--workload-configuration="+workload, "--system-configuration="+system, "--network-configuration="+network, "--remote-memory-configuration="+memory]
    astra_st = time()
    p = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    # Calculating Simulator's Throughput
    throughput = []
    prompt_th = 0    # Avg Prompt Throguhput per Sec
    gen_th = 0       # Avg Generation Throughput per Sec
    last_log = 0    # last logged time
    FREQ = 1000000000 # 1 GHz
    INTERVAL = 500000000 # 0.5 second
    RATIO = FREQ//INTERVAL
    total_prompt = 0
    total_gen = 0
    total_latency = 0

    while True:
        out = readWait(p)
        astra_ed = time()
        astra_time += (astra_ed - astra_st)*1000
        out_dict = parseOutput(out[-2])
        # print(out_dict)
        if out_dict != None:
            sys = out_dict['sys']
            id = out_dict['id']
            current = out_dict['cycle']


        # get avaliable request
        # the new request always starts at sys[0]
        if sys == 0:
            new_req = scheduler.getRequest(current, [sys])

            if new_req != None:
                if sub_batch:
                    sb_st = time()
                    bats = subbatchInt(new_req)
                    sb_ed = time()
                    subbatch_time += sb_ed - sb_st
                else:
                    bats = [new_req]

                for bat in bats:
                    # Compile with codelet and generate full request txt with genesys
                    comp, sim = generateText(bat, parallel, npu_group)
                    compile_time += comp
                    simulate_time += sim

                    # PIM activate
                    if pim_type != None:
                        # call the pim simulator and get the result
                        # pim_times of gen pahse GEMV 
                        pim_st = time()                       
                        addPIMtime(bat, npu_group, estimate_mha_latency(bat), pim_type)
                        pim_ed = time()
                        pim_time += pim_ed - pim_st
                # Schedule the subbatches
                if sub_batch:
                    sb_st = time()
                    mergeText(new_req, bats, npu_num, npu_group)
                    sb_ed = time()
                    subbatch_time += sb_ed - sb_st
                # Make Chakra Grapth
                graph = generateGraph(new_req, parallel, npu_group, npu_num)
                graph_time += graph
        # for other systems
        else:
            new_req = scheduler.getInflight(id+1, sys)

        # if no request to issue, pass the waiting
        if new_req == None:
            # check latest inflight request
                astra_st = time()
                writeFlush(p, "pass")
        
        else:
            # Send workload to astra-sim
            if new_req != None:
                # set workload file
                workload = getWorkload(new_req, parallel, npu_group)
                # print(f"sys[{sys}]: {workload}")
                astra_st = time()
                writeFlush(p, workload)

        # check time to store throughput
        if current > last_log + INTERVAL:
            # store the prompt
            throughput.append((prompt_th*RATIO, gen_th*RATIO))
            last_log += INTERVAL
            print(f"[{last_log/FREQ}s] Avg Throughput: propmt: {prompt_th*RATIO} genration: {gen_th*RATIO}")
            prompt_th = 0
            gen_th = 0
        # check request is done
        prompt_t, gen_t = scheduler.addDone(id, sys, current)
        # add tokens in throughput
        prompt_th += prompt_t
        total_prompt += prompt_t
        gen_th += gen_t
        total_gen += gen_t
        
        if scheduler.isRequestEmpty():
            throughput.append((prompt_th*RATIO, gen_th*RATIO))
            last_log += INTERVAL
            print(f"[{last_log/FREQ}s] Avg Throughput: propmt: {prompt_th*RATIO} genration: {gen_th*RATIO}")
            print("---------------------------")
            print("Exiting The Simulator")
            if scheduler.weight == scheduler.used_mem:
                print("Memory Is All Freed")
            else:
                print("Unfreed Memory Exists")
            astra_st = time()
            writeFlush(p, "exit")
            break

    # check all requests are well done
    checkEnd(p)
    astra_ed = time()
    astra_time += (astra_ed - astra_st)*1000
    end = astra_ed
    # print results
    scheduler.printResult()
    total_latency = current/FREQ
    print('---------------------------')
    print(f"Total prompts: {total_prompt}")
    print(f"Total Generation: {total_gen}")
    print(f"Throughput per {1/RATIO} sec: {throughput}")
    print(f"Total clocks: {current}")
    print(f"Total latency: {total_latency}")
    print(f"Total throughput: prompt: {total_prompt/total_latency} generation: {total_gen/total_latency}")
    print('---------------------------')
    orca_time = round(scheduler.orca*1000, 3)
    vllm_time = round(scheduler.vllm*1000, 3)
    astra_time = round(astra_time, 3)
    graph_time = round(graph_time, 3)
    total_time = round((end-start)*1000, 3)
    compile_time = round(compile_time/1000000, 3)
    simulate_time = round(simulate_time/1000000, 3)
    pim_time = round(pim_time*1000, 3)
    subbatch_time = round(subbatch_time*1000, 3)
    print('---------------------------')
    print(f"Total compile time: {compile_time}")
    print(f"Total simulate time: {simulate_time}")
    print(f"Total graph time: {graph_time}")
    print(f"Total astra time: {astra_time}")
    print(f"Total scheduler time: {round(total_time - compile_time - simulate_time - graph_time - astra_time - pim_time,3)}")
    if scheduling == 'orca':
        print(f"Total ORCA time: {orca_time}")
    if kv_manage == 'vllm':
        print(f"Total vLLM time: {vllm_time}")
    if pim_type != None:
        print(f"Total pim time: {pim_time}")
    if sub_batch:
        print(f"Total sub-batch interleaving time: {subbatch_time}")
    print(f"Total simulation time: {total_time}")



if __name__ == "__main__":
    main()