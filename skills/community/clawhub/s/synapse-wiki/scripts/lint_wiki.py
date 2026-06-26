#!/usr/bin/env python3
"""
lint_wiki.py — Wiki 健康检查

检查项目:
- 死链接：目标页面不存在的 [[Target]]
- 孤立页面：没有入站链接的 Wiki 页面
- 索引缺失：未列入 wiki/index.md 的页面
- 未链接概念：在多个页面被提及 3+ 次但缺少独立页面的术语

用法:
    python3 lint_wiki.py /path/to/wiki
"""

import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict


def find_all_wikilinks(content: str) -> list:
    """Find all [[wikilinks]] in content."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def find_all_pages(wiki_root: Path) -> dict:
    """Find all wiki pages by type (recursively scan subdirectories)."""
    pages = {
        "concepts": {},
        "entities": {},
        "summaries": {},
    }

    # Recursively scan concepts directory
    for md_file in (wiki_root / "wiki" / "concepts").rglob("*.md"):
        title = extract_title(md_file.read_text(encoding="utf-8"))
        pages["concepts"][title] = md_file

    # Recursively scan entities directory
    for md_file in (wiki_root / "wiki" / "entities").rglob("*.md"):
        title = extract_title(md_file.read_text(encoding="utf-8"))
        pages["entities"][title] = md_file

    # Recursively scan summaries directory
    for md_file in (wiki_root / "wiki" / "summaries").rglob("*.md"):
        # For summaries, always use filename as title (matches wikilink format)
        # This ensures [[filename]] links work correctly
        title = md_file.stem
        pages["summaries"][title] = md_file

    return pages


def extract_title(content: str) -> str:
    """Extract title from frontmatter or first heading."""
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            fm_text = content[4:end].strip()
            for line in fm_text.split("\n"):
                if line.startswith("title:"):
                    return line.split(":", 1)[1].strip().strip('"\'')

    match = re.search(r"^# (.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    return "Untitled"


def check_dead_links(wiki_root: Path, pages: dict) -> list:
    """Check for dead wikilinks."""
    dead_links = []
    all_titles = set()

    for category in pages.values():
        all_titles.update(category.keys())

    for category in pages.values():
        for title, path in category.items():
            content = path.read_text(encoding="utf-8")
            links = find_all_wikilinks(content)

            for link in links:
                if link not in all_titles:
                    dead_links.append({
                        "source": str(path.relative_to(wiki_root)),
                        "link": link,
                    })

    return dead_links


def check_orphan_pages(wiki_root: Path, pages: dict) -> list:
    """Check for orphan pages (no inbound links)."""
    orphan_pages = []
    all_titles = set()
    all_links = set()

    for category in pages.values():
        for title, path in category.items():
            all_titles.add(title)
            content = path.read_text(encoding="utf-8")
            links = find_all_wikilinks(content)
            all_links.update(links)

    for category in pages.values():
        for title, path in category.items():
            if title not in all_links:
                orphan_pages.append(str(path.relative_to(wiki_root)))

    return orphan_pages


def check_index_coverage(wiki_root: Path, pages: dict) -> list:
    """Check for pages not listed in index.md."""
    missing_from_index = []

    index_path = wiki_root / "wiki" / "index.md"
    if not index_path.exists():
        return missing_from_index

    index_content = index_path.read_text(encoding="utf-8")

    for category in pages.values():
        for title, path in category.items():
            if f"[[{title}]]" not in index_content:
                missing_from_index.append(str(path.relative_to(wiki_root)))

    return missing_from_index


def check_unlinked_concepts(wiki_root: Path, pages: dict) -> list:
    """Check for terms mentioned 3+ times but lacking a page."""
    concept_mentions = defaultdict(int)

    for category in pages.values():
        for title, path in category.items():
            content = path.read_text(encoding="utf-8")
            headings = re.findall(r"^## (.+)$", content, re.MULTILINE)
            for h in headings:
                concept_mentions[h.strip()] += 1

    all_titles = set()
    for category in pages.values():
        all_titles.update(category.keys())

    unlinked = []
    for concept, count in concept_mentions.items():
        if count >= 3 and concept not in all_titles:
            unlinked.append({"concept": concept, "count": count})

    return unlinked


def run_lint(wiki_root: Path) -> dict:
    """Run all lint checks."""
    print(f"Linting wiki: {wiki_root}")
    print("-" * 60)

    pages = find_all_pages(wiki_root)
    total_pages = sum(len(cat) for cat in pages.values())
    print(f"Wiki pages: {total_pages}")

    results = {
        "dead_links": check_dead_links(wiki_root, pages),
        "orphan_pages": check_orphan_pages(wiki_root, pages),
        "missing_from_index": check_index_coverage(wiki_root, pages),
        "unlinked_concepts": check_unlinked_concepts(wiki_root, pages),
    }

    if results["dead_links"]:
        print("\n--- Dead Links ---")
        for item in results["dead_links"][:20]:
            print(f"  [{item['source']}] -> [[{item['link']}]]")

    if results["orphan_pages"]:
        print("\n--- Orphan Pages ---")
        for page in results["orphan_pages"][:20]:
            print(f"  {page}")

    if results["missing_from_index"]:
        print("\n--- Missing from Index ---")
        for page in results["missing_from_index"][:20]:
            print(f"  {page}")

    if results["unlinked_concepts"]:
        print("\n--- Unlinked Concepts (3+ mentions) ---")
        for item in results["unlinked_concepts"][:20]:
            print(f"  {item['concept']} ({item['count']} mentions)")

    print()
    print("-" * 60)
    print(f"Summary:")
    print(f"  Dead links: {len(results['dead_links'])}")
    print(f"  Orphan pages: {len(results['orphan_pages'])}")
    print(f"  Missing from index: {len(results['missing_from_index'])}")
    print(f"  Unlinked concepts: {len(results['unlinked_concepts'])}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Wiki 健康检查（死链接/孤立页面/缺失索引）")
    parser.add_argument("wiki", help="Wiki 根目录路径")
    args = parser.parse_args()

    wiki_root = Path(args.wiki).resolve()

    if not wiki_root.exists():
        print(f"Error: Wiki root not found: {wiki_root}")
        sys.exit(1)

    results = run_lint(wiki_root)

    issues = (
        len(results["dead_links"]) +
        len(results["orphan_pages"]) +
        len(results["missing_from_index"]) +
        len(results["unlinked_concepts"])
    )

    if issues > 0:
        print(f"\n⚠ {issues} issues found")
    else:
        print("\n✅ Wiki is healthy!")

    sys.exit(0 if issues == 0 else 1)


if __name__ == "__main__":
    main()
