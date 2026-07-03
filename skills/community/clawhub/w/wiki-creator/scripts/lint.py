"""lint.py — 结构体检

用法:
    python lint.py [--root <wiki-root>]

输出 JSON 体检报告：
{
  "orphans": [...],              # 孤立页（零入链）
  "dangling_links": [...],       # 悬空链接（指向不存在页）
  "missing_pages": [...],        # 被多处引用却无独立页
  "missing_cross_refs": [...],   # 同主题页未互联（启发式）
  "no_source_claims": [...],     # 无来源断言的页面
  "topic_orphans": [...],        # frontmatter topic 不在 SCHEMA
  "oversized_topics": [...],     # 主题 > 1000 页
  "page_count": int,
  "topic_count": int,
}
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from _root import detect_wiki_root, normalize_path

DEFAULT_ROOT = detect_wiki_root()

WIKILINK_RE = re.compile(r"\[\[([a-z0-9][a-z0-9-/]*)\]\]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)

MAX_TOPIC_PAGES = 1000


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def parse_frontmatter(text: str) -> tuple[dict, str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    fm_text, body = m.group(1), m.group(2)
    fm = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip()
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            fm[k] = [x.strip().strip("'\"") for x in inner.split(",")] if inner else []
        else:
            fm[k] = v.strip("'\"")
    return fm, body


def load_topics_from_schema(wiki_dir: Path) -> set[str]:
    schema_path = wiki_dir / "SCHEMA.md"
    if not schema_path.exists():
        return set()
    text = schema_path.read_text(encoding="utf-8")
    slugs = set()
    in_topics = False
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("## 主题清单"):
            in_topics = True
            continue
        if in_topics and s.startswith("## "):
            in_topics = False
            continue
        if not in_topics or not s.startswith("|") or s.startswith("|-") or s.startswith("| slug"):
            continue
        parts = [p.strip() for p in s.strip("|").split("|")]
        if parts and parts[0]:
            slugs.add(parts[0])
    return slugs


def load_pages(wiki_dir: Path) -> list[dict]:
    pages_dir = wiki_dir / "pages"
    if not pages_dir.exists():
        return []
    pages = []
    for md in sorted(pages_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(text)
        slug = md.stem
        pages.append(
            {
                "slug": slug,
                "path": md.relative_to(wiki_dir).as_posix(),
                "title": fm.get("title", slug),
                "topic": fm.get("topic", ""),
                "entity_type": fm.get("entity_type", ""),
                "sources": fm.get("sources", []),
                "wikilinks": [
                    link.rsplit("/", 1)[-1] if "/" in link else link
                    for link in WIKILINK_RE.findall(body)
                ],
                "has_source_section": bool(
                    re.search(r"^##\s*(证据|来源|证据\s*/\s*来源)", body, re.MULTILINE)
                ),
                "body": body,
            }
        )
    return pages


def lint(root: Path) -> dict:
    wiki_dir = root / "wiki"
    if not wiki_dir.exists():
        return {"error": "wiki/ 不存在"}

    pages = load_pages(wiki_dir)
    page_slugs = {p["slug"] for p in pages}
    backlinks = load_json(wiki_dir / ".backlinks.json", {})
    schema_topics = load_topics_from_schema(wiki_dir)

    # 1. 孤立页：零入链（且不是 index.md 中首次出现的入口；这里简单按零入链判定）
    orphans = [p["slug"] for p in pages if not backlinks.get(p["slug"])]

    # 2. 悬空链接：指向不存在页
    dangling = set()
    for p in pages:
        for link in p["wikilinks"]:
            if link not in page_slugs:
                dangling.add(link)
    dangling_links = sorted(dangling)

    # 3. 缺失页面：被多处引用却无独立页（>=2 入链的悬空链接）
    missing_pages = sorted(
        slug for slug, refs in backlinks.items() if slug not in page_slugs and len(refs) >= 2
    )

    # 4. 缺失交叉引用：同主题页未互联（启发式——同主题但相互无 wikilink）
    by_topic = defaultdict(list)
    for p in pages:
        by_topic[p["topic"]].append(p)
    missing_cross_refs = []
    for topic, group in by_topic.items():
        if len(group) <= 1:
            continue
        for p in group:
            linked = set(p["wikilinks"])
            others = [o["slug"] for o in group if o["slug"] != p["slug"]]
            unlinked_others = [o for o in others if o not in linked]
            if len(unlinked_others) >= 2:
                missing_cross_refs.append(
                    {"page": p["slug"], "topic": topic, "unlinked_same_topic": unlinked_others[:5]}
                )

    # 5. 无来源断言：有结论但无 ## 证据 / 来源，或 sources 为空
    no_source_claims = [
        p["slug"] for p in pages if not p["has_source_section"] or not p["sources"]
    ]

    # 6. 主题孤儿：frontmatter topic 不在 SCHEMA 主题清单
    topic_orphans = [
        {"page": p["slug"], "topic": p["topic"]}
        for p in pages
        if schema_topics and p["topic"] not in schema_topics
    ]

    # 7. 主题过大：> MAX_TOPIC_PAGES
    oversized_topics = [
        {"topic": t, "count": len(g)} for t, g in by_topic.items() if len(g) > MAX_TOPIC_PAGES
    ]

    return {
        "page_count": len(pages),
        "topic_count": len(by_topic),
        "orphans": orphans,
        "dangling_links": dangling_links,
        "missing_pages": missing_pages,
        "missing_cross_refs": missing_cross_refs[:20],  # 限流
        "no_source_claims": no_source_claims,
        "topic_orphans": topic_orphans,
        "oversized_topics": oversized_topics,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="wiki 结构体检")
    parser.add_argument("--root", default=str(DEFAULT_ROOT))
    args = parser.parse_args()
    result = lint(normalize_path(args.root))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if "error" not in result else 1


if __name__ == "__main__":
    sys.exit(main())
