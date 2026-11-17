"""
WCS 方向测试数据录入
录入 WCS 设备、调度规则、通信协议及相关关系
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from storage.knowledge_store import KnowledgeStore
from utils.id_generator import generate_entity_id, generate_relation_id

store = KnowledgeStore(str(Path(__file__).parent / "storage"))

# ===== WCS 设备 =====

# 1. 堆垛机
stacker = {
    "device_type": "堆垛机",
    "model": "SC-2000",
    "capacity": 1500,
    "speed": 3.0,
    "communication": ["Modbus TCP", "OPC UA"]
}
stacker_id = generate_entity_id("WCS_Device", stacker, "docs/wcs/stacker_sc2000.pdf")
store.add_entity(stacker_id, "WCS_Device", stacker,
    provenance={"source_type": "document", "source_path": "docs/wcs/stacker_sc2000.pdf",
                "extracted_at": "2026-07-12T10:00:00Z", "confidence": 0.95},
    tags=["SC-2000", "堆垛机", "WCS"])

# 2. 输送机
conveyor = {
    "device_type": "输送机",
    "model": "CV-500",
    "capacity": 500,
    "speed": 1.5,
    "communication": ["Modbus TCP", "Profinet"]
}
conveyor_id = generate_entity_id("WCS_Device", conveyor, "docs/wcs/conveyor_cv500.pdf")
store.add_entity(conveyor_id, "WCS_Device", conveyor,
    provenance={"source_type": "document", "source_path": "docs/wcs/conveyor_cv500.pdf",
                "extracted_at": "2026-07-12T10:00:00Z", "confidence": 0.95},
    tags=["CV-500", "输送机", "WCS"])

# 3. AGV
agv = {
    "device_type": "AGV",
    "model": "AGV-L200",
    "capacity": 200,
    "speed": 2.0,
    "communication": ["WiFi", "OPC UA"]
}
agv_id = generate_entity_id("WCS_Device", agv, "docs/wcs/agv_l200.pdf")
store.add_entity(agv_id, "WCS_Device", agv,
    provenance={"source_type": "document", "source_path": "docs/wcs/agv_l200.pdf",
                "extracted_at": "2026-07-12T10:00:00Z", "confidence": 0.92},
    tags=["AGV-L200", "AGV", "WCS"])

# 4. 分拣机
sorter = {
    "device_type": "分拣机",
    "model": "ST-3000",
    "capacity": 800,
    "speed": 4.0,
    "communication": ["EtherCAT", "Modbus TCP"]
}
sorter_id = generate_entity_id("WCS_Device", sorter, "docs/wcs/sorter_st3000.pdf")
store.add_entity(sorter_id, "WCS_Device", sorter,
    provenance={"source_type": "document", "source_path": "docs/wcs/sorter_st3000.pdf",
                "extracted_at": "2026-07-12T10:00:00Z", "confidence": 0.90},
    tags=["ST-3000", "分拣机", "WCS"])

# ===== 调度规则 =====

# 1. FIFO 调度
fifo_rule = {
    "name": "FIFO先进先出调度",
    "algorithm": "按入库时间排序，先入先出",
    "priority": "FIFO",
    "constraints": ["适用于标准品存储", "不适用于优先级差异大的场景"]
}
fifo_id = generate_entity_id("ScheduleRule", fifo_rule, "docs/wcs/scheduling_rules.xlsx")
store.add_entity(fifo_id, "ScheduleRule", fifo_rule,
    provenance={"source_type": "document", "source_path": "docs/wcs/scheduling_rules.xlsx",
                "extracted_at": "2026-07-12T10:30:00Z", "confidence": 0.90},
    tags=["FIFO", "调度", "WCS"])

# 2. 优先级调度
priority_rule = {
    "name": "优先级加权调度",
    "algorithm": "按订单优先级+库位距离加权排序",
    "priority": "优先级",
    "constraints": ["优先级分3级: 紧急/普通/低优", "距离权重系数0.3"]
}
priority_id = generate_entity_id("ScheduleRule", priority_rule, "docs/wcs/scheduling_rules.xlsx")
store.add_entity(priority_id, "ScheduleRule", priority_rule,
    provenance={"source_type": "document", "source_path": "docs/wcs/scheduling_rules.xlsx",
                "extracted_at": "2026-07-12T10:30:00Z", "confidence": 0.88},
    tags=["优先级", "调度", "WCS"])

# 3. 动态调度
dynamic_rule = {
    "name": "动态负载均衡调度",
    "algorithm": "实时监控设备负载，动态分配任务到最空闲设备",
    "priority": "动态",
    "constraints": ["需要实时数据采集支持", "适用于多设备协同场景"]
}
dynamic_id = generate_entity_id("ScheduleRule", dynamic_rule, "docs/wcs/scheduling_rules.xlsx")
store.add_entity(dynamic_id, "ScheduleRule", dynamic_rule,
    provenance={"source_type": "document", "source_path": "docs/wcs/scheduling_rules.xlsx",
                "extracted_at": "2026-07-12T10:30:00Z", "confidence": 0.85},
    tags=["动态调度", "负载均衡", "WCS"])

# ===== 通信协议 =====

# 1. Modbus TCP
modbus = {
    "name": "Modbus TCP",
    "version": "1.0",
    "message_format": "请求/响应模式，功能码+数据寄存器",
    "endpoints": ["502端口", "保持寄存器", "线圈寄存器"]
}
modbus_id = generate_entity_id("Protocol", modbus, "docs/wcs/protocols.md")
store.add_entity(modbus_id, "Protocol", modbus,
    provenance={"source_type": "document", "source_path": "docs/wcs/protocols.md",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.98},
    tags=["Modbus TCP", "Modbus", "TCP", "协议", "通信", "WCS"])

# 2. OPC UA
opcua = {
    "name": "OPC UA",
    "version": "1.05",
    "message_format": "面向服务的架构，支持订阅/发布模式",
    "endpoints": ["4840端口", "节点浏览", "订阅通知"]
}
opcua_id = generate_entity_id("Protocol", opcua, "docs/wcs/protocols.md")
store.add_entity(opcua_id, "Protocol", opcua,
    provenance={"source_type": "document", "source_path": "docs/wcs/protocols.md",
                "extracted_at": "2026-07-12T11:00:00Z", "confidence": 0.98},
    tags=["OPC UA", "OPC", "协议", "通信", "WCS"])

# ===== 关系 =====

# ScheduleRule dispatches_to WCS_Device
for device_id in [stacker_id, conveyor_id, sorter_id]:
    rel_id = generate_relation_id(fifo_id, device_id, "dispatches_to")
    store.add_relation(rel_id, fifo_id, device_id, "dispatches_to", confidence=0.8,
        provenance={"source_path": "docs/wcs/scheduling_rules.xlsx"})

for device_id in [stacker_id, agv_id]:
    rel_id = generate_relation_id(priority_id, device_id, "dispatches_to")
    store.add_relation(rel_id, priority_id, device_id, "dispatches_to", confidence=0.8,
        provenance={"source_path": "docs/wcs/scheduling_rules.xlsx"})

for device_id in [conveyor_id, agv_id, sorter_id]:
    rel_id = generate_relation_id(dynamic_id, device_id, "dispatches_to")
    store.add_relation(rel_id, dynamic_id, device_id, "dispatches_to", confidence=0.7,
        provenance={"source_path": "docs/wcs/scheduling_rules.xlsx"})

# WCS_Device communicates_via Protocol
for device_id in [stacker_id, conveyor_id, sorter_id]:
    rel_id = generate_relation_id(device_id, modbus_id, "communicates_via")
    store.add_relation(rel_id, device_id, modbus_id, "communicates_via", confidence=0.9,
        provenance={"source_path": "docs/wcs/protocols.md"})

for device_id in [stacker_id, agv_id]:
    rel_id = generate_relation_id(device_id, opcua_id, "communicates_via")
    store.add_relation(rel_id, device_id, opcua_id, "communicates_via", confidence=0.9,
        provenance={"source_path": "docs/wcs/protocols.md"})

print("WCS 方向数据录入完成:")
print(f"  WCS_Device: 4 个 (SC-2000堆垛机, CV-500输送机, AGV-L200, ST-3000分拣机)")
print(f"  ScheduleRule: 3 个 (FIFO, 优先级, 动态)")
print(f"  Protocol: 2 个 (Modbus TCP, OPC UA)")
print(f"  关系: dispatches_to + communicates_via")
