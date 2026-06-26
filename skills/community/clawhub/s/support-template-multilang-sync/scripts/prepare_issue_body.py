#!/usr/bin/env python3
import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description='Prepare a GitHub issue body for support template updates.')
parser.add_argument('--file', required=True, help='Updated template file path')
parser.add_argument('--languages', required=True, help='Comma-separated languages added or updated')
parser.add_argument('--wiki-status', default='pending', help='Wiki sync status')
parser.add_argument('--notes', default='', help='Optional extra notes')
args = parser.parse_args()

path = Path(args.file)
content = path.read_text(encoding='utf-8')
sections = [line.strip() for line in content.splitlines() if line.startswith('## ')]
langs = [x.strip() for x in args.languages.split(',') if x.strip()]

body = f'''## Summary
- Updated template file: `{args.file}`
- Languages added/updated: {', '.join(langs) if langs else 'N/A'}
- Wiki sync status: {args.wiki_status}

## Response Sections
'''
for s in sections:
    body += f'- {s[3:]}\n'

if args.notes:
    body += f'\n## Notes\n{args.notes}\n'

print(body)
