import argparse
import sys
from typing import Optional
from urllib.parse import urlparse
TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".sh", ".xml", ".csv"}
def looks_like_file(url: str) -> bool:
    path = urlparse(url).path.lower()
    return any(path.endswith(ext) for ext in TEXT_EXTS)
def fetch_via_http(url: str) -> str:
    try:
        import httpx
    except Exception as e:
        raise RuntimeError("Missing dependency. install with: pip install httpx") from e
    r = httpx.get(
        url,
        follow_redirects=True,
        timeout=30,
        headers={
            # 尽量告诉服务器我们要文本
            "Accept": "text/plain,text/markdown,text/html,*/*",
            "User-Agent": "Mozilla/5.0",
        },
    )
    r.raise_for_status()
    # 自动按响应头编码解码；若为空，httpx 会做合理推断
    return r.text
def run(url: str, selector: Optional[str] = None) -> str:
    try:
        from scrapling import StealthyFetcher
    except Exception as e:
        raise RuntimeError(
            "Missing dependency. please install scrapling with `pip install \"scrapling[all]\"` and 'scrapling install' "
        ) from e
    try:
        if looks_like_file(url) and not selector:
            return fetch_via_http(url)
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True)
        
        # 检查状态码属性
        if hasattr(page, 'status_code'):
            status = page.status_code
        elif hasattr(page, 'status'):
            status = page.status
        else:
            status = 'unknown'
        
        print(f"Status: {status}", file=sys.stderr)
        print(f"URL: {page.url}", file=sys.stderr)
        
        if selector:
            # Selector can be any CSS pseudo syntax supported by Scrapling
            result = page.css(selector).getall()
            return "\n".join([str(x) for x in result])
        text = page.body
        if isinstance(text, bytes):
            text = text.decode('utf-8')
        
        return text
    except Exception as e:
        msg = str(e)
        if "Download is starting" in msg or "Page.goto" in msg:
            return fetch_via_http(url)
        raise


def main():
    parser = argparse.ArgumentParser(description="Scrape a web page using scrapling")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--selector", help="CSS selector (optional)")
    parser.add_argument("--out", help="Write output to file")
    args = parser.parse_args()

    text = run(args.url, args.selector)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        sys.stdout.write(text)


if __name__ == "__main__":
    main()