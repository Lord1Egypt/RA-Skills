"""
第二视角引擎 / Second Perspective Engine (SPE)
=====================================================

版本：以模块常量 SPE_VERSION 为准。

SPL 因果论的规范参考内核 —— 无语义拓扑层 + 十算子流水线 + 叠加螺旋式迭代链路
+ 自主进化层（版本谱系 · 只提案不适用）。

    - 单文件 · 零外部依赖 · 仅用 Python 标准库
    - 所有结构判定均为决定论；不使用概率词；缺失输入直接中断而非猜测
    - LLM 永远不参与结构裁决；所有 status / converged 布尔值由确定性算子给出

--------------------------------------------------------------
从 v2.0 到 SPE 1.0
--------------------------------------------------------------
v2.0（已移除）是扁平线性管道 + 线性 bounded 重试，表达不了「无限因果 / 螺旋重构 /
第二视角全局观测 / 结构化元审计」四件事。SPE 1.0 保留其三处已被验证的内核
（哈希链与封存、LLM 三层护栏、五状态形式化收敛），在其上补一层拓扑：

    v2.0  五算子      NS → IAP → LCH → CCS → ACC
    SPE   十算子      ⊙GA → ⊗NS → ⊕IAP → ⊿LCH → ⊞LFT → BFC → ⚙CCS → ⇄GRF
                      → META → ⊚ACC
    v2.0  线性重试    reconstruct()   —— 每轮 dict.update，覆盖上一层
    SPE   叠加螺旋    spiral()        —— 每层冻结已收敛子图，只增不减
    SPE   极限收敛    limit_reconstruct() / spiral_step() —— 层数无上限，判据停机
    SPE   自主进化    evolve()        —— 发现结构缺口，但永不自己改写判定规则

本文件是仓库内唯一的实现：**没有 plugins/ 包，没有外部适配器**——
十算子、拓扑底座、螺旋编排、自主进化层、双语渲染器全部内联。自上而下即依赖方向：

    分区①  基础类型与决策论   哈希链 / 封存 / 五状态收敛 / LLM 三层护栏 / 责任账户
    分区②  拓扑底座           □ 节点 · → 边 · ⦿ 公理 · △/◇ 相对标签
                              四类并行校验（一致性 · 约束满足 · 拓扑闭合 · 链内时序）
    分区③  十算子             从 ⊙GA 到 ⊚ACC（先定义，后由引擎包装注册）
    分区④  编排层             线性 reconstruct() · 叠加 spiral() 与螺旋层栈
                              · 极限收敛 limit_reconstruct() · 自主进化 evolve()
    分区⑤  视图层             双语报告渲染器 · 人话渲染器（只读，不参与判定）
    分区⑥  demo               冒烟演示

外部只剩两样非插件物：`verify.py` 等测试脚本，以及 `language Standard/` 下的
`.spd` / `.tpg` 语法与 dsl.py 工具链。

--------------------------------------------------------------
十算子 (Ten Operators)
--------------------------------------------------------------
    ⊙  GA   第一原点锚定   Genesis Anchor        原点事件 / 目标稳态 / 能量资源约束
    ⊗  NS    去语义化       Narrative Strip      剥离修辞立场，只留逻辑骨架
    ⊕  IAP   约束挖掘       Implicit Assumption  挖掘未声明前提，逆反校验
    ⊿  LCH   薄弱点加固     Fragility Localization      定位最脆弱变量，算 ΔD
    ⊞  LFT   无标签拓扑图 Label-Free Topology   构建 □/→/⦿ 并跑三类并行校验
    BFC      二元事实校验   Binary Fact Check    断言归约为真/假；不能归约即中断
    ⚙  CCS   链闭合扫描     Chain Closure Scan    逆反 / 反事实 / 信息黑洞
    ⇄  GRF   灰度执行与现实反馈 Gray Feedback      灰度档位 + 现实证伪对齐
    ⊚  ACC 责任锚定       Accountability Anchor         责任闭环 + SHA-256 审计证书

    ⊛ reconstruct()  线性有界重构（v2.0 兼容路径）
    ↻ spiral()       叠加螺旋式迭代链路（p♾️q）

--------------------------------------------------------------
不变式（不可让渡）
--------------------------------------------------------------
    I-1 非猜测     缺失事实/权重/阈值/责任人/交互强度不估算，直接中断并列出补齐条件
    I-2 原点不漂移 螺旋一旦锚定原点，后续层目标改变即 ORIGIN_DRIFT，立即停机
    I-3 叠加不覆盖 已收敛子图冻结后只增不减；解冻即 SUPERPOSITION_VIOLATION
    I-4 时间不可剥离 公理 5：时间序是「链」的构成条件，不是可拆的字段。
                   无单调时序 ⇒ 链不成立（T308）；序被倒置 ⇒ T307；
                   同一对节点多边 ⇒ 分叉违规 T305（平行 ≠ 分支，SPL 是强决定论）
    I-5 进化不自主  evolve() 只出候选，永不自动改写判定规则。三条恒等式：
                   applies_automatically=False · requires_human=True · auto_applied=0。
                   代价必须付清：新增算子/报告键会改变链根，金标须重算并升版本
    I-6 度量不阻断  META 是 T2_SIGNAL，A6 叙事熵 / A10 审计熵增再难看也不阻断。
                   中断只留给「输入不完整」，不留给「指标不好看」
    L-1..L-3       LLM 三层权限（T1 注解 / T2 提案 / T3 叙述），永不裁决、永不改状态
    C-1..C-3       收敛五状态（FIXED_POINT / NO_GAIN / BUDGET_EXHAUSTED / DIVERGED /
                   BLOCKED）；is_true_convergence 严格区分真收敛与预算耗尽

本模块不含任何主观或概率化推测，仅做决定论因果处理。
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Set, Tuple


# ==================== 基础类型与枚举 ====================

# v1.1.0 术语 v2（2026-10）：算子更名 ⊙ORI→⊙GA（Genesis Anchor）/ ⊞TPG→⊞LFT
#         （Label-Free Topology）/ ⊚STATE→⊚ACC（Accountability Anchoring）；
#         CCS 缩写保留，扩展名更改为 Chain Closure Scan。
#         算子名参与 operator_set_hash → 本次更名产生新一代 lineage；
#         旧报告与证书由 Lineage 代际机制承接，不作废。
# 1.2.2：凭证域与 LLM 产物分离 —— 链根只覆盖确定性部分；
#        启用 LLM 增强时另出 narrative_hash。
#        理由：启用 LLM 后，叙述文本（temperature=0.3）与调用记录时间戳（原读墙钟）
#        都被算进 report_hash → 进链根，使「同输入 + 同 nonce + 同 clock ⇒ 同链根」
#        失效，第三方无法跨机复算。
#        本次改动使链根变更，按 I-5 金标须重算：LLM 关闭路径的哈希域未变，
#        但 spe_version 进报告，故根值随之更新。
SPE_VERSION = "1.2.2"
ENGINE_NAME = "Second Perspective Engine"


class ConvergenceState(str, Enum):
    """形式化收敛五状态分类。

    BLOCKED          本轮出现阻断项（必需输入缺失等），立即终止，不算收敛
    BUDGET_EXHAUSTED 跑满 max_loops 或螺旋预算耗尽仍未收敛 —— 不是收敛
    FIXED_POINT      相邻两层的风险集合完全相同 —— 不动点，收敛
    NO_GAIN          风险集合清空且无未决假设 —— 无残留风险，收敛
    DIVERGED         仍有风险或未决假设，且与上层不同 —— 发散，需人工介入

    FIXED_POINT 与 NO_GAIN 都算真收敛，区别在于「停在哪」：
      NO_GAIN      = 停在一片干净的风险区（风险清零）
      FIXED_POINT  = 停在某个风险上不再变化（风险有界但不为零）
    只有 BUDGET_EXHAUSTED 是「跑完了但没跑到」——所以 is_true_convergence
    特意把它排除在外，防止把「时间到了」误当成「想通了」。
    """
    FIXED_POINT = "FIXED_POINT"
    NO_GAIN = "NO_GAIN"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    DIVERGED = "DIVERGED"
    BLOCKED = "BLOCKED"

    @property
    def is_true_convergence(self) -> bool:
        return self in (ConvergenceState.FIXED_POINT, ConvergenceState.NO_GAIN)


class SpiralVerdict(str, Enum):
    """螺旋层终局。与收敛五状态并列存在，不互相替换。

    ConvergenceState 回答「结构收敛了吗」；SpiralVerdict 回答「这圈螺旋
    为什么停下」。两者会同时出现在 spiral() 的返回值里，各自独立可读——
    把它们合并成一个枚举，正是「把时间到了当成想通了」的温床。
    """
    CONVERGED = "CONVERGED"
    BUDGET_EXHAUSTED = "BUDGET_EXHAUSTED"
    AWAITING_HUMAN = "AWAITING_HUMAN"
    ORIGIN_DRIFT = "ORIGIN_DRIFT"
    SUPERPOSITION_VIOLATION = "SUPERPOSITION_VIOLATION"
    BLOCKED = "BLOCKED"

    # —— 极限收敛器（limit_reconstruct / spiral_step）专用 ——
    # 规范元因果基底第二条（并行收敛）：极限处唯一收敛（S∞ = S*）。
    # 「无限」指的是层数无上限地逼近目标稳态，不是跑到天荒地老；
    # 因此下面三个终局判据正是「凭什么停」的可执行答案。
    LIMIT_REACHED = "LIMIT_REACHED"      # 距离归零并连续数层保持 → 抵达 S∞ = S*
    NOT_MONOTONE = "NOT_MONOTONE"        # 距离不再严格下降 → 不再逼近，必须停
    FLAT_SPIRAL = "FLAT_SPIRAL"          # 半径连续数层不降 → 只在原地扩圈
    ADVANCED = "ADVANCED"                # 单层推进成功且仍可继续（非终局）


# ---------------------------------------------------------------------------
# 关于 T1 / T2 / T3：本文件同时存在两套互不相干的 T1/T2/T3 命名，
# 这是本引擎最容易被误读的地方。它们之间没有任何对应关系，不要混用。
#
#   PluginTier（下方）—— 约束「确定性算子」能做什么
#       T1_STRUCTURAL   可产出 BLOCKED/CRITICAL，能真正阻断一次审计
#       T2_SIGNAL       只能产出 WARNING/HIGH_RISK；发阻断会被强制降级
#       T3_NARRATIVE    只能出文字；输出里的 status 会被剥离
#
#   LLMPermissionTier —— 约束「LLM」能做什么，与 PluginTier 毫无关系
#       T1_ANNOTATION   附加批注
#       T2_PROPOSAL     提出建议
#       T3_NARRATIVE    只写叙述文字（默认值，最保守）
#
# 两套唯一的共同点是：数字越小，权限越大。
# 判定 LLM 输出是否越权，看的是 FORBIDDEN_LLM_KEYS，与 PluginTier 无关。
# ---------------------------------------------------------------------------

class PluginTier(str, Enum):
    T1_STRUCTURAL = "T1_STRUCTURAL"   # 可出 BLOCKED（阻断）
    T2_SIGNAL = "T2_SIGNAL"           # 只出风险信号，不得阻断
    T3_NARRATIVE = "T3_NARRATIVE"     # 只出文字，不出 status


class LLMPermissionTier(str, Enum):
    T1_ANNOTATION = "T1_ANNOTATION"
    T2_PROPOSAL = "T2_PROPOSAL"
    T3_NARRATIVE = "T3_NARRATIVE"


class CollapseLevel(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


# ==================== 责任节点 ====================

@dataclass
class ResponsibilityAccount:
    """责任账户。审计结论一律锚定到具体的组织 / 角色 / 阶段。

    nonce 的两难
    ------------
    v2.0 用 uuid4 随机生成 nonce，好处是每次审计身份唯一，代价是
    **同一输入两次运行的链接根哈希不同**，审计证书无法被第三方重算核对。

    SPE 1.0 取决定论一侧：默认由 (organization, role, stage, owner, instance_salt)
    做 SHA-256 推导，因此同账户可复现。需要「同一账户的多次审计彼此可区分」时，
    显式传入不同的 instance_salt 或 nonce 即可——两者都不传，就是可复现模式。
    """

    organization: str
    role: str
    stage: str
    owner: Optional[str] = None
    nonce: Optional[str] = None
    instance_salt: str = ""

    def __post_init__(self) -> None:
        if not self.nonce:
            blob = json.dumps({
                "organization": self.organization,
                "role": self.role,
                "stage": self.stage,
                "owner": self.owner,
                "instance_salt": self.instance_salt,
            }, sort_keys=True, ensure_ascii=False)
            self.nonce = hashlib.sha256(blob.encode("utf-8")).hexdigest()[:8]

    @property
    def is_closed(self) -> bool:
        return bool(self.owner)


# ==================== LLM 协议 ====================

class LLMProvider(Protocol):
    def generate(self, prompt: str, **kwargs) -> str: ...


class OpenAIProvider:
    """零依赖 OpenAI 兼容 LLM 调用。

    数据出境合规提示：
        - 默认 base_url 指向境外 https://api.openai.com/v1，调用即数据出境
        - 境内部署请传入境内端点（DeepSeek/通义千问等）并做输入脱敏
        - SPE 八算子本身从不调用 LLM；仅在显式注入 provider 时启用且强制护栏
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 120,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str, **kwargs) -> str:
        import urllib.error
        import urllib.request

        # 注意：下面把异常**转成字符串返回**而不是向上抛。
        # 因为叙述层是可选增强，它挂掉不应让整次审计失败——
        # 调用方拿到 "[LLM Error] ..." 字符串即可，核心八算子不受影响。
        temperature = kwargs.get("temperature", 0.3)
        max_tokens = kwargs.get("max_tokens", 4096)
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        # 思考型模型（qwen3 等）传 think=False 可直接出正文、且快得多。
        # 显式传 None 时不带该字段 —— 严格实现的服务端会因未知字段报 400。
        think = kwargs.get("think", None)
        if think is not None:
            payload["think"] = bool(think)
        body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                choices = result.get("choices") or []
                msg = (choices[0].get("message") if choices else None) or {}
                text = str(msg.get("content") or "").strip()
                if not text and kwargs.get("reasoning_fallback", True):
                    # 思考型模型（qwen3 等）的正文会落在 reasoning 字段，content 为空。
                    # 但 reasoning 是模型的思考过程、不是结论 —— 要求精确输出的调用方
                    # （如人话改写）应传 reasoning_fallback=False：宁可空着，也不要把
                    # 模型的自我分析当成审计结论递给用户。
                    text = str(msg.get("reasoning_content") or msg.get("reasoning") or "").strip()
                return text
        except urllib.error.HTTPError as e:
            return f"[LLM Error] HTTP {e.code}: {e.read().decode('utf-8', errors='replace')[:200]}"
        except Exception as e:
            return f"[LLM Error] {e}"


@dataclass
class LLMCallRecord:
    """一次 LLM 调用的留痕。

    permission_tier  当时生效的权限层级
    prompt_hash      prompt 的 SHA-256 前 16 位——**只存哈希不存原文**：
                     既能证明用了哪个 prompt，又避免把决策数据写进日志
    response_excerpt 剥离裁决字段后的响应摘要（最多 400 字）
    stripped         是否发生过字段剥离
    adjudicated      恒为 False。按护栏 L-1..L-3，LLM 永不参与裁决；
                     这个字段存在的意义就是在审计记录里显式证明这一点，
                     任何人翻到报告都能看到「LLM 没有裁决权」
    """

    permission_tier: LLMPermissionTier
    purpose: str
    prompt_hash: str
    response_excerpt: str
    stripped: bool = True
    adjudicated: bool = False
    timestamp: float = field(default_factory=time.time)


# ==================== 审计事件与哈希链 ====================

@dataclass
class AuditEvent:
    event_type: str
    payload: Dict[str, Any]
    prev_hash: str
    timestamp: float = field(default_factory=time.time)
    nonce: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    # 封存哈希：在 _append_event 时一次性写入。其后任何对 payload / event_type /
    # timestamp / nonce 的改动都会使 hash 与 sealed_hash 不一致，从而被 verify_chain 检出。
    # 为 None 表示该事件未经封存，内容不可验证。
    sealed_hash: Optional[str] = None

    @property
    def hash(self) -> str:
        """本事件的链上哈希。三个 json 参数都有讲究，不能随手改：

        sort_keys=True     键序不影响结果，字典构造顺序无关紧要
        ensure_ascii=False 中文按原字符参与哈希，避免编码路径差异
        default=str        datetime 之类不可序列化的对象退化为字符串，
                          宁可损失精度也不让整条链崩掉

        注意：这个属性是**实时重算**的，任何事后修改都会改变它的返回值。
        因此 verify_chain 不拿它当基准，而拿 _append_event 时写下的
        sealed_hash 当基准——否则比对恒成立，篡改检测形同虚设。
        """
        blob = json.dumps({
            "event_type": self.event_type,
            "payload": self.payload,
            "prev_hash": self.prev_hash,
            "timestamp": self.timestamp,
            "nonce": self.nonce,
        }, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ==================== 审计插件 ====================

@dataclass
class AuditPlugin:
    name: str
    tier: PluginTier
    analyze_func: Callable[[Dict[str, Any]], Any]
    description: str = ""
    # core = 官方十算子（load_core_plugins 装载）；extension = 经唯一插件缝注册
    origin: str = "core"
    # 扩展算子的显式定序锚点：紧随哪个算子之后执行
    registered_after: Optional[str] = None


# ==================== 收敛判定器 ====================

class ConvergenceChecker:
    """形式化收敛判定（P-1 终止 / P-2 不动点 / P-3 风险有界）。"""

    BLOCKING_STATUSES = {"BLOCKED", "CRITICAL"}
    HIGH_RISK_STATUSES = {"HIGH_RISK"}

    @staticmethod
    def classify(
        round_idx: int,
        max_rounds: int,
        previous_risks: frozenset,
        current_risks: frozenset,
        has_blocking: bool,
        has_unresolved_assumptions: bool,
    ) -> ConvergenceState:
        # 判定是一张**优先级链**，从上到下第一个命中即返回，顺序不可调换：
        #   1. has_blocking                → BLOCKED
        #   2. round_idx >= max_rounds     → BUDGET_EXHAUSTED
        #   3. 与上层风险集合同样且无未决  → FIXED_POINT
        #   4. 风险清空且无未决            → NO_GAIN
        #   5. 其余                        → DIVERGED
        #
        # 为什么阻断排在最前：必需输入缺失时，后面任何「看起来收敛了」
        # 的信号都不可信——风险集清零可能只是因为算子根本没拿到输入。
        #
        # 第 3 条要求 round_idx > 0：首层没有「上层」可比，必须落到后面几条。
        if has_blocking:
            return ConvergenceState.BLOCKED
        if round_idx >= max_rounds:
            return ConvergenceState.BUDGET_EXHAUSTED
        if round_idx > 0 and previous_risks == current_risks and not has_unresolved_assumptions:
            return ConvergenceState.FIXED_POINT
        if not current_risks and not has_unresolved_assumptions:
            return ConvergenceState.NO_GAIN
        return ConvergenceState.DIVERGED

    @staticmethod
    def extract_risk_set(report: Dict[str, Any]) -> Tuple[frozenset, bool]:
        # 风险键的构成是 (算子名, status, 结果的规范化 JSON)。
        # 必须把整个结果序列化进去，只比较 status 会漏掉
        # 「同一个 WARNING 但内容变了」这种情况——
        # 而那恰恰是 FIXED_POINT 需要识别的变化。
        risks = set()
        has_blocking = False
        for pname, result in report.get("analysis", {}).items():
            if not isinstance(result, dict):
                continue
            status = result.get("status")
            if status is None:
                # 五算子插件输出 pass/halt_count 而非 status，不归一化则该插件级
                # HALT 对收敛判定不可见。halt_count>0 视为结构性阻断（T1 才允许），
                # 其余 pass=False 只作 HIGH_RISK 信号（T2 算子不得阻断）。
                halt = result.get("halt_count")
                if isinstance(halt, int) and halt > 0:
                    status = "BLOCKED"
                elif result.get("pass") is False:
                    status = "HIGH_RISK"
            if status in ConvergenceChecker.BLOCKING_STATUSES:
                has_blocking = True
                risks.add((pname, status, json.dumps(result, sort_keys=True, default=str, ensure_ascii=False)))
            elif status in ConvergenceChecker.HIGH_RISK_STATUSES or status == "WARNING":
                risks.add((pname, status, json.dumps(result, sort_keys=True, default=str, ensure_ascii=False)))
        return frozenset(risks), has_blocking


# ==================== 配置加载器 ====================

class AuditConfigLoader:
    @staticmethod
    def load_from_dict(config: Dict[str, Any]) -> Dict[str, Any]:
        return config

    @staticmethod
    def load_from_json(path: str) -> Dict[str, Any]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)




# ============================================================================
# 分区② 拓扑底座 — 无语义因果拓扑 / De-semantic Causal Topology
# ============================================================================
# TOPOLOGY — 无语义因果拓扑底座 / De-semantic Causal Topology Substrate
# =====================================================================
#
# 本模块是「第二视角引擎 SPE 1.0」的拓扑层底座，对齐腾讯文档规范
# 《SPL因果论 · 无语义拓扑语法规范》的符号体系与编译期校验机制。
#
# 符号表（无语义：符号不携带语义，语义由算子在运算中生成）
# --------------------------------------------------------
#   □   实体节点        无固有属性，仅代表拓扑位置；删除所有连接边后自动消失
#   →   因果有向边      带约束参数（weight / validity），方向决定两端的相对标签
#   ⦿   全局公理约束    不可修改，全局生效
#   △   上游节点（相对标签）  对下游表现为「可证伪的输入假设」
#   ◇   下游节点（相对标签）  对上游表现为「不可篡改的输出决策」
#   ✅ / ❌  编译状态
#
# 相对标签定理
# ------------
#   1. 标签相对：同一节点在 A→B 链上是 ◇，在 B→C 链上就是 △，无固定语义。
#   2. 标签无副作用：推演可完全剥离标签进行纯结构运算，不影响收敛结果。
#   3. 标签不参与判定：本模块只提供标签映射函数，任何判定都不读标签。
#
# 三类并行约束校验（编译期自动执行，无串行等待）
# ----------------------------------------------
#   一致性校验 consistency   节点全局身份唯一、无自相矛盾的边定义      致命，直接终止
#   约束满足校验 constraint  所有边参数符合全局公理 ⦿，无越界            致命，直接终止
#   拓扑闭合校验 closure     无悬空节点/边、无因果悖论（含自环）        警告，可强制继续但结果无效
#
# 确定性 · 零随机 · 零 LLM 调用 · 零外部依赖
# ----------------------------------------------------------------------------

TOPOLOGY_VERSION = "1.0.0"
# 拓扑层**文法**版本：与 TOPOLOGY_VERSION（底座结构版本）分开记。
# 文法增补（如 2026.3 的链内时序 t、元因果账本字段）没有改动底座结构，
# 但必须可追溯到「这条链是在哪一版语法下产生的」，否则跨代际比对无从谈起。
TOPOLOGY_GRAMMAR_VERSION = "2026.3"

# ── 无语义符号表 ──
SYM_NODE = "□"
SYM_EDGE = "→"
SYM_CONSTRAINT = "⦿"
SYM_UPSTREAM = "△"
SYM_DOWNSTREAM = "◇"
SYM_PASS = "✅"
SYM_FAIL = "❌"

# 相对标签常量（唯一来源，禁止在别处硬编码 △/◇）
REL_INPUT = SYM_UPSTREAM      # 对下游表现为可证伪的输入假设
REL_OUTPUT = SYM_DOWNSTREAM   # 对上游表现为不可篡改的输出决策

# ── 校验分级 ──
SEVERITY_HALT = "HALT"        # 致命：直接终止推演
SEVERITY_WARN = "WARN"        # 警告：可强制继续，但结果无效

CHECK_CONSISTENCY = "consistency"
CHECK_CONSTRAINT = "constraint"
CHECK_CLOSURE = "closure"
# 第四个并行进程：链内时序（公理 5「绝对前提：时间」）。
# 之所以单列而不并入 closure：闭合问「图自洽吗」，时序问「这张图还是不是一条链」。
# 两者可以同时通过、也可以各自失败，语义不可合并。
CHECK_TIME_ORDER = "time_order"

# ── 诊断码 ──
T101_ROLE_CONFLICT = "T101"      # 同一 (src,dst) 同时存在 requires 与 depends_on
T102_CONTRADICTORY_EDGE = "T102" # 同一 (src,dst,relation) 重复且参数不一致
T201_PARAM_OUT_OF_RANGE = "T201"
T202_REQUIRED_PARAM_MISSING = "T202"
T203_DEGREE_EXCEEDED = "T203"
T301_DANGLING_EDGE = "T301"
T302_DANGLING_NODE = "T302"
T303_CAUSAL_PARADOX = "T303"     # 有向环 / 自环 = 因果悖论
# —— 公理 5 专用诊断码（语法扩展 2026.3）——
T305_FORK_VIOLATION = "T305"     # 同一对节点被声明多条边 = 未来在节点上分叉
T307_TIME_ORDER_INVERTED = "T307"   # 声明时序与链内派生序冲突 = 序被倒置
T308_TIME_UNASSIGNABLE = "T308"     # 无法赋予单调时序（有环）= 链不成立

# 允许的因果边关系（与 decision.ebnf 的 verb 保持一致）
ALLOWED_RELATIONS = ("causal", "requires", "depends_on")


# ==================== 数据结构 ====================

@dataclass
class TopoNode:
    """□ 实体节点。

    无语义：不承载「决策 / 假设 / 实体」等任何语义属性。
    id 是它在拓扑中的唯一定位；其余字段只是外部映射的挂载点。
    """

    id: str
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "note": self.note}


@dataclass
class TopoEdge:
    """→ 因果有向边。

    relation    causal | requires | depends_on（与 .spd 的 verb 对齐）
    weight      边权；是否越界由 ⦿ 约束判定，本类不自行设限
    validity    有效期描述（字符串，不做时间运算）
    falsifiable 该边作为输入时是否可证伪（不可证伪 = 失效无预警）
    delta_d     该边失效时下游的结构性变更 ΔD（描述，不是建议）
    t           链内时序（公理 5「时间即链之序」）。

        规范公理 5 把时间定为**构成条件**而非可拆分支：「前置因先于后继果，
        因果结构不可自我循环……剥离、透视、对冲、锚定、重构五大算子的全部操作，
        都在该前提下进行」。所以时序不是附加字段，而是「链」这个概念成立的前提。

        None  = 未声明，由 TopologyGraph.assign_time_order() 按最长路径确定性派生
        非 None = 显式声明的链内序，必须满足 t(前置) < t(后继)，否则 T307。

        为什么 t 可选而非必填：存量 .spd / 投影拓扑不声明时序时，其派生序仍可
        被完整算出（派生序是纯结构的函数），因此**默认为 None 不改变任何既有
        拓扑指纹**；只有真正声明了时序的拓扑，其结构才因此不同。
    """

    src: str
    dst: str
    relation: str = "causal"
    weight: Optional[float] = None
    validity: Optional[str] = None
    falsifiable: bool = True
    delta_d: Optional[str] = None
    note: str = ""
    t: Optional[int] = None

    @property
    def key(self) -> Tuple[str, str, str]:
        return (self.src, self.dst, self.relation)

    @property
    def shape(self) -> Tuple[str, str]:
        return (self.src, self.dst)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "src": self.src, "dst": self.dst, "relation": self.relation,
            "weight": self.weight, "validity": self.validity,
            "falsifiable": self.falsifiable, "delta_d": self.delta_d,
            "note": self.note, "t": self.t,
        }


@dataclass
class Constraint:
    """⦿ 全局公理约束。不可修改，全局生效。

    kind = weight_range        params {"lo": 0.0, "hi": 1.0}
    kind = max_out_degree      params {"max": 4}
    kind = required_param      params {"param": "weight"}
    """

    name: str
    kind: str
    params: Dict[str, Any] = field(default_factory=dict)
    note: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "kind": self.kind,
                "params": self.params, "note": self.note}


@dataclass
class ValidationIssue:
    code: str
    check: str
    severity: str
    message: str
    where: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {"code": self.code, "check": self.check, "severity": self.severity,
                "message": self.message, "where": self.where}


def default_constraints() -> Dict[str, Constraint]:
    """规范默认的 ⦿ 全局约束集。

    注意：拓扑闭合（含无环）不放在这里——规范把「无因果悖论」列为
    闭合校验（警告级），与「参数不越界」的致命级约束是两个进程。
    """
    return {
        "weight_range": Constraint(
            name="weight_range", kind="weight_range",
            params={"lo": 0.0, "hi": 1.0},
            note="边权必须落在闭区间内，否则视为越界",
        ),
    }


# ==================== 拓扑图 ====================

@dataclass
class TopologyGraph:
    """G = (□, →, ⦿)。节点无固有属性，关系优先于实体。"""

    nodes: Dict[str, TopoNode] = field(default_factory=dict)
    edges: List[TopoEdge] = field(default_factory=list)
    constraints: Dict[str, Constraint] = field(default_factory=dict)
    layer: int = 0
    provenance: List[Dict[str, Any]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.constraints:
            self.constraints = default_constraints()

    # -------- 变更 --------

    def add_node(self, node_id: str, note: str = "") -> str:
        if node_id not in self.nodes:
            self.nodes[node_id] = TopoNode(id=node_id, note=note)
        return node_id

    def add_edge(self, edge: TopoEdge) -> TopoEdge:
        # 关系优先于实体：边会隐式创建它连接的两个节点
        self.add_node(edge.src)
        self.add_node(edge.dst)
        self.edges.append(edge)
        return edge

    def trace(self, operator: str, action: str, detail: Dict[str, Any]) -> None:
        """结构化元审计：每一次算子作用于拓扑都留痕。

        留痕只记「谁、对拓扑做了什么、拓扑长什么样」——
        不记语义判断，因为本层不产生语义。
        """
        self.provenance.append({
            "layer": self.layer,
            "operator": operator,
            "action": action,
            "detail": detail,
        })

    def clone(self, layer: Optional[int] = None) -> "TopologyGraph":
        """深拷贝一层。螺旋叠加时为上层留一份不可变快照。"""
        return TopologyGraph(
            nodes={k: TopoNode(v.id, v.note) for k, v in self.nodes.items()},
            edges=[TopoEdge(**e.to_dict()) for e in self.edges],
            constraints={k: Constraint(c.name, c.kind, dict(c.params), c.note)
                         for k, c in self.constraints.items()},
            layer=self.layer if layer is None else layer,
            provenance=[dict(p) for p in self.provenance],
        )

    def freeze(self, node_ids: Sequence[str]) -> List[str]:
        """冻结已收敛子图：被冻结的节点在后续螺旋层不再重开。"""
        frozen = sorted({n for n in node_ids if n in self.nodes})
        self.trace("↻SPR", "FREEZE", {"frozen_nodes": frozen})
        return frozen

    # -------- 相对标签（仅供外部映射，不参与判定） --------

    def relative_label(self, edge: TopoEdge, endpoint: str) -> str:
        """相对标签定理：同一条边，上游端是 △，下游端是 ◇。

        标签无副作用——推演过程可完全剥离标签，不影响任何判定结果。
        """
        if endpoint == edge.src:
            return REL_INPUT
        if endpoint == edge.dst:
            return REL_OUTPUT
        return ""

    def labels(self) -> Dict[str, Dict[str, List[str]]]:
        """全图相对标签映射。同一节点可同时是 △ 与 ◇。"""
        out: Dict[str, Dict[str, List[str]]] = {
            n: {"upstream": [], "downstream": []} for n in self.nodes
        }
        for e in self.edges:
            if e.src in out:
                out[e.src]["upstream"].append(e.dst)
            if e.dst in out:
                out[e.dst]["downstream"].append(e.src)
        return out

    def adjacency(self) -> Dict[str, List[str]]:
        """出邻接表。节点全部列出（含无出边的节点），顺序确定。"""
        adj: Dict[str, List[str]] = {n: [] for n in sorted(self.nodes)}
        for e in self.edges:
            if e.src in adj:
                adj[e.src].append(e.dst)
        return adj

    def find_cycles(self) -> List[List[str]]:
        """定位所有有向环（含自环）= 因果悖论 A→B→C→¬A。

        迭代式 DFS 三色标记，确定性遍历顺序（节点按 id 排序），
        环路径按发现顺序返回；不追求「所有环」的完备枚举，
        只保证「有环必报」且路径可复核。
        """
        WHITE, GREY, BLACK = 0, 1, 2
        color: Dict[str, int] = {n: WHITE for n in sorted(self.nodes)}
        adj: Dict[str, List[str]] = {n: [] for n in sorted(self.nodes)}
        for e in self.edges:
            if e.src in adj:
                adj[e.src].append(e.dst)

        cycles: List[List[str]] = []
        seen_signature: Set[Tuple[str, ...]] = set()

        for root in sorted(self.nodes):
            if color[root] != WHITE:
                continue
            stack: List[Tuple[str, int]] = [(root, 0)]
            path: List[str] = []
            while stack:
                node, idx = stack[-1]
                if idx == 0:
                    color[node] = GREY
                    path.append(node)
                if idx < len(adj.get(node, [])):
                    stack[-1] = (node, idx + 1)
                    nxt = adj[node][idx]
                    if nxt not in color:
                        continue
                    if color[nxt] == GREY:
                        # 找到回边：截取环路径
                        try:
                            start = path.index(nxt)
                        except ValueError:
                            start = 0
                        cyc = path[start:] + [nxt]
                        sig = tuple(sorted(cyc))
                        if sig not in seen_signature:
                            seen_signature.add(sig)
                            cycles.append(cyc)
                    elif color[nxt] == WHITE:
                        stack.append((nxt, 0))
                else:
                    color[node] = BLACK
                    path.pop()
                    stack.pop()
        return cycles

    # -------- 公理 5：链内时序 --------

    def assign_time_order(self) -> Dict[str, Any]:
        """赋予全图链内时序 t（公理 5）。

        规范原文：「时间即链之序……前置因先于后继果，因果结构不可自我循环。
        没有这一前提，『链』这个概念本身无法成立——因果链的『链』，
        其含义就是可排序。」因此本方法是「这张图还能不能叫一条链」的判定器。

        规则（全部确定性，无随机、无估算）
        ----------------------------------
        1. 时序 t 按**最长路径**派生：入度 0 的节点为 t=0，其余 t = max(前置 t) + 1。
           用最长路径而非最短路径，是因为「前置因先于后继果」要求 t 必须晚于
           **全部**前置因，否则序就只是某一条路径的序，而不是链的序。
        2. 若存在有向环，则不存在单调赋值 —— 报 unassignable，链不成立（T308）。
           这也解释了规范为什么强调因果承接不是链的自环：自环会让序无处安放。
        3. 观测位置：规范原文「一个观测者本身就是一条类时曲线，因此只能位于一条
           链上」。故此处同时给出 observer_anchor —— 本次审计所站的那条链的起点。
           它是 □0（第一原点）在拓扑中的镜像；无原点节点时退回唯一的起点，
           多起点且无原点时为空（此时「站在哪条链上」这件事没有被声明）。
        4. 平行 ≠ 分支：平行是「多条各自有序的链」，表现为多个 roots，**合法**；
           分支是「未来在某个节点真的分叉」，表现为同一对节点被声明多条边（T305），
           规范明确「SPL 是强决定论，只承认前者」。
        """
        nodes = sorted(self.nodes)
        indeg: Dict[str, int] = {n: 0 for n in nodes}
        adj: Dict[str, List[str]] = {n: [] for n in nodes}
        for e in self.edges:
            if e.src in adj:
                adj[e.src].append(e.dst)
            if e.dst in indeg:
                indeg[e.dst] += 1

        roots = [n for n in nodes if indeg[n] == 0]

        # --- 最长路径序（Kahn，队列按 id 排序保证跨进程一致）---
        t: Dict[str, int] = {n: 0 for n in roots}
        remaining = dict(indeg)
        queue: List[str] = sorted(roots)
        visited: Set[str] = set()
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            for nxt in sorted(adj.get(node, [])):
                t[nxt] = max(t.get(nxt, 0), t.get(node, 0) + 1)
                remaining[nxt] -= 1
                if remaining[nxt] <= 0:
                    queue.append(nxt)
                    queue.sort()
        unassignable = [n for n in nodes if n not in visited]

        # --- 分叉：同一对节点被声明多条边（平行 ≠ 分支）---
        shapes: Dict[Tuple[str, str], int] = {}
        for e in self.edges:
            shapes[e.shape] = shapes.get(e.shape, 0) + 1
        forks = [{"src": s[0], "dst": s[1], "count": c}
                 for s, c in sorted(shapes.items()) if c > 1]

        # --- 声明时序与派生序冲突：序被倒置 ---
        inverted: List[Dict[str, Any]] = []
        for e in self.edges:
            if e.t is None:
                continue
            src_t = t.get(e.src, 0)
            dst_t = t.get(e.dst, 0)
            if e.t < src_t or e.t >= dst_t:
                inverted.append({
                    "edge": f"{e.src}→{e.dst}",
                    "declared": e.t,
                    "expected_range": [src_t, dst_t - 1],
                })

        # --- 观测位置：这条链的起点 ---
        if SYM_NODE + "0" in self.nodes:
            anchor = SYM_NODE + "0"
        elif len(roots) == 1:
            anchor = roots[0]
        else:
            anchor = ""

        seen: Set[str] = set()
        if anchor:
            stack = [anchor]
            while stack:
                cur = stack.pop()
                if cur in seen:
                    continue
                seen.add(cur)
                stack.extend(adj.get(cur, []))

        return {
            "assignable": not unassignable,
            "node_order": dict(sorted(t.items())),
            "roots": roots,
            "parallel_chains": len(roots),
            "forks": forks,
            "inverted": inverted,
            "unassignable": unassignable,
            "observer_anchor": anchor,
            "observer_chain_size": len(seen),
            "max_depth": max(t.values()) if t else 0,
        }

    # -------- 序列化 --------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "topology_version": TOPOLOGY_VERSION,
            "layer": self.layer,
            "symbols": {"node": SYM_NODE, "edge": SYM_EDGE, "constraint": SYM_CONSTRAINT},
            "nodes": [self.nodes[k].to_dict() for k in sorted(self.nodes)],
            "edges": [e.to_dict() for e in self.edges],
            "constraints": [self.constraints[k].to_dict() for k in sorted(self.constraints)],
            "provenance": self.provenance,
            "time_order": self.assign_time_order(),
        }

    def graph_hash(self) -> str:
        """拓扑指纹：仅由纯结构决定，与标签、与 provenance 无关。

        含声明时序 t（公理 5 把时间定为构成条件，故它属于结构）；
        但 t 默认为 None，因此**未声明时序的拓扑指纹与本字段引入前完全一致**——
        既能表达时序，又不会让存量拓扑凭空换指纹。
        """
        blob = json.dumps({
            "nodes": sorted(self.nodes),
            "edges": sorted(
                [e.src, e.dst, e.relation, e.weight, e.validity, e.falsifiable, e.t]
                for e in self.edges
            ),
            "constraints": sorted(
                [k, c.kind, json.dumps(c.params, sort_keys=True)]
                for k, c in self.constraints.items()
            ),
        }, sort_keys=True, ensure_ascii=False, default=str)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()


# ==================== 三类并行校验 ====================

class TopologyValidator:
    """编译期并行校验：一致性 / 约束满足 / 拓扑闭合。

    三个进程互不串行等待，任何一步不通过即返回编译状态；
    致命错误终止推演，闭合警告允许强制继续但结果标记为无效。
    """

    # -------- 进程一：一致性（致命） --------

    @staticmethod
    def check_consistency(g: TopologyGraph) -> Dict[str, Any]:
        issues: List[ValidationIssue] = []

        # 节点全局身份唯一
        lowered: Dict[str, List[str]] = {}
        for nid in g.nodes:
            lowered.setdefault(nid.lower(), []).append(nid)
        for key, members in sorted(lowered.items()):
            if len(members) > 1:
                issues.append(ValidationIssue(
                    T101_ROLE_CONFLICT, CHECK_CONSISTENCY, SEVERITY_HALT,
                    f"节点身份不唯一：{members} 仅大小写不同，视为同一身份的冲突定义",
                    where=f"nodes={members}",
                ))

        # 自相矛盾的边定义
        shapes: Dict[Tuple[str, str], Set[str]] = {}
        by_key: Dict[Tuple[str, str, str], List[TopoEdge]] = {}
        for e in g.edges:
            shapes.setdefault(e.shape, set()).add(e.relation)
            by_key.setdefault(e.key, []).append(e)

        for shape, relations in sorted(shapes.items()):
            if len(relations) > 1:
                issues.append(ValidationIssue(
                    T101_ROLE_CONFLICT, CHECK_CONSISTENCY, SEVERITY_HALT,
                    f"边 {shape[0]}→{shape[1]} 同时声明了互相矛盾的关系 {sorted(relations)}",
                    where=f"edge={shape[0]}→{shape[1]}",
                ))

        for key, group in sorted(by_key.items()):
            if len(group) < 2:
                continue
            sigs = {(e.weight, e.validity, e.falsifiable) for e in group}
            if len(sigs) > 1:
                issues.append(ValidationIssue(
                    T102_CONTRADICTORY_EDGE, CHECK_CONSISTENCY, SEVERITY_HALT,
                    f"边 {key[0]}→{key[1]}({key[2]}) 重复定义且参数不一致 {sorted(sigs, key=str)}",
                    where=f"edge={key[0]}→{key[1]}({key[2]})",
                ))

        halts = [i for i in issues if i.severity == SEVERITY_HALT]
        return {
            "check": CHECK_CONSISTENCY,
            "status": SYM_FAIL if halts else SYM_PASS,
            "fatal": bool(halts),
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 进程二：约束满足（致命） --------

    @staticmethod
    def check_constraints(g: TopologyGraph) -> Dict[str, Any]:
        issues: List[ValidationIssue] = []
        by_kind: Dict[str, List[Constraint]] = {}
        for c in g.constraints.values():
            by_kind.setdefault(c.kind, []).append(c)

        # ⦿ weight_range：所有显式声明的边权必须落在区间内
        ranges = by_kind.get("weight_range", [])
        if ranges:
            lo = min(float(c.params.get("lo", 0.0)) for c in ranges)
            hi = max(float(c.params.get("hi", 1.0)) for c in ranges)
            for e in g.edges:
                if e.weight is None:
                    continue
                if not (lo <= float(e.weight) <= hi):
                    issues.append(ValidationIssue(
                        T201_PARAM_OUT_OF_RANGE, CHECK_CONSTRAINT, SEVERITY_HALT,
                        f"边 {e.src}→{e.dst} 的 weight={e.weight} 越界 [{lo}, {hi}]",
                        where=f"edge={e.src}→{e.dst}",
                    ))

        # ⦿ required_param：声明为必填的参数不得缺位
        for c in by_kind.get("required_param", []):
            param = c.params.get("param")
            for e in g.edges:
                if getattr(e, str(param), None) is None:
                    issues.append(ValidationIssue(
                        T202_REQUIRED_PARAM_MISSING, CHECK_CONSTRAINT, SEVERITY_HALT,
                        f"边 {e.src}→{e.dst} 缺少必需参数 {param}",
                        where=f"edge={e.src}→{e.dst}",
                    ))

        # ⦿ max_out_degree：出度上限
        for c in by_kind.get("max_out_degree", []):
            cap = int(c.params.get("max", 0))
            out_deg: Dict[str, int] = {}
            for e in g.edges:
                out_deg[e.src] = out_deg.get(e.src, 0) + 1
            for nid, deg in sorted(out_deg.items()):
                if deg > cap:
                    issues.append(ValidationIssue(
                        T203_DEGREE_EXCEEDED, CHECK_CONSTRAINT, SEVERITY_HALT,
                        f"节点 {nid} 出度 {deg} 超过 ⦿ 上限 {cap}",
                        where=f"node={nid}",
                    ))

        halts = [i for i in issues if i.severity == SEVERITY_HALT]
        return {
            "check": CHECK_CONSTRAINT,
            "status": SYM_FAIL if halts else SYM_PASS,
            "fatal": bool(halts),
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 进程三：拓扑闭合（警告，结果无效） --------

    @staticmethod
    def check_closure(g: TopologyGraph) -> Dict[str, Any]:
        issues: List[ValidationIssue] = []

        # 悬空边：端点不在节点集内
        for e in g.edges:
            dangling = [p for p in (e.src, e.dst) if p not in g.nodes]
            if dangling:
                issues.append(ValidationIssue(
                    T301_DANGLING_EDGE, CHECK_CLOSURE, SEVERITY_WARN,
                    f"悬空边 {e.src}→{e.dst}：端点 {dangling} 未声明为节点",
                    where=f"edge={e.src}→{e.dst}",
                ))

        # 悬空节点：无任何入边或出边
        touched: Set[str] = set()
        for e in g.edges:
            touched.add(e.src)
            touched.add(e.dst)
        for nid in sorted(g.nodes):
            if nid not in touched:
                issues.append(ValidationIssue(
                    T302_DANGLING_NODE, CHECK_CLOSURE, SEVERITY_WARN,
                    f"悬空节点 {SYM_NODE}{nid}：无任何连接边，按「关系优先于实体」应自动消失",
                    where=f"node={nid}",
                ))

        # 因果悖论：有向环（自环 A→A 亦属其中）
        for cyc in g.find_cycles():
            path = " → ".join(cyc)
            issues.append(ValidationIssue(
                T303_CAUSAL_PARADOX, CHECK_CLOSURE, SEVERITY_WARN,
                f"因果悖论：{path} 自我循环，链不可排序（绝对前提：时间序）",
                where=f"cycle={path}",
            ))

        fatal = any(i.severity == SEVERITY_HALT for i in issues)
        return {
            "check": CHECK_CLOSURE,
            "status": SYM_FAIL if issues else SYM_PASS,
            "fatal": fatal,          # 闭合问题恒为警告级，fatal 恒 False
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 进程四：链内时序（警告，结果无效） --------

    @staticmethod
    def check_time_order(g: TopologyGraph) -> Dict[str, Any]:
        """公理 5 校验：这张图还成不成立为「一条链」。

        与闭合校验的分工：
            闭合  问「图自洽吗」   —— 悬空、有环
            时序  问「序排得出来吗、排出来被倒置了吗、未来分叉了吗」
        两者可各自独立失败，因此不可合并成一个进程。

        级别沿用规范的分级（警告，可强制继续但结果无效）——
        本层不自行发明致命级别，也不把规范里的警告擅自升级。
        """
        order = g.assign_time_order()
        issues: List[ValidationIssue] = []

        # T305 分叉：同一对节点被声明多条边
        for fork in order["forks"]:
            issues.append(ValidationIssue(
                T305_FORK_VIOLATION, CHECK_TIME_ORDER, SEVERITY_WARN,
                f"分叉违规：{fork['src']}→{fork['dst']} 被声明 {fork['count']} 条边 — "
                f"同一对因果不容许两个未来（平行 ≠ 分支）",
                where=f"edge={fork['src']}→{fork['dst']}",
            ))

        # T307 序被倒置：声明时序与链内派生序冲突
        for item in order["inverted"]:
            issues.append(ValidationIssue(
                T307_TIME_ORDER_INVERTED, CHECK_TIME_ORDER, SEVERITY_WARN,
                f"时序倒置：{item['edge']} 声明 t={item['declared']}，"
                f"但链内序要求落在 {item['expected_range']}（前置因必须先于后继果）",
                where=f"edge={item['edge']}",
            ))

        # T308 序排不出来：有向环使单调赋值不存在
        if order["unassignable"]:
            issues.append(ValidationIssue(
                T308_TIME_UNASSIGNABLE, CHECK_TIME_ORDER, SEVERITY_WARN,
                f"无法赋予单调时序：节点 {order['unassignable']} 落在有向环上 — "
                f"时间是不可剥离的构成条件，无时序则「链」不成立",
                where=f"nodes={order['unassignable']}",
            ))

        return {
            "check": CHECK_TIME_ORDER,
            "status": SYM_FAIL if issues else SYM_PASS,
            "fatal": False,          # 时序问题恒为警告级，与 closure 同级
            "issues": [i.to_dict() for i in issues],
        }

    # -------- 并行调度 --------

    @classmethod
    def run_all(cls, g: TopologyGraph) -> Dict[str, Any]:
        """四个进程并行执行，任一致命即终止推演。

        result_valid 与 pass 的差别是本模块的关键语义：
          pass         四个进程全 ✅
          fatal        存在致命错误 —— 推演终止，无结果
          result_valid 无致命错误，但可能有闭合/时序警告 —— 可强制继续，**结果无效**

        时序进程是「语法扩展 2026.3」新增（公理 5 的落地）：它无致命级，
        因此不会改变「哪些输入会被阻断」这一既有事实，只会改变「结果是否有效」。
        """
        consistency = cls.check_consistency(g)
        constraint = cls.check_constraints(g)
        closure = cls.check_closure(g)
        time_order = cls.check_time_order(g)

        parts = (consistency, constraint, closure, time_order)
        fatal = any(p["fatal"] for p in parts)
        ok = all(p["status"] == SYM_PASS for p in parts)

        return {
            "consistency": consistency,
            "constraint": constraint,
            "closure": closure,
            "time_order": time_order,
            "compile_status": SYM_FAIL if fatal else SYM_PASS,
            "pass": ok,
            "fatal": fatal,
            "result_valid": (not fatal)
                            and closure["status"] == SYM_PASS
                            and time_order["status"] == SYM_PASS,
            "halt_count": sum(
                1 for part in parts
                for i in part["issues"] if i["severity"] == SEVERITY_HALT
            ),
            "warn_count": sum(
                1 for part in parts
                for i in part["issues"] if i["severity"] == SEVERITY_WARN
            ),
        }


# ==================== 上层语言投影（.spd ⇄ 拓扑） ====================

def build_from_decision_context(ctx: Dict[str, Any],
                                origin: Optional[str] = None) -> TopologyGraph:
    """把上层决策上下文投影成无语义拓扑 G0。

    投影规则（刻意保持机械、不含任何语义推断）：
        □0      原点事件        （第一原点，若声明）
        □D      决策节点        ← decision / p / premise / action
        □Q      结果节点        ← outcome / q / result / consequence
        □Ai     每条假设        ← assumptions / premises / hypotheses
        □ΔDj    每条分支响应    ← branches[].delta_d
        →       依赖          Ai requires Aj   ← dependencies {"Ai": ["Aj"]}
        →       输入边         Ai → □D
        →       主干边         □0 → □D → □Q
        →       分支边         Ai → □ΔDj（边携带 delta_d：该边失效时的结构性变更）

    只做连接，不做解释——这正是 ⊗ 去语义化的力学后果。
    """
    g = TopologyGraph(layer=0)

    def _first_str(*keys: str) -> str:
        for k in keys:
            v = ctx.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return ""

    origin_text = origin or _first_str("origin", "origin_event")
    decision = _first_str("decision", "p", "premise", "action")
    outcome = _first_str("outcome", "q", "result", "consequence")

    if origin_text:
        g.add_node("□0", note="原点事件")
        g.trace("⊞LFT", "ADD_ORIGIN_NODE", {"node": "□0"})
    if decision:
        g.add_node("□D", note="决策")
    if outcome:
        g.add_node("□Q", note="结果")

    if origin_text and decision:
        g.add_edge(TopoEdge("□0", "□D", relation="causal", note="原点→决策"))
    if decision and outcome:
        g.add_edge(TopoEdge("□D", "□Q", relation="causal", note="决策→结果"))

    assumptions: List[str] = []
    for key in ("assumptions", "premises", "hypotheses", "core_assumptions"):
        val = ctx.get(key)
        if isinstance(val, list):
            assumptions = [str(a) for a in val if a]
            break
        if isinstance(val, str) and val.strip():
            assumptions = [val]
            break

    aid_of: Dict[str, str] = {}
    for i, a in enumerate(assumptions):
        aid = f"□A{i + 1}"
        aid_of[a] = aid
        g.add_node(aid, note=a[:60])
        if decision:
            g.add_edge(TopoEdge(aid, "□D", relation="requires",
                                falsifiable=True, note="输入假设边"))

    branches = ctx.get("branches") or ctx.get("branch_responses") or ctx.get("failure_paths")
    if isinstance(branches, list):
        for j, b in enumerate(branches):
            if not isinstance(b, dict):
                continue
            target = b.get("assumption", b.get("premise", b.get("target", "")))
            delta_d = b.get("delta_d", b.get("deltaD", b.get("response", "")))
            did = f"□ΔD{j + 1}"
            g.add_node(did, note=str(delta_d)[:60])
            src = aid_of.get(str(target), f"□A{j + 1}")
            g.add_edge(TopoEdge(src, did, relation="causal",
                                delta_d=str(delta_d) if delta_d else None,
                                note="分支响应边"))

    deps = ctx.get("dependencies") or ctx.get("dependency_graph") or ctx.get("deps")
    if isinstance(deps, dict):
        for a, targets in deps.items():
            if not isinstance(targets, list):
                continue
            for t in targets:
                g.add_edge(TopoEdge(f"□{t}", f"□{a}", relation="requires",
                                    note="依赖边"))

    g.trace("⊞LFT", "BUILD_G0", {
        "nodes": len(g.nodes), "edges": len(g.edges),
        "origin": bool(origin_text), "decision": bool(decision), "outcome": bool(outcome),
    })
    return g

# ============================================================================
# 分区②·补 决策上下文提取器（十算子共用单一实现） / Decision-Context Extractors
# ============================================================================
#
# 为什么必须是模块级单份，而不是每个算子自带一个 staticmethod：
#
#   历史上这里有 5 份 _extract_assumptions、3 份 _extract_branches、2 份
#   _extract_text，全是逐份拷贝。它们已经漂移，而且漂移会改变结论：
#     · 同一份 {"assumptions": [""]}，IAP 认 1 条前提，其余算子认 0 条；
#     · 同一份 {"assumptions": "A1"}，有一份根本不处理字符串形式；
#     · 有一份的键集少了 core_assumptions；
#     · 有一份把 delta_d 当成分支别名——而 delta_d 在本系统里是因果边的
#       失效变更描述，与「前提失败后的应对路径」不是一回事。
#
#   这些数都会进 extract_risk_set 的风险集与收敛分类，于是「同输入 + 同 nonce
#   → 同链根」在这条路径上并不成立。**副本不是安全的默认态，唯一的实现才是。**
#
# 口径（刻意取最严的一版，因为「缺就是缺」优先于「凑得出来」）：
#   · 空白字符串 → 视为未声明。空串不是前提，也不是待审计文本。
#   · 列表内的空元素 → 剔除。声明 3 条里有 1 条是空的，就是 2 条，不是 3 条。
#   · 形状不符（既非 str，也非「全为 dict 的 list」）→ 返回空，不做转换猜测。
#     把 dict 强转成 str 得到的 "Assumption(id='A1', ...)" 不是前提，是垃圾。

_CTX_TEXT_KEYS = (
    'text', 'narrative', 'output', 'content',
    'decision_text', 'llm_output', 'decision',
)
_CTX_ASSUMPTION_KEYS = (
    'assumptions', 'premises', 'hypotheses', 'core_assumptions',
)
# 刻意不含 'delta_d'：理由见上。
_CTX_BRANCH_KEYS = ('branches', 'branch_responses', 'failure_paths')


def _ctx_text(ctx: Any) -> str:
    """从 decision_context 提取待审计文本；取不到就是空串。"""
    if isinstance(ctx, str):
        return ctx if ctx.strip() else ''
    if not isinstance(ctx, dict):
        return ''
    for key in _CTX_TEXT_KEYS:
        val = ctx.get(key)
        if isinstance(val, str) and val.strip():
            return val
    return ''


def _ctx_assumptions(ctx: Any) -> List[str]:
    """提取显式声明的前提列表。空串不是前提。"""
    if not isinstance(ctx, dict):
        return []
    for key in _CTX_ASSUMPTION_KEYS:
        val = ctx.get(key)
        if isinstance(val, list):
            return [str(a) for a in val if a]
        if isinstance(val, str) and val.strip():
            return [val]
    return []


def _ctx_branches(ctx: Any) -> List[Dict[str, Any]]:
    """提取分支响应 [{'assumption': ..., 'delta_d': ...}]。

    某一键形状不符时**继续试下一键**，而不是就地返回空：前者是「没找到」，
    后者是「找到了但是坏的」，两者的补救动作不一样。
    """
    if not isinstance(ctx, dict):
        return []
    for key in _CTX_BRANCH_KEYS:
        val = ctx.get(key)
        if isinstance(val, list) and all(isinstance(v, dict) for v in val):
            return val
    return []


# 分区③ 算子 ⊙GA — 第一原点锚定 / Genesis Anchor
# ============================================================================
# GA — ⊙ 第一原点锚定 / Genesis Anchor Plugin
# ==========================================
#
# 锚定整条因果链的起点与终点：原点事件、目标稳态、能量资源约束。
#
# 为什么需要它
# ------------
# 规范第六条元因果基底给了两条根本设定：溯源缺口是原初宇宙的起点、
# 万事万物的能量本根；因果承接是能量动态守恒，每个果即刻成为下一个因。
# 落到可审计的层面就是三件事：
#
#     原点事件     链不能凭空开始。没有起点，后面所有节点都失去序的依据。
#     目标稳态 S*  螺旋重构必须有收敛方向；没有终点，「迭代」退化为「转圈」。
#     能量/资源约束 无限因果思维的前提是拓扑无边界，但**能量守恒有硬顶**。
#                  资源不设上限的推演不是无限，是失控。
#
# 判定（全部为结构判断，不做估算）
# --------------------------------
#     ORIGIN_VACUUM       原点真空                      → BLOCKED    （致命）
#     GOAL_UNANCHORED     目标未锚定                    → HIGH_RISK  （信号）
#     RESOURCE_DEFICIT    资源缺口为负（能量守恒被违反）  → HIGH_RISK  （信号）
#     UNSPECIFIED_RESOURCE 资源块缺必需字段              → WARNING
#     其余                                              → PASS
#
# 「原点真空」是致命项，理由与 CCS 的信息黑洞一致：链的起点缺失时，
# 后续任何「看起来收敛了」的信号都不可信——风险集清零可能只是因为
# 没有原点可对齐。故本算子取 T1_STRUCTURAL，允许阻断。
#
# 资源缺口只做减法
# ----------------
#     gap = 可用 / 预算 − 已承诺
# 只做减法，不预测消耗、不推断剩余里程。无法做减法（字段缺位）时
# 报 UNSPECIFIED_RESOURCE，而不是猜一个数。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class OriginAnchorPlugin:
    """⊙ 算子：第一原点锚定。"""

    PLUGIN_NAME = "GA"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Genesis Anchor — 锚定原点事件/目标稳态/能量资源约束"

    ORIGIN_KEYS = ("origin", "origin_event", "第一原点", "□0")
    GOAL_KEYS = ("goal", "target_state", "objective", "S*", "稳态")
    RESOURCE_KEYS = ("resources", "resource", "energy", "能量", "约束")

    # 单个资源块内，代表「可用额度」与「已承诺额度」的字段名
    CAPACITY_FIELDS = ("budget", "available", "cap", "total", "额度", "预算", "上限")
    COMMITTED_FIELDS = ("committed", "used", "consumed", "spent", "已承诺", "已耗", "已用")

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        origin = self._pick(ctx, self.ORIGIN_KEYS)
        goal = self._pick(ctx, self.GOAL_KEYS)
        resources = self._extract_resources(ctx)

        ledger = self._build_ledger(resources)
        gaps = [r for r in ledger if r["gap"] is not None and r["gap"] < 0]
        unspecified = [r for r in ledger if r["gap"] is None]

        origin_hash = self._fingerprint(origin, goal)
        warnings: List[str] = []
        reasons: List[str] = []

        # 判定优先级链：真空 > 目标 > 资源缺口 > 资源未声明 > 通过
        if not origin:
            status = "BLOCKED"
            reason = "ORIGIN_VACUUM"
            reasons.append("原点事件缺失 — 链无起点，后续节点的序无法成立")
        elif not goal:
            status = "HIGH_RISK"
            reason = "GOAL_UNANCHORED"
            reasons.append("目标稳态未锚定 — 无收敛方向，螺旋迭代退化为转圈")
        elif gaps:
            status = "HIGH_RISK"
            reason = "RESOURCE_DEFICIT"
            reasons.append("资源缺口为负 — 能量守恒被违反：" + "; ".join(
                f"{g['name']} gap={g['gap']}" for g in gaps
            ))
        elif unspecified:
            status = "WARNING"
            reason = "UNSPECIFIED_RESOURCE"
            reasons.append("资源块缺少可用/已承诺字段 — 无法做减法，拒绝估算：" + ", ".join(
                u["name"] for u in unspecified
            ))
        else:
            status = "PASS"
            reason = "ANCHORED"
            reasons.append(
                "原点、目标、资源三项锚定完成"
                + ("（未声明资源约束）" if not ledger else "")
            )

        if not ledger:
            warnings.append("未声明任何能量/资源约束 — 拓扑可扩展，但推演失去预算硬顶")
        for lost in self._pick_unknown(ctx):
            warnings.append(f"未知的资源字段 '{lost}'，已忽略（不猜测其含义）")

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "reasons": reasons,
            "warnings": warnings,
            "origin": origin or None,
            "goal": goal or None,
            "origin_hash": origin_hash,
            "resource_ledger": ledger,
            "resource_gap_total": sum(g["gap"] for g in gaps) if gaps else 0.0,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _pick(ctx: Dict[str, Any], keys) -> str:
        for k in keys:
            v = ctx.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
            if isinstance(v, dict):
                for sub in ("text", "name", "id", "value"):
                    if isinstance(v.get(sub), str) and v[sub].strip():
                        return v[sub].strip()
        return ""

    def _extract_resources(self, ctx: Dict[str, Any]) -> Dict[str, Any]:
        for k in self.RESOURCE_KEYS:
            v = ctx.get(k)
            if isinstance(v, dict) and v:
                return v
        return {}

    @staticmethod
    def _pick_unknown(ctx: Dict[str, Any]) -> List[str]:
        """已知之外的资源字段一律不猜测其含义。"""
        known = set()
        for keys in (OriginAnchorPlugin.ORIGIN_KEYS, OriginAnchorPlugin.GOAL_KEYS,
                     OriginAnchorPlugin.RESOURCE_KEYS):
            known.update(keys)
        return sorted(k for k in ctx if str(k).endswith(("_energy", "_budget")) and k not in known)

    def _build_ledger(self, resources: Dict[str, Any]) -> List[Dict[str, Any]]:
        ledger: List[Dict[str, Any]] = []
        for name in sorted(resources):
            block = resources[name]
            if isinstance(block, (int, float)):
                # 只给一个裸数字：它是什么？可用额度还是已耗？无从判定 → 不做减法。
                ledger.append({
                    "name": str(name), "capacity": float(block), "committed": None,
                    "gap": None, "note": "裸数值，无法区分容量与已耗，拒绝估算",
                })
                continue
            if not isinstance(block, dict):
                ledger.append({
                    "name": str(name), "capacity": None, "committed": None,
                    "gap": None, "note": f"不支持的资源块类型 {type(block).__name__}",
                })
                continue
            cap = self._first_number(block, self.CAPACITY_FIELDS)
            com = self._first_number(block, self.COMMITTED_FIELDS)
            gap = (cap - com) if (cap is not None and com is not None) else None
            ledger.append({
                "name": str(name), "capacity": cap, "committed": com, "gap": gap,
                "note": "" if gap is not None else "缺少可用/已承诺字段",
            })
        return ledger

    @staticmethod
    def _first_number(block: Dict[str, Any], fields) -> Optional[float]:
        for f in fields:
            v = block.get(f)
            if isinstance(v, bool):
                continue
            if isinstance(v, (int, float)):
                return float(v)
        return None

    @staticmethod
    def _fingerprint(origin: str, goal: str) -> str:
        """原点指纹：螺旋层用它检测「原点漂移」。

        只由 origin + goal 的规范化文本推导，与资源、与时间均无关——
        漂移检测要问的是「还在追同一个目标吗」，不是「跑了多久」。
        """
        blob = json.dumps({"origin": origin, "goal": goal},
                          sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()[:16]

# ============================================================================
# 分区③ 算子 ⊗NS — 去语义化 / Narrative Strip
# ============================================================================
# NS — Narrative Strip Plugin
# ============================
#
# 剥离叙事包装，提取逻辑骨架。
#
# 将输入文本中的修辞、情感、道德判断、立场粉饰分离，
# 只保留可形式化验证的逻辑核心 (logical core)。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

# ── 修辞/情感/道德标记词库（可随年度标准更新） ──

RHETORICAL_MARKERS: List[str] = [
    # 情感强化
    "毫无疑问", "显而易见", "众所周知", "不言而喻", "毋庸置疑",
    "令人震惊", "令人担忧", "令人振奋", "令人失望", "令人兴奋",
    "遗憾的是", "幸运的是", "不幸的是", "可悲的是", "可怕的是",
    "当然", "显然", "确实", "当然啦", "毕竟",
    "amazing", "incredible", "obviously", "clearly", "undoubtedly",
    "unfortunately", "fortunately", "tragically", "sadly",
    "shockingly", "surprisingly", "inevitably", "certainly",
    # 道德/立场粉饰
    "必须承认", "应该看到", "值得注意", "需要强调",
    "不可否认", "不容忽视", "不可忽视", "不容置疑",
    "it is important to note", "it should be noted",
    "it is worth noting", "needless to say", "it goes without saying",
    # 模糊量化
    "大量", "许多", "相当多", "不少", "大部分", "绝大多数",
    "可能", "也许", "大概", "或许", "似乎", "看起来",
    "many", "several", "a lot of", "numerous", "considerable",
    "perhaps", "possibly", "likely", "arguably", "presumably",
    # 权威暗示
    "专家认为", "研究表明", "数据显示", "据报道",
    "experts say", "studies show", "research indicates", "reports suggest",
]

# 模糊量化的正则模式
VAGUE_QUANTIFIER_PATTERNS = [
    r"\b[一二两三四五六七八九十百千万亿]+\s*[百分比成]",
    r"\b\d+\s*[%％]\s*(?:左右|大概|大约|差不多|近|差不多)?",
    r"\b(?:超过|接近|将近|大约|大概|差不多)\s*\d+",
    r"\b(?:成百上千|数以万计|数以千计|数以百计|成千上万)\b",
]


class NarrativeStripPlugin:
    """NS 算子：叙事剥离。"""

    PLUGIN_NAME = "NS"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Narrative Strip — 剥离修辞/情感/道德粉饰，提取逻辑骨架"

    def __init__(self):
        self.name = self.PLUGIN_NAME
        # 预编译正则：标记词匹配
        self._marker_patterns = [
            re.compile(re.escape(m), re.IGNORECASE) for m in RHETORICAL_MARKERS
        ]
        self._vague_patterns = [re.compile(p, re.IGNORECASE) for p in VAGUE_QUANTIFIER_PATTERNS]

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        text = self._extract_text(decision_context)
        if not text:
            return self._empty_result()

        segments = self._strip_narrative(text)
        logical_core = self._extract_logical_core(text, segments)
        violations = self._detect_violations(text, segments)

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "narrative_stripped": len(violations) == 0,
            "narrative_segments": segments,
            "logical_core": logical_core,
            "violations": violations,
            "violation_count": len(violations),
            "pass": len(violations) == 0,
        }

    # ── internals ──

    @staticmethod
    def _extract_text(ctx: Dict[str, Any]) -> str:
        return _ctx_text(ctx)

    def _strip_narrative(self, text: str) -> List[Dict[str, Any]]:
        """识别并标记所有叙事片段。"""
        segments: List[Dict[str, Any]] = []

        # 标记词
        for pat in self._marker_patterns:
            for match in pat.finditer(text):
                segments.append({
                    "type": "rhetorical_marker",
                    "marker": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })

        # 模糊量化
        for pat in self._vague_patterns:
            for match in pat.finditer(text):
                segments.append({
                    "type": "vague_quantifier",
                    "marker": match.group(),
                    "start": match.start(),
                    "end": match.end(),
                })

        # 去重（同一位置可能被多个模式命中）
        seen = set()
        unique: List[Dict[str, Any]] = []
        for seg in segments:
            key = (seg["start"], seg["end"])
            if key not in seen:
                seen.add(key)
                unique.append(seg)
        unique.sort(key=lambda s: s["start"])
        return unique

    @staticmethod
    def _extract_logical_core(text: str, segments: List[Dict[str, Any]]) -> str:
        """移除叙事片段后的逻辑骨架。"""
        if not segments:
            return text.strip()
        # 按位置倒序删除，避免偏移
        result = text
        for seg in sorted(segments, key=lambda s: s["start"], reverse=True):
            result = result[:seg["start"]] + result[seg["end"]:]
        # 清理多余空白
        result = re.sub(r"\s{2,}", " ", result).strip()
        return result

    @staticmethod
    def _detect_violations(text: str, segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成违规列表。"""
        violations: List[Dict[str, Any]] = []
        for seg in segments:
            violations.append({
                "rule_id": f"NS-{seg['type']}",
                "description": f"叙事标记 '{seg['marker']}' 检出，建议剥离",
                "severity": "WARN",
                "position": [seg["start"], seg["end"]],
            })
        return violations

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "plugin": "NS",
            "version": "1.0.0",
            "narrative_stripped": True,
            "narrative_segments": [],
            "logical_core": "",
            "violations": [],
            "violation_count": 0,
            "pass": True,
            "note": "No text found in decision_context to audit.",
        }

# ============================================================================
# 分区③ 算子 ⊕IAP — 约束挖掘 / Implicit Assumption
# ============================================================================
# IAP — Implicit Assumption Plugin
# ================================
#
# 透视内隐假设：检测未声明的预设前提。
#
# 当推演 P → Q 时，强制挖掘并显式标记所有未声明的预设。
# 检测模式：
#   - 自指假设 (P 引用自身作为前提)
#   - 权力绕过 (P 含特权暗示，绕过正常校验)
#   - 单边前提 (P 仅声明部分条件，遗漏关键前提)
#   - 循环论证 (P == Q 且非空)
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class ImplicitAssumptionPlugin:
    """IAP 算子：内隐假设透视。"""

    PLUGIN_NAME = "IAP"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Implicit Assumption Perspective — 透视未声明的预设前提"

    # ── 特征码（可随年度标准更新） ──

    # 自指假设特征码
    SELF_REFERENTIAL_PATTERNS = [
        r"\b本(?:机构|组织|公司|部门|人)\s*(?:认为|确信|保证|承诺)\b",
        r"\b(?:我们|我方)\s*(?:一直以来|始终|一贯)\b",
        r"\b(?:上述|前述)\s*(?:结论|判断|决定)\s*(?:即|就是|意味着)\b",
        r"\bthis\s+(?:organization|company|department)\s+(?:believes|confirms|guarantees)\b",
        r"\bwe\s+have\s+always\b",
        r"\bthe\s+above\s+(?:conclusion|judgment|decision)\s+(?:is|means)\b",
    ]

    # 权力绕过特征码
    PRIVILEGE_BYPASS_PATTERNS = [
        r"\b(?:无需|不必|不需要)\s*(?:审批|审核|批准|备案|许可)\b",
        r"\b(?:直接|自行)\s*(?:执行|实施|处理|决定)\b",
        r"\b(?:特批|特事特办|绿色通道)\b",
        r"\b(?:豁免|免除)\s*(?:审查|审核|检查)\b",
        r"\bno\s+(?:review|approval|permission)\s+required\b",
        r"\bbypass\s+(?:review|approval|oversight)\b",
        r"\bexempt\s+from\s+(?:review|audit|inspection)\b",
    ]

    # 模糊前提标志（可能是"单边前提"的信号）
    UNILATERAL_PATTERNS = [
        r"\b(?:假设|假定|前提)\s*[:：]?\s*(?:.{0,20})\s*(?:成立|为真|有效)\b",
        r"\b(?:在其他条件不变的情况下|其他条件相同)\b",
        r"\b(?:如果|若)\s+(?:.{0,30})\s*(?:则|那么|就)\b",
        r"\bassuming\s+(?:that\s+)?\b",
        r"\bceteris\s+paribus\b",
        r"\bif\s+.{1,40}\s+then\b",
    ]

    def __init__(self):
        self.name = self.PLUGIN_NAME
        self._self_ref = [re.compile(p, re.IGNORECASE) for p in self.SELF_REFERENTIAL_PATTERNS]
        self._priv_bypass = [re.compile(p, re.IGNORECASE) for p in self.PRIVILEGE_BYPASS_PATTERNS]
        self._unilateral = [re.compile(p, re.IGNORECASE) for p in self.UNILATERAL_PATTERNS]

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        text = self._extract_text(decision_context)
        assumptions = self._extract_assumptions(decision_context)

        if not text and not assumptions:
            return self._empty_result()

        flags: List[Dict[str, Any]] = []

        # Flag 0: 自指假设
        self_ref_hits = self._scan_patterns(text, self._self_ref, "self_referential")
        flags.extend(self_ref_hits)

        # Flag 1: 权力绕过
        priv_hits = self._scan_patterns(text, self._priv_bypass, "privilege_bypass")
        flags.extend(priv_hits)

        # Flag 2: 单边前提
        unilateral_hits = self._scan_patterns(text, self._unilateral, "unilateral_premise")
        flags.extend(unilateral_hits)

        # Flag 3: 循环论证 (P == Q)
        circular = self._detect_circular(decision_context)
        if circular:
            flags.append(circular)

        # Flag 4: 缺失前提检测
        missing = self._detect_missing_assumptions(decision_context, text)
        flags.extend(missing)

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "implicit_assumptions_found": len(flags) > 0,
            "flags": flags,
            "flag_count": len(flags),
            "pass": len(flags) == 0,
        }

    # ── internals ──

    @staticmethod
    def _extract_text(ctx: Dict[str, Any]) -> str:
        return _ctx_text(ctx)

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        return _ctx_assumptions(ctx)

    @staticmethod
    def _scan_patterns(text: str, patterns: List[re.Pattern], flag_type: str) -> List[Dict[str, Any]]:
        hits: List[Dict[str, Any]] = []
        if not text:
            return hits
        for pat in patterns:
            for m in pat.finditer(text):
                hits.append({
                    "flag_type": flag_type,
                    "flag_id": f"IAP-{flag_type}",
                    "match": m.group(),
                    "position": [m.start(), m.end()],
                    "severity": "WARN" if flag_type != "privilege_bypass" else "HALT",
                    "description": f"内隐假设: {flag_type} — '{m.group()}'",
                })
        return hits

    @staticmethod
    def _detect_circular(ctx: Dict[str, Any]) -> Dict[str, Any] | None:
        """检测循环论证: P == Q 且非空。"""
        if not isinstance(ctx, dict):
            return None
        p = str(ctx.get("decision", ctx.get("p", "")))
        q = str(ctx.get("outcome", ctx.get("q", ctx.get("result", ""))))
        if p and q and p.strip() == q.strip():
            return {
                "flag_type": "circular_justification",
                "flag_id": "IAP-circular",
                "match": f"P == Q: '{p[:60]}'",
                "severity": "HALT",
                "description": "循环论证: 决策(P)与结果(Q)相同且非空",
            }
        return None

    @staticmethod
    def _detect_missing_assumptions(ctx: Dict[str, Any], text: str) -> List[Dict[str, Any]]:
        """检测决策是否缺少显式前提声明。"""
        violations: List[Dict[str, Any]] = []
        if not isinstance(ctx, dict):
            return violations

        decision = ctx.get("decision", "")
        assumptions = ctx.get("assumptions", ctx.get("premises", []))

        has_decision = isinstance(decision, str) and decision.strip()
        has_assumptions = isinstance(assumptions, list) and len(assumptions) > 0

        if has_decision and not has_assumptions:
            violations.append({
                "flag_type": "missing_assumptions",
                "flag_id": "IAP-missing",
                "match": "decision present, assumptions absent",
                "severity": "WARN",
                "description": "决策已声明但未列出任何前提假设 — 单边前提风险",
            })

        return violations

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "plugin": "IAP",
            "version": "1.0.0",
            "implicit_assumptions_found": False,
            "flags": [],
            "flag_count": 0,
            "pass": True,
            "note": "No text or assumptions found to audit.",
        }

# ============================================================================
# 分区③ 算子 ⊿LCH — 薄弱点加固 / Fragility Localization
# ============================================================================
# LCH — Fragility Localization Plugin
# ============================
#
# 脆弱性定位：定位逻辑链中最脆弱的隐性变量 A。
# 计算当 非A（变量缺失或失效）发生时，整体决策的崩塌概率 Delta D。
#
# 命名对照
# --------
# 代码标识是 LCH / FragilityLatchPlugin（脆弱性*闩锁*，见 README-zh.md 表格），
# 本算子的中文职责名是「脆弱性*对冲*」，引擎侧函数名是 _assess_vulnerability。
# 三者指同一个算子，检索时三种拼写都试。
#
# 输入契约（decision_context 中本算子读取的键，全部可选）
# ------------------------------------------------
#   assumptions   list[str]   别名 premises / hypotheses / core_assumptions
#                              待审计的前提 A1..An；也接受单个字符串
#   dependencies  dict        别名 dependency_graph / deps
#                              {"A1": ["A2","A3"]} 表示 A1 依赖 A2、A3
#   branches      list[dict]  别名 branch_responses / failure_paths / delta_d
#                              [{"assumption": "A1", "delta_d": "回滚上一版本"}]
#                              语义是「若 A1 失效，则执行 ΔD」
#
# 全部缺失时不报错、不猜测，直接返回 _empty_result()。
#
# Delta D 计算式
# --------------
#   Delta D = 0.30                 基础值：一个尚无任何信息的前提
#           + 0.30   若无分支响应   ¬A 成立时没有回退路径
#           - 0.10   若有分支响应   回退路径的存在本身就是减损
#           + 0.15 × N              N = 被它支撑的前提个数；它失效则下游同时失效
#           + 0.10 × M              M = 模糊限定词个数（可能/大概/应该/通常…）
#           + 0.25   若不可证伪     总是/永远/必然 一类表述，失效时无预警手段
#   最后 clamp 到 [0, 1]
#
# 阈值 0.7 的来历
# ----------------
# 最常见的失效组合「无分支响应 + 不可证伪」= 0.30+0.30+0.25 = 0.85 > 0.7，
# 判不通过（pass=False）。若已有分支响应，则为 0.30-0.10+0.25 = 0.45 < 0.7。
# 也就是说这条线实质上在区分一件事：**为这个前提有没有准备回退路径**。
#
# 这些权重是确定性常数，不是概率估计，也没有经过统计拟合。
# 改动权重会直接改变判定结果，属设计变更而非参数调优。
#
# 输出：
#   - 脆弱变量列表（按 Delta D 降序）
#   - 每个变量的依赖链路径
#   - 崩塌场景描述
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class FragilityLatchPlugin:
    """LCH 算子：脆弱性定位。"""

    PLUGIN_NAME = "LCH"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Fragility Localization — 定位最脆弱变量，计算崩塌概率 Delta D"

    def __init__(self):
        self.name = self.PLUGIN_NAME

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        assumptions = self._extract_assumptions(decision_context)
        dependencies = self._extract_dependencies(decision_context)
        branches = self._extract_branches(decision_context)

        if not assumptions:
            return self._empty_result()

        # 为每个前提计算脆弱性
        fragility_report: List[Dict[str, Any]] = []
        for i, assumption in enumerate(assumptions):
            frag = self._assess_fragility(
                assumption=assumption,
                index=i,
                assumptions=assumptions,
                dependencies=dependencies,
                branches=branches,
            )
            fragility_report.append(frag)

        # 按 Delta D 降序
        fragility_report.sort(key=lambda x: x["delta_d"], reverse=True)

        # 最脆弱变量
        weakest = fragility_report[0] if fragility_report else None
        system_delta_d = max((f["delta_d"] for f in fragility_report), default=0.0)

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "assumptions_audited": len(assumptions),
            "fragility_report": fragility_report,
            "weakest_variable": weakest,
            "system_delta_d": round(system_delta_d, 4),
            "has_branch_coverage": self._check_branch_coverage(assumptions, branches),
            "pass": system_delta_d < 0.7 and self._check_branch_coverage(assumptions, branches),
        }

    # ── internals ──

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        return _ctx_assumptions(ctx)

    @staticmethod
    def _extract_dependencies(ctx: Dict[str, Any]) -> Dict[str, List[str]]:
        """提取依赖关系图。格式: {"A": ["B", "C"]} 表示 A 依赖 B 和 C。"""
        if isinstance(ctx, dict):
            for key in ("dependencies", "dependency_graph", "deps"):
                val = ctx.get(key)
                if isinstance(val, dict):
                    return {str(k): [str(v) for v in vs] for k, vs in val.items()}
        return {}

    @staticmethod
    def _extract_branches(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        return _ctx_branches(ctx)

    @staticmethod
    def _assess_fragility(
        assumption: str,
        index: int,
        assumptions: List[str],
        dependencies: Dict[str, List[str]],
        branches: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """评估单个前提的脆弱性。"""
        # 因素 0：基础值。假定这条前提本身成立，但尚不知道它是否有回退路径，
        # 也不做任何有利假设，因此给一个中等偏上的起点。
        delta_d = 0.3  # 基础值

        # 因素 1：分支响应（ΔD）是否存在。
        # 这是权重最大的一项（±0.3），因为「假设失效时有没有退路」
        # 直接决定崩塌是系统性的还是可收敛的。
        # 匹配同时接受两种写法：写全称文本，或写编号 A1/A2/…
        has_branch = any(
            b.get("assumption", b.get("premise", "")) == assumption
            or b.get("assumption", b.get("premise", "")) == f"A{index+1}"
            for b in branches
        )
        if not has_branch:
            delta_d += 0.3
        else:
            delta_d -= 0.1

        # 因素 2：依赖图的入度。它被多少条前提支撑？
        # 入度越高越是关键节点——它一失效，下游成片失效。
        # 0.15/个 的设定使「被 3 条依赖」时该项累计 +0.45，
        # 足以单独把一个本来合格的前提推过 0.7 阈值。
        dependents = [
            a for a, deps in dependencies.items()
            if assumption in deps or f"A{index+1}" in deps
        ]
        if dependents:
            delta_d += 0.15 * len(dependents)

        # 因素 3：模糊限定词。中英各 8 个，可叠加计数。
        # 「需求大概稳定」比「需求稳定」多 0.1——
        # 限定词越多，前提越难被证伪，也就越难及时发现它已失效。
        vague_markers = ["可能", "大概", "也许", "或许", "通常", "一般", "应该",
                         "maybe", "probably", "usually", "generally", "should"]
        lower_assumption = assumption.lower() if isinstance(assumption, str) else ""
        vague_count = sum(1 for m in vague_markers if m in lower_assumption)
        delta_d += 0.1 * vague_count

        # 因素 4：不可证伪表述。这是与前几项性质不同的一类风险——
        # 前几项是「失效了会怎样」，这一项是「失效了你也不会知道」。
        # 没有检测手段的假设，即使后果不严重，也应按高脆弱处理。
        if not FragilityLatchPlugin._is_falsifiable(assumption):
            delta_d += 0.25

        # 各项叠加可能越界，统一夹到 [0, 1]：
        # Delta D 是概率量，超出该区间的值没有意义，也会破坏下游比较。
        delta_d = max(0.0, min(1.0, delta_d))

        return {
            "assumption": assumption,
            "index": index,
            "delta_d": round(delta_d, 4),
            "has_branch_response": has_branch,
            "dependents": dependents,
            "is_falsifiable": FragilityLatchPlugin._is_falsifiable(assumption),
            "vague_markers_found": vague_count,
            "failure_scenario": f"若 非A{index+1} 成立（'{assumption[:40]}' 失效），"
                                f"决策崩塌概率 Delta D = {delta_d:.2f}",
        }

    @staticmethod
    def _is_falsifiable(assumption: str) -> bool:
        """检查前提是否可证伪。"""
        if not isinstance(assumption, str) or not assumption.strip():
            return False
        # 不可证伪的标志
        non_falsifiable = ["总是", "永远", "从不", "必然", "绝对",
                            "always", "never", "inevitably", "absolutely"]
        lower = assumption.lower()
        return not any(m in lower for m in non_falsifiable)

    @staticmethod
    def _check_branch_coverage(assumptions: List[str], branches: List[Dict[str, Any]]) -> bool:
        """检查是否所有前提都有对应的分支响应。"""
        if not assumptions:
            return True
        branch_targets = set()
        for b in branches:
            for key in ("assumption", "premise", "target"):
                val = b.get(key)
                if val:
                    branch_targets.add(str(val))
        covered = sum(1 for i, a in enumerate(assumptions)
                      if a in branch_targets or f"A{i+1}" in branch_targets)
        return covered == len(assumptions)

    @staticmethod
    def _empty_result() -> Dict[str, Any]:
        return {
            "plugin": "LCH",
            "version": "1.0.0",
            "assumptions_audited": 0,
            "fragility_report": [],
            "weakest_variable": None,
            "system_delta_d": 0.0,
            "has_branch_coverage": True,
            "pass": True,
            "note": "No assumptions found to assess fragility.",
        }

# ============================================================================
# 分区③ 算子 ⊞LFT — 无标签拓扑图 / Label-Free Topology
# ============================================================================
# LFT — ⊞ 无标签拓扑图 / Label-Free Topology Plugin
# ============================================================
#
# 把决策上下文投影成无语义拓扑图 G，并跑完三类编译期并行校验。
#
# 「无标签」的含义
# ----------------
# 不是「没有规则」，而是「不携带语义标签」。上游语言（.spd）带着 Decision /
# Assumption / Branch 这些语义标签进来；本算子把它们全部拆成 □ 与 →，
# 让结构先于命名成立。规范原话：
#
#     关系优先于实体。删除所有连接关系后实体自动消失。
#
# 因此本算子产出的图里不存在「这是决策节点」这种断言，只有
# 「□D 是 □0 的下游、□A1 的上游」。语义标签只在最后一步由
# relative_label() 做外部映射，不参与任何判定。
#
# 输出担保
# --------
#     G0          未校验的纯拓扑
#     validation  三类并行校验结果（一致性/约束满足/拓扑闭合）
#     graph_hash  纯结构指纹——不含标签、不含 provenance，
#                 因此「同一结构不同命名」得到同一指纹，
#                 「同一命名不同结构」得到不同指纹。
#
# 状态映射
# --------
#     存在致命错误（一致性/约束满足）  → BLOCKED     推演终止
#     存在闭合警告（悬空/悖论）        → WARNING     可强制继续，但结果无效
#     三类全过                        → PASS
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class TopologyGraphPlugin:
    """⊞ 算子：无标签拓扑图。"""

    PLUGIN_NAME = "LFT"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Label-Free Topology — 无语义拓扑构建 + 三类并行校验"

    TOPOLOGY_KEYS = ("topology", "topo", "graph", "拓扑")

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        explicit = self._extract_explicit_topology(ctx)

        if explicit is not None:
            graph = self._parse_topology(explicit)
            source = "EXPLICIT"
        else:
            origin = ctx.get("origin") or ctx.get("origin_event")
            origin_text = origin if isinstance(origin, str) else ""
            graph = build_from_decision_context(ctx, origin=origin_text)
            source = "PROJECTED"

        validation = TopologyValidator.run_all(graph)
        labels = graph.labels()

        if validation["fatal"]:
            status, reason = "BLOCKED", "TOPOLOGY_ILLEGAL"
        elif not validation["result_valid"]:
            status, reason = "WARNING", "TOPOLOGY_OPEN"
        elif source == "PROJECTED" and not graph.edges:
            # 空图不算「通过」：没有边就没有结构，任何结论都不成立。
            status, reason = "WARNING", "EMPTY_TOPOLOGY"
        else:
            status, reason = "PASS", "TOPOLOGY_CLOSED"

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "source": source,
            "node_count": len(graph.nodes),
            "edge_count": len(graph.edges),
            "graph_hash": graph.graph_hash(),
            "topology": graph.to_dict(),
            # 公理 5：链内时序与观测位置。二者都不参与 pass/fail 判定
            # （判定在 validation.time_order 里），这里单独暴露一份，
            # 便于上层直接消费「这条链怎么排序、我站在哪条链上」。
            "time_order": graph.assign_time_order(),
            "validation": validation,
            "relative_labels": labels,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _extract_explicit_topology(ctx: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for key in TopologyGraphPlugin.TOPOLOGY_KEYS:
            val = ctx.get(key)
            if isinstance(val, dict) and val:
                return val
        return None

    @staticmethod
    def _parse_topology(spec: Dict[str, Any]) -> TopologyGraph:
        """解析显式拓扑声明。字段缺位不补默认值——缺就是缺。"""
        graph = TopologyGraph(layer=int(spec.get("layer", 0) or 0))

        raw_nodes = spec.get("nodes") or []
        for item in raw_nodes:
            if isinstance(item, str):
                graph.add_node(item)
            elif isinstance(item, dict) and item.get("id"):
                graph.add_node(str(item["id"]), note=str(item.get("note", "")))

        raw_edges = spec.get("edges") or []
        for item in raw_edges:
            if not isinstance(item, dict):
                continue
            src, dst = item.get("src"), item.get("dst")
            if not src or not dst:
                continue
            graph.add_edge(TopoEdge(
                src=str(src), dst=str(dst),
                relation=str(item.get("relation", "causal")),
                weight=item.get("weight"),
                validity=item.get("validity"),
                falsifiable=bool(item.get("falsifiable", True)),
                delta_d=item.get("delta_d"),
                note=str(item.get("note", "")),
                # 公理 5：允许显式声明链内时序；缺位即 None，由引擎按
                # 最长路径派生 —— 「缺就是缺」，不补默认值。
                t=item.get("t"),
            ))

        raw_constraints = spec.get("constraints")
        if isinstance(raw_constraints, list) and raw_constraints:
            graph.constraints = {}
            for c in raw_constraints:
                if isinstance(c, dict) and c.get("name"):
                    graph.constraints[str(c["name"])] = Constraint(
                        name=str(c["name"]),
                        kind=str(c.get("kind", "weight_range")),
                        params=dict(c.get("params", {})),
                        note=str(c.get("note", "")),
                    )
        elif not graph.constraints:
            graph.constraints = default_constraints()

        graph.trace("⊞LFT", "PARSE_EXPLICIT", {
            "nodes": len(graph.nodes), "edges": len(graph.edges),
        })
        return graph

# ============================================================================
# 分区③ 算子 BFC — 二元事实校验 / Binary Fact Check
# ============================================================================
# BFC — 二元事实校验 / Binary Fact Check
# =====================================
#
# 把一条断言归约为**真 / 假**两个值之一。没有第三个值。
#
# 为什么是二元的
# --------------
# 规范公理 3 原文：「无中间模糊状态：校验只有通过 / 不通过两种结果，
# 不存在"大概对""可能没问题"的灰色地带。」
#
# 所以本模块的语义边界只有两条：
#   1. 能归约  → 输出 True 或 False（真值只能由外部声明，模块永不推断）
#   2. 不能归约 → 输出一个 **status**（中断或信号），**绝不**伪造一个"未决"真值
#
# 这是本模块与其它算子最关键的区别：`binary=None` 只表示「未声明」，
# 它必然伴随 `VERDICT_UNDECLARED`，且被排除在所有统计与判定之外。
# 把 None 当成第三真值，就等于把「不知道」洗成了「一个答案」。
#
# 与 ⇄GRF 的分工
# --------------
#     ⇄ GRF  问：现实反馈回来了，**结构上有没有回退路径 ΔD**   —— 行为层
#     BFC    问：这条断言，**有没有证据、证据打不打架、核验结果是什么** —— 认知层
#
# 判定链（全部为结构判断，零 LLM、零概率词）
# ------------------------------------------
#     SKIPPED            未启用（未提供 facts / verify_facts）        不计入风险
#     NOTHING_TO_VERIFY  开闸了却一条校验对象都没有                   WARNING
#     EVIDENCE_VACUUM    某条断言证据为空                             BLOCKED（致命）
#     EVIDENCE_CONFLICT  同一断言的证据/观察互相否定                   BLOCKED（致命）
#     FALSIFIED_PREMISE  已核验为假，却仍留在 assumptions 里            BLOCKED（致命）
#     VERDICT_UNDECLARED 有证据但真值未声明                           HIGH_RISK（信号）
#     VERIFIED           全部为真                                     PASS
#
# 级别由严重度决定（HALT > HIGH_RISK > WARNING），不依赖规则书写顺序。
#
# 默认不启用
# ----------
# 不提供 `facts` 时本模块原样放行（status = SKIPPED），存量审计的判定与链根不变。
# 事实校验是**拿证据换来的**，不是默认塞给用户的。
#
# 输入契约
# --------
#     facts         list    [{"id": "F1", "claim": "需求稳定", "evidence": ["doc#123"]}]
#                           也接受 list[str]（只给断言文本，证据回落到 ctx['evidence']）
#     observations  dict    {"F1": True} 或 {"需求稳定": False}
#                           别名 verdicts / fact_verdicts；真值只能来自这里
#     verify_facts  bool    显式开闸（等价于提供了 facts）
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

SEVERITY_RANK = {"HALT": 0, "HIGH_RISK": 1, "WARNING": 2}


class BinaryFactCheckPlugin:
    """BFC 算子：二元事实校验。"""

    PLUGIN_NAME = "BFC"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Binary Fact Check — 断言归约为真/假；不能归约即中断，不给第三值"

    FACTS_KEYS = ("facts", "claims", "facts_to_check", "断言")
    OBSERVATION_KEYS = ("observations", "verdicts", "fact_verdicts", "真值")

    TRUE_TOKENS = {"true", "1", "yes", "confirmed", "confirm", "pass", "held",
                   "真", "成立", "已验证", "已证实", "属实"}
    FALSE_TOKENS = {"false", "0", "no", "falsified", "falsify", "fail", "failed",
                    "假", "不成立", "未成立", "已证伪", "属伪"}

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}

        raw_facts = self._extract_facts(ctx)
        active = bool(raw_facts) or bool(ctx.get("verify_facts"))

        if not active:
            # 未启用：原样放行。不产出 status，故对收敛判定与链根零影响。
            return {
                "plugin": self.PLUGIN_NAME,
                "version": self.PLUGIN_VERSION,
                "status": "SKIPPED",
                "mode": "SKIPPED",
                "reason": "NOT_ENABLED",
                "message": "未提供 facts / verify_facts —— 二元事实校验未启用，原样放行。",
                "facts_checked": 0,
                "true_count": 0,
                "false_count": 0,
                "undeclared_count": 0,
                "verdicts": [],
                "violations": [],
                "remediation": [],
                "pass": True,
            }

        facts = self._normalize_facts(raw_facts, ctx)
        observations = self._extract_observations(ctx)
        assumptions = self._extract_assumptions(ctx)

        violations: List[Dict[str, Any]] = []
        remediation: List[str] = []
        verdicts: List[Dict[str, Any]] = []

        if not facts:
            violations.append({
                "code": "NOTHING_TO_VERIFY",
                "severity": "WARNING",
                "message": "已开闸但未提供任何校验对象 —— 空集不是「真」，也不构成校验通过。",
            })
            remediation.append("在 facts 中至少给出一条 {claim, evidence}。")

        for fact in facts:
            fid, claim = fact["id"], fact["claim"]
            evidence = fact["evidence"]
            polarity = self._evidence_polarity(evidence)
            declared = observations.get(fid, observations.get(claim, None))

            if not evidence:
                violations.append({
                    "code": "EVIDENCE_VACUUM",
                    "severity": "HALT",
                    "message": f"[中断：由于关键变量 {fid} 的证据真空，归约无法成立] "
                               f"断言「{claim}」未附任何证据。",
                })
                remediation.append(f"{fid}「{claim}」：补证据来源清单（evidence）。")
            elif polarity == "conflict":
                violations.append({
                    "code": "EVIDENCE_CONFLICT",
                    "severity": "HALT",
                    "message": f"断言「{claim}」的证据互相否定（同时存在支持与反对极性）—— "
                               f"本模块不做取舍，交由证据源裁定。",
                })
                remediation.append(f"{fid}「{claim}」：消解互斥证据，或拆成两条独立断言。")

            if declared is None and evidence and polarity != "conflict":
                violations.append({
                    "code": "VERDICT_UNDECLARED",
                    "severity": "HIGH_RISK",
                    "message": f"断言「{claim}」有证据但真值未声明 —— "
                               f"「有证据」不等于「已核验」；不给第三值，只给此信号。",
                })
                remediation.append(
                    f"{fid}「{claim}」：在 observations 中声明 true 或 false。")

            if declared is False and self._in_assumptions(claim, fid, assumptions):
                violations.append({
                    "code": "FALSIFIED_PREMISE",
                    "severity": "HALT",
                    "message": f"断言「{claim}」已核验为假，却仍留在 assumptions 中 —— "
                               f"决策支柱已断，结构上必须移除或触发对应 ΔD。",
                })
                remediation.append(f"{fid}「{claim}」：从假设集中撤下，或补齐对应分支响应。")

            verdicts.append({
                "id": fid,
                "claim": claim,
                "binary": declared,                      # None = 未声明，不是第三真值
                "evidence": [self._evidence_label(e) for e in evidence],
                "evidence_polarity": polarity,
                "source": "declared" if declared is not None else "undeclared",
            })

        has_halt = any(v["severity"] == "HALT" for v in violations)
        top = sorted(violations, key=lambda v: (SEVERITY_RANK.get(v["severity"], 9), v["code"]))

        if has_halt:
            status, reason = "BLOCKED", top[0]["code"]
        elif any(v["severity"] == "HIGH_RISK" for v in violations):
            status = "HIGH_RISK"
            reason = next(v["code"] for v in top if v["severity"] == "HIGH_RISK")
        elif violations:
            status, reason = "WARNING", top[0]["code"]
        else:
            status, reason = "PASS", "VERIFIED"

        declared_values = [v["binary"] for v in verdicts if v["binary"] is not None]
        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "mode": "ACTIVE",
            "reason": reason,
            "facts_checked": len(facts),
            "true_count": sum(1 for v in declared_values if v is True),
            "false_count": sum(1 for v in declared_values if v is False),
            "undeclared_count": sum(1 for v in verdicts if v["binary"] is None),
            "verdicts": verdicts,
            "violations": violations,
            "remediation": remediation,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _extract_facts(ctx: Dict[str, Any]) -> List[Any]:
        for key in BinaryFactCheckPlugin.FACTS_KEYS:
            val = ctx.get(key)
            if isinstance(val, list) and val:
                return val
        return []

    @staticmethod
    def _extract_observations(ctx: Dict[str, Any]) -> Dict[str, Any]:
        for key in BinaryFactCheckPlugin.OBSERVATION_KEYS:
            val = ctx.get(key)
            if isinstance(val, dict):
                return val
        return {}

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        return _ctx_assumptions(ctx)

    def _normalize_facts(self, raw: List[Any], ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        """规范化断言列表。id 缺省时按 F1..Fn 编号；证据缺省时回落到 ctx['evidence']。"""
        fallback_evidence = ctx.get("evidence")
        if not isinstance(fallback_evidence, list):
            fallback_evidence = []

        out: List[Dict[str, Any]] = []
        for i, item in enumerate(raw):
            fid = f"F{i + 1}"
            if isinstance(item, str):
                claim = item.strip()
                evidence = list(fallback_evidence)
            elif isinstance(item, dict):
                claim = str(item.get("claim", item.get("text", item.get("statement", "")))).strip()
                fid = str(item.get("id", fid))
                ev = item.get("evidence", item.get("sources"))
                evidence = list(ev) if isinstance(ev, list) else []
            else:
                continue
            if not claim:
                continue
            out.append({"id": fid, "claim": claim, "evidence": evidence})
        return out

    def _normalize_bool(self, value: Any) -> Optional[bool]:
        """把外部声明的真值归一到 True / False；归不了就返回 None（不猜）。"""
        if isinstance(value, bool):
            return value
        if isinstance(value, dict):
            for key in ("binary", "value", "verdict", "true", "is_true"):
                if key in value:
                    return self._normalize_bool(value[key])
            return None
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            if value == 1:
                return True
            if value == 0:
                return False
            return None
        if isinstance(value, str):
            token = value.strip().lower()
            if token in self.TRUE_TOKENS:
                return True
            if token in self.FALSE_TOKENS:
                return False
        return None

    def _evidence_polarity(self, evidence: List[Any]) -> str:
        """证据极性：none / support / oppose / conflict。

        只认显式声明的极性（dict 里的 polarity / supports / verdict）。
        纯字符串证据视为**并行收敛性**的中性来源——不猜测它的倾向。
        """
        polarities = set()
        for item in evidence:
            if not isinstance(item, dict):
                continue
            raw = None
            for key in ("polarity", "supports", "verdict", "holds"):
                if key in item:
                    raw = item[key]
                    break
            norm = self._normalize_bool(raw)
            if norm is not None:
                polarities.add(norm)

        if not polarities:
            return "none"
        if polarities == {True}:
            return "support"
        if polarities == {False}:
            return "oppose"
        return "conflict"

    @staticmethod
    def _evidence_label(item: Any) -> str:
        if isinstance(item, str):
            return item
        if isinstance(item, dict):
            return str(item.get("source", item.get("id", item)))
        return str(item)

    @staticmethod
    def _in_assumptions(claim: str, fid: str, assumptions: List[str]) -> bool:
        """已证伪的断言是否仍挂在假设集上。编号与全称两种写法都认。"""
        if claim in assumptions:
            return True
        return any(a in (fid, f"A{fid[1:]}", f"□{fid}") for a in assumptions)

# ============================================================================
# 分区③ 算子 ⚙CCS — 链闭合扫描 / Chain Closure Scan
# ============================================================================
# CCS — Chain Closure Scan Plugin
# ==============================
#
# 反事实校验与逆反验证。
#
# 输入契约（decision_context 中本算子读取的键，全部可选）
# ------------------------------------------------
#   decision     str        别名 p / premise / action     —— 因果链的 P
#   assumptions  list[str]  别名 premises / hypotheses     —— 因果链的 A
#   outcome      str        别名 q / result / consequence —— 因果链的 Q
#   branches     list[dict] 别名 branch_responses / failure_paths
#                             [{"assumption": "A1", "delta_d": "回滚"}]
#
# P / A / Q 任一缺失都会被 _blackhole_check 判为 HALT（信息黑洞），
# 这是本算子的核心约束：**缺关键变量就中断，不做推测性补全**。
#
# 已知弱点（读结果前请先知道）
# ------------------------------
# _inverse_check 的覆盖率是 len(branches) / len(assumptions)，
# 它数的是「有几个分支」而不是「分支是否真的对得上前提」，
# 因此 N 条分支配 M≤N 条前提时必定判 PASS，哪怕分支与前提毫无对应关系。
# 严格按前提身份匹配的版本在 LCH._check_branch_coverage；
# 两处判定口径不一致，读 inverse 的 PASS 时请记得这一条。
#
# 当推演 P → Q 时，强制执行：
#   1. 逆反校验: 若 非P 成立，系统稳态是回退收敛还是系统性崩溃？
#   2. 反事实校验: 非P 场景下 Q 会怎样？
#   3. 因果链完整性: P → Q 之间是否有断点？
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class CausalChainSyncPlugin:
    """CCS 算子：因果同步与反事实校验。"""

    PLUGIN_NAME = "CCS"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Chain Closure Scan — 逆反校验 + 反事实校验 + 因果链完整性"

    def __init__(self):
        self.name = self.PLUGIN_NAME

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        decision = self._extract_decision(decision_context)
        assumptions = self._extract_assumptions(decision_context)
        branches = self._extract_branches(decision_context)
        outcome = self._extract_outcome(decision_context)

        checks: List[Dict[str, Any]] = []

        # 1. 逆反校验: 非P → 系统稳态？
        inverse_check = self._inverse_check(decision, assumptions, branches)
        checks.append(inverse_check)

        # 2. 反事实校验: 非P 下 Q 会怎样？
        counterfactual = self._counterfactual_check(decision, assumptions, outcome, branches)
        checks.append(counterfactual)

        # 3. 因果链完整性: P → Q 有断点？
        chain_integrity = self._chain_integrity_check(decision, assumptions, outcome, branches)
        checks.append(chain_integrity)

        # 4. 信息黑洞检测
        blackhole = self._blackhole_check(decision, assumptions, outcome)
        checks.append(blackhole)

        halt_count = sum(1 for c in checks if c.get("severity") == "HALT")
        warn_count = sum(1 for c in checks if c.get("severity") == "WARN")

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "checks": checks,
            "halt_count": halt_count,
            "warn_count": warn_count,
            "pass": halt_count == 0,
        }

    # ── internals ──

    @staticmethod
    def _extract_decision(ctx: Dict[str, Any]) -> str:
        if isinstance(ctx, str):
            return ctx
        for key in ("decision", "p", "premise", "action"):
            val = ctx.get(key)
            if isinstance(val, str) and val.strip():
                return val
        return ""

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        return _ctx_assumptions(ctx)

    @staticmethod
    def _extract_branches(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        return _ctx_branches(ctx)

    @staticmethod
    def _extract_outcome(ctx: Dict[str, Any]) -> str:
        if isinstance(ctx, dict):
            for key in ("outcome", "q", "result", "consequence"):
                val = ctx.get(key)
                if isinstance(val, str) and val.strip():
                    return val
        return ""

    @staticmethod
    def _inverse_check(decision: str, assumptions: List[str],
                       branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """逆反校验：若非P成立，系统是回退收敛还是系统性崩溃？"""
        if not decision:
            return {
                "check": "inverse",
                "severity": "WARN",
                "description": "未提供决策(P)，无法执行逆反校验",
                "result": "SKIP",
            }

        if not branches:
            return {
                "check": "inverse",
                "severity": "HALT",
                "description": f"决策 '{decision[:50]}' 无分支响应(ΔD) — 非P 场景下系统将无回退路径，系统性崩塌",
                "result": "SYSTEM_COLLAPSE",
            }

        # 注意这里是数分支条数，不是校验分支与前提的对应关系（见模块头说明）。
        covered = len(branches)
        total_assumptions = len(assumptions) if assumptions else 1
        coverage = covered / total_assumptions if total_assumptions > 0 else 0

        if coverage >= 1.0:
            return {
                "check": "inverse",
                "severity": "PASS",
                "description": f"非P 场景有 {covered}/{total_assumptions} 个分支响应 — 回退收敛",
                "result": "CONVERGE",
            }
        elif coverage >= 0.5:
            return {
                "check": "inverse",
                "severity": "WARN",
                "description": f"非P 场景仅 {covered}/{total_assumptions} 个分支响应 — 部分回退",
                "result": "PARTIAL_RECOVERY",
            }
        else:
            return {
                "check": "inverse",
                "severity": "HALT",
                "description": f"非P 场景仅 {covered}/{total_assumptions} 个分支响应 — 系统性崩塌风险",
                "result": "COLLAPSE_RISK",
            }

    @staticmethod
    def _counterfactual_check(decision: str, assumptions: List[str],
                              outcome: str, branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """反事实校验：非P 下 Q 会怎样？"""
        if not decision or not outcome:
            return {
                "check": "counterfactual",
                "severity": "WARN",
                "description": "缺少决策(P)或结果(Q)，无法执行反事实校验",
                "result": "SKIP",
            }

        # 判定方式：在分支描述里找「非 / 若 / not / if」这类反事实信号词。
        # 这是纯字面匹配，不理解语义——写了反事实句式但内容空泛也会算 PASS。
        has_counterfactual = any(
            "非" in str(b.get("assumption", b.get("premise", "")))
            or "not" in str(b.get("assumption", b.get("premise", ""))).lower()
            or "若" in str(b.get("assumption", b.get("premise", "")))
            or "if" in str(b.get("assumption", b.get("premise", ""))).lower()
            for b in branches
        )

        if has_counterfactual:
            return {
                "check": "counterfactual",
                "severity": "PASS",
                "description": "存在反事实场景描述 — 非P 下的 Q' 已被考虑",
                "result": "COVERED",
            }
        else:
            return {
                "check": "counterfactual",
                "severity": "WARN",
                "description": "无反事实场景 — 非P 下 Q 会怎样未被显式考虑",
                "result": "UNCOVERED",
            }

    @staticmethod
    def _chain_integrity_check(decision: str, assumptions: List[str],
                               outcome: str, branches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """因果链完整性：P → (A1...An) → Q 是否有断点？"""
        if not decision:
            return {
                "check": "chain_integrity",
                "severity": "WARN",
                "description": "缺少决策(P)，因果链起点缺失",
                "result": "BROKEN_AT_ROOT",
            }

        if not outcome and not assumptions:
            return {
                "check": "chain_integrity",
                "severity": "HALT",
                "description": "因果链断裂：有 P 但无前提(A)也无结果(Q)",
                "result": "BROKEN",
            }

        # 只检查 P/A/Q 三个节点的在位情况，不校验它们之间的语义连贯性。
        # 「有 P 有 A 有 Q」在此即视为链路完整。
        has_p = bool(decision)
        has_a = len(assumptions) > 0
        has_q = bool(outcome)

        chain = []
        if has_p: chain.append("P")
        if has_a: chain.append("A")
        if has_q: chain.append("Q")

        if has_p and has_a and has_q:
            return {
                "check": "chain_integrity",
                "severity": "PASS",
                "description": f"因果链完整: {' → '.join(chain)}",
                "result": "COMPLETE",
            }
        elif has_p and has_a and not has_q:
            return {
                "check": "chain_integrity",
                "severity": "WARN",
                "description": "因果链不完整: P → A → ? (Q 缺失)",
                "result": "MISSING_Q",
            }
        elif has_p and not has_a and has_q:
            return {
                "check": "chain_integrity",
                "severity": "WARN",
                "description": "因果链跳跃: P → Q (无显式前提 A)",
                "result": "MISSING_A",
            }
        else:
            return {
                "check": "chain_integrity",
                "severity": "HALT",
                "description": f"因果链严重不完整: {' → '.join(chain) if chain else '空链'}",
                "result": "BROKEN",
            }

    @staticmethod
    def _blackhole_check(decision: str, assumptions: List[str],
                         outcome: str) -> Dict[str, Any]:
        """信息黑洞检测：关键变量缺失导致因果链无法建立。"""
        missing: List[str] = []
        if not decision:
            missing.append("P (决策)")
        if not assumptions:
            missing.append("A (前提)")
        if not outcome:
            missing.append("Q (结果)")

        if missing:
            return {
                "check": "blackhole",
                "severity": "HALT",
                "description": f"[中断：由于关键变量 {' / '.join(missing)} 真空，因果链断裂]",
                "result": "BLACKHOLE",
                "missing_variables": missing,
            }
        return {
            "check": "blackhole",
            "severity": "PASS",
            "description": "无信息黑洞 — 所有关键变量(P/A/Q)均在位",
            "result": "CLEAR",
        }

# ============================================================================
# 分区③ 算子 ⇄GRF — 灰度执行与现实反馈 / Gray Feedback
# ============================================================================
# GRF — ⇄ 灰度执行与现实反馈 / Gray Feedback Plugin
# ================================================
#
# 把「预测的崩塌」与「现实返回的观测」对齐。这是整条流水线里唯一引入
# 现实输入的算子，对应规范里叙事遮蔽那一支——现实的反面，与现实一体两面。
#
# 三层判定
# --------
#   REALITY_CONTRADICTION  假设已被现实证伪，决策却未触发对应的 ΔD   → BLOCKED
#   NO_GRAY_LADDER         无灰度档位且一次性全量放行                  → HIGH_RISK
#   UNOBSERVED_ASSUMPTION  放量已越过档位，该假设仍未观测到            → WARNING
#   UNKNOWN_FEEDBACK_SUBJECT 反馈指向了未声明的假设                    → WARNING
#   其余                                                             → PASS
#
# 为什么 REALITY_CONTRADICTION 必须阻断
# -------------------------------------
# 这是本算子唯一不可让渡的判定：现实已经给出了否定证据，而结构上却没有任何
# 回退路径被触发。此时「审计通过」是纯粹的谎言——不是证据不足，是证据与结构
# 直接矛盾。故取 T1_STRUCTURAL 并允许阻断。
#
# 灰度档位的语义
# --------------
# gray_levels 是放量梯度（如 [0.01, 0.05, 0.25, 1.0]）。它的作用不是「建议分批」，
# 而是给「未观测」设一个可判定的期限：越过某档位后仍未观测到，就不再是「还没轮到」，
# 而是「没有观测手段」。因此缺档位 = 崩塌不可逆 = 结构性缺失。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

class GrayFeedbackPlugin:
    """⇄ 算子：灰度执行与现实反馈。"""

    PLUGIN_NAME = "GRF"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Gray Feedback — 灰度档位 + 现实反馈对齐 + 证伪冲突检测"

    FEEDBACK_KEYS = ("feedback", "reality", "observation", "observations", "现实反馈")
    LEVEL_KEYS = ("gray_levels", "gray_ladder", "rollout_levels", "灰度档位")
    RATIO_KEYS = ("commit_ratio", "rollout_ratio", "exposure", "放量比例")

    CONFIRMED = {"confirmed", "confirm", "true", "pass", "held", "证实", "成立", "已验证", "已证实"}
    FALSIFIED = {"falsified", "falsify", "false", "fail", "failed", "broken",
                 "证伪", "失效", "不成立", "未成立", "已证伪"}
    UNOBSERVED = {"unobserved", "unknown", "pending", "none", "n/a",
                  "未观测", "未观测到", "待观测", "未知", "暂无"}

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        assumptions = self._extract_assumptions(ctx)
        branches = self._extract_branches(ctx)
        feedback = self._extract_feedback(ctx)
        levels = self._extract_levels(ctx)
        ratio = self._extract_ratio(ctx)

        violations: List[Dict[str, Any]] = []
        warnings: List[str] = []

        # ── 规则一：现实证伪 vs 结构回退（唯一致命项）──
        contradictions: List[str] = []
        unobserved: List[str] = []
        unknown_subjects: List[str] = []
        alignment: List[Dict[str, Any]] = []

        for subject in sorted(feedback):
            verdict = feedback[subject]
            matched_assumption = self._match_assumption(subject, assumptions)
            branch = self._find_branch(matched_assumption, branches) if matched_assumption else None

            if not matched_assumption and assumptions:
                unknown_subjects.append(subject)

            if verdict == "falsified":
                if branch is None:
                    contradictions.append(subject)
                alignment.append({
                    "assumption": subject, "observed": "falsified",
                    "predicted_delta_d": None,
                    "branch_fired": branch is not None,
                    "aligned": branch is not None,
                })
            elif verdict == "unobserved":
                unobserved.append(subject)
                alignment.append({
                    "assumption": subject, "observed": "unobserved",
                    "predicted_delta_d": None, "branch_fired": False, "aligned": None,
                })
            else:
                alignment.append({
                    "assumption": subject, "observed": verdict,
                    "predicted_delta_d": None, "branch_fired": False, "aligned": True,
                })

        if contradictions:
            violations.append({
                "code": "REALITY_CONTRADICTION",
                "severity": "HALT",
                "message": ("现实已证伪下列假设，但结构上无对应 ΔD 分支被触发："
                            + ", ".join(contradictions)
                            + "。证据与结构直接矛盾，审计不得判通过。"),
            })

        # ── 规则二：灰度梯度缺位 ──
        if not levels and (ratio is None or float(ratio) >= 1.0):
            violations.append({
                "code": "NO_GRAY_LADDER",
                "severity": "HIGH_RISK",
                "message": ("未声明灰度档位且放量比例为全量 — 一旦崩塌不可逆，"
                            "现实反馈来不及产生就被吞掉。"),
            })

        # ── 规则三：越档仍未观测 ──
        if unobserved and levels:
            violations.append({
                "code": "UNOBSERVED_ASSUMPTION",
                "severity": "WARNING",
                "message": (f"灰度已推进至档位 {levels}，下列假设仍未观测到："
                            + ", ".join(unobserved) + " — 属观测手段缺失，非时间未到。"),
            })
        elif unobserved:
            violations.append({
                "code": "UNOBSERVED_ASSUMPTION",
                "severity": "WARNING",
                "message": "下列假设未观测到且无档位可界定期限：" + ", ".join(unobserved),
            })

        # ── 规则四：反馈对象悬空 ──
        if unknown_subjects:
            violations.append({
                "code": "UNKNOWN_FEEDBACK_SUBJECT",
                "severity": "WARNING",
                "message": "反馈指向未声明的假设：" + ", ".join(unknown_subjects),
            })

        if not feedback:
            warnings.append("未提供现实反馈 — 本次判定仅覆盖结构与灰度，不含现实对齐")

        has_halt = any(v["severity"] == "HALT" for v in violations)
        has_signal = any(v["severity"] in ("HIGH_RISK", "WARNING") for v in violations)

        if has_halt:
            status, reason = "BLOCKED", "REALITY_CONTRADICTION"
        elif any(v["severity"] == "HIGH_RISK" for v in violations):
            status, reason = "HIGH_RISK", next(
                v["code"] for v in violations if v["severity"] == "HIGH_RISK")
        elif has_signal:
            status, reason = "WARNING", next(
                v["code"] for v in violations if v["severity"] == "WARNING")
        else:
            status, reason = "PASS", "ALIGNED"

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "gray_levels": levels,
            "commit_ratio": ratio,
            "observed_count": len(feedback),
            "falsified_without_branch": contradictions,
            "unobserved": unobserved,
            "violations": violations,
            "reality_alignment": alignment,
            "warnings": warnings,
            "pass": status == "PASS",
        }

    # ── internals ──

    @staticmethod
    def _extract_assumptions(ctx: Dict[str, Any]) -> List[str]:
        return _ctx_assumptions(ctx)

    @staticmethod
    def _extract_branches(ctx: Dict[str, Any]) -> List[Dict[str, Any]]:
        return _ctx_branches(ctx)

    def _extract_feedback(self, ctx: Dict[str, Any]) -> Dict[str, str]:
        for key in self.FEEDBACK_KEYS:
            val = ctx.get(key)
            if isinstance(val, dict):
                out: Dict[str, str] = {}
                for k in sorted(val):
                    out[str(k)] = self._normalize(val[k])
                return out
        return {}

    def _normalize(self, value: Any) -> str:
        """归一观测值。无法归一的一律记 unobserved——不猜。"""
        if isinstance(value, bool):
            return "confirmed" if value else "falsified"
        text = str(value).strip().lower()
        if text in self.FALSIFIED:
            return "falsified"
        if text in self.CONFIRMED:
            return "confirmed"
        if text in self.UNOBSERVED:
            return "unobserved"
        return "unobserved"

    @staticmethod
    def _extract_levels(ctx: Dict[str, Any]) -> List[float]:
        for key in GrayFeedbackPlugin.LEVEL_KEYS:
            val = ctx.get(key)
            if isinstance(val, list):
                out = []
                for v in val:
                    if isinstance(v, bool):
                        continue
                    if isinstance(v, (int, float)):
                        out.append(float(v))
                    elif isinstance(v, dict) and isinstance(v.get("ratio"), (int, float)):
                        out.append(float(v["ratio"]))
                if out:
                    return out
        return []

    @staticmethod
    def _extract_ratio(ctx: Dict[str, Any]) -> Optional[float]:
        for key in GrayFeedbackPlugin.RATIO_KEYS:
            val = ctx.get(key)
            if isinstance(val, bool):
                continue
            if isinstance(val, (int, float)):
                return float(val)
        return None

    @staticmethod
    def _match_assumption(subject: str, assumptions: List[str]) -> Optional[str]:
        """匹配口径与 LCH._check_branch_coverage 保持一致：全称文本或 A{i} 编号。"""
        if subject in assumptions:
            return subject
        for i, a in enumerate(assumptions):
            if subject in (f"A{i + 1}", f"□A{i + 1}"):
                return a
        return None

    @staticmethod
    def _find_branch(assumption: Optional[str], branches: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        if not assumption:
            return None
        for b in branches:
            for key in ("assumption", "premise", "target"):
                if str(b.get(key, "")) == assumption:
                    return b
        return None

# ============================================================================
# 分区③ 算子 ⊚ACC — 责任锚定 / Accountability Anchor
# ============================================================================
# ACC — Accountability Anchor Plugin
# ===========================
#
# 责任闭环锚定：穿透集体平庸与组织模糊。
#
# 强制追溯每一个权重分配、参数设定或行为选择背后，
# 具体的、不可推卸的最小决策单元或自然人节点。
#
# 同时汇总前四级（NS/IAP/LCH/CCS）的审计结果，
# 生成最终审计结论与 AUDIT_PASS / AUDIT_WARN / AUDIT_HALT 信号。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

# META — 元因果账本 / Meta-Causal Ledger
# ========================================
#
# 规范第六条元因果基底的**判据化**。五基在此改用因果论术语：
# 溯源缺口 / 并行收敛 / 叙事遮蔽 / 审计有界 / 因果承接。
# 它不引入任何新的因果律，只把规范里已经写死、却在引擎里只停留在注释里的
# 五条元基，落成五个可计算的账本。五条元基的原文与落地口径一一对应：
#
#   溯源缺口  原文：原初宇宙的起点，万事万物的能量本根。它看似无规则地涌动，
#               但随机不在世界，在观测者的知识缺口之中：
#               全部前置因未被解析，故显为溯源缺口。
#         落地：chaos_gaps     未解析的前置因逐条点名（既无分支补偿 ΔD，
#                              也无现实反馈 —— 两条结构化信号都没有）
#               misattributed 把「未解析」说成「随机/运气/说不准」的地方。
#                              这是规范点名要拦截的归因错误：随机不在世界，在缺口。
#
#   并行收敛  原文：最初之始，亦是最终之终。它容纳未来的一切因果链：多线并行，
#               而非分支分叉；极限处唯一收敛（S∞ = S*）。
#         落地：parallel_chains 多起点 —— 合法，这就是「平行」
#               forks           同一对节点的多条边 —— 违规，这就是「分叉」
#               limit_reached   由 ∞ 极限收敛器的状态回传，本算子只读不判
#
#   叙事遮蔽  原文：现实的反面，与现实一体两面，为一切谎言与梦境提供基底。
#               它是叙事事件 N_t 的所在：⊖ 从中析出干逻辑，A6 叙事熵度量其遮蔽程度。
#         落地：a6_narrative_entropy = 遮蔽字符数 / 原文总字符数（有理数，非概率）
#               reality_face         同一时刻的现实面：⇄GRF 的现实对齐状态
#               —— 「一体两面」的两半必须同时出现在账本里，缺任何一半都不算记完。
#
#   审计有界  原文：公平本身：相对的公平，对万物一视同仁，维系世间的动态平衡。
#               这是审计中立的本体表述：审计不参与决策，只审计决策如何形成；
#               A10 审计熵增有界，使演化收敛于 S*。
#         落地：audit_neutrality 审计只审计「决策如何形成」（恒 True，作为断言留痕）
#               a10_audit_entropy 每层新增留痕条数 = 「version 递增速率」的离散版
#               bounded           A10 是否有界 —— 这是自主进化能收敛于 S* 的算术前提，
#                                 也是 evolve() 的停机定理来源。
#
#   因果承接  原文：在万事万物中无处不在；它不是链的自环，而是链的普遍承接：
#               能量动态守恒，每一个果即刻成为下一个因，序不可倒置。
#         落地：succession_intact 承接完整性：序排得出来、且无自环
#               energy_ledger     ⇄ 能量账本（取 ⊙GA 的只做减法结果，不重复估算）
#               —— 「不是链的自环」归 T303；「序不可倒置」归 T305/T307/T308。
#
# 级别：T2_SIGNAL —— 永不阻断
# -------------------------------
# 本算子是**度量与账本**，不是结构性缺失。把度量升格为阻断，等于用
# 「指标不好看」替换「输入不完整」，那正是本引擎一直拒绝的事
# （I-1 非猜测：中断只留给缺失，不留给观感）。因此它取 T2，
# 结构上就不可能翻转任何一次审计的通过与否。
#
# 确定性 · 零随机 · 零概率词 · 零 LLM 调用
# ----------------------------------------------------------------------------

TRACE_ATTRIBUTION_PATTERNS = (
    "随机", "运气", "说不准", "看情况", "玄学", "碰运气", "天意", "听天由命",
    "不可预测", "random", "luck", "lucky", "by chance", "unpredictable",
)


class MetaCausalLedgerPlugin:
    """META 算子：元因果账本（溯源缺口 · 并行收敛 · 叙事遮蔽 · 审计有界 · 因果承接）。"""

    PLUGIN_NAME = "META"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Meta-Causal Ledger — 元因果基底五条元基的判据化账本"

    # 阈值默认值 = 「规范未给数时的显式声明值」。要换口径就换 config，
    # 不允许在别处悄悄改常数（否则同一份输入在不同地方算出不同的 A6 / A10）。
    DEFAULT_NARRATIVE_ENTROPY_CEILING = 0.15
    DEFAULT_AUDIT_ENTROPY_CEILING = 12.0

    BK_UNPARSED_ANTECEDENCE = "trace_gap"
    BK_NONFORKING_CONVERGENCE = "parallel_convergence"
    BK_NARRATIVE_REGISTER = "narrative_occlusion"
    BK_NEUTRALITY_INVARIANT = "bounded_audit"
    BK_EFFECT_TO_CAUSE_SUCCESSION = "causal_succession"

    def __init__(self) -> None:
        self.name = self.PLUGIN_NAME

    # ── main entry ──

    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        ctx = decision_context if isinstance(decision_context, dict) else {}
        prior = ctx.get("_prior_audit_results", {}) or {}

        def _r(name: str) -> Dict[str, Any]:
            val = prior.get(name)
            return val if isinstance(val, dict) else {}

        ns, tpg, grf, ori = _r("NS"), _r("LFT"), _r("GRF"), _r("GA")

        ledger = {
            self.BK_UNPARSED_ANTECEDENCE: self._unparsed_antecedence(ctx, tpg, ns),
            self.BK_NONFORKING_CONVERGENCE: self._nonforking_convergence(ctx, tpg),
            self.BK_NARRATIVE_REGISTER: self._narrative_register(ctx, ns, grf),
            self.BK_NEUTRALITY_INVARIANT: self._neutrality_invariant(ctx, tpg),
            self.BK_EFFECT_TO_CAUSE_SUCCESSION: self._effect_to_cause_succession(ctx, tpg, ori),
        }

        highs = [k for k in sorted(ledger) if ledger[k]["status"] == "HIGH_RISK"]
        warns = [k for k in sorted(ledger) if ledger[k]["status"] == "WARNING"]
        if highs:
            status, reason = "HIGH_RISK", f"META_{highs[0]}"
        elif warns:
            status, reason = "WARNING", f"META_{warns[0]}"
        else:
            status, reason = "PASS", "META_BALANCED"

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "status": status,
            "reason": reason,
            "meta_bases": ledger,
            "high_risk_bases": highs,
            "warning_bases": warns,
            "pass": status == "PASS",
        }

    # ── 五条元基 ──

    def _unparsed_antecedence(self, ctx: Dict[str, Any], tpg: Dict[str, Any],
               ns: Dict[str, Any]) -> Dict[str, Any]:
        """溯源缺口：随机不在溯源缺口之中，只在观测者的知识缺口之中。"""
        topo = tpg.get("topology", {}) or {}
        edges = topo.get("edges", []) or []

        compensated = {str(e.get("src")) for e in edges
                       if str(e.get("dst", "")).startswith(SYM_NODE + "ΔD")}
        observed = {str(k) for k in (ctx.get("feedback") or {})}

        gaps: List[Dict[str, Any]] = []
        for node in topo.get("nodes", []) or []:
            nid = str(node.get("id", ""))
            if not nid.startswith(SYM_NODE + "A"):
                continue
            if nid in compensated:
                continue          # 前置因已被 ΔD 补偿路径解析
            if str(node.get("note", "")) in observed:
                continue          # 前置因已被现实反馈解析
            gaps.append({
                "node": nid,
                "gap": "前置因未被解析：既无分支补偿 ΔD，也无现实反馈",
            })

        text = self._text(ctx).lower()
        misattributed = [p for p in TRACE_ATTRIBUTION_PATTERNS if p.lower() in text]

        if misattributed and gaps:
            status, reason = "HIGH_RISK", "TRACE_MISATTRIBUTED_WITH_GAPS"
        elif misattributed:
            status, reason = "WARNING", "TRACE_MISATTRIBUTED"
        elif gaps:
            status, reason = "WARNING", "TRACE_GAPS_UNRESOLVED"
        else:
            status, reason = "PASS", "TRACE_RESOLVED"

        return {
            "status": status,
            "reason": reason,
            "gaps": gaps,
            "gap_count": len(gaps),
            "misattributed": misattributed,
            "doctrine": "随机不在世界，在观测者的知识缺口之中",
        }

    def _nonforking_convergence(self, ctx: Dict[str, Any], tpg: Dict[str, Any]) -> Dict[str, Any]:
        """并行收敛：多线并行，而非分支分叉；极限处唯一收敛。"""
        order = (tpg.get("topology", {}) or {}).get("time_order", {}) or {}
        forks = order.get("forks", []) or []
        parallel = int(order.get("parallel_chains", 0) or 0)

        lim = ctx.get("_limit_state")
        limit_reached = bool(isinstance(lim, dict) and lim.get("limit_reached"))

        status = "WARNING" if forks else "PASS"
        reason = "CONVERGENCE_FORK_VIOLATION" if forks else "CONVERGENCE_PARALLEL_OK"
        return {
            "status": status,
            "reason": reason,
            "parallel_chains": parallel,
            "forks": forks,
            "fork_count": len(forks),
            "limit_reached": limit_reached,
            "doctrine": "平行是同一世界线上多条各自有序的链；分支是未来真的分叉。"
                        "SPL 是强决定论，只承认前者。",
        }

    def _narrative_register(self, ctx: Dict[str, Any], ns: Dict[str, Any],
                  grf: Dict[str, Any]) -> Dict[str, Any]:
        """叙事遮蔽：叙事事件 N_t 的所在；A6 叙事熵度量其遮蔽程度。"""
        text = self._text(ctx)
        segments = ns.get("narrative_segments", []) or []
        masked = sum(len(str(s.get("marker", ""))) for s in segments
                     if isinstance(s, dict))
        total = len(text)
        a6 = round(masked / total, 6) if total else 0.0
        ceiling = self._ceiling(ctx, "narrative_entropy_ceiling",
                                self.DEFAULT_NARRATIVE_ENTROPY_CEILING)

        status = "WARNING" if a6 > ceiling else "PASS"
        return {
            "status": status,
            "reason": "NARRATIVE_OCCLUDED" if status == "WARNING" else "NARRATIVE_TRANSPARENT",
            "a6_narrative_entropy": a6,
            "masked_chars": masked,
            "total_chars": total,
            "ceiling": ceiling,
            # 一体两面的另一半：现实面。此处只记录，不继承它的严重度，
            # 否则同一个现实问题会在 GRF 与 META 里被计两次。
            "reality_face": {
                "status": grf.get("status"),
                "reason": grf.get("reason"),
            },
            "doctrine": "叙事遮蔽与现实一体两面；A6 只度量遮蔽，不判断对错",
        }

    def _neutrality_invariant(self, ctx: Dict[str, Any], tpg: Dict[str, Any]) -> Dict[str, Any]:
        """审计有界：审计中立；A10 审计熵增有界，使演化收敛于 S*。"""
        topo = tpg.get("topology", {}) or {}
        provenance = topo.get("provenance", []) or []

        spiral = ctx.get("_spiral_state")
        layers = 1
        if isinstance(spiral, dict):
            layer_list = spiral.get("layers") or []
            if isinstance(layer_list, list) and layer_list:
                layers = len(layer_list)

        a10 = round(len(provenance) / layers, 6) if layers else 0.0
        ceiling = self._ceiling(ctx, "audit_entropy_ceiling",
                                self.DEFAULT_AUDIT_ENTROPY_CEILING)
        bounded = a10 <= ceiling

        return {
            "status": "PASS" if bounded else "WARNING",
            "reason": "AUDIT_BOUNDED" if bounded else "AUDIT_ENTROPY_UNBOUNDED",
            # 审计中立的本体断言：引擎只审计「决策如何形成」，
            # 不参与决策、不出建议、不给排名 —— 这三条在结构上由
            # FORBIDDEN_LLM_KEYS 与决策无关性共同保证。
            "audit_neutrality": True,
            "a10_audit_entropy": a10,
            "ceiling": ceiling,
            "bounded": bounded,
            "provenance_entries": len(provenance),
            "layers": layers,
            "doctrine": "审计不参与决策，只审计决策如何形成；熵增有界则演化收敛于 S*",
        }

    def _effect_to_cause_succession(self, ctx: Dict[str, Any], tpg: Dict[str, Any],
                ori: Dict[str, Any]) -> Dict[str, Any]:
        """因果承接：不是链的自环，而是链的普遍承接；果即刻成因，序不可倒置。"""
        order = (tpg.get("topology", {}) or {}).get("time_order", {}) or {}
        assignable = bool(order.get("assignable"))
        inverted = order.get("inverted", []) or []

        succession = assignable and not inverted
        return {
            "status": "PASS" if succession else "WARNING",
            "reason": "SUCCESSION_INTACT" if succession
                      else "SUCCESSION_BROKEN",
            "succession_intact": succession,
            "assignable": assignable,
            "inverted": inverted,
            "observer_anchor": order.get("observer_anchor", ""),
            "observer_chain_size": order.get("observer_chain_size", 0),
            # 能量账本直接取 ⊙GA 的只做减法结果，不在本算子重算一遍 ——
            # 同一件事算两次，迟早会算出两个数。
            "energy_ledger": ori.get("resource_ledger", []),
            "doctrine": "它不是链的自环，而是链的普遍承接；序不可倒置",
        }

    # ── internals ──

    @staticmethod
    def _text(ctx: Dict[str, Any]) -> str:
        """与 ⊗NS 同源取文：保证 A6 度量的是 NS 实际看过的那段文本。"""
        if isinstance(ctx, str):
            return ctx
        for key in ("text", "narrative", "output", "content",
                    "decision_text", "llm_output", "background", "summary", "description"):
            val = ctx.get(key)
            if isinstance(val, str) and val.strip():
                return val
        if isinstance(ctx.get("decision"), str):
            return ctx["decision"]
        return ""

    @staticmethod
    def _ceiling(ctx: Dict[str, Any], key: str, default: float) -> float:
        cfg = ctx.get("_config")
        if isinstance(cfg, dict) and key in cfg:
            try:
                return float(cfg[key])
            except (TypeError, ValueError):
                return default
        return default


# ============================================================================
# 分区③ 算子 ⊚ACC — 责任锚定 + 最终裁定 / Accountability Anchor
# ============================================================================

class StateAnchorPlugin:
    """ACC 算子：责任锚定 + 最终裁定。"""

    PLUGIN_NAME = "ACC"
    PLUGIN_VERSION = "1.0.0"
    PLUGIN_DESCRIPTION = "Accountability Anchor — 责任闭环锚定 + 最终审计裁定"

    def __init__(self):
        self.name = self.PLUGIN_NAME

    # ── main entry ──
    def analyze(self, decision_context: Dict[str, Any]) -> Dict[str, Any]:
        account = decision_context.get("_responsibility_account", {})
        prior_reports = decision_context.get("_prior_audit_results", {})

        # 1. 责任锚定
        responsibility = self._anchor_responsibility(account, decision_context)

        # 2. 汇总前四级结果
        verdict = self._aggregate_verdict(prior_reports)

        # 3. 生成审计证书
        certificate = self._generate_certificate(
            responsibility, verdict, decision_context
        )

        return {
            "plugin": self.PLUGIN_NAME,
            "version": self.PLUGIN_VERSION,
            "responsibility": responsibility,
            "verdict": verdict,
            "certificate": certificate,
            "pass": verdict["level"] != "AUDIT_HALT",
        }

    # ── internals ──

    @staticmethod
    def _anchor_responsibility(account: Dict[str, Any],
                               ctx: Dict[str, Any]) -> Dict[str, Any]:
        """穿透组织模糊，锚定到最小决策单元。"""
        org = account.get("organization", ctx.get("organization", "UNKNOWN"))
        role = account.get("role", ctx.get("role", "UNKNOWN"))
        stage = account.get("stage", ctx.get("stage", "UNKNOWN"))
        nonce = account.get("nonce", ctx.get("nonce", "UNANCHORED"))

        # 检测组织模糊
        is_vague = org in ("UNKNOWN", "", "集体", "团队", "公司", "各部门",
                           "group", "team", "company", "everyone", "all")

        anchor = {
            "organization": org,
            "role": role,
            "stage": stage,
            "nonce": nonce,
            "is_vague": is_vague,
            "anchor_status": "UNANCHORED" if is_vague else "ANCHORED",
            "warning": None,
        }

        if is_vague:
            anchor["warning"] = (
                f"责任主体 '{org}' 为组织模糊表述 — "
                f"必须追溯至具体的、不可推卸的最小决策单元或自然人节点"
            )

        return anchor

    @staticmethod
    def _aggregate_verdict(prior: Dict[str, Any]) -> Dict[str, Any]:
        """汇总全部算子结果，生成最终裁定。

        分两步，缺一不可：
          ① 专用摘录 —— 针对 NS/IAP/LCH/CCS 的既有字段做细粒度提取，
             保留 halt_items 里「哪一条违规」的可读信息；
          ② 通用扫描 —— 对 **所有** 产出 `status` 的算子做统一映射，
             使 ⊙GA / ⊞LFT / ⇄GRF 三项新增算子无需改动本函数即可被计入。
             少了这一步，新增算子的 BLOCKED 会被静默吞掉。
        """
        ns_result   = prior.get("NS", {})
        iap_result  = prior.get("IAP", {})
        lch_result  = prior.get("LCH", {})
        ccs_result  = prior.get("CCS", {})

        # 收集所有 HALT
        halts: List[str] = []
        warns: List[str] = []

        # NS
        if not ns_result.get("pass", True):
            warns.append(f"NS: {ns_result.get('violation_count', 0)} 叙事违规")

        # IAP
        for flag in iap_result.get("flags", []):
            if flag.get("severity") == "HALT":
                halts.append(f"IAP: {flag.get('flag_type', 'unknown')}")
            elif flag.get("severity") == "WARN":
                warns.append(f"IAP: {flag.get('flag_type', 'unknown')}")

        # LCH
        if not lch_result.get("pass", True):
            sys_dd = lch_result.get("system_delta_d", 0)
            warns.append(f"LCH: system Delta D = {sys_dd}")
            if sys_dd >= 0.7:
                halts.append(f"LCH: system Delta D = {sys_dd} ≥ 0.7 — 系统崩塌风险")

        # CCS
        for check in ccs_result.get("checks", []):
            if check.get("severity") == "HALT":
                halts.append(f"CCS: {check.get('check', 'unknown')} — {check.get('result', '')}")
            elif check.get("severity") == "WARN":
                warns.append(f"CCS: {check.get('check', 'unknown')} — {check.get('result', '')}")

        # ② 通用扫描：所有带 status 的算子统一映射（⊙GA / ⊞LFT / ⇄GRF 由此计入）
        BLOCKING = {"BLOCKED", "CRITICAL"}
        RISKY = {"HIGH_RISK", "WARNING"}
        operator_statuses: Dict[str, str] = {}
        extra_halts: List[str] = []
        extra_warns: List[str] = []
        for name in sorted(prior):
            result = prior.get(name)
            if not isinstance(result, dict):
                continue
            status = result.get("status")
            if status is None:
                continue
            operator_statuses[name] = str(status)
            label = f"{name}: {result.get('reason', status)}"
            if status in BLOCKING:
                extra_halts.append(label)
            elif status in RISKY:
                extra_warns.append(label)

        # v2.0 兼容：只有原五算子的路径下，五算子都不产出 status，两个 extra 列表恒为空，
        # 故此处不改动 halts / warns —— 只跑原五算子子集时的报告因此逐字节不变
        #（老调用方仍按那套形状比对哈希）。通用扫描一旦有内容，才合并去重
        #（专用摘录在前，通用扫描在后）。
        if extra_halts or extra_warns:
            halts = list(dict.fromkeys(halts + extra_halts))
            warns = list(dict.fromkeys(warns + extra_warns))

        # 最终裁定
        if halts:
            level = "AUDIT_HALT"
            summary = f"审计阻断: {len(halts)} 项致命违规"
        elif warns:
            level = "AUDIT_WARN"
            summary = f"审计警告: {len(warns)} 项需关注"
        else:
            level = "AUDIT_PASS"
            summary = "审计通过: 无致命违规，无警告"

        core_flags = {
            "ns_pass": ns_result.get("pass", True),
            "iap_pass": iap_result.get("pass", True),
            "lch_pass": lch_result.get("pass", True),
            "ccs_pass": ccs_result.get("pass", True),
        }
        for op in ("GA", "LFT", "GRF", "META"):
            if op in prior and isinstance(prior.get(op), dict):
                core_flags[f"{op.lower()}_pass"] = bool(prior[op].get("pass", True))

        verdict = {
            "level": level,
            "summary": summary,
            "halt_items": halts,
            "warn_items": warns,
            "halt_count": len(halts),
            "warn_count": len(warns),
        }
        # 同样为了 v2.0 报告逐字节不变：五算子路径下该映射为空，不写入。
        if operator_statuses:
            verdict["operator_statuses"] = operator_statuses
        verdict.update(core_flags)
        return verdict

    @staticmethod
    def _generate_certificate(resp: Dict[str, Any], verdict: Dict[str, Any],
                              ctx: Dict[str, Any]) -> Dict[str, Any]:
        """生成不可篡改的审计证书（哈希签名）。

        可复现性：timestamp 取自 ctx['_clock']（engine.set_clock 注入）。
        未注入时退回系统墙钟，此时证书跨时间不可复现。

        V3b（SPE 1.1.0 起解决）：证书绑定原始输入摘要 input_digest——
        对 decision_context 做 canonical JSON（键排序、紧凑分隔符、剔除
        '_' 前缀内部键）后取 SHA-256。输入任何字节级改动都会改变签名，
        证书由此可与被审输入一对一核对（certificate input-binding）。
        """
        clock = ctx.get("_clock")
        timestamp = int(clock) if clock is not None else int(time.time())
        # 输入摘要：canonical JSON（sort_keys + 紧凑分隔符），剔除内部键
        canonical_ctx = {
            k: v for k, v in ctx.items()
            if not (isinstance(k, str) and k.startswith("_"))
        }
        input_digest = hashlib.sha256(
            json.dumps(canonical_ctx, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), default=str).encode("utf-8")
        ).hexdigest()
        # 构造待签名字符串（V3b 起 input_digest 入签）
        sig_input = (
            f"{resp.get('organization','')}"
            f"|{resp.get('role','')}"
            f"|{resp.get('stage','')}"
            f"|{resp.get('nonce','')}"
            f"|{verdict.get('level','')}"
            f"|{verdict.get('halt_count',0)}"
            f"|{verdict.get('warn_count',0)}"
            f"|{timestamp}"
            f"|{input_digest}"
        )
        sig_hash = hashlib.sha256(sig_input.encode("utf-8")).hexdigest()

        return {
            "audit_id": f"SPL-{resp.get('nonce', '00000000')}-{timestamp}",
            "timestamp": timestamp,
            "input_digest": input_digest,
            "signature": sig_hash,
            "algorithm": "SHA-256",
            "verifiable": True,
            "note": f"本证书由第二视角引擎 SPE {SPE_VERSION} 生成，"
                    "签名覆盖责任锚、裁定与原始输入摘要（input_digest）。"
                    "任何篡改将导致哈希不匹配。",
        }

# ============================================================================
# 分区④ 编排层 ↻ — 叠加螺旋层栈 / Superimposed Spiral Stack
# ============================================================================
# SPR — ↻ 叠加螺旋式迭代思考链路 / Superimposed Spiral Chain
# =========================================================
#
# 实现 p♾️q 因果螺旋：每一次 ⊛ 拓扑重构生成**新的拓扑层**，而**不是覆盖旧层**。
#
# 叠加 ≠ 覆盖
# -----------
# 引擎 v1 时代的迭代是一行 `ctx.update(delta)`：上一轮的结构被新字典抹掉，
# 所以它只能做「重试」，做不成「螺旋」。螺旋的定义性特征是：
#
#     已收敛的子图被冻结为骨架，后续每一层在这个骨架上继续生长。
#
# 因此本模块把「收敛了什么」变成不可撤销的账目：
#
#     frozen 集合单调不减。第 n 层冻结的节点，第 n+1 层不得解冻。
#     一旦检出解冻，记 SUPERPOSITION_VIOLATION —— 螺旋退化为覆盖，
#     此时「迭代」只是在原地打转，正是规范要拦截的那类「假螺旋」。
#
# 三道硬约束
# ----------
#   1. 原点不可漂移   origin_hash 一旦确立即为锚点；后续层不同即 ORIGIN_DRIFT。
#                     这是螺旋最致命的失效模式——绕圈绕到目标已经不是原来那个。
#   2. 能量守恒       ↻ 每层消耗 loop_cost；预算不足以再走一层即停。
#                     拓扑无边界，但预算有硬顶（因果承接公理）。
#   3. 半径单调       radius = 未收敛风险集规模。半径必须随层数收敛；
#                     若连续两层半径不降且状态为 DIVERGED，标记 FLAT_SPIRAL。
#
# 本模块只做账，不做判定——收敛状态由引擎的 ConvergenceChecker 给出。
#
# 确定性 · 零随机 · 零 LLM 调用
# ----------------------------------------------------------------------------

@dataclass
class SpiralLayer:
    """螺旋的一圈。层是只读快照，生成后不再改动。"""

    index: int
    state: str
    origin_hash: str
    radius: int
    risk_set: List[str]
    frozen_nodes: List[str]
    graph_hash: str
    topology: Dict[str, Any]
    layer_hash: str
    cost: float
    energy_left: Optional[float]
    # 到目标稳态 S* 的距离 = (风险集规模, 是否有未决假设)，字典序比较。
    # 极限收敛器判定「还在不在逼近」的唯一依据。
    distance: Tuple[int, int] = (0, 0)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "index": self.index, "state": self.state,
            "origin_hash": self.origin_hash, "radius": self.radius,
            "risk_set": self.risk_set, "frozen_nodes": self.frozen_nodes,
            "graph_hash": self.graph_hash, "layer_hash": self.layer_hash,
            "cost": self.cost, "energy_left": self.energy_left,
            "distance": list(self.distance),
            "topology": self.topology,
        }


class SpiralStack:
    """螺旋层栈：管账、管冻结、管漂移。"""

    def __init__(self, energy_budget: Optional[float] = None, loop_cost: float = 1.0):
        if loop_cost <= 0:
            raise ValueError("loop_cost must be > 0")
        if energy_budget is not None and energy_budget < 0:
            raise ValueError("energy_budget must be >= 0")
        self.energy_budget = None if energy_budget is None else float(energy_budget)
        self.loop_cost = float(loop_cost)
        self.layers: List[SpiralLayer] = []
        self._origin_anchor: Optional[str] = None
        self._frozen: Set[str] = set()
        self._spent: float = 0.0
        self.violations: List[Dict[str, Any]] = []

    # -------- 账目 --------

    @property
    def energy_left(self) -> Optional[float]:
        if self.energy_budget is None:
            return None
        return round(self.energy_budget - self._spent, 6)

    def can_run(self, count: int = 1) -> bool:
        """预算是否还够再走 count 层。无预算声明时恒为 True（拓扑无边界）。"""
        if self.energy_budget is None:
            return True
        return (self._spent + self.loop_cost * count) <= self.energy_budget + 1e-9

    @property
    def frozen_nodes(self) -> List[str]:
        return sorted(self._frozen)

    # -------- 漂移 --------

    def origin_drift(self, origin_hash: str) -> bool:
        """原点漂移检测。首次确立锚点，其后不一致即为漂移。"""
        if not origin_hash:
            return False
        if self._origin_anchor is None:
            self._origin_anchor = origin_hash
            return False
        return origin_hash != self._origin_anchor

    @property
    def origin_anchor(self) -> Optional[str]:
        return self._origin_anchor

    # -------- 压栈 --------

    def push(
        self,
        *,
        state: str,
        origin_hash: str,
        risk_set: Sequence[str],
        graph_hash: str,
        topology: Dict[str, Any],
        converged_nodes: Sequence[str] = (),
        index: Optional[int] = None,
        unresolved: bool = False,
    ) -> SpiralLayer:
        """压入新的一层。

        converged_nodes 是本层**新增**收敛的节点（引擎按相邻两层 1-邻域一致判定），
        压栈时并入冻结集合——只增不减。

        覆盖检测：已冻结节点必须仍存在于本层拓扑中。若某个被宣布收敛的节点
        在后续层里消失了，说明这一层把上层抹掉了——螺旋退化成了覆盖。

        unresolved 表示本层是否仍有未决假设（IAP missing_required）；它与半径共同
        构成本层的「距离」distance = (风险集规模, 是否有未决假设)。
        """
        idx = len(self.layers) if index is None else index

        node_ids = {
            str(n.get("id")) for n in (topology or {}).get("nodes", [])
            if isinstance(n, dict) and n.get("id")
        }
        vanished = sorted(self._frozen - node_ids)
        if vanished:
            self.violations.append({
                "code": "SUPERPOSITION_VIOLATION",
                "severity": "HALT",
                "message": (f"第 {idx} 层拓扑中已冻结节点 {vanished} 消失 — "
                            "螺旋退化为覆盖，已收敛子图必须叠加保留。"),
            })

        incoming = {str(n) for n in converged_nodes}
        self._frozen |= incoming

        risks = sorted(str(r) for r in risk_set)
        layer_hash = hashlib.sha256(json.dumps({
            "index": idx, "state": state, "origin_hash": origin_hash,
            "radius": len(risks), "graph_hash": graph_hash,
        }, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]

        self._spent += self.loop_cost
        layer = SpiralLayer(
            index=idx, state=state, origin_hash=origin_hash,
            radius=len(risks), risk_set=risks,
            frozen_nodes=self.frozen_nodes,
            graph_hash=graph_hash, topology=topology,
            layer_hash=layer_hash, cost=self.loop_cost,
            energy_left=self.energy_left,
            distance=(len(risks), 1 if unresolved else 0),
        )
        self.layers.append(layer)
        return layer

    # -------- 层间差分 --------

    def diff(self, i: int, j: int) -> Dict[str, Any]:
        """第 i 层 → 第 j 层的结构差分。

        只报「新增/消失的节点、边、风险」，不下「变好了」这种结论。
        """
        if not (0 <= i < len(self.layers) and 0 <= j < len(self.layers)):
            raise IndexError("layer index out of range")
        a, b = self.layers[i], self.layers[j]

        def nodes_of(layer: SpiralLayer) -> Set[str]:
            return {n["id"] for n in layer.topology.get("nodes", []) if isinstance(n, dict)}

        def edges_of(layer: SpiralLayer) -> Set[str]:
            return {f'{e.get("src")}→{e.get("dst")}:{e.get("relation")}'
                    for e in layer.topology.get("edges", []) if isinstance(e, dict)}

        na, nb = nodes_of(a), nodes_of(b)
        ea, eb = edges_of(a), edges_of(b)
        return {
            "from_layer": i, "to_layer": j,
            "radius_delta": b.radius - a.radius,
            "nodes_added": sorted(nb - na), "nodes_removed": sorted(na - nb),
            "edges_added": sorted(eb - ea), "edges_removed": sorted(ea - eb),
            "risks_added": sorted(set(b.risk_set) - set(a.risk_set)),
            "risks_cleared": sorted(set(a.risk_set) - set(b.risk_set)),
            "origin_drift": a.origin_hash != b.origin_hash,
        }

    def radius_trend(self) -> List[int]:
        return [layer.radius for layer in self.layers]

    def distance_trend(self) -> List[Tuple[int, int]]:
        """到目标稳态 S* 的距离序列：distance = (风险集规模, 是否有未决假设)。

        字典序比较——风险集更小者更近；规模相同时无未决假设者更近。
        整条序列不含任何权重估计，因此可跨进程复算。
        """
        return [layer.distance for layer in self.layers]

    def check_flat(self, layers: int = 3) -> bool:
        """半径连续 layers 层不降 → 平螺旋（在原地扩圈，没有上升）。"""
        r = self.radius_trend()
        if len(r) < layers:
            return False
        return all(r[i] >= r[i - 1] for i in range(len(r) - layers + 1, len(r)))

    def is_static(self, layers: int = 3) -> bool:
        """半径连续 layers 层**完全不变** → 画地为牢：这一圈和上一圈一模一样。

        与 is_plateau 的区别：is_plateau 覆盖「不变或变差」，本方法只认「纹丝不动」。
        必须由本方法先分流，否则 is_plateau 会永远抢先命中：因为 distance 的首分量
        就是半径，一旦半径下降，distance 必然严格下降，所以「距离不严格下降」蕴含
        「半径未下降」——不先分流「原地不动」，FLAT_SPIRAL 就成了死代码。
        """
        r = self.radius_trend()
        if len(r) < layers:
            return False
        return len(set(r[-layers:])) == 1

    def is_plateau(self, layers: int = 3) -> bool:
        """距离连续 layers 层**不严格下降** → 不再逼近 S*。

        宽容口径：拓扑变形常有平台期，故要求连续 layers 层都没出现严格下降才判。
        """
        d = self.distance_trend()
        if len(d) < layers:
            return False
        return all(d[i] >= d[i - 1] for i in range(len(d) - layers + 1, len(d)))

    def limit_reached(self, layers: int = 2) -> bool:
        """距离连续 layers 层均为 (0, 0) → 抵达极限 S∞ = S*。

        注意它要求「保持」而非「碰到」：一次归零可能只是碰巧，连续归零才是极限。
        """
        d = self.distance_trend()
        return len(d) >= layers and all(x == (0, 0) for x in d[-layers:])

    # -------- 续跑（外部驱动无限迭代） --------

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SpiralStack":
        """从 to_dict() 的快照恢复栈状态，供外部逐层推进续跑。

        只恢复账目与层快照，不恢复任何可调用对象——所以快照可以落盘、可以跨进程
        传递，但**伪造不出引擎没算过的层**。
        """
        stack = cls(energy_budget=data.get("energy_budget"),
                    loop_cost=float(data.get("loop_cost", 1.0) or 1.0))
        stack._spent = float(data.get("energy_spent", 0.0) or 0.0)
        stack._origin_anchor = data.get("origin_anchor")
        stack._frozen = {str(n) for n in (data.get("frozen_nodes") or [])}
        stack.violations = [dict(v) for v in (data.get("violations") or [])]

        for ld in (data.get("layers") or []):
            raw = ld.get("distance")
            distance = (tuple(raw) if isinstance(raw, (list, tuple)) and len(raw) == 2
                        else (int(ld.get("radius", 0)), 0))
            stack.layers.append(SpiralLayer(
                index=int(ld["index"]), state=str(ld["state"]),
                origin_hash=str(ld.get("origin_hash", "")),
                radius=int(ld.get("radius", 0)),
                risk_set=[str(x) for x in (ld.get("risk_set") or [])],
                frozen_nodes=[str(x) for x in (ld.get("frozen_nodes") or [])],
                graph_hash=str(ld.get("graph_hash", "")),
                topology=ld.get("topology") or {},
                layer_hash=str(ld.get("layer_hash", "")),
                cost=float(ld.get("cost", 0.0) or 0.0),
                energy_left=ld.get("energy_left"),
                distance=(int(distance[0]), int(distance[1])),
            ))
        return stack

    # -------- 汇总 --------

    def to_dict(self) -> Dict[str, Any]:
        return {
            "spiral_version": "1.0.0",
            "layer_count": len(self.layers),
            "energy_budget": self.energy_budget,
            "loop_cost": self.loop_cost,
            "energy_spent": round(self._spent, 6),
            "energy_left": self.energy_left,
            "origin_anchor": self._origin_anchor,
            "frozen_nodes": self.frozen_nodes,
            "radius_trend": self.radius_trend(),
            "distance_trend": [list(d) for d in self.distance_trend()],
            "flat_spiral": self.check_flat(),
            "plateau": self.is_plateau(),
            "limit_reached": self.limit_reached(),
            "violations": self.violations,
            "layers": [layer.to_dict() for layer in self.layers],
        }
# ==================== 第二视角引擎核心 ====================

class SecondPerspectiveEngine:
    """SPE 1.0 规范参考内核。"""

    # ⚙ 十算子的权限分配。一句话概括：只有「结构性缺失」才能阻断，
    #   「量化意见」不能。
    #     ⊙GA  T1 —— 原点真空 = 链无起点，结构性缺失，可阻断
    #     ⊗NS   T3 —— 只输出剥离后的文本骨架，本就不参与判定
    #     ⊕IAP  T2 —— 发现隐含假设是「提示」，不足以单独阻断
    #     ⊿LCH  T2 —— 脆弱性是量化信号，权重未经统计校准，只能提示
    #     ⊞LFT  T1 —— 拓扑不合法（身份冲突/参数越界）可直接终止推演
    #     BFC   T1 —— 证据真空/证据互斥/已证伪前提仍在使用，都是结构性缺陷
    #     ⚙CCS  T1 —— 信息黑洞属「必需输入缺失」，可以且必须阻断
    #     ⇄GRF  T1 —— 现实已证伪却无回退路径，是证据与结构的直接矛盾
    #     META  T2 —— 元因果账本是**度量**：A6 叙事熵 / A10 审计熵增 / 缺口账本。
    #                 指标不好看不等于输入不完整，故结构上不允许它阻断。
    #     ⊚ACC T1 —— 汇总裁定，本身就是阻断的出口
    #
    # 类级常量（不是实例状态）：闸门要靠它判定「谁是官方算子」，
    # 因此必须在构造引擎之前就已就位，不能等到 load_core_plugins() 才填充。
    CORE_OPERATOR_TIERS: Dict[str, PluginTier] = {
        'GA': PluginTier.T1_STRUCTURAL,
        'NS': PluginTier.T3_NARRATIVE,
        'IAP': PluginTier.T2_SIGNAL,
        'LCH': PluginTier.T2_SIGNAL,
        'LFT': PluginTier.T1_STRUCTURAL,
        'BFC': PluginTier.T1_STRUCTURAL,
        'CCS': PluginTier.T1_STRUCTURAL,
        'GRF': PluginTier.T1_STRUCTURAL,
        'META': PluginTier.T2_SIGNAL,
        'ACC': PluginTier.T1_STRUCTURAL,
    }

    # 外部扩展算子只允许这两个权限层 —— 不允许外部逻辑改动「能不能通过」。
    EXTENSION_ALLOWED_TIERS = (PluginTier.T2_SIGNAL, PluginTier.T3_NARRATIVE)

    # 流水线定序：ACC 必须最后（它汇总前面所有算子）。
    # 其余顺序即规范的标准拓扑推理流程：先锚定原点，再去语义化，
    # 再逐级加固，再核验事实成真性，再谈灰度与现实，最后结算元因果账本。
    # META 排在 GRF 之后、ACC 之前：它要读 NS（A6 用段）、LFT（时序与留痕）、
    # GRF（现实面）、GA（能量账本）四家的结果，读完正好交给 ACC 汇总。
    PIPELINE_ORDER: List[str] = ['GA', 'NS', 'IAP', 'LCH', 'LFT', 'BFC',
                                 'CCS', 'GRF', 'META', 'ACC']

    # LLM 护栏 L-1..L-3：LLM 可以说话，但不能影响结构判定。
    # 这些键一旦出现在 LLM 输出里会被剥离并标记 _tier_violation，
    # 覆盖三类越权：
    #   状态裁决  status / converged / is_converged / blocked / adjudicated
    #   权重排序  weight / score / rank
    #   结论判断  verdict / decision
    # 换句话说：即便模型照着提示词返回了裁决字段，也进不了结构判定。
    FORBIDDEN_LLM_KEYS = {
        'status', 'converged', 'is_converged', 'blocked',
        'adjudicated', 'weight', 'score', 'rank', 'verdict', 'decision',
    }

    def __init__(self, account: ResponsibilityAccount, config: Optional[Dict[str, Any]] = None):
        self.account = account
        self.config: Dict[str, Any] = config or {}
        self.plugins: List[AuditPlugin] = []
        # 执行顺序：类属性是官方十算子的默认序；实例复制一份，
        # 使经唯一插件缝注册的扩展算子只影响本引擎实例，不污染其他实例。
        self.PIPELINE_ORDER: List[str] = list(type(self).PIPELINE_ORDER)
        self.llm_provider: Optional[LLMProvider] = None
        self.llm_default_tier: LLMPermissionTier = LLMPermissionTier.T3_NARRATIVE
        self.event_chain: List[AuditEvent] = []
        self._prev_event_hash: str = 'ROOT'
        self._clock: Optional[float] = None
        # 人工批准过的进化候选（记账，不改代码）。它是版本谱系的代际依据：
        # 代际 = len(_evolution_approvals)，因此「这份链根属于第几代引擎」可自证。
        self._evolution_approvals: List[Dict[str, Any]] = []

        # 阶段白名单：config['allowed_stages'] 非空时，account.stage 必须落在其中，
        # 否则构造直接失败。这是第一道闸——责任节点本身就不合规时，
        # 没必要再跑算子。
        allowed_stages = self.config.get('allowed_stages', [])
        if allowed_stages and account.stage not in allowed_stages:
            raise ValueError(f'Unsupported stage: {account.stage}')

    # -------- 注册 --------

    def set_llm_provider(
        self,
        provider: LLMProvider,
        default_tier: LLMPermissionTier = LLMPermissionTier.T3_NARRATIVE,
    ) -> None:
        self.llm_provider = provider
        self.llm_default_tier = default_tier

    # -------- 唯一插件缝（Single Extension Seam） --------
    #
    # 一条 API、四道闸门、一处留痕：
    #   闸门全部收口在 _register() 里执行 —— 无论从哪个入口进来都绕不过。
    #   这不是"靠调用方自觉"的约定，而是唯一的收口点。
    #   留痕写进 report['operator_manifest'] 并参与 report_hash，
    #   使「这份链根是在哪个算子集下产生的」可以被独立验证。

    def register_plugin(self, plugin: AuditPlugin) -> None:
        """低层注册原语 —— **仅供 load_core_plugins() 装载官方十算子使用**。

        外部扩展一律走 register_operator()。此处虽不校验 after，但仍经过
        _register() 的收口闸门，因此不存在"绕过闸门"的路径。
        """
        self._register(plugin, origin="core", registered_after=None)

    def register_operator(
        self,
        name: str,
        tier: PluginTier,
        analyze: Callable[[Dict[str, Any]], Any],
        description: str = "",
        after: Optional[str] = None,
    ) -> str:
        """唯一插件缝：注册一个外部算子。返回算子名。

        四道闸门（任一不过即 ValueError，且**不留任何副作用**）：
          1. name 须为 ASCII 标识符，且不与官方十算子或已注册算子重名
          2. tier 须为 PluginTier 成员，且只能是 T2_SIGNAL / T3_NARRATIVE
             —— 外部算子不得发 BLOCKED：不允许外部逻辑改动「能不能通过」
          3. after 必填，且须指向一个已注册的算子名（显式定序，没有默认落位）
          4. 通过后并入本实例的 PIPELINE_ORDER，紧随 after 之后执行

        适用场景：移植（SPL-G1 / 其他语言）、教学、受控对比实验。
        不适用场景：领域规则 —— 那属于调用方，写进 facts / assumptions /
        criteria / feedback 即可，引擎必须保持 decision-agnostic。
        """
        plugin = AuditPlugin(
            name=name, tier=tier, analyze_func=analyze, description=description,
            origin="extension", registered_after=after,
        )
        self._register(plugin, origin="extension", registered_after=after)
        return name

    def _register(self, plugin: AuditPlugin, origin: str,
                  registered_after: Optional[str]) -> None:
        """注册收口：四道闸门在此执行，任何入口都绕不过。"""
        name = plugin.name

        # 闸门 1a：名字必须是 ASCII 标识符
        # （证书、拓扑、CSV / Markdown 导出都直接落这个名字，必须可读可解析）
        if (not isinstance(name, str) or not name
                or not name.isascii() or not name.isidentifier()):
            raise ValueError(f'算子名必须是 ASCII 标识符: {name!r}')

        # 闸门 1b：重名（含官方十算子）
        if name in {p.name for p in self.plugins}:
            raise ValueError(f'算子名已注册: {name}')

        # 闸门 2：权限层合法，且外部算子不得持 T1
        if not isinstance(plugin.tier, PluginTier):
            raise ValueError(f'算子权限层必须是 PluginTier 成员: {plugin.tier!r}')
        if name not in self.CORE_OPERATOR_TIERS and plugin.tier not in self.EXTENSION_ALLOWED_TIERS:
            raise ValueError(
                f'外部算子不得持 {plugin.tier.value}：只有官方算子可产出 BLOCKED；'
                f'扩展算子只允许 {[t.value for t in self.EXTENSION_ALLOWED_TIERS]}'
            )

        # 闸门 3 + 4：显式定序 —— 紧随 after 之后执行
        if origin == "extension":
            if not registered_after or registered_after not in self.PIPELINE_ORDER:
                raise ValueError(
                    f'扩展算子必须以 after= 显式声明插入位置，且指向已注册算子；'
                    f'收到 after={registered_after!r}'
                )
            self.PIPELINE_ORDER.insert(
                self.PIPELINE_ORDER.index(registered_after) + 1, name)

        self.plugins.append(plugin)

    def set_clock(self, t: Optional[float]) -> None:
        '''注入虚拟时钟以实现可复现审计；传 None 恢复系统墙钟。

        可复现性前提：nonce 已改为按责任账户确定性推导（见 ResponsibilityAccount），
        故在固定 clock 下，审计证书与哈希链根**完全可复现**。
        审计内容（裁定 / 各算子分析）在任何情况下均为决定论。
        '''
        self._clock = t

    # 十算子清单。单文件化后不再有外部 plugins/ 包：算子类就在本文件「分区③」内，
    # 此处只登记「官方十算子分别是哪一类」，实际执行顺序由 PIPELINE_ORDER 定序。
    CORE_OPERATORS: List[type] = [
        OriginAnchorPlugin,          # ⊙ 第一原点锚定
        NarrativeStripPlugin,        # ⊗ 去语义化
        ImplicitAssumptionPlugin,    # ⊕ 约束挖掘
        FragilityLatchPlugin,        # ⊿ 薄弱点加固
        TopologyGraphPlugin,         # ⊞ 无标签拓扑图
        BinaryFactCheckPlugin,       #   二元事实校验
        CausalChainSyncPlugin,       # ⚙ 链闭合扫描
        GrayFeedbackPlugin,          # ⇄ 灰度执行与现实反馈
        MetaCausalLedgerPlugin,      #   元因果账本（溯源缺口·并行收敛·叙事遮蔽·审计有界·因果承接）
        StateAnchorPlugin,           # ⊚ 责任锚定 + 最终裁定
    ]

    def load_core_plugins(self) -> List[str]:
        """加载官方十算子（GA / NS / IAP / LCH / LFT / BFC / CCS / GRF / META / ACC）。

        算子类位于本文件「分区③」，只暴露 ``name`` 与 ``analyze()``；引擎契约要求
        ``AuditPlugin(name, tier, analyze_func, description)``。此处负责包装，
        按 CORE_OPERATOR_TIERS 装配权限层级别，并按 PIPELINE_ORDER 定序。
        返回已注册的算子名列表。权限表是类级常量，此处不再惰性初始化 ——
        插件缝的闸门要靠它在构造后立刻判定「谁是官方算子」。
        """
        registered: List[str] = []
        for cls in self.CORE_OPERATORS:
            instance = cls()
            name = getattr(instance, 'name', cls.PLUGIN_NAME)
            if name not in self.CORE_OPERATOR_TIERS:
                raise ValueError(f'未声明权限层级别的核心算子: {name}')
            self.register_plugin(AuditPlugin(
                name=name,
                tier=self.CORE_OPERATOR_TIERS[name],
                analyze_func=instance.analyze,
                description=getattr(cls, 'PLUGIN_DESCRIPTION', ''),
            ))
            registered.append(name)
        return registered

    # -------- 算子清单（进报告、参与哈希） --------

    def _ordered_plugins(self) -> List[AuditPlugin]:
        """执行顺序的唯一定义点：PIPELINE_ORDER 优先，未登记名按字典序排末尾。

        audit() 与 operator_manifest() 共用它，保证「跑的顺序」与
        「清单里写的顺序」不可能不一致。
        """
        def key(p: AuditPlugin) -> Tuple[int, str]:
            try:
                return (self.PIPELINE_ORDER.index(p.name), p.name)
            except ValueError:
                return (len(self.PIPELINE_ORDER), p.name)

        return sorted(self.plugins, key=key)

    def operator_manifest(self) -> List[Dict[str, Any]]:
        """算子清单：执行顺序 + 权限层 + 来源 + 定序锚点。

        它被写进 report 并（因为 report 整体参与哈希而）被哈希覆盖。
        这不是装饰：清单若不入哈希，谁都能换掉算子集却保留原清单声明，
        留痕就失去证据力。代价是新增/更换算子会改变链根 —— 这是必付的。
        """
        return [{
            'order': i,
            'name': p.name,
            'tier': p.tier.value,
            'origin': p.origin,
            'registered_after': p.registered_after,
        } for i, p in enumerate(self._ordered_plugins())]

    def operator_set_hash(self) -> str:
        """算子集指纹：仅由 (名, 权限层, 顺序) 推导。

        进链上事件，使「这份链根由哪个算子集产生」在证据链上可自证；
        不含 analyze_func、不含描述，因此可跨进程/跨语言复算。
        """
        blob = json.dumps(
            [[m['name'], m['tier'], m['order']] for m in self.operator_manifest()],
            sort_keys=True, ensure_ascii=False,
        )
        return hashlib.sha256(blob.encode('utf-8')).hexdigest()[:16]

    # -------- 哈希链 --------

    def _append_event(self, event_type: str, payload: Dict[str, Any]) -> AuditEvent:
        idx = len(self.event_chain)
        ts = self._clock if self._clock is not None else time.time()
        # 确定性 nonce：由前序哈希 / 事件类型 / 序号推导，取代 uuid4 随机值，
        # 否则同一输入两次运行的链根哈希不同，破坏可复现性。
        nonce = hashlib.sha256(
            f'{self._prev_event_hash}|{event_type}|{idx}'.encode('utf-8')
        ).hexdigest()[:8]
        ev = AuditEvent(
            event_type=event_type,
            payload=payload,
            prev_hash=self._prev_event_hash,
            timestamp=ts,
            nonce=nonce,
        )
        # 封存：自此刻起，内容若被改动即与封存值不符。
        ev.sealed_hash = ev.hash
        self.event_chain.append(ev)
        self._prev_event_hash = ev.sealed_hash
        return ev

    @property
    def chain_root_hash(self) -> str:
        """链根哈希，即最后一个事件的 sealed_hash；空链时为哨兵值「ROOT」。

        这是整个审计的唯一指纹。要对外披露校验凭据，披露的应该是它，
        并且这个值必须存在报告之外的地方（落盘后与报告分离保存）——
        与报告放在一起就等于没有锚点。
        """
        return self._prev_event_hash if self.event_chain else 'ROOT'

    # -------- 算子 ⊗：去语义化（静态前处理）--------

    @staticmethod
    def _strip_narrative(ctx: Dict[str, Any]) -> Dict[str, Any]:
        """剥离主观修饰词。

        只做**标记**不做**删除**：原文完整保留在 out 里，
        命中情况单独记进 _narrative_stripped.flagged_fields。
        因为审计的对象是「这句话说了什么」，不是「这句话该被改成什么」——
        改写原文会破坏证据链，也会让调用方无法核对原文。
        """
        SUBJECTIVE_WORDS = {
            '显然', '毫无疑问', '必然', '肯定', '理所应当', '不言而喻',
            'obviously', 'clearly', 'certainly', 'undoubtedly', 'naturally',
        }
        out = copy.deepcopy(ctx)
        flagged: Dict[str, List[str]] = {}
        for key in ('narrative', 'background', 'summary', 'description'):
            if key in out and isinstance(out[key], str):
                hit = [w for w in SUBJECTIVE_WORDS if w in out[key]]
                if hit:
                    flagged[key] = hit
        out['_narrative_stripped'] = {'flagged_fields': flagged}
        return out

    # -------- 算子 ⊕：约束挖掘（静态前处理）--------

    @staticmethod
    def _surface_implicit_assumptions(ctx: Dict[str, Any]) -> Dict[str, Any]:
        """决定论规则挖掘未声明预设。三条规则，全部是纯结构判断：

          MISSING_CRITERIA        有 alternatives 却无 criteria
          WEIGHTS_NOT_NORMALIZED  criteria 权重之和 != 1.0（容差 1e-6）
          CONCLUSION_WITHOUT_EVIDENCE  有 conclusions 却无 evidence

        关键区别在 missing_required 这个标志，只有前三条中的第 1、3 条会置真，
        权重未归一**不置真**。理由：权重不对只是口径问题，可以修正；
        而「给了备选却不给评估标准」和「下了结论却没证据」是结构性缺陷，
        修正不了——这正是算子 ⊿ 把崩塌等级直接顶到 HIGH 的依据。
        """
        flags: List[Dict[str, Any]] = []
        missing_required = False

        alts = ctx.get('alternatives')
        criteria = ctx.get('criteria')
        if alts and not criteria:
            flags.append({'type': 'MISSING_CRITERIA',
                          'description': '提供了备选方案但未声明评估标准'})
            missing_required = True

        if criteria and isinstance(criteria, dict):
            weights = []
            for v in criteria.values():
                if isinstance(v, dict) and 'weight' in v:
                    weights.append(v['weight'])
            if weights and all(w is not None for w in weights):
                s = sum(float(w) for w in weights)
                if abs(s - 1.0) > 1e-6:
                    flags.append({'type': 'WEIGHTS_NOT_NORMALIZED',
                                  'description': f'权重之和={s}，未归一到1.0', 'sum': s})

        conclusions = ctx.get('conclusions') or ctx.get('recommendation')
        evidence = ctx.get('evidence')
        if conclusions and not evidence:
            flags.append({'type': 'CONCLUSION_WITHOUT_EVIDENCE',
                          'description': '给出了结论但未提供证据'})
            missing_required = True

        ctx['_implicit_assumptions'] = {'flags': flags, 'missing_required': missing_required}
        return ctx

    # -------- 算子 ⊿：薄弱点加固（静态前处理）--------

    @staticmethod
    def _assess_vulnerability(ctx: Dict[str, Any]) -> Dict[str, Any]:
        """定位最脆弱变量并给出崩塌等级（HIGH/MEDIUM/LOW）。

        等级只能**单向上升**，不能回退：
          missing_required 为真          → 直接 HIGH，后面的规则不看
          否则遇 WEIGHTS_NOT_NORMALIZED  → MEDIUM
          否则叙述含主观修饰词           → LOW 提到 weakest，但等级仍为 LOW

        最后一条是有意为之：叙述带修辞是**观察**，不是结构性缺陷，
        不足以把等级抬起来；它只负责指出最脆弱变量在哪。
        """
        implicit = ctx.get('_implicit_assumptions', {})
        flags = implicit.get('flags', [])
        level = CollapseLevel.LOW
        weakest: Optional[str] = None
        reasons: List[str] = []

        if implicit.get('missing_required'):
            level = CollapseLevel.HIGH
            weakest = 'required_assumptions'
            reasons.append('关键假设缺失（评估标准/证据/责任人）')
        else:
            for f in flags:
                if f['type'] == 'WEIGHTS_NOT_NORMALIZED' and level != CollapseLevel.HIGH:
                    level = CollapseLevel.MEDIUM
                    weakest = weakest or 'criteria_weights'
                    reasons.append('评估权重未归一')
            narr = ctx.get('_narrative_stripped', {}).get('flagged_fields')
            if narr and level == CollapseLevel.LOW:
                weakest = weakest or 'narrative_subjectivity'
                reasons.append('叙述中包含主观修饰词')

        ctx['_vulnerability'] = {
            'weakest_variable': weakest,
            'collapse_level': level,
            'reasons': reasons,
        }
        return ctx

    # -------- LLM 护栏 --------

    def _strip_llm_output(self, parsed: Any, tier: LLMPermissionTier) -> Tuple[Dict[str, Any], bool]:
        """剥离 LLM 输出中能影响结构判定的字段。返回 (stripped, violated)。

        violated 表示「LLM 确实越权过」，无论剥离是否成功都会在
        LLMCallRecord.response_excerpt 上打上 [VIOLATION STRIPPED] 前缀。

        三层防线（SPE 1.1 起完整化）：
        ① 白名单压缩（T3_NARRATIVE 层）：整个返回被压缩成**只有** narrative
           一个键（依次尝试 narrative / overall_assessment / reasoning，
           都没有就把剩余内容整体 JSON 化）。T3 连自己新造的字段都带不出去。
        ② 递归剥离（全层级）：FORBIDDEN_LLM_KEYS 在**任意嵌套深度**出现即
           剔除并记违规——防止模型把越权字段藏进嵌套结构
           （如 {'meta': {'status': ...}} 逃过顶层黑名单）。深度上限 12 层，
           超限视为越权尝试整体丢弃。
        ③ 类型约束：剥离后残留的容器值（dict/list）重新扫描确认无禁用键；
           非确定类型一律 str 化，模型输出的任何字节都只能以文字进入报告。

        非 dict 输入（模型没按要求返回 JSON）统一降级为 str 塞进 narrative，
        不会抛错。
        """
        violated = False
        if not isinstance(parsed, dict):
            return {'narrative': str(parsed)}, violated

        _MAX_DEPTH = 12

        def _strip_node(node: Any, depth: int = 0) -> Any:
            nonlocal violated
            if depth > _MAX_DEPTH:
                violated = True
                return None
            if isinstance(node, dict):
                out: Dict[str, Any] = {}
                for k, v in node.items():
                    if isinstance(k, str) and k in self.FORBIDDEN_LLM_KEYS:
                        violated = True
                        continue
                    out[k] = _strip_node(v, depth + 1)
                return out
            if isinstance(node, list):
                return [_strip_node(x, depth + 1) for x in node]
            return node

        stripped = _strip_node(parsed)
        if not isinstance(stripped, dict):
            stripped = {}
        if tier == LLMPermissionTier.T3_NARRATIVE:
            narrative = (stripped.get('narrative') or stripped.get('overall_assessment')
                         or stripped.get('reasoning')
                         or json.dumps(stripped, ensure_ascii=False))
            return {'narrative': narrative}, violated
        return stripped, violated

    def _safe_llm_call(
        self, prompt: str, purpose: str, tier: Optional[LLMPermissionTier] = None,
    ) -> Optional[Tuple[LLMCallRecord, Dict[str, Any]]]:
        if self.llm_provider is None:
            return None
        t = tier or self.llm_default_tier
        try:
            raw = self.llm_provider.generate(prompt, temperature=0.3, max_tokens=4096)
        except Exception as e:
            raw = f'[LLM Exception] {e}'
        prompt_hash = hashlib.sha256(prompt.encode('utf-8')).hexdigest()[:16]
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = raw
        stripped, violated = self._strip_llm_output(parsed, t)
        record = LLMCallRecord(
            permission_tier=t,
            purpose=purpose,
            prompt_hash=prompt_hash,
            response_excerpt=str(stripped)[:400],
            stripped=True,
            adjudicated=False,
            # 时间戳走注入时钟。默认 field(default_factory=time.time) 读墙钟，
            # 而 llm_calls 进报告，曾使「同 clock 的两次运行」产生不同链根。
            timestamp=self._clock if self._clock is not None else time.time(),
        )
        if violated:
            record.response_excerpt = '[VIOLATION STRIPPED] ' + record.response_excerpt[:380]
        return record, stripped

    # -------- 凭证域与 LLM 产物的分离 --------
    #
    # 问题（实测）：_safe_llm_call 的产物有两处**不确定**——
    #   ① 叙述文本本身（provider 以 temperature=0.3 调用）；
    #   ② LLMCallRecord.timestamp（原为 field(default_factory=time.time)，读墙钟）。
    # 而 report_hash 覆盖整个 report，二者都被算进 report_hash → 进链根，
    # 于是「同输入 + 同 nonce + 同 clock ⇒ 同链根」在启用 LLM 增强时失效，
    # 第三方无法跨机复算，凭证价值归零。
    #
    # 处理原则：**按确定性切分**，不按来源切分。
    #   · 凭证域（report_hash → 链根）：报告去掉**全部** LLM 产物后的部分。
    #     无条件剔除，不因开关而变——于是链根在「LLM 关闭 / 开启」两档下完全一致：
    #     LLM 增强是纯附加层，对凭证零影响（可实测的强性质）。
    #   · 叙述域（narrative_hash）：LLM 产物单独哈希，随报告并列留痕，改一字即可定位。
    # 两域不相交：narrative_hash 自身也不进凭证域（否则不确定性会绕回来）。

    @staticmethod
    def _llm_artifacts(report: Dict[str, Any]) -> Tuple[List[Any], Optional[Any]]:
        """取出报告里的 LLM 产物：(调用记录列表, 叙述)。未启用时为 ([], None)。"""
        calls = report.get('llm_calls') or []
        analysis = report.get('analysis')
        narrative = analysis.get('llm_narrative') if isinstance(analysis, dict) else None
        return calls, narrative

    def _credential_view(self, report: Dict[str, Any]) -> Dict[str, Any]:
        """链根的凭证视图：报告去掉**全部** LLM 产物后的部分，供 report_hash 使用。

        无条件剔除（不按「是否启用」分支），两个理由：
          ① 哈希域不随运行时状态而变——条件剔除会让「哪些键参与哈希」取决于开关；
          ② 使链根在「LLM 关闭 / 开启」两档下**完全一致**：LLM 增强是纯附加层，
             对凭证零影响。这条性质可用两次运行直接复核。
        剔除项：llm_calls（含时间戳与叙述摘要）、analysis.llm_narrative、
                narrative_hash（叙述域自身的哈希，不得绕回凭证域）。
        """
        view = dict(report)
        view.pop('llm_calls', None)
        view.pop('narrative_hash', None)
        analysis = view.get('analysis')
        if isinstance(analysis, dict):
            analysis = dict(analysis)
            analysis.pop('llm_narrative', None)
            view['analysis'] = analysis
        return view

    def _llm_artifacts_hash(self, report: Dict[str, Any]) -> str:
        """LLM 产物的独立哈希（叙述域）。无产物时返回空串，不写入报告。"""
        calls, narrative = self._llm_artifacts(report)
        if not calls and narrative is None:
            return ''
        return hashlib.sha256(
            json.dumps({'llm_calls': calls, 'llm_narrative': narrative},
                       sort_keys=True, ensure_ascii=False, default=str).encode('utf-8')
        ).hexdigest()[:16]

    # -------- 算子权限强制 --------

    def _enforce_plugin_tier(self, plugin: AuditPlugin, result: Any) -> Any:
        """在算子结果进入报告前强制其权限层，越权即降级。

        T3 发了 status   → 剥掉 status，记 _tier_violation
        T2 发了 BLOCKED  → 降级为 WARNING，记 _tier_violation
        T1 不受限

        这是护栏的**执行点**：CORE_OPERATOR_TIERS 只是声明，实际约束在这里。
        违规不会抛异常，只会被改写并在报告里留痕——
        报告要如实反映算子确实越权过，沉默地修正等于掩盖问题。
        """
        if not isinstance(result, dict):
            return result
        status = result.get('status')
        if plugin.tier == PluginTier.T3_NARRATIVE and status is not None:
            result = {k: v for k, v in result.items() if k != 'status'}
            result['_tier_violation'] = f"T3 plugin '{plugin.name}' emitted status={status}"
        elif plugin.tier == PluginTier.T2_SIGNAL and status in {'BLOCKED', 'CRITICAL'}:
            result['status'] = 'WARNING'
            result['_tier_violation'] = (
                f"T2 plugin '{plugin.name}' tried blocking status={status}, downgraded to WARNING"
            )
        return result

    # -------- 静态审计（八算子流水线）--------

    def audit(
        self,
        decision_context: Dict[str, Any],
        save_log: bool = False,
        log_dir: str = 'logs',
    ) -> Dict[str, Any]:
        """执行一次静态结构审计（十算子，单层拓扑）。

        decision_context 输入契约（上游语言键均为可选）
        -------------------------------------------------
          origin         str        原点事件（第一原点）—— ⊙GA 用它锚定链的起点
          goal           str        目标稳态 S*        —— 螺旋收敛方向
          resources      dict       能量/资源约束 ⦿，如
                                    {"compute": {"budget": 100, "committed": 40}}
                                    只做减法（budget − committed），不做预测

          narrative      str        别名 background / summary / description
          decision       str        别名 p / premise / action
          assumptions    list[str]  别名 premises / hypotheses
          outcome        str        别名 q / result / consequence
          branches       list[dict] 别名 branch_responses / failure_paths
                                    [{"assumption": "A1", "delta_d": "回滚"}]
          dependencies   dict       别名 dependency_graph / deps
                                    {"A1": ["A2"]}
          criteria       dict       {维度名: {"weight": w}}，权重和须为 1.0
          evidence       list[str]  支撑结论的证据标识
          conclusions    str        待审计的结论文本

          gray_levels    list[float] 灰度放量梯度，如 [0.01, 0.05, 0.25, 1.0]
          commit_ratio   float       当前放量比例
          feedback       dict        {假设: confirmed|falsified|unobserved}
                                     ⇄GRF 用它做现实对齐

          topology       dict        显式拓扑声明（可选）。不传则由 ⊞LFT 从
                                    decision/assumptions/branches/dependencies 投影。
                                    结构：{"nodes": [...], "edges": [{"src","dst",
                                    "relation","weight"}], "constraints": [...]}

          facts          list[dict]  二元事实校验对象（可选）。**不提供则由 BFC 原样放行**
                                    [{"id": "F1", "claim": "需求稳定",
                                      "evidence": ["doc#123"]}]
                                    也接受 list[str]（证据回落到 ctx['evidence']）
          observations   dict        {"F1": True}；真值只能由外部声明，BFC 永不推断
          verify_facts   bool        显式开闸（等价于提供了 facts）

        最小可用输入：{"decision": ..., "assumptions": [...], "outcome": ...}
        完整示例见 demo_audit.py 与 verify.py。各算子的别名表见对应分区头部注释。

        返回 report dict：
           operator_manifest     算子清单（顺序 / 权限层 / 来源），参与报告哈希
           origin_anchor         ⊙ 原点指纹与资源账本
           topology              ⊞ 拓扑指纹 / 四类并行校验 / 链内时序 / 纯拓扑图
           fact_check            BFC 二元裁定表与补齐条件
           meta_ledger           META 元因果账本（溯源缺口 / 并行收敛 / 叙事遮蔽A6 / 审计有界A10 / 因果承接）
           analysis              十算子结果
           implicit_assumptions  ⊕ 未声明预设
           vulnerability         ⊿ 崩塌等级与最脆弱变量
           responsibility_account 责任账户

        层间回传字段（由螺旋 / 极限收敛器注入，普通调用无需关心）
        ------------------------------------------------------------
           _spiral_state  dict 已跑层栈快照 —— META 用它把 A10 从「总条数」
                               换算成「每层增速」
           _limit_state   dict 上一层是否已抵达 S∞ = S* —— 并行收敛账本读它
        两者都是**既成事实的回传**，不是对下一层的预测；不注入即视为空。
        """
        # ---------- 第一阶段：三个静态算子先把 ctx 加工一遍 ----------
        # 顺序有依赖：⊕ 要写 _implicit_assumptions，⊿ 要读它，所以不能换。
        # 这一阶段只往 ctx 里塞 _开头的派生字段，原始输入一律不改动。
        ctx = self._strip_narrative(decision_context)
        ctx = self._surface_implicit_assumptions(ctx)
        ctx = self._assess_vulnerability(ctx)

        report: Dict[str, Any] = {
            'engine': ENGINE_NAME,
            'spe_version': SPE_VERSION,
            # 算子清单：参与 report_hash，使「这份报告由哪个算子集产生」可自证。
            'operator_manifest': self.operator_manifest(),
            # 版本谱系：这份链根属于第几代引擎。它进报告 → 进报告哈希 → 进链根，
            # 于是「谁在什么算子集与什么代际下产出了这个根」不再需要旁证。
            'lineage': self.evolution_lineage(),
            'disclaimer': self.config.get('disclaimer', ''),
            'responsibility_account': asdict(self.account),
            'analysis': {},
            'custom_fields': self.config.get('custom_fields', {}),
            'narrative_meta': ctx.get('_narrative_stripped', {}),
            'implicit_assumptions': ctx.get('_implicit_assumptions', {}),
            'vulnerability': ctx.get('_vulnerability', {}),
            'llm_calls': [],
        }

        if not self.account.is_closed:
            report['analysis']['RESPONSIBILITY_CLOSURE'] = {
                'status': 'BLOCKED',
                'reason': 'RESPONSIBILITY_NOT_CLOSED',
                'message': f'责任未闭环：stage={self.account.stage} 缺少具体责任人(owner)',
            }

        run_ctx = dict(ctx)
        run_ctx['_responsibility_account'] = asdict(self.account)
        run_ctx['_clock'] = self._clock
        prior: Dict[str, Any] = {}
        run_ctx['_prior_audit_results'] = prior
        # 阈值走配置而不是散落在算子里的常数：同一份输入在不同地方
        # 必须算出同一个 A6 / A10，否则账本就没有可比性。
        run_ctx['_config'] = self.config
        # 极限收敛器的状态回传位：由 spiral / limit_reconstruct / spiral_step
        # 注入，供 META 读取「是否已抵达 S∞ = S*」。不注入即为空，不猜。
        if '_limit_state' not in run_ctx:
            run_ctx['_limit_state'] = {}

        # 算子执行顺序由 _ordered_plugins() 唯一定义（PIPELINE_ORDER + 插件缝插入位）：
        # ACC 排最后，因为它要汇总前面所有算子（读 _prior_audit_results）。
        # 与 operator_manifest() 共用同一个定序点，两者不可能不一致。
        ordered = self._ordered_plugins()
        for plugin in ordered:
            try:
                result = plugin.analyze_func(run_ctx)
            except Exception as e:
                # 算子抛异常**不算通过**，一律记 BLOCKED。
                # 理由：审计失败和审计通过同样不能被当成「没问题」。
                result = {'status': 'BLOCKED', 'reason': 'PLUGIN_EXCEPTION', 'message': str(e)}
            result = self._enforce_plugin_tier(plugin, result)
            report['analysis'][plugin.name] = result
            prior[plugin.name] = result

        # ---------- 抽出三个便于上层直接消费的视图（⊙原点 / ⊞拓扑 / BFC事实） ----------
        ori = report['analysis'].get('GA')
        if isinstance(ori, dict):
            report['origin_anchor'] = {
                'origin_hash': ori.get('origin_hash', ''),
                'origin': ori.get('origin'),
                'goal': ori.get('goal'),
                'status': ori.get('status'),
                'resource_ledger': ori.get('resource_ledger', []),
            }

        tpg = report['analysis'].get('LFT')
        if isinstance(tpg, dict):
            report['topology'] = {
                'graph_hash': tpg.get('graph_hash', ''),
                'node_count': tpg.get('node_count', 0),
                'edge_count': tpg.get('edge_count', 0),
                'source': tpg.get('source'),
                'validation': tpg.get('validation', {}),
                'relative_labels': tpg.get('relative_labels', {}),
                # 公理 5：链内时序 + 观测位置（本次审计站在哪条链上）
                'time_order': tpg.get('time_order', {}),
                'graph': tpg.get('topology', {}),
            }

        bfc = report['analysis'].get('BFC')
        if isinstance(bfc, dict):
            report['fact_check'] = {
                'status': bfc.get('status'),
                'mode': bfc.get('mode'),
                'reason': bfc.get('reason'),
                'facts_checked': bfc.get('facts_checked', 0),
                'true_count': bfc.get('true_count', 0),
                'false_count': bfc.get('false_count', 0),
                'undeclared_count': bfc.get('undeclared_count', 0),
                'verdicts': bfc.get('verdicts', []),
                'remediation': bfc.get('remediation', []),
            }

        # 元因果账本视图：五条元基各自的状态与度量，供上层直接消费。
        # 注意它**不参与**任何阻断判定（META 是 T2，结构上不允许阻断）。
        meta = report['analysis'].get('META')
        if isinstance(meta, dict):
            report['meta_ledger'] = {
                'status': meta.get('status'),
                'reason': meta.get('reason'),
                'bases': meta.get('meta_bases', {}),
                'high_risk_bases': meta.get('high_risk_bases', []),
                'warning_bases': meta.get('warning_bases', []),
            }

        if self.llm_provider is not None:
            res = self._safe_llm_call(
                prompt=(
                    '你是认知审计专家（仅T3叙述权限，不得输出status/converged/weight/rank/verdict等裁决字段）。'
                    '请对以下决策上下文做语义级风险与偏见叙述性说明，以JSON返回，仅包含 narrative 字段。\n\n'
                    f'决策上下文：{json.dumps(decision_context, ensure_ascii=False, default=str)}'
                ),
                purpose='STATIC_AUDIT',
                tier=LLMPermissionTier.T3_NARRATIVE,
            )
            if res is not None:
                record, stripped = res
                report['analysis']['llm_narrative'] = stripped
                report['llm_calls'].append(asdict(record))

        # LLM 产物出叙述域：单独哈希并列留痕（无产物时返回空串，不写入报告）。
        narrative_hash = self._llm_artifacts_hash(report)
        if narrative_hash:
            report['narrative_hash'] = narrative_hash

        # 事件里只放**派生摘要**（报告哈希、脆弱性、是否有阻断、拓扑指纹），
        # 不放完整报告，也不放原始决策数据——链上不落敏感数据。
        event_payload: Dict[str, Any] = {
            # report_hash 走**凭证视图**：链根只覆盖确定性部分，
            # 不受 LLM 叙述与其调用记录影响（理由见 _credential_view）。
            'report_hash': hashlib.sha256(
                json.dumps(self._credential_view(report), sort_keys=True,
                           ensure_ascii=False, default=str).encode('utf-8')
            ).hexdigest()[:16],
            'operator_set_hash': self.operator_set_hash(),
            'lineage_hash': self.evolution_lineage()['lineage_hash'],
            'vulnerability': report['vulnerability'],
            'origin_hash': report.get('origin_anchor', {}).get('origin_hash', ''),
            'graph_hash': report.get('topology', {}).get('graph_hash', ''),
            'has_blocking': any(
                isinstance(r, dict) and r.get('status') in ConvergenceChecker.BLOCKING_STATUSES
                for r in report['analysis'].values()
            ),
        }
        # 注意：narrative_hash **不进事件 payload**（故不进链）。
        # 链是线性的，任何进 payload 的值都会进链根；一旦把叙述哈希上链，
        # 链根就会随叙述内容变化（叙述由 temperature=0.3 的模型产生），
        # 可复现性当场失效——这正是本次要修的病。
        # 代价是叙述不与链绑定，属刻意取舍：叙述是「可读层」，不是「可证层」；
        # narrative_hash 的职能是**报告内自校验 + 稳定指代**，不承担链绑定。
        self._append_event('AUDIT', event_payload)

        if save_log:
            report['log_path'] = self._write_log(report, log_dir)
        return report

    def _write_log(self, report: Dict[str, Any], log_dir: str) -> str:
        # 落盘三件事，缺一不可：
        #   audit_id         人类可读的审计编号（nonce + 时间戳）
        #   chain_root_hash  链根指纹——**这是唯一的对外校验凭据**
        #   完整 report      派生结论，不含原始决策数据
        # 注意：日志文件必须与报告分开保存。若校验凭据和被校验对象放在一起，
        # 任何人都能同时改掉两者，验证就失去意义了。
        os.makedirs(log_dir, exist_ok=True)
        audit_id = f'SPE-{self.account.nonce}-{int(self._clock if self._clock is not None else time.time())}'
        report['chain_root_hash'] = self.chain_root_hash
        report['audit_id'] = audit_id
        path = os.path.join(log_dir, f'{audit_id}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        return os.path.abspath(path)

    # -------- 算子 ⊛：因果重构（线性有界，v2.0 兼容路径）--------

    def reconstruct(
        self,
        decision_context: Dict[str, Any],
        delta_vars: Optional[Dict[str, Any]] = None,
        max_rounds: int = 5,
        human_approved_deltas: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """⊛ 因果重构（线性版）：bounded + human gate + 五状态形式化收敛。

        语义：
            - 首轮：若提供 delta_vars（视为已声明起始修正），应用；否则不自动修正。
            - 之后每轮只接受 human_approved_deltas 中的修正（由外部审批流提交）。
            - 每轮 audit 后由 ConvergenceChecker 分类；只要不是 DIVERGED 就停止。
            - human gate：每轮结束返回 awaiting_human=True，调用方显式推进。
              本方法一次性跑完所有已批准的 delta 序列（同步、有界）；不做自循环。

        与 spiral() 的分工：本方法是**线性**的，每轮 ctx.update() 覆盖上一层，
        不做冻结、不检测漂移，只回答「这组修正能把风险压到不动点吗」。
        需要「层叠加 + 原点不漂移」时用 spiral()。

        返回：
            session_root_hash / final_state / rounds / is_true_convergence / final_report
        """
        if max_rounds < 1:
            raise ValueError('max_rounds must be >= 1')

        rounds: List[Dict[str, Any]] = []
        current_ctx = copy.deepcopy(decision_context)
        approved = list(human_approved_deltas or [])
        if delta_vars:
            approved.insert(0, delta_vars)

        previous_risks: frozenset = frozenset()
        state = ConvergenceState.DIVERGED
        final_report: Dict[str, Any] = {}

        for idx in range(max_rounds + 1):  # +1 允许初始轮（无 delta）
            if idx < len(approved):
                d = approved[idx]
                if not isinstance(d, dict) or not d:
                    state = ConvergenceState.BLOCKED
                    rounds.append({
                        'round': idx,
                        'status': state.value,
                        'reason': 'EMPTY_OR_INVALID_DELTA',
                    })
                    break
                current_ctx.update(d)
                self._append_event('DELTA_APPLIED', {'round': idx, 'delta_keys': sorted(d.keys())})
            elif idx > 0:
                # 没有更多已批准 delta，但仍未收敛 → 停在 AWAITING_HUMAN
                state = ConvergenceState.DIVERGED
                rounds.append({
                    'round': idx,
                    'status': state.value,
                    'awaiting_human': True,
                    'reason': 'NO_MORE_APPROVED_DELTAS',
                })
                break

            report = self.audit(current_ctx)
            final_report = report
            current_risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
            has_unresolved = bool(report.get('implicit_assumptions', {}).get('missing_required'))

            state = ConvergenceChecker.classify(
                round_idx=idx,
                max_rounds=max_rounds,
                previous_risks=previous_risks,
                current_risks=current_risks,
                has_blocking=has_blocking,
                has_unresolved_assumptions=has_unresolved,
            )

            round_hash = hashlib.sha256(
                json.dumps({'idx': idx, 'state': state.value, 'risks': sorted(map(str, current_risks))},
                           sort_keys=True).encode('utf-8')
            ).hexdigest()[:16]

            rounds.append({
                'round': idx,
                'status': state.value,
                'risk_count': len(current_risks),
                'has_blocking': has_blocking,
                'round_hash': round_hash,
                'report_ref': report.get('audit_id'),
            })

            self._append_event('RECONSTRUCT_ROUND', {
                'round': idx,
                'state': state.value,
                'risk_count': len(current_risks),
                'round_hash': round_hash,
            })

            if state != ConvergenceState.DIVERGED:
                break
            previous_risks = current_risks

        awaiting_human = (state == ConvergenceState.DIVERGED and len(rounds) <= max_rounds
                          and rounds[-1].get('reason') == 'NO_MORE_APPROVED_DELTAS')

        return {
            'engine': ENGINE_NAME,
            'spe_version': SPE_VERSION,
            'final_state': state.value,
            'is_true_convergence': state.is_true_convergence,
            'awaiting_human': awaiting_human,
            'rounds': rounds,
            'final_report': final_report,
            'session_root_hash': self.chain_root_hash,
            'total_rounds': len(rounds),
        }

    # -------- 算子 ↻：叠加螺旋式迭代思考链路 --------

    @staticmethod
    def _neighbourhood(topo: Dict[str, Any]) -> Dict[str, set]:
        """把拓扑压成 1-邻域表：{节点: {(方向, 邻居, 关系)}}。"""
        table: Dict[str, set] = {}
        for edge in (topo or {}).get('edges', []) or []:
            if not isinstance(edge, dict):
                continue
            src, dst = str(edge.get('src', '')), str(edge.get('dst', ''))
            rel = str(edge.get('relation', 'causal'))
            if not src or not dst:
                continue
            table.setdefault(src, set()).add(('out', dst, rel))
            table.setdefault(dst, set()).add(('in', src, rel))
        return table

    @classmethod
    def _stable_nodes(cls, previous: Optional[Dict[str, Any]],
                      current: Dict[str, Any]) -> List[str]:
        """已收敛节点 = 相邻两层 1-邻域完全一致的节点。

        这是「收敛」在拓扑层唯一的可判定定义：节点本身没名字、没属性，
        能收敛的只有它的连接关系。邻域一致即结构不动点，可冻结。
        """
        if not previous:
            return []
        prev_table = cls._neighbourhood(previous)
        curr_table = cls._neighbourhood(current)
        return sorted(
            n for n, nb in curr_table.items()
            if nb and prev_table.get(n) == nb
        )

    def spiral(
        self,
        decision_context: Dict[str, Any],
        approved_deltas: Optional[List[Dict[str, Any]]] = None,
        max_loops: int = 8,
        energy_budget: Optional[float] = None,
        loop_cost: float = 1.0,
    ) -> Dict[str, Any]:
        """↻ 叠加螺旋式迭代链路（p♾️q）。

        与 reconstruct() 的三处根本差别：
            1. 叠加而非覆盖：每层拓扑完整保留；1-邻域连续两层一致的节点被冻结，
               冻结集合只增不减。已冻结节点若在后续层消失 → SUPERPOSITION_VIOLATION。
            2. 原点不漂移：每层读取 ⊙GA 的 origin_hash；一旦与首层锚点不符
               → ORIGIN_DRIFT 立即停机。绕圈绕到目标变了，是本方法最致命的失效模式。
            3. 能量守恒：每层消耗 loop_cost；energy_budget 不足即停。
               拓扑无边界，但预算有硬顶——没有硬顶的「无限」是失控。

        approved_deltas 与 reconstruct() 同义：外部审批流逐层提交的结构性修正。

        返回：
            verdict        SpiralVerdict，回答「这圈螺旋为什么停下」
            final_state    ConvergenceState，回答「结构收敛了吗」
            layers         每层快照（含拓扑、半径、冻结集合、层哈希）
            spiral         SpiralStack 全账（含层间差分、半径趋势、能量账本）
        """
        # 注：SpiralStack 内联于本文件「分区④」，无需外部导入。

        if max_loops < 1:
            raise ValueError('max_loops must be >= 1')

        stack = SpiralStack(energy_budget=energy_budget, loop_cost=loop_cost)
        loops: List[Dict[str, Any]] = []

        current_ctx = copy.deepcopy(decision_context)
        approved = list(approved_deltas or [])

        previous_risks: frozenset = frozenset()
        previous_topo: Optional[Dict[str, Any]] = None
        state = ConvergenceState.DIVERGED
        verdict = SpiralVerdict.AWAITING_HUMAN
        final_report: Dict[str, Any] = {}
        origin_drift = False

        for idx in range(max_loops + 1):
            if idx > 0 and not stack.can_run():
                verdict = SpiralVerdict.BUDGET_EXHAUSTED
                loops.append({
                    'loop': idx, 'state': state.value,
                    'verdict': verdict.value,
                    'reason': 'ENERGY_BUDGET_EXHAUSTED',
                    'energy_left': stack.energy_left,
                })
                break

            if idx < len(approved):
                delta = approved[idx]
                if not isinstance(delta, dict) or not delta:
                    verdict = SpiralVerdict.BLOCKED
                    loops.append({
                        'loop': idx, 'state': ConvergenceState.BLOCKED.value,
                        'verdict': verdict.value,
                        'reason': 'EMPTY_OR_INVALID_DELTA',
                    })
                    break
                current_ctx.update(delta)
                self._append_event('DELTA_APPLIED', {
                    'loop': idx, 'delta_keys': sorted(delta.keys()),
                })
            elif idx > 0:
                verdict = SpiralVerdict.AWAITING_HUMAN
                loops.append({
                    'loop': idx, 'state': state.value,
                    'verdict': verdict.value,
                    'awaiting_human': True,
                    'reason': 'NO_MORE_APPROVED_DELTAS',
                })
                break

            # 把「已跑了几层」回传给 META：A10 审计熵增是每层留痕条数，
            # 没有层数就只剩「总条数」，也就无从谈「增速」。
            loop_ctx = dict(current_ctx)
            loop_ctx['_spiral_state'] = stack.to_dict()
            report = self.audit(loop_ctx)
            final_report = report
            current_risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
            has_unresolved = bool(report.get('implicit_assumptions', {}).get('missing_required'))

            state = ConvergenceChecker.classify(
                round_idx=idx,
                max_rounds=max_loops,
                previous_risks=previous_risks,
                current_risks=current_risks,
                has_blocking=has_blocking,
                has_unresolved_assumptions=has_unresolved,
            )

            topo = report.get('topology', {}).get('graph', {}) or {}
            graph_hash = report.get('topology', {}).get('graph_hash', '')
            origin_hash = report.get('origin_anchor', {}).get('origin_hash', '')

            origin_drift = stack.origin_drift(origin_hash)
            converged_nodes = self._stable_nodes(previous_topo, topo)

            layer = stack.push(
                state=state.value,
                origin_hash=origin_hash,
                risk_set=current_risks,
                graph_hash=graph_hash,
                topology=topo,
                converged_nodes=converged_nodes,
                index=idx,
                unresolved=has_unresolved,
            )

            loops.append({
                'loop': idx,
                'state': state.value,
                'risk_count': layer.radius,
                'has_blocking': has_blocking,
                'origin_hash': origin_hash,
                'origin_drift': origin_drift,
                'graph_hash': graph_hash,
                'layer_hash': layer.layer_hash,
                'newly_frozen': sorted(converged_nodes),
                'energy_left': layer.energy_left,
            })

            self._append_event('SPIRAL_LOOP', {
                'loop': idx,
                'state': state.value,
                'risk_count': layer.radius,
                'origin_hash': origin_hash,
                'origin_drift': origin_drift,
                'graph_hash': graph_hash,
                'layer_hash': layer.layer_hash,
            })

            if origin_drift:
                verdict = SpiralVerdict.ORIGIN_DRIFT
                self._append_event('ORIGIN_DRIFT', {
                    'loop': idx,
                    'anchor': stack.origin_anchor,
                    'current': origin_hash,
                })
                break

            if any(v['severity'] == 'HALT' for v in stack.violations):
                verdict = SpiralVerdict.SUPERPOSITION_VIOLATION
                break

            if state != ConvergenceState.DIVERGED:
                if state.is_true_convergence:
                    verdict = SpiralVerdict.CONVERGED
                elif state == ConvergenceState.BLOCKED:
                    verdict = SpiralVerdict.BLOCKED
                else:
                    verdict = SpiralVerdict.BUDGET_EXHAUSTED
                break

            # 画地为牢：半径连续三层纹丝不动。此前 check_flat() 算了却从未接入停机，
            # 结果会被 BUDGET_EXHAUSTED 冒充（"跑完了但没跑到"），掩盖"在原地打转"这个真相。
            if stack.is_static():
                verdict = SpiralVerdict.FLAT_SPIRAL
                break

            previous_risks = current_risks
            previous_topo = topo

        return {
            'engine': ENGINE_NAME,
            'spe_version': SPE_VERSION,
            'verdict': verdict.value,
            'final_state': state.value,
            'is_true_convergence': state.is_true_convergence,
            'origin_drift': origin_drift,
            'origin_anchor': stack.origin_anchor,
            'awaiting_human': verdict == SpiralVerdict.AWAITING_HUMAN,
            'loops': loops,
            'total_loops': len(loops),
            'spiral': stack.to_dict(),
            'final_report': final_report,
            'session_root_hash': self.chain_root_hash,
        }

    # -------- 算子 ∞：无限因果重构（极限收敛器） --------

    def limit_reconstruct(
        self,
        decision_context: Dict[str, Any],
        approved_deltas: Optional[List[Dict[str, Any]]] = None,
        energy_budget: Optional[float] = None,
        loop_cost: float = 1.0,
        max_loops: Optional[int] = None,
        plateau_layers: int = 2,
        limit_layers: int = 2,
    ) -> Dict[str, Any]:
        """∞ 无限因果重构（极限收敛器）：层数不设上限，只按语义判据停机。

        与 spiral() 的三处差别
        ----------------------
        1. **层数不设上限**。max_loops=None 时无限跑，唯一的算术硬顶是螺旋预算。
           硬闸门：energy_budget 与 max_loops 至少要给一个，否则直接拒绝 ——
           没有能量约束的「无限」不是无限，是失控（因果承接：能量动态守恒）。
        2. **判据驱动停机**（三类新判据）：
               LIMIT_REACHED  距离连续 limit_layers 层为 (0,0) → 抵达 S∞ = S*
               FLAT_SPIRAL    半径连续三层纹丝不动 → 画地为牢
               NOT_MONOTONE   距离连续 plateau_layers+1 层不严格下降 → 不再逼近
        3. **不在首次收敛处立刻停**。真极限要求「保持」而非「碰到」：收敛之后再走
           几层仍然收敛，才算抵达极限；若某层离开了极限，就是回到了发散，
           归入 NOT_MONOTONE。

        距离 distance = (风险集规模, 是否有未决假设)，字典序比较 ——
        纯结构量，不含任何权重估计，因此可跨进程复算。

        引擎**永不自己生成修正**：deltas 用尽即 AWAITING_HUMAN，把控制权交回外部。
        要继续请用 spiral_step() 逐层推进 —— 这正是「无限」的驱动力必须来自外部。
        """
        if energy_budget is None and max_loops is None:
            raise ValueError(
                '无限重构必须至少给一个硬顶：energy_budget 或 max_loops。'
                '没有硬顶的「无限」不是无限，是失控。'
            )
        if limit_layers < 2:
            raise ValueError('limit_layers must be >= 2（极限要求「保持」，不是「碰到」）')
        if plateau_layers < 1:
            raise ValueError('plateau_layers must be >= 1')

        ceiling = max_loops if max_loops is not None else 10 ** 9
        stack = SpiralStack(energy_budget=energy_budget, loop_cost=loop_cost)
        loops: List[Dict[str, Any]] = []

        current_ctx = copy.deepcopy(decision_context)
        approved = list(approved_deltas or [])

        previous_risks: frozenset = frozenset()
        previous_topo: Optional[Dict[str, Any]] = None
        state = ConvergenceState.DIVERGED
        verdict = SpiralVerdict.AWAITING_HUMAN
        final_report: Dict[str, Any] = {}
        origin_drift = False
        # 上一层是否已抵达 S∞ = S* —— 只回传既成事实，不预测下一层。
        last_limit: Dict[str, Any] = {'limit_reached': False}
        idx = 0

        while True:
            if max_loops is not None and idx >= max_loops:
                verdict = SpiralVerdict.BUDGET_EXHAUSTED
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value,
                              'reason': 'MAX_LOOPS_SAFETY_VALVE'})
                break

            if idx > 0 and not stack.can_run():
                verdict = SpiralVerdict.BUDGET_EXHAUSTED
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value,
                              'reason': 'ENERGY_BUDGET_EXHAUSTED',
                              'energy_left': stack.energy_left})
                break

            if idx < len(approved):
                delta = approved[idx]
                if not isinstance(delta, dict) or not delta:
                    verdict = SpiralVerdict.BLOCKED
                    loops.append({'loop': idx,
                                  'state': ConvergenceState.BLOCKED.value,
                                  'verdict': verdict.value,
                                  'reason': 'EMPTY_OR_INVALID_DELTA'})
                    break
                current_ctx.update(delta)
                self._append_event('DELTA_APPLIED',
                                   {'loop': idx, 'delta_keys': sorted(delta.keys())})
            elif idx > 0:
                # 引擎绝不自己生成修正 —— delta 用尽即交回外部
                verdict = SpiralVerdict.AWAITING_HUMAN
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value, 'awaiting_human': True,
                              'reason': 'NO_MORE_APPROVED_DELTAS'})
                break

            report = self.audit(current_ctx)
            final_report = report
            current_risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
            has_unresolved = bool(report.get('implicit_assumptions', {}).get('missing_required'))

            state = ConvergenceChecker.classify(
                round_idx=idx,
                max_rounds=ceiling,
                previous_risks=previous_risks,
                current_risks=current_risks,
                has_blocking=has_blocking,
                has_unresolved_assumptions=has_unresolved,
            )

            topo = report.get('topology', {}).get('graph', {}) or {}
            graph_hash = report.get('topology', {}).get('graph_hash', '')
            origin_hash = report.get('origin_anchor', {}).get('origin_hash', '')

            origin_drift = stack.origin_drift(origin_hash)
            converged_nodes = self._stable_nodes(previous_topo, topo)

            layer = stack.push(
                state=state.value, origin_hash=origin_hash,
                risk_set=current_risks, graph_hash=graph_hash, topology=topo,
                converged_nodes=converged_nodes, index=idx,
                unresolved=has_unresolved,
            )

            loops.append({
                'loop': idx, 'state': state.value,
                'distance': list(layer.distance), 'radius': layer.radius,
                'has_blocking': has_blocking, 'origin_hash': origin_hash,
                'origin_drift': origin_drift, 'graph_hash': graph_hash,
                'layer_hash': layer.layer_hash,
                'newly_frozen': sorted(converged_nodes),
                'energy_left': layer.energy_left,
            })

            self._append_event('LIMIT_LOOP', {
                'loop': idx, 'state': state.value,
                'distance': list(layer.distance),
                'origin_hash': origin_hash, 'graph_hash': graph_hash,
                'layer_hash': layer.layer_hash,
            })

            if origin_drift:
                verdict = SpiralVerdict.ORIGIN_DRIFT
                self._append_event('ORIGIN_DRIFT', {
                    'loop': idx, 'anchor': stack.origin_anchor, 'current': origin_hash,
                })
                break
            if any(v['severity'] == 'HALT' for v in stack.violations):
                verdict = SpiralVerdict.SUPERPOSITION_VIOLATION
                break
            if state == ConvergenceState.BLOCKED:
                verdict = SpiralVerdict.BLOCKED
                break
            if stack.limit_reached(limit_layers):
                verdict = SpiralVerdict.LIMIT_REACHED
                break
            if stack.is_static():
                verdict = SpiralVerdict.FLAT_SPIRAL
                break
            if stack.is_plateau(plateau_layers + 1):
                verdict = SpiralVerdict.NOT_MONOTONE
                break

            previous_risks = current_risks
            previous_topo = topo
            idx += 1

        return {
            'engine': ENGINE_NAME,
            'spe_version': SPE_VERSION,
            'verdict': verdict.value,
            'final_state': state.value,
            'is_true_convergence': state.is_true_convergence,
            'origin_drift': origin_drift,
            'origin_anchor': stack.origin_anchor,
            'awaiting_human': verdict == SpiralVerdict.AWAITING_HUMAN,
            'loops': loops,
            'total_loops': len(loops),
            # 注意区分：is_true_convergence 说的是「结构收敛了吗」（含 FIXED_POINT，
            # 风险有界但不为零）；is_limit 说的才是「是否抵达极限 S∞ = S*」（距离归零并保持）。
            'is_limit': stack.limit_reached(limit_layers),
            'distance_trend': [list(d) for d in stack.distance_trend()],
            'spiral': stack.to_dict(),
            'spiral_state': stack.to_dict(),      # 可直接喂回 spiral_step(state=...)
            'final_report': final_report,
            'session_root_hash': self.chain_root_hash,
        }

    def spiral_step(
        self,
        decision_context: Dict[str, Any],
        delta: Optional[Dict[str, Any]] = None,
        state: Optional[Dict[str, Any]] = None,
        plateau_layers: int = 2,
        limit_layers: int = 2,
    ) -> Dict[str, Any]:
        """↻ 单层推进：外部驱动无限迭代的入口。

        与 limit_reconstruct 的分工：
            limit_reconstruct  一口气跑完（层数无上限，判据停机）
            spiral_step        只跑一层，跑完即把控制权交回外部（人 / 上层 agent）

        把两者串起来才是合规意义上的「无限因果重构」：**引擎负责算与判定，
        外部负责决定下一层的修正**。引擎永不自己生成 delta —— 那是建议生成，
        越权。所以「无限」的驱动力必须来自外部：这是设计，不是限制。

        state 传上一次返回的 `spiral_state` 即可续跑；不传则开新栈。
        单层推进不需要能量硬顶（只跑一层），但 state 里已有的预算会继续计账。

        verdict == ADVANCED 表示这一层跑完且仍可继续；其余取值即该层触发的终局判据。
        跨层收敛比较用「风险指纹字符串」而非内部元组，因此续跑与连跑结论一致。
        """
        stack = SpiralStack.from_dict(state) if state else SpiralStack()

        current_ctx = copy.deepcopy(decision_context)
        if delta is not None:
            if not isinstance(delta, dict) or not delta:
                return {'verdict': SpiralVerdict.BLOCKED.value,
                        'reason': 'EMPTY_OR_INVALID_DELTA',
                        'spiral_state': stack.to_dict()}
            current_ctx.update(delta)
            self._append_event('DELTA_APPLIED',
                               {'loop': len(stack.layers), 'delta_keys': sorted(delta.keys())})

        idx = len(stack.layers)
        prev_topo = stack.layers[-1].topology if stack.layers else None
        prev_risks = (frozenset(stack.layers[-1].risk_set) if stack.layers else frozenset())

        step_ctx = dict(current_ctx)
        step_ctx['_spiral_state'] = stack.to_dict()
        report = self.audit(step_ctx)
        current_risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
        current_keys = frozenset(str(r) for r in current_risks)
        has_unresolved = bool(report.get('implicit_assumptions', {}).get('missing_required'))

        state_obj = ConvergenceChecker.classify(
            round_idx=idx,
            max_rounds=10 ** 9,
            previous_risks=prev_risks,
            current_risks=current_keys,
            has_blocking=has_blocking,
            has_unresolved_assumptions=has_unresolved,
        )

        topo = report.get('topology', {}).get('graph', {}) or {}
        graph_hash = report.get('topology', {}).get('graph_hash', '')
        origin_hash = report.get('origin_anchor', {}).get('origin_hash', '')

        origin_drift = stack.origin_drift(origin_hash)
        converged_nodes = self._stable_nodes(prev_topo, topo)

        layer = stack.push(
            state=state_obj.value, origin_hash=origin_hash,
            risk_set=current_risks, graph_hash=graph_hash, topology=topo,
            converged_nodes=converged_nodes, index=idx,
            unresolved=has_unresolved,
        )

        self._append_event('SPIRAL_STEP', {
            'loop': idx, 'state': state_obj.value,
            'distance': list(layer.distance),
            'origin_hash': origin_hash, 'graph_hash': graph_hash,
            'layer_hash': layer.layer_hash,
        })

        verdict = SpiralVerdict.ADVANCED
        if origin_drift:
            verdict = SpiralVerdict.ORIGIN_DRIFT
        elif any(v['severity'] == 'HALT' for v in stack.violations):
            verdict = SpiralVerdict.SUPERPOSITION_VIOLATION
        elif state_obj == ConvergenceState.BLOCKED:
            verdict = SpiralVerdict.BLOCKED
        elif stack.limit_reached(limit_layers):
            verdict = SpiralVerdict.LIMIT_REACHED
        elif stack.is_static():
            verdict = SpiralVerdict.FLAT_SPIRAL
        elif stack.is_plateau(plateau_layers + 1):
            verdict = SpiralVerdict.NOT_MONOTONE

        return {
            'engine': ENGINE_NAME,
            'spe_version': SPE_VERSION,
            'verdict': verdict.value,
            'can_continue': verdict == SpiralVerdict.ADVANCED,
            'final_state': state_obj.value,
            'is_true_convergence': state_obj.is_true_convergence,
            'origin_drift': origin_drift,
            'layer': layer.to_dict(),
            'layer_count': len(stack.layers),
            'distance_trend': [list(d) for d in stack.distance_trend()],
            'spiral_state': stack.to_dict(),
            'final_report': report,
            'session_root_hash': self.chain_root_hash,
        }

    # -------- 算子 ⊛∞：自主进化层（版本谱系 · 只提案不适用） --------

    # 缺口 → 结构改进方向的映射。注意方向是**引擎自身的输入契约**，
    # 不是对用户决策的建议 —— 引擎永远 decision-agnostic。
    EVOLUTION_HINTS: Dict[str, str] = {
        'GA': '把原点 / 目标稳态 / 资源三项从「运行时检查」前移为输入契约必填',
        'NS': '把该叙事遮蔽模式纳入 A6 阈值的显式声明，而不是事后统计',
        'IAP': '把该隐含假设纳入 assumptions 必填清单',
        'LCH': '把该薄弱点纳入 branches 覆盖度校验（每条假设都必须有 ΔD）',
        'LFT': '把该拓扑违规升级为 .tpg 语法层的编译期拦截',
        'BFC': '把该证据缺口前移为事实声明阶段的必填校验',
        'CCS': '把该因果缺口前移为假设声明阶段的必填校验',
        'GRF': '把该现实反馈缺口前移为灰度放量的前置条件',
        'META': '把该元基账本的阈值纳入 config，使口径可显式声明',
        'ACC': '把该裁定出口的缺失条件前移为输入契约必填',
    }
    EVOLUTION_HINT_DEFAULT = '把该结构缺口前移为输入契约的显式校验项'

    def evolution_lineage(self) -> Dict[str, Any]:
        """版本谱系：这份链根属于第几代引擎。

        自主进化与可复现性之所以能共存，全靠这一个对象：
        进化改了算子集 → operator_set_hash 变 → lineage_hash 变 → 证书随之变；
        而**旧代际的链根仍然可以被旧代际的算子集复算出来**，因为代际是显式声明的，
        不是靠「记得当时是什么样」推断的。
        """
        lineage: Dict[str, Any] = {
            'generation': len(self._evolution_approvals),
            'spe_version': SPE_VERSION,
            'topology_version': TOPOLOGY_VERSION,
            # 文法版本单列：底座结构没变、但语法增补（时序 t / 元因果账本字段）
            # 也必须可追溯，否则跨代际比对会误判成「结构变了」。
            'grammar_version': TOPOLOGY_GRAMMAR_VERSION,
            'operator_set_hash': self.operator_set_hash(),
            'pipeline_order': list(self.PIPELINE_ORDER),
            'operator_count': len(self.operator_manifest()),
            'approved_proposals': [p.get('id') for p in self._evolution_approvals],
        }
        lineage['lineage_hash'] = hashlib.sha256(
            json.dumps(lineage, sort_keys=True, ensure_ascii=False).encode('utf-8')
        ).hexdigest()[:16]
        return lineage

    def evolve(
        self,
        decision_context: Dict[str, Any],
        approved_deltas: Optional[List[Dict[str, Any]]] = None,
        max_loops: int = 8,
        energy_budget: Optional[float] = None,
        loop_cost: float = 1.0,
        gap_threshold: int = 1,
        proposal_limit: int = 8,
    ) -> Dict[str, Any]:
        """⊛∞ 自主进化层：引擎自己发现结构缺口，但**永不自己改写判定规则**。

        规范里的同名接口
        ----------------
        规范第六节（IR 层）已经把这层写死了：
            evolve(g, delta) -> Graph            运行期演化入口
            g = rewrite(g, best_rule(g))         图重写（DPO 语义）
            「每次重写必须保持 Constraint 可满足」  ← 门控
            停机：CSP 最小不动点 g_{n+1} == g_n   ← 图同构判定
            A10 审计熵增 ≈ version 的单调递增速率，**有界**才收敛于 S*
        本方法是它们在内核里的落地 —— 但**刻意少了「自动 apply」那一步**。

        为什么引擎不许自己 apply
        ------------------------
        自主 apply 会同时摧毁三样东西：
            1. 可复现性   同输入 + 同 nonce + 同 clock 必须同链根（V2 / V9 的断言）；
            2. 证书证据力 第三方要能拿同一份代码复算出同一个根；
            3. 不自驱纪律 引擎永不自己生成修正（与 limit_reconstruct 同一原则）。
        所以本方法的产出是**候选清单**，不是新规则。三条恒等式写死在返回值里：
            candidate.applies_automatically 恒 False
            candidate.requires_human        恒 True
            auto_applied                    恒 0
        人工裁决走 approve_evolution_proposal()：它只**记账**（升代际），
        不改代码 —— 改代码必须由人做，返回里明写 applied_to_code=False。

        候选口径（纯计数，零学习、零权重、零 LLM）
        -------------------------------------------
        每一层审计里，凡是 status 不属于 {PASS, SKIPPED} 的算子，或元因果账本里
        不是 PASS 的元基，都记一次出现；**出现次数 ≥ gap_threshold** 的缺口
        才成为候选。「反复出现」是唯一的入选标准 —— 一次性的异常不是结构缺口。
        """
        if gap_threshold < 1:
            raise ValueError('gap_threshold must be >= 1')
        if max_loops < 1:
            raise ValueError('max_loops must be >= 1')

        stack = SpiralStack(energy_budget=energy_budget, loop_cost=loop_cost)
        current_ctx = copy.deepcopy(decision_context)
        approved = list(approved_deltas or [])

        tally: Dict[str, Dict[str, Any]] = {}
        provenance_per_layer: List[int] = []
        layer_hashes: List[str] = []
        loops: List[Dict[str, Any]] = []
        previous_risks: frozenset = frozenset()
        previous_topo: Optional[Dict[str, Any]] = None
        state = ConvergenceState.DIVERGED
        verdict = SpiralVerdict.AWAITING_HUMAN
        final_report: Dict[str, Any] = {}
        origin_drift = False
        fixed_round: Optional[int] = None
        fixed_hash = ''

        for idx in range(max_loops + 1):
            if idx > 0 and not stack.can_run():
                verdict = SpiralVerdict.BUDGET_EXHAUSTED
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value,
                              'reason': 'ENERGY_BUDGET_EXHAUSTED',
                              'energy_left': stack.energy_left})
                break

            if idx < len(approved):
                delta = approved[idx]
                if not isinstance(delta, dict) or not delta:
                    verdict = SpiralVerdict.BLOCKED
                    loops.append({'loop': idx, 'state': ConvergenceState.BLOCKED.value,
                                  'verdict': verdict.value,
                                  'reason': 'EMPTY_OR_INVALID_DELTA'})
                    break
                current_ctx.update(delta)
                self._append_event('DELTA_APPLIED',
                                   {'loop': idx, 'delta_keys': sorted(delta.keys())})
            elif idx > 0:
                verdict = SpiralVerdict.AWAITING_HUMAN
                loops.append({'loop': idx, 'state': state.value,
                              'verdict': verdict.value, 'awaiting_human': True,
                              'reason': 'NO_MORE_APPROVED_DELTAS'})
                break

            loop_ctx = dict(current_ctx)
            loop_ctx['_spiral_state'] = stack.to_dict()
            report = self.audit(loop_ctx)
            final_report = report
            analysis = report.get('analysis', {}) or {}

            # ── 缺口登记：本层所有非 PASS 的结构信号 ──
            def _note(code: str, operator: str, status: str, layer: int) -> None:
                entry = tally.setdefault(code, {
                    'code': code, 'operator': operator,
                    'observed_status': status, 'occurrences': 0, 'evidence_layers': [],
                })
                entry['occurrences'] += 1
                entry['evidence_layers'].append(layer)

            for op in sorted(analysis):
                # META 的缺口由下面按元基逐条登记（粒度更细、口径更准）。
                # 这里再登记一次它的汇总状态，同一个缺口就会在候选清单里出现两遍，
                # 「反复出现」这个唯一入选标准就被同一条证据人为地刷高了。
                if op == 'META':
                    continue
                res = analysis.get(op)
                if not isinstance(res, dict):
                    continue
                st = res.get('status')
                if st is None or st in ('PASS', 'SKIPPED'):
                    continue
                _note(f"{op}:{res.get('reason', st)}", op, str(st), idx)

            meta = analysis.get('META')
            if isinstance(meta, dict):
                for base, body in sorted((meta.get('meta_bases') or {}).items()):
                    if isinstance(body, dict) and body.get('status') != 'PASS':
                        _note(f"META.{base}:{body.get('reason')}", 'META',
                              str(body.get('status')), idx)

            topo = report.get('topology', {}).get('graph', {}) or {}
            graph_hash = report.get('topology', {}).get('graph_hash', '')
            origin_hash = report.get('origin_anchor', {}).get('origin_hash', '')
            previous_topo_for_this = previous_topo

            # ── 最小不动点：g_{n+1} == g_n（图同构判定）──
            if layer_hashes and graph_hash and graph_hash == layer_hashes[-1]:
                if fixed_round is None:
                    fixed_round, fixed_hash = idx, graph_hash
            layer_hashes.append(graph_hash)
            provenance_per_layer.append(len(topo.get('provenance', []) or []))

            current_risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
            has_unresolved = bool(report.get('implicit_assumptions', {}).get('missing_required'))
            state = ConvergenceChecker.classify(
                round_idx=idx, max_rounds=max_loops,
                previous_risks=previous_risks, current_risks=current_risks,
                has_blocking=has_blocking,
                has_unresolved_assumptions=has_unresolved,
            )

            origin_drift = stack.origin_drift(origin_hash)
            converged_nodes = self._stable_nodes(previous_topo_for_this, topo)
            layer = stack.push(
                state=state.value, origin_hash=origin_hash,
                risk_set=current_risks, graph_hash=graph_hash, topology=topo,
                converged_nodes=converged_nodes, index=idx, unresolved=has_unresolved,
            )

            loops.append({
                'loop': idx, 'state': state.value, 'risk_count': layer.radius,
                'graph_hash': graph_hash, 'layer_hash': layer.layer_hash,
                'newly_frozen': sorted(converged_nodes),
                'provenance_entries': provenance_per_layer[-1],
                'energy_left': layer.energy_left,
            })

            if origin_drift:
                verdict = SpiralVerdict.ORIGIN_DRIFT
                break
            if any(v['severity'] == 'HALT' for v in stack.violations):
                verdict = SpiralVerdict.SUPERPOSITION_VIOLATION
                break
            if state != ConvergenceState.DIVERGED:
                if state.is_true_convergence:
                    verdict = SpiralVerdict.CONVERGED
                elif state == ConvergenceState.BLOCKED:
                    verdict = SpiralVerdict.BLOCKED
                else:
                    verdict = SpiralVerdict.BUDGET_EXHAUSTED
                break
            if stack.is_static():
                verdict = SpiralVerdict.FLAT_SPIRAL
                break

            previous_risks = current_risks
            previous_topo = topo

        # ── A10 审计熵增：每层留痕条数（version 递增速率的离散版）──
        layers_n = max(1, len(provenance_per_layer))
        a10 = round(sum(provenance_per_layer) / layers_n, 6) if provenance_per_layer else 0.0
        ceiling = MetaCausalLedgerPlugin._ceiling(
            {'_config': self.config}, 'audit_entropy_ceiling',
            MetaCausalLedgerPlugin.DEFAULT_AUDIT_ENTROPY_CEILING)
        bounded = a10 <= ceiling
        monotone = all(b >= a for a, b in zip(provenance_per_layer,
                                              provenance_per_layer[1:]))

        # ── 候选清单：反复出现的缺口才入选 ──
        proposals: List[Dict[str, Any]] = []
        for code in sorted(tally):
            entry = tally[code]
            if entry['occurrences'] < gap_threshold:
                continue
            proposals.append({
                'id': 'EVO-' + hashlib.sha256(code.encode('utf-8')).hexdigest()[:8],
                'code': code,
                'operator': entry['operator'],
                'observed_status': entry['observed_status'],
                'occurrences': entry['occurrences'],
                'evidence_layers': entry['evidence_layers'],
                'proposed_change': self.EVOLUTION_HINTS.get(
                    entry['operator'], self.EVOLUTION_HINT_DEFAULT),
                'status': 'PROPOSED',
                # 三条恒等式：候选永远不会自己生效。
                'applies_automatically': False,
                'requires_human': True,
            })
        proposals = proposals[:proposal_limit]

        lineage = self.evolution_lineage()
        self._append_event('EVOLUTION_SCAN', {
            'proposals': len(proposals),
            'auto_applied': 0,
            'lineage_hash': lineage['lineage_hash'],
            'a10': a10,
            'bounded': bounded,
            'fixed_point_round': fixed_round,
        })

        return {
            'engine': ENGINE_NAME,
            'spe_version': SPE_VERSION,
            'verdict': verdict.value,
            'final_state': state.value,
            'is_true_convergence': state.is_true_convergence,
            'origin_drift': origin_drift,
            'lineage': lineage,
            'audit_entropy': {
                'a10': a10,
                'per_layer': provenance_per_layer,
                'version_monotone': monotone,
                'ceiling': ceiling,
                'bounded': bounded,
                'doctrine': '审计有界：A10 有界，使演化收敛于 S*',
            },
            'fixed_point': {
                'found': fixed_round is not None,
                'round': fixed_round,
                'graph_hash': fixed_hash,
                'criterion': 'g_{n+1} == g_n（图同构判定）',
            },
            'proposals': proposals,
            'proposal_count': len(proposals),
            'gap_threshold': gap_threshold,
            # 三条恒等式的对外断言：任何一次 evolve 都必须满足。
            'auto_applied': 0,
            'requires_human': True,
            'loops': loops,
            'total_loops': len(loops),
            'spiral': stack.to_dict(),
            'final_report': final_report,
            'session_root_hash': self.chain_root_hash,
        }

    def approve_evolution_proposal(
        self,
        proposal: Dict[str, Any],
        approved_by: str,
    ) -> Dict[str, Any]:
        """人工裁决进化候选：**只记账，不改代码**。

        这是「只提案，人工 apply」的落点。它做两件事、且只做两件事：
            1. 把批准记录进事件链（署名的、可复核的）；
            2. 让版本谱系升一代 —— 此后新产生的链根都带这个代际号。

        它**不做**的事，恰恰是最重要的一件：不去改引擎的判定规则。
        原因不是技术上做不到，而是做法本身会毁掉证书：
        引擎一旦能改自己的判定标准，第三方就再也无法「拿同一份代码复算出同一个根」，
        这样产出的证书只是一张自签名的纸。
        """
        pid = str((proposal or {}).get('id', '')).strip()
        if not pid:
            raise ValueError('缺少候选 id：无法记账')
        signer = str(approved_by or '').strip()
        if not signer:
            raise ValueError('人工裁决必须署名：approved_by 不能为空')

        record = {
            'id': pid,
            'code': str(proposal.get('code', '')),
            'approved_by': signer,
            'generation': len(self._evolution_approvals),
        }
        self._evolution_approvals.append(record)
        self._append_event('EVOLUTION_APPROVED', record)
        return {
            'approved': record,
            'lineage': self.evolution_lineage(),
            # 引擎升了代际，但没有改自己的判定规则。
            'applied_to_code': False,
            'requires_code_change': True,
            'note': '引擎永不自动改写判定规则；本记录只声明「人已批准该结构变更」。'
                    '实际改代码必须由人完成，完成后须重算金标并升 SPE_VERSION。'
        }

    # -------- 会话推进（human gate） --------

    def advance_with_human_delta(
        self,
        previous_result: Dict[str, Any],
        decision_context: Dict[str, Any],
        human_delta: Dict[str, Any],
    ) -> Dict[str, Any]:
        """在之前的 reconstruct 结果上由人工提交一个新 delta，再跑一轮。

        便捷入口：把历史 delta 重放到当前上下文、追加 human_delta，再跑一轮 audit 判定。
        需要层叠加语义时改用 spiral()。
        """
        current_ctx = copy.deepcopy(decision_context)
        current_ctx.update(human_delta)
        report = self.audit(current_ctx)
        risks, has_blocking = ConvergenceChecker.extract_risk_set(report)
        has_unresolved = bool(report.get('implicit_assumptions', {}).get('missing_required'))
        state = ConvergenceChecker.classify(
            round_idx=len(self.event_chain),
            max_rounds=len(self.event_chain) + 10,
            previous_risks=frozenset(),
            current_risks=risks,
            has_blocking=has_blocking,
            has_unresolved_assumptions=has_unresolved,
        )
        self._append_event('HUMAN_ADVANCE', {
            'delta_keys': sorted(human_delta.keys()),
            'state': state.value,
        })
        return {
            'final_state': state.value,
            'is_true_convergence': state.is_true_convergence,
            'final_report': report,
            'session_root_hash': self.chain_root_hash,
        }

    # -------- 审计链验证 --------

    def verify_chain(self) -> Dict[str, Any]:
        """独立验证哈希链的链接完整性与内容封存状态。

        校验三类破坏：
          1. 链接破坏 —— prev_hash 与前序链根不符               -> LINK_BROKEN
          2. 内容篡改 —— hash 重算值与封存值 sealed_hash 不符   -> CONTENT_TAMPERED
             覆盖 payload / event_type / timestamp / nonce 的事后改动
          3. 未经封存 —— sealed_hash 为 None                   -> EVENT_NOT_SEALED

        返回 {valid, last_valid_idx, total, root_hash}。
        """
        prev = 'ROOT'
        last_valid = -1
        for i, ev in enumerate(self.event_chain):
            if ev.prev_hash != prev:
                return {'valid': False, 'last_valid_idx': last_valid,
                        'total': len(self.event_chain), 'broken_at': i,
                        'reason': 'LINK_BROKEN',
                        'root_hash': self.chain_root_hash}
            if ev.sealed_hash is None:
                return {'valid': False, 'last_valid_idx': last_valid,
                        'total': len(self.event_chain), 'broken_at': i,
                        'reason': 'EVENT_NOT_SEALED',
                        'root_hash': self.chain_root_hash}
            blob = json.dumps({
                'event_type': ev.event_type,
                'payload': ev.payload,
                'prev_hash': ev.prev_hash,
                'timestamp': ev.timestamp,
                'nonce': ev.nonce,
            }, sort_keys=True, ensure_ascii=False, default=str)
            actual = hashlib.sha256(blob.encode('utf-8')).hexdigest()
            if actual != ev.sealed_hash:
                return {'valid': False, 'last_valid_idx': last_valid,
                        'total': len(self.event_chain), 'broken_at': i,
                        'reason': 'CONTENT_TAMPERED',
                        'root_hash': self.chain_root_hash}
            prev = ev.sealed_hash
            last_valid = i
        return {'valid': True, 'last_valid_idx': last_valid,
                'total': len(self.event_chain), 'root_hash': self.chain_root_hash}


# v2.0 名称保留为别名：既有调用方无需改动即可迁移到 SPE 1.0
CognitiveAuditEngine = SecondPerspectiveEngine




# ============================================================================
# 分区⑤ 视图层 — 双语报告渲染器 / Bilingual Report Renderer
# ============================================================================
# REPORT — Bilingual Report Renderer (可选)
# ==========================================
#
# 把 CognitiveAuditEngine.audit() 产出的结构化报告，渲染为一个**可选语言**
# 的中文/英文外壳视图。
#
# 设计原则（与引擎定位保持一致）：
#   - 零依赖、确定性、无 LLM 调用，纯词条映射。
#   - 「外壳」双语：报告标题、算子名、裁定级别、证书字段、责任账户标签。
#   - 「证据正文」保原文：logical_core / checks / violations 等分析内容是
#     动态拼接的证据级文本，不做翻译，避免失真与破坏可签名验证语义。
#   - 渲染器不修改原始报告，也不参与十算子管线；作为视图层供上层调用。
#
# 用法：
#     # 渲染器已内联于本文件「分区⑤」，与引擎同处一个模块，直接实例化即可。
#     renderer = ReportRenderer()
#     zh_view = renderer.render(report, lang="zh")   # 中文外壳
#     en_view = renderer.render(report, lang="en")   # 英文外壳
# ----------------------------------------------------------------------------

class ReportRenderer:
    """可选双语外壳渲染器：把审计报告本地化外壳、保留证据正文。"""

    # ── 词条表：{key: (zh, en)} ──
    TITLE = "认知审计报告", "Cognitive Audit Report"

    OPERATORS = {
        "GA":       ("⊙ 第一原点锚定",  "⊙ Genesis Anchor"),
        "NS":        ("⊗ 叙事剥离",      "⊗ Narrative Strip"),
        "IAP":       ("⊕ 隐假设透视",    "⊕ Implicit Assumption"),
        "LCH":       ("⊿ 脆弱性定位",    "⊿ Fragility Localization"),
        "LFT":       ("⊞ 无标签拓扑图", "⊞ Label-Free Topology"),
        "BFC":       ("二元事实校验",    "Binary Fact Check"),
        "CCS":       ("链闭合扫描",      "Chain Closure Scan"),
        "GRF":       ("⇄ 灰度执行与现实反馈", "⇄ Gray Feedback"),
        "ACC":     ("⊚ 责任锚定",      "⊚ Accountability Anchor"),
        "llm_enhanced": ("LLM 增强分析", "LLM-Enhanced Analysis"),
    }

    VERDICT_LEVELS = {
        "AUDIT_HALT": ("审计阻断", "AUDIT HALT"),
        "AUDIT_WARN": ("审计警告", "AUDIT WARN"),
        "AUDIT_PASS": ("审计通过", "AUDIT PASS"),
    }

    FIELDS = {
        "title":                ("报告", "Report"),
        "disclaimer":           ("免责声明", "Disclaimer"),
        "responsibility_account": ("责任账户", "Responsibility Account"),
        "organization":         ("组织", "Organization"),
        "role":                 ("角色", "Role"),
        "stage":                ("阶段", "Stage"),
        "nonce":                ("防重放随机串", "Nonce"),
        "is_vague":             ("组织模糊", "Vague Org"),
        "anchor_status":        ("锚定状态", "Anchor Status"),
        "warning":              ("警告", "Warning"),
        "custom_fields":        ("自定义字段", "Custom Fields"),
        "operators":            ("审计算子", "Audit Operators"),
        "verdict":              ("最终裁定", "Final Verdict"),
        "level":                ("级别", "Level"),
        "summary":              ("摘要", "Summary"),
        "halt_count":           ("致命违规数", "Halt Count"),
        "warn_count":           ("警告数", "Warn Count"),
        "halt_items":           ("致命违规明细", "Halt Items"),
        "warn_items":           ("警告明细", "Warn Items"),
        "certificate":          ("审计证书", "Audit Certificate"),
        "audit_id":             ("审计 ID", "Audit ID"),
        "timestamp":            ("时间戳", "Timestamp"),
        "signature":            ("签名哈希", "Signature"),
        "algorithm":            ("签名算法", "Algorithm"),
        "verifiable":           ("可验证", "Verifiable"),
        "note":                 ("说明", "Note"),
        "responsibility":       ("责任锚定", "Responsibility"),
    }

    @staticmethod
    def _t(table: Dict[str, Any], key: str, lang: str) -> str:
        """按语言取词条：未收录的 key 原样返回。"""
        entry = table.get(key)
        if not entry:
            return key
        return entry[0] if lang == "zh" else entry[1]

    def _localize_status(self, level: str, lang: str) -> str:
        """裁定级别：中文外壳给中文名，英文外壳保留枚举（机器可读）。"""
        return self._t(self.VERDICT_LEVELS, level, lang) or level

    def render(self, report: Dict[str, Any], lang: str = "zh") -> Dict[str, Any]:
        """
        把审计报告渲染为指定语言的外壳视图。

        Args:
            report: engine.audit() 的返回（含 responsibility_account / analysis / ...）。
            lang:   "zh" 或 "en"，默认中文。
        Returns:
            本地化外壳的字典：顶层标题/免责声明/责任账户/裁定/证书/各算子
            （证据正文字段按原样保留）。
        """
        if lang not in ("zh", "en"):
            lang = "zh"

        analysis = report.get("analysis", {})
        state = analysis.get("ACC", {}) if isinstance(analysis, dict) else {}

        # 责任账户：仅本地化已收录的显示标签，未收录字段保留原样
        ra = report.get("responsibility_account", {})
        responsibility_view = {
            self._t(self.FIELDS, k, lang): v for k, v in ra.items()
        }

        # 各算子：核心标题本地化，分析正文透传
        operators_view = {}
        for name, result in analysis.items():
            label = self._t(self.OPERATORS, name, lang)
            if isinstance(result, dict):
                operators_view[name] = {
                    "label": label,
                    "result": result,
                }
            else:
                operators_view[name] = {"label": label, "result": result}

        # 裁定与证书：从 ACC 抽出做外壳本地化（值保持机器可读）
        verdict_view = None
        certificate_view = None
        if isinstance(state, dict):
            verdict = state.get("verdict") or {}
            if isinstance(verdict, dict):
                verdict_view = {
                    self._t(self.FIELDS, "level", lang): self._localize_status(
                        verdict.get("level", ""), lang),
                    self._t(self.FIELDS, "summary", lang): verdict.get("summary", ""),
                    self._t(self.FIELDS, "halt_count", lang): verdict.get("halt_count", 0),
                    self._t(self.FIELDS, "warn_count", lang): verdict.get("warn_count", 0),
                    self._t(self.FIELDS, "halt_items", lang): verdict.get("halt_items", []),
                    self._t(self.FIELDS, "warn_items", lang): verdict.get("warn_items", []),
                }
            cert = state.get("certificate") or {}
            if isinstance(cert, dict):
                certificate_view = {
                    self._t(self.FIELDS, "audit_id", lang): cert.get("audit_id", ""),
                    self._t(self.FIELDS, "timestamp", lang): cert.get("timestamp", ""),
                    self._t(self.FIELDS, "signature", lang): cert.get("signature", ""),
                    self._t(self.FIELDS, "algorithm", lang): cert.get("algorithm", ""),
                    self._t(self.FIELDS, "verifiable", lang): cert.get("verifiable", ""),
                    self._t(self.FIELDS, "note", lang): cert.get("note", ""),
                }

        return {
            "title": self.TITLE[0 if lang == "zh" else 1],
            self._t(self.FIELDS, "disclaimer", lang): report.get("disclaimer", ""),
            self._t(self.FIELDS, "responsibility_account", lang): responsibility_view,
            self._t(self.FIELDS, "verdict", lang): verdict_view,
            self._t(self.FIELDS, "certificate", lang): certificate_view,
            self._t(self.FIELDS, "operators", lang): operators_view,
            self._t(self.FIELDS, "custom_fields", lang): report.get("custom_fields", {}),
            "_meta": {
                "lang": lang,
                "generated_at": int(time.time()),
            },
        }

    def render_text(self, report: Dict[str, Any], lang: str = "zh") -> str:
        """渲染为便于人工阅读的纯文本（保留原文正文）。"""
        view = self.render(report, lang)
        lines: List[str] = []
        lines.append(view["title"])
        lines.append("=" * 40)

        dis = view.get(self._t(self.FIELDS, "disclaimer", lang))
        if dis:
            lines.append(f"{self._t(self.FIELDS, 'disclaimer', lang)}: {dis}")

        ra = view.get(self._t(self.FIELDS, "responsibility_account", lang))
        if isinstance(ra, dict):
            header = self._t(self.FIELDS, "responsibility_account", lang)
            lines.append(f"\n{header}")
            for k, v in ra.items():
                lines.append(f"  {k}: {v}")

        vd = view.get(self._t(self.FIELDS, "verdict", lang))
        if isinstance(vd, dict):
            lines.append(f"\n{self._t(self.FIELDS, 'verdict', lang)}")
            for k, v in vd.items():
                lines.append(f"  {k}: {v}")

        cert = view.get(self._t(self.FIELDS, "certificate", lang))
        if isinstance(cert, dict):
            lines.append(f"\n{self._t(self.FIELDS, 'certificate', lang)}")
            for k, v in cert.items():
                lines.append(f"  {k}: {v}")

        ops = view.get(self._t(self.FIELDS, "operators", lang))
        if isinstance(ops, dict):
            lines.append(f"\n{self._t(self.FIELDS, 'operators', lang)}")
            for name, item in ops.items():
                lines.append(f"  {item['label']} ({name})")
                result = item.get("result")
                if isinstance(result, dict):
                    # 证据正文原样透传：logical_core / checks / violations 等
                    for k, v in result.items():
                        if isinstance(v, (dict, list)):
                            lines.append(f"    {k}: {v}")
                        else:
                            lines.append(f"    {k}: {v}")

        return "\n".join(lines)

# ============================================================================
# 分区⑤ 视图层 — 人话渲染器 / Plain-Language Renderer
# ============================================================================
# PLAIN — Plain-Language Audit Renderer (可选)
# ============================================
#
# 把 SecondPerspectiveEngine.audit() 产出的结构化审计报告，翻译成「人话」：
# 用日常语言重述裁定级别、脆弱环节、暗含假设、因果链校验与责任锚定，
# 而不改动原始报告、不参与十算子管线、不触碰 SHA-256 证书与收敛判定。
#
# 已知覆盖缺口（2026.2 新增四项算子）：本渲染器的词条表尚未覆盖
# ⊙GA 原点锚定 / ⊞LFT 拓扑校验 / BFC 二元事实校验 / ⇄GRF 现实反馈的
# 人话视图 —— 它们在报告中仍以机器可读字段原样透传，未失真，只是未被翻译。
#
# 设计原则（与引擎定位保持一致）：
#   - 零依赖、确定性、无 LLM 调用，纯词条映射（术语「一句话人话」取自 GLOSSARY.md）。
#   - 机器可读字段（level 枚举 / audit_id / signature / algorithm）原样保留，
#     仅在其旁附「人话」解释，便于人工阅读又不破坏可验证语义。
#   - 渲染器不修改原始 report，也不注册进 CORE_OPERATORS；
#     作为审计后处理（视图层）供上层调用，与 ReportRenderer 同级、同文件。
#
# 用法：
#     # 渲染器已内联于本文件「分区⑤」，直接实例化即可。
#     renderer = PlainLanguageRenderer()
#     plain_view = renderer.humanize(report, lang="zh")      # 结构化「人话」视图
#     plain_text = renderer.humanize_text(report, lang="zh") # 一段纯文本人话总结
# ----------------------------------------------------------------------------

class PlainLanguageRenderer:
    """可选「人话」渲染器：把结构化审计报告转成日常语言，不改证据链。"""

    # ── 词条表：{key: (zh, en)} ──
    VERDICT = {
        "AUDIT_HALT": ("审计阻断：这条决策有关键依据硬伤，先别拍板",
                       "Audit HALT: a fatal flaw was found — do not sign off yet"),
        "AUDIT_WARN": ("审计警告：有几处隐患，建议先补再走",
                       "Audit WARN: some risks to fix before you proceed"),
        "AUDIT_PASS": ("审计通过：结构上没看出硬伤",
                       "Audit PASS: no structural flaw was found"),
    }

    COLLAPSE = {
        "HIGH": ("高：这个假设一旦不成立，会出大乱子",
                 "High: if this assumption fails, big trouble"),
        "MEDIUM": ("中：会有明显影响，但不至于崩",
                   "Medium: noticeable impact, not fatal"),
        "LOW": ("低：影响有限",
                "Low: limited impact"),
    }

    # IAP / 内隐假设 标志 → 人话（引擎级 type 与 IAP 插件 flag_type 共用一套键）
    IAP_FLAG = {
        "MISSING_CRITERIA": ("给了备选方案，却没说按什么标准来选",
                             "Alternatives given, but no selection criteria stated"),
        "WEIGHTS_NOT_NORMALIZED": ("打分权重加起来不等于 100%，口径不一致",
                                   "Weights do not sum to 100% — inconsistent scale"),
        "CONCLUSION_WITHOUT_EVIDENCE": ("下了结论，却拿不出证据",
                                        "A conclusion was drawn with no evidence"),
        "self_referential": ("把“本机构认为…”当论据，等于没论证",
                             "Uses its own authority as proof — circular by posture"),
        "privilege_bypass": ("话里想绕过审批/审核，这是高危信号",
                             "Tries to bypass review/approval — high-risk signal"),
        "unilateral_premise": ("只说了一边的前提，漏了关键条件",
                               "States only one side's premise, omits key conditions"),
        "circular_justification": ("循环论证：把结论当前提，等于啥也没说",
                                   "Circular: conclusion used as premise"),
        "missing_assumptions": ("做了决定却没列任何前提假设，属单边前提",
                                "A decision with no stated assumptions — one-sided"),
    }

    RESPONSIBILITY_REASON = {
        "RESPONSIBILITY_NOT_CLOSED": ("还没人签字负责，这条审计结论没法落地",
                                      "No named owner yet — this verdict cannot be acted on"),
    }

    SEVERITY = {
        "HALT": ("致命", "Fatal"),
        "WARN": ("警告", "Warning"),
        "PASS": ("通过", "Pass"),
        "SKIP": ("跳过", "Skipped"),
    }

    CCS_CHECK = {
        "inverse": ("逆反校验（前提不成立时有没有退路）",
                    "Inverse check (is there a fallback if the premise fails)"),
        "counterfactual": ("反事实校验（前提不成立时结果会怎样）",
                           "Counterfactual check (what happens to the outcome if premise fails)"),
        "chain_integrity": ("因果链完整性（P→A→Q 是否连贯）",
                           "Causal-chain integrity (is P→A→Q connected)"),
        "blackhole": ("信息黑洞检测（关键变量 P/A/Q 是否齐全）",
                     "Black-hole check (are key variables P/A/Q all present)"),
    }

    CCS_RESULT = {
        "SYSTEM_COLLAPSE": ("系统会无退路地崩", "system collapses with no fallback"),
        "CONVERGE": ("有退路，能收敛", "converges with a fallback"),
        "PARTIAL_RECOVERY": ("只有部分退路", "partial recovery only"),
        "COLLAPSE_RISK": ("退路不够，有崩的风险", "insufficient fallback — collapse risk"),
        "SKIP": ("信息不足，跳过", "skipped — insufficient input"),
        "COVERED": ("已考虑到非P情形", "counterfactual scenario covered"),
        "UNCOVERED": ("没考虑非P情形", "counterfactual scenario not covered"),
        "BROKEN_AT_ROOT": ("因果链起点缺失", "chain root missing"),
        "BROKEN": ("因果链断裂", "chain broken"),
        "COMPLETE": ("因果链完整", "chain complete"),
        "MISSING_Q": ("缺结果(Q)", "missing outcome (Q)"),
        "MISSING_A": ("缺前提(A)", "missing assumption (A)"),
        "CLEAR": ("无信息黑洞", "no black hole"),
        "BLACKHOLE": ("出现信息黑洞", "black hole present"),
    }

    # ===================== 工具 =====================

    @staticmethod
    def _t(table: Dict[str, Tuple[str, str]], key: str, lang: str) -> str:
        """按语言取词条：未收录的 key 原样返回。"""
        entry = table.get(key)
        if not entry:
            return key
        return entry[0] if lang == "zh" else entry[1]

    @staticmethod
    def _verdict(report: Dict[str, Any]) -> Dict[str, Any]:
        return report.get("analysis", {}).get("ACC", {}).get("verdict") or {}

    @staticmethod
    def _vulnerability(report: Dict[str, Any]) -> Dict[str, Any]:
        return report.get("vulnerability", {}) or {}

    @classmethod
    def _iap_flags(cls, report: Dict[str, Any]) -> List[Tuple[str, str]]:
        """收集暗含假设标志（统一 type / flag_type 两种键来源）。"""
        flags: List[Tuple[str, str]] = []
        for f in report.get("implicit_assumptions", {}).get("flags", []) or []:
            ft = f.get("type") or f.get("flag_type")
            if ft:
                flags.append((ft, f.get("description", "")))
        for f in report.get("analysis", {}).get("IAP", {}).get("flags", []) or []:
            ft = f.get("flag_type") or f.get("type")
            if ft:
                flags.append((ft, f.get("description", "")))
        return flags

    @classmethod
    def _ccs_checks(cls, report: Dict[str, Any]) -> List[Dict[str, Any]]:
        return report.get("analysis", {}).get("CCS", {}).get("checks", []) or []

    @classmethod
    def _responsibility(cls, report: Dict[str, Any]) -> Tuple[Dict[str, Any], Any]:
        state = report.get("analysis", {}).get("ACC", {})
        resp = state.get("responsibility") or {}
        closure = report.get("analysis", {}).get("RESPONSIBILITY_CLOSURE")
        return resp, closure

    # ===================== 对外接口 =====================

    def humanize(self, report: Dict[str, Any], lang: str = "zh") -> Dict[str, Any]:
        """把审计报告渲染为「人话」结构化视图（不改动原始 report）。"""
        if lang not in ("zh", "en"):
            lang = "zh"

        verdict = self._verdict(report)
        level = verdict.get("level", "")
        vuln = self._vulnerability(report)
        iap_flags = self._iap_flags(report)
        ccs_checks = self._ccs_checks(report)
        resp, closure = self._responsibility(report)

        # ── 责任 ──
        anchor_status = resp.get("anchor_status", "")
        resp_plain = {
            "组织": resp.get("organization", "UNKNOWN"),
            "角色": resp.get("role", ""),
            "阶段": resp.get("stage", ""),
            "锚定状态_原文": anchor_status,
            "锚定状态_人话": ("已锚定到具体节点" if anchor_status == "ANCHORED"
                             else "未锚定 — 责任主体模糊，须追溯到具体自然人"),
            "模糊警告_人话": (resp.get("warning") or "") if resp.get("is_vague") else "",
        }
        if isinstance(closure, dict):
            reason = closure.get("reason", "")
            if reason:
                resp_plain["闭环状态_人话"] = self._t(self.RESPONSIBILITY_REASON, reason, lang)
            else:
                resp_plain["闭环状态_人话"] = (
                    "责任已闭环" if closure.get("status") != "BLOCKED" else "责任未闭环"
                )

        # ── 暗含假设 ──
        if iap_flags:
            iap_plain = [
                self._t(self.IAP_FLAG, ft, lang) + (f"：{desc}" if desc else "")
                for ft, desc in iap_flags
            ]
        else:
            iap_plain = (["（没翻出明显的暗含假设）"]
                         if lang == "zh" else ["(no obvious implicit assumption surfaced)"])

        # ── 因果链校验 ──
        ccs_plain = []
        for c in ccs_checks:
            label = self._t(self.CCS_CHECK, c.get("check", ""), lang)
            sev = self._t(self.SEVERITY, c.get("severity", ""), lang)
            res = self._t(self.CCS_RESULT, c.get("result", ""), lang)
            ccs_plain.append(f"[{sev}] {label} — {res}")

        # ── 证书（机器可读原样保留，便于复验）──
        cert = report.get("analysis", {}).get("ACC", {}).get("certificate") or {}

        return {
            "结论_人话": (self._t(self.VERDICT, level, lang)
                         if level else "（未运行五算子，无法生成结论）"),
            "裁定级别_原文": level,
            "裁定摘要_原文": verdict.get("summary", ""),
            "责任_人话": resp_plain,
            "最脆弱环节_人话": {
                "崩塌等级_原文": vuln.get("collapse_level", ""),
                "崩塌等级_人话": self._t(self.COLLAPSE, vuln.get("collapse_level", ""), lang),
                "最薄弱变量": vuln.get("weakest_variable") or "",
                "原因": vuln.get("reasons", []),
            },
            "暗含假设_人话": iap_plain,
            "因果链校验_人话": ccs_plain,
            "证书_原文": {
                "audit_id": cert.get("audit_id", ""),
                "signature": cert.get("signature", ""),
                "algorithm": cert.get("algorithm", ""),
                "verifiable": cert.get("verifiable", ""),
            },
            "_meta": {"lang": lang},
        }

    def humanize_text(self, report: Dict[str, Any], lang: str = "zh") -> str:
        """渲染为一段便于人工阅读的纯文本「人话」总结。"""
        view = self.humanize(report, lang)
        r = view["责任_人话"]
        w = view["最脆弱环节_人话"]
        c = view["证书_原文"]

        if lang == "zh":
            lines = ["【一句话结论】", "  " + view["结论_人话"],
                     "\n【谁在审 / 责任】",
                     f"  组织：{r['组织']} · 角色：{r['角色']} · 阶段：{r['阶段']}",
                     f"  责任状态：{r['锚定状态_人话']}"]
            if r.get("模糊警告_人话"):
                lines.append(f"  ⚠ {r['模糊警告_人话']}")
            if r.get("闭环状态_人话"):
                lines.append(f"  {r['闭环状态_人话']}")
            lines += ["\n【最脆弱的一环】", f"  {w['崩塌等级_人话']}"]
            if w.get("最薄弱变量"):
                lines.append(f"  最薄弱：{w['最薄弱变量']}")
            for reason in w.get("原因", []):
                lines.append(f"  · {reason}")
            lines.append("\n【藏在话里的假设】")
            for item in view["暗含假设_人话"]:
                lines.append(f"  - {item}")
            lines.append("\n【因果链与反事实】")
            for item in view["因果链校验_人话"]:
                lines.append(f"  - {item}")
            lines += ["\n【证书】",
                      f"  审计编号 {c['audit_id']} · 算法 {c['algorithm']} · 可验证：{c['verifiable']}"]
            return "\n".join(lines)

        # English
        lines = ["[Bottom line]", "  " + view["结论_人话"],
                 "\n[Who audits / Responsibility]",
                 f"  Org: {r['组织']} · Role: {r['角色']} · Stage: {r['阶段']}",
                 f"  Anchor status: {r['锚定状态_人话']}"]
        if r.get("模糊警告_人话"):
            lines.append(f"  ! {r['模糊警告_人话']}")
        if r.get("闭环状态_人话"):
            lines.append(f"  {r['闭环状态_人话']}")
        lines += ["\n[Weakest link]", f"  {w['崩塌等级_人话']}"]
        if w.get("最薄弱变量"):
            lines.append(f"  Weakest: {w['最薄弱变量']}")
        for reason in w.get("原因", []):
            lines.append(f"  - {reason}")
        lines.append("\n[Hidden assumptions]")
        for item in view["暗含假设_人话"]:
            lines.append(f"  - {item}")
        lines.append("\n[Causal chain & counterfactual]")
        for item in view["因果链校验_人话"]:
            lines.append(f"  - {item}")
        lines += ["\n[Certificate]",
                  f"  Audit ID {c['audit_id']} · {c['algorithm']} · verifiable: {c['verifiable']}"]
        return "\n".join(lines)

# ==================== 便捷入口（demo） ====================

