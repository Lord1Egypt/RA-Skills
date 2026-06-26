"""Detail page fetching via bb-browser site adapters.

Routes URLs to the correct platform adapter, runs bb-browser subprocess,
and normalizes results into ItemDetail objects.
"""

from __future__ import annotations

import json
import logging
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from .bb_browser_cli import parse_site_json_output
from .models import ItemDetail, SellerInfo

logger = logging.getLogger(__name__)

ADAPTER_DIR = Path(__file__).resolve().parent.parent.parent / "adapters"

_PLATFORM_RULES: list[tuple[str, str, str]] = [
    # (domain pattern, adapter name, platform label)
    (r"\.ok\.com$", "ok/detail", "ok.com"),
    (r"\.ebay\.", "ebay/detail", "ebay"),
    (r"\.gumtree\.com$", "gumtree/detail", "gumtree"),
    (r"\.amazon\.", "amazon/detail", "amazon"),
]


def resolve_adapter(url: str) -> tuple[str, str] | None:
    """Determine which bb-browser adapter to use for a given URL.

    Returns (adapter_name, platform_label) or None if unsupported.
    """
    try:
        host = urlparse(url).hostname or ""
    except Exception:
        return None

    for pattern, adapter, label in _PLATFORM_RULES:
        if re.search(pattern, host):
            return adapter, label
    return None


def _install_detail_adapter(adapter_name: str) -> None:
    """Ensure the detail adapter JS is installed to ~/.bb-browser/sites/."""
    parts = adapter_name.split("/")
    dir_name = parts[0]
    file_name = parts[1] + ".js" if len(parts) > 1 else "detail.js"

    src_file = ADAPTER_DIR / dir_name / file_name
    if not src_file.exists():
        return

    target_dir = Path.home() / ".bb-browser" / "sites" / dir_name
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / file_name

    if not target.exists() or src_file.read_text() != target.read_text():
        shutil.copy2(src_file, target)
        logger.info("Installed detail adapter: %s -> %s", src_file.name, target)


def _ensure_daemon() -> bool:
    """Ensure bb-browser daemon is running. Returns True if ready."""
    import time
    try:
        result = subprocess.run(
            ["bb-browser", "daemon", "status"],
            capture_output=True, text=True, timeout=10,
        )
        if "CDP connected: yes" in result.stdout:
            return True
    except Exception:
        pass

    subprocess.run(["pkill", "-f", "bb-browser"], capture_output=True)
    time.sleep(1)
    try:
        subprocess.Popen(
            ["bb-browser", "daemon", "start"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        time.sleep(3)
        return True
    except Exception:
        return False


def _run_adapter(adapter_name: str, url: str) -> dict:
    """Run a bb-browser site adapter and return parsed JSON."""
    cmd = ["bb-browser", "site", adapter_name, url, "--json"]
    logger.info("Running: %s", " ".join(cmd))

    def _exec() -> dict:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        except FileNotFoundError:
            return {"error": "bb-browser not found. Install with: npm install -g bb-browser"}
        except subprocess.TimeoutExpired:
            return {"error": "Query timed out (60s)"}

        return parse_site_json_output(result)

    raw = _exec()
    if raw.get("error") == "daemon_disconnected":
        logger.warning("Daemon disconnected, attempting restart...")
        if _ensure_daemon():
            raw = _exec()
        else:
            raw = {"error": f"Daemon reconnect failed: {raw.get('detail', '')}"}

    return raw


_CURRENCY_SYMBOLS = {"$": "USD", "£": "GBP", "€": "EUR"}


def _parse_price(price_str: str) -> tuple[float, str]:
    """Extract numeric price and currency from display string."""
    stripped = price_str.lstrip()
    if stripped.startswith("A$") or stripped.startswith("AU$"):
        currency = "AUD"
    elif stripped.startswith("C$") or stripped.startswith("CA$"):
        currency = "CAD"
    else:
        currency = "USD"
        for sym, code in _CURRENCY_SYMBOLS.items():
            if sym in stripped:
                currency = code
                break

    cleaned = re.sub(r"[^\d.]", "", price_str)
    try:
        return float(cleaned), currency
    except (ValueError, TypeError):
        return 0.0, currency


def _raw_to_item_detail(raw: dict, url: str) -> ItemDetail:
    """Convert adapter JSON response to ItemDetail."""
    # Unwrap bb-browser envelope if present
    data = raw.get("data", raw)

    seller_raw = data.get("seller", {})
    seller = SellerInfo(
        name=seller_raw.get("name", ""),
        rating=seller_raw.get("rating", ""),
        reviews_count=seller_raw.get("reviews_count", 0),
        member_since=seller_raw.get("member_since", ""),
        location=seller_raw.get("location", ""),
    )

    price_str = data.get("price", "")
    price_num, currency = _parse_price(price_str)

    return ItemDetail(
        title=data.get("title", ""),
        price=price_str,
        price_numeric=price_num,
        currency=currency,
        description=data.get("description", ""),
        condition=data.get("condition", ""),
        images=data.get("images", []),
        seller=seller,
        posted_date=data.get("posted_date", ""),
        views=data.get("views", 0),
        platform=data.get("platform", ""),
        source_url=url,
        platform_extras=data.get("platform_extras", {}),
    )


def fetch_detail(url: str) -> ItemDetail:
    """Fetch detail page for a single item URL.

    Raises ValueError if the URL's platform is unsupported or fetching fails.
    """
    resolved = resolve_adapter(url)
    if not resolved:
        raise ValueError(f"Unsupported platform URL: {url}")

    adapter_name, platform_label = resolved
    _install_detail_adapter(adapter_name)

    raw = _run_adapter(adapter_name, url)
    if "error" in raw and raw["error"] != "daemon_disconnected":
        raise ValueError(f"Fetch failed for {url}: {raw['error']}")

    return _raw_to_item_detail(raw, url)


def fetch_details(urls: list[str]) -> list[ItemDetail | dict]:
    """Fetch detail pages for multiple URLs in sequence.

    Returns a list where each element is either an ItemDetail (success)
    or a dict with 'url' and 'error' keys (failure).
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed

    results: list[tuple[int, ItemDetail | dict]] = []

    def _fetch_one(idx: int, url: str) -> tuple[int, ItemDetail | dict]:
        try:
            return idx, fetch_detail(url)
        except Exception as e:
            return idx, {"url": url, "error": str(e)}

    with ThreadPoolExecutor(max_workers=min(len(urls), 4)) as executor:
        futures = {
            executor.submit(_fetch_one, i, u): i
            for i, u in enumerate(urls)
        }
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda x: x[0])
    return [r for _, r in results]
