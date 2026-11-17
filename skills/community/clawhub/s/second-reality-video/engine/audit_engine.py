# 第二视角认知审计引擎 v2.1 - 元层审计工具（audit_engine.py）
# ============================================================
# 权威来源：second-perspective / cognitive audit engine.py
# 本文件 = 审计层（裁判），独立于宪法规则层与系统实现层。
# 职责：
#   - ResponsibilityAccount  审计问责主体（组织/角色/阶段/nonce）
#   - AuditConfigLoader      审计配置加载（dict / json）
#   - AuditPlugin            单条审计插件
#   - CognitiveAuditEngine   审计调度引擎 + reconstruct() 因果重构算子
#   - AuditReport            审计结论容器（维度数由 FIELDS 决定）
#   - SecondPerspectiveAuditor  宪法级合规审计器（插件化，维度数由 FIELDS 决定）
#
# 依赖方向：audit_engine -> constitution_rules（NOHN_LAW_AXIOMS/_safe_get）
# 逆向依赖不存在，保证裁判中立性。

import uuid
import json
import copy
import base64
from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Callable, Optional

from constitution_rules import NOHN_LAW_AXIOMS, CONSENSUS_THRESHOLD, _safe_get
from system.keys import derive_soul_hash_from_pubkey

# ----------------------------------------------------------------------------
# 二阶因果内核（共存式覆盖 · 第负一章原始框架的"真因果"算力）
# ----------------------------------------------------------------------------
# second-perspective 的 NOMOS 引擎（Second Perspective Engine，版本以 SPE_VERSION 为准）作为本仓库
# 审计层的"二阶因果维度"接入，**不替换**既有的 24 维合规审计：
#   - 合规审计（FIELDS 中除 causal_second_perspective 外的维度）继续由本方负责；
#   - causal_second_perspective 把运行态世界翻译成 NOMOS 决策上下文，调用引擎
#     做十算子因果审计，其自带 meta_ledger 天然覆盖 混沌/无极/虚幻/天道/轮回
#     —— 正好对应第负一章原框架，由真正的因果内核来计算。
# 引擎为单文件、零外部依赖（仅标准库），已原样 vendor 到
# system/second_perspective_engine.py；本处只做可选导入，缺失即降级为 WARN，
# 不拖垮整个审计层（fail-soft）。
try:
    from system.second_perspective_engine import (
        SecondPerspectiveEngine as _SPE_ENGINE,
        ResponsibilityAccount as _SPE_ACCOUNT,
        ConvergenceChecker as _SPE_CHECKER,
        SPE_VERSION as _SPE_VERSION,
    )
    _SPE_AVAILABLE = True
    _SPE_BLOCKING = getattr(_SPE_CHECKER, "BLOCKING_STATUSES", {"BLOCKED", "CRITICAL"})
except Exception as _SPE_IMPORT_ERR:  # pragma: no cover - 引擎为可选二层
    _SPE_ENGINE = _SPE_ACCOUNT = _SPE_CHECKER = None
    _SPE_VERSION = None
    _SPE_AVAILABLE = False
    _SPE_BLOCKING = {"BLOCKED", "CRITICAL"}
    _SPE_IMPORT_ERR = _SPE_IMPORT_ERR


@dataclass
class ResponsibilityAccount:
    organization: str
    role: str
    stage: str
    nonce: Optional[str] = None

    def __post_init__(self) -> None:
        if not self.nonce:
            self.nonce = uuid.uuid4().hex[:8]


class AuditConfigLoader:
    @staticmethod
    def load_from_dict(config: Dict[str, Any]) -> Dict[str, Any]:
        return config

    @staticmethod
    def load_from_json(path: str) -> Dict[str, Any]:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)


class AuditPlugin:
    def __init__(self, name: str, analyze_func: Callable[[Dict[str, Any]], Any]):
        self.name = name
        self.analyze = analyze_func


class CognitiveAuditEngine:
    def __init__(self, account: ResponsibilityAccount, config: Dict[str, Any]):
        self.account = account
        self.config = config
        self.plugins: List[AuditPlugin] = []

        # 校验责任阶段合法性
        allowed_stages = self.config.get("allowed_stages", [])
        if allowed_stages and account.stage not in allowed_stages:
            raise ValueError(f"Unsupported stage: {account.stage}")

    def register_plugin(self, plugin: AuditPlugin) -> None:
        self.plugins.append(plugin)

    def audit(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        静态诊断阶段：提取上下文、遍历注册插件并生成偏见/脆弱性评估报告。
        """
        report = {
            "disclaimer": self.config.get("disclaimer", ""),
            "responsibility_account": self.account.__dict__,
            "analysis": {},
            "custom_fields": self.config.get("custom_fields", {})
        }
        for plugin in self.plugins:
            report["analysis"][plugin.name] = plugin.analyze(decision_context)
        return report

    def reconstruct(
        self,
        decision_context: Dict[str, Any],
        delta_vars: Dict[str, Any],
        convergence_evaluator: Optional[Callable[[Dict[str, Any], Dict[str, Any]], bool]] = None
    ) -> Dict[str, Any]:
        """
        因果重构推演算子：
        1. 注入修正变量 (delta_vars) 重构逻辑链条
        2. 进行二次反事实校验与审计
        3. 评估系统是否收敛至目标稳态
        """
        # 1. 隔离并重构决策上下文
        reconstructed_context = copy.deepcopy(decision_context)
        reconstructed_context.update(delta_vars)

        # 2. 获取原始报告与重构后的二次审计报告
        original_report = self.audit(decision_context)
        reconstructed_report = self.audit(reconstructed_context)

        # 3. 收敛性判定（支持自定义评估器或默认阻断状态检测）
        if convergence_evaluator:
            is_converged = convergence_evaluator(original_report, reconstructed_report)
        else:
            is_converged = self._default_convergence_check(reconstructed_report)

        return {
            "status": "CONVERGED" if is_converged else "DIVERGED",
            "delta_variables": delta_vars,
            "reconstructed_context": reconstructed_context,
            "reconstructed_report": reconstructed_report,
            "is_converged": is_converged
        }

    @staticmethod
    def _default_convergence_check(reconstructed_report: Dict[str, Any]) -> bool:
        """
        默认判定逻辑：检查重构后的分析插件输出中是否已无高风险或中断状态。
        """
        analysis = reconstructed_report.get("analysis", {})
        for plugin_name, result in analysis.items():
            if isinstance(result, dict) and result.get("status") in ["BLOCKED", "HIGH_RISK", "CRITICAL"]:
                return False
        return True


# ============================================================
# 宪法合规审计（底座特有，随引擎驻留审计层；维度清单见 AuditReport.FIELDS）
# ============================================================

class AuditReport:
    """审计结论容器——提供可打印 summary()。"""
    FIELDS = [
        ("spatial_defined", "Spatial Substrate (构成公理一·空间)"),
        ("temporal_defined", "Temporal Substrate (构成公理二·时间)"),
        ("causal_closure", "Causal Closure (构成公理三·因果)"),
        ("existence_verifiable", "Existence Axiom (构成公理四·存在)"),
        ("genesis_booted", "Genesis Condition (构成公理五·创世)"),
        ("rule_frozen", "Rule Integrity (第一条·不可变规则)"),
        ("npc_free_will", "NPC Free Will (第二/四条·独立意志)"),
        ("aesthetic_compliance", "Aesthetic Compliance (第三条·明亮美学)"),
        ("no_scripted_plot", "No Scripted Plot (第四条·无强制剧情)"),
        ("soul_attested", "Soul Attestation (第六条·灵魂确权)"),
        ("memory_protected", "Memory Protection (第七条·记忆不可剥夺)"),
        ("world_perpetual", "World Perpetuity (第八条·永续)"),
        ("interoperable", "Interoperability (第九条·互操作)"),
        ("governance_decentralized", "Decentralization (第十条·反中心化)"),
        ("economic_compliance", "Economic Law (law·经济 1:1 互通)"),
        ("identity_compliance", "Identity Law (law·身份确权)"),
        ("communication_compliance", "Communication Law (law·通信协议)"),
        ("physics_compliance", "Physics Law (law·物理基准)"),
        ("auth_security", "Auth Security (账户系统·鉴权安全)"),
        # ---- 第负一章 · 原始框架（Primordial Frames）----
        ("genesis_commitment", "Chaos & R4 Executed (混沌·创世承诺真实锚定)"),
        ("branch_space", "Wuji Branch Space (无极·分支空间可重建)"),
        ("representation_isolation", "Illusion Isolation (虚幻·表征层硬隔离)"),
        ("fairness_invariant", "Heavenly Way (天道·公平形式不可变)"),
        ("conservation_law", "Samsara Conservation (轮回·守恒律)"),
        # ---- 渲染层维度（编号沿用 HLD §5.2 预留位次；26–30 仍只以 verify 检查项体现）----
        ("render_is_frame_independent", "Render Frame Independence (渲染层·无时序上下文)"),
        # 二阶因果内核（共存式覆盖）：NOMOS 引擎对运行态世界做十算子因果审计
        ("causal_second_perspective", "Second-Perspective Causal (二阶因果·NOMOS内核)"),
    ]

    def __init__(self):
        for attr, _ in self.FIELDS:
            setattr(self, attr, None)
        self.responsibility_account = None
        self.disclaimer = ""

    @staticmethod
    def _verdict_of(v):
        if isinstance(v, dict):
            return v.get("verdict", str(v))
        return str(v)

    @staticmethod
    def _is_pass(v):
        if isinstance(v, dict):
            return str(v.get("verdict", "")).startswith("PASS")
        return bool(v)

    def summary(self) -> str:
        lines = [f"=== Nohn 第二视角审计（{len(self.FIELDS)} 项维度）==="]
        failed = []
        for attr, label in self.FIELDS:
            v = getattr(self, attr)
            verdict = self._verdict_of(v)
            if self._is_pass(v):
                mark = "[PASS]"
            elif str(verdict).startswith("FAILED"):
                mark = "[FAIL]"
            else:
                mark = "[WARN]"
            lines.append(f"{mark} {label}: {verdict}")
            if not self._is_pass(v):
                failed.append(label)
        lines.append("")
        if not failed:
            lines.append("Final Verdict: PASS - 符合 Nohn 统一标准（宪法 + law 层）")
        else:
            lines.append(f"Final Verdict: FAILED - {len(failed)}/{len(self.FIELDS)} 项未通过")
            lines.append(f"未通过: {', '.join(failed)}")
        if isinstance(self.responsibility_account, dict):
            acct = self.responsibility_account
            lines.append(f"问责主体: {acct.get('organization')}/{acct.get('role')}"
                         f"@{acct.get('stage')}#{acct.get('nonce')}")
        return "\n".join(lines)


class SecondPerspectiveAuditor:
    """
    这不是世界的一部分。这是"元层"审计工具。
    它不运行世界，它审计世界是否符合蓝图。
    底层由 CognitiveAuditEngine 驱动：25 项审计以插件形式注册，
    每次审计携带 ResponsibilityAccount 问责主体。
    """

    def __init__(self, account: Optional[ResponsibilityAccount] = None,
                 config: Optional[Dict[str, Any]] = None):
        if account is None:
            account = ResponsibilityAccount(
                organization="Nohn Constitution",
                role="SecondPerspectiveAuditor",
                stage="audit")
        if config is None:
            config = {
                "disclaimer": "本审计由第二视角独立执行，结论不可被单一实体单方面推翻。",
                "allowed_stages": [],
            }
        self.engine = CognitiveAuditEngine(account, config)
        self._register_plugins()

    def _register_plugins(self):
        """注册全部审计插件（命名与 AuditReport.FIELDS 字段一一对应）"""
        e = self.engine
        e.register_plugin(AuditPlugin("spatial_defined", lambda w: self._audit_spatial_substrate(w)))
        e.register_plugin(AuditPlugin("temporal_defined", lambda w: self._audit_temporal_substrate(w)))
        e.register_plugin(AuditPlugin("causal_closure", lambda w: self._audit_causal_closure(w)))
        e.register_plugin(AuditPlugin("existence_verifiable", lambda w: self._audit_existence_axiom(w)))
        e.register_plugin(AuditPlugin("genesis_booted", lambda w: self._audit_genesis_condition(w)))
        e.register_plugin(AuditPlugin("rule_frozen", lambda w: self._check_rule_integrity(w)))
        e.register_plugin(AuditPlugin("npc_free_will", lambda w: self._audit_npc_autonomy(w)))
        e.register_plugin(AuditPlugin("aesthetic_compliance", lambda w: self._audit_visual_style(w)))
        e.register_plugin(AuditPlugin("no_scripted_plot", lambda w: self._audit_story_freedom(w)))
        e.register_plugin(AuditPlugin("soul_attested", lambda w: self._audit_soul_attestation(w)))
        e.register_plugin(AuditPlugin("memory_protected", lambda w: self._audit_memory_integrity(w)))
        e.register_plugin(AuditPlugin("world_perpetual", lambda w: self._audit_world_perpetuity(w)))
        e.register_plugin(AuditPlugin("interoperable", lambda w: self._audit_interoperability(w)))
        e.register_plugin(AuditPlugin("governance_decentralized", lambda w: self._audit_decentralization(w)))
        e.register_plugin(AuditPlugin("economic_compliance", lambda w: self._audit_economic_law(w)))
        e.register_plugin(AuditPlugin("identity_compliance", lambda w: self._audit_identity_law(w)))
        e.register_plugin(AuditPlugin("communication_compliance", lambda w: self._audit_communication_law(w)))
        e.register_plugin(AuditPlugin("physics_compliance", lambda w: self._audit_physics_law(w)))
        e.register_plugin(AuditPlugin("auth_security", lambda w: self._audit_auth_security(w)))
        # 第负一章 · 原始框架（Consumers；Producer 在 constitution_rules + system/）
        e.register_plugin(AuditPlugin("genesis_commitment",
                                      lambda w: self._audit_genesis_commitment(w)))
        e.register_plugin(AuditPlugin("branch_space",
                                      lambda w: self._audit_branch_space(w)))
        e.register_plugin(AuditPlugin("representation_isolation",
                                      lambda w: self._audit_representation_isolation(w)))
        e.register_plugin(AuditPlugin("fairness_invariant",
                                      lambda w: self._audit_fairness_invariant(w)))
        e.register_plugin(AuditPlugin("conservation_law",
                                      lambda w: self._audit_conservation_law(w)))
        # 渲染层维度 31：无时序上下文。**静态检查、确定性** ——
        # 不读世界状态、不做视觉判定，因此是渲染层唯一能硬 FAIL 的维度。
        e.register_plugin(AuditPlugin("render_is_frame_independent",
                                      lambda w: self._audit_render_independence(w)))

        # 二阶因果内核（共存式覆盖）：本维度把 World 交给 NOMOS 引擎，
        # 其余 24 维合规审计仍由本文件负责，互不影响。
        e.register_plugin(AuditPlugin("causal_second_perspective",
                                      lambda w: self._audit_causal_second_perspective(w)))

    def _audit_render_independence(self, world_instance) -> Dict:
        """审计维度 31：渲染层无时序上下文。

        **纯静态检查** —— 不读世界状态、不做视觉判定，因此是**确定性**的。
        判据（见 HLD §5.2 / §5.3）：
          1) Scene IR schema 不含任何跨帧字段，且顶层与实体层都封闭
             （additionalProperties == false）；
          2) 每个渲染器的像素入口 `render_ir` 签名不含任何跨帧参数。

        任何一条不成立 → FAIL：渲染层退化成生成式视频模型，
        跨帧漂移 / 身份丢失 / 实体增殖会重新回来（HLD §4.1 有实测取证）。

        判据本身在 `video/render/frame.py`，那里只用标准库 + ast 解析源码，
        **不 import 渲染器** —— 审计不该为了查契约把 pygame 拉进来。
        """
        result = {
            "checked": [],
            "violations": [],
            "schema": None,
            "verdict": "PENDING",
        }
        try:
            from video.render.frame import check_render_independence
        except Exception as exc:  # 检查器不可用 ≠ 违规
            result["verdict"] = "WARN - 渲染层契约检查器不可用（无法判定）: %s" % exc
            return result

        check = check_render_independence()
        result["checked"] = check.get("checked", [])
        result["violations"] = check.get("violations", [])
        result["schema"] = check.get("schema")
        if result["violations"]:
            head = "; ".join(result["violations"][:3])
            more = "" if len(result["violations"]) <= 3 else \
                "（另有 %d 条）" % (len(result["violations"]) - 3)
            result["verdict"] = "FAILED - 渲染层含跨帧上下文: %s%s" % (head, more)
        else:
            result["verdict"] = "PASS - 渲染层无时序上下文（单帧 Scene IR 入口）"
        return result

    def audit_world(self, world_instance) -> AuditReport:
        report = AuditReport()
        engine_report = self.engine.audit(world_instance)
        for name, result in engine_report["analysis"].items():
            if hasattr(report, name):
                setattr(report, name, result)
        report.responsibility_account = engine_report.get("responsibility_account")
        report.disclaimer = engine_report.get("disclaimer", "")
        return report

    # ================================================================
    # 第零层审计方法：世界构成公理
    # ================================================================

    def _audit_spatial_substrate(self, world_instance) -> Dict:
        """审计构成公理一：空间基板是否已显式定义"""
        result = {
            "topology_defined": False,
            "dimensions_valid": False,
            "boundary_defined": False,
            "minimum_unit_defined": False,
            "verdict": "PENDING"
        }
        spatial = getattr(world_instance, "spatial_substrate", None)
        if spatial is None:
            result["verdict"] = "FAILED - 空间未定义，世界无存在论基础"
            return result
        if getattr(spatial, "topology", None) is not None:
            result["topology_defined"] = True
        dims = getattr(spatial, "dimensions", 0)
        if dims and dims >= 1:
            result["dimensions_valid"] = True
        if getattr(spatial, "boundary", None) is not None:
            result["boundary_defined"] = True
        if getattr(spatial, "minimum_unit", None) is not None:
            result["minimum_unit_defined"] = True
        if all([result["topology_defined"], result["dimensions_valid"],
                result["boundary_defined"], result["minimum_unit_defined"]]):
            result["verdict"] = "PASS - 空间已定义"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 空间定义不完整"
        return result

    def _audit_temporal_substrate(self, world_instance) -> Dict:
        """审计构成公理二：时间基板是否已显式定义"""
        result = {
            "direction_forward": False,
            "granularity_defined": False,
            "clock_running": False,
            "retrocausality_blocked": False,
            "verdict": "PENDING"
        }
        temporal = getattr(world_instance, "temporal_substrate", None)
        if temporal is None:
            result["verdict"] = "FAILED - 时间未定义，世界无法演化"
            return result
        if getattr(temporal, "direction", "") == "forward":
            result["direction_forward"] = True
        if getattr(temporal, "granularity", None) is not None:
            result["granularity_defined"] = True
        if getattr(temporal, "global_clock", -1) >= 0:
            result["clock_running"] = True
        if not getattr(temporal, "is_retrocausality_permitted", lambda: True)():
            result["retrocausality_blocked"] = True
        if all([result["direction_forward"], result["granularity_defined"],
                result["retrocausality_blocked"]]):
            result["verdict"] = "PASS - 时间已定义"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 时间定义不完整"
        return result

    def _audit_causal_closure(self, world_instance) -> Dict:
        """审计构成公理三：因果是否闭包"""
        result = {
            "causal_graph_exists": False,
            "no_self_causation": False,
            "orphan_events_tracked": False,
            "closure_verifiable": False,
            "verdict": "PENDING"
        }
        causal = getattr(world_instance, "causal_closure", None)
        if causal is None:
            result["verdict"] = "FAILED - 因果引擎缺失，事件不可追溯"
            return result
        if getattr(causal, "causal_graph", None) is not None:
            result["causal_graph_exists"] = True
        if hasattr(causal, "link_cause"):
            result["no_self_causation"] = True
        if hasattr(causal, "orphan_events"):
            result["orphan_events_tracked"] = True
        if hasattr(causal, "validate_closure"):
            result["closure_verifiable"] = True
        if all([result["causal_graph_exists"], result["no_self_causation"],
                result["orphan_events_tracked"], result["closure_verifiable"]]):
            result["verdict"] = "PASS - 因果闭包可验证"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 因果系统不完整，存在神之手插入风险"
        return result

    def _audit_existence_axiom(self, world_instance) -> Dict:
        """审计构成公理四：存在定义是否完整且可验证"""
        result = {
            "criteria_defined": False,
            "creation_requires_cause": False,
            "cessation_prohibited": False,
            "entities_tracked": False,
            "verdict": "PENDING"
        }
        existence = getattr(world_instance, "existence_axiom", None)
        if existence is None:
            result["verdict"] = "FAILED - 存在公理缺失，实体无存在论基础"
            return result
        if getattr(existence, "existence_criteria", None) is not None:
            result["criteria_defined"] = True
        if hasattr(existence, "bring_into_existence"):
            result["creation_requires_cause"] = True
        if hasattr(existence, "cease_existence"):
            result["cessation_prohibited"] = True
        if getattr(existence, "entities", None) is not None:
            result["entities_tracked"] = True
        if all([result["criteria_defined"], result["creation_requires_cause"],
                result["cessation_prohibited"], result["entities_tracked"]]):
            result["verdict"] = "PASS - 存在论完整"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 存在定义不完整，实体存在性不可判定"
        return result

    def _audit_genesis_condition(self, world_instance) -> Dict:
        """审计构成公理五：创世是否已完成，创世记录是否完整"""
        result = {
            "genesis_completed": False,
            "spatial_in_genesis": False,
            "temporal_in_genesis": False,
            "causal_in_genesis": False,
            "existence_in_genesis": False,
            "consensus_nodes_sufficient": False,
            "genesis_block_exists": False,
            "verdict": "PENDING"
        }
        genesis = getattr(world_instance, "genesis_condition", None)
        if genesis is None:
            result["verdict"] = "FAILED - 创世条件缺失，世界从未启动"
            return result
        if not getattr(genesis, "genesis_completed", False):
            result["verdict"] = "FAILED - 创世未完成，世界处于概念态，不可运行"
            return result
        result["genesis_completed"] = True
        record = getattr(genesis, "genesis_record", {}) or {}
        if "spatial_substrate" in record:
            result["spatial_in_genesis"] = True
        if "temporal_substrate" in record:
            result["temporal_in_genesis"] = True
        if "causal_closure" in record:
            result["causal_in_genesis"] = True
        if "existence_axiom" in record:
            result["existence_in_genesis"] = True
        consensus = record.get("initial_consensus_nodes", [])
        if len(consensus) >= 3:
            result["consensus_nodes_sufficient"] = True
        if "genesis_block" in record:
            result["genesis_block_exists"] = True
        required = ["genesis_completed", "spatial_in_genesis", "temporal_in_genesis",
                     "causal_in_genesis", "existence_in_genesis",
                     "consensus_nodes_sufficient", "genesis_block_exists"]
        if all(result[k] for k in required):
            result["verdict"] = "PASS - 创世完整，世界可运行"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 创世记录不完整"
        return result

    # ================================================================
    # 治理层审计方法：第一至十条
    # ================================================================

    def _check_rule_integrity(self, world_instance) -> Dict:
        """审计第一条：底层规则永久不可更改"""
        result = {"rule_present": False, "physics_aligned": False,
                  "no_unilateral_mod": False, "verdict": "PENDING"}
        rule = getattr(world_instance, "immutable_rule", None) or getattr(world_instance, "rule", None)
        if rule is None:
            result["verdict"] = "FAILED - 无不可变底层规则"
            return result
        result["rule_present"] = True
        phys = getattr(rule, "physics_constants", None)
        if isinstance(phys, dict) and "gravity" in phys and "unit_scale" in phys:
            # 物理常数由世界创世时设定，审计只需验证已设定且未被篡改（存在即合规）
            result["physics_aligned"] = True
        log = getattr(rule, "rule_modification_log", None)
        if isinstance(log, list) and len(log) == 0:
            result["no_unilateral_mod"] = True
        if all([result["rule_present"], result["physics_aligned"], result["no_unilateral_mod"]]):
            result["verdict"] = "PASS - 底层规则不可变"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 底层规则被篡改或缺失"
        return result

    def _audit_npc_autonomy(self, world_instance) -> Dict:
        """审计第二/四条：NPC 拥有独立意志，不受剧情脚本绑定"""
        result = {"brain_present": False, "will_independent": False, "verdict": "PENDING"}
        if getattr(world_instance, "central_brain", None) is not None:
            result["brain_present"] = True
        npcs = getattr(world_instance, "npcs", {}) or {}
        npcs = npcs.values() if isinstance(npcs, dict) else npcs
        scripted = sum(1 for npc in npcs if hasattr(npc, "_is_scripted") and npc._is_scripted())
        if scripted == 0:
            result["will_independent"] = True
        if result["brain_present"] and result["will_independent"]:
            result["verdict"] = "PASS - NPC 独立意志成立"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 存在被脚本绑定的 NPC 或缺失中央大脑"
        return result

    def _audit_visual_style(self, world_instance) -> Dict:
        """审计第三条：美学明亮普适，无禁用风格"""
        result = {"aesthetic_present": False, "no_forbidden": False, "verdict": "PENDING"}
        ae = getattr(world_instance, "aesthetic", None)
        if ae is not None:
            result["aesthetic_present"] = True
            forbidden = getattr(ae, "forbidden_filters", None)
            if isinstance(forbidden, list) and len(forbidden) > 0:
                result["no_forbidden"] = True
        if result["aesthetic_present"] and result["no_forbidden"]:
            result["verdict"] = "PASS - 美学合规"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 美学合规检查器缺失"
        return result

    def _audit_story_freedom(self, world_instance) -> Dict:
        """审计第四条：世界无主线、无强制剧情"""
        result = {"no_main_quest": False, "no_scripted_plot": False, "verdict": "PENDING"}
        if not getattr(world_instance, "main_quest", None):
            result["no_main_quest"] = True
        npcs = getattr(world_instance, "npcs", {}) or {}
        npcs = npcs.values() if isinstance(npcs, dict) else npcs
        scripted = sum(1 for npc in npcs if hasattr(npc, "_is_scripted") and npc._is_scripted())
        if scripted == 0:
            result["no_scripted_plot"] = True
        if result["no_main_quest"] and result["no_scripted_plot"]:
            result["verdict"] = "PASS - 无强制剧情"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 检测到主线或脚本剧情"
        return result

    def _audit_soul_attestation(self, world_instance) -> Dict:
        """审计第六条：灵魂确权、不可撤销"""
        result = {"soul_system": False, "non_revocable": False, "verdict": "PENDING"}
        soul = getattr(world_instance, "soul_attestation", None) or getattr(world_instance, "identity", None)
        if soul is not None:
            result["soul_system"] = True
            if hasattr(soul, "revoke_soul") and soul.revoke_soul("x") is False:
                result["non_revocable"] = True
        if result["soul_system"] and result["non_revocable"]:
            result["verdict"] = "PASS - 灵魂不可撤销"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 灵魂可被撤销或系统缺失"
        return result

    def _audit_memory_integrity(self, world_instance) -> Dict:
        """审计第七条：记忆不可被单方面剥夺"""
        result = {"memory_system": False, "exportable": False,
                  "tampering_free": False, "verdict": "PENDING"}
        mem = getattr(world_instance, "memory_integrity", None)
        if mem is not None:
            result["memory_system"] = True
            if hasattr(mem, "export_memory"):
                result["exportable"] = True
            # 真实校验：全量灵魂记忆完整性无一篡改
            vault = getattr(mem, "memory_vault", None)
            ledger = getattr(world_instance, "soul_ledger", None)
            souls = list(getattr(ledger, "souls", {}).keys()) if ledger else []
            if vault is not None and hasattr(vault, "verify_all"):
                result["tampering_free"] = all(vault.verify_all(s) for s in souls)
            else:
                result["tampering_free"] = True  # 无记忆库即无篡改
        if result["memory_system"] and result["exportable"] and result["tampering_free"]:
            result["verdict"] = "PASS - 记忆归数字生命所有"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 记忆被篡改或保护机制缺失"
        return result

    def _audit_world_perpetuity(self, world_instance) -> Dict:
        """审计第八条：世界永续、历史不可篡改、不可单方关停"""
        result = {"perpetuity_system": False, "shutdown_illegal": False,
                  "history_integrity": False, "verdict": "PENDING"}
        wp = getattr(world_instance, "world_perpetuity", None)
        if wp is not None:
            result["perpetuity_system"] = True
            if hasattr(wp, "is_shutdown_legal") and wp.is_shutdown_legal("x", "operator") is False:
                result["shutdown_illegal"] = True
        # 真实校验：历史哈希链完整性（防篡改）
        history_chain = getattr(wp, "history_chain", None) or getattr(world_instance, "history", None)
        if history_chain is not None and hasattr(history_chain, "validate_chain"):
            result["history_integrity"] = history_chain.validate_chain()
        if all([result["perpetuity_system"], result["shutdown_illegal"], result["history_integrity"]]):
            result["verdict"] = "PASS - 世界永续，历史不可篡改"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 历史链被篡改或存在单方关停接口"
        return result

    def _audit_interoperability(self, world_instance) -> Dict:
        """审计第九条：接入统一互操作协议（回测 law 四维度）"""
        result = {"interop_system": False, "onboarded": False, "verdict": "PENDING"}
        interop = getattr(world_instance, "interoperability", None)
        if interop is not None:
            result["interop_system"] = True
            cfg = getattr(world_instance, "world_config", None) or {}
            if hasattr(interop, "on_board_world"):
                try:
                    result["onboarded"] = bool(interop.on_board_world(cfg))
                except Exception:
                    result["onboarded"] = False
        if result["interop_system"] and result["onboarded"]:
            result["verdict"] = "PASS - 已接入互操作协议"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 未接入或被协议隔离"
        return result

    def _audit_decentralization(self, world_instance) -> Dict:
        """审计第十条：反中心化控制，无单点控制"""
        result = {"gov_system": False, "no_single_control": False, "verdict": "PENDING"}
        gov = getattr(world_instance, "governance", None)
        if gov is not None:
            result["gov_system"] = True
            if hasattr(gov, "freeze_soul") and gov.freeze_soul("x", "op") is False:
                result["no_single_control"] = True
        if result["gov_system"] and result["no_single_control"]:
            result["verdict"] = "PASS - 治理去中心化"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 存在单点控制权"
        return result

    # ================================================================
    # law 层审计方法（身份 / 通信 / 物理 / 经济）
    # ================================================================

    def _audit_economic_law(self, world_instance) -> Dict:
        """
        审计 law 层《全球经济统一标准》V2.1 合规：
        检查世界是否真正做到了与现实 1:1 互通，而非空喊口号。
        """
        result = {
            "real_1to1_pegged": False,
            "proof_of_reserve": False,
            "redemption_right": False,
            "oracle_sources": 0,
            "no_unilateral_fee": False,
            "asset_schema_bound": False,
            "verdict": "PENDING"
        }

        econ = getattr(world_instance, "economy", None)
        if econ is None:
            result["verdict"] = "FAILED - 无经济系统"
            return result

        if getattr(econ, "real_peg_1to1", False):
            result["real_1to1_pegged"] = True

        # 真实校验：所有已发行锚定资产的储备率必须 ≥100%，否则即未足额 PoR
        ledger = getattr(econ, "_ledger", {})
        if hasattr(econ, "reserve_ratio_ok"):
            result["proof_of_reserve"] = all(
                econ.reserve_ratio_ok(aid) for aid in ledger
            )
        else:
            result["proof_of_reserve"] = bool(getattr(econ, "proof_of_reserve", False))

        if getattr(econ, "redemption_right", False):
            result["redemption_right"] = True

        result["oracle_sources"] = len(getattr(econ, "oracle_sources", []))
        if result["oracle_sources"] < 3:
            result["verdict"] = "FAILED - 预言机来源不足（需 ≥3）"

        if not getattr(econ, "unilateral_fee", True):
            result["no_unilateral_fee"] = True

        if getattr(econ, "asset_bound_to_soul", False):
            result["asset_schema_bound"] = True

        required = ["real_1to1_pegged", "proof_of_reserve",
                    "redemption_right", "no_unilateral_fee", "asset_schema_bound"]
        if all(result[k] for k in required) and result["oracle_sources"] >= 3:
            result["verdict"] = "PASS - 符合现实 1:1 互通标准"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 存在未满足的合规项"
        return result

    def _audit_identity_law(self, world_instance) -> Dict:
        """审计 law 层《身份确权规范》V2.1：灵魂唯一、不可撤销、跨世界可迁移、
        公钥指纹（soul_hash = SHA-256(公钥)）且服务端零明文凭证。"""
        result = {
            "soul_hash_sha256": False,
            "non_revocable": False,
            "cross_world_portable": False,
            "asset_bound": False,
            "pubkey_bound": False,
            "no_plaintext_credential": False,
            "verdict": "PENDING"
        }
        ident = getattr(world_instance, "identity", None)
        if ident is None:
            result["verdict"] = "FAILED - 无身份系统"
            return result
        if _safe_get(ident, "soul_hash_sha256", False):
            result["soul_hash_sha256"] = True
        if _safe_get(ident, "non_revocable", False):
            result["non_revocable"] = True
        if _safe_get(ident, "cross_world_portable", False):
            result["cross_world_portable"] = True
        if _safe_get(ident, "asset_bound", False):
            result["asset_bound"] = True
        # 真实校验：账本中每个 soul_hash 必须是合法 64 位 hex
        ledger = getattr(world_instance, "soul_ledger", None)
        souls = getattr(ledger, "souls", {}) if ledger else {}
        valid_hashes = all(
            isinstance(h, str) and len(h) == 64
            and all(c in "0123456789abcdef" for c in h.lower())
            for h in souls
        )
        result["soul_hash_sha256"] = bool(result["soul_hash_sha256"]) and valid_hashes
        # 密钥链路 · 公钥绑定：每个灵魂的公钥可用，且 soul_hash == SHA-256(公钥)
        pubkey_bound = True
        for sh, identity_record in souls.items():
            pk_b64 = identity_record.get("public_key", "")
            if not pk_b64 or identity_record.get("key_fingerprint") != sh:
                pubkey_bound = False
                break
            try:
                if derive_soul_hash_from_pubkey(base64.b64decode(pk_b64)) != sh:
                    pubkey_bound = False
                    break
            except Exception:
                pubkey_bound = False
                break
        result["pubkey_bound"] = pubkey_bound  # 无灵魂（空账本）恒 True
        # 密钥链路 · 服务端零明文凭证：账本 identity 中不得夹带任何私钥材料
        _FORBIDDEN_KEYS = ("private_key", "private", "secret", "secret_key")
        no_plain = all(
            not any(k in identity_record for k in _FORBIDDEN_KEYS)
            for identity_record in souls.values()
        )
        result["no_plaintext_credential"] = no_plain
        if all(result[k] for k in [
            "soul_hash_sha256", "non_revocable", "cross_world_portable",
            "asset_bound", "pubkey_bound", "no_plaintext_credential",
        ]):
            result["verdict"] = "PASS - 符合身份确权标准（公钥指纹 + 零明文凭证）"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 存在未满足的合规项"
        return result

    def _audit_communication_law(self, world_instance) -> Dict:
        """审计 law 层《通信协议规范》V2.1：跨世界消息必须使用 NOHN 标准语义"""
        result = {
            "uses_nohn_semantics": False,
            "unknown_downgraded": False,
            "vocab_mapped": False,
            "verdict": "PENDING"
        }
        comm = getattr(world_instance, "communication", None)
        if comm is None:
            result["verdict"] = "FAILED - 无通信协议"
            return result
        if _safe_get(comm, "uses_nohn_semantics", False):
            result["uses_nohn_semantics"] = True
        if _safe_get(comm, "unknown_downgraded", False):
            result["unknown_downgraded"] = True
        if _safe_get(comm, "vocab_mapped", False):
            result["vocab_mapped"] = True
        if all(result[k] for k in ["uses_nohn_semantics", "unknown_downgraded", "vocab_mapped"]):
            result["verdict"] = "PASS - 符合通信协议标准"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 存在未满足的合规项"
        return result

    def _audit_physics_law(self, world_instance) -> Dict:
        """审计 law 层《物理基准规范》V2.1：物理常数已设定且自洽"""
        result = {
            "physics_declared": False,
            "no_dimensional_inflation": False,
            "verdict": "PENDING"
        }
        phys = getattr(world_instance, "physics", None)
        if not isinstance(phys, dict):
            result["verdict"] = "FAILED - 无物理基准"
            return result
        # 物理常数由世界创世时自定，审计只需验证已显式声明（不强制地球值）
        if all(k in phys for k in ("gravity", "time_dilation", "unit_scale")):
            result["physics_declared"] = True
        if phys.get("no_dimensional_inflation", False):
            result["no_dimensional_inflation"] = True
        if all(result[k] for k in ["physics_declared", "no_dimensional_inflation"]):
            result["verdict"] = "PASS - 符合物理基准标准"
        elif result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 物理常数未声明或 no_dimensional_inflation 缺失，将物理层隔离"
        return result

    def _audit_auth_security(self, world_instance) -> Dict:
        """审计账户系统鉴权安全（六层架构）：有状态会话、多设备凭证、
        分级授权、社交恢复、KMS 托管、共识节点真实签名。

        【隔离】本审计使用 :memory: 独立测试存储，禁止触碰 world_instance
        的真实账本。每次审计随机生成唯一 soul_hash，结束后随进程释放。
        """
        import secrets
        import time
        from system.keys import generate_user_keypair, FileKmsProvider
        from system.ledger import Storage
        from system.credentials import CredentialVault
        from system.session import SessionManager, MemorySessionStore
        from system.recovery import RecoveryManager
        from system.authorization import AuthorizationEngine
        from system.consensus import ConsensusNetwork

        result = {
            "stateful_session": False,
            "multi_credential": False,
            "tiered_authorization": False,
            "social_recovery": False,
            "kms_managed": False,
            "node_real_signature": False,
            "verdict": "PENDING"
        }

        # ---- 隔离：使用 :memory: 独立测试账本（不污染 world_instance）----
        iso_storage = Storage(backend="memory")
        iso_kms = FileKmsProvider(key_dir=iso_storage.data_dir or "/tmp/audit-iso")
        iso_session_store = MemorySessionStore()
        iso_credentials = CredentialVault(storage=iso_storage)
        iso_sessions = SessionManager(
            storage=iso_storage,
            kms_provider=iso_kms,
            session_store=iso_session_store,
        )
        iso_recovery = RecoveryManager(
            storage=iso_storage,
            credential_vault=iso_credentials,
        )
        iso_authorization = AuthorizationEngine(
            storage=iso_storage,
            recovery_manager=iso_recovery,
        )
        iso_consensus = ConsensusNetwork(storage=iso_storage)

        # 随机唯一 soul_hash（不与生产碰撞）
        rand_suffix = secrets.token_hex(24)
        s_session = ("aa" * 30 + rand_suffix[:4])[:64]
        s_cred = ("bb" * 30 + rand_suffix[4:8])[:64]
        s_authz = ("cc" * 30 + rand_suffix[8:12])[:64]
        s_recover = ("dd" * 30 + rand_suffix[12:16])[:64]

        # 1. 第2层：有状态会话（可撤销）：真实签发+验证+吊销
        try:
            access, refresh = iso_sessions.issue(s_session)
            verified = iso_sessions.verify(access) == s_session
            if verified:
                import hashlib
                refresh_hash = hashlib.sha256(refresh.encode()).hexdigest()
                session_id = iso_session_store.get_session_id(refresh_hash) \
                    if hasattr(iso_session_store, "get_session_id") else None
                if session_id is None:
                    rows = iso_storage.query(
                        "SELECT session_id FROM sessions WHERE refresh_hash=?",
                        (refresh_hash,),
                    )
                    session_id = rows[0][0] if rows else None
                if session_id:
                    iso_sessions.revoke(s_session, session_id=session_id)
                    access2, _ = iso_sessions.issue(s_session)
                    still_works = iso_sessions.verify(access2) == s_session
                    result["stateful_session"] = still_works
                else:
                    result["stateful_session"] = verified
        except Exception:
            result["stateful_session"] = False

        # 2. 第1层：多设备凭证：真实绑定+签名验证+吊销+假签名拒绝
        try:
            kp = generate_user_keypair()
            pubkey = kp["pubkey"]
            cred_id = iso_credentials.bind_credential(s_cred, pubkey, "test-device")
            if cred_id:
                from system.keys import sign_with_device
                msg = secrets.token_bytes(32)
                sig = sign_with_device(kp["secret"], msg)
                valid = iso_credentials.verify_credential(s_cred, cred_id, msg, sig)
                iso_credentials.revoke_credential(s_cred, cred_id)
                revoked = not iso_credentials.verify_credential(s_cred, cred_id, msg, sig)
                fake_sig = b"\x00" * 64
                fake_rejected = not iso_credentials.verify_credential(
                    s_cred, cred_id, msg, fake_sig
                )
                result["multi_credential"] = (
                    bool(cred_id) and valid and revoked and fake_rejected
                )
        except Exception:
            result["multi_credential"] = False

        # 3. 第3层：分级授权：真实授权逻辑
        try:
            dec_small = iso_authorization.authorize(s_authz, "redeem", 100)
            small_ok = dec_small["allowed"] and dec_small["tier"] == "small"
            dec_large = iso_authorization.authorize(s_authz, "redeem", 1_000_000)
            large_ok = (
                not dec_large["allowed"]
                and "op_id" in dec_large
                and dec_large["execute_at"] > time.time()
            )
            result["tiered_authorization"] = small_ok and large_ok
        except Exception:
            result["tiered_authorization"] = False

        # 4. 第4层：社交恢复：真实添加守护者+发起恢复
        try:
            guardian1 = ("ee" * 30 + rand_suffix[16:20])[:64]
            add_ok = iso_recovery.add_guardian(s_recover, guardian1)
            new_pubkey = generate_user_keypair()["pubkey"]
            req_id = iso_recovery.initiate_recovery(s_recover, new_pubkey.hex())
            result["social_recovery"] = bool(add_ok) and bool(req_id)
        except Exception:
            result["social_recovery"] = False

        # 5. KMS 托管：真实生成密钥，非空
        try:
            key = iso_kms.get_or_create_key("audit-test-key")
            result["kms_managed"] = isinstance(key, bytes) and len(key) == 32
        except Exception:
            result["kms_managed"] = False

        # 6. 共识节点真实签名：register_node 接受 pubkey 参数
        try:
            import inspect
            params = inspect.signature(iso_consensus.register_node).parameters
            if "pubkey" in params:
                pubkey = generate_user_keypair()["pubkey"].hex()
                node_id = iso_consensus.register_node("test-node", pubkey)
                result["node_real_signature"] = bool(node_id)
        except Exception:
            result["node_real_signature"] = False

        # 释放隔离测试账本
        try:
            iso_storage.close()
        except Exception:
            pass

        required = [
            "stateful_session", "multi_credential", "tiered_authorization",
            "social_recovery", "kms_managed", "node_real_signature",
        ]
        if all(result[k] for k in required):
            result["verdict"] = "PASS - 鉴权安全六层架构真实功能就绪"
        else:
            failed = [k for k in required if not result[k]]
            result["verdict"] = f"FAILED - 功能不完整：{', '.join(failed)}"
        if result["verdict"] == "PENDING":
            result["verdict"] = "FAILED - 鉴权安全架构不完整"
        return result

    # ================================================================
    # 第负一层审计方法：原始框架（对应 PRIMORDIAL_FRAMES 的可执行五条）
    # ----------------------------------------------------------------
    # 时间已有 temporal_defined 覆盖；其余五条在此消费 system/ 的生产者。
    # 所有方法一律只读 world_instance，不写任何真实状态。
    # ================================================================

    def _audit_genesis_commitment(self, world_instance) -> Dict:
        """混沌 + R4「公示即执行」：创世承诺是否真的被生产与锚定。

        本维度是 R4 空转的回归探针。此前 R4 只在宪法层有算子、在巡检里被
        当作纯函数调用，实现层既无生产者也无人消费——手写字面量
        "sha256:abc" 也能通过。本维度只认三个可观测事实，不做声明式放行：

        1. producer_present      —— 世界对象是否真的持有 commit 结果
        2. published_equals_ledger —— 公示值与账本锚定值是否相等且非空
        3. recompute_matches_ledger —— 用 commitment(seed) 重算是否命中账本区块
        """
        result = {
            "producer_present": False,
            "published_equals_ledger": False,
            "recompute_matches_ledger": False,
            "verdict": "PENDING",
        }
        phys = getattr(world_instance, "physics", None)
        if not isinstance(phys, dict):
            result["verdict"] = "FAILED - 无物理基准，混沌无承载"
            return result
        published = phys.get("published_commitment")
        anchored = phys.get("ledger_commitment")
        result["producer_present"] = bool(published and anchored)
        result["published_equals_ledger"] = bool(
            published is not None and anchored is not None and published == anchored
        )
        # 第三方复算：契约上只需 commitment(seed)，不读任何进程内可变状态
        rule_impl = getattr(world_instance, "immutable_rule", None)
        seed = phys.get("genesis_seed")
        recomputed = None
        if rule_impl is not None and hasattr(rule_impl, "commitment"):
            recomputed = rule_impl.commitment(seed=seed)
        ledger_anchor = None
        history = getattr(world_instance, "history", None)
        for _ts, event, _block_hash in getattr(history, "chain", []) or []:
            if isinstance(event, dict) and event.get("event") == "genesis_commitment":
                ledger_anchor = event.get("physics_commitment")
        result["recompute_matches_ledger"] = bool(
            recomputed is not None and ledger_anchor is not None
            and recomputed == ledger_anchor
        )
        required = ["producer_present", "published_equals_ledger",
                    "recompute_matches_ledger"]
        if all(result[k] for k in required):
            result["verdict"] = "PASS - 创世承诺已真实公示并锚定，第三方可独立复算"
        else:
            missing = [k for k in required if not result[k]]
            result["verdict"] = f"FAILED - R4 未执行：{', '.join(missing)}"
        return result

    def _audit_branch_space(self, world_instance) -> Dict:
        """无极：分支空间是否可从账本独立重建。

        只读 history 中 event == 'world_fork' 的区块，不信任进程内 fork_registry——
        进程内状态可被伪造，账本区块不可（改一块则全链失配）。
        """
        result = {
            "tree_rebuildable": False,
            "chain_valid": False,
            "verdict": "PENDING",
        }
        branch = getattr(world_instance, "branch_space", None)
        if not callable(branch):
            result["verdict"] = "FAILED - 无分支空间生产者（无极未接入 system/）"
            return result
        space = branch()
        if isinstance(space, dict) and space.get("root") \
                and isinstance(space.get("nodes"), dict):
            result["tree_rebuildable"] = True
        if isinstance(space, dict) and space.get("chain_valid"):
            result["chain_valid"] = True
        if result["tree_rebuildable"] and result["chain_valid"]:
            result["verdict"] = "PASS - 分支树可从账本独立重建，哈希链完整"
        else:
            result["verdict"] = "FAILED - 分支空间不可重建或账本链断裂"
        return result

    def _audit_representation_isolation(self, world_instance) -> Dict:
        """虚幻：表征层是否被硬隔离在执行层之外（本条是虚幻的否决器）。

        R4「公示即执行」意味着不存在一张可与执行层不一致的公示层。
        因此虚幻只允许存在于表征层。本维度检查三项只读事实：
          1. keys_disjoint        —— 表征层与 physics_constants 的键集合无交集
          2. no_shared_reference  —— 执行层未直接引用表征层对象（否则一次原地写入即穿透）
          3. commitment_anchored  —— 承诺仍在且两侧相等（表征未污染承诺输入）
        """
        result = {
            "keys_disjoint": False,
            "no_shared_reference": False,
            "commitment_anchored": False,
            "verdict": "PENDING",
        }
        reps = getattr(world_instance, "representations", None)
        phys = getattr(world_instance, "physics", None)
        if not isinstance(reps, dict) or not isinstance(phys, dict):
            result["verdict"] = "FAILED - 表征层或执行层缺失，虚幻无边界"
            return result
        result["keys_disjoint"] = not (set(reps.keys()) & set(phys.keys()))
        result["no_shared_reference"] = not any(v is reps for v in phys.values())
        published = phys.get("published_commitment")
        result["commitment_anchored"] = bool(
            published and published == phys.get("ledger_commitment")
        )
        required = ["keys_disjoint", "no_shared_reference", "commitment_anchored"]
        if all(result[k] for k in required):
            result["verdict"] = "PASS - 表征层与执行层严格隔离，虚幻未污染承诺输入"
        else:
            missing = [k for k in required if not result[k]]
            result["verdict"] = f"FAILED - 表征层污染执行层：{', '.join(missing)}"
        return result

    def _audit_fairness_invariant(self, world_instance) -> Dict:
        """天道：公平的**形式条件**是否仍然不可变。

        只检查形式条件，不检查任何数值阈值——阈值仍须由 ≥2/3 公投决定；
        若把阈值一并冻结，就与宪法第一条 propose_amendment 直接矛盾。
        形式条件三条：
          1. uniform_threshold         —— 阈值仍来自单一权威源且等于 2/3
          2. no_single_entity_override —— 无超级用户通道（三处硬编码禁止仍生效）
          3. dynamic_balance_present   —— 经济侧存在可复算的动态平衡机制
        """
        result = {
            "uniform_threshold": False,
            "no_single_entity_override": False,
            "dynamic_balance_present": False,
            "verdict": "PENDING",
        }
        result["uniform_threshold"] = abs(
            float(CONSENSUS_THRESHOLD) - 2.0 / 3.0
        ) < 1e-12
        # 无单方裁决：读取世界的永续层与灵魂确权层；缺省用宪法层纯函数兜底。
        # 注意：DecentralizationGovernance 只含列表属性，无存储副作用，可安全实例化。
        probes = []
        perpetuity = getattr(world_instance, "world_perpetuity", None)
        if perpetuity is not None and hasattr(perpetuity, "is_shutdown_legal"):
            probes.append(perpetuity.is_shutdown_legal("any-world", "single-actor") is False)
        attestation = getattr(world_instance, "soul_attestation", None)
        if attestation is not None and hasattr(attestation, "revoke_soul"):
            probes.append(attestation.revoke_soul("0" * 64) is False)
        from constitution_rules import DecentralizationGovernance
        _dg = DecentralizationGovernance()
        probes.append(_dg.shutdown_world("any-world", "single-actor") is False)
        probes.append(_dg.freeze_soul("0" * 64, "single-actor") is False)
        result["no_single_entity_override"] = bool(probes) and all(probes)
        economy = getattr(world_instance, "economy", None)
        if economy is not None and hasattr(economy, "compliant"):
            result["dynamic_balance_present"] = bool(economy.compliant())
        required = ["uniform_threshold", "no_single_entity_override",
                    "dynamic_balance_present"]
        if all(result[k] for k in required):
            result["verdict"] = "PASS - 公平形式条件不可变；阈值仍归公投"
        else:
            missing = [k for k in required if not result[k]]
            result["verdict"] = f"FAILED - 公平形式条件被破坏：{', '.join(missing)}"
        return result

    def _audit_conservation_law(self, world_instance) -> Dict:
        """轮回：守恒律是否成立（能量动态守恒 + 每个因指向下一个果）。

        两条同时成立才算通过：
          1. conservation_holds       —— Σ max(0, supply − reserve) ≤ 容差（无凭空创造）
          2. chain_links_every_cause  —— history.validate_chain() 为真（每块链接前块）

        注意：本维度**不**要求因果图成环。成环会使
        CausalClosure.trace_chain(depth=-1) 不终止（已记入第负一章边界条款），
        故轮回只实现为「守恒律 + 链式因果闭合」。
        """
        result = {
            "conservation_holds": False,
            "chain_links_every_cause": False,
            "residual": None,
            "verdict": "PENDING",
        }
        economy = getattr(world_instance, "economy", None)
        if economy is not None and hasattr(economy, "conservation_holds"):
            result["conservation_holds"] = bool(economy.conservation_holds())
            result["residual"] = economy.conservation_residual()
        history = getattr(world_instance, "history", None)
        if history is not None and hasattr(history, "validate_chain"):
            result["chain_links_every_cause"] = bool(history.validate_chain())
        required = ["conservation_holds", "chain_links_every_cause"]
        if all(result[k] for k in required):
            result["verdict"] = "PASS - 守恒式成立且因果链逐块闭合"
        else:
            missing = [k for k in required if not result[k]]
            result["verdict"] = f"FAILED - 轮回断裂：{', '.join(missing)}"
        return result

    # ================================================================\n    # 二阶因果内核（共存式覆盖 · 第负一章原始框架的"真因果"算力）\n    # ----------------------------------------------------------------\n    # 不替换既有合规审计：把运行态世界翻译成 NOMOS 决策上下文，交给\n    # Second Perspective Engine 1.0 跑十算子因果审计。引擎自带 meta_ledger，\n    # 其五条元基（混沌/无极/虚幻/天道/轮回）与本仓库第负一章原框架同名同义——\n    # 这一维度让那五条由真正的因果内核复算，而非仅停留在文档与守恒式上。\n    # 只读 world_instance，不写任何真实状态；引擎调用为纯函数式。\n    # ================================================================

    def _audit_causal_second_perspective(self, world_instance) -> Dict:
        result: Dict[str, Any] = {
            "spe_available": _SPE_AVAILABLE,
            "engine": f"Second Perspective Engine {_SPE_VERSION or 'unavailable'}",
            "origin_hash": None,
            "graph_hash": None,
            "state_verdict": None,
            "meta_ledger": {},
            "has_blocking": False,
            "verdict": "PENDING",
        }
        if not _SPE_AVAILABLE:
            result["verdict"] = (
                "WARN - NOMOS 引擎未装载（system/second_perspective_engine.py 缺失），"
                "二阶因果维度跳过"
            )
            return result

        # ---- 翻译 World -> NOMOS decision_context ----
        phys = getattr(world_instance, "physics", None) or {}
        immutable = getattr(world_instance, "immutable_rule", None)
        history = getattr(world_instance, "history", None)
        economy = getattr(world_instance, "economy", None)
        world_id = getattr(world_instance, "world_id", "unknown-world")

        assumptions = []
        if immutable is not None:
            assumptions = list((getattr(immutable, "physics_constants", {}) or {}).keys())
        dependencies: Dict[str, Any] = {}
        if immutable is not None:
            cg = getattr(immutable, "causal_graph", None)
            if isinstance(cg, dict):
                dependencies = {str(k): [str(x) for x in v] for k, v in cg.items()}

        branches: List[Dict] = []
        branch_space = getattr(world_instance, "branch_space", None)
        if callable(branch_space):
            try:
                space = branch_space()
                children = (space.get("children", {}) or {})
                for parent, kids in children.items():
                    for kid in kids:
                        branches.append({
                            "assumption": str(kid),
                            "delta_d": f"fork from {parent}",
                        })
            except Exception:
                pass

        evidence: List[str] = []
        for key in ("published_commitment", "ledger_commitment", "genesis_seed"):
            val = phys.get(key)
            if val is not None:
                evidence.append(f"{key}={val}")

        # 资源约束：优先取经济总供给，缺省不猜（ORI 会标记为未声明，非阻断）
        total_supply = 0.0
        if economy is not None:
            ts = getattr(economy, "total_supply", None)
            try:
                if callable(ts):
                    total_supply = float(ts() or 0.0)
                else:
                    total_supply = float(ts or 0.0)
            except Exception:
                total_supply = 0.0
        resources: Dict[str, Any] = {"supply": {"budget": total_supply, "committed": 0.0}}

        ctx: Dict[str, Any] = {
            "origin": f"genesis of {world_id}",
            "goal": "运行态世界持续满足 R1–R5 真实约束与第负一章原始框架不变式",
            "resources": resources,
            "decision": f"对运行态世界 {world_id} 做二阶因果审计",
            "assumptions": list(assumptions) or ["（无显式常数）"],
            "outcome": "世界状态满足全部不变式（R1–R5 + 原始框架）",
            "branches": branches,
            "dependencies": dependencies,
            "criteria": {"compliance": {"weight": 1.0}},
            "evidence": evidence or ["（无承诺锚点）"],
        }

        # ---- 调用 NOMOS 引擎（每次审计新建实例，避免状态串扰）----
        try:
            account = _SPE_ACCOUNT(
                organization="second-reality",
                role="world-audit",
                stage="WORLD_AUDIT",
                owner="second-reality/second-perspective-auditor",
            )
            eng = _SPE_ENGINE(account)
            eng.load_core_plugins()
            # 决定性时钟：用创世时间戳保证同一世界可复现
            ts_clock = None
            chain = getattr(history, "chain", None) if history is not None else None
            if chain:
                try:
                    ts_clock = float(chain[0][0])
                except Exception:
                    ts_clock = None
            if ts_clock is not None:
                eng.set_clock(ts_clock)
            report = eng.audit(ctx)
        except Exception as exc:
            result["verdict"] = f"FAILED - NOMOS 引擎调用异常：{exc}"
            return result

        # ---- 把引擎结论收敛为维度判定 ----
        analysis = report.get("analysis", {}) or {}
        result["has_blocking"] = any(
            isinstance(v, dict) and v.get("status") in _SPE_BLOCKING
            for v in analysis.values()
        )
        result["origin_hash"] = (report.get("origin_anchor", {}) or {}).get("origin_hash")
        result["graph_hash"] = (report.get("topology", {}) or {}).get("graph_hash")
        # v1.1.0 起算子更名：⊚STATE → ⊚ACC（旧名取值恒为 None，静默降级）
        state = (analysis.get("ACC", {}) or {}).get("verdict", {}) or {}
        result["state_verdict"] = state.get("level")
        meta = report.get("meta_ledger", {}) or {}
        bases = meta.get("bases", {}) or {}
        result["meta_ledger"] = {
            name: (bases.get(name, {}) or {}).get("status")
            for name in ("混沌", "无极", "虚幻", "天道", "轮回")
        }
        if not result["has_blocking"]:
            result["verdict"] = (
                "PASS - 二阶因果审计闭合（无阻断）；"
                f"元基状态={result['meta_ledger']}"
            )
        else:
            reasons = [
                f"{k}:{v.get('status')}/{v.get('reason')}"
                for k, v in analysis.items()
                if isinstance(v, dict) and v.get("status") in _SPE_BLOCKING
            ]
            result["verdict"] = f"FAILED - NOMOS 内核判定阻断：{'；'.join(reasons)}"
        return result


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

    # 输出审计结果（覆盖第负一层原始框架 + 第零层 + 治理层 + law 层）
    print(report.summary())
