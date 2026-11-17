"""scripts/report.py - 汇总（§5.12）。"""

import re
from typing import Any, Dict, List


def synthesize(
    sources: List[Dict[str, Any]],
    scores: List[Dict[str, Any]],
    query: str,
    schema: List[Dict[str, Any]] = None,
    uncertainties: List[Dict[str, Any]] = None,
    verdicts: List[Dict[str, Any]] = None,
    citation_real_rate: float = None,
    n_uncertain: int = 0,
) -> str:
    """先答后源、按主题聚、冲突显式标注、给置信度；跳 uncertain/None。
    schema: 维度化输出(A) — 按维度分段, detail_level 控制每维深度; 不传则扁平(向后兼容)。
    uncertainties: B 顶层槽 — 末尾附"未确认项"小节。
    """
    if not sources:
        base = "（未检索到可用来源，结论待核实）"
        if schema:
            base = "\n".join(
                f"## {d['name']}（{d.get('detail_level', '简要')}）\n（无来源）" for d in schema
            )
        if uncertainties:
            base += _uncertain_section(uncertainties)
        return base
    paired = sorted(
        zip(sources, scores),
        key=lambda x: x[1].get("rerank_score", x[1].get("weighted", 0)),
        reverse=True,
    )
    top_src, top_score = paired[0]
    snippet = (top_src.get("snippet") or "").strip()
    if snippet.lower() in ("uncertain", "none", "待定", ""):
        snippet = "（信息不确定）"
    # 编号引用（M31）：来源按出现顺序编号，供行内 [n] 与末尾列表共用
    refs = []
    src_index = {}
    for i, s in enumerate(sources, 1):
        u = s.get("url")
        if u and u.lower() not in ("uncertain", "none"):
            refs.append(u)
            src_index[u] = i
    if schema:
        findings = _schema_layout(schema, sources, scores, src_index)
    else:
        findings = f"先答：{snippet[:300]}"
        top_idx = src_index.get(top_src.get("url"))
        if top_idx:
            findings += f" [{top_idx}]"
        findings += "\n"
        # 冲突标注：最低加权分与最高差距大则标相反观点（优先 rerank_score）
        if len(paired) > 1:
            low_src, low_score = paired[-1]
            _top = top_score.get("rerank_score", top_score.get("weighted", 0))
            _low = low_score.get("rerank_score", low_score.get("weighted", 0))
            if _low < _top * 0.6:
                low_snip = (low_src.get("snippet") or "")[:120]
                low_idx = src_index.get(low_src.get("url"))
                findings += (
                    f"\n相反观点（低可信源）{('[' + str(low_idx) + ']') if low_idx else ''}"
                    f"：{low_snip}\n"
                )
    if refs:
        findings += "\n来源：\n" + "\n".join(f"[{i}] {r}" for i, r in enumerate(refs, 1))
    findings += f"\n\n置信度：{confidence_of(scores, verdicts, citation_real_rate, n_uncertain)}"
    return append_uncertainties(findings, uncertainties)


def confidence_of(
    scores: List[Dict[str, Any]],
    verdicts: List[Dict[str, Any]] = None,
    citation_real_rate: float = None,
    n_uncertain: int = 0,
) -> float:
    """整体置信度（答案正确性合成，P0-2）。

    旧口径（仅 scores）→ 来源打分均值，度量的是"来源看起来多靠谱"，与答案正确性无关。
    新口径融合三信号：
      - M51 TRUE 率：事实被来源锚定的比例（锚定越多越可信，抬升置信度）；
      - 引文真实率：findings 中引用的 URL 真实存在于 sources 的比例（假引用拉低）；
      - 矛盾/不确定性：极性/数字矛盾、未确认项越多越降权。
    向后兼容：verdicts/citation_real_rate 缺省时回退旧均值，不破坏既有调用方。
    """
    if not scores:
        return 0.0
    mean_w = sum(s.get("weighted", 0) for s in scores) / len(scores)

    base = mean_w
    if verdicts:
        n = len(verdicts)
        n_true = sum(1 for v in verdicts if v.get("verdict") == "TRUE")
        n_contra = sum(
            1 for v in verdicts if v.get("reason") in ("polarity_mismatch", "numeric_mismatch")
        )
        if n_true:
            # 锚定事实抬升置信度（有来源支撑 → 高置信）
            base = max(base, 0.5 + 0.45 * (n_true / n))
        if n_contra:
            # 来源与事实矛盾 → 强降权
            base = base * max(0.3, 1.0 - 0.4 * (n_contra / n))
    if citation_real_rate is not None:
        base = base * max(0.0, min(1.0, citation_real_rate))
    if n_uncertain and n_uncertain > 0:
        base = base * max(0.5, 1.0 - 0.1 * n_uncertain)
    return round(max(0.0, min(1.0, base)), 3)


def append_uncertainties(findings: str, uncertainties: List[Dict[str, Any]] = None) -> str:
    """在已生成的正文末尾追加"未确认项"小节。

    uncertainties 只影响末尾追加，因此上层拿到 uncertainties 后无需重跑 synthesize。
    """
    if not uncertainties:
        return findings
    return findings + _uncertain_section(uncertainties)


def _cap(detail_level: str) -> int:
    return {"极简": 60, "简要": 120, "详细": 300}.get(detail_level, 120)


def _tokens(name: str) -> List[str]:
    """维度名 → 匹配 token（中文长词拆 2-gram，提升来源↔维度命中率）。"""
    toks = re.findall(r"[\u4e00-\u9fa5]{2,}|[A-Za-z]{2,}", name or "")
    grams = []
    for t in toks:
        if re.search(r"[\u4e00-\u9fa5]", t) and len(t) > 2:
            grams += [t[i : i + 2] for i in range(len(t) - 1)]
        else:
            grams.append(t)
    return grams or [name or ""]


def _schema_layout(schema, sources, scores, src_index=None) -> str:
    src_index = src_index or {}
    out = []
    ranked = sorted(
        zip(sources, scores),
        key=lambda x: x[1].get("rerank_score", x[1].get("weighted", 0)),
        reverse=True,
    )
    # 维度 token 与来源正文各只算一次：原实现在"预检 + 主循环"的双层遍历里
    # 对每个来源都重跑一次分词正则与文本拼接，复杂度 O(维度×来源) 次正则。
    dim_tokens = [_tokens(d["name"]) for d in schema]
    texts = [(s, (s.get("text") or s.get("snippet") or "")) for s, _ in ranked]
    dim_matched = [[s for s, txt in texts if any(g in txt for g in toks)] for toks in dim_tokens]
    # 预检: 是否有任一维度匹配到专属来源(外部/web_fetch 多语 docs 常全不匹配)
    any_matched = any(dim_matched)
    shown_comprehensive = False
    for idx, d in enumerate(schema):
        name, lvl = d["name"], d.get("detail_level", "简要")
        cap = _cap(lvl)
        matched = dim_matched[idx]
        if matched:
            body = ""
            for s in matched[:2]:
                sn = (s.get("snippet") or "")[:cap]
                if sn:
                    n = src_index.get(s.get("url"))
                    body += f"- {sn}{(' [' + str(n) + ']') if n else ''}\n"
            out.append(f"## {name}（{lvl}）\n{body}")
        elif not any_matched:
            # 外部/多语 docs: 维度无法细分, 仅首维度放综合来源, 其余指引(避免空壳/重复)
            if not shown_comprehensive:
                body = ""
                for s, _ in ranked[:3]:
                    sn = (s.get("snippet") or "")[:cap]
                    if sn:
                        n = src_index.get(s.get("url"))
                        body += f"- {sn}{(' [' + str(n) + ']') if n else ''}\n"
                out.append(f"## {name}（{lvl}）\n{body}")
                shown_comprehensive = True
            else:
                out.append(f"## {name}（{lvl}）\n（综合来源见首节；本维度按此框架组织结论）\n")
        else:
            out.append(f"## {name}（{lvl}）\n（该维度暂无直接来源）\n")
    return "\n".join(out)


def _uncertain_section(uncertainties) -> str:
    if not uncertainties:
        return ""
    lines = ["\n未确认项："]
    for u in uncertainties[:8]:
        lines.append(f"- {u.get('fact', '')[:120]}（{u.get('reason', '')}）")
    return "\n".join(lines)
