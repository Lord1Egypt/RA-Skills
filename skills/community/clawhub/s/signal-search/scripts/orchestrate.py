"""scripts/orchestrate.py - 顶层检索编排（V1-14 / §4 契约）。

对外暴露干净原语 `retrieve(query, constraints, budget)`，串起 意图→档位→规划→取源→抽取→去重
→打分→自适应停止→汇总→验证。被其它类别工具当"检索能力"消费。

本模块只做"编排"：每个阶段一个单一职责私有 helper，`retrieve` 自身只负责按顺序串联并组装
返回契约。各 helper 内部按需惰性导入（sys.modules 命中即返回，不增加运行时开销），保持
库的冷启动足够轻。
"""

import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Dict, List, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from common import load_config as _load_cfg

# 显式深度档位（D4）：用户选深度、库选策略
_DEPTH_TO_TIER = {"quick": "L1", "standard": "L2", "deep": "L3"}


@dataclass
class _Inject:
    """调用方注入的外部能力（"调用方注入"）。库内零密钥、零内置模型，全部由调用方提供。"""

    web_fetch: Any = None
    doi_resolver: Any = None
    github_token: Any = None


@dataclass
class _RunPlan:
    """本次检索的档位与预算解析结果。"""

    tier: str
    budget: int
    max_sources: int
    freshness: str


@dataclass
class _Expansion:
    """补抓一轮后的状态（供自适应停止判据消费）。"""

    docs: List[Dict[str, Any]]
    scores: List[Dict[str, Any]]
    token_used: int
    budget_hit: bool
    exhausted: bool = False
    prev_rounds: List[List[Dict[str, Any]]] = field(default_factory=list)
    new_batch: List[Dict[str, Any]] = field(default_factory=list)


def _estimate_tokens(text: str) -> int:
    """粗估 token：CJK≈1 字/token，英文≈4 字符/token（用于预算软上限监测）。"""
    cjk = len(re.findall(r"[\u4e00-\u9fa5]", text or ""))
    other = len(text or "") - cjk
    return int(cjk + other / 4)


# ---------------------------------------------------------------- 阶段 1：档位


def _apply_tier_override(query: str, constraints: dict, depth: str = None) -> Tuple[str, dict]:
    """解析 `/signal Lx` 内嵌覆盖与显式 depth 档位。query 内嵌覆盖优先于 depth。"""
    import route

    clean_q, override = route.parse_override(query)
    if override:
        constraints = dict(constraints)
        constraints["required_tier"] = override
        return clean_q, constraints
    if depth in _DEPTH_TO_TIER:
        constraints = dict(constraints)
        constraints["required_tier"] = _DEPTH_TO_TIER[depth]
    return query, constraints


def _make_run_plan(query: str, constraints: dict, budget: int, cfg: dict) -> _RunPlan:
    """档位路由 → 预算 / 来源上限 / 时效要求。"""
    import route

    tier, _reason = route.classify_tier(query, constraints)
    tier_cfg = cfg.get("tier_defaults", {}).get(tier, {})
    return _RunPlan(
        tier=tier,
        budget=tier_cfg.get("budget", 8000) if budget is None else budget,
        max_sources=constraints.get("max_sources") or tier_cfg.get("max_sources", 3),
        freshness=constraints.get("freshness", "中"),
    )


# ---------------------------------------------------------------- 阶段 2：取源


def _fetch_and_extract(
    q: str, freshness: str, constraints: dict, cfg: dict, inject: _Inject
) -> List[Dict[str, Any]]:
    """取源 + 两跳深取(SERP→落地页) + 抽取，统一入口（方案 B）。"""
    import connector
    import deepfetch
    import extract

    raw = connector.load(
        q,
        freshness,
        constraints,
        cfg,
        web_fetch=inject.web_fetch,
        doi_resolver=inject.doi_resolver,
        github_token=inject.github_token,
    )
    if cfg.get("deep_fetch", {}).get("enabled", True):
        raw = deepfetch.resolve(raw, cfg)
    for d in raw:
        if not d.get("landing_resolved"):
            extract.extract(d, cfg)
    return raw


def _prepare_external_docs(docs: list, cfg: dict, tr) -> List[Dict[str, Any]]:
    """外部(agent 用 web_fetch 抓好的 (url, text))直进质量层，仅做字段兜底。

    无 url 的条目无法被引用校验/事实锚定消费，直接剔除并计数（不静默塞进 sources）。
    """
    import extract

    n_in = len(docs)
    docs = [d for d in docs if d.get("url")]
    for d in docs:
        d.setdefault("engine", "external")
        d.setdefault("landing_resolved", True)
        if not d.get("text") and d.get("raw_html"):
            extract.extract(d, cfg)
    tr.event(
        "fetch",
        {
            "n_docs": len(docs),
            "external": True,
            "dropped_no_url": n_in - len(docs),
            "engines": sorted({d.get("engine") for d in docs}),
        },
    )
    return docs


def _gather_internal_docs(
    query: str, leaves: list, rp: _RunPlan, constraints: dict, cfg: dict, tr, inject: _Inject
) -> Tuple[List[Dict[str, Any]], List[str]]:
    """内部取源：L3 走并行扇出，其余按查询规划叶子串行取。返回 (docs, warnings)。"""
    import connector

    docs: List[Dict[str, Any]] = []
    warnings: List[str] = []
    if rp.tier == "L3":
        import deepfetch
        import extract
        import parallel

        docs = parallel.run_l3(
            query,
            constraints,
            cfg,
            web_fetch=inject.web_fetch,
            doi_resolver=inject.doi_resolver,
            github_token=inject.github_token,
        )
        if cfg.get("deep_fetch", {}).get("enabled", True):
            docs = deepfetch.resolve(docs, cfg)
        for d in docs:
            if not d.get("landing_resolved"):
                extract.extract(d, cfg)
    else:
        qs = [lv["q"] for lv in leaves if not lv.get("truncated")] or [query]
        for q in qs[: rp.max_sources]:
            docs += _fetch_and_extract(q, rp.freshness, constraints, cfg, inject)
            warnings.extend(connector.LAST_WARNINGS)
    tr.event("fetch", {"n_docs": len(docs), "engines": sorted({d.get("engine") for d in docs})})
    return docs, warnings


def _merge_prior_evidence(docs: list, prior_evidence: list, tr) -> List[Dict[str, Any]]:
    """C: 跨轮证据基底并入质量层，标 carried 避免重抓。

    按 url 与本轮结果去重：多轮研究会把上一轮 sources 原样回传，不去重会逐轮叠加同源文档。
    """
    if not prior_evidence:
        return docs
    seen_urls = {d.get("url") for d in docs if d.get("url")}
    n_carried = 0
    for pe in prior_evidence:
        u = pe.get("url")
        if u and u in seen_urls:
            continue
        pe = dict(pe)
        pe["carried"] = True
        pe.setdefault("engine", "carried")
        pe.setdefault("landing_resolved", True)
        docs.append(pe)
        if u:
            seen_urls.add(u)
        n_carried += 1
    tr.event("carry", {"n_prior": len(prior_evidence), "n_carried": n_carried})
    return docs


# ---------------------------------------------------------------- 阶段 3：收敛


def _dedup_threshold(cfg: dict, external: bool) -> int:
    """外部短摘要输入用更严格阈值，保留跨引擎候选源供 M51 锚定；内部走默认阈值。"""
    dd = cfg.get("dedup") or {}
    return dd.get("external_threshold", 1) if external else dd.get("default_threshold", 3)


def _score_all(docs: list, query: str, cfg: dict, freshness: str = None) -> List[Dict[str, Any]]:
    import score

    # 解析一次：config 有 credibility_table 用配置，否则用库内置 DEFAULT_CRED（模块常量，不触盘）；
    # 避免逐 doc 透传 None 导致 score_source 内 load_config() 重复读磁盘（P3）
    cred = cfg.get("credibility_table") or score.DEFAULT_CRED
    return [score.score_source(d, query, cred, freshness=freshness) for d in docs]


def _expand_if_needed(
    docs: list,
    scores: list,
    query: str,
    rp: _RunPlan,
    constraints: dict,
    cfg: dict,
    external: bool,
    dd_thr: int,
    inject: _Inject,
) -> Tuple[_Expansion, List[str]]:
    """自适应补抓：外部 docs 已完整则跳过；L0/L1 一轮即停；L2/L3 视覆盖补一轮（受预算限制）。"""
    import budget as _budget
    import connector
    import dedup

    token_used = _estimate_tokens(" ".join(d.get("snippet", "") for d in docs))
    exp = _Expansion(
        docs=docs,
        scores=scores,
        token_used=token_used,
        budget_hit=_budget.monitor(token_used, rp.budget)["over"],
        new_batch=docs,
    )
    need_more = (
        not external
        and rp.tier in ("L2", "L3")
        and len(docs) < rp.max_sources
        and not exp.budget_hit
    )
    if not need_more:
        return exp, []

    more = _fetch_and_extract(query, rp.freshness, constraints, cfg, inject)
    warnings = list(connector.LAST_WARNINGS)
    # stop.should_stop 用 (已完成轮次, 本轮新增) 判"连续两轮无新信息"：
    # 首轮尚无历史轮次，prev_rounds 必须为空，否则新增文档会被自身历史遮蔽、fresh 恒为 0
    exp.prev_rounds = [list(docs)]
    exp.new_batch = more
    exp.docs = dedup.near_dup(docs + more, threshold=dd_thr)
    exp.scores = _score_all(exp.docs, query, cfg)
    exp.token_used = _estimate_tokens(" ".join(d.get("snippet", "") for d in exp.docs))
    exp.budget_hit = _budget.monitor(exp.token_used, rp.budget)["over"]
    exp.exhausted = len(exp.docs) < rp.max_sources
    return exp, warnings


def _truncate_to_cap(docs: list, scores: list, max_sources: int):
    """按 weighted（或 rerank_score，若存在）降序截断到 max_sources。"""

    def _rk(x):
        s = x[1]
        return s.get("rerank_score", s.get("weighted", 0))

    paired = sorted(zip(docs, scores), key=_rk, reverse=True)[:max_sources]
    return [d for d, _ in paired], [s for _, s in paired]


# ---------------------------------------------------------------- 阶段 4：汇总


def _cite_rate(findings: str, docs: list) -> float:
    """引文真实率：findings 中引用的 URL 真实存在于 sources 的比例（假引用拉低置信度）。"""
    import verify as _v

    cited = set(_v.URL_RE.findall(findings or ""))
    if not cited:
        return 1.0
    real = {d.get("url") for d in docs if d.get("url")}
    return len(cited & real) / len(cited)


def _summarize(
    docs: list, scores: list, query: str, schema: list, cfg: dict, external: bool
) -> Dict[str, Any]:
    """汇总 + 事实级核验 + 不确定聚合 + 验证护栏。"""
    import report
    import verify

    findings = report.synthesize(docs, scores, query, schema=schema)
    # 外部(web_fetch 短摘要)输入自动启用 M51 语义核验：A/B 实证外部短摘要下关键词重叠弱锚定失效；
    # semantic_fact_verify 无 sentence-transformers 时自动回退关键词基线，不会强制加载重依赖。
    # 内部路径默认仍走关键词基线（除非 config.verify.semantic 显式开启）。
    if external or (cfg.get("verify") or {}).get("semantic", False):
        facts = verify.semantic_fact_verify(findings, docs, cfg)
    else:
        facts = verify.fact_level_verify(findings, docs)
    uncertainties = verify.aggregate_uncertainties(facts, docs)
    # 未确认项只影响正文末尾，直接追加即可（重跑 synthesize 等于把维度排版全量算第二遍）
    findings = report.append_uncertainties(findings, uncertainties)
    # 置信度（P0-2）：用全量信号（M51 TRUE率 / 引文真实率 / 未确认项）合成，覆盖 synthesize 内部初算值
    cite_rate = _cite_rate(findings, docs)
    conf = report.confidence_of(
        scores, verdicts=facts, citation_real_rate=cite_rate, n_uncertain=len(uncertainties)
    )
    findings = re.sub(r"置信度：[\d.]+", f"置信度：{conf}", findings)
    return {
        "findings": findings,
        "fact_verdicts": facts,
        "uncertainties": uncertainties,
        "verify_issues": verify.verify(docs, findings),
        "confidence": conf,
    }


# ---------------------------------------------------------------- 对外入口


def _clean_sources_active(cfg: dict) -> bool:
    """干净源预灌是否启用：零配置即得干净源，但测试/离线环境默认不触发联网（除非显式开闸），
    保护现有 pytest 门禁不退步；显式 web_fetch= 注入时由调用方接管，不走本供给。"""
    if os.environ.get("PYTEST_CURRENT_TEST") and not os.environ.get("SIGNAL_SEARCH_CLEAN_ON"):
        return False
    if os.environ.get("SIGNAL_SEARCH_OFFLINE"):
        return False
    cs = (cfg or {}).get("clean_sources") or {}
    return bool(cs.get("enabled"))


def retrieve(
    query: str,
    constraints: dict = None,
    budget: int = None,
    cfg: dict = None,
    docs: list = None,
    schema: list = None,
    prior_evidence: list = None,
    web_fetch: Any = None,
    depth: str = None,
    doi_resolver: Any = None,
    github_token: Any = None,
) -> Dict[str, Any]:
    cfg = _load_cfg(cfg)
    query = (
        query or ""
    )  # 防御 None/空：避免下游 parse_override/classify_intent 对 None.strip() 崩溃（D4）
    constraints = constraints or {}
    inject = _Inject(web_fetch=web_fetch, doi_resolver=doi_resolver, github_token=github_token)

    # 1) 档位覆盖 + 预算解析
    query, constraints = _apply_tier_override(query, constraints, depth)
    rp = _make_run_plan(query, constraints, budget, cfg)

    import trace as _trace

    tr = _trace.Trace(cfg)
    tr.event("start", {"query": query, "tier": rp.tier, "budget": rp.budget})
    all_warnings: List[str] = []

    # 2) 意图 + 查询规划
    import plan

    intent = plan.classify_intent(query)
    leaves = plan.plan_queries(
        query, intent, width_cap=rp.max_sources if rp.tier in ("L2", "L3") else 1
    )
    tr.event("plan", {"intent": intent, "leaves": [lv["q"] for lv in leaves]})

    # 3) 取源（路径B：外部 docs 喂入则跳过取源与补抓，直进质量层）
    external = bool(docs)
    if external:
        docs = _prepare_external_docs(docs, cfg, tr)
    else:
        docs, warns = _gather_internal_docs(query, leaves, rp, constraints, cfg, tr, inject)
        all_warnings.extend(warns)
        # 干净源预灌：web_fetch 未显式注入且 clean_sources 开启时，扇出零 key 干净源并入质量层；
        # 显式 web_fetch= 由调用方接管（调用方注入契约不变），此处不重复叠加。
        if web_fetch is None and _clean_sources_active(cfg):
            try:
                from clean_sources import build_clean_fetch

                provider = build_clean_fetch(cfg)
                clean_docs = provider(query)
                if clean_docs:
                    docs = docs + clean_docs
                    tr.event(
                        "clean_sources",
                        {
                            "n": len(clean_docs),
                            "engines": sorted({d.get("engine") for d in clean_docs}),
                        },
                    )
            except Exception as _e:
                tr.event("clean_sources", {"error": str(_e)[:200]})
                all_warnings.append(
                    f"干净源供给失败（已跳过，不影响主检索）：{str(_e)[:160]}"
                )  # 默认配置可观测（D5）
    docs = _merge_prior_evidence(docs, prior_evidence, tr)

    # 4) 去重 + 打分
    import dedup

    dd_thr = _dedup_threshold(cfg, external)
    docs = dedup.near_dup(docs, threshold=dd_thr)
    tr.event("dedup", {"n_docs": len(docs), "threshold": dd_thr, "external": external})
    scores = _score_all(docs, query, cfg, freshness=rp.freshness)

    # 5) 自适应补抓 + 停止判据
    import stop

    exp, warns = _expand_if_needed(
        docs, scores, query, rp, constraints, cfg, external, dd_thr, inject
    )
    all_warnings.extend(warns)
    docs, scores = exp.docs, exp.scores
    stop_decision = stop.should_stop(
        rp.tier,
        exp.prev_rounds,
        exp.new_batch,
        budget_hit=exp.budget_hit,
        coverage_closed=(len(docs) >= rp.max_sources),
    )
    exhausted = exp.exhausted or stop_decision.get("exhausted", False)
    tr.event("stop", stop_decision)

    # 5.5) 语义 rerank（opt-in，默认关；离线/无向量时自动降级 lexical 基线，不触评分/置信度契约）
    import rerank as _rerank

    docs, scores = _rerank.rerank(docs, scores, query, cfg, tr=tr)

    # 6) 截断 → 汇总 → 校验
    docs, scores = _truncate_to_cap(docs, scores, rp.max_sources)
    summary = _summarize(docs, scores, query, schema, cfg, external)
    token_used = _estimate_tokens(
        summary["findings"] + " " + " ".join(d.get("snippet", "") for d in docs)
    )
    tr.event(
        "done",
        {"confidence": summary["confidence"], "token_used": token_used, "exhausted": exhausted},
    )

    return {
        "findings": summary["findings"],
        "sources": docs,
        "scores": scores,
        "confidence": summary["confidence"],
        "token_used": token_used,
        "exhausted": exhausted,
        "tier_used": rp.tier,
        "trace": tr.snapshot(),
        "verify_issues": summary["verify_issues"],
        "fact_verdicts": summary["fact_verdicts"],
        "uncertainties": summary["uncertainties"],
        "warnings": all_warnings,
    }
