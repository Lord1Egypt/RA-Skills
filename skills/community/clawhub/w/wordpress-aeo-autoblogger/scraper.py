import asyncio
import logging
import requests
from typing import List

from models import ScrapedCompetitor

logger = logging.getLogger("openclaw.scraper")

"""
Scraping tier reference:

TIER 1: Playwright (local, stealth mode)    → quality: "high"     score: 1.0
TIER 2: Firecrawl API                       → quality: "high"     score: 0.9
TIER 3: Crawl4AI API                        → quality: "medium"   score: 0.75
TIER 4: Jina Reader API (jina.ai/r/)        → quality: "medium"   score: 0.65
TIER 5: Google Cache (via Playwright)       → quality: "low"      score: 0.4
TIER 6: Gemini grounding synthesis only     → quality: "low"      score: 0.2
"""


# ==========================================
# HELPERS
# ==========================================

def playwright_available() -> bool:
    """Checks if Playwright is installed to safely gate Tier 1 execution."""
    try:
        import playwright
        return True
    except ImportError:
        return False


def build_competitor(url: str, result: dict, tier: int, quality: str) -> ScrapedCompetitor:
    """Maps a raw extraction dict to the ScrapedCompetitor Pydantic model."""
    return ScrapedCompetitor(
        url=url,
        title=result.get("title"),
        meta_description=result.get("meta_description"),
        h1=result.get("h1"),
        h2s=result.get("h2s", []),
        schema_types_found=result.get("schema_types_found", []),
        schema_raw=result.get("schema_raw"),
        word_count=result.get("word_count", 0),
        readability_score=result.get("readability_score"),
        content_summary=result.get("body_text", "")[:2000],
        scrape_tier_used=tier,
        scrape_quality=quality,
        error=None
    )


async def scrape_firecrawl(url: str, api_key: str, timeout: int = 15) -> dict:
    """Stub for Firecrawl integration (Tier 2)."""
    # TODO: Implement full Firecrawl API POST request here
    logger.debug(f"Firecrawl stub called for {url}")
    return {}


async def scrape_crawl4ai(url: str, api_key: str, timeout: int = 15) -> dict:
    """Stub for Crawl4AI integration (Tier 3)."""
    # TODO: Implement full Crawl4AI API request here
    logger.debug(f"Crawl4AI stub called for {url}")
    return {}


async def scrape_jina(url: str, api_key: str = None, timeout: int = 15) -> dict:
    """Full implementation for Jina Reader API (Tier 4). Works without a key."""
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    resp = await asyncio.to_thread(requests.get, url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    data = resp.json().get("data", {})

    content = data.get("content", "")
    return {
        "title":      data.get("title"),
        "body_text":  content,
        "word_count": len(content.split()) if content else 0,
    }


# ==========================================
# CORE SCRAPING ENGINE
# ==========================================

async def scrape_url(url: str, config: dict) -> ScrapedCompetitor:
    """
    Attempts each scraping tier in order.  Returns on first success.
    Logs all failures.  Never raises — always returns a ScrapedCompetitor,
    even if scrape_quality == "failed".

    SCRAPE_MODE (v5.2):
      "api_only"   → Tier 1 (Playwright) is SKIPPED.  Start at Tier 2.
                     Default for all ClawHub installs.  Works with zero paid
                     scraping credentials (Jina Reader free tier is the final fallback).
      "playwright" → Full 6-tier waterfall including Tier 1.
                     Requires PROXY_* fields to be configured.
    """
    errors = []
    timeout = 15
    scrape_mode = config.get("SCRAPE_MODE", "api_only")

    # TIER 1: Playwright with stealth + residential proxy
    if scrape_mode == "playwright" and playwright_available():
        try:
            result = await scrape_playwright(url, config=config, timeout=timeout)
            if is_meaningful_content(result):
                return build_competitor(url, result, tier=1, quality="high")
        except Exception as e:
            errors.append(f"T1 Playwright: {e}")

    # TIER 2: Firecrawl
    if config.get("SCRAPER_TIER2_KEY"):
        try:
            result = await scrape_firecrawl(url, api_key=config["SCRAPER_TIER2_KEY"], timeout=timeout)
            if is_meaningful_content(result):
                return build_competitor(url, result, tier=2, quality="high")
        except Exception as e:
            errors.append(f"T2 Firecrawl: {e}")

    # TIER 3: Crawl4AI
    if config.get("SCRAPER_TIER3_KEY"):
        try:
            result = await scrape_crawl4ai(url, api_key=config["SCRAPER_TIER3_KEY"], timeout=timeout)
            if is_meaningful_content(result):
                return build_competitor(url, result, tier=3, quality="medium")
        except Exception as e:
            errors.append(f"T3 Crawl4AI: {e}")

    # TIER 4: Jina Reader (free, no key required for basic use)
    try:
        jina_url = f"https://r.jina.ai/{url}"
        result = await scrape_jina(jina_url, api_key=config.get("JINA_API_KEY"), timeout=timeout)
        if is_meaningful_content(result):
            return build_competitor(url, result, tier=4, quality="medium")
    except Exception as e:
        errors.append(f"T4 Jina: {e}")

    # TIER 5: Google Cache via Playwright
    if scrape_mode == "playwright" and playwright_available():
        try:
            cache_url = f"https://webcache.googleusercontent.com/search?q=cache:{url}"
            result = await scrape_playwright(cache_url, config=config, timeout=timeout, stealth=False)
            if is_meaningful_content(result):
                return build_competitor(url, result, tier=5, quality="low")
        except Exception as e:
            errors.append(f"T5 GCache: {e}")

    # TIER 6: Return a failed record — downstream uses Gemini grounding data only
    logger.warning(f"All scrape tiers failed for {url}. Errors: {errors}")
    return ScrapedCompetitor(
        url=url,
        scrape_tier_used=6,
        scrape_quality="failed",
        error=" | ".join(errors)
    )


def build_proxy_config(config: dict) -> dict:
    """
    Builds the Playwright proxy configuration object from config.
    Supports BrightData, Smartproxy, Oxylabs, and any custom HTTP/HTTPS proxy.
    """
    import random
    import string

    provider = config.get("PROXY_PROVIDER", "custom")
    gate     = config["PROXY_GATE"]
    user     = config["PROXY_USER"]
    password = config["PROXY_PASS"]
    country  = config.get("PROXY_COUNTRY", "US").lower()

    session_id = "".join(random.choices(string.ascii_lowercase + string.digits, k=10))

    if provider in {"brightdata", "smartproxy"}:
        formatted_user = f"{user}-country-{country}-session-{session_id}"
    elif provider == "oxylabs":
        formatted_user = f"{user}-country-{country}"
    else:
        formatted_user = user

    return {
        "server":   f"http://{gate}",
        "username": formatted_user,
        "password": password,
    }


async def scrape_playwright(
    url: str,
    config: dict,
    timeout: int = 15,
    stealth: bool = True,
    retry_on_ban: bool = True
) -> dict:
    from playwright.async_api import async_playwright
    from playwright_stealth import stealth_async

    max_attempts = 3 if retry_on_ban else 1

    for attempt in range(max_attempts):
        proxy_cfg = build_proxy_config(config)

        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                proxy=proxy_cfg,
                # FIX (security): Removed --no-sandbox and --disable-setuid-sandbox.
                # Navigating to unknown third-party competitor URLs with the sandbox
                # disabled exposes the host OS to container-escape exploits via
                # malicious JavaScript payloads. The Chromium sandbox must remain
                # enabled whenever browsing untrusted external content.
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--disable-dev-shm-usage",
                ]
            )
            context = await browser.new_context(
                proxy=proxy_cfg,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                ),
                viewport={"width": 1440, "height": 900},
                locale="en-US",
                timezone_id="America/New_York",
                extra_http_headers={
                    "Accept-Language":  "en-US,en;q=0.9",
                    "Accept-Encoding":  "gzip, deflate, br",
                    "DNT":              "1",
                }
            )

            await context.route(
                "**/*",
                lambda route: (
                    route.abort()
                    if route.request.resource_type in {"image", "media", "font", "websocket"}
                    else route.continue_()
                )
            )

            page = await context.new_page()
            if stealth:
                await stealth_async(page)

            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=timeout * 1000)
                await page.wait_for_timeout(1500)

                if await is_bot_wall(page):
                    logger.warning(
                        f"Bot wall detected on attempt {attempt + 1} for {url}. "
                        "Rotating proxy and retrying..."
                    )
                    await browser.close()
                    if attempt < max_attempts - 1:
                        continue
                    raise Exception(
                        f"Bot wall persisted after {max_attempts} proxy rotations"
                    )

                return await extract_page_data(page)

            finally:
                await browser.close()

    raise Exception("Playwright failed after all retry attempts")


async def is_bot_wall(page) -> bool:
    """Detects Cloudflare challenges, CAPTCHAs, Datadome, and access-denied walls."""
    title   = (await page.title()).lower()
    content = await page.content()
    signals = [
        "just a moment"              in title,
        "access denied"              in title,
        "403 forbidden"              in title,
        "please verify you are a human" in content,
        "cf-browser-verification"   in content,
        "dd_referrer"                in content,
        "recaptcha"                  in content.lower(),
        "__cf_bm"                    in content,
        len(content) < 500,
    ]
    return any(signals)


async def extract_page_data(page) -> dict:
    """Extracts all SEO-relevant signals from a rendered page."""
    return await page.evaluate("""() => {
        const getText = (sel) => document.querySelector(sel)?.textContent?.trim() || null;
        const getMeta = (name) =>
            document.querySelector(`meta[name="${name}"]`)?.content
            || document.querySelector(`meta[property="${name}"]`)?.content
            || null;
        const getH2s = () => [...document.querySelectorAll('h2')].map(h => h.textContent.trim());
        const getH3s = () => [...document.querySelectorAll('h3')].map(h => h.textContent.trim());
        const getSchemas = () =>
            [...document.querySelectorAll('script[type="application/ld+json"]')]
            .map(s => s.textContent);
        const contentBlocks = [
            ...document.querySelectorAll('article, main, [role="main"], .content, #content')
        ]
            .map(el => el.innerText)
            .filter(t => t.length > 200);
        const bodyText = contentBlocks.length > 0
            ? contentBlocks[0]
            : document.body.innerText;
        return {
            title:            getText('title'),
            meta_description: getMeta('description') || getMeta('og:description'),
            h1:               getText('h1'),
            h2s:              getH2s(),
            h3s:              getH3s(),
            schema_blocks:    getSchemas(),
            word_count:       bodyText.split(/\s+/).filter(w => w.length > 0).length,
            body_text:        bodyText.substring(0, 15000),
        };
    }""")


def is_meaningful_content(result: dict) -> bool:
    """
    Returns False if the scraped content is not usable for competitive analysis.
    Prevents low-signal pages from corrupting the Task Reference File.
    """
    if not result:
        return False
    word_count = result.get("word_count", 0)
    body_text  = result.get("body_text", "")
    checks = [
        word_count >= 200,
        len(body_text) >= 500,
        result.get("title") is not None,
        "enable javascript"   not in body_text.lower(),
        "please enable cookies" not in body_text.lower(),
    ]
    return all(checks)


def calculate_trf_quality(competitors: List[ScrapedCompetitor]) -> tuple[str, float]:
    """
    Computes an aggregate quality label and 0.0-1.0 score for the Task Reference File.
    This score is logged and used by downstream steps to calibrate confidence.
    """
    if not competitors:
        return "low", 0.0

    tier_scores = {1: 1.0, 2: 0.9, 3: 0.75, 4: 0.65, 5: 0.4, 6: 0.0}
    scores = [tier_scores.get(c.scrape_tier_used, 0.0) for c in competitors]
    avg    = sum(scores) / len(scores)

    if avg >= 0.75:
        return "high", avg
    elif avg >= 0.45:
        return "medium", avg
    else:
        return "low", avg
