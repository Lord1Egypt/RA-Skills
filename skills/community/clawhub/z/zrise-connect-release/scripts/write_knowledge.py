#!/usr/bin/env python3
"""
Write content to Zrise knowledge.article.
Creates new article or updates existing one with HTML content.

Usage:
    python3 write_knowledge.py --title "Article Title" --body "Markdown content"
    python3 write_knowledge.py --title "Title" --body-file result.md
    python3 write_knowledge.py --article-id 2219 --body "Updated content"
    python3 write_knowledge.py --title "Title" --body "Content" --parent-id 617 --permission write
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from zrise_utils import connect_zrise

try:
    import markdown as md
except ImportError:
    md = None


def md_to_html(text):
    """Extract content from JSON wrapper, return as-is (Odoo knowledge uses HTML, not markdown)."""
    # Extract from JSON wrapper if present
    s = text.strip()
    if s.startswith('{'):
        depth, end = 0, -1
        for i, c in enumerate(s):
            if c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: end = i + 1; break
        if end > 0:
            try:
                parsed = json.loads(s[:end])
                for key in ('output', 'result', 'content', 'text', 'response'):
                    val = parsed.get(key)
                    if isinstance(val, str) and len(val) > 50:
                        text = val
                        break
                    elif isinstance(val, dict):
                        for k2 in ('output', 'content', 'text'):
                            v2 = val.get(k2)
                            if isinstance(v2, str) and len(v2) > 50:
                                text = v2
                                break
            except (json.JSONDecodeError, TypeError):
                pass
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--title', help='Article title (for new article)')
    parser.add_argument('--body', help='Markdown/HTML body content')
    parser.add_argument('--body-file', help='Path to file with body content')
    parser.add_argument('--article-id', type=int, help='Update existing article')
    parser.add_argument('--parent-id', type=int, help='Parent article ID')
    parser.add_argument('--permission', choices=['none', 'read', 'write'], default='read')
    parser.add_argument('--icon', default='📄', help='Article icon emoji')
    parser.add_argument('--category', choices=['workspace', 'private', 'shared'], default='workspace')
    parser.add_argument('--is-published', action='store_true')
    args = parser.parse_args()

    # Get body content
    if args.body_file:
        content = Path(args.body_file).read_text(encoding='utf-8')
    elif args.body:
        content = args.body
    else:
        parser.error('Need --body or --body-file')

    body_html = md_to_html(content)

    db, uid, secret, models, url = connect_zrise()

    if args.article_id:
        # Update existing
        models.execute_kw(db, uid, secret, 'knowledge.article', 'write',
                          [[args.article_id], {'body': body_html}])
        article_id = args.article_id
        mode = 'updated'
    else:
        if not args.title:
            parser.error('Need --title for new article')
        # Create new
        vals = {
            'name': args.title,
            'body': body_html,
            'internal_permission': args.permission,
            'icon': args.icon,
            'is_published': args.is_published,
        }
        if args.parent_id:
            vals['parent_id'] = args.parent_id

        article_id = models.execute_kw(db, uid, secret, 'knowledge.article', 'create', [vals])
        mode = 'created'

    # Read back to confirm
    res = models.execute_kw(db, uid, secret, 'knowledge.article', 'read',
                            [[article_id]], {'fields': ['id', 'name', 'article_url']})

    output = {
        'ok': True,
        'article_id': article_id,
        'title': args.title or res[0]['name'],
        'url': res[0].get('article_url', ''),
        'mode': mode,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
