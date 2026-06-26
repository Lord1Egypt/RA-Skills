"""硬件配置助手：提供常用PLC型号和模块的目录路径"""

class HardwareCatalog:
    """西门子硬件目录路径常量"""

    # S7-1200 CPU
    CPU_S7_1200 = {
        "CPU 1211C": "SIMATIC.PLC.S71200.CPU 1211C",
        "CPU 1212C": "SIMATIC.PLC.S71200.CPU 1212C",
        "CPU 1214C": "SIMATIC.PLC.S71200.CPU 1214C",
        "CPU 1215C": "SIMATIC.PLC.S71200.CPU 1215C",
        "CPU 1217C": "SIMATIC.PLC.S71200.CPU 1217C",
    }

    # S7-1500 CPU
    CPU_S7_1500 = {
        "CPU 1511-1 PN": "SIMATIC.PLC.S71500.CPU 1511-1 PN",
        "CPU 1513-1 PN": "SIMATIC.PLC.S71500.CPU 1513-1 PN",
        "CPU 1515-2 PN": "SIMATIC.PLC.S71500.CPU 1515-2 PN",
        "CPU 1516-3 PN/DP": "SIMATIC.PLC.S71500.CPU 1516-3 PN/DP",
        "CPU 1518-4 PN/DP": "SIMATIC.PLC.S71500.CPU 1518-4 PN/DP",
    }

    # 数字量输入模块
    DI_MODULES = {
        "DI 16x24VDC": "SIMATIC.DI.S71200.DI 16x24VDC",
        "DI 32x24VDC": "SIMATIC.DI.S71200.DI 32x24VDC",
        "DI 16x230VAC": "SIMATIC.DI.S71200.DI 16x230VAC",
    }

    # 数字量输出模块
    DO_MODULES = {
        "DO 16x24VDC": "SIMATIC.DO.S71200.DO 16x24VDC",
        "DO 32x24VDC": "SIMATIC.DO.S71200.DO 32x24VDC",
        "DO 16xRelay": "SIMATIC.DO.S71200.DO 16xRelay",
    }

    # 模拟量输入模块
    AI_MODULES = {
        "AI 4x13bit": "SIMATIC.AI.S71200.AI 4x13bit",
        "AI 8x13bit": "SIMATIC.AI.S71200.AI 8x13bit",
    }

    # 模拟量输出模块
    AO_MODULES = {
        "AO 2x14bit": "SIMATIC.AO.S71200.AO 2x14bit",
        "AO 4x14bit": "SIMATIC.AO.S71200.AO 4x14bit",
    }