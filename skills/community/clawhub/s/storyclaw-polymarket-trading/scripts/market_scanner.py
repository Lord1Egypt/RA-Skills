#!/usr/bin/env python3
"""
Market scanner: discover Polymarket markets matching a strategy filter.
Uses the Gamma API for keyword search + liquidity/expiry filtering.

Filter schema:
  keywords (list[str]):         search terms, OR logic
  min_liquidity_usdc (float):   minimum CLOB liquidity (default 1000)
  max_days_to_expiry (int):     only markets expiring within N days (default 30)
  min_days_to_expiry (int):     skip if expiring in < N days (default 1)

Returns list of dicts:
  token_id, end_ts, name, outcome, liquidity, slug
"""

import json
import time
import urllib.request
import urllib.parse

GAMMA_BASE = "https://gamma-api.polymarket.com"
HEADERS = {"User-Agent": "Mozilla/5.0"}

# Maps common keywords to Gamma API tag slugs for broad category pre-filtering.
# Keywords not in this map fall back to fetching all active events.
KEYWORD_TO_TAGS = {
    "bitcoin": ["crypto"],
    "btc": ["crypto"],
    "ethereum": ["crypto"],
    "eth": ["crypto"],
    "crypto": ["crypto"],
    "solana": ["crypto"],
    "sol": ["crypto"],
    "trump": ["politics"],
    "congress": ["politics"],
    "senate": ["politics"],
    "election": ["politics"],
    "president": ["politics"],
    "democrat": ["politics"],
    "republican": ["politics"],
    "sports": ["sports"],
    "soccer": ["sports"],
    "football": ["sports"],
    "world cup": ["sports"],
    "nba": ["sports"],
    "nfl": ["sports"],
    "tennis": ["sports"],
    "f1": ["sports"],
}

# Broad/category keywords that map to a tag but shouldn't be used to filter
# event titles — they're too generic to appear literally in market questions.
BROAD_KEYWORDS = {
    "crypto", "politics", "sports", "finance", "tech", "science",
    "entertainment", "business", "economy", "world",
}


def _gamma_get(path):
    url = f"{GAMMA_BASE}{path}"
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def _parse_end_ts(end_date_str):
    if not end_date_str:
        return None
    try:
        import datetime
        s = end_date_str.replace("Z", "+00:00")
        dt = datetime.datetime.fromisoformat(s)
        return int(dt.timestamp())
    except Exception:
        return None


def _parse_token_ids(clob_raw):
    if not clob_raw:
        return []
    try:
        return json.loads(clob_raw) if isinstance(clob_raw, str) else clob_raw
    except Exception:
        return []


def _parse_outcomes(outcomes_raw):
    if not outcomes_raw:
        return []
    try:
        return json.loads(outcomes_raw) if isinstance(outcomes_raw, str) else outcomes_raw
    except Exception:
        return []


def _fetch_events_by_tag(tag_slug, limit=200):
    """Fetch events from Gamma API filtered by tag slug."""
    try:
        data = _gamma_get(f"/events?active=true&closed=false&limit={limit}&tag_slug={tag_slug}")
        return data if isinstance(data, list) else data.get("data", [])
    except Exception:
        return []


def scan_markets(market_filter):
    """
    Search for markets matching the filter. Returns up to 20 results sorted
    by liquidity descending.

    Strategy:
    1. Map keywords → tag slugs for broad category fetch via events endpoint
    2. Filter events/markets client-side: keyword must appear in event title or market question
    3. Apply liquidity and expiry filters
    """
    keywords = market_filter.get("keywords", [])
    min_liq = float(market_filter.get("min_liquidity_usdc", 1000))
    max_days = int(market_filter.get("max_days_to_expiry", 30))
    min_days = int(market_filter.get("min_days_to_expiry", 1))

    now = time.time()
    max_end_ts = now + max_days * 86400
    min_end_ts = now + min_days * 86400

    kws_lower = [k.lower() for k in keywords]

    # Split into broad (tag-only) and specific (must match title) keywords
    broad_kws = [kw for kw in kws_lower if kw in BROAD_KEYWORDS]
    specific_kws = [kw for kw in kws_lower if kw not in BROAD_KEYWORDS]

    # Collect tag slugs to fetch, deduplicated
    tag_slugs = set()
    for kw in kws_lower:
        tags = KEYWORD_TO_TAGS.get(kw)
        if tags:
            tag_slugs.update(tags)
    if not tag_slugs:
        # Unknown keywords — search across common tags
        tag_slugs = {"crypto", "politics", "sports", "finance", "tech"}

    # Fetch events per tag slug
    all_events = []
    seen_event_ids = set()
    for slug in tag_slugs:
        for event in _fetch_events_by_tag(slug):
            eid = event.get("id")
            if eid and eid not in seen_event_ids:
                seen_event_ids.add(eid)
                all_events.append(event)

    results = []
    seen_tokens = set()

    for event in all_events:
        event_title = (event.get("title") or "").lower()

        # Broad-only keywords: tag fetch is sufficient, skip title filter
        # Specific keywords: at least one must appear in the event title
        if specific_kws and not any(kw in event_title for kw in specific_kws):
            continue

        event_liq = float(event.get("liquidityClob") or event.get("liquidity") or 0)
        if event_liq < min_liq:
            continue

        for m in (event.get("markets") or []):
            if not m.get("active") or m.get("closed"):
                continue

            end_ts = _parse_end_ts(m.get("endDate") or m.get("endDateIso"))
            if not end_ts or end_ts < min_end_ts or end_ts > max_end_ts:
                continue

            liq = float(m.get("liquidityClob") or m.get("liquidity") or 0)
            if liq < min_liq:
                continue

            token_ids = _parse_token_ids(m.get("clobTokenIds"))
            outcomes = _parse_outcomes(m.get("outcomes"))

            for i, token_id in enumerate(token_ids):
                if token_id in seen_tokens:
                    continue
                seen_tokens.add(token_id)
                outcome = outcomes[i] if i < len(outcomes) else f"outcome_{i}"
                results.append({
                    "token_id": token_id,
                    "end_ts": end_ts,
                    "name": m.get("question", event.get("title", "unknown")),
                    "outcome": outcome,
                    "liquidity": liq,
                    "slug": m.get("slug", event.get("slug", "")),
                })

    results.sort(key=lambda x: x["liquidity"], reverse=True)
    return results[:20]


if __name__ == "__main__":
    import sys
    keywords = sys.argv[1:] or ["trump", "election"]
    filt = {"keywords": keywords, "min_liquidity_usdc": 500, "max_days_to_expiry": 60}
    markets = scan_markets(filt)
    print(f"Found {len(markets)} markets:")
    for m in markets:
        import datetime
        exp = datetime.datetime.fromtimestamp(m["end_ts"], tz=datetime.timezone.utc).strftime("%Y-%m-%d")
        print(f"  [{m['outcome']}] {m['name'][:60]}  liq=${m['liquidity']:.0f}  exp={exp}")
        print(f"    token: {m['token_id'][:30]}...")
