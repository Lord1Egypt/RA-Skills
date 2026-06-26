#!/usr/bin/env python3
import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
NOTION_VERSION = "2025-09-03"


def notion_headers():
    key = os.environ.get("NOTION_API_KEY") or os.environ.get("NOTION_TOKEN")
    if not key:
        raise SystemExit("Missing NOTION_API_KEY/NOTION_TOKEN")
    return {
        "Authorization": f"Bearer {key}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    }


def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", "ignore")


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'\\x([0-9a-fA-F]{2})', lambda m: chr(int(m.group(1), 16)), text)
    return html.unescape(text).strip()


def extract_metadata(html_data: str):
    title = "Unknown Title"
    m = re.search(r'property="og:title" content="(.*?)"', html_data)
    if m:
        title = clean_text(m.group(1))
    else:
        m = re.search(r'window\.msg_title = window\.title = [\'\"](.*?)[\'\"]', html_data)
        if not m:
            m = re.search(r'var msg_title = [\'\"](.*?)[\'\"]', html_data)
        if m:
            title = clean_text(m.group(1))

    author = "Unknown"
    m = re.search(r'property="og:article:author" content="(.*?)"', html_data)
    if m:
        author = clean_text(m.group(1))
    else:
        m = re.search(r'nickname: JsDecode\([\'\"](.*?)[\'\"]\)', html_data)
        if not m:
            m = re.search(r'var nickname = ["\'](.*?)["\'];', html_data)
        if m:
            author = clean_text(m.group(1))

    publish_date = "Unknown"
    m = re.search(r'var (?:ct|create_time) = ["\'](\d+)["\']', html_data)
    if m:
        try:
            publish_date = dt.datetime.fromtimestamp(int(m.group(1))).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            pass
    return title, author, publish_date


def parse_article(html_data: str):
    start_match = re.search(r'id=["\']?js_content["\']?', html_data)
    if not start_match:
        desc_match = re.search(r'name="description"\s+content="(.*?)"', html_data, re.S)
        if desc_match:
            return [{"type": "paragraph", "text": clean_text(desc_match.group(1))}]
        return [{"type": "paragraph", "text": "Content container (js_content) not found."}]

    start_idx = start_match.start()
    tag_start = html_data.rfind('<div', 0, start_idx)
    if tag_start == -1:
        tag_start = start_idx
    content_area = html_data[tag_start:]

    end_idx = len(content_area)
    for pattern in [r'id="qr_code"', r'id="js_pc_qr_code"', r'id="js_view_source"', r'<(script|style)']:
        m = re.search(pattern, content_area)
        if m and m.start() < end_idx:
            end_idx = m.start()
    content_html = content_area[:end_idx]

    blocks = []

    def add_text_block(text, block_type="paragraph"):
        text = clean_text(text)
        if text:
            blocks.append({"type": block_type, "text": text})

    img_pattern = re.compile(r'<img[^>]+(?:data-src|src)=["\'](.*?)["\'][^>]*>', re.S | re.I)
    pos = 0
    for m in img_pattern.finditer(content_html):
        before = content_html[pos:m.start()]
        before = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', before, flags=re.S | re.I)
        before = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', before, flags=re.S | re.I)
        before = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', before, flags=re.S | re.I)
        before = re.sub(r'<(p|br|div|section|li|tr|blockquote)[^>]*>', '\n', before, flags=re.I)
        before = re.sub(r'<[^>]+>', '', before)
        for line in before.split('\n'):
            line = clean_text(line)
            if not line:
                continue
            if line.startswith('### '):
                blocks.append({"type": "heading_3", "text": line[4:]})
            elif line.startswith('## '):
                blocks.append({"type": "heading_2", "text": line[3:]})
            elif line.startswith('# '):
                blocks.append({"type": "heading_1", "text": line[2:]})
            else:
                blocks.append({"type": "paragraph", "text": line})
        img_url = m.group(1)
        if img_url.startswith('//'):
            img_url = 'https:' + img_url
        if img_url.startswith('http'):
            blocks.append({"type": "image", "url": img_url})
        pos = m.end()

    tail = content_html[pos:]
    tail = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\n# \1\n', tail, flags=re.S | re.I)
    tail = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n## \1\n', tail, flags=re.S | re.I)
    tail = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', tail, flags=re.S | re.I)
    tail = re.sub(r'<(p|br|div|section|li|tr|blockquote)[^>]*>', '\n', tail, flags=re.I)
    tail = re.sub(r'<[^>]+>', '', tail)
    for line in tail.split('\n'):
        line = clean_text(line)
        if not line:
            continue
        if line.startswith('### '):
            blocks.append({"type": "heading_3", "text": line[4:]})
        elif line.startswith('## '):
            blocks.append({"type": "heading_2", "text": line[3:]})
        elif line.startswith('# '):
            blocks.append({"type": "heading_1", "text": line[2:]})
        else:
            blocks.append({"type": "paragraph", "text": line})

    deduped = []
    last = None
    for b in blocks:
        if b != last:
            deduped.append(b)
            last = b
    return deduped


def notion_request(method, url, data=None):
    body = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(url, data=body, headers=notion_headers(), method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())


def text_obj(content):
    return {"type": "text", "text": {"content": content[:2000]}}


def block_from_item(item):
    t = item["type"]
    if t.startswith("heading_"):
        return {"object": "block", "type": t, t: {"rich_text": [text_obj(item["text"])]}}
    if t == "image":
        return {"object": "block", "type": "image", "image": {"type": "external", "external": {"url": item["url"]}}}
    return {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(item["text"])]}}


def create_page(parent_id, parent_type, title, author, publish_date, source_url):
    if parent_type == "database":
        payload = {
            "parent": {"database_id": parent_id},
            "properties": {
                "Name": {"title": [{"text": {"content": title[:80]}}]}
            },
            "children": [
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(f"Author: {author}")]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(f"Publish date: {publish_date}")]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(f"Source: {source_url}")]}}
            ]
        }
    else:
        payload = {
            "parent": {"page_id": parent_id},
            "properties": {"title": {"title": [{"text": {"content": title[:100]}}]}},
            "children": [
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(f"Author: {author}")]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(f"Publish date: {publish_date}")]}},
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [text_obj(f"Source: {source_url}")]}}
            ]
        }
    return notion_request("POST", "https://api.notion.com/v1/pages", payload)


def append_blocks(page_id, items):
    blocks = [block_from_item(x) for x in items]
    for i in range(0, len(blocks), 80):
        payload = {"children": blocks[i:i+80]}
        notion_request("PATCH", f"https://api.notion.com/v1/blocks/{page_id}/children", payload)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("wechat_url")
    ap.add_argument("notion_parent_id")
    ap.add_argument("--parent-type", choices=["page", "database"], default="page")
    args = ap.parse_args()

    html_data = fetch(args.wechat_url)
    title, author, publish_date = extract_metadata(html_data)
    content_items = parse_article(html_data)

    page = create_page(args.notion_parent_id, args.parent_type, title, author, publish_date, args.wechat_url)
    append_blocks(page["id"], content_items)
    print(json.dumps({
        "title": title,
        "author": author,
        "publish_date": publish_date,
        "page_id": page["id"],
        "url": page.get("url")
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
