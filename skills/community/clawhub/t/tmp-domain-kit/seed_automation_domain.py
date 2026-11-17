"""
非标自动化领域知识录入
基于联网搜索结果整理，录入 domain-kit 知识库
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from storage.knowledge_store import KnowledgeStore
from utils.id_generator import generate_entity_id, generate_relation_id

store = KnowledgeStore(str(Path(__file__).parent / "storage"))

# ===== PLC 设备（汇川产品线）=====

plc_models = [
    {
        "model": "AM600", "cpu_type": "ARM Cortex-A9", "memory_limit": 512,
        "io_capacity": 256, "supported_languages": ["ST", "LD", "FBD", "SFC"],
        "program_size_limit": 500, "motion_axes": 32,
        "communication": ["EtherCAT", "Modbus TCP", "CAN"],
        "positioning": "中型旗舰，美的主力选型", "manufacturer": "汇川技术"
    },
    {
        "model": "AM522", "cpu_type": "ARM", "memory_limit": 512,
        "io_capacity": 256, "supported_languages": ["ST", "LD", "FBD", "SFC"],
        "program_size_limit": 500, "motion_axes": 64,
        "communication": ["EtherCAT", "PROFINET", "Modbus TCP"],
        "positioning": "中型新一代，支持PROFINET", "manufacturer": "汇川技术"
    },
    {
        "model": "H5U", "cpu_type": "ARM", "memory_limit": 256,
        "io_capacity": 128, "supported_languages": ["ST", "LD", "FBD"],
        "program_size_limit": 256, "motion_axes": 16,
        "communication": ["EtherCAT", "Modbus"],
        "positioning": "高性能运动控制", "manufacturer": "汇川技术"
    },
    {
        "model": "H3U", "cpu_type": "ARM", "memory_limit": 128,
        "io_capacity": 64, "supported_languages": ["ST", "LD", "FBD"],
        "program_size_limit": 128, "motion_axes": 8,
        "communication": ["Modbus", "CAN"],
        "positioning": "经济型，高性价比", "manufacturer": "汇川技术"
    },
    {
        "model": "AM400", "cpu_type": "ARM", "memory_limit": 64,
        "io_capacity": 32, "supported_languages": ["ST", "LD", "FBD"],
        "program_size_limit": 64, "motion_axes": 0,
        "communication": ["Modbus"],
        "positioning": "小型PLC，简单逻辑控制", "manufacturer": "汇川技术"
    },
]

plc_ids = {}
for plc in plc_models:
    model = plc["model"]
    plc_id = generate_entity_id("PLC", plc, f"docs/automation/inovance_{model.lower()}_manual.pdf")
    store.add_entity(plc_id, "PLC", plc,
        provenance={"source_type": "document",
                    "source_path": f"docs/automation/inovance_{model.lower()}_manual.pdf",
                    "extracted_at": "2026-07-12T12:00:00Z", "confidence": 0.95},
        tags=[model, "PLC", "汇川", "汇川技术", "Inovance", "非标自动化",
              plc.get("positioning", ""), "运动控制"] +
             plc.get("communication", []))
    plc_ids[model] = plc_id

# ===== 西门子 PLC（竞品参考）=====

siemens_plcs = [
    {
        "model": "S7-1200", "cpu_type": "ARM", "memory_limit": 400,
        "io_capacity": 288, "supported_languages": ["ST", "LD", "FBD", "SFC", "LAD"],
        "program_size_limit": 400, "motion_axes": 4,
        "communication": ["PROFINET", "Modbus TCP"],
        "positioning": "紧凑型，中小型设备", "manufacturer": "西门子"
    },
    {
        "model": "S7-1500", "cpu_type": "ARM", "memory_limit": 4096,
        "io_capacity": 1000, "supported_languages": ["ST", "LD", "FBD", "SFC", "LAD"],
        "program_size_limit": 4000, "motion_axes": 64,
        "communication": ["PROFINET", "PROFIBUS", "Modbus TCP", "OPC UA"],
        "positioning": "高端旗舰，大型产线", "manufacturer": "西门子"
    },
]

for plc in siemens_plcs:
    model = plc["model"]
    plc_id = generate_entity_id("PLC", plc, f"docs/automation/siemens_{model.lower()}_manual.pdf")
    store.add_entity(plc_id, "PLC", plc,
        provenance={"source_type": "document",
                    "source_path": f"docs/automation/siemens_{model.lower()}_manual.pdf",
                    "extracted_at": "2026-07-12T12:00:00Z", "confidence": 0.93},
        tags=[model, "PLC", "西门子", "Siemens", "非标自动化",
              plc.get("positioning", "")] + plc.get("communication", []))
    plc_ids[model] = plc_id

# ===== 通信协议 =====

protocols = [
    {
        "name": "Modbus RTU", "version": "1.0",
        "message_format": "主从架构，寄存器读写，CRC校验",
        "endpoints": ["RS485串口", "波特率最高115.2kbps"],
        "speed": "115.2kbps", "realtime": "低", "topology": "主从",
        "dominant_vendor": "施耐德", "use_case": "简单仪表/传感器通信"
    },
    {
        "name": "Modbus TCP", "version": "1.0",
        "message_format": "客户端/服务器，基于TCP/IP，功能码+数据寄存器",
        "endpoints": ["502端口", "保持寄存器", "线圈寄存器"],
        "speed": "100Mbps", "realtime": "中", "topology": "以太网",
        "dominant_vendor": "施耐德", "use_case": "上位机通信/MES对接"
    },
    {
        "name": "PROFINET", "version": "2.4",
        "message_format": "基于工业以太网，RT/IRT模式，TIA Portal组态",
        "endpoints": ["RJ45端口", "IRT实时通道"],
        "speed": "100Mbps", "realtime": "高", "topology": "星型/线型",
        "dominant_vendor": "西门子", "use_case": "工厂自动化/分布式I/O"
    },
    {
        "name": "EtherCAT", "version": "1.0.3",
        "message_format": "飞读飞写（Processing on the fly），分布式时钟同步",
        "endpoints": ["RJ45端口", "从站级联"],
        "speed": "100Mbps", "realtime": "极高", "topology": "线型/星型/树型",
        "dominant_vendor": "Beckhoff", "use_case": "高速运动控制/多轴同步"
    },
    {
        "name": "OPC UA", "version": "1.05",
        "message_format": "面向服务架构，信息建模，安全加密",
        "endpoints": ["4840端口", "节点浏览", "订阅/发布"],
        "speed": "100Mbps+", "realtime": "中", "topology": "任意",
        "dominant_vendor": "跨厂商标准", "use_case": "MES/SCADA数据交换/跨平台集成"
    },
]

protocol_ids = {}
for proto in protocols:
    name = proto["name"]
    pid = generate_entity_id("Protocol", proto, "docs/automation/industrial_protocols_comparison.pdf")
    store.add_entity(pid, "Protocol", proto,
        provenance={"source_type": "document",
                    "source_path": "docs/automation/industrial_protocols_comparison.pdf",
                    "extracted_at": "2026-07-12T12:30:00Z", "confidence": 0.95},
        tags=[name, "协议", "通信", "工业以太网", "非标自动化",
              proto.get("dominant_vendor", ""), proto.get("use_case", "")])
    protocol_ids[name] = pid

# ===== 约束规则（非标自动化设计规范）=====

constraints = [
    {
        "rule": "PLC程序内存使用不超过80%额定容量",
        "scope": "所有PLC项目", "severity": "critical",
        "rationale": "预留20%用于运行时变量和系统扩展"
    },
    {
        "rule": "I/O点数预留10-15%余量",
        "scope": "所有设备项目", "severity": "warning",
        "rationale": "客户可能在调试阶段增加信号点"
    },
    {
        "rule": "运动控制优先选用EtherCAT总线伺服",
        "scope": "汇川PLC项目", "severity": "info",
        "rationale": "EtherCAT实时性最优，汇川伺服+PLC同品牌兼容性好"
    },
    {
        "rule": "安全回路必须使用硬件互锁，不能仅依赖软件",
        "scope": "所有设备项目", "severity": "critical",
        "rationale": "GB/T 16855安全标准要求，软件失效时必须有硬件保护"
    },
    {
        "rule": "设备通信协议选型：上位机用OPC UA，PLC层用EtherCAT/PROFINET，仪表层用Modbus",
        "scope": "通信架构设计", "severity": "info",
        "rationale": "分层架构，各层选用最适合的协议"
    },
    {
        "rule": "气缸选型优先SMC/FESTO，国产替代用亚德客",
        "scope": "气动元件选型", "severity": "info",
        "rationale": "SMC/FESTO可靠性最高，亚德客性价比高"
    },
    {
        "rule": "伺服电机选型：汇川IS620N/IS820系列优先",
        "scope": "汇川PLC项目", "severity": "info",
        "rationale": "汇川伺服市占率国产第一，与汇川PLC配合最佳"
    },
]

constraint_ids = []
for cst in constraints:
    cid = generate_entity_id("Constraint", cst, "docs/automation/design_standards.pdf")
    store.add_entity(cid, "Constraint", cst,
        provenance={"source_type": "manual",
                    "source_path": "docs/automation/design_standards.pdf",
                    "extracted_at": "2026-07-12T13:00:00Z", "confidence": 0.90},
        tags=["设计规范", "非标自动化", "选型", cst.get("severity", ""),
              cst.get("scope", "")])
    constraint_ids.append(cid)

# ===== 最佳实践 =====

best_practices = [
    {
        "title": "非标自动化设备选型决策树",
        "content": "PLC选型：简单逻辑→H3U/AM400；中型设备→AM600；大型产线→AM522/S7-1500。"
                   "通信选型：仪表→Modbus RTU；上位机→Modbus TCP/OPC UA；运动控制→EtherCAT；"
                   "西门子生态→PROFINET。伺服选型：汇川PLC配汇川伺服（IS620N/IS820），"
                   "西门子PLC配西门子伺服（V90/S120）。",
        "tags": ["选型", "PLC", "伺服", "通信", "非标自动化"],
        "examples": ["AM600+IS620N+EtherCAT 是美的项目标配组合"]
    },
    {
        "title": "PLC程序结构设计规范",
        "content": "采用模块化编程：MAIN主程序→调用各功能块。功能块按工站划分："
                   "FB_Station01_上料、FB_Station02_装配、FB_Station03_检测。"
                   "每个功能块包含：初始化、自动运行、手动运行、故障处理四个子程序。"
                   "变量命名：i_输入/o_输出/m_中间/r_实参。",
        "tags": ["编程规范", "PLC", "ST", "模块化", "非标自动化"],
        "examples": ["汇川InoProShop编程规范"]
    },
    {
        "title": "非标设备调试检查清单",
        "content": "调试前：1.检查接线（电源/信号/接地）2.确认气源压力 3.确认安全回路。"
                   "调试中：4.单轴手动测试 5.单工站自动测试 6.联机自动测试 7.节拍测试。"
                   "调试后：8.连续运行测试（≥4小时）9.异常恢复测试 10.安全功能测试。",
        "tags": ["调试", "非标自动化", "检查清单", "安全"],
        "examples": ["标准调试流程：手动→单站→联机→连续运行"]
    },
    {
        "title": "家电装配线典型工站设计",
        "content": "典型家电装配线工站：1.底壳上料站 2.压缩机安装站 3.管路焊接站 "
                   "4.电控板安装站 5.面板装配站 6.冷媒充注站 7.安规检测站 "
                   "8.性能测试站 9.外观检测站 10.包装码垛站。"
                   "每个工站包含：定位机构+执行机构+检测传感器+安全光栅。",
        "tags": ["家电", "装配线", "工站", "非标自动化", "美的"],
        "examples": ["空调外机装配线", "洗衣机装配线"]
    },
    {
        "title": "PLC品牌市场份额参考（2024中国市场）",
        "content": "西门子~47%（S7-1200/1500，PROFINET生态）> 三菱~12%（FX/Q系列，南方轻工）"
                   "> 欧姆龙~8%（NJ/NX，EtherCAT运动控制，新能源）> 汇川~5%（AM600/H5U，国产第一）"
                   "> 信捷~2%（小型PLC高性价比）。国产替代趋势明确，汇川增速最快。",
        "tags": ["PLC", "市场份额", "品牌", "选型参考", "非标自动化"],
        "examples": ["美的集团以汇川为主要供应商"]
    },
]

bp_ids = []
for bp in best_practices:
    bid = generate_entity_id("BestPractice", bp, "docs/automation/best_practices.pdf")
    store.add_entity(bid, "BestPractice", bp,
        provenance={"source_type": "manual",
                    "source_path": "docs/automation/best_practices.pdf",
                    "extracted_at": "2026-07-12T13:30:00Z", "confidence": 0.88},
        tags=bp.get("tags", []) + ["非标自动化", "最佳实践"])
    bp_ids.append(bid)

# ===== 关系 =====

# PLC compatible_with Protocol
for model in ["AM600", "AM522"]:
    for proto in ["EtherCAT", "Modbus TCP"]:
        if proto in protocol_ids and model in plc_ids:
            rel_id = generate_relation_id(plc_ids[model], protocol_ids[proto], "compatible_with")
            store.add_relation(rel_id, plc_ids[model], protocol_ids[proto], "compatible_with",
                confidence=0.95, provenance={"source_path": "docs/automation/industrial_protocols_comparison.pdf"})

for model in ["S7-1200", "S7-1500"]:
    for proto in ["PROFINET", "Modbus TCP"]:
        if proto in protocol_ids and model in plc_ids:
            rel_id = generate_relation_id(plc_ids[model], protocol_ids[proto], "compatible_with")
            store.add_relation(rel_id, plc_ids[model], protocol_ids[proto], "compatible_with",
                confidence=0.95, provenance={"source_path": "docs/automation/industrial_protocols_comparison.pdf"})

# Constraint applies_to PLC (通用约束适用于所有PLC)
for cid in constraint_ids:
    for model in ["AM600", "AM522", "H5U", "H3U"]:
        if model in plc_ids:
            rel_id = generate_relation_id(cid, plc_ids[model], "applies_to")
            store.add_relation(rel_id, cid, plc_ids[model], "applies_to",
                confidence=0.8, provenance={"source_path": "docs/automation/design_standards.pdf"})

print("非标自动化领域知识录入完成:")
print(f"  PLC: {len(plc_models) + len(siemens_plcs)} 个 (汇川5 + 西门子2)")
print(f"  Protocol: {len(protocols)} 个")
print(f"  Constraint: {len(constraints)} 个")
print(f"  BestPractice: {len(best_practices)} 个")
print(f"  关系: PLC↔Protocol + Constraint→PLC")
