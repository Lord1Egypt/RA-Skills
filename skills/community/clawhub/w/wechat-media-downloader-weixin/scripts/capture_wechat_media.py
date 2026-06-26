#!/usr/bin/env python3
import argparse, json, os, re, time, urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright

MEDIA_HINTS = ['videourl','playurl','music','voice','audio','mpvideo','qqmusic','kugou','m4a','mp3','m3u8']


def consider(url, kind, seen, captured):
    if not url or url in seen:
        return
    u = url.lower()
    if any(h in u for h in MEDIA_HINTS) or re.search(r'\.(mp4|m4a|mp3|aac|wav|flac|ogg|webm|m3u8)(\?|$)', u):
        seen.add(url)
        captured.append({'url': url, 'type': kind})
        print('CAPTURED', url, flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('url')
    ap.add_argument('--out', required=True)
    ap.add_argument('--monitor-seconds', type=int, default=40)
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    info = json.loads(urllib.request.urlopen('http://127.0.0.1:9222/json/version', timeout=10).read().decode('utf-8'))
    ws = info['webSocketDebuggerUrl']

    captured = []
    seen = set()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws)
        context = browser.contexts[0] if browser.contexts else browser.new_context()
        page = None
        for pg in context.pages:
            try:
                if 'mp.weixin.qq.com' in pg.url or pg.url == 'about:blank':
                    page = pg
                    break
            except Exception:
                pass
        page = page or (context.pages[0] if context.pages else context.new_page())

        page.on('request', lambda req: consider(req.url, f'request:{req.resource_type}', seen, captured))
        page.on('response', lambda res: consider(res.url, f'response:{res.request.resource_type}', seen, captured))

        if 'mp.weixin.qq.com' not in page.url:
            page.goto(args.url, wait_until='domcontentloaded', timeout=120000)

        print(f'Monitoring page for {args.monitor_seconds}s. Click play in Chrome if needed.', flush=True)
        for _ in range(max(1, args.monitor_seconds // 5)):
            time.sleep(5)
            try:
                content = page.content()
                (out / 'manual_page.html').write_text(content, encoding='utf-8')
                for m in re.finditer(r'https?://[^\"\'\s<>]+', content):
                    consider(m.group(0), 'html', seen, captured)
                try:
                    txt = page.locator('body').inner_text(timeout=3000)
                    (out / 'manual_page_text.txt').write_text(txt, encoding='utf-8')
                except Exception:
                    pass
            except Exception:
                pass

    (out / 'manual_captured_urls.json').write_text(json.dumps(captured, ensure_ascii=False, indent=2), encoding='utf-8')
    print('TOTAL', len(captured), flush=True)


if __name__ == '__main__':
    main()
