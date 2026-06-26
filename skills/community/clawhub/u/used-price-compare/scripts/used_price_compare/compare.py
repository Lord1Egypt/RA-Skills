"""Multi-platform price comparison engine.

Runs bb-browser site adapters in parallel across multiple platforms,
normalizes results, and produces a unified structured data report.
Analysis and purchase recommendations are handled by the calling Agent.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .bb_browser_cli import parse_site_json_output
from .platforms import Platform, get_city_slug, normalize_city, resolve_platforms

logger = logging.getLogger(__name__)

ADAPTER_DIR = Path(__file__).resolve().parent.parent.parent / "adapters"


@dataclass
class CompareItem:
    title: str
    price: float
    price_display: str
    currency: str
    url: str
    source: str
    source_display: str
    condition: str = ""
    location: str = ""
    image: str = ""
    seller: str = ""
    rating: str = ""
    prime: bool = False

    @property
    def is_ok(self) -> bool:
        return self.source == "ok"



@dataclass
class CompareResult:
    keyword: str
    city: str
    platforms_queried: list[str] = field(default_factory=list)
    platforms_success: list[str] = field(default_factory=list)
    platforms_failed: dict[str, str] = field(default_factory=dict)
    platform_display_names: dict[str, str] = field(default_factory=dict)
    items: list[CompareItem] = field(default_factory=list)
    lowest_price: CompareItem | None = None
    ok_best: CompareItem | None = None


_CURRENCY_SYMBOLS = {"$": "USD", "£": "GBP", "€": "EUR"}


def _detect_currency(price_str: str) -> str:
    """Detect currency code from a price display string."""
    stripped = price_str.lstrip()
    if stripped.startswith("A$") or stripped.startswith("AU$"):
        return "AUD"
    if stripped.startswith("C$") or stripped.startswith("CA$"):
        return "CAD"
    for sym, code in _CURRENCY_SYMBOLS.items():
        if sym in stripped:
            return code
    return "USD"


def _parse_price(price_str: str) -> float:
    """Extract numeric price from display string like '$1,234.56' or '£999'."""
    cleaned = re.sub(r"[^\d.]", "", price_str)
    try:
        return float(cleaned)
    except (ValueError, TypeError):
        return float("inf")


def _install_adapter(platform: Platform) -> None:
    """Copy adapter JS to ~/.bb-browser/sites/ so bb-browser can find it.

    The adapter filesystem layout uses the adapter prefix as directory name:
      adapter="ebay/search-uk" → src=adapters/ebay/search-uk.js
                                → dst=~/.bb-browser/sites/ebay/search-uk.js
    """
    # adapter = "ebay/search-uk" → dir_name = "ebay", file_stem = "search-uk"
    parts = platform.adapter.split("/")
    dir_name = parts[0]
    file_name = parts[1] + ".js" if len(parts) > 1 else "search.js"

    src_file = ADAPTER_DIR / dir_name / file_name
    if not src_file.exists():
        return

    target_dir = Path.home() / ".bb-browser" / "sites" / dir_name
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / file_name

    if not target.exists() or src_file.read_text() != target.read_text():
        shutil.copy2(src_file, target)
        logger.info("Installed adapter: %s → %s", src_file.name, target)


def _ensure_daemon() -> bool:
    """Ensure bb-browser daemon is running and connected. Returns True if ready."""
    import socket, time
    try:
        result = subprocess.run(
            ["bb-browser", "daemon", "status"],
            capture_output=True, text=True, timeout=10
        )
        if "CDP connected: yes" in result.stdout:
            return True
    except Exception:
        pass
    # Try to restart
    subprocess.run(["pkill", "-f", "bb-browser"], capture_output=True)
    time.sleep(1)
    try:
        subprocess.Popen(
            ["bb-browser", "daemon", "start"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
        )
        time.sleep(3)
        return True
    except Exception:
        return False


def _query_platform(
    platform: Platform,
    keyword: str,
    city: str = "los-angeles",
    country: str | None = None,
) -> dict[str, Any]:
    """Run bb-browser site adapter for a single platform. Auto-retries on daemon failure."""
    from .platforms import get_country_for_city
    resolved_country = country or get_country_for_city(city)
    city_slug = get_city_slug(city, platform.name)

    overrides: dict[str, str] = {}
    if platform.name == "ok":
        overrides["country"] = resolved_country
        overrides["city"] = city_slug
    elif platform.name == "gumtree":
        if city_slug:
            overrides["location"] = city_slug
        else:
            overrides["location"] = city.replace("-", " ").title()
    # eBay and Amazon are nationwide — no city override needed

    cmd = platform.build_cmd(keyword, **overrides)
    logger.info("Running: %s", " ".join(cmd))

    def _run_query() -> dict[str, Any]:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
            )
        except FileNotFoundError:
            return {"error": "bb-browser not found. Install with: npm install -g bb-browser"}
        except subprocess.TimeoutExpired:
            return {"error": "Query timed out (60s)"}

        return parse_site_json_output(result)

    # First attempt
    raw = _run_query()
    if raw.get("error") == "daemon_disconnected":
        logger.warning("Daemon disconnected, attempting restart...")
        if _ensure_daemon():
            raw = _run_query()
        else:
            raw = {"error": f"Daemon reconnect failed: {raw.get('detail', raw.get('error'))}"}

    return raw


_COUNTRY_CURRENCY_SYMBOL = {"us": "$", "uk": "£", "au": "A$", "ca": "C$", "ae": "AED "}


def _normalize_items(platform: Platform, raw: dict) -> list[CompareItem]:
    """Convert platform-specific response to unified CompareItem list."""
    listings = raw.get("listings", [])
    fallback_symbol = _COUNTRY_CURRENCY_SYMBOL.get(platform.country, "$")
    items = []
    for entry in listings:
        title = entry.get("title", "")
        price_str = entry.get("price", "")

        # Strip duplicate currency symbols from adapter output (e.g. "$$300" → "$300")
        price_str = re.sub(r"^(\$)\1+", r"\1", price_str)
        price_str = re.sub(r"^(£)\1+", r"\1", price_str)

        price = _parse_price(price_str)
        if price == float("inf"):
            continue

        currency = _detect_currency(price_str)
        has_symbol = price_str and price_str.lstrip()[:1] in ("$", "£", "€", "A", "C")
        display = price_str if has_symbol else f"{fallback_symbol}{price:.2f}"

        prime_raw = entry.get("prime", "")
        is_prime = prime_raw in (True, "Prime") if prime_raw else False

        items.append(CompareItem(
            title=title,
            price=price,
            price_display=display,
            currency=currency,
            url=entry.get("url", ""),
            source=platform.name,
            source_display=platform.display_name,
            condition=entry.get("condition", ""),
            location=entry.get("location", ""),
            image=entry.get("image", ""),
            seller=entry.get("seller", ""),
            rating=entry.get("rating", ""),
            prime=is_prime,
        ))
    return items


def compare_prices(
    keyword: str,
    city: str = "los-angeles",
    country: str | None = None,
    platforms: list[str] | None = None,
    top_n: int = 5,
) -> CompareResult:
    """Compare prices across multiple platforms for a given keyword.

    Platform routing:
    - For family-based platforms (eBay), the correct country variant
      is auto-selected based on city→country mapping.
    - User can specify "ebay" (auto-route) or "ebay-uk" (explicit).

    Args:
        keyword: Product to search for.
        city: City (normalized form like 'los-angeles').
        country: Country code (default: inferred from city).
        platforms: Platform names to query (default: all enabled).
        top_n: Number of cheapest items to return per platform.

    Returns:
        CompareResult with sorted items (no analysis or recommendation).
    """
    city = normalize_city(city)

    target_platforms = resolve_platforms(
        city=city,
        country=country,
        platform_filter=platforms,
    )

    # Install adapters before querying
    for plat in target_platforms:
        _install_adapter(plat)

    result = CompareResult(
        keyword=keyword,
        city=city,
        platforms_queried=[p.name for p in target_platforms],
        platform_display_names={p.name: p.display_name for p in target_platforms},
    )

    # Query all platforms in parallel
    with ThreadPoolExecutor(max_workers=max(len(target_platforms), 1)) as executor:
        futures = {
            executor.submit(_query_platform, plat, keyword, city, country): plat
            for plat in target_platforms
        }

        for future in as_completed(futures):
            plat = futures[future]
            try:
                raw = future.result()
            except Exception as e:
                result.platforms_failed[plat.name] = str(e)
                continue

            if "error" in raw:
                result.platforms_failed[plat.name] = raw["error"]
                hint = raw.get("hint", "")
                if hint:
                    result.platforms_failed[plat.name] += f". {hint}"
                continue

            # Unwrap bb-browser envelope: {"success":true,"data":{...}} -> {...}
            inner = raw.get("data", raw)
            items = _normalize_items(plat, inner)
            if items:
                result.platforms_success.append(plat.name)
                items.sort(key=lambda x: x.price)
                result.items.extend(items[:top_n])
            else:
                # Use adapter's summary message if it explains why there are no results
                summary = inner.get("summary", "")
                if isinstance(summary, str) and summary:
                    result.platforms_failed[plat.name] = summary
                else:
                    result.platforms_failed[plat.name] = "No listings with valid prices"

    # Sort all items by price
    result.items.sort(key=lambda x: x.price)

    if result.items:
        result.lowest_price = result.items[0]
        ok_items = [i for i in result.items if i.source == "ok"]
        if ok_items:
            result.ok_best = ok_items[0]

    return result


_COUNTRY_TO_OK_DOMAIN = {"uk": "uk", "au": "au", "ca": "ca", "ae": "ae"}


def _ok_domain_for_city(city: str) -> str:
    """Return the OK.com subdomain (e.g. 'uk', 'us') for a given city."""
    from .platforms import get_country_for_city

    country = get_country_for_city(normalize_city(city))
    return _COUNTRY_TO_OK_DOMAIN.get(country, "us")


def _ok_search_url(result: CompareResult) -> str:
    """Build an OK.com search URL for the result's city and keyword."""
    ok_domain = _ok_domain_for_city(result.city)
    ok_city_slug = get_city_slug(result.city, "ok")
    kw = quote(result.keyword, safe="")
    return f"https://{ok_domain}.ok.com/en/city-{ok_city_slug}/cate-marketplace/?keyword={kw}"



def format_comparison_table(result: CompareResult) -> dict:
    """Format CompareResult into structured data output.

    Returns raw price ranking and platform breakdown.
    Analysis and recommendations are handled by the evaluate sub-skill.
    """
    items_by_platform: dict[str, list[dict]] = {}
    for item in result.items:
        platform_items = items_by_platform.setdefault(item.source_display, [])
        platform_items.append({
            "title": item.title,
            "price": item.price_display,
            "url": item.url,
            "condition": item.condition,
            "location": item.location,
            "seller": item.seller,
        })

    price_ranking = []
    for i, item in enumerate(result.items, 1):
        price_ranking.append({
            "rank": i,
            "title": item.title,
            "price": item.price_display,
            "currency": item.currency,
            "source": item.source_display,
            "url": item.url,
        })

    # Force per-platform output in queried order, even for failed/empty platforms.
    forced_by_platform: dict[str, list[dict]] = {}
    platform_sections: list[dict] = []
    for platform_name in result.platforms_queried:
        display_name = result.platform_display_names.get(platform_name, platform_name)
        rows = items_by_platform.get(display_name, [])
        forced_by_platform[display_name] = rows

        if platform_name in result.platforms_failed:
            status = "failed"
            error = result.platforms_failed[platform_name]
        elif platform_name in result.platforms_success:
            status = "success"
            error = ""
        else:
            status = "unknown"
            error = ""

        platform_sections.append({
            "name": platform_name,
            "display_name": display_name,
            "status": status,
            "error": error,
            "items": rows,
        })

    output = {
        "success": True,
        "keyword": result.keyword,
        "city": result.city,
        "platforms": {
            "queried": result.platforms_queried,
            "success": result.platforms_success,
            "failed": result.platforms_failed,
        },
        "price_ranking": price_ranking,
        "by_platform": forced_by_platform,
        "platform_sections": platform_sections,
        "lowest_price": {
            "title": result.lowest_price.title,
            "price": result.lowest_price.price_display,
            "source": result.lowest_price.source_display,
            "url": result.lowest_price.url,
        } if result.lowest_price else None,
        "ok_best": {
            "title": result.ok_best.title,
            "price": result.ok_best.price_display,
            "url": result.ok_best.url,
        } if result.ok_best else None,
        "ok_search_url": _ok_search_url(result),
    }

    return output
