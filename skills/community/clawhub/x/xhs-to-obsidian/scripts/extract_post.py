#!/usr/bin/env python3
"""Extract Xiaohongshu post content from URL using cookies."""

import json
import urllib.request
import urllib.error
import ssl
import re
import sys
import os
import argparse
from datetime import datetime


def load_cookies(cookie_path: str) -> str:
    with open(cookie_path) as f:
        cookies = json.load(f)
    return '; '.join(f"{c['name']}={c['value']}" for c in cookies)


def extract_post_id(url: str) -> tuple[str, str]:
    """Extract note ID and xsec_token from URL."""
    # Pattern: xiaohongshu.com/explore/xxx or xiaohongshu.com/discovery/item/xxx
    patterns = [
        r'xiaohongshu\.com/explore/([a-f0-9]{24})',
        r'xiaohongshu\.com/discovery/item/([a-f0-9]{24})',
    ]
    for p in patterns:
        m = re.search(p, url)
        if m:
            post_id = m.group(1)
            xsec_m = re.search(r'xsec_token=([a-f0-9]+)', url)
            xsec = xsec_m.group(1) if xsec_m else ''
            return post_id, xsec
    raise ValueError(f"Cannot parse post ID from URL: {url}")


def fetch_post(url: str, cookie_str: str) -> dict:
    """Fetch and parse post data from __INITIAL_STATE__."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = urllib.request.Request(url)
    req.add_header('Cookie', cookie_str)
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
    req.add_header('Referer', 'https://www.xiaohongshu.com/')

    try:
        resp = urllib.request.urlopen(req, timeout=15, context=ctx)
        html = resp.read().decode('utf-8', errors='ignore')
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise ValueError("POST_NOT_AVAILABLE")
        raise

    # Handle redirect to error page
    if '404' in resp.geturl() or 'error' in resp.geturl():
        raise ValueError("POST_NOT_AVAILABLE")

    m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.+?\}\s*)\s*</script>', html, re.DOTALL)
    if not m:
        raise ValueError("Cannot find __INITIAL_STATE__ in page")
    raw = m.group(1).replace('undefined', 'null')
    data = json.loads(raw)

    # Navigate to note data
    note_map = data.get('note', {}).get('noteDetailMap', {})
    key = list(note_map.keys())[0]
    note = note_map[key]['note']
    return note


def format_interact(interact: dict) -> str:
    liked = interact.get('likedCount', 'N/A')
    collected = interact.get('collectedCount', 'N/A')
    comment = interact.get('commentCount', 'N/A')
    return f"{liked}赞 / {collected}收藏 / {comment}评论"


def build_markdown(note: dict, video_transcript: str = None) -> str:
    """Build Obsidian markdown from note data."""
    title = note.get('title', '') or note.get('desc', '')[:30]
    short_title = title[:15] if len(title) > 15 else title
    date = datetime.fromtimestamp(note.get('time', 0)).strftime('%Y-%m-%d') if note.get('time') else ''
    author = note.get('user', {}).get('nickname', '未知')
    post_id = note.get('noteId', '')
    post_url = f"https://www.xiaohongshu.com/explore/{post_id}"
    post_type = note.get('type', 'image')
    interact = note.get('interactInfo', {})
    tags = ', '.join(note.get('tagList', [])) or '无'

    # Image list
    images = note.get('imageList', [])
    img_md = ''
    for i, img in enumerate(images):
        img_url = img.get('urlDefault', img.get('url', ''))
        if img_url:
            img_md += f"\n![图{i+1}]({img_url})"

    # Core content
    desc = note.get('desc', '')
    # Clean tag marks
    desc_clean = re.sub(r'#\S+#', '', desc).strip()

    # Video transcript section
    transcript_md = ''
    if video_transcript:
        transcript_md = f"\n\n## 视频转录\n\n{video_transcript}"

    md = f"""# {title}

{desc_clean}{img_md}{transcript_md}

---

> **来源**: 小红书 · {author}  
> **日期**: {date}  
> **互动**: {format_interact(interact)}  
> **标签**: {tags}  
> **链接**: {post_url}
"""
    return md


def save_markdown(content: str, title: str, output_dir: str, date: str) -> str:
    """Save markdown file to Obsidian vault."""
    short_title = title[:15].replace('/', '-').replace('\\', '-')
    filename = f"{date} {short_title}.md"
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def main():
    parser = argparse.ArgumentParser(description='Extract Xiaohongshu post to Obsidian markdown')
    parser.add_argument('url', help='Xiaohongshu post URL')
    parser.add_argument('--cookies', default='~/cookies.json', help='Cookies file path')
    parser.add_argument('--output', default='~/Documents/Obsidian Vault/xhs', help='Obsidian vault path')
    parser.add_argument('--output-json', action='store_true', help='Output result as JSON')
    args = parser.parse_args()

    cookie_path = os.path.expanduser(args.cookies)
    output_dir = os.path.expanduser(args.output)

    if not os.path.exists(cookie_path):
        result = {'error': 'COOKIES_NOT_FOUND', 'cookie_path': cookie_path}
        print(json.dumps(result))
        sys.exit(1)

    cookie_str = load_cookies(cookie_path)
    post_id, xsec = extract_post_id(args.url)
    url_with_token = args.url
    if xsec:
        url_with_token = args.url if 'xsec_token' in args.url else f"{args.url}&xsec_token={xsec}"

    try:
        note = fetch_post(url_with_token, cookie_str)
    except ValueError as e:
        if str(e) == 'POST_NOT_AVAILABLE':
            result = {'error': 'POST_NOT_AVAILABLE', 'message': 'This post is not available or requires login'}
        elif str(e) == 'COOKIES_EXPIRED':
            result = {'error': 'COOKIES_EXPIRED', 'message': 'Cookies expired, please re-export from Chrome'}
        else:
            result = {'error': 'PARSE_ERROR', 'message': str(e)}
        print(json.dumps(result))
        sys.exit(1)
    except Exception as e:
        result = {'error': 'FETCH_ERROR', 'message': str(e)}
        print(json.dumps(result))
        sys.exit(1)

    # Build markdown
    video_transcript = None
    if note.get('type') == 'video' and note.get('video', {}).get('media', {}).get('stream'):
        # For now, just include video info (transcription requires ffmpeg + whisper)
        stream = note['video']['media']['stream']
        # Try to get masterUrl from available streams
        master_url = None
        for s in stream:
            if s.get('masterUrl'):
                master_url = s['masterUrl']
                break
        if master_url:
            # Signal that video needs transcription
            note['_video_url'] = master_url

    md_content = build_markdown(note, video_transcript)
    date_str = datetime.fromtimestamp(note.get('time', 0)).strftime('%Y-%m-%d') if note.get('time') else datetime.now().strftime('%Y-%m-%d')
    os.makedirs(output_dir, exist_ok=True)
    filepath = save_markdown(md_content, note.get('title', 'untitled') or note.get('desc', '')[:30], output_dir, date_str)

    result = {
        'success': True,
        'filepath': filepath,
        'post_id': note.get('noteId', ''),
        'title': note.get('title', ''),
        'type': note.get('type', 'image'),
        'date': date_str,
        'video_url': note.get('_video_url'),
    }
    print(json.dumps(result))


if __name__ == '__main__':
    main()
