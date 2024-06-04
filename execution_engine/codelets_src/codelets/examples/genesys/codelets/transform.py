from codelets.adl.graph import ArchitectureNode
from codelets.templates.codelet_template import CodeletTemplate
from codelets.examples.genesys import OP_DTYPES, DTYPE_MAP
from . import add_simd_constraint, add_flex_simd_constraints


def tensor_reshape4d2d(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("tensor_reshape4d2d") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[0].shape[3])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
    return cdlt

def tensor_reshape3d2d(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("tensor_reshape3d2d") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
    return cdlt

def tensor_reshape2d3d(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("tensor_reshape2d3d") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.outputs[0].shape[2])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C, H], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
    return cdlt


def tensor_reshape4d3d(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("tensor_reshape4d3d") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[0].shape[3])

        ON = cdlt.dummy_op("ON", cdlt.node.outputs[0].shape[0])
        OC = cdlt.dummy_op("OC", cdlt.node.outputs[0].shape[1])
        OH = cdlt.dummy_op("OH", cdlt.node.outputs[0].shape[2])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [ON, OC, OH], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
    return cdlt


def tensor_reshape3d4d(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("tensor_reshape3d4d") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])

        N1 = cdlt.dummy_op("N1", cdlt.node.outputs[0].shape[0])
        C1 = cdlt.dummy_op("C1", cdlt.node.outputs[0].shape[1])
        H1 = cdlt.dummy_op("H1", cdlt.node.outputs[0].shape[2])
        W1 = cdlt.dummy_op("W1", cdlt.node.outputs[0].shape[3])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N1, C1, H1, W1], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
    return cdlt

def tensor_squeeze(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("tensor_squeeze") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[0].shape[3])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
    return cdlt


def tensor_resize(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    # TODO: Right now, shapes are fixed. Need to enable different dimension combinations
    with CodeletTemplate("resize") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H1 = cdlt.dummy_op("H1", cdlt.node.inputs[0].shape[2])
        W1 = cdlt.dummy_op("W1", cdlt.node.inputs[0].shape[3])

        H2 = cdlt.dummy_op("H2", cdlt.node.outputs[0].shape[2])
        W2 = cdlt.dummy_op("W2", cdlt.node.outputs[0].shape[3])
        DIMS = cdlt.dummy_op('DIMS', cdlt.node.inputs[1].shape[0])

        op1 = cdlt.create_operand_template("op1", OP_DTYPES, [N, C, H1, W1], default_dtype=acc_dtype)
        scales = cdlt.create_operand_template("scale", OP_DTYPES, [DIMS], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C, H2, W2], default_dtype=acc_dtype)
        cdlt.set_inputs([op1, scales])
        cdlt.set_outputs([out])
    return cdlt

def tensor_pad(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    with CodeletTemplate("tensor_pad") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[0].shape[3])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
        cdlt.configure("end", "SIMD")
    return cdlt


def tensor_flip(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    with CodeletTemplate("tensor_flip") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[0].shape[3])

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
        cdlt.configure("end", "SIMD")

    return cdlt


def concat(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    with CodeletTemplate("concat") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        IC1 = cdlt.dummy_op("IC1", cdlt.node.inputs[0].shape[1])
        IC2 = cdlt.dummy_op("IC2", cdlt.node.inputs[1].shape[1])
        OC = cdlt.dummy_op("OC", cdlt.node.outputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[0].shape[3])

        op1 = cdlt.create_operand_template("op1", OP_DTYPES, [N, IC1, H, W], default_dtype=acc_dtype)
        op2 = cdlt.create_operand_template("op2", OP_DTYPES, [N, IC2, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, OC, H, W], default_dtype=acc_dtype)
        cdlt.set_inputs([op1, op2])
        cdlt.set_outputs([out])

    return cdlt

def concat3d(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    with CodeletTemplate("concat3d") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        IC1 = cdlt.dummy_op("IC1", cdlt.node.inputs[0].shape[1])
        IC2 = cdlt.dummy_op("IC2", cdlt.node.inputs[1].shape[1])
        OC = cdlt.dummy_op("OC", cdlt.node.outputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])

        op1 = cdlt.create_operand_template("op1", OP_DTYPES, [N, IC1, H], default_dtype=acc_dtype)
        op2 = cdlt.create_operand_template("op2", OP_DTYPES, [N, IC2, H], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, OC, H], default_dtype=acc_dtype)
        cdlt.set_inputs([op1, op2])
        cdlt.set_outputs([out])

    return cdlt

def split(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    with CodeletTemplate("split") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[0].shape[2])

        C1 = cdlt.dummy_op("C1", cdlt.node.outputs[0].shape[1])
        H1 = cdlt.dummy_op("H1", cdlt.node.outputs[0].shape[2])

        op1 = cdlt.create_operand_template("op1", OP_DTYPES, [N, C, H], default_dtype=acc_dtype)
        out1 = cdlt.create_operand_template("out1", OP_DTYPES, [N, C1, H1], default_dtype=acc_dtype)
        out2 = cdlt.create_operand_template("out2", OP_DTYPES, [N, C1, H1], default_dtype=acc_dtype)
        out3 = cdlt.create_operand_template("out3", OP_DTYPES, [N, C1, H1], default_dtype=acc_dtype)
        cdlt.set_inputs([op1])
        cdlt.set_outputs([out1, out2, out3])

    return cdlt

def where(hag: ArchitectureNode):
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['ACC_WIDTH']}"]
    with CodeletTemplate("elem_where") as cdlt:

        N = cdlt.dummy_op("N", cdlt.node.inputs[1].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.inputs[1].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.inputs[1].shape[2])
        W = cdlt.dummy_op("W", cdlt.node.inputs[1].shape[3])
        ONE = cdlt.dummy_op("ONE", cdlt.node.inputs[0].shape[1])


        cond = cdlt.create_operand_template("cond", OP_DTYPES, [N, ONE, H, W], default_dtype=acc_dtype)
        x = cdlt.create_operand_template("x", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C, H, W], default_dtype=acc_dtype)

        cdlt.set_inputs([x, cond])
        cdlt.set_outputs([out])

    return cdlt

# TODO: Emit a warning when encountering this layer, as it is unique to the ViT model
def elem_gather(hag: ArchitectureNode):
    acc_dtype_name = f"FXP{hag.meta_cfg['ACC_WIDTH']}"
    inpt_dtype = DTYPE_MAP[f"FXP{hag.meta_cfg['DATA_WIDTH']}"]
    acc_dtype = DTYPE_MAP[acc_dtype_name]
    # # TODO: Add option to create operand
    # THIS ASSUMES THE AXIS IS THE OUTERMOST AXIS. IN THE FUTURE, NEED TO ADAPT TO DIFFERENT AXES
    with CodeletTemplate("elem_gather") as cdlt:
        N = cdlt.dummy_op("N", cdlt.node.outputs[0].shape[0])
        C = cdlt.dummy_op("C", cdlt.node.outputs[0].shape[1])
        H = cdlt.dummy_op("H", cdlt.node.outputs[0].shape[2])
        ONE = cdlt.dummy_op("ONE", 1)

        data = cdlt.create_operand_template("data", OP_DTYPES, [N, C], default_dtype=acc_dtype)
        indices = cdlt.dummy_op("indices", cdlt.node.indices, dtype=acc_dtype_name)
        out = cdlt.create_operand_template("out", OP_DTYPES, [N, C, H], default_dtype=acc_dtype)

        cdlt.set_inputs([data])
        cdlt.set_outputs([out])
        # Change this to be the reciprocal as a FXP value

        # axis = cdlt.dummy_op("axis", cdlt.node.kwargs['axes'][0])
        SIMD_SIZE = cdlt.dummy_op("SIMD_SIZE", cdlt.hag.all_subgraph_nodes['SIMD'].dimensions[0])

        cdlt.configure("start", "SIMD")

        with cdlt.loop(H) as h:
            with cdlt.loop(C) as c:
                with cdlt.loop(N) as n:
                    cdlt.transfer(data, ["DRAM", "VMEM1"])
                    out.set_write_destination("VMEM2")
                    cdlt.compute("MOVE", [data[n, c]], [out[n, c, h]], target="SIMD")
                    cdlt.transfer(out, ["VMEM2", "DRAM"])
        cdlt.configure("end", "SIMD")


    cdlt = add_simd_constraint(hag, cdlt, "H")

    return cdlt

def load_transform_cdlts(cfg):

    TRANSFORM_CDLTS = {
        'tensor_reshape4d2d': tensor_reshape4d2d,
        'tensor_reshape4d3d': tensor_reshape4d3d,
        'tensor_reshape3d4d': tensor_reshape3d4d,
        'tensor_reshape3d2d': tensor_reshape3d2d,
        'tensor_reshape2d3d': tensor_reshape2d3d,
        'split': split,
        'tensor_squeeze': tensor_squeeze,
        'concat': concat,
        'concat3d': concat3d,
        'resize': tensor_resize,
        'elem_where': where,
        'elem_gather': elem_gather,
        # 'tensor_flip': tensor_flip,
        # 'tensor_pad': tensor_pad,
    }
    return TRANSFORM_CDLTS
