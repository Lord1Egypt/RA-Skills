#!/usr/bin/env python3
"""Parse public-apis README.md and build a searchable JSON database."""

import re
import json
import sys
from pathlib import Path

def parse_readme(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    apis = []
    # Find all category sections: ### CategoryName
    # Then parse table rows within each section until next ### or end
    category_pattern = re.compile(r'^### (.+)$', re.MULTILINE)
    categories = list(category_pattern.finditer(content))

    for i, cat_match in enumerate(categories):
        category = cat_match.group(1).strip()
        start = cat_match.end()
        end = categories[i + 1].start() if i + 1 < len(categories) else len(content)
        section = content[start:end]

        # Parse markdown table rows: | [Name](url) | Description | Auth | HTTPS | CORS |
        row_pattern = re.compile(
            r'\|\s*\[([^\]]+)\]\(([^)]+)\)\s*\|\s*(.+?)\s*\|\s*`?([^`|]+?)`?\s*\|\s*(Yes|No|Unknown)\s*\|\s*(Yes|No|Unknown)\s*\|'
        )

        for match in row_pattern.finditer(section):
            name = match.group(1).strip()
            url = match.group(2).strip()
            desc = match.group(3).strip()
            auth = match.group(4).strip()
            https = match.group(5).strip()
            cors = match.group(6).strip()

            # Clean up auth
            if auth.lower() in ('no', 'none', ''):
                auth = 'No'
            elif auth.startswith('$'):
                auth = auth[1:]

            apis.append({
                'name': name,
                'url': url,
                'description': desc,
                'category': category,
                'auth': auth,
                'https': https,
                'cors': cors,
            })

    return apis

def main():
    md_path = sys.argv[1] if len(sys.argv) > 1 else 'README.md'
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'apis.json'

    apis = parse_readme(md_path)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(apis, f, ensure_ascii=False, indent=2)

    print(f"Extracted {len(apis)} APIs into {output_path}")

    # Show category stats
    cats = {}
    for api in apis:
        cats[api['category']] = cats.get(api['category'], 0) + 1
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()
