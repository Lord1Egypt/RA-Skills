"""scripts/verify.py - 验证护栏 VERITAS + 事实级核验(M51)（§5.13 / §5.23）。"""

import re
from typing import Any, Dict, List, Optional, Tuple

from common import load_config

URL_RE = re.compile(r"https?://[^\s)\"'\uff08\uff09]+")
# 锚定用全部 token（含通用词，用于重叠计数与回退）
KW_RE = re.compile(r"[\d]{2,}|[A-Za-z\u4e00-\u9fa5]{2,}")
# 关键实体：数字/百分比、全大写缩写(≥2)、英文词(≥3)。中文无分词，整句会被当作一个词，
# 故不把 CJK 纳入"关键实体"（纯中文事实回退到 token 重叠判据），仅以数字/英文实体做精确锚定。
KEY_RE = re.compile(r"\d+(?:\.\d+)?%?|[A-Z]{2,}|[A-Za-z]{3,}")
# 否定/极性词（用于事实与来源极性一致性校验，避免"不支持X"误锚"支持X"）
NEG_RE = re.compile(r"(不|无|非|没有|相反|并非|未|否|缺乏|缺少|拒绝|反对)")


def _kw(text: str) -> set:
    """抽取全部 token 词集（重叠计数用）。"""
    return set(KW_RE.findall(text or ""))


def _key_entities(text: str) -> set:
    """抽取事实锚定的关键实体（数字/专名）。零依赖启发式：数字、长词、缩写。"""
    return set(KEY_RE.findall(text or ""))


def _polarity(text: str) -> bool:
    """含否定/极性词则返回 True。用于事实↔来源极性一致性判定。"""
    return bool(NEG_RE.search(text or ""))


def _source_ctx(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """每个来源只做一次正文取值与分词，供所有事实复用（避免 fact×source 重复正则扫描）。
    预计算 kw(全部 token) / keys(关键实体) / neg(极性) / text(原文)，热路径不再重复扫描。
    """
    ctx = []
    for s in sources or []:
        text = s.get("text") or s.get("snippet") or ""
        if not text:
            continue
        ctx.append(
            {
                "url": s.get("url"),
                "text": text,
                "kw": _kw(text),
                "keys": _key_entities(text),
                "neg": _polarity(text),
                "vec": None,
                "vec_done": False,
            }
        )
    return ctx


def _claim_text(findings: str) -> str:
    """去掉非论断区块(来源/置信度/未确认项)与 synthesize 生成的元数据行(维度标题/占位),
    仅校验答案论断, 避免把引用列表/维度标题当事实核验。"""
    txt = findings or ""
    for marker in ("来源：", "未确认项：", "置信度："):
        idx = txt.find(marker)
        if idx != -1:
            txt = txt[:idx]
    # 剥离 synthesize 生成的元数据行: markdown 标题(## 维度名) 与 占位行
    _META = re.compile(
        r"^\s*#{1,6}\s.*$"
        r"|^（该维度暂无直接来源）$"
        r"|^（无来源）$"
        r"|^（信息不确定）$"
        r"|^（未检索到可用来源，结论待核实）$"
        r"|^（综合来源见首节；本维度按此框架组织结论）$",
        re.M,
    )
    txt = _META.sub("", txt)
    return txt


def verify(sources: List[Dict[str, Any]], findings: str) -> List[Dict[str, Any]]:
    """引文真实：findings 中每个 URL 必须 ∈ sources；未抓取的一律标待核实/剔除。"""
    issues = []
    src_urls = {s.get("url") for s in sources if s.get("url")}
    cited = set(URL_RE.findall(findings or ""))
    for u in cited:
        if u not in src_urls:
            issues.append({"type": "citation_not_fetched", "url": u, "action": "标待核实/剔除"})
    return issues


def fact_level_verify(
    findings: str, sources: List[Dict[str, Any]], cfg: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """拆原子事实 → 逐条锚定到具体来源 → verdict(TRUE/UNCERTAIN)。

    零依赖加固（P0-1，堵住"共享≥1词即 TRUE"的假 TRUE）：
      1) 关键实体精确锚定：事实含数字/英文实体时，要求最佳来源覆盖足够比例(verify.coverage_threshold)
         且「全部数字实体必须在来源中出现」(防 300万 vs 427万 错配)，否则 UNCERTAIN。
      2) 极性一致：事实含否定词时，锚定来源极性须一致，否则 UNCERTAIN(polarity_mismatch)，
         避免"不支持X"误锚到"支持X"。
      3) 纯中文事实(无数字/英文实体)：回退到原 token 重叠判据(保守，避免假 TRUE)。
    无可靠锚定一律 UNCERTAIN（不轻判 FALSE，留待人工/强模型/语义后端）。
    语义后端可用时由 semantic_fact_verify 走 Bi-Encoder 增强，本函数作为零依赖基线与其回退。
    """
    _cfg = cfg or load_config()
    vcfg = (_cfg.get("verify") or {}) if isinstance(_cfg, dict) else {}
    coverage_thr = vcfg.get("coverage_threshold", 0.5)

    sents = re.split(r"[。！？;；\n]", _claim_text(findings))
    facts = [s.strip() for s in sents if len(s.strip()) > 4]
    src_ctx = _source_ctx(sources)  # 来源分词/实体/极性预计算一次
    results = []
    for f in facts:
        fkw = _kw(f)
        if not fkw:
            results.append(
                {
                    "fact": f[:160],
                    "verdict": "UNCERTAIN",
                    "source": None,
                    "score": 0.0,
                    "reason": "no_overlap_source",
                }
            )
            continue
        fkeys = _key_entities(f)  # 数字/英文实体（可靠）
        fnums = {k for k in fkeys if re.search(r"\d", k)}  # 数字实体最可证伪
        fneg = _polarity(f)
        # 选最佳来源：(关键实体覆盖率, 原始 token 重叠) 字典序
        best = None  # (cov, raw, url, neg, keys)
        for sc in src_ctx:
            cov = (len(fkeys & sc["keys"]) / len(fkeys)) if fkeys else 0.0
            raw = len(fkw & sc["kw"])
            cand = (cov, raw, sc["url"], sc["neg"], sc["keys"])
            if best is None or (cov, raw) > (best[0], best[1]):
                best = cand
        if best is None:
            # 全部来源都无可用正文（text/snippet 缺失）→ 无法锚定，保守判 UNCERTAIN
            results.append(
                {
                    "fact": f[:160],
                    "verdict": "UNCERTAIN",
                    "source": None,
                    "score": 0.0,
                    "reason": "no_source_text",
                }
            )
            continue
        cov, raw, url, sneg, best_keys = best
        if fneg != sneg:
            results.append(
                {
                    "fact": f[:160],
                    "verdict": "UNCERTAIN",
                    "source": None,
                    "score": round(cov, 3),
                    "reason": "polarity_mismatch",
                }
            )
        elif fnums and not (fnums <= best_keys):
            # 数字实体未全部出现在来源 → 疑似数字错配，保守不锚定
            results.append(
                {
                    "fact": f[:160],
                    "verdict": "UNCERTAIN",
                    "source": None,
                    "score": round(cov, 3),
                    "reason": "numeric_mismatch",
                }
            )
        elif fkeys:
            if cov >= coverage_thr and raw >= 1:
                results.append(
                    {
                        "fact": f[:160],
                        "verdict": "TRUE",
                        "source": url,
                        "score": round(cov, 3),
                        "reason": "source_anchor",
                    }
                )
            else:
                results.append(
                    {
                        "fact": f[:160],
                        "verdict": "UNCERTAIN",
                        "source": None,
                        "score": round(cov, 3),
                        "reason": "low_coverage" if cov < coverage_thr else "weak_anchor",
                    }
                )
        else:
            # 纯中文无数字/英文实体：回退原 token 重叠判据（保守，避免假 TRUE）
            if raw >= 1:
                results.append(
                    {
                        "fact": f[:160],
                        "verdict": "TRUE",
                        "source": url,
                        "score": round(cov, 3),
                        "reason": "source_overlap",
                    }
                )
            else:
                results.append(
                    {
                        "fact": f[:160],
                        "verdict": "UNCERTAIN",
                        "source": None,
                        "score": round(cov, 3),
                        "reason": "weak_anchor",
                    }
                )
    return results


def _semantic_backend_available() -> bool:
    """语义后端（sentence-transformers）是否可用；不可用时调用方回退关键词基线。"""
    try:
        from embed import _TRY_ST  # noqa: F401

        return _TRY_ST
    except Exception:
        return False


def _split_facts(findings: str) -> List[str]:
    """论断文本拆原子事实：去元数据后按句切分，过滤过短片段。"""
    sents = re.split(r"[。！？;；\n]", _claim_text(findings))
    return [s.strip() for s in sents if len(s.strip()) > 4]


def _embed_one(text: str, embed_fn) -> Optional[List[float]]:
    """惰性向量化单段文本；失败返回 None（不抛，交由上层降级）。"""
    try:
        _v = embed_fn([text])
        return _v[0] if _v else None
    except Exception:
        return None


def _score_fact(
    f: str, fkw: set, src_ctx: List[Dict[str, Any]], threshold: float, embed_fn, sim_fn
) -> Tuple[str, Optional[str], float, str]:
    """单条事实 × 多来源：关键词预筛 + 语义相似终判。

    返回 (verdict, source, score, reason)。事实向量仅惰性计算一次；来源向量逐源惰性计算并
    缓存于 src_ctx（facts×sources 的向量化降为 facts+sources）。相似度 ≥ 阈值 → TRUE 锚定来源 URL，
    否则 UNCERTAIN（不轻判 FALSE）。
    """
    best_url, best_sim = None, 0.0
    fvec = None
    for sc in src_ctx:
        if not (fkw & sc["kw"]):  # 关键词预筛：无交集跳过语义计算
            continue
        if fvec is None:
            fvec = _embed_one(f, embed_fn)
        if fvec is None:
            break  # 事实侧向量化失败 → 本事实无法语义判定
        if not sc["vec_done"]:
            sc["vec_done"] = True
            sc["vec"] = _embed_one(sc["text"], embed_fn)
        if sc["vec"] is None:
            continue
        try:
            sim = sim_fn(fvec, sc["vec"])
        except Exception:
            sim = 0.0
        if sim > best_sim:
            best_sim = sim
            best_url = sc["url"]
    if best_sim >= threshold and best_url:
        return "TRUE", best_url, round(best_sim, 3), "source_overlap"
    return "UNCERTAIN", None, round(best_sim, 3), "weak_anchor"


def semantic_fact_verify(
    findings: str,
    sources: List[Dict[str, Any]],
    cfg: Dict[str, Any] = None,
    threshold: float = None,
) -> List[Dict[str, Any]]:
    """M51 语义核验（增强版）：关键词预筛 → Bi-Encoder 语义相似终判（中文友好）。

    每条原子事实先与每个 source 做关键词重叠预筛（廉价、省算力）；预筛命中者再经
    embed.embed 向量化 + embed.similarity 余弦相似度终判。相似度 ≥ 阈值 → TRUE 并锚定该来源
    URL；否则 UNCERTAIN（不轻判 FALSE）。无 sentence-transformers 时 embed 降级为关键词向量，
    语义路径退化为弱语义，此时建议回退 fact_level_verify（由调用方按 config 决定）。

    gating：由 config.verify.semantic 控制是否调用本函数；本函数本身不依赖重依赖即可运行
    （缺失时自动回退 fact_level_verify），故可安全置于热路径之外。
    """
    # 无可用语义后端 → 回退关键词基线，避免假"语义"
    if not _semantic_backend_available():
        return fact_level_verify(findings, sources)

    cfg = cfg or {}
    if threshold is None:
        threshold = (cfg.get("verify") or {}).get("semantic_threshold", 0.55)

    facts = _split_facts(findings)
    # 来源正文的分词与向量各只算一次（原实现对每个事实重复向量化同一来源，
    # 向量化次数从 facts×sources 降为 facts+sources；Bi-Encoder 逐句独立编码，等价）
    src_ctx = _source_ctx(sources)
    from embed import embed, similarity  # 调用时取最新（含 monkeypatch 覆盖）

    results = []
    for f in facts:
        fkw = _kw(f)
        if not fkw:
            results.append(
                {
                    "fact": f[:160],
                    "verdict": "UNCERTAIN",
                    "source": None,
                    "score": 0.0,
                    "reason": "no_overlap_source",
                }
            )
            continue
        verdict, source, score, reason = _score_fact(f, fkw, src_ctx, threshold, embed, similarity)
        results.append(
            {
                "fact": f[:160],
                "verdict": verdict,
                "source": source,
                "score": score,
                "reason": reason,
            }
        )
    return results


def aggregate_uncertainties(
    verdicts: List[Dict[str, Any]], docs: List[Dict[str, Any]] = None
) -> List[Dict[str, Any]]:
    """聚合 UNCERTAIN 事实为顶层 uncertainties 列表(B)。
    reason: no_overlap_source(无来源命中) / weak_anchor(弱锚定) / cross_source_conflict(跨源冲突)。
    """
    _NEG = re.compile(r"(不|无|非|没有|相反|并非|未|否)")
    by_fact = {}
    for v in verdicts:
        if v.get("verdict") == "UNCERTAIN":
            by_fact[v.get("fact", "")] = v.get("reason", "weak_anchor")
    # 跨源冲突: 同一事实被不同来源以相反极性支撑
    conflict_facts = set()
    if docs:
        url_snip = {d.get("url"): (d.get("snippet") or d.get("text") or "") for d in docs}
        pos, neg = {}, {}
        for v in verdicts:
            if v.get("verdict") == "TRUE" and v.get("source"):
                sn = url_snip.get(v["source"], "")
                (neg if _NEG.search(sn) else pos).setdefault(v.get("fact", ""), []).append(
                    v["source"]
                )
        conflict_facts = set(pos) & set(neg)
    out = []
    seen = set()
    for f, reason in by_fact.items():
        r = "cross_source_conflict" if f in conflict_facts else reason
        out.append({"fact": f[:160], "source": None, "reason": r})
        seen.add(f)
    # 跨源冲突但事实本身被 TRUE 支撑(仍须提示矛盾)
    for f in conflict_facts:
        if f in seen:
            continue
        out.append({"fact": f[:160], "source": None, "reason": "cross_source_conflict"})
    return out
