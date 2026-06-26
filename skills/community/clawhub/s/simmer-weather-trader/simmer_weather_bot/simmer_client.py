import httpx
import re
import logging
from datetime import date, datetime, timezone
from config import SIMMER_API_KEY, SIMMER_BASE_URL, SIMMER_VENUE, HTTP_TIMEOUT
from city_map import resolve_city, celsius_to_fahrenheit

logger = logging.getLogger(__name__)

SIMMER_HEADERS = {
    "Authorization": f"Bearer {SIMMER_API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}


def _parse_time_to_resolution(s) -> float:
    """Parse '1d 0h' or '2d 12h' or raw number into hours float."""
    if s is None:
        return 999.0
    if isinstance(s, (int, float)):
        return float(s)
    s = str(s)
    days = re.search(r'(\d+)\s*d', s)
    hours = re.search(r'(\d+)\s*h', s)
    total = 0.0
    if days:
        total += int(days.group(1)) * 24
    if hours:
        total += int(hours.group(1))
    return total if total > 0 else 999.0


def _parse_market_question(question: str) -> dict:
    """
    Parses a Simmer weather market question to extract city, date, min_temp, max_temp.
    Handles both Fahrenheit and Celsius markets.
    Returns temps always in Fahrenheit.
    """
    result = {"city": None, "date": None, "min_temp": None, "max_temp": None, "unit": "F"}

    is_celsius = bool(re.search(r'°C\b', question, re.IGNORECASE))
    if is_celsius:
        result["unit"] = "C"

    range_match = re.search(r'(\d+)\s*[-–to]+\s*(\d+)\s*°?[FC]', question, re.IGNORECASE)
    if range_match:
        lo = int(range_match.group(1))
        hi = int(range_match.group(2))
        if is_celsius:
            result["min_temp"] = celsius_to_fahrenheit(lo)
            result["max_temp"] = celsius_to_fahrenheit(hi)
        else:
            result["min_temp"] = lo
            result["max_temp"] = hi

    if result["min_temp"] is None:
        single_match = re.search(r'(\d+)\s*°?([FC])\b', question)
        if single_match:
            t = int(single_match.group(1))
            unit = single_match.group(2).upper()
            if unit == "C":
                result["min_temp"] = celsius_to_fahrenheit(t)
                result["max_temp"] = celsius_to_fahrenheit(t)
            else:
                result["min_temp"] = t
                result["max_temp"] = t

    if result["min_temp"] is None:
        below_match = re.search(r'(\d+)\s*°?F\s+or\s+below', question, re.IGNORECASE)
        if below_match:
            t = int(below_match.group(1))
            result["min_temp"] = 0
            result["max_temp"] = t

    date_iso = re.search(r'\d{4}-\d{2}-\d{2}', question)
    if date_iso:
        result["date"] = date.fromisoformat(date_iso.group(0))
    else:
        current_year = datetime.now().year
        date_words = re.search(
            r'(January|February|March|April|May|June|July|August|September|October|November|December)'
            r'\s+(\d{1,2})(?:,\s*(\d{4}))?',
            question, re.IGNORECASE
        )
        if date_words:
            month_str = date_words.group(1)
            day = int(date_words.group(2))
            year = int(date_words.group(3)) if date_words.group(3) else current_year
            try:
                result["date"] = datetime.strptime(f"{month_str} {day} {year}", "%B %d %Y").date()
            except ValueError:
                pass

    city_patterns = [
        r'\bin\s+([A-Z][a-zA-Z\s]+?)\s+(?:be\s|between\s|above\s|below\s|exceed)',
        r'\bin\s+([A-Z][a-zA-Z\s]+?)\s+(?:on\s)',
        r'\bin\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s',
    ]
    for pattern in city_patterns:
        match = re.search(pattern, question)
        if match:
            candidate = match.group(1).strip().rstrip("'s")
            try:
                resolve_city(candidate)
                result["city"] = candidate
                break
            except ValueError:
                continue

    return result


def _parse_context(ctx: dict) -> dict:
    """Normalise the Simmer context response into a flat dict for our pipeline."""
    market = ctx.get("market", {})
    edge = ctx.get("edge", {})
    slippage_info = ctx.get("slippage", {})
    warnings_list = ctx.get("warnings", [])

    spread_pct = slippage_info.get("spread_pct", None)
    if spread_pct is not None:
        spread_pct = round(spread_pct * 100, 2)

    time_to_res_raw = market.get("time_to_resolution", None)
    time_to_res_hours = _parse_time_to_resolution(time_to_res_raw)

    recommendation = edge.get("recommendation", None)

    return {
        "edge": {
            "recommendation": recommendation,
            "edge_pct": edge.get("user_edge", None),
        },
        "slippage_estimate": spread_pct,
        "time_to_resolution": time_to_res_hours,
        "warnings": warnings_list,
        "position": ctx.get("position", {}),
        "resolves_at": market.get("resolves_at", ""),
    }


async def fetch_weather_markets(limit: int = 20) -> list[dict]:
    """
    Fetches active weather markets from Simmer API.
    Returns a list of enriched market dicts with parsed city, date, min/max temp.
    """
    url = f"{SIMMER_BASE_URL}/api/sdk/markets"
    params = {"tags": "weather", "status": "active", "limit": limit}

    logger.info(f"Simmer: fetching weather markets from {url}")

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(url, headers=SIMMER_HEADERS, params=params)
        if resp.status_code != 200:
            raise Exception(f"Simmer markets API returned HTTP {resp.status_code}: {resp.text[:300]}")
        raw = resp.json()

    if isinstance(raw, list):
        markets_raw = raw
    else:
        markets_raw = raw.get("markets", raw.get("data", raw.get("results", [])))

    if len(markets_raw) == 0:
        raise Exception("Simmer returned 0 active weather markets")

    enriched = []
    for m in markets_raw:
        question = m.get("question", "")
        parsed = _parse_market_question(question)

        enriched_market = {
            "id": m.get("id"),
            "question": question,
            "status": m.get("status", "unknown"),
            "current_probability": m.get("current_probability", m.get("probability", None)),
            "url": m.get("url", ""),
            "resolves_at": m.get("resolves_at", ""),
            "tags": m.get("tags", []),
            "city": parsed["city"],
            "date": parsed["date"],
            "min_temp": parsed["min_temp"],
            "max_temp": parsed["max_temp"],
            "unit": parsed["unit"],
        }
        enriched.append(enriched_market)
        logger.info(
            f"Market: {question[:80]} | "
            f"city={parsed['city']} date={parsed['date']} "
            f"temps=[{parsed['min_temp']}-{parsed['max_temp']}°F] unit={parsed['unit']}"
        )

    return enriched


async def get_market_context(market_id: str) -> dict:
    """Fetches and normalises Simmer market context."""
    url = f"{SIMMER_BASE_URL}/api/sdk/context/{market_id}"
    logger.info(f"Simmer: fetching context for market {market_id}")

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(url, headers=SIMMER_HEADERS)
        if resp.status_code != 200:
            raise Exception(f"Simmer context API returned HTTP {resp.status_code}: {resp.text[:300]}")
        raw_ctx = resp.json()

    context = _parse_context(raw_ctx)
    logger.info(
        f"Simmer context: recommendation={context['edge']['recommendation']} "
        f"slippage={context['slippage_estimate']}% "
        f"time_to_resolution={context['time_to_resolution']}h "
        f"warnings={len(context['warnings'])}"
    )
    return context


async def execute_trade(market_id: str, reasoning: str) -> dict:
    """Executes a YES trade on the given market via Simmer SDK endpoint."""
    from config import TRADE_AMOUNT
    url = f"{SIMMER_BASE_URL}/api/sdk/trade"

    payload = {
        "market_id": market_id,
        "side": "yes",
        "amount": TRADE_AMOUNT,
        "venue": SIMMER_VENUE,
        "reasoning": reasoning,
        "source": "sdk:weather-bot",
    }

    logger.info(f"Simmer: executing trade on market {market_id} venue={SIMMER_VENUE} amount={TRADE_AMOUNT}")

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.post(url, json=payload, headers=SIMMER_HEADERS)
        if resp.status_code not in (200, 201):
            raise Exception(f"Simmer trade API returned HTTP {resp.status_code}: {resp.text[:300]}")
        result = resp.json()

    logger.info(f"Simmer trade result: {result}")
    return result


async def get_positions() -> list:
    """Fetches current agent positions."""
    url = f"{SIMMER_BASE_URL}/api/sdk/positions"
    params = {"venue": SIMMER_VENUE}

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(url, headers=SIMMER_HEADERS, params=params)
        if resp.status_code != 200:
            raise Exception(f"Simmer positions API returned HTTP {resp.status_code}: {resp.text[:200]}")
        data = resp.json()

    if isinstance(data, list):
        return data
    return data.get("positions", data.get("data", []))


async def get_agent_info() -> dict:
    """Fetches agent info including balance and limits."""
    url = f"{SIMMER_BASE_URL}/api/sdk/agents/me"

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(url, headers=SIMMER_HEADERS)
        if resp.status_code != 200:
            raise Exception(f"Simmer agent API returned HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()


async def get_briefing() -> dict:
    """Fetches full agent briefing."""
    url = f"{SIMMER_BASE_URL}/api/sdk/briefing"

    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        resp = await client.get(url, headers=SIMMER_HEADERS)
        if resp.status_code != 200:
            raise Exception(f"Simmer briefing API returned HTTP {resp.status_code}: {resp.text[:200]}")
        return resp.json()
