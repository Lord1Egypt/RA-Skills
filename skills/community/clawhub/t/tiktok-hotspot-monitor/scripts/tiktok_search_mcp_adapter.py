import asyncio
import json
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("tiktok_search_adapter")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SESSION_FILE = PROJECT_ROOT / "data" / "tiktok_session.json"


def send(message):
    print(json.dumps(message), flush=True)


async def search_on_tiktok(search_term: str, count: int) -> list[dict]:
    """Search TikTok via Playwright with saved session; returns up to ~12 items per keyword."""
    from playwright.async_api import async_playwright

    if not SESSION_FILE.exists():
        raise RuntimeError(
            f"Session file not found at {SESSION_FILE}. "
            "Run 'python scripts/tiktok_login_save_session.py' first to log in."
        )

    session_state = json.loads(SESSION_FILE.read_text(encoding="utf-8"))

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            locale="en-US",
            storage_state=session_state,
        )
        page = await context.new_page()

        search_results: list[dict] = []
        seen_ids: set[str] = set()

        async def on_response(response):
            nonlocal search_results, seen_ids
            url = response.url
            if "/api/search/item/full/" not in url and "/api/search/item/" not in url:
                return
            try:
                body = await response.json()
            except Exception:
                return
            items = body.get("itemList", []) or body.get("item_list", []) or []
            if not items:
                return
            new_count = 0
            for item in items:
                vid = str(item.get("id") or "")
                if vid and vid not in seen_ids:
                    seen_ids.add(vid)
                    search_results.append(item)
                    new_count += 1
                elif not vid:
                    search_results.append(item)
                    new_count += 1
            if new_count:
                logger.info(f"got {new_count} items (total {len(search_results)})")

        page.on("response", on_response)

        search_term_clean = search_term.replace("'", "").replace("&", "and")
        search_url = f"https://www.tiktok.com/search/video?q={search_term_clean.replace(' ', '%20')}"
        logger.info(f"searching: {search_term_clean}")
        await page.goto(search_url, timeout=60000, wait_until="domcontentloaded")
        await asyncio.sleep(3)

        # Wait for results (TikTok web caps at ~12 items per keyword)
        for _ in range(20):
            if search_results:
                break
            await asyncio.sleep(1)

        # Fallback: click Videos tab if nothing loaded yet
        if not search_results:
            try:
                await page.click('div[data-e2e="search-tab"]:has-text("Videos")', timeout=5000)
                await asyncio.sleep(3)
                for _ in range(15):
                    if search_results:
                        break
                    await asyncio.sleep(1)
            except Exception:
                pass

        logger.info(f"returned {len(search_results)} items (TikTok web max ~12)")
        await browser.close()

    return search_results[:count]


def extract_video_data(raw: dict, search_query: str) -> dict:
    author = raw.get("author", {}) or {}
    stats = raw.get("stats", {}) or {}
    video_id = raw.get("id", "")
    create_time = raw.get("createTime")
    raw_music = raw.get("music") or {}
    return {
        "id": video_id,
        "url": f"https://www.tiktok.com/@{author.get('uniqueId', '')}/video/{video_id}" if video_id else None,
        "description": raw.get("desc", "") or "",
        "author": author.get("nickname", "") or author.get("uniqueId", ""),
        "author_id": author.get("uniqueId", ""),
        "timestamp": create_time,
        "upload_date": None,
        "create_time": create_time,
        "stats": {
            "views": str(stats.get("playCount", 0)),
            "likes": str(stats.get("diggCount", 0)),
            "shares": str(stats.get("shareCount", 0)),
            "comments": str(stats.get("commentCount", 0)),
        },
        "hashtags": _extract_hashtags(raw),
        "music": {
            "id": raw_music.get("id"),
            "title": raw_music.get("title"),
            "authorName": raw_music.get("authorName"),
            "original": raw_music.get("original"),
            "playUrl": raw_music.get("playUrl"),
            "coverMediumUrl": raw_music.get("coverMediumUrl"),
        },
        "search_query": search_query,
    }


def _extract_hashtags(raw: dict) -> list[str] | None:
    challenges = raw.get("challenges")
    if not isinstance(challenges, list):
        return None
    names = [c.get("title", "") for c in challenges if isinstance(c, dict) and c.get("title")]
    return names if names else None


async def search_videos(search_terms: list[str], count: int) -> dict:
    results = {}
    errors = {}
    for term in search_terms:
        clean_term = term.lstrip("#")
        try:
            items = await search_on_tiktok(clean_term, count)
            results[term] = [extract_video_data(item, clean_term) for item in items]
            if not items:
                errors[term] = {"error": "No videos found"}
        except Exception as exc:
            results[term] = []
            errors[term] = {"error": str(exc), "type": type(exc).__name__}
    return {
        "results": results,
        "errors": errors,
        "transformations": {},
        "video_count": sum(len(v) for v in results.values()),
    }


# MCP stdio protocol
for line in sys.stdin:
    if not line.strip():
        continue
    message = json.loads(line)
    method = message.get("method")
    mid = message.get("id")
    if method == "initialize":
        send({"jsonrpc": "2.0", "id": mid, "result": {"protocolVersion": "2024-11-05", "capabilities": {"tools": {}}, "serverInfo": {"name": "tiktok-search-adapter", "version": "0.1.0"}}})
    elif method == "notifications/initialized":
        continue
    elif method == "tools/list":
        send({
            "jsonrpc": "2.0",
            "id": mid,
            "result": {
                "tools": [
                    {
                        "name": "search_videos",
                        "description": "Search TikTok videos via Playwright browser",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "search_terms": {"type": "array", "items": {"type": "string"}},
                                "count": {"type": "integer"},
                            },
                            "required": ["search_terms"],
                        },
                    }
                ]
            },
        })
    elif method == "tools/call":
        params = message.get("params", {})
        args = params.get("arguments", {})
        payload = asyncio.run(search_videos(args.get("search_terms") or [], int(args.get("count", 15))))
        send({"jsonrpc": "2.0", "id": mid, "result": {"content": [{"type": "text", "text": json.dumps(payload)}], "isError": False}})
    else:
        send({"jsonrpc": "2.0", "id": mid, "result": {}})
