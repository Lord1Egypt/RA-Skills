#!/usr/bin/env python3
"""
Vedic chart report builder.

Input contract:
  report-folder/
    report.meta.json
    sections/
      01-overview.md
      02-core-audit.md
      03-timing.md

Output:
  report-folder/dist/report.html

The renderer is intentionally narrow. It supports only the markdown subset that
the chart analysis skill is expected to produce:
  - headings
  - paragraphs
  - bold text
  - inline code
  - unordered and ordered lists
  - blockquotes
  - fenced code blocks
  - horizontal rules
  - simple GFM-style tables
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

RE_FENCE = re.compile(r"^```(?P<lang>[A-Za-z0-9_-]+)?\s*$")
RE_HEADING = re.compile(r"^(#{1,6})\s+(.*\S)\s*$")
RE_HR = re.compile(r"^\s{0,3}([-*_])(?:\s*\1){2,}\s*$")
RE_BLOCKQUOTE = re.compile(r"^>\s?(.*)$")
RE_UL = re.compile(r"^[-+*]\s+(.*)$")
RE_OL = re.compile(r"^\d+\.\s+(.*)$")
RE_TABLE_SEPARATOR = re.compile(r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?\s*$")
RE_SECTION_FILE = re.compile(r"^(?P<number>\d{2,})-(?P<slug>[A-Za-z0-9_\-\u4e00-\u9fff]+)\.md$")

CSS = """
:root {
  color-scheme: light;
  --bg: #f5f1e8;
  --panel: rgba(255, 252, 246, 0.94);
  --panel-strong: #fffaf0;
  --ink: #2a231d;
  --muted: #6e6257;
  --line: #d7c9b8;
  --line-strong: #b8976b;
  --accent: #8d5a2b;
  --accent-soft: #efe1cf;
  --shadow: 0 20px 48px rgba(74, 51, 29, 0.08);
  --radius-lg: 22px;
  --radius-md: 16px;
  --radius-sm: 12px;
  --sans: "Segoe UI", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif;
  --serif: Georgia, "Times New Roman", "Songti SC", "Noto Serif CJK SC", serif;
}

* {
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  font-family: var(--sans);
  color: var(--ink);
  background:
    radial-gradient(circle at top left, rgba(215, 190, 153, 0.34), transparent 32%),
    linear-gradient(180deg, #f9f6ef 0%, var(--bg) 100%);
  line-height: 1.72;
}

a {
  color: var(--accent);
}

.page {
  width: min(1120px, calc(100vw - 32px));
  margin: 24px auto 56px;
}

.hero,
.card,
.section {
  background: var(--panel);
  border: 1px solid rgba(183, 155, 119, 0.28);
  box-shadow: var(--shadow);
  backdrop-filter: blur(10px);
}

.hero {
  padding: 36px;
  border-radius: 30px;
  overflow: hidden;
  position: relative;
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    linear-gradient(135deg, rgba(220, 197, 165, 0.26), transparent 58%),
    radial-gradient(circle at top right, rgba(141, 90, 43, 0.12), transparent 26%);
  pointer-events: none;
}

.hero-inner {
  position: relative;
  z-index: 1;
}

.eyebrow {
  margin: 0 0 10px;
  text-transform: uppercase;
  letter-spacing: 0.24em;
  font-size: 12px;
  color: var(--accent);
  font-weight: 700;
}

.title {
  margin: 0;
  font-family: var(--serif);
  font-size: clamp(34px, 5vw, 56px);
  line-height: 1.08;
}

.subtitle {
  margin: 14px 0 0;
  max-width: 760px;
  color: var(--muted);
  font-size: 16px;
}

.meta-grid {
  margin-top: 28px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 14px;
}

.meta-item {
  background: rgba(255, 249, 239, 0.75);
  border: 1px solid rgba(183, 155, 119, 0.24);
  border-radius: var(--radius-md);
  padding: 14px 16px;
}

.meta-label {
  font-size: 12px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--muted);
}

.meta-value {
  margin-top: 6px;
  font-weight: 600;
}

.stack {
  display: grid;
  gap: 18px;
  margin-top: 20px;
}

.two-up {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.card {
  border-radius: var(--radius-lg);
  padding: 24px;
}

.card h2,
.section-header h2 {
  margin: 0 0 12px;
  font-family: var(--serif);
  font-size: 28px;
}

.card p,
.card li {
  color: var(--ink);
}

.card ul {
  margin: 10px 0 0 20px;
  padding: 0;
}

.toc-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: grid;
  gap: 10px;
}

.toc-list li a {
  display: flex;
  justify-content: space-between;
  gap: 12px;
  padding: 12px 14px;
  border-radius: var(--radius-sm);
  text-decoration: none;
  background: rgba(239, 225, 207, 0.48);
  border: 1px solid rgba(183, 155, 119, 0.18);
}

.toc-number {
  color: var(--muted);
  font-size: 13px;
  font-weight: 700;
}

.toc-title {
  color: var(--ink);
  text-align: right;
  font-weight: 600;
}

.section {
  border-radius: 28px;
  overflow: hidden;
}

.section-header {
  padding: 24px 28px 18px;
  background:
    linear-gradient(180deg, rgba(241, 228, 208, 0.9), rgba(255, 250, 242, 0.6));
  border-bottom: 1px solid rgba(183, 155, 119, 0.24);
}

.section-kicker {
  text-transform: uppercase;
  letter-spacing: 0.18em;
  font-size: 12px;
  color: var(--accent);
  font-weight: 700;
}

.section-body {
  padding: 26px 28px 30px;
}

.section-body > :first-child {
  margin-top: 0;
}

.section-body h3,
.section-body h4,
.section-body h5,
.section-body h6 {
  margin: 1.4em 0 0.6em;
  font-family: var(--serif);
  line-height: 1.25;
}

.section-body p {
  margin: 0 0 1em;
}

.section-body ul,
.section-body ol {
  margin: 0 0 1em 1.4em;
  padding: 0;
}

.section-body li {
  margin-bottom: 0.45em;
}

.section-body blockquote {
  margin: 1.2em 0;
  padding: 14px 18px;
  border-left: 4px solid var(--line-strong);
  background: rgba(239, 225, 207, 0.52);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  color: #3d3228;
}

.section-body hr {
  border: none;
  border-top: 1px solid var(--line);
  margin: 1.5em 0;
}

.section-body pre {
  margin: 1.2em 0;
  padding: 16px;
  overflow-x: auto;
  background: #221c18;
  color: #f5ecdf;
  border-radius: var(--radius-md);
}

.section-body code {
  font-family: Consolas, "SFMono-Regular", Menlo, monospace;
  font-size: 0.92em;
}

.section-body p code,
.section-body li code,
.section-body td code,
.section-body th code {
  background: rgba(239, 225, 207, 0.72);
  padding: 0.14em 0.36em;
  border-radius: 8px;
  color: #4a3828;
}

.code-lang {
  display: inline-block;
  margin-bottom: 10px;
  padding: 3px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.12);
  color: #f4dec7;
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.2em 0;
  background: rgba(255, 252, 246, 0.72);
  border: 1px solid rgba(183, 155, 119, 0.28);
  border-radius: 14px;
  overflow: hidden;
}

th,
td {
  padding: 12px 14px;
  text-align: left;
  vertical-align: top;
  border-bottom: 1px solid rgba(183, 155, 119, 0.18);
}

th {
  background: rgba(239, 225, 207, 0.72);
  font-weight: 700;
}

tr:last-child td {
  border-bottom: none;
}

.footer {
  text-align: center;
  color: var(--muted);
  font-size: 14px;
  padding: 14px 0 0;
}

@media (max-width: 860px) {
  .page {
    width: min(100vw - 20px, 1120px);
    margin: 10px auto 28px;
  }

  .hero,
  .card,
  .section {
    border-radius: 22px;
  }

  .hero,
  .card,
  .section-body,
  .section-header {
    padding-left: 18px;
    padding-right: 18px;
  }

  .two-up {
    grid-template-columns: 1fr;
  }

  th,
  td {
    padding: 10px 12px;
  }
}
"""

LABELS = {
    "cn": {
        "eyebrow": "吠陀命盘研判",
        "subtitle": "先给现实判断，再拆盘面抓手。每一节都围绕判断、抓手和使用提醒来组织。",
        "toc_title": "目录",
        "reading_title": "阅读方式",
        "reading_points": [
            "先看每节开头的现实判断，确认这段到底在说什么。",
            "再看盘面抓手，理解为什么会得出这个判断。",
            "最后看使用提醒，分清哪些能落地，哪些仍需保留弹性。",
        ],
        "risk_title": "风险提示",
        "risk_points": [
            "时机窗口代表阶段，不代表事件保证。",
            "如果出生时间不稳，宫位级结论与精细时点都需要降级阅读。",
            "这份 HTML 只负责呈现，不替你修补原始数据错误。",
        ],
        "notes_title": "备注",
        "glossary_title": "术语提示",
        "glossary_points": [
            "`命主盘（Rashi chart）` 用来看外在结构、主事分工与现实落点。",
            "`九分盘（Navamsha chart）` 用来看成熟后的质量、耐久度和兑现环境。",
            "`八镜框架` 只是内部拆盘抓手，对外表达时要始终翻译成现实语言。",
        ],
        "meta": {
            "client_name": "客户",
            "lagna": "上升",
            "gender": "性别",
            "status": "状态",
            "report_kind": "报告类型",
            "source_system": "研判体系",
        },
        "section_kicker": "章节",
        "footer": "吠陀命盘分析报告 HTML 版，适合屏幕阅读与归档复盘。",
    },
    "en": {
        "eyebrow": "Vedic Chart Analysis",
        "subtitle": "Each section is organized around a real-world judgment, chart evidence, and practical usage notes.",
        "toc_title": "Contents",
        "reading_title": "How to read this",
        "reading_points": [
            "Read the judgment first.",
            "Use the chart evidence to see why the conclusion was made.",
            "Use the usage notes to separate advice from uncertainty.",
        ],
        "risk_title": "Limits",
        "risk_points": [
            "Timing windows are ranges, not guarantees.",
            "Weak birth time lowers confidence on house-specific claims.",
            "This HTML preserves the report; it does not repair bad source data.",
        ],
        "notes_title": "Notes",
        "glossary_title": "Glossary",
        "glossary_points": [
            "`Rashi chart` refers to the main natal structure chart.",
            "`Navamsha chart` is used for maturity, durability, and fulfillment quality.",
            "`Eight-lens framing` is an internal reading scaffold and should always be translated into plain language when surfaced.",
        ],
        "meta": {
            "client_name": "Client",
            "lagna": "Lagna",
            "gender": "Gender",
            "status": "Status",
            "report_kind": "Report Type",
            "source_system": "Analysis System",
        },
        "section_kicker": "Section",
        "footer": "Vedic chart analysis HTML report for screen reading and archived review.",
    },
}


class ReportError(Exception):
    """Raised when the report folder does not match the expected contract."""


@dataclass
class Section:
    number: str
    slug: str
    title: str
    body: str
    anchor: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a Vedic chart analysis HTML report.")
    parser.add_argument("folder", help="Report folder containing report.meta.json and sections/")
    parser.add_argument("--output", default=None, help="Override the output HTML path")
    parser.add_argument("--lang", choices=["cn", "en"], default=None, help="Override report language")
    parser.add_argument("--client-name", default=None, help="Override client_name")
    parser.add_argument("--lagna", default=None, help="Override lagna")
    parser.add_argument("--gender", default=None, help="Override gender")
    parser.add_argument("--status", default=None, help="Override status")
    parser.add_argument("--report-kind", default=None, help="Override report_kind")
    parser.add_argument("--source-system", default=None, help="Override source_system")
    parser.add_argument("--notes", nargs="*", default=None, help="Override notes as one or more items")
    return parser.parse_args()


def load_meta(report_dir: Path, args: argparse.Namespace) -> dict[str, Any]:
    meta_path = report_dir / "report.meta.json"
    if not meta_path.is_file():
        raise ReportError(f"Missing meta file: {meta_path}")

    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReportError(f"Invalid JSON in {meta_path}: {exc}") from exc

    if not isinstance(meta, dict):
        raise ReportError("report.meta.json must contain a JSON object.")

    overrides = {
        "lang": args.lang,
        "client_name": args.client_name,
        "lagna": args.lagna,
        "gender": args.gender,
        "status": args.status,
        "report_kind": args.report_kind,
        "source_system": args.source_system,
    }
    for key, value in overrides.items():
        if value is not None:
            meta[key] = value

    if args.notes is not None:
        meta["notes"] = args.notes

    if "lang" not in meta or not meta["lang"]:
        meta["lang"] = "cn"
    if meta["lang"] not in LABELS:
        raise ReportError("lang must be either 'cn' or 'en'.")

    if "notes" not in meta or meta["notes"] is None:
        meta["notes"] = []

    required = [
        "client_name",
        "lagna",
        "gender",
        "status",
        "report_kind",
        "source_system",
    ]
    missing = [key for key in required if not str(meta.get(key, "")).strip()]
    if missing:
        raise ReportError(f"Missing required meta fields: {', '.join(missing)}")

    if not isinstance(meta["notes"], (list, str)):
        raise ReportError("notes must be either a string or a list of strings.")

    return meta


def load_sections(report_dir: Path) -> list[Section]:
    sections_dir = report_dir / "sections"
    if not sections_dir.is_dir():
        raise ReportError(f"Missing sections directory: {sections_dir}")

    files = sorted(path for path in sections_dir.iterdir() if path.is_file() and path.suffix.lower() == ".md")
    if not files:
        raise ReportError("sections/ does not contain any markdown files.")

    sections: list[Section] = []
    for path in files:
        match = RE_SECTION_FILE.match(path.name)
        if not match:
            raise ReportError(
                f"Invalid section filename '{path.name}'. Expected the form NN-slug.md."
            )

        body_text = path.read_text(encoding="utf-8")
        fallback_title = slug_to_title(match.group("slug"))
        title, body = extract_title_and_body(body_text, fallback_title)
        anchor = f"section-{match.group('number')}-{match.group('slug').lower()}"
        sections.append(
            Section(
                number=match.group("number"),
                slug=match.group("slug"),
                title=title,
                body=body,
                anchor=anchor,
            )
        )

    return sections


def slug_to_title(slug: str) -> str:
    human = slug.replace("_", " ").replace("-", " ").strip()
    if re.search(r"[A-Za-z]", human):
        return " ".join(part.capitalize() if part.islower() else part for part in human.split())
    return human


def extract_title_and_body(text: str, fallback_title: str) -> tuple[str, str]:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    first_content_index = 0
    while first_content_index < len(lines) and not lines[first_content_index].strip():
        first_content_index += 1

    if first_content_index < len(lines):
        match = RE_HEADING.match(lines[first_content_index])
        if match:
            title = match.group(2).strip()
            body_lines = lines[:first_content_index] + lines[first_content_index + 1 :]
            return title, "\n".join(body_lines).strip()

    return fallback_title, text.strip()


def render_html(meta: dict[str, Any], sections: list[Section]) -> str:
    lang = meta["lang"]
    labels = LABELS[lang]
    title = f"{meta['client_name']} — {meta['report_kind']}"

    hero = build_hero(meta, labels)
    cards = build_support_cards(meta, labels)
    toc = build_toc(sections, labels)
    body = "\n".join(build_section_html(section, labels) for section in sections)
    footer = f'<div class="footer">{escape(labels["footer"])}</div>'

    return f"""<!DOCTYPE html>
<html lang="{html_lang(lang)}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <style>{CSS}</style>
</head>
<body>
  <main class="page">
    {hero}
    <div class="stack">
      {cards}
      {toc}
      {body}
      {footer}
    </div>
  </main>
</body>
</html>"""


def build_hero(meta: dict[str, Any], labels: dict[str, Any]) -> str:
    meta_labels = labels["meta"]
    items = [
        ("client_name", meta["client_name"]),
        ("lagna", meta["lagna"]),
        ("gender", meta["gender"]),
        ("status", meta["status"]),
        ("report_kind", meta["report_kind"]),
        ("source_system", meta["source_system"]),
    ]
    meta_html = "\n".join(
        f'<div class="meta-item"><div class="meta-label">{escape(meta_labels[key])}</div><div class="meta-value">{escape(str(value))}</div></div>'
        for key, value in items
    )
    return f"""
<section class="hero">
  <div class="hero-inner">
    <p class="eyebrow">{escape(labels["eyebrow"])}</p>
    <h1 class="title">{escape(meta["report_kind"])}</h1>
    <p class="subtitle">{escape(labels["subtitle"])}</p>
    <div class="meta-grid">
      {meta_html}
    </div>
  </div>
</section>"""


def build_support_cards(meta: dict[str, Any], labels: dict[str, Any]) -> str:
    notes = normalize_notes(meta.get("notes", []))
    reading = build_card(labels["reading_title"], labels["reading_points"])
    risk = build_card(labels["risk_title"], labels["risk_points"])
    extras = [
        build_card(labels["glossary_title"], labels["glossary_points"]),
    ]
    if notes:
        extras.append(build_card(labels["notes_title"], notes))

    extra_html = "\n".join(extras)
    return f"""
<div class="two-up">
  {reading}
  {risk}
</div>
{extra_html}"""


def build_card(title: str, items: list[str]) -> str:
    list_html = "\n".join(f"<li>{render_inline(item)}</li>" for item in items)
    return f"""
<section class="card">
  <h2>{escape(title)}</h2>
  <ul>
    {list_html}
  </ul>
</section>"""


def build_toc(sections: list[Section], labels: dict[str, Any]) -> str:
    items = []
    for section in sections:
        items.append(
            f'<li><a href="#{escape(section.anchor)}"><span class="toc-number">{escape(section.number)}</span><span class="toc-title">{escape(section.title)}</span></a></li>'
        )
    return f"""
<section class="card">
  <h2>{escape(labels["toc_title"])}</h2>
  <ul class="toc-list">
    {''.join(items)}
  </ul>
</section>"""


def build_section_html(section: Section, labels: dict[str, Any]) -> str:
    rendered = render_markdown(section.body)
    return f"""
<section id="{escape(section.anchor)}" class="section">
  <div class="section-header">
    <div class="section-kicker">{escape(labels["section_kicker"])} {escape(section.number)}</div>
    <h2>{escape(section.title)}</h2>
  </div>
  <div class="section-body">
    {rendered}
  </div>
</section>"""


def render_markdown(text: str) -> str:
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[str] = []
    index = 0

    while index < len(lines):
        line = lines[index]

        if not line.strip():
            index += 1
            continue

        fence = RE_FENCE.match(line)
        if fence:
            language = fence.group("lang") or ""
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not RE_FENCE.match(lines[index]):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            blocks.append(render_code_block("\n".join(code_lines), language))
            continue

        if is_table_start(lines, index):
            table_lines = [lines[index], lines[index + 1]]
            index += 2
            while index < len(lines) and "|" in lines[index] and lines[index].strip():
                table_lines.append(lines[index])
                index += 1
            blocks.append(render_table(table_lines))
            continue

        heading = RE_HEADING.match(line)
        if heading:
            blocks.append(render_heading(len(heading.group(1)), heading.group(2).strip()))
            index += 1
            continue

        if RE_HR.match(line):
            blocks.append("<hr>")
            index += 1
            continue

        quote = RE_BLOCKQUOTE.match(line)
        if quote:
            quote_lines = [quote.group(1)]
            index += 1
            while index < len(lines):
                nested = RE_BLOCKQUOTE.match(lines[index])
                if not nested:
                    break
                quote_lines.append(nested.group(1))
                index += 1
            blocks.append(render_blockquote(quote_lines))
            continue

        list_match = RE_UL.match(line) or RE_OL.match(line)
        if list_match:
            ordered = bool(RE_OL.match(line))
            items: list[str] = [list_match.group(1)]
            index += 1
            while index < len(lines):
                next_match = RE_OL.match(lines[index]) if ordered else RE_UL.match(lines[index])
                if not next_match:
                    break
                items.append(next_match.group(1))
                index += 1
            blocks.append(render_list(items, ordered))
            continue

        paragraph_lines = [line.strip()]
        index += 1
        while index < len(lines) and lines[index].strip() and not is_block_start(lines, index):
            paragraph_lines.append(lines[index].strip())
            index += 1
        blocks.append(f"<p>{render_inline(' '.join(paragraph_lines))}</p>")

    return "\n".join(blocks)


def is_block_start(lines: list[str], index: int) -> bool:
    line = lines[index]
    return bool(
        RE_FENCE.match(line)
        or RE_HEADING.match(line)
        or RE_HR.match(line)
        or RE_BLOCKQUOTE.match(line)
        or RE_UL.match(line)
        or RE_OL.match(line)
        or is_table_start(lines, index)
    )


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    if "|" not in lines[index]:
        return False
    return bool(RE_TABLE_SEPARATOR.match(lines[index + 1]))


def render_heading(level: int, text: str) -> str:
    mapped_level = min(level + 2, 6)
    return f"<h{mapped_level}>{render_inline(text)}</h{mapped_level}>"


def render_blockquote(lines: list[str]) -> str:
    content = "<br>".join(render_inline(line.strip()) for line in lines if line.strip())
    return f"<blockquote>{content}</blockquote>"


def render_list(items: list[str], ordered: bool) -> str:
    tag = "ol" if ordered else "ul"
    rendered = "".join(f"<li>{render_inline(item.strip())}</li>" for item in items)
    return f"<{tag}>{rendered}</{tag}>"


def render_code_block(code: str, language: str) -> str:
    badge = f'<div class="code-lang">{escape(language)}</div>' if language else ""
    return f"<pre>{badge}<code>{escape(code)}</code></pre>"


def render_table(lines: list[str]) -> str:
    rows = [split_table_row(line) for line in lines if line.strip()]
    header = rows[0]
    body = rows[2:]
    head_html = "".join(f"<th>{render_inline(cell)}</th>" for cell in header)
    body_html = []
    for row in body:
        cells = "".join(f"<td>{render_inline(cell)}</td>" for cell in row)
        body_html.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{head_html}</tr></thead><tbody>{''.join(body_html)}</tbody></table>"


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def render_inline(text: str) -> str:
    placeholders: dict[str, str] = {}

    def stash(pattern: re.Pattern[str], raw: str, renderer) -> str:
        def replacer(match: re.Match[str]) -> str:
            key = f"__PLACEHOLDER_{len(placeholders)}__"
            placeholders[key] = renderer(match)
            return key

        return pattern.sub(replacer, raw)

    text = stash(
        re.compile(r"`([^`]+)`"),
        text,
        lambda match: f"<code>{escape(match.group(1))}</code>",
    )
    text = stash(
        re.compile(r"\[([^\]]+)\]\(([^)]+)\)"),
        text,
        lambda match: f'<a href="{escape(match.group(2), quote=True)}">{escape(match.group(1))}</a>',
    )

    escaped = escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)

    for key, value in placeholders.items():
        escaped = escaped.replace(key, value)

    return escaped


def normalize_notes(raw_notes: Any) -> list[str]:
    if isinstance(raw_notes, list):
        return [str(item).strip() for item in raw_notes if str(item).strip()]
    if isinstance(raw_notes, str):
        return [line.strip() for line in raw_notes.splitlines() if line.strip()]
    return []


def html_lang(lang: str) -> str:
    return "zh-CN" if lang == "cn" else "en"


def main() -> int:
    args = parse_args()
    report_dir = Path(args.folder).expanduser().resolve()
    if not report_dir.is_dir():
        raise ReportError(f"Report folder does not exist: {report_dir}")

    meta = load_meta(report_dir, args)
    sections = load_sections(report_dir)
    html = render_html(meta, sections)

    output_path = Path(args.output).expanduser().resolve() if args.output else report_dir / "dist" / "report.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"Wrote HTML report: {output_path}")
    print(f"Sections: {len(sections)} | Language: {meta['lang']} | Client: {meta['client_name']}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ReportError as exc:
        print(f"Error: {exc}")
        raise SystemExit(1) from exc
