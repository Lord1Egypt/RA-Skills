#!/usr/bin/env python3
"""
Steel Anti-Dumping News - Fetcher
==================================
Fetches the latest steel anti-dumping (AD) and countervailing duty (CVD) news
from Mysteel Global's Global Trade Updates feed.

Source: https://www.mysteel.net/market-insights/news/ad-and-cvd/

The listing page is server-side rendered (Vue/Nuxt), so the latest batch of
articles is available directly in the HTML. This script uses only the Python
standard library by default (no pip installs required).

For deeper history (older pages), pass --pages N to paginate using Playwright
(optional; requires `pip install playwright && playwright install chromium`).

Usage:
    python fetch_ad_cvd_news.py [options]

Options:
    --limit N            Limit output to N articles (default: 10)
    --pages N            Fetch N listing pages (default: 1). N>1 requires Playwright.
    --keyword TEXT       Only keep articles whose title/summary contains TEXT
    --format FORMAT      Output format: text, json, markdown (default: text)
    --export             Save results to a JSON file
    --out PATH           Output file path for --export
    --help               Show this help
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ============================================================================
# Configuration
# ============================================================================

LISTING_URL = "https://www.mysteel.net/market-insights/news/ad-and-cvd/"
BASE_URL = "https://www.mysteel.net"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# ============================================================================
# HTTP fetch (dependency-free)
# ============================================================================


def fetch_html(url=LISTING_URL):
    """Fetch raw HTML for a listing page using the standard library."""
    req = Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urlopen(req, timeout=45) as resp:
            return resp.read().decode("utf-8", "replace")
    except HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Network error: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ============================================================================
# HTML parsing (regex based, resilient to framework markup)
# ============================================================================


def clean(text):
    """Strip tags and collapse whitespace."""
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("&amp;", "&").replace("&nbsp;", " ").replace("&#39;", "'").replace("&quot;", '"')
    return re.sub(r"\s+", " ", text).strip()


def parse_articles(html):
    """Extract article items from listing HTML."""
    items = re.findall(
        r'<li class="d-flex align-center m-list-item"[^>]*>(.*?)</li>',
        html,
        re.DOTALL,
    )
    articles = []
    seen = set()
    for it in items:
        href_m = re.search(r'<a href="(/news/[^"]+)"', it)
        if not href_m:
            continue
        href = href_m.group(1)
        if href in seen:
            continue
        seen.add(href)

        title_m = re.search(r'<p title="([^"]*)"', it)
        title_clean_m = re.search(r'<p class="m-title[^"]*"[^>]*>(.*?)</p>', it, re.DOTALL)
        title = clean(title_m.group(1)) if title_m else (clean(title_clean_m.group(1)) if title_clean_m else "")

        desc_m = re.search(r'<p class="description[^"]*"[^>]*>(.*?)</p>', it, re.DOTALL)
        summary = clean(desc_m.group(1)) if desc_m else ""

        date_m = re.search(r'<p class="date[^"]*"[^>]*>(.*?)</p>', it, re.DOTALL)
        date_str = clean(date_m.group(1)) if date_m else ""

        articles.append(
            {
                "title": title,
                "url": BASE_URL + href,
                "summary": summary,
                "date": date_str,
            }
        )
    return articles


# ============================================================================
# Optional Playwright multi-page fetch
# ============================================================================


def fetch_pages_playwright(pages):
    """Fetch multiple listing pages by driving the on-page pagination."""
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "Playwright is required for --pages > 1.\n"
            "Install with: pip install playwright && playwright install chromium",
            file=sys.stderr,
        )
        sys.exit(1)

    collected = {}
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(LISTING_URL, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)

            for page_no in range(1, pages + 1):
                html = page.content()
                for art in parse_articles(html):
                    collected[art["url"]] = art

                if page_no == pages:
                    break

                # Click the pagination button for the next page number
                target = str(page_no + 1)
                buttons = page.query_selector_all(".m-pagination button, .v-pagination button")
                clicked = False
                for b in buttons:
                    try:
                        if b.inner_text().strip() == target:
                            b.click()
                            clicked = True
                            break
                    except Exception:
                        continue
                if not clicked:
                    break
                page.wait_for_timeout(2500)
        finally:
            browser.close()

    # Preserve page order (dict preserves insertion)
    return list(collected.values())


# ============================================================================
# Filtering & formatting
# ============================================================================


def filter_keyword(articles, keyword):
    kw = keyword.lower()
    out = []
    for a in articles:
        hay = (a["title"] + " " + a["summary"]).lower()
        if kw in hay:
            out.append(a)
    return out


def fmt_text(articles, meta):
    if not articles:
        return "No matching steel anti-dumping news found.\n"
    lines = []
    lines.append("=" * 60)
    lines.append("  Latest Steel Anti-Dumping & Countervailing Duty News")
    lines.append("=" * 60)
    lines.append(f"  Source : {LISTING_URL}")
    lines.append(f"  Fetched: {meta['fetchedAt']}")
    lines.append(f"  Count  : {len(articles)}")
    lines.append("-" * 60)
    for i, a in enumerate(articles, 1):
        lines.append(f"{i}. {a['title']}")
        lines.append(f"   🗓️  {a['date']}")
        if a["summary"]:
            s = a["summary"]
            if len(s) > 220:
                s = s[:220] + "..."
            lines.append(f"   📝 {s}")
        lines.append(f"   🔗 {a['url']}")
        lines.append("")
    return "\n".join(lines)


def fmt_markdown(articles, meta):
    if not articles:
        return "# Latest Steel Anti-Dumping News\n\n_No matching news found._\n"
    lines = ["# Latest Steel Anti-Dumping & CVD News", ""]
    lines.append(f"_Source: [Mysteel Global]({LISTING_URL}) · Fetched {meta['fetchedAt']}_")
    lines.append("")
    for a in articles:
        lines.append(f"## [{a['title']}]({a['url']})")
        lines.append(f"**{a['date']}**")
        lines.append("")
        if a["summary"]:
            lines.append(a["summary"])
            lines.append("")
    return "\n".join(lines)


def fmt_json(articles, meta):
    payload = {
        "fetchedAt": meta["fetchedAt"],
        "source": LISTING_URL,
        "count": len(articles),
        "articles": articles,
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


# ============================================================================
# Main
# ============================================================================


def parse_args():
    p = argparse.ArgumentParser(
        description="Fetch the latest steel anti-dumping (AD/CVD) news from Mysteel Global.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python fetch_ad_cvd_news.py\n"
            "  python fetch_ad_cvd_news.py --limit 5\n"
            "  python fetch_ad_cvd_news.py --keyword \"cold-rolled\"\n"
            "  python fetch_ad_cvd_news.py --format json\n"
            "  python fetch_ad_cvd_news.py --pages 3 --format markdown\n"
            "  python fetch_ad_cvd_news.py --export\n"
        ),
    )
    p.add_argument("--limit", type=int, default=10, help="Max articles to output (0 = all)")
    p.add_argument("--pages", type=int, default=1, help="Listing pages to fetch (default 1)")
    p.add_argument("--keyword", type=str, default=None, help="Filter by keyword")
    p.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    p.add_argument("--export", action="store_true", help="Save results to a JSON file")
    p.add_argument("--out", type=str, default=None, help="Output path for --export")
    return p.parse_args()


def main():
    args = parse_args()

    if args.pages > 1:
        articles = fetch_pages_playwright(args.pages)
    else:
        html = fetch_html()
        articles = parse_articles(html)

    if not articles:
        print("No articles could be parsed. The page structure may have changed.", file=sys.stderr)
        sys.exit(1)

    if args.keyword:
        articles = filter_keyword(articles, args.keyword)

    if args.limit and args.limit > 0:
        articles = articles[: args.limit]

    meta = {"fetchedAt": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")}

    if args.export:
        path = args.out or f"steel_ad_cvd_news_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(path, "w", encoding="utf-8") as f:
            f.write(fmt_json(articles, meta))
        print(f"Exported {len(articles)} articles to {path}", file=sys.stderr)
        return

    if args.format == "json":
        print(fmt_json(articles, meta))
    elif args.format == "markdown":
        print(fmt_markdown(articles, meta))
    else:
        print(fmt_text(articles, meta))


if __name__ == "__main__":
    main()
