# 虚拟世界核心引擎 - 基于Nohn蓝图架构 v2.0
# ============================================================
# 本文件 = 宪法聚合层（constitution.py）
# ------------------------------------------------------------
# 不再内嵌规则实现与审计实现，而是作为统一出口 re-export：
#   - 宪法规则层   -> constitution_rules.py
#       NOHN_LAW_AXIOMS, _safe_get, 构成公理一~五, 治理公理一~十
#   - 审计层       -> audit_engine.py
#       ResponsibilityAccount, AuditPlugin, CognitiveAuditEngine,
#       AuditConfigLoader, AuditReport, SecondPerspectiveAuditor
#
# 保持向后兼容：`from constitution import X` 对旧调用方（如
# virtual_world.py、compatibility_bridge.py）依然有效。
# 分层职责：
#   constitution_rules.py  = 规则（宪法本体）
#   audit_engine.py        = 裁判（第二视角审计引擎 v2.1）
#   system/                = 系统（区块链锚点/多智能体/运行时）
#   virtual_world.py       = 演示运行时客户端
# ============================================================

# --- 规则层：宪法本体（原始框架 + 构成公理 + 治理公理 + law 单一权威常量）---
from constitution_rules import (
    NOHN_LAW_AXIOMS,
    _safe_get,
    PRIMORDIAL_FRAMES,
    primordial_completeness,
    SpatialSubstrate,
    TemporalSubstrate,
    CausalClosure,
    ExistenceAxiom,
    GenesisCondition,
    ImmutableWorldRule,
    WorldCentralBrain,
    ConsensusEngine,
    SimulationEngine,
    MemoryVault,
    AestheticCompliance,
    IndependentWill,
    SoulAttestation,
    SoulLedger,
    MemoryInalienability,
    MemoryGuardian,
    WorldPerpetuity,
    HistoryLedger,
    SnapshotRegistry,
    MandatoryInteroperability,
    UniversalVocabulary,
    PhysicsBaseline,
    IdentityProtocol,
    EconomicBaseline,
    DecentralizationGovernance,
)

# --- 审计层：第二视角认知审计引擎 v2.1（元层裁判）---
from audit_engine import (
    ResponsibilityAccount,
    AuditConfigLoader,
    AuditPlugin,
    CognitiveAuditEngine,
    AuditReport,
    SecondPerspectiveAuditor,
)

# 显式导出清单：本聚合层对外提供的全部符号（向后兼容旧调用方）
__all__ = [
    "NOHN_LAW_AXIOMS",
    "_safe_get",
    "PRIMORDIAL_FRAMES",
    "primordial_completeness",
    "SpatialSubstrate",
    "TemporalSubstrate",
    "CausalClosure",
    "ExistenceAxiom",
    "GenesisCondition",
    "ImmutableWorldRule",
    "WorldCentralBrain",
    "ConsensusEngine",
    "SimulationEngine",
    "MemoryVault",
    "AestheticCompliance",
    "IndependentWill",
    "SoulAttestation",
    "SoulLedger",
    "MemoryInalienability",
    "MemoryGuardian",
    "WorldPerpetuity",
    "HistoryLedger",
    "SnapshotRegistry",
    "MandatoryInteroperability",
    "UniversalVocabulary",
    "PhysicsBaseline",
    "IdentityProtocol",
    "EconomicBaseline",
    "DecentralizationGovernance",
    "ResponsibilityAccount",
    "AuditConfigLoader",
    "AuditPlugin",
    "CognitiveAuditEngine",
    "AuditReport",
    "SecondPerspectiveAuditor",
]


# ============================================================
# 使用示例：如何用这份蓝图"审计"一个虚拟世界
# ============================================================

if __name__ == "__main__":
    # 演示：用第二视角认知审计引擎审计一个外部世界。
    # 这里用一个最简对象模拟一个未定义空间/时间/因果/存在/创世、
    # 也未接入 law 四维度的示例世界，因此应整体 FAILED。
    class FakeWorld:
        world_id = "ExampleWorld 2.0"

    auditor = SecondPerspectiveAuditor()
    report = auditor.audit_world(FakeWorld())

    # 输出审计结果（维度数由 AuditReport.FIELDS 派生；覆盖第负一层原始框架
    # + 第零层构成公理 + 治理层 + law 层）
    print(report.summary())
