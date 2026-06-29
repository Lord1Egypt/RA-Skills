#!/usr/bin/env python3
"""
render_markdown.py — Stage 5 (Markdown variant)

Consumes summary.json + meta.json and produces a self-contained Markdown
report mirroring the HTML version. Optimised for GitHub / Feishu /
Notion / Obsidian rendering: native ```mermaid``` fenced blocks, compact
tables, no over-bullet'd structures.

USAGE
    python3 scripts/render_markdown.py <summary.json>
        --meta_json <meta.json>
        [--file_count <int>]
        > report.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# meta helpers (tolerant to both flat and nested github_meta schemas)
# ---------------------------------------------------------------------------

def _meta_get(meta: dict, *keys: str, default: Any = None) -> Any:
    """Look up a key in meta, falling back to meta['github_meta']."""
    for k in keys:
        if k in meta and meta[k] not in (None, ""):
            return meta[k]
    gm = meta.get("github_meta") or {}
    for k in keys:
        if k in gm and gm[k] not in (None, ""):
            return gm[k]
    return default


def _repo_url(meta: dict) -> str:
    url = meta.get("repo_url")
    if url:
        return url
    owner = meta.get("owner")
    repo = meta.get("repo")
    if owner and repo:
        return f"https://github.com/{owner}/{repo}"
    return ""


def _ref(meta: dict) -> str:
    """Best ref to anchor permalinks: commit_sha → branch → default_branch → HEAD."""
    for k in ("commit_sha", "sha"):
        v = meta.get(k)
        if v:
            return v
    for k in ("branch", "default_branch"):
        v = _meta_get(meta, k)
        if v:
            return v
    return "HEAD"


def _gh_blob_url(meta: dict, evidence: str) -> str | None:
    """Convert `path:line` into a github.com permalink anchored at the commit SHA."""
    if not evidence or ":" not in evidence:
        return None
    owner = meta.get("owner")
    repo = meta.get("repo")
    if not owner or not repo:
        return None
    ref = _ref(meta)
    path, _, line = evidence.partition(":")
    line = line.strip()
    if not line.isdigit():
        digits = "".join(c if c.isdigit() else " " for c in line).split()
        if not digits:
            return f"https://github.com/{owner}/{repo}/blob/{ref}/{path}"
        line = digits[0]
    return f"https://github.com/{owner}/{repo}/blob/{ref}/{path}#L{line}"


def _gh_path_url(meta: dict, path: str) -> str | None:
    """Convert a bare repo path (file or directory) into a github.com URL.

    Directories (trailing `/` or no dot in basename) → `/tree/<ref>/<path>`.
    Files → `/blob/<ref>/<path>`. Lets every code-path mention in the report
    become a one-click jump to GitHub.
    """
    if not path:
        return None
    owner = meta.get("owner")
    repo = meta.get("repo")
    if not owner or not repo:
        return None
    ref = _ref(meta)
    clean = path.strip().rstrip("/")
    if not clean:
        return None
    is_dir = path.rstrip().endswith("/") or "." not in clean.rsplit("/", 1)[-1]
    kind = "tree" if is_dir else "blob"
    return f"https://github.com/{owner}/{repo}/{kind}/{ref}/{clean}"


def _path_link(meta: dict, path: str) -> str:
    """Render a code path as a bare-text link `[path](url)`.

    NOTE: we deliberately do NOT wrap the visible text in backticks.
    Rationale — some renderers (Feishu, certain Notion blocks) handle
    inline-code-inside-link inconsistently: sometimes they strip the
    backticks, sometimes they break the link entirely, sometimes they
    display the FULL URL as the visible text. Plain text inside the link
    renders identically everywhere and stays cleanly clickable.
    """
    if not path:
        return "—"
    url = _gh_path_url(meta, path)
    if url:
        return f"[{path}]({url})"
    return f"`{path}`"


def _ev_link(meta: dict, evidence: str) -> str:
    """Render `path:line` as `[path:line](url#Lline)` (no backticks)."""
    if not evidence:
        return "—"
    url = _gh_blob_url(meta, evidence)
    if url:
        return f"[{evidence}]({url})"
    return f"`{evidence}`"


def _cell(text: Any) -> str:
    """Escape pipes / newlines / collapse whitespace for table cells."""
    if text is None:
        return ""
    s = str(text).replace("\r", "").replace("\n", "<br/>")
    s = s.replace("|", "\\|")
    return s.strip()


# ---------------------------------------------------------------------------
# section renderers
# ---------------------------------------------------------------------------

def _badge(label: str, value: str, color: str) -> str:
    """Render a colored inline badge using emoji + bold, no external CDN.

    Works reliably on GitHub / Feishu / Notion / Obsidian regardless of
    network reachability to img.shields.io.
    """
    dot = {
        "blue": "🔵",
        "yellow": "🟡",
        "green": "🟢",
        "red": "🔴",
        "purple": "🟣",
        "orange": "🟠",
        "gray": "⚪",
    }.get(color, "⚪")
    return f"{dot} **{label}**: `{value}`"


def render_hero(summary: dict, meta: dict, file_count: int | None) -> str:
    name = summary.get("project_name") or meta.get("repo", "Unknown Project")
    one_liner = summary.get("one_liner", "")
    repo_url = _repo_url(meta)
    stars = _meta_get(meta, "stars", "star_count")
    language = _meta_get(meta, "primary_language", "language")
    license_name = _meta_get(meta, "license")
    sha = (meta.get("commit_sha") or "")[:7]
    branch = _meta_get(meta, "branch", "default_branch")

    badges: list[str] = []
    if language:
        badges.append(_badge("Language", str(language), "blue"))
    if stars is not None:
        badges.append(_badge("Stars", str(stars), "yellow"))
    if license_name:
        badges.append(_badge("License", str(license_name), "green"))
    if sha:
        badges.append(_badge("Commit", sha, "gray"))
    if file_count:
        badges.append(_badge("Files", str(file_count), "purple"))

    lines: list[str] = []
    lines.append(f"# {name}")
    lines.append("")
    if one_liner:
        lines.append(f"> **{one_liner}**")
        lines.append("")
    if badges:
        lines.append(" &nbsp;·&nbsp; ".join(badges))
        lines.append("")

    # meta line as a compact key-value sentence
    meta_bits: list[str] = []
    if repo_url:
        meta_bits.append(f"**Repo** [{repo_url.replace('https://', '')}]({repo_url})")
    if branch:
        meta_bits.append(f"**Branch** `{branch}`")
    if sha:
        meta_bits.append(f"**Commit** `{sha}`")
    if file_count:
        meta_bits.append(f"**Files** {file_count}")
    if meta_bits:
        lines.append(" &nbsp;·&nbsp; ".join(meta_bits))
        lines.append("")

    return "\n".join(lines) + "\n"


def render_tldr(summary: dict) -> str:
    rows = []
    for label, key in [
        ("🎯 面向谁", "who_for"),
        ("🧩 解决什么", "problem_solved"),
        ("💎 核心价值", "core_value"),
    ]:
        val = summary.get(key)
        if val:
            rows.append((label, val))
    if not rows:
        return ""
    out = ["## TL;DR", "", "| | |", "|---|---|"]
    for label, val in rows:
        out.append(f"| **{label}** | {_cell(val)} |")
    out.append("")
    return "\n".join(out) + "\n"


def render_tech_stack(summary: dict) -> str:
    stack = summary.get("tech_stack") or []
    if not stack:
        return ""
    lines = ["## 技术栈", "", "| 层 | 组件 |", "|---|---|"]
    for layer in stack:
        layer_name = _cell(layer.get("layer", ""))
        items = ", ".join(layer.get("items") or [])
        lines.append(f"| **{layer_name}** | {_cell(items)} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_architecture(summary: dict) -> str:
    mermaid = (summary.get("architecture_mermaid") or "").strip()
    if not mermaid:
        return ""
    return "## 系统架构\n\n```mermaid\n" + mermaid + "\n```\n\n"


def render_key_models(summary: dict, meta: dict) -> str:
    models = summary.get("key_models") or []
    if not models:
        return ""
    lines = [
        "## 核心模型",
        "",
        "项目里反复出现、贯穿多个模块的领域对象 / 数据结构。",
        "",
        "| # | 模型 | 路径 | 用途 | 关键字段 | 证据 |",
        "|---|---|---|---|---|---|",
    ]
    for i, m in enumerate(models, 1):
        name = _cell(m.get("name", ""))
        path = m.get("path", "")
        purpose = _cell(m.get("purpose", ""))
        fields = _cell(m.get("key_fields", ""))
        evidence = _ev_link(meta, m.get("evidence", ""))
        path_md = _path_link(meta, path)
        lines.append(
            f"| {i} | **{name}** | {path_md} | {purpose} | {fields} | {evidence} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def render_key_modules(summary: dict, meta: dict) -> str:
    modules = summary.get("key_modules") or []
    if not modules:
        return ""
    out = ["## 关键模块详解", ""]
    for i, mod in enumerate(modules, 1):
        name = mod.get("name", "")
        path = mod.get("path", "")
        responsibility = mod.get("responsibility", "")
        principle = mod.get("principle", "")
        subflow = mod.get("subflow") or []
        evidence_list = mod.get("evidence_list") or []

        header_path = f" &nbsp;·&nbsp; {_path_link(meta, path)}" if path else ""
        out.append(f"### {i}. {name}{header_path}")
        out.append("")

        # 紧凑的 attribute 表(同名 key-value 表格,粘到 Feishu 表格不会塌)
        attrs: list[tuple[str, str]] = []
        if responsibility:
            attrs.append(("职责", responsibility))
        if principle:
            attrs.append(("核心原理", principle))
        if attrs:
            out.append("| | |")
            out.append("|---|---|")
            for k, v in attrs:
                out.append(f"| **{k}** | {_cell(v)} |")
            out.append("")

        if subflow:
            out.append("**关键流程**")
            out.append("")
            for j, step in enumerate(subflow, 1):
                out.append(f"{j}. {step}")
            out.append("")

        if evidence_list:
            ev_inline = " &nbsp;·&nbsp; ".join(_ev_link(meta, ev) for ev in evidence_list)
            out.append(f"**证据**: {ev_inline}")
            out.append("")
    return "\n".join(out) + "\n"


def render_sequence(summary: dict) -> str:
    mermaid = (summary.get("sequence_mermaid") or "").strip()
    if not mermaid:
        return ""
    return "## 主流程时序\n\n```mermaid\n" + mermaid + "\n```\n\n"


def render_api_surface(summary: dict, meta: dict) -> str:
    apis = summary.get("api_surface") or []
    if not apis:
        return ""
    # Drop rows that lack any of the three required fields — half-empty rows
    # are noise. If nothing useful is left, hide the section entirely.
    valid = [
        a for a in apis
        if (a.get("type") or "").strip()
        and (a.get("signature") or "").strip()
        and (a.get("purpose") or "").strip()
    ]
    if not valid:
        return ""
    type_icon = {
        "CLI": "💻 CLI",
        "HTTP": "🌐 HTTP",
        "WebSocket": "🔌 WS",
        "WS": "🔌 WS",
        "MCP": "🤖 MCP",
        "SDK": "📦 SDK",
        "gRPC": "⚡ gRPC",
        "Webhook": "📡 Webhook",
    }
    lines = [
        "## 对外接口",
        "",
        "| 类型 | 签名 | 用途 | 证据 |",
        "|---|---|---|---|",
    ]
    for a in valid:
        typ_raw = a.get("type", "")
        typ = type_icon.get(typ_raw, typ_raw)
        sig = _cell(a.get("signature", ""))
        purpose = _cell(a.get("purpose", ""))
        ev = _ev_link(meta, a.get("evidence", "")) if a.get("evidence") else "—"
        sig_md = f"`{sig}`" if sig else "—"
        lines.append(f"| {typ} | {sig_md} | {purpose} | {ev} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_deps(summary: dict) -> str:
    deps = summary.get("dependencies") or []
    if not deps:
        return ""
    lines = ["## 关键依赖", "", "| 依赖 | 用途 | 重要度 |", "|---|---|---|"]
    for d in deps:
        crit = d.get("criticality", "")
        badge = "🔴 核心" if crit == "核心" else ("🟡 辅助" if crit else "—")
        lines.append(
            f"| **{_cell(d.get('name', ''))}** | "
            f"{_cell(d.get('purpose', ''))} | {badge} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def render_highlights(summary: dict) -> str:
    items = summary.get("highlights") or []
    if not items:
        return ""
    return "## 项目特色\n\n" + "\n".join(f"- {h}" for h in items) + "\n\n"


def render_limitations(summary: dict, meta: dict) -> str:
    items = summary.get("limitations") or []
    if not items:
        return ""
    sev_icon = {"high": "🔴 高", "medium": "🟠 中", "low": "🟢 低"}
    cat_icon = {
        "performance": "⚡ 性能",
        "security": "🔒 安全",
        "scalability": "📈 扩展性",
        "usability": "👤 易用性",
        "compatibility": "🧩 兼容性",
        "documentation": "📚 文档",
        "test_coverage": "🧪 测试覆盖",
        "architecture": "🏗️ 架构",
        "other": "🔧 其他",
    }

    # Compact table view (overview) + detail sub-section.
    lines = [
        "## 限制 / 待优化点",
        "",
        "诚实评估,共 " + str(len(items)) + " 条。",
        "",
        "| # | 严重度 | 类别 | 标题 | 证据 |",
        "|---|---|---|---|---|",
    ]
    for i, lim in enumerate(items, 1):
        sev = sev_icon.get(lim.get("severity", ""), lim.get("severity", "") or "—")
        cat = cat_icon.get(lim.get("category", ""), lim.get("category", "") or "—")
        title = _cell(lim.get("title", ""))
        ev = _ev_link(meta, lim.get("evidence", "")) if lim.get("evidence") else "—"
        lines.append(f"| {i} | {sev} | {cat} | {title} | {ev} |")
    lines.append("")
    lines.append("### 详细说明")
    lines.append("")
    for i, lim in enumerate(items, 1):
        title = lim.get("title", "")
        detail = lim.get("detail", "")
        sev = sev_icon.get(lim.get("severity", ""), lim.get("severity", ""))
        cat = cat_icon.get(lim.get("category", ""), lim.get("category", ""))
        ev = lim.get("evidence", "")
        lines.append(f"#### {i}. {title}")
        lines.append("")
        tag_bits = []
        if sev:
            tag_bits.append(sev)
        if cat:
            tag_bits.append(cat)
        if tag_bits:
            lines.append(" &nbsp;·&nbsp; ".join(tag_bits))
            lines.append("")
        if detail:
            lines.append(detail)
            lines.append("")
        if ev:
            lines.append(f"> 证据: {_ev_link(meta, ev)}")
            lines.append("")
    return "\n".join(lines) + "\n"


def render_glossary(summary: dict) -> str:
    items = summary.get("glossary") or []
    if not items:
        return ""
    lines = ["## 术语对照", "", "| 术语 | 白话解释 |", "|---|---|"]
    for g in items:
        lines.append(
            f"| **{_cell(g.get('term', ''))}** | "
            f"{_cell(g.get('plain', ''))} |"
        )
    lines.append("")
    return "\n".join(lines) + "\n"


def render_footer(meta: dict) -> str:
    repo_url = _repo_url(meta)
    sha = meta.get("commit_sha", "")
    branch = _meta_get(meta, "branch", "default_branch")
    bits: list[str] = []
    if repo_url:
        bits.append(f"Source [{repo_url.replace('https://', '')}]({repo_url})")
    if branch:
        bits.append(f"branch `{branch}`")
    if sha:
        bits.append(f"commit `{sha[:7]}`")
    if not bits:
        return ""
    return (
        "---\n\n"
        + "*" + " · ".join(bits) + "*\n\n"
        + "*Generated by `repo-explainer` — every conclusion is backed by `path:line` evidence; click any code reference above to verify on GitHub.*\n"
    )


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def render(summary: dict, meta: dict, file_count: int | None) -> str:
    sections = [
        render_hero(summary, meta, file_count),
        render_tldr(summary),
        render_tech_stack(summary),
        render_architecture(summary),
        render_key_models(summary, meta),
        render_key_modules(summary, meta),
        render_sequence(summary),
        render_api_surface(summary, meta),
        render_deps(summary),
        render_highlights(summary),
        render_limitations(summary, meta),
        render_glossary(summary),
        render_footer(meta),
    ]
    return "\n".join(s for s in sections if s).rstrip() + "\n"


def main() -> int:
    p = argparse.ArgumentParser(description="Render summary.json into a Markdown report.")
    p.add_argument("summary_json", help="Path to summary.json (Stage 4 output).")
    p.add_argument("--meta_json", required=True, help="Path to meta.json (Stage 1 output).")
    p.add_argument("--file_count", type=int, default=None, help="Total file count for hero badge.")
    args = p.parse_args()

    summary = json.loads(Path(args.summary_json).read_text(encoding="utf-8"))
    meta = json.loads(Path(args.meta_json).read_text(encoding="utf-8"))
    sys.stdout.write(render(summary, meta, args.file_count))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
