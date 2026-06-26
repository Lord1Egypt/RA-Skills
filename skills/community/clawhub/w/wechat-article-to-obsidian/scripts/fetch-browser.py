#!/opt/homebrew/opt/python@3.13/bin/python3.13
"""
Browser fallback fetcher for WeChat articles.
Usage: python3 fetch-browser.py <url> <output_html>
"""
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 fetch-browser.py <url> <output_html>", file=sys.stderr)
        sys.exit(1)

    url = sys.argv[1]
    output = Path(sys.argv[2])

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="chrome", headless=True)
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            locale="zh-CN",
        )
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45000)
            try:
                page.wait_for_load_state("networkidle", timeout=15000)
            except Exception:
                pass
            page.wait_for_timeout(2500)

            data = page.evaluate(
                """
                () => {
                  const qs = (sel) => document.querySelector(sel);
                  const getText = (sel) => qs(sel)?.textContent?.trim() || '';
                  const getHtml = (sel) => qs(sel)?.innerHTML || '';
                  const meta = Array.from(document.querySelectorAll('meta')).reduce((acc, el) => {
                    const k = el.getAttribute('property') || el.getAttribute('name');
                    const v = el.getAttribute('content');
                    if (k && v) acc[k] = v;
                    return acc;
                  }, {});
                  return {
                    title: window.msg_title || meta['og:title'] || getText('#activity-name') || getText('.rich_media_title') || document.title || '',
                    author: window.nickname || getText('#js_name') || meta['author'] || '',
                    publishDate: getText('#publish_time') || '',
                    contentHtml: getHtml('#js_content') || getHtml('.rich_media_content') || ''
                  };
                }
                """
            )
        finally:
            browser.close()

    def esc(s: str) -> str:
        return str(s or "").replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")

    html = f"""<!doctype html>
<html>
<head>
<meta charset=\"utf-8\">
<title>{data.get('title','')}</title>
<script>
function htmlDecode(s){{return s;}}
var msg_title = '{esc(data.get('title',''))}';
var nickname = htmlDecode('{esc(data.get('author',''))}');
var msg_link = '{esc(url)}';
</script>
</head>
<body>
<h1 class=\"rich_media_title\">{data.get('title','')}</h1>
<div id=\"js_name\">{data.get('author','')}</div>
<div id=\"publish_time\">{data.get('publishDate','')}</div>
<div id=\"js_content\">{data.get('contentHtml','')}</div>
</body>
</html>"""

    output.write_text(html, encoding="utf-8")
    print(json.dumps({
        "ok": True,
        "title": data.get("title", ""),
        "author": data.get("author", ""),
        "publishDate": data.get("publishDate", ""),
        "contentLength": len(data.get("contentHtml", "") or ""),
        "output": str(output),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
