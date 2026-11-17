"""scripts/research.py - 研究编排层（入口服别→分档L0-L3→按档澄清/拆解/派agent）。

库本身**不直接 spawn agent**：通过注入 agent_fn/fetch_fn 回调实现派发，prompt 用
**锁定模板**（仅替换变量，禁止自由改写）。无注入时降级为库内 retrieve() 多维度拆解，
零硬依赖。这延续路径 B"抓取外移"与"质量层库"的哲学：研究循环由调用方(agent 层)驱动，
本模块只负责编排与状态。

设计对齐 deep-research 两个子技能的可借鉴机制（已按用户拍板库化重映射，不整体搬工作流）：
- 点1 重框 → 入口服别 + 分档耦合的"最小化澄清"（L0/L1 基本不问，L2/L3 仅歧义处问一句）
- 点3 重框 → 按档位+意图派子 agent（L0/L1 不派，L2 按维度派，L3 多角色循环），prompt 锁模板
- 点2     → ResearchState 内存对象，落盘由调用方决定（model_dump_json），库不写文件
"""

import os
import re
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

import orchestrate

# ---- D4 显式深度档位：用户选深度、库选策略（只做参数面，不增引擎）----
_DEPTH_TIER = {"quick": "L1", "standard": "L2", "deep": "L3"}


def _depth_to_tier(depth: Optional[str]) -> Optional[str]:
    """depth -> 内部档位；非已知值返回 None（交既有启发式）。"""
    return _DEPTH_TIER.get(depth) if depth else None


# ---- 锁定模板（仅替换变量，禁止自由改写）----
_TIER_CLASSIFY_TMPL = (
    "任务: 判断问题复杂度档位(L0-L3)\n问题: {query}\n"
    "L0 单一事实/定义/数值; L1 一个明确子问题需一次检索; "
    "L2 需多维度拆解或对原因/做法给结论; L3 需多轮检索-批判-精炼跨源综合\n"
    "只返回一词: L0 / L1 / L2 / L3"
)
_DISPATCH_RESEARCHER_TMPL = (
    "任务: 调研维度「{dimension}」(深度:{detail_level})\n主题: {topic}\n时间范围: {time_range}\n"
    "要求: 获取证据并返回该维度结论与来源\n禁止: 改写本模板结构"
)
_DISPATCH_CRITIC_TMPL = (
    "任务: 批判审查研究发现, 标出无来源支撑/跨源冲突/过度推断处\n"
    "主题: {topic}\n研究发现: {findings}\n返回: 问题清单+改进建议"
)


@dataclass
class ResearchState:
    """研究循环的内存状态对象（点2：不写文件，调用方按需序列化）。"""

    query: str
    tier: str = "auto"
    schema: List[Dict[str, Any]] = field(default_factory=list)
    evidence: List[Dict[str, Any]] = field(default_factory=list)  # 跨轮累积基底(prior_evidence)
    clarifications: List[str] = field(default_factory=list)
    iterations: int = 0
    findings: str = ""
    uncertainties: List[Dict[str, Any]] = field(default_factory=list)
    sources: List[Dict[str, Any]] = field(default_factory=list)
    scores: List[Dict[str, Any]] = field(default_factory=list)
    confidence: float = 0.0
    fact_verdicts: List[Dict[str, Any]] = field(default_factory=list)
    verify_issues: List[Dict[str, Any]] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    vault_dir: Optional[str] = None
    resume: bool = False
    confirm_outline: bool = False


@dataclass
class _Deps:
    """调用方注入的能力集合（"调用方注入"）：库内零密钥、零内置模型、不自行 spawn agent。

    把 retriever 的固定 kwargs 收口在 `retrieve()` 里，避免同一组注入参数在
    维度派发 / 首轮检索 / L3 精炼三处各写一遍（漏传即静默丢注入，已踩过一次）。
    """

    retriever: Callable
    cfg: Dict[str, Any] = field(default_factory=dict)
    agent_fn: Optional[Callable] = None
    fetch_fn: Optional[Callable] = None
    web_fetch: Optional[Callable] = None
    closure_fn: Optional[Callable] = None
    doi_resolver: Optional[Callable] = None
    github_token: Any = None

    def retrieve(
        self, query: str, schema: List[Dict[str, Any]], evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return self.retriever(
            query,
            cfg=self.cfg,
            schema=schema,
            prior_evidence=list(evidence) or None,
            web_fetch=self.web_fetch,
            doi_resolver=self.doi_resolver,
            github_token=self.github_token,
        )


def _heuristic_tier(query: str) -> str:
    q = (query or "").strip()
    if len(q) < 18 and not any(
        k in q
        for k in ("为什么", "对比", "区别", "根因", "如何", "分析", "评估", "方案", "研究", "原因")
    ):
        return "L0"
    if any(k in q for k in ("为什么", "根因", "原因", "如何")):
        return "L2"
    if any(k in q for k in ("对比", "区别", "分析", "评估", "方案", "研究", "调研")):
        return "L2"
    return "L1"


def _classify_tier(query: str, cfg: Dict[str, Any], tier: str = "auto") -> str:
    if tier and tier != "auto":
        return tier
    rc = (cfg or {}).get("research") or {}
    # opt-in 模型分档: 由调用方注入 tier_classify_fn 实现(库内置仅启发式)
    if rc.get("model_tier") and rc.get("tier_classify_fn"):
        try:
            return rc["tier_classify_fn"](query, _TIER_CLASSIFY_TMPL)
        except Exception:
            pass
    return _heuristic_tier(query)


def _clarify(query: str, tier: str, cfg: Dict[str, Any], clarify_fn: Callable) -> Optional[str]:
    """点1 重框: L0/L1 基本不问; L2/L3 仅在 clarify_fn 提供且判定歧义时问一句。"""
    if tier in ("L0", "L1") or not clarify_fn:
        return None
    if ((cfg or {}).get("research") or {}).get("clarify_l2l3", True) is False:
        return None
    # 启发式: 过短或明显缺对象的问句视为需澄清
    if len(query.strip()) < 15:
        try:
            return clarify_fn(query)
        except Exception:
            return None
    return None


_DEFAULT_DIMENSIONS = [
    {"name": "定义与概念", "detail_level": "简要"},
    {"name": "机制/原理", "detail_level": "详细"},
    {"name": "对比/异同", "detail_level": "简要"},
    {"name": "现状/应用", "detail_level": "简要"},
    {"name": "争议/局限", "detail_level": "简要"},
]

# 金融分析维度模板：命中金融意图（股价/财报/营收…）时替代通用百科模板。
# 维度名含财报文本已有关键词（营业收入/归母净利润/每股收益/ROE/同比），确保 report 布局命中。
_FINANCE_DIMENSIONS = [
    {"name": "营业收入", "detail_level": "简要"},
    {"name": "归母净利润", "detail_level": "简要"},
    {"name": "每股收益", "detail_level": "简要"},
    {"name": "ROE", "detail_level": "简要"},
    {"name": "同比变动", "detail_level": "简要"},
]


def _decompose(query: str, tier: str, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    """拆解为维度 schema(A 的输入)。L0/L1 返回空(扁平输出); L3 各维升为详细。

    金融意图(query 含股价/财报/营收等) → 改用金融分析维度模板，替代通用百科模板。
    """
    if tier in ("L0", "L1"):
        return []
    from connector import _source_intent

    if _source_intent(query) == "finance":
        if tier == "L3":
            return [dict(d, detail_level="详细") for d in _FINANCE_DIMENSIONS]
        return [dict(d) for d in _FINANCE_DIMENSIONS]
    if tier == "L3":
        return [dict(d, detail_level="详细") for d in _DEFAULT_DIMENSIONS]
    return [dict(d) for d in _DEFAULT_DIMENSIONS]


def _time_range(cfg: Dict[str, Any]) -> str:
    return ((cfg or {}).get("research") or {}).get("time_range", "近3年")


def _merge_evidence(evidence: List[Dict[str, Any]], new_items) -> List[Dict[str, Any]]:
    """按 url 去重并入证据基底（原地）。

    质量层返回的 sources 本身含上一轮 carried 条目，逐轮/逐维度无脑 extend 会让同一来源
    反复叠加、prior_evidence 随轮次膨胀（每轮都要重新打分/核验）。此处按 url 收口。
    """
    if not new_items:
        return evidence
    if isinstance(new_items, dict):
        new_items = [new_items]
    seen = {e.get("url") for e in evidence if e.get("url")}
    for it in new_items:
        if not isinstance(it, dict):
            continue
        u = it.get("url")
        if u and u in seen:
            continue
        if u:
            seen.add(u)
        evidence.append(it)
    return evidence


def _closure_satisfied(
    schema: List[Dict[str, Any]], evidence: List[Dict[str, Any]], findings: str
) -> bool:
    """D2 逻辑闭环停：主问题是否已能回答（呼应深分协议 §3「我为什么可以在这里停」）。

    启发式：证据基底中至少 1 条锚定来源(url) + 每个 schema 子目标关键词已在证据文本中出现。
    子目标关键词按中文分隔符切分（去「与/和/及/(/)」等连接词），任一词命中即视为该维已覆盖。
    无 schema（扁平 L0/L1）时退化为「有 findings 且有锚定来源」即闭环。
    """
    has_anchored = any(e.get("url") for e in evidence)
    if not has_anchored:
        return False
    ev_text = " ".join(
        (e.get("text") or "") + " " + (e.get("url") or "") + " " + (e.get("snippet") or "")
        for e in evidence
    ).lower()
    if not schema:
        return bool(findings.strip())
    for dim in schema:
        name = dim.get("name", "") or ""
        tokens = [t for t in re.split(r"[\s/、，,（）()与和及]+", name) if len(t) >= 2]
        if not tokens:
            tokens = [name]
        if not any(tok.lower() in ev_text for tok in tokens):
            return False
    return True


# ---------------------------------------------------------------- 阶段助手

_VAULT_NOTE = "落盘已开启；设 vault_dir=None 可关闭，关闭后将丢失续跑/可重跑/结构化留存"


def _open_vault(vault_dir: Optional[str], cfg: Dict[str, Any], query: str, tier: str):
    """解析并初始化 Research Vault（A1）。返回 (vault_path_or_None, meta_vault, resolved_dir)。

    P1-7 默认关：仅当调用方显式传入 vault_dir，或 cfg.research.vault_enabled=True（且配置了 vault_dir）
    时才落盘；否则一律回到纯内存，避免默认把 vault 写到 cwd 污染工作区。
    """
    if vault_dir is None:
        rc = (cfg or {}).get("research") or {}
        if rc.get("vault_enabled", False):
            vault_dir = rc.get("vault_dir")
    if not vault_dir:
        return None, {"enabled": False}, None
    import vault as _vault

    vp = _vault.init_vault(vault_dir, query, tier)
    _vault.write_index(vp, query, tier)
    return vp, {"enabled": True, "path": os.path.abspath(vp), "note": _VAULT_NOTE}, vault_dir


def _resume_snapshot(vp: str, state: ResearchState) -> bool:
    """A4 可重跑：已完成则把缓存结果灌回 state 并返回 True（跳过重抓）。"""
    import vault as _vault

    st0 = _vault.load_state(vp)
    if not (st0.get("completed") and st0.get("findings") is not None):
        return False
    state.findings = st0.get("findings", "")
    state.iterations = st0.get("iterations", state.iterations)
    return True


def _dispatch_dimensions(query: str, state: ResearchState, deps: _Deps) -> None:
    """点3 重框：按维度派子 agent（外部注入优先）或库内按维度检索。"""
    schema = state.schema
    if not schema:
        return
    if deps.agent_fn:
        # 外部真派子 agent（agent 层接 web_fetch / 子 agent，锁模板）
        for dim in schema:
            prompt = _DISPATCH_RESEARCHER_TMPL.format(
                dimension=dim["name"],
                detail_level=dim["detail_level"],
                topic=query,
                time_range=_time_range(deps.cfg),
            )
            _merge_evidence(state.evidence, deps.agent_fn(prompt, dim=dim, fetch_fn=deps.fetch_fn))
        return
    if ((deps.cfg or {}).get("research") or {}).get("agent_dispatch"):
        # 库内按维度派发（用内部两跳抓取，零硬依赖，开箱即用）
        for dim in schema:
            sub = deps.retrieve(f"{query}（聚焦维度：{dim['name']}）", [dim], state.evidence)
            _merge_evidence(state.evidence, sub.get("sources", []))


def _absorb_first(state: ResearchState, res: Dict[str, Any]) -> None:
    """首轮质量层结果并入 state。"""
    state.findings = res.get("findings", "")
    state.uncertainties = res.get("uncertainties", [])
    state.sources = res.get("sources", [])
    state.scores = res.get("scores", [])
    state.confidence = res.get("confidence", 0.0)
    state.fact_verdicts = res.get("fact_verdicts", [])
    state.verify_issues = res.get("verify_issues", [])
    state.warnings = list(res.get("warnings", []))
    state.iterations = 1
    _merge_evidence(state.evidence, state.sources)


def _absorb_refined(state: ResearchState, res: Dict[str, Any]) -> None:
    """精炼轮结果并入 state：仅当正文更长才替换（防越精炼越短），缺省字段保持上轮。"""
    findings = res.get("findings", "")
    if len(findings) > len(state.findings):
        state.findings = findings
    state.uncertainties = res.get("uncertainties", state.uncertainties)
    state.sources = res.get("sources", state.sources)
    if res.get("scores") is not None:
        state.scores = res.get("scores", state.scores)
    if res.get("confidence") is not None:
        state.confidence = res.get("confidence", state.confidence)
    state.fact_verdicts = res.get("fact_verdicts", state.fact_verdicts)
    state.verify_issues = res.get("verify_issues", state.verify_issues)
    for w in res.get("warnings", []):
        if w not in state.warnings:
            state.warnings.append(w)
    _merge_evidence(state.evidence, state.sources)


def _refine_loop(
    query: str, state: ResearchState, deps: _Deps, max_iter: int, closure_check: bool
) -> None:
    """L3 精炼循环：每轮把新增来源并回证据基底，下一轮才真正"在已有证据上精炼"。

    D2 逻辑闭环停：循环前置 + 末置各判一次——主问题已能回答即提前停（iter < max_iter）。
    注入 closure_fn 时优先用真语义判停（调用方的 LLM），否则退关键词启发式。
    """
    for _ in range(max(0, max_iter - 1)):
        if closure_check and _closure_satisfied(state.schema, state.evidence, state.findings):
            return
        res = deps.retrieve(query, state.schema, state.evidence)
        state.iterations += 1
        _absorb_refined(state, res)
        if deps.closure_fn is not None:
            try:
                if deps.closure_fn(query, state.evidence, state.findings):
                    return
            except Exception:
                pass
        if closure_check and _closure_satisfied(state.schema, state.evidence, state.findings):
            return


def _persist_vault(
    vp: str,
    query: str,
    state: ResearchState,
    resume: bool,
    cfg: Dict[str, Any],
    export_citations: Optional[str],
    meta: Dict[str, Any],
) -> None:
    """A3/A4 落盘：去重写 items + 幂等 report + 引用导出 + .state.json。"""
    import vault as _vault

    done = set(_vault.load_state(vp).get("completed", [])) if resume else set()
    base = len(done)
    for i, src in enumerate(state.evidence):
        u = src.get("url")
        if u and u in done:
            continue
        _vault.write_item(vp, base + i + 1, query, src)
        if u:
            done.add(u)
    # D8：恒用增量模式（T7 已声明幂等、不重复重读 items），避免 L3 每轮全量重读语料
    _vault.render_report(vp, sources=state.sources, incremental=True)
    # D5 引用导出：bibtex / md / both（纯文本轻量，纯 web 源退化为 URL 引用）
    if export_citations and state.sources:
        fmt = str(export_citations).lower()
        if fmt in ("bibtex", "both"):
            _vault.write_citations(vp, state.sources, "bibtex")
        if fmt in ("md", "both"):
            _vault.write_citations(vp, state.sources, "md")
        meta["vault"]["citations"] = {"format": fmt}
    _vault.save_state(
        vp, {"completed": list(done), "findings": state.findings, "iterations": state.iterations}
    )


def _detect_conflicts(
    query: str, state: ResearchState, conflict_check_fn: Optional[Callable], meta: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """T3：M51 语义冲突检测（可选门控；默认 None 不检测，保持零依赖）。"""
    if not (conflict_check_fn and state.evidence):
        return []
    try:
        conflicts = conflict_check_fn(query, state.evidence) or []
    except Exception:
        return []
    if conflicts:
        meta["conflicts"] = conflicts
    return conflicts


def _skip_message(query: str, reason: str) -> str:
    """P0-3 自主不检索时的拒答/澄清文案。"""
    q = (query or "").strip()
    if reason == "无需检索":
        return (
            "（该问题关于本检索能力自身，无需联网检索）\n"
            "我是 Signal-Search 质量层检索：输入一个事实/对比/调研类问题，"
            "我会先分档(L0–L3)、取源、打分、做事实级核验(M51)与引文真实护栏(VERITAS)，"
            "再给出带置信度与未确认项的结论。请直接提出你的检索问题。"
        )
    if reason == "需澄清":
        return (
            "（问题过于含糊，暂未检索）\n"
            f"你的问题「{q}」缺少可检索的对象或限定条件，直接检索只会返回噪声。"
            "请补充：具体对象（如「某公司/某技术/某事件」）与你想了解的维度"
            "（如「原理/对比/最新进展/风险」），我再帮你检索。"
        )
    # 不可检索（空/寒暄等）
    return (
        "（未检索）\n"
        f"「{q}」不是可检索的问题。请提出一个事实核查、对比或调研类问题，"
        "例如「2025 年主流大模型上下文窗口最大的是哪家」。"
    )


# 注：_skip_message 上方曾有遗留的 _snapshot 死代码块（位于其提前 return 之后，不可达），
# 已于 P0-3/P1 清理；research() 的返回统一由下方 _snapshot() 负责。


def _snapshot(state: ResearchState, meta: Dict[str, Any], **extra) -> Dict[str, Any]:
    """汇总 ResearchState + meta 为 research() 最终返回 dict（P0-3 补回：原缺失定义，research 每路 return 均依赖它）。

    - extra 中的字段（findings/confidence/skipped/skip_reason/needs_confirm/outline/resumed/conflicts 等）
      同时出现在顶层与 meta 内，兼容 research_cli / eval 的读取方式。
    """
    result: Dict[str, Any] = {
        "query": state.query,
        "tier": state.tier,
        "tier_used": state.tier,
        "schema": list(state.schema),
        "iterations": state.iterations,
        "findings": extra.get("findings", state.findings),
        "confidence": extra.get("confidence", state.confidence),
        "uncertainties": list(state.uncertainties),
        "sources": list(state.sources),
        "scores": list(state.scores),
        "fact_verdicts": list(state.fact_verdicts),
        "verify_issues": list(state.verify_issues),
        "clarifications": list(state.clarifications),
        "meta": {**meta, "warnings": list(state.warnings), **extra},
    }
    result.update(extra)  # 顶层暴露 skipped/needs_confirm/outline/resumed/conflicts/skip_reason
    return result


def research(
    query: str,
    cfg: Dict[str, Any] = None,
    tier: str = "auto",
    clarify_fn: Callable = None,
    agent_fn: Callable = None,
    fetch_fn: Callable = None,
    max_iter: int = 3,
    prior_evidence: List[Dict[str, Any]] = None,
    retriever: Callable = None,
    web_fetch: Callable = None,
    vault_dir: str = None,
    resume: bool = False,
    confirm_outline: bool = False,
    depth: str = None,
    closure_check: bool = True,
    export_citations: str = None,
    conflict_check_fn: Callable = None,
    closure_fn: Callable = None,
    doi_resolver: Callable = None,
    github_token: Any = None,
) -> Dict[str, Any]:
    """研究编排入口。

    流程: 入口服别 → 分档(L0-L3) → (按档澄清) → (拆解→schema) → (按档派 agent/检索) → 合成。
    - retriever: 质量层检索函数, 默认 orchestrate.retrieve; 测试可注入假实现。
    - agent_fn(prompt, dim, fetch_fn): 注入时按维度派子 agent(锁模板 _DISPATCH_RESEARCHER_TMPL)。
    - prior_evidence: 跨轮证据基底(C), 标 carried 并入质量层, 避免重抓。
    - vault_dir: Research Vault 落盘目录(A1-A5)。默认 None → 不落盘（纯内存，P1-7 默认关）；
      仅当显式传入 vault_dir，或 cfg.research.vault_enabled=True 时才落盘。开启时返回 meta.vault 提醒可关。
    - resume: 重跑时跳过已完成 item、不重抓缓存（A4）。
    - confirm_outline: 写 outline.md 后早返回（meta.needs_confirm=True），等调用方确认/编辑再继续（A5 HITL）。
    - depth: D4 显式深度档位 "quick"→L1 / "standard"→L2 / "deep"→L3；给定时覆盖 tier 启发式，null→auto。
      只做参数面，不增引擎；文档明示「用户选深度、库选策略」。
    - closure_check: D2 逻辑闭环停，默认 True。L3 循环在「主问题已能回答」（各子目标证据已覆盖+≥1 锚定源）
      时提前停，呼应深分协议 §3「我为什么可以在这里停」；设 False 回覆盖率停。
    - export_citations: D5 引用导出 "bibtex"/"md"/"both"；vault 开启时
      在 vault 内写 citations.bib / references.md。
    - conflict_check_fn: 可选回调(query, evidence)->冲突列表；由调用方注入
      （即 agent 用的 LLM，见 examples/conflict_llm.py 适配器），做 M51 语义冲突
      检测，结果写 meta.conflicts + 返回 conflicts。库内不调用任何 LLM；默认 None
      不检测，零依赖。
    - closure_fn: 可选回调(query, evidence, findings)->bool；提供则 L3 循环用真
      语义判停（主问题是否已答），优先于关键词启发式（默认 None 维持 D2 启发式）。
    - doi_resolver: 可选回调(arxiv_id)->doi 字符串；提供则学术源(arXiv)按 id 回填
      DOI，BibTeX 升级 @article（D3）。库内不内置任何书目源、不读环境变量；默认
      None 不回填、退 @misc。书目源由调用方注入（S2/Crossref/自有库皆可）。
    - github_token: 可选字符串/列表；提供则 GitHub 源(B2)用此 token 打官方 API，
      调用方注入、优选于 env GITHUB_TOKEN。库内仍读 env 作开箱即用兜底，但调用方
      想用自己的直接传。默认 None → 回落 env GITHUB_TOKEN → 再无则 web_fetch 兜底。
    """
    cfg = cfg or {}
    deps = _Deps(
        retriever=retriever or orchestrate.retrieve,
        cfg=cfg,
        agent_fn=agent_fn,
        fetch_fn=fetch_fn,
        web_fetch=web_fetch,
        closure_fn=closure_fn,
        doi_resolver=doi_resolver,
        github_token=github_token,
    )

    # D4 显式深度档位：depth 给定时覆盖 tier 启发式（用户选深度、库选策略）
    tier = _depth_to_tier(depth) or _classify_tier(query, cfg, tier)
    state = ResearchState(
        query=query,
        tier=tier,
        evidence=list(prior_evidence or []),
        vault_dir=vault_dir,
        resume=resume,
        confirm_outline=confirm_outline,
    )

    # P0-3 自主不检索：在检索/落盘前先行判定，命中则直接拒答/澄清，不浪费检索与 IO。
    # 保守判定：仅对无检索价值/过于含糊/自答即可 的输入命中，正常 L0–L3 可检索查询一律放行。
    if ((cfg or {}).get("research") or {}).get("should_skip", True):
        from plan import classify_intent as _classify_intent
        from route import should_skip_search as _should_skip

        skip, reason = _should_skip(
            query, intent=_classify_intent(query), ctx={"tier": tier, "cfg": cfg}
        )
        if skip:
            return _snapshot(
                state,
                {"vault": {"enabled": False}, "skipped": True, "skip_reason": reason},
                skipped=True,
                skip_reason=reason,
                findings=_skip_message(query, reason),
                confidence=0.0,
            )

    # Vault 集成（A1-A5）：解析落盘目录 + 初始化（默认开，见 config.research.vault_dir）
    vp, meta_vault, vault_dir = _open_vault(vault_dir, cfg, query, tier)
    meta: Dict[str, Any] = {"vault": meta_vault}

    # 1) 澄清(按档) — 点1 重框
    cl = _clarify(query, tier, cfg, clarify_fn)
    if cl:
        state.clarifications.append(cl)
        query = f"{query}（澄清：{cl}）"

    # 2) 拆解 → schema
    state.schema = _decompose(query, tier, cfg)

    # A2 STORM 多视角大纲（vault 开启时落盘；HITL: confirm_outline 写 outline 后早返回）
    if vp is not None:
        import vault as _vault

        _vault.write_outline(vp, query, state.schema, tier)
        if confirm_outline:
            return _snapshot(
                state,
                meta,
                needs_confirm=True,
                outline=_vault.vault_path(vault_dir, query) + "/outline.md",
            )
        # A4 可重跑：resume 且已完成则跳过重抓，直接返回缓存（不调 retriever）
        if resume and _resume_snapshot(vp, state):
            return _snapshot(state, meta, resumed=True)

    # 3) 派发 — 点3 重框
    _dispatch_dimensions(query, state, deps)

    # 4) 质量层(retrieve())
    _absorb_first(state, deps.retrieve(query, state.schema, state.evidence))

    # 5) L3 精炼循环(用 prior_evidence 跨轮累积)
    if tier == "L3":
        _refine_loop(query, state, deps, max_iter, closure_check)

    # 6) 落盘 + 冲突检测
    if vp is not None:
        _persist_vault(vp, query, state, resume, cfg, export_citations, meta)
    conflicts = _detect_conflicts(query, state, conflict_check_fn, meta)

    return _snapshot(state, meta, conflicts=conflicts)
