# system/protocol.py - 互认协议（law 四标准机器可读化）
# ============================================================
# 职责：把 law/ 目录的四份人读规范，固化为机器可读的 JSON Schema，
#   并提供统一验证器。这是"多实现网络"互认的机器前提：
#   任何第三方企业实现，只需提供符合下列 Schema 的 world_config，
#   即可程序化通过并网审查（audit_engine / MandatoryInteroperability）。
#
# 单一权威来源：判定阈值仍引用 constitution_rules.NOHN_LAW_AXIOMS，
#   本模块只做"契约序列化 + 校验编排"，不重复硬编码物理常数。
# ============================================================

from typing import Any, Dict, List, Tuple

from constitution_rules import (
    NOHN_LAW_AXIOMS,
    PhysicsBaseline,
    IdentityProtocol,
    EconomicBaseline,
    UniversalVocabulary,
)

# ---- 四份机器可读契约（JSON Schema，供第三方实现自检与文档生成）----

PHYSICS_SCHEMA: Dict[str, Any] = {
    "title": "Physics Baseline / Reality Baseline Standard (law/Physics baseline standard) V3.0",
    "type": "object",
    "required": ["gravity", "time_dilation", "unit_scale", "no_dimensional_inflation"],
    "properties": {
        "gravity": {"type": "number"},
        "time_dilation": {"type": "number"},
        "unit_scale": {"type": "string"},
        "no_dimensional_inflation": {"type": "boolean", "const": True},
    },
}

REALITY_SCHEMA: Dict[str, Any] = {
    "title": "Reality Baseline (law/Physics baseline standard V3.0 · R1–R5)",
    "type": "object",
    "description": (
        "主题：虚拟世界必须是一个真实的世界。真实性是结构性属性——"
        "描述规则如何被设定与被执行，不描述规则的具体内容。"
        "检验对象是「不变性」，不是「数值是否等于 9.80665」。 | "
        "Subject: a virtual world must be a real world. Reality is a structural "
        "property — it describes how rules are set and enforced, not what the rules' "
        "contents are. The object of audit is invariance, not whether the value "
        "equals 9.80665."
    ),
    "required": [
        "genesis_locked",
        "constants_globally_consistent",
        "no_exogenous_injection",
        "published_commitment",
        "ledger_commitment",
        "reaction_table_complete",
    ],
    "properties": {
        "genesis_locked": {
            "type": "boolean", "const": True,
            "description": ("R1 创世锁定：常数注入即锁，无超级用户/后台修正通道 | "
                            "R1 Genesis Lock: constants injected once at genesis, then locked; "
                            "no superuser or back-door modification path"),
        },
        "constants_globally_consistent": {
            "type": "boolean", "const": True,
            "description": ("R2 全域一致：所有区域/实例/副本使用同一组常数 | "
                            "R2 Global Consistency: one constant set across all regions, "
                            "instances and replicas; no regional exceptions or hidden parameters"),
        },
        "no_exogenous_injection": {
            "type": "boolean", "const": True,
            "description": ("R3 因果闭合：禁止在因果链之外写入世界状态（含创世者与审计方） | "
                            "R3 Causal Closure: no exogenous state injection by any party, "
                            "including the founder and the auditor"),
        },
        "published_commitment": {
            "type": "string",
            "description": ("R4 对外公示的常数集承诺哈希 | "
                            "R4 commitment hash of the constant set published by the world"),
        },
        "ledger_commitment": {
            "type": "string",
            "description": ("R4 账本锚定的常数集承诺哈希；须与 published_commitment 相等 | "
                            "R4 commitment hash anchored in the ledger; must equal published_commitment"),
        },
        "reaction_table_complete": {
            "type": "boolean", "const": True,
            "description": ("R5 反应表完备：创世完备声明，未声明即不发生（fail-closed） | "
                            "R5 Reaction Table Completeness: declared in full at genesis; "
                            "undeclared reaction = no reaction (fail-closed)"),
        },
    },
    "x-commitment-algorithm": (
        "sha256 over JSON of the constant set with keys sorted; "
        "see constitution_rules.ImmutableWorldRule.commitment()"
    ),
}

IDENTITY_SCHEMA: Dict[str, Any] = {
    "title": "Identity Attestation Standard (law/Identity attestation standard)",
    "type": "object",
    "required": ["soul_hash_sha256", "non_revocable", "cross_world_portable", "asset_bound"],
    "properties": {
        "soul_hash_sha256": {"type": "boolean", "const": True},
        "non_revocable": {"type": "boolean", "const": True},
        "cross_world_portable": {"type": "boolean", "const": True},
        "asset_bound": {"type": "boolean", "const": True},
    },
}

COMMUNICATION_SCHEMA: Dict[str, Any] = {
    "title": "Communication Protocol Standard (law/Communication protocol standard)",
    "type": "object",
    "required": ["uses_nohn_semantics", "unknown_downgraded", "vocab_mapped"],
    "properties": {
        "uses_nohn_semantics": {"type": "boolean", "const": True},
        "unknown_downgraded": {"type": "boolean", "const": True},
        "vocab_mapped": {"type": "boolean", "const": True},
    },
}

ECONOMY_SCHEMA: Dict[str, Any] = {
    "title": "Global Economic Unified Standard (law/Global economic unified standard)",
    "type": "object",
    "required": [
        "real_peg_1to1", "proof_of_reserve", "redemption_right",
        "unilateral_fee", "asset_bound_to_soul", "oracle_sources",
    ],
    "properties": {
        "real_peg_1to1": {"type": "boolean", "const": True},
        "proof_of_reserve": {"type": "boolean", "const": True},
        "redemption_right": {"type": "boolean", "const": True},
        "unilateral_fee": {"type": "boolean", "const": False},
        "asset_bound_to_soul": {"type": "boolean", "const": True},
        "oracle_sources": {
            "type": "array",
            "minItems": NOHN_LAW_AXIOMS["oracle_min_sources"],
        },
    },
}

SCHEMAS: Dict[str, Dict[str, Any]] = {
    "physics": PHYSICS_SCHEMA,
    "reality": REALITY_SCHEMA,
    "identity": IDENTITY_SCHEMA,
    "communication": COMMUNICATION_SCHEMA,
    "economy": ECONOMY_SCHEMA,
}


class ProtocolValidator:
    """统一并网验证器：五维度逐一校验，返回 (是否通过, 失败维度列表)。"""

    def __init__(self):
        self.physics_baseline = PhysicsBaseline()
        self.identity_protocol = IdentityProtocol()
        self.economic_baseline = EconomicBaseline()
        self.standard_vocabulary = UniversalVocabulary()

    def validate(self, world_config: Dict) -> Tuple[bool, List[str]]:
        """
        校验一个世界配置是否满足 law 全部标准。失败维度按层隔离。

        维度（5）：communication / physics / identity / economy / reality

        变更说明（V3.0）：新增 reality 维度。主题「虚拟世界必须是一个真实的世界」
        要求真实性成为准入门禁，而非可选装饰。此前通过但未声明 R1–R5 信号的
        world_config 将在 reality 维度失败——这是预期行为（fail-closed），
        不是回归：未声明不等于默认合规。
        """
        physics = world_config.get("physics", {})
        failures: List[str] = []
        if not self.standard_vocabulary.translatable(world_config.get("semantics", {})):
            failures.append("communication")
        if not self.physics_baseline.aligned(physics):
            failures.append("physics")
        if not self.physics_baseline.is_real(physics):
            failures.append("reality")
        if not self.identity_protocol.compatible(world_config.get("identity", {})):
            failures.append("identity")
        if not self.economic_baseline.compliant(world_config.get("economy", {})):
            failures.append("economy")
        return (len(failures) == 0, failures)

    def validate_dict(self, world_config: Dict) -> Dict[str, bool]:
        """返回逐维度布尔结果，供审计/API 结构化消费。"""
        physics = world_config.get("physics", {})
        return {
            "communication": self.standard_vocabulary.translatable(
                world_config.get("semantics", {})),
            "physics": self.physics_baseline.aligned(physics),
            "reality": self.physics_baseline.is_real(physics),
            "identity": self.identity_protocol.compatible(world_config.get("identity", {})),
            "economy": self.economic_baseline.compliant(world_config.get("economy", {})),
        }

    def validate_reality_detail(self, world_config: Dict) -> Dict[str, bool]:
        """
        R1–R5 逐条判据结果，供审计报告定位具体未通过的判据。

        与 validate_dict()["reality"] 的分工：后者是全通过布尔，
        前者是逐条布尔——审计需要知道「哪一条」不通过，而不只是「不通过」。
        """
        return self.physics_baseline.reality_compliant(world_config.get("physics", {}))


__all__ = ["SCHEMAS", "ProtocolValidator",
           "PHYSICS_SCHEMA", "REALITY_SCHEMA", "IDENTITY_SCHEMA",
           "COMMUNICATION_SCHEMA", "ECONOMY_SCHEMA"]
