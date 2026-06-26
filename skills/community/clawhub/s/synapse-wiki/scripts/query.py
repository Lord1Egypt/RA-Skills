#!/usr/bin/env python3
"""
query.py — Query the Wiki knowledge base

用法:
    python3 query.py /path/to/wiki "query text"

功能:
1. 验证 wiki/index.md 存在
2. 读取 index.md 找到相关页面
3. 综合答案并保存
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime


def find_relevant_pages(index_content: str, query: str) -> list:
    """Find potentially relevant pages from index based on query keywords."""
    query_keywords = query.lower().split()
    relevant = []

    for line in index_content.split('\n'):
        if line.startswith('- [['):
            # Extract page title and summary
            match = re.match(r'- \[\[([^\]]+)\]\] — (.+)', line)
            if match:
                title, summary = match.groups()
                # Check if any keyword matches
                text = (title + ' ' + summary).lower()
                if any(kw in text for kw in query_keywords if len(kw) > 2):
                    relevant.append({'title': title, 'summary': summary})

    return relevant[:10]  # Limit to top 10


def read_wiki_pages(wiki_root: Path, pages: list) -> list:
    """Read full content of wiki pages."""
    results = []

    # Search in all wiki directories
    for category in ['concepts', 'entities', 'summaries']:
        cat_dir = wiki_root / 'wiki' / category
        if not cat_dir.exists():
            continue

        for md_file in cat_dir.glob('*.md'):
            content = md_file.read_text(encoding='utf-8')
            title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
            if title_match:
                title = title_match.group(1).strip()
                # 如果 pages 为空则跳过（没有匹配到 index 条目），否则检查标题是否匹配
                if pages and any(p['title'] == title for p in pages):
                    results.append({
                        'path': str(md_file.relative_to(wiki_root)),
                        'title': title,
                        'content': content
                    })

    return results


def synthesize_answer(query: str, pages: list) -> str:
    """Synthesize an answer from the pages."""
    if not pages:
        return f"没有找到与 \"{query}\" 相关的 Wiki 页面。\n\n建议：\n1. 使用 /synapse-wiki ingest 摄取更多资料\n2. 检查查询关键词"

    answer = [
        f"# 查询：{query}",
        f"\n*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "\n---\n",
    ]

    for page in pages[:5]:  # Limit to 5 pages for context
        answer.append(f"\n## {page['title']}\n")
        # Extract main content (skip frontmatter and first heading)
        content = page['content']
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                content = content[end+3:].strip()
        answer.append(content)
        answer.append(f"\n*来源：{page['path']}*")

    return '\n'.join(answer)


def save_query_result(wiki_root: Path, query: str, answer: str):
    """Save query result to outputs/queries/."""
    output_dir = wiki_root / 'outputs' / 'queries'
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = query.lower().replace(' ', '-').replace('?', '')[:30]
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    output_path = output_dir / f"{timestamp}-{slug}.md"

    output_path.write_text(answer, encoding='utf-8')
    return output_path


def query_wiki(wiki_root: Path, query: str) -> str:
    """Query the wiki and return synthesized answer."""
    index_path = wiki_root / 'wiki' / 'index.md'

    if not index_path.exists():
        return "Error: wiki/index.md not found. Please initialize or ingest first."

    index_content = index_path.read_text(encoding='utf-8')

    # Find relevant pages
    relevant_pages = find_relevant_pages(index_content, query)

    # Read full page content
    pages = read_wiki_pages(wiki_root, relevant_pages)

    # Synthesize answer
    answer = synthesize_answer(query, pages)

    # Save result
    output_path = save_query_result(wiki_root, query, answer)

    return f"{answer}\n\n---\n\n答案已保存至：{output_path}"


def main():
    parser = argparse.ArgumentParser(description="查询 Wiki 知识库")
    parser.add_argument("wiki", help="Wiki 根目录路径")
    parser.add_argument("query", help="查询文本")
    args = parser.parse_args()

    wiki_root = Path(args.wiki).resolve()
    query = args.query

    if not wiki_root.exists():
        print(f"Error: Wiki root not found: {wiki_root}")
        sys.exit(1)

    print(f"Querying wiki: {wiki_root}")
    print(f"Query: {query}")
    print("=" * 60)

    result = query_wiki(wiki_root, query)
    print(result)


if __name__ == "__main__":
    main()
