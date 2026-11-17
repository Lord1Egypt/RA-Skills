#!/usr/bin/env python3
"""Save structured v1.1 research report to skill-local memory."""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
RESEARCH_DIR = SKILL_DIR / "research" / "sessions"
INDEX_FILE = SKILL_DIR / "research" / "index.md"


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return (s[:48] or "topic")


def format_references(papers: list[dict]) -> list[str]:
    lines = ["| 序号 | 标题 | 作者 | 年份 | 来源 | 链接 |", "|------|------|------|------|------|------|"]
    for i, p in enumerate(papers, 1):
        authors = ", ".join(p.get("authors") or [])[:60] or "—"
        year = str(p.get("year") or "—")
        source = p.get("source") or "—"
        link = p.get("doi") or p.get("url") or "—"
        if p.get("doi") and not str(link).startswith("http"):
            link = f"https://doi.org/{p['doi']}"
        title = (p.get("title") or "Untitled").replace("|", "\\|")[:80]
        lines.append(f"| [{i}] | {title} | {authors} | {year} | {source} | {link} |")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser(description="Save structured research report")
    parser.add_argument("--topic", required=True, help="User question / research topic")
    parser.add_argument("--papers-json", help="Path to search_literature JSON output")
    parser.add_argument("--session-id", help="Reuse session id for follow-up")
    parser.add_argument("--report-file", help="Full report markdown file (v1.1 structured)")
    parser.add_argument("--summary", help="Legacy: conclusion summary only")
    parser.add_argument("--review", help="Literature review section (~300 chars)")
    parser.add_argument("--gaps", help="Research gaps and innovation points")
    parser.add_argument("--recommendations", help="Research recommendations (~200 chars)")
    parser.add_argument(
        "--follow-ups",
        help="Three follow-up directions (newline-separated or JSON array)",
    )
    args = parser.parse_args()

    papers: list[dict] = []
    if args.papers_json:
        path = Path(args.papers_json)
        if path.exists():
            data = json.loads(path.read_text(encoding="utf-8"))
            papers = data.get("papers") or []

    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    SKILL_DIR.joinpath("research").mkdir(exist_ok=True)

    now = datetime.now(timezone.utc)
    session_id = args.session_id or f"{now.strftime('%Y%m%d')}-{slugify(args.topic)}"

    if args.report_file:
        report_path = Path(args.report_file)
        report_body = report_path.read_text(encoding="utf-8").strip()
    else:
        follow_ups = []
        if args.follow_ups:
            raw = args.follow_ups.strip()
            if raw.startswith("["):
                follow_ups = json.loads(raw)
            else:
                follow_ups = [ln.strip() for ln in raw.splitlines() if ln.strip()]
        follow_block = "\n".join(f"{i}. {item}" for i, item in enumerate(follow_ups[:3], 1))

        sections = [
            "## 结论摘要",
            "",
            (args.summary or "（待填写）").strip(),
            "",
            "## 参考文献",
            "",
        ]
        if papers:
            sections.extend(format_references(papers))
        else:
            sections.append("（无检索结果）")
        sections.extend(
            [
                "",
                "## 文献综述",
                "",
                (args.review or "（待填写）").strip(),
                "",
                "## 研究空白与创新点",
                "",
                (args.gaps or "（待填写）").strip(),
                "",
                "## 研究建议",
                "",
                (args.recommendations or "（待填写）").strip(),
                "",
                "## 追问建议",
                "",
                follow_block or "1. （待填写）\n2. （待填写）\n3. （待填写）",
                "",
            ]
        )
        report_body = "\n".join(sections)

    body = [
        f"# {args.topic}",
        "",
        f"- session_id: `{session_id}`",
        f"- version: `1.1`",
        f"- updated: {now.isoformat()}",
        "",
        report_body,
        "",
    ]

    out_path = RESEARCH_DIR / f"{session_id}.md"
    out_path.write_text("\n".join(body), encoding="utf-8")

    if INDEX_FILE.exists():
        index_lines = INDEX_FILE.read_text(encoding="utf-8").splitlines()
    else:
        index_lines = ["# Smart Research Sessions", ""]
    entry = f"- [{args.topic[:60]}](sessions/{session_id}.md) — {now.strftime('%Y-%m-%d')} v1.1"
    if entry not in index_lines:
        index_lines.insert(2, entry)
    INDEX_FILE.write_text("\n".join(index_lines) + "\n", encoding="utf-8")

    print(json.dumps({"session_id": session_id, "path": str(out_path.relative_to(SKILL_DIR))}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
