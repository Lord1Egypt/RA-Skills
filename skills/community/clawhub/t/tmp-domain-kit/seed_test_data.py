"""
录入测试数据到知识库
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from storage.knowledge_store import KnowledgeStore
from utils.id_generator import generate_entity_id, generate_relation_id

store = KnowledgeStore(str(Path(__file__).parent / "storage"))

# 1. PLC 实体
plc_entity = {
    "model": "AM600",
    "cpu_type": "ARM Cortex-A9",
    "memory_limit": 512,
    "io_capacity": 256,
    "supported_languages": ["ST", "LD", "FBD"],
    "program_size_limit": 500
}
plc_id = generate_entity_id("PLC", plc_entity, "docs/AM600_manual_v2.1.pdf")
store.add_entity(plc_id, "PLC", plc_entity,
    provenance={"source_type": "document", "source_path": "docs/AM600_manual_v2.1.pdf",
                "extracted_at": "2026-07-12T10:30:00Z", "confidence": 0.98},
    tags=["AM600", "PLC", "硬件参数"])

# 2. 约束规则
constraint_entity = {
    "rule": "AM600 程序编译后大小不得超过 500KB",
    "scope": "所有 AM600 项目",
    "severity": "critical",
    "rationale": "AM600 用户程序区限制为 512KB，需预留 12KB 用于系统变量"
}
cst_id = generate_entity_id("Constraint", constraint_entity, "docs/team_rules_2025.xlsx")
store.add_entity(cst_id, "Constraint", constraint_entity,
    provenance={"source_type": "manual", "source_path": "docs/team_rules_2025.xlsx",
                "extracted_at": "2026-07-12T08:00:00Z", "confidence": 0.9},
    tags=["AM600", "编译约束", "内存限制"])

# 3. 代码模板
template_entity = {
    "name": "AM600_输送带启停控制_ST",
    "language": "ST",
    "content": "PROGRAM ConveyorControl\nVAR\n  StartBtn: BOOL;\n  StopBtn: BOOL;\n  MotorRun: BOOL;\nEND_VAR\n\nIF StartBtn AND NOT StopBtn THEN\n  MotorRun := TRUE;\nELSIF StopBtn THEN\n  MotorRun := FALSE;\nEND_IF",
    "parameters": ["StartBtn (BOOL)", "StopBtn (BOOL)"],
    "description": "AM600 输送带基础启停控制，带安全互锁"
}
tpl_id = generate_entity_id("CodeTemplate", template_entity, "templates/conveyor_base_v3.st")
store.add_entity(tpl_id, "CodeTemplate", template_entity,
    provenance={"source_type": "code", "source_path": "templates/conveyor_base_v3.st",
                "extracted_at": "2026-07-12T09:00:00Z", "confidence": 1.0},
    tags=["AM600", "ST", "输送带", "启停控制", "模板"])

# 4. 最佳实践
bp_entity = {
    "title": "AM600 输送带速度闭环调参经验",
    "content": "积分时间建议从 0.5s 起步，避免过冲。比例增益先从 1.0 开始，逐步增大。",
    "tags": ["调参", "速度闭环"],
    "examples": ["输送带速度控制", "张力控制"]
}
bp_id = generate_entity_id("BestPractice", bp_entity, "docs/team_rules_2025.xlsx")
store.add_entity(bp_id, "BestPractice", bp_entity,
    provenance={"source_type": "manual", "source_path": "docs/team_rules_2025.xlsx",
                "extracted_at": "2026-07-12T08:00:00Z", "confidence": 0.85},
    tags=["AM600", "调参", "速度闭环", "最佳实践"])

# 5. 关系：CodeTemplate depends_on PLC
rel_id = generate_relation_id(tpl_id, plc_id, "depends_on")
store.add_relation(rel_id, tpl_id, plc_id, "depends_on", confidence=1.0,
    provenance={"source_path": "templates/conveyor_base_v3.st"})

# 6. 关系：Constraint applies_to PLC
rel_id2 = generate_relation_id(cst_id, plc_id, "applies_to")
store.add_relation(rel_id2, cst_id, plc_id, "applies_to", confidence=1.0,
    provenance={"source_path": "docs/team_rules_2025.xlsx"})

print(f"录入完成：4 个实体 + 2 条关系")
print(f"  PLC: {plc_id[:16]}...")
print(f"  Constraint: {cst_id[:16]}...")
print(f"  CodeTemplate: {tpl_id[:16]}...")
print(f"  BestPractice: {bp_id[:16]}...")
