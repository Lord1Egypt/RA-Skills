#!/usr/bin/env python3
"""
Save parsed WeChat article blocks to a Notion database.
Usage: python3 save_to_notion.py <article_json_file> <notion_url> <article_url> [read_time] [keywords] [comment] [rating]

- article_json_file: output from fetch_wechat.py
- notion_url: Notion database URL (https://www.notion.so/xxx?v=yyy)
- article_url: original WeChat article URL
- read_time: ISO datetime string (default: now, Asia/Shanghai)
- keywords: comma-separated string (optional)
- comment: short comment string (optional, posted as page comment)
- rating: integer 1-5 star rating (optional; 3+ auto-adds "Featured" tag)

Field mapping is auto-detected from the database schema by field type:
  title → article title
  url   → article URL
  date  → read time
  select → star rating
  multi_select → keywords
"""

import sys
import json
import subprocess
import re
import os
import time
from datetime import datetime, timezone, timedelta


def load_key():
    # NOTION_API_KEY is injected by OpenClaw from skills.entries.notion.apiKey in openclaw.json
    key = os.environ.get('NOTION_API_KEY', '').strip()
    if key:
        return key
    print(
        'ERROR: Notion API key not found.\n'
        'Configure it in OpenClaw: skills.entries.notion.apiKey = "ntn_xxx"\n'
        '\n'
        'Get your key at https://notion.so/my-integrations\n'
        'Then share your Notion database with the integration ("..." → "Connect to").',
        file=sys.stderr
    )
    sys.exit(1)


def extract_db_id(notion_url):
    m = re.search(r'notion\.so/([a-f0-9]{32})', notion_url)
    if m:
        raw = m.group(1)
        return f'{raw[:8]}-{raw[8:12]}-{raw[12:16]}-{raw[16:20]}-{raw[20:]}'
    m = re.search(r'([a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12})', notion_url)
    if m:
        return m.group(1)
    return None


def notion_request(method, path, body=None, key=None):
    cmd = ['curl', '-s', '-X', method,
           f'https://api.notion.com/v1{path}',
           '-H', f'Authorization: Bearer {key}',
           '-H', 'Notion-Version: 2025-09-03',
           '-H', 'Content-Type: application/json']
    if body:
        cmd += ['-d', json.dumps(body)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if not result.stdout.strip():
        return {}
    return json.loads(result.stdout)


def detect_fields(db_id, key):
    """
    Auto-detect field names by type. Returns a dict mapping semantic role to field name:
      { 'title': 'Title', 'url': 'URL', 'date': 'Read Time', 'multi_select': 'Tags' }

    Strategy:
    1. Try GET /databases/{id} for standard databases (returns properties in schema)
    2. Fall back to GET /search to find a page in this database and infer from its properties
    """
    def _parse_props(props):
        mapping = {}
        for name, prop in props.items():
            t = prop.get('type')
            if t == 'title' and 'title' not in mapping:
                mapping['title'] = name
            elif t == 'url' and 'url' not in mapping:
                mapping['url'] = name
            elif t == 'date' and 'date' not in mapping:
                mapping['date'] = name
            elif t == 'select' and 'select' not in mapping:
                mapping['select'] = name
            elif t == 'multi_select' and 'multi_select' not in mapping:
                mapping['multi_select'] = name
        return mapping

    # Try database schema first (use 2022-06-28 — newer versions omit properties)
    cmd = ['curl', '-s', f'https://api.notion.com/v1/databases/{db_id}',
           '-H', f'Authorization: Bearer {key}',
           '-H', 'Notion-Version: 2022-06-28']
    r = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)
    props = r.get('properties', {})
    if props:
        return _parse_props(props)

    # Fall back: search for pages in this database
    r = notion_request('POST', '/search', {
        'filter': {'value': 'page', 'property': 'object'},
        'page_size': 5
    }, key=key)
    for result in r.get('results', []):
        parent = result.get('parent', {})
        if parent.get('database_id', '').replace('-', '') == db_id.replace('-', ''):
            props = result.get('properties', {})
            if props:
                return _parse_props(props)

    # Final fallback: use default English field names
    print('  WARNING: could not detect fields from database, using default English field names.', file=sys.stderr)
    return {
        'title': 'Title',
        'url': 'URL',
        'date': 'Read Time',
        'select': 'Rating',
        'multi_select': 'Tags',
    }


def make_notion_block(b):
    t = b['type']
    if t == 'image':
        return {'object': 'block', 'type': 'image', 'image': {'type': 'external', 'external': {'url': b['url']}}}
    if t == 'code':
        return {'object': 'block', 'type': 'code', 'code': {
            'rich_text': [{'type': 'text', 'text': {'content': b['text'][:2000]}}],
            'language': 'plain text'
        }}
    rt = []
    for r in b.get('rich_text', []):
        run = {'type': 'text', 'text': {'content': r['text']['content'][:2000]}}
        if r.get('annotations'):
            run['annotations'] = r['annotations']
        rt.append(run)
    if not rt:
        rt = [{'type': 'text', 'text': {'content': ''}}]
    if t == 'heading_2':
        return {'object': 'block', 'type': 'heading_2', 'heading_2': {'rich_text': rt}}
    if t == 'bulleted_list_item':
        return {'object': 'block', 'type': 'bulleted_list_item', 'bulleted_list_item': {'rich_text': rt}}
    return {'object': 'block', 'type': 'paragraph', 'paragraph': {'rich_text': rt}}


STAR_MAP = {1: '⭐', 2: '⭐⭐', 3: '⭐⭐⭐', 4: '⭐⭐⭐⭐', 5: '⭐⭐⭐⭐⭐'}


def save(article_path, notion_url, article_url, read_time=None, keywords=None, comment=None, rating=None):
    key = load_key()
    db_id = extract_db_id(notion_url)
    if not db_id:
        print('ERROR: could not extract database id from URL', file=sys.stderr)
        sys.exit(1)

    with open(article_path) as f:
        d = json.load(f)

    if read_time is None:
        read_time = datetime.now().astimezone().strftime('%Y-%m-%dT%H:%M:%S%z')
        # Format offset as +HH:MM (insert colon): +0800 → +08:00
        if len(read_time) >= 5 and read_time[-5] in ('+', '-') and ':' not in read_time[-5:]:
            read_time = read_time[:-2] + ':' + read_time[-2:]

    # Auto-detect field names from database schema
    fields = detect_fields(db_id, key)
    print(f'  Detected fields: {fields}')

    missing = [r for r in ('title', 'url', 'date') if r not in fields]
    if missing:
        print(f'ERROR: database is missing required field types: {missing}', file=sys.stderr)
        print('Please ensure your database has Title, URL, and Date fields.', file=sys.stderr)
        sys.exit(1)

    # Auto-add "Featured" tag for rating >= 3
    if rating and rating >= 3:
        keywords = keywords or []
        if 'Featured' not in keywords:
            keywords.append('Featured')

    if keywords:
        print(f'  Keywords: {", ".join(keywords)}')
    if rating:
        print(f'  Rating: {STAR_MAP.get(rating, rating)}')

    # Build properties using detected field names
    properties = {
        fields['title']: {'title': [{'text': {'content': d['title']}}]},
        fields['url']:   {'url': article_url},
        fields['date']:  {'date': {'start': read_time}},
    }
    if rating and 'select' in fields:
        properties[fields['select']] = {'select': {'name': STAR_MAP.get(rating, str(rating))}}
    if keywords and 'multi_select' in fields:
        properties[fields['multi_select']] = {'multi_select': [{'name': k} for k in keywords]}

    # Create page
    page = notion_request('POST', '/pages', {
        'parent': {'database_id': db_id},
        'properties': properties,
    }, key=key)

    page_id = page.get('id')
    if not page_id:
        print(f'ERROR creating page: {page.get("message","")}', file=sys.stderr)
        sys.exit(1)
    print(f'Created page: {page_id}')

    # Write blocks in batches of 100
    blocks = [make_notion_block(b) for b in d['blocks']]
    total = 0
    for i in range(0, len(blocks), 100):
        batch = blocks[i:i+100]
        r = notion_request('PATCH', f'/blocks/{page_id}/children', {'children': batch}, key=key)
        if r.get('object') == 'list':
            total += len(batch)
            print(f'  batch {i//100+1}: ok ({len(batch)} blocks)')
        else:
            print(f'  batch {i//100+1}: error - {r.get("message","")}', file=sys.stderr)
        time.sleep(0.4)

    print(f'Done: {total} blocks written')

    # Write comment
    if comment:
        r = notion_request('POST', '/comments', {
            'parent': {'page_id': page_id},
            'rich_text': [{'type': 'text', 'text': {'content': comment}}]
        }, key=key)
        if r.get('object') == 'comment':
            print(f'Comment: {comment}')
        else:
            print(f'Comment failed: {r.get("message","")}', file=sys.stderr)

    return page_id


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: save_to_notion.py <article_json> <notion_url> <article_url> [read_time] [keywords] [comment] [rating]',
              file=sys.stderr)
        sys.exit(1)
    article_path = sys.argv[1]
    notion_url = sys.argv[2]
    article_url = sys.argv[3]
    read_time = sys.argv[4] if len(sys.argv) > 4 else None
    keywords = [k.strip() for k in sys.argv[5].replace('，', ',').split(',') if k.strip()] if len(sys.argv) > 5 else None
    comment = sys.argv[6].strip() if len(sys.argv) > 6 else None
    rating = int(sys.argv[7]) if len(sys.argv) > 7 else None
    save(article_path, notion_url, article_url, read_time, keywords, comment, rating)
