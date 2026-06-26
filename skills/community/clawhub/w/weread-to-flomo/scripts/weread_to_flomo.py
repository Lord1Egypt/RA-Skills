#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List
from zoneinfo import ZoneInfo

TZ = ZoneInfo('Asia/Shanghai')
BOOKMARK_RE = re.compile(
    r'<!-- bookmarkId: (?P<id>.+?) -->\n'
    r'<!-- time: (?P<time>.+?) -->\n'
    r'<!-- chapterUid: (?P<chapter>.+?) -->\n\n'
    r'> (?P<quote>.*?)(?=\n<!-- bookmarkId: |\n<!-- reviewId: |\n\n### |\n\n## |\Z)',
    re.S,
)
REVIEW_RE = re.compile(
    r'<!-- reviewId: (?P<id>.+?) -->\n'
    r'<!-- time: (?P<time>.+?) -->\n'
    r'<!-- chapterUid: (?P<chapter>.*?) -->\n\n'
    r'>(?P<body>.*?)(?=\n<!-- reviewId: |\n<!-- bookmarkId: |\n\n### |\n\n## |\Z)',
    re.S,
)
TITLE_RE = re.compile(r'^title:\s*"?(.*?)"?$', re.M)
CHAPTER_HEAD_RE = re.compile(r'^###\s+(.+)$', re.M)


@dataclass
class Entry:
    kind: str
    entry_id: str
    created: datetime
    book_title: str
    chapter_name: str
    content: str

    @property
    def unique_key(self) -> str:
        return f'{self.kind}:{self.entry_id}'


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding='utf-8'))
    return {'sent': {}}


def save_state(path: Path, state: dict) -> None:
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def parse_frontmatter_value(pattern: re.Pattern[str], text: str, fallback: str = '') -> str:
    m = pattern.search(text)
    return (m.group(1).strip() if m else fallback).strip()


def normalize_quote(text: str) -> str:
    lines = []
    for raw in text.strip().splitlines():
        line = raw.strip()
        if line.startswith('>'):
            line = line[1:].strip()
        if line:
            lines.append(line)
    return '\n'.join(lines).strip()


def parse_markdown_file(path: Path) -> List[Entry]:
    text = path.read_text(encoding='utf-8')
    title = parse_frontmatter_value(TITLE_RE, text, path.stem)
    entries: List[Entry] = []
    chapter_positions = [(m.start(), m.group(1).strip()) for m in CHAPTER_HEAD_RE.finditer(text)]

    def chapter_for(pos: int) -> str:
        current = ''
        for start, name in chapter_positions:
            if start > pos:
                break
            current = name
        return current

    for m in BOOKMARK_RE.finditer(text):
        created = datetime.fromisoformat(m.group('time').replace('Z', '+00:00')).astimezone(TZ)
        quote = normalize_quote(m.group('quote'))
        if quote:
            entries.append(Entry('bookmark', m.group('id').strip(), created, title, chapter_for(m.start()), quote))

    for m in REVIEW_RE.finditer(text):
        created = datetime.fromisoformat(m.group('time').replace('Z', '+00:00')).astimezone(TZ)
        body = normalize_quote(m.group('body'))
        if body:
            entries.append(Entry('review', m.group('id').strip(), created, title, chapter_for(m.start()), body))

    return entries


def build_flomo_content(entry: Entry, tag_prefix: str) -> str:
    return f"{entry.content}\n\n#{tag_prefix} #{tag_prefix}/「{entry.book_title}」"


def post_to_flomo(webhook: str, content: str) -> dict:
    data = urllib.parse.urlencode({'content': content}).encode()
    req = urllib.request.Request(webhook, data=data, method='POST')
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode('utf-8', 'ignore'))


def should_include(entry: Entry, mode: str, target_date: datetime | None) -> bool:
    if mode == 'all':
        return True
    if mode == 'today':
        return entry.created.date() == datetime.now(TZ).date()
    if mode == 'date' and target_date is not None:
        return entry.created.date() == target_date.date()
    return False


def main() -> None:
    parser = argparse.ArgumentParser(description='Sync WeRead Markdown exports to flomo')
    parser.add_argument('--weread-dir', required=True)
    parser.add_argument('--flomo-webhook', required=True)
    parser.add_argument('--mode', choices=['today', 'date', 'all'], default='today')
    parser.add_argument('--date', help='YYYY-MM-DD when mode=date')
    parser.add_argument('--state-file')
    parser.add_argument('--tag-prefix', default='02_读书')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    weread_dir = Path(args.weread_dir)
    state_path = Path(args.state_file) if args.state_file else weread_dir / '.weread-flomo-state.json'
    target_date = datetime.strptime(args.date, '%Y-%m-%d').replace(tzinfo=TZ) if args.date else None
    state = load_state(state_path)
    sent = state.setdefault('sent', {})

    entries: List[Entry] = []
    for path in sorted(weread_dir.glob('*.md')):
        entries.extend(parse_markdown_file(path))
    entries = [e for e in entries if should_include(e, args.mode, target_date)]
    entries.sort(key=lambda e: (e.created, e.book_title, e.entry_id))

    newly_sent = 0
    for entry in entries:
        if entry.unique_key in sent:
            continue
        content = build_flomo_content(entry, args.tag_prefix)
        if args.dry_run:
            print('---')
            print(entry.unique_key, entry.created.isoformat(), entry.book_title)
            print(content)
            continue
        result = post_to_flomo(args.flomo_webhook, content)
        if result.get('code') != 0:
            raise RuntimeError(f'flomo error for {entry.unique_key}: {result}')
        sent[entry.unique_key] = {
            'sentAt': datetime.now(TZ).isoformat(),
            'bookTitle': entry.book_title,
            'created': entry.created.isoformat(),
            'kind': entry.kind,
            'slug': result.get('memo', {}).get('slug', ''),
            'hash': hashlib.sha256(content.encode('utf-8')).hexdigest(),
        }
        newly_sent += 1
        print(f'Sent {entry.unique_key} -> flomo ({entry.book_title})')

    if not args.dry_run:
        save_state(state_path, state)
    print(f'Done. mode={args.mode} candidates={len(entries)} newly_sent={newly_sent}')


if __name__ == '__main__':
    main()
