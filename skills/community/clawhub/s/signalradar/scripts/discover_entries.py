#!/usr/bin/env python3
"""URL parsing, API lookup, and market normalization for SignalRadar v0.8.0.

Replaces the keyword-based topic discovery with URL→event slug→API resolution.
Also provides shared helpers (extract_probability, is_settled) used by other modules.
"""

from __future__ import annotations

import json
import re
import socket
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

GAMMA_API_BASE = "https://gamma-api.polymarket.com"
CLOB_API_BASE = "https://clob.polymarket.com"
HTTP_TIMEOUT = 15
# Shorter than HTTP_TIMEOUT: trend context is optional display data, and a
# CLOB outage must not stall alert delivery for more than a few seconds.
TREND_HTTP_TIMEOUT = 8
USER_AGENT = "signalradar-skill/1.0"


# ---------------------------------------------------------------------------
# Shared helpers (used across modules)
# ---------------------------------------------------------------------------

def first_non_null(item: dict[str, Any], keys: list[str]) -> Any:
    """Return value of the first key that exists and is not None."""
    for key in keys:
        if key in item and item[key] is not None:
            return item[key]
    return None


def as_percent(value: Any) -> float | None:
    """Convert probability value to 0-100 percentage.

    API returns 0-1 decimals. Values <= 1.0 are multiplied by 100.
    This is the SINGLE conversion point for the entire system.
    """
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        return None
    if v <= 1.0:
        return round(v * 100.0, 6)
    return round(v, 6)


def extract_probability(item: dict[str, Any]) -> float | None:
    """Extract Yes outcome probability as percentage (0-100) from API response.

    Priority: outcomePrices (most accurate real-time price) > other fields.
    lastTradePrice is the last executed trade, NOT the current market price —
    it can be stale and misleading.
    """
    # 1. outcomePrices is the most accurate source (real-time order book mid-price)
    outcome_prices = item.get("outcomePrices")
    if isinstance(outcome_prices, str) and outcome_prices.startswith("["):
        try:
            outcome_prices = json.loads(outcome_prices)
        except (json.JSONDecodeError, ValueError):
            outcome_prices = None
    if isinstance(outcome_prices, list) and outcome_prices:
        p = as_percent(outcome_prices[0])
        if p is not None:
            return p
    # 2. Fallback: other probability fields (excluding lastTradePrice which is stale)
    val = first_non_null(
        item,
        ["probability", "current", "price", "lastPrice", "yesPrice"],
    )
    p = as_percent(val)
    if p is not None:
        return p
    # 3. Last resort: lastTradePrice (may be stale, but better than nothing)
    val = first_non_null(item, ["lastTradePrice"])
    return as_percent(val)


def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    lowered = text.strip().lower()
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return lowered.strip("-") or "unknown"


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

def _api_get(path: str, timeout: int = HTTP_TIMEOUT) -> Any:
    """GET request to gamma API. Returns parsed JSON or raises."""
    url = f"{GAMMA_API_BASE}{path}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---------------------------------------------------------------------------
# URL parsing
# ---------------------------------------------------------------------------

def parse_polymarket_url(url: str) -> str | None:
    """Extract event slug from a Polymarket URL.

    Handles:
      https://polymarket.com/event/grok-5-release
      https://polymarket.com/event/grok-5-release/will-grok-5-be-released
      https://www.polymarket.com/event/grok-5-release?tid=123
    """
    url = url.strip()
    m = re.match(
        r"https?://(?:www\.)?polymarket\.com/event/([a-zA-Z0-9_-]+)",
        url,
    )
    if m:
        return m.group(1)
    return None


# ---------------------------------------------------------------------------
# API resolution: 3-step lookup
# ---------------------------------------------------------------------------

def resolve_event(slug: str) -> dict[str, Any]:
    """Resolve event slug to event info + market list.

    3-step lookup:
      1. GET /events?slug=<slug> — exact match
      2. GET /events?active=true&limit=100 — fuzzy search by slug keywords
      3. Return error dict

    Returns:
      {
        "ok": True,
        "event_title": str,
        "event_id": str,
        "slug": str,
        "markets": [normalized_market, ...]
      }
    or:
      {"ok": False, "error": str}
    """
    # Step 1: exact slug match
    try:
        data = _api_get(f"/events?slug={slug}")
        events = data if isinstance(data, list) else [data] if isinstance(data, dict) else []
        for event in events:
            if not isinstance(event, dict):
                continue
            markets = _extract_markets_from_event(event, slug)
            if markets:
                return {
                    "ok": True,
                    "event_title": str(event.get("title", event.get("slug", slug))),
                    "event_id": str(event.get("id", "")),
                    "slug": slug,
                    "markets": markets,
                }
    except Exception:
        pass  # fall through to step 2

    # Step 2: fuzzy search — split slug into keywords, search in questions
    try:
        data = _api_get("/events?active=true&limit=100")
        events = data if isinstance(data, list) else []
        keywords = set(slug.lower().replace("-", " ").split())
        keywords = {k for k in keywords if len(k) >= 3}

        best_event = None
        best_score = 0
        for event in events:
            if not isinstance(event, dict):
                continue
            title = str(event.get("title", "")).lower()
            event_slug = str(event.get("slug", "")).lower()
            combined = title + " " + event_slug
            hits = sum(1 for k in keywords if k in combined)
            if hits > best_score:
                best_score = hits
                best_event = event

        if best_event and best_score >= max(1, len(keywords) // 2):
            markets = _extract_markets_from_event(best_event, slug)
            if markets:
                return {
                    "ok": True,
                    "event_title": str(best_event.get("title", slug)),
                    "event_id": str(best_event.get("id", "")),
                    "slug": str(best_event.get("slug", slug)),
                    "markets": markets,
                }
    except Exception:
        pass

    # Step 3: not found
    return {
        "ok": False,
        "error": (
            f"Event '{slug}' not found in Polymarket API. "
            "It may be closed, settled, or the URL may be incorrect."
        ),
    }


def _extract_markets_from_event(event: dict[str, Any], slug: str) -> list[dict[str, Any]]:
    """Extract and normalize markets from an event API response."""
    raw_markets = event.get("markets", [])
    if not isinstance(raw_markets, list):
        return []

    event_id = str(event.get("id", ""))
    event_title = str(event.get("title", ""))

    markets = []
    for m in raw_markets:
        if not isinstance(m, dict):
            continue
        normalized = normalize_market(m, slug=slug, event_id=event_id)
        if normalized:
            markets.append(normalized)
    return markets


def normalize_market(
    raw: dict[str, Any],
    slug: str = "",
    event_id: str = "",
) -> dict[str, Any] | None:
    """Normalize a single market from API response to SignalRadar format.

    Returns dict with: market_id, question, probability, slug, event_id,
                       status, end_date, entry_id
    or None if essential data is missing.
    """
    market_id = first_non_null(raw, ["id", "market_id", "marketId", "conditionId"])
    question = first_non_null(raw, ["question", "title", "name"])
    if market_id is None or not question:
        return None

    probability = extract_probability(raw)
    if probability is None:
        return None

    market_id = str(market_id)
    if not event_id:
        event_id = str(first_non_null(raw, ["event_id", "eventId", "event", "parentEvent"]) or market_id)
    if not slug:
        slug = str(raw.get("slug", "") or slugify(str(question)))

    status = str(first_non_null(raw, ["status", "state"]) or "active")
    if "active" in raw and raw.get("active") is False:
        status = "inactive"
    # Check 'closed' field directly
    if raw.get("closed") is True:
        status = "closed"

    end_date = first_non_null(raw, ["endDate", "end_date", "closeTime", "endDateIso"])
    if end_date:
        end_date = str(end_date)[:10]  # Keep only date portion

    # entry_id format: polymarket:{market_id}:{slug}:{event_id}
    entry_id = f"polymarket:{market_id}:{slug}:{event_id}"

    return {
        "market_id": market_id,
        "question": str(question),
        "probability": probability,
        "slug": slug,
        "event_id": event_id,
        "status": status.lower(),
        "end_date": end_date,
        "entry_id": entry_id,
        "url": f"https://polymarket.com/event/{slug}",
    }


# ---------------------------------------------------------------------------
# Single market fetch (for run-time checks)
# ---------------------------------------------------------------------------

def fetch_market_current_result(market_id: str) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    """Fetch current state of a single market by ID with stable error metadata."""
    try:
        raw = _api_get(f"/markets/{market_id}")
        if isinstance(raw, dict):
            market = normalize_market(raw)
            if market is not None:
                # Transient snapshot context for HIT-alert display only.
                # Deliberately NOT added inside normalize_market: that output
                # is persisted to watchlist.json by the add/discover flow,
                # and these point-in-time values must not leak into it.
                market["clob_token_id"] = extract_clob_token_id(raw)
                market["volume_24h"] = _safe_float(raw.get("volume24hr"))
                market["liquidity"] = _safe_float(raw.get("liquidityNum"))
            return market, None
        return None, {
            "code": "SR_SOURCE_UNAVAILABLE",
            "message": "Polymarket API returned an unexpected response for this market.",
        }
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None, {
                "code": "SR_SOURCE_UNAVAILABLE",
                "message": "Polymarket API could not find this market.",
            }
        return None, {
            "code": "SR_SOURCE_UNAVAILABLE",
            "message": f"Polymarket API returned HTTP {exc.code}.",
        }
    except urllib.error.URLError as exc:
        reason = getattr(exc, "reason", None)
        if isinstance(reason, socket.timeout):
            return None, {
                "code": "SR_TIMEOUT",
                "message": "Polymarket API timed out while fetching this market.",
            }
        return None, {
            "code": "SR_SOURCE_UNAVAILABLE",
            "message": "Could not reach Polymarket API.",
        }
    except TimeoutError:
        return None, {
            "code": "SR_TIMEOUT",
            "message": "Polymarket API timed out while fetching this market.",
        }
    except Exception:
        return None, {
            "code": "SR_SOURCE_UNAVAILABLE",
            "message": "Could not fetch current market data from Polymarket API.",
        }
    return None, {
        "code": "SR_SOURCE_UNAVAILABLE",
        "message": "Could not fetch current market data from Polymarket API.",
    }


def fetch_market_current(market_id: str) -> dict[str, Any] | None:
    """Fetch current state of a single market by ID.

    Returns normalized market dict or None on failure.
    """
    market, _error = fetch_market_current_result(market_id)
    return market


# ---------------------------------------------------------------------------
# HIT-alert display context (v1.1.0): 7d price trend + volume/liquidity.
# Display-only enrichment — never feeds decisions, baselines, or audit logs.
# ---------------------------------------------------------------------------

def _safe_float(value: Any) -> float | None:
    """float() that returns None instead of raising on bad input."""
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def extract_clob_token_id(raw: dict[str, Any]) -> str:
    """First CLOB token id (tracks outcomes[0]='Yes', same side as outcomePrices[0]).

    clobTokenIds from the gamma API is a JSON-encoded STRING like
    '["98022...", "5383..."]' — same trap as outcomePrices. Returns "" when
    missing or malformed.
    """
    ids = raw.get("clobTokenIds")
    if isinstance(ids, str):
        try:
            ids = json.loads(ids)
        except (json.JSONDecodeError, ValueError):
            return ""
    if isinstance(ids, list) and ids:
        return str(ids[0]).strip()
    return ""


def fetch_price_history_points(clob_token_id: str) -> list[Any]:
    """Fetch 7-day price history from the Polymarket CLOB API. NEVER raises.

    Returns the raw history point list, or [] on any failure (network error,
    timeout, HTTP error, bad JSON — and unknown tokens, for which CLOB
    returns HTTP 200 with {"history": []} rather than an error).

    Deliberately not routed through _api_get: different host, shorter
    timeout, and a never-raise contract (alerts must deliver even when
    CLOB is down).
    """
    token = str(clob_token_id or "").strip()
    if not token:
        return []
    try:
        url = (
            f"{CLOB_API_BASE}/prices-history"
            f"?market={urllib.parse.quote(token)}&interval=1w&fidelity=360"
        )
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=TREND_HTTP_TIMEOUT) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        history = data.get("history") if isinstance(data, dict) else None
        return history if isinstance(history, list) else []
    except Exception:  # noqa: BLE001 — graceful degradation by design
        return []


def summarize_trend(points: Any) -> dict[str, Any] | None:
    """Summarize CLOB price-history points into percent stats. Pure; never raises.

    Returns {"start_pct", "end_pct", "low_pct", "high_pct", "points"} or None
    when fewer than 2 valid points survive filtering.
    """
    samples: list[tuple[int, float]] = []
    for item in points if isinstance(points, list) else []:
        if not isinstance(item, dict):
            continue
        try:
            t = int(item.get("t"))
            p = float(item.get("p"))
        except (TypeError, ValueError):
            continue
        if not (0.0 <= p <= 1.0):
            continue
        samples.append((t, p))
    if len(samples) < 2:
        return None
    samples.sort(key=lambda s: s[0])
    probs = [p for _, p in samples]
    return {
        "start_pct": round(probs[0] * 100.0, 1),
        "end_pct": round(probs[-1] * 100.0, 1),
        "low_pct": round(min(probs) * 100.0, 1),
        "high_pct": round(max(probs) * 100.0, 1),
        "points": len(probs),
    }


# ---------------------------------------------------------------------------
# Settled detection
# ---------------------------------------------------------------------------

def is_settled(market: dict[str, Any]) -> bool:
    """Determine if a market is settled.

    Priority: API status fields first, end_date fallback.
    """
    status = str(market.get("status", "")).lower()
    if status in ("closed", "resolved", "settled", "inactive"):
        return True

    # end_date fallback
    end_date = market.get("end_date")
    if end_date:
        try:
            ed = datetime.strptime(str(end_date)[:10], "%Y-%m-%d").replace(tzinfo=timezone.utc)
            if ed < datetime.now(timezone.utc):
                return True
        except (ValueError, TypeError):
            pass

    return False


def safe_name(entry_id: str) -> str:
    """Convert entry_id to filesystem-safe name for baseline files."""
    return re.sub(r"[:/\\]", "_", entry_id)


# ---------------------------------------------------------------------------
# Onboarding preset URLs
# ---------------------------------------------------------------------------

ONBOARDING_URLS = [
    "https://polymarket.com/event/what-price-will-bitcoin-hit-before-2027",
    "https://polymarket.com/event/gpt-6-released-by",
    "https://polymarket.com/event/us-x-iran-ceasefire-by",
    "https://polymarket.com/event/claude-5-released-by",
    "https://polymarket.com/event/will-jesus-christ-return-before-2027",
    "https://polymarket.com/event/will-the-us-confirm-that-aliens-exist-before-2027",
]
