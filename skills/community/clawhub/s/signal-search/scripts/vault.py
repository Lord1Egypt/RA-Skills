"""scripts/vault.py - Research Vault 收集层（markdown 留存 + 可重跑 + HITL）。

A1/A2/A3/A4/A5。正文 markdown + frontmatter 机器字段；`.state.json` 仅游标/去重集，
保持金库对人对干净。零硬依赖：frontmatter 用 YAML 解析（若环境有），否则极简降级。

调用方经 `research(vault_dir=...)` 触发落盘；显式 `vault_dir=None` 关闭（回到纯内存）。
"""

import datetime
import hashlib
import json
import os
from typing import Any, Dict, List

try:
    import yaml  # 可选：更稳的 frontmatter 解析

    _HAS_YAML = True
except Exception:  # pragma: no cover - 更轻路径
    _HAS_YAML = False


def slug(text: str) -> str:
    """任意字符串 -> 10 位 hash slug（避免中文/特殊字符做目录名）。"""
    return hashlib.sha1((text or "").encode("utf-8")).hexdigest()[:10]


# ---- frontmatter（正文与机器字段的分界）----
def _fm_dump(meta: Dict[str, Any]) -> str:
    if _HAS_YAML:
        body = yaml.safe_dump(meta, allow_unicode=True, sort_keys=False)
        return f"---\n{body}---\n"
    lines = "\n".join(f"{k}: {v}" for k, v in meta.items())
    return f"---\n{lines}\n---\n"


def _now() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")


def _write(p: str, rel: str, content: str) -> None:
    with open(os.path.join(p, rel), "w", encoding="utf-8") as f:
        f.write(content)


def vault_path(vault_dir: str, query: str) -> str:
    return os.path.join(vault_dir, slug(query))


def init_vault(vault_dir: str, query: str, tier: str) -> str:
    p = vault_path(vault_dir, query)
    os.makedirs(os.path.join(p, "items"), exist_ok=True)
    return p


def write_index(p: str, query: str, tier: str) -> None:
    fm = {"created": _now(), "updated": _now(), "tier": tier, "query": query, "hash": slug(query)}
    body = (
        f"# Research Vault: {query}\n\n"
        f"> 状态: 收集中 | 档位: {tier}\n\n"
        f"本目录为 Signal-Search Research Vault（markdown 留存，可重跑）。\n"
        f"- `outline.md` 研究大纲（可验证清单，STORM 多视角）\n"
        f"- `items/` 原子证据笔记（frontmatter 承载机器字段）\n"
        f"- `report.md` 终稿（从 items 幂等重生成）\n"
        f"- `.state.json` 机器游标/去重集（人无需读）\n"
    )
    _write(p, "INDEX.md", _fm_dump(fm) + body)


def write_outline(p: str, query: str, schema: List[Dict[str, Any]], tier: str) -> None:
    """A2 STORM 多视角 + RhinoInsight 可验证清单（启发式，零 LLM；agent_fn 可增强）。"""
    perspectives = ["Domain Expert", "Skeptic", "Practitioner", "Newcomer", "Adjacent"]
    lines = [
        f"# 研究大纲: {query}\n",
        f"> 档位: {tier} | STORM 视角: {', '.join(perspectives)}\n",
        "\n## 盲点探测（多视角互问）\n",
    ]
    for pv in perspectives:
        lines.append(f"- **{pv} 视角**：关于「{query}」，最关键未明子问题是？（dispatch 后回填）\n")
    lines.append("\n## 可验证清单（子目标 + 验收标准）\n")
    if not schema:
        lines.append("- [ ] **综合检索** — 验收: 已获 ≥1 可信来源支撑主问题结论\n")
    for i, dim in enumerate(schema or [], 1):
        name = dim.get("name", f"维度{i}")
        lines.append(f"{i}. [ ] **{name}** — 验收: 已获 ≥1 可信来源支撑该维度结论\n")
    _write(p, "outline.md", "\n".join(lines) + "\n")


def write_item(p: str, idx: int, query: str, source: Dict[str, Any], detail: str = "") -> None:
    """写 items/<nn>-<slug>.md：frontmatter(status/sources/queries/confidence) + 正文。"""
    nn = f"{idx:02d}"
    url = source.get("url", "")
    meta = {
        "status": "done",
        "url": url,
        "queries": [query],
        "confidence": source.get("confidence", "中"),
        "source_type": source.get("source_type", "web"),
    }
    body = f"# 证据 {nn}\n\n"
    if detail:
        body += detail + "\n\n"
    elif source.get("text"):
        body += source["text"][:4000] + "\n\n"
    if url:
        body += f"来源: {url}\n"
    _write(p, os.path.join("items", f"{nn}-{slug(url or query)}.md"), _fm_dump(meta) + body)


def render_report(p: str, sources: List[Dict[str, Any]] = None, incremental: bool = False) -> str:
    """从 items 幂等重生成 report.md（重跑不产生重复内容）。

    D5：vault 开启时末尾追加「## 引用」区，列出所有来源 URL（可复制）。
    T7：incremental=True 且 report.md 已存在时，仅追加未含的新 items（避免超长研究全量重读）。
    """
    import re as _re

    items_dir = os.path.join(p, "items")
    existing: set = set()
    if incremental and os.path.isfile(os.path.join(p, "report.md")):
        with open(os.path.join(p, "report.md"), encoding="utf-8") as f:
            cur = f.read()
        for m in _re.findall(r"^## (\S+\.md)", cur, _re.M):
            existing.add(m)
        cur_no_cit = _re.split(r"\n## 引用\n", cur)[0].rstrip() + "\n"
        parts = [cur_no_cit]
    else:
        parts = ["# 研究报告\n"]
    if os.path.isdir(items_dir):
        for fn in sorted(os.listdir(items_dir)):
            if not fn.endswith(".md"):
                continue
            if incremental and fn in existing:
                continue
            with open(os.path.join(items_dir, fn), encoding="utf-8") as f:
                txt = f.read()
            end = txt.find("\n---", 3)
            body = txt[end + 4 :].strip() if end != -1 else txt
            parts.append(f"## {fn}\n\n{body}\n")
    parts.append(_citation_md(sources))
    report = "\n".join(parts).rstrip() + "\n"
    _write(p, "report.md", report)
    return report


# ---- D5 引用导出（纯文本轻量；纯 web 源退化为 URL 引用，结构化citation优先）----
def _dedup_sources(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    out: List[Dict[str, Any]] = []
    for s in sources or []:
        u = s.get("url")
        if not u or u in seen:
            continue
        seen.add(u)
        out.append(s)
    return out


def _citation_md(sources: List[Dict[str, Any]]) -> str:
    items = _dedup_sources(sources)
    if not items:
        return ""
    lines = ["\n## 引用\n"]
    for i, s in enumerate(items, 1):
        title = s.get("title") or s.get("snippet") or s.get("url")
        lines.append(f"{i}. [{title}]({s['url']})")
    return "\n".join(lines) + "\n"


def _citation_bibtex(sources: List[Dict[str, Any]]) -> str:
    items = _dedup_sources(sources)
    if not items:
        return ""
    blocks = []
    for i, s in enumerate(items, 1):
        url = s["url"]
        title = s.get("title") or s.get("snippet") or url
        cit = s.get("citation")
        key = (cit or {}).get("key") if isinstance(cit, dict) else None
        key = key or f"src{i}"
        if isinstance(cit, dict) and cit.get("doi"):
            author = cit.get("authors", "unknown")
            year = cit.get("year", "n.d.")
            blocks.append(
                f"@article{{{key},\n  title = {{{title}}},\n  author = {{{author}}},\n"
                f"  year = {{{year}}},\n  doi = {{{cit['doi']}}},\n  url = {{{url}}}\n}}"
            )
        else:
            # 无 DOI：退化为 @misc，但优先把结构化 citation 字段（股票代码/repo）写入 note
            note = s.get("source_type", "web")
            if isinstance(cit, dict):
                _nf = [f"{k}={cit[k]}" for k in ("stock_code", "repo", "source") if cit.get(k)]
                if _nf:
                    note = "; ".join(_nf)
            blocks.append(
                f"@misc{{{key},\n  title = {{{title}}},\n"
                f"  howpublished = {{{url}}},\n"
                f"  note = {{{note}}}\n}}"
            )
    return "\n".join(blocks).rstrip() + "\n"


def write_citations(p: str, sources: List[Dict[str, Any]], fmt: str = "bibtex") -> str:
    """T6 引用导出扩展：bibtex / md / ris / csl / noteexpress，写对应文件到 vault，返回路径。"""
    fmt = (fmt or "bibtex").lower()
    if fmt == "md":
        content, fn = _citation_md(sources), "references.md"
    elif fmt == "ris":
        content, fn = _citation_ris(sources), "references.ris"
    elif fmt == "csl":
        content, fn = _citation_csl(sources), "references.csl"
    elif fmt == "noteexpress":
        content, fn = _citation_noteexpress(sources), "references.ne"
    else:
        content, fn = _citation_bibtex(sources), "citations.bib"
    _write(p, fn, content)
    return os.path.join(p, fn)


def _citation_ris(sources: List[Dict[str, Any]]) -> str:
    items = _dedup_sources(sources)
    if not items:
        return ""
    blocks = []
    for s in items:
        title = s.get("title") or s.get("snippet") or s.get("url")
        blocks.append(f"TY  - GEN\nTI  - {title}\nUR  - {s['url']}\nER  - ")
    return "\n".join(blocks).rstrip() + "\n"


def _citation_csl(sources: List[Dict[str, Any]]) -> str:
    items = _dedup_sources(sources)
    return json.dumps(
        [
            {"title": s.get("title") or s.get("snippet") or s.get("url"), "URL": s.get("url")}
            for s in items
        ],
        ensure_ascii=False,
        indent=2,
    )


def _citation_noteexpress(sources: List[Dict[str, Any]]) -> str:
    items = _dedup_sources(sources)
    if not items:
        return ""
    blocks = []
    for i, s in enumerate(items, 1):
        title = s.get("title") or s.get("snippet") or s.get("url")
        blocks.append(f"#:@文献[{i}]\n标题={title}\nURL={s['url']}")
    return "\n".join(blocks).rstrip() + "\n"


def load_state(p: str) -> Dict[str, Any]:
    sp = os.path.join(p, ".state.json")
    if os.path.isfile(sp):
        try:
            with open(sp, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_state(p: str, state: Dict[str, Any]) -> None:
    with open(os.path.join(p, ".state.json"), "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
