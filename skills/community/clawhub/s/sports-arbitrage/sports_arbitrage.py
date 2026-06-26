#!/usr/bin/env python3
"""
Sports Arbitrage Scanner
========================
ClawHub automaton skill that scans sports odds across multiple bookmakers,
detects arbitrage opportunities, calculates optimal stake splits, and logs
all actionable arbs (> MIN_PROFIT_PCT) to stdout and a JSON results file.

Arbitrage condition: sum(1/odds_i) < 1.0 using best available odds per outcome
from any bookmaker combination.

Author:  Mibayy
Version: 1.0.0
"""

import os
import sys
import json
import logging
import datetime
import itertools
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: 'requests' package is not installed. Run: pip install requests")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Configuration from environment variables
# ---------------------------------------------------------------------------
ODDS_API_KEY   = os.environ.get("ODDS_API_KEY", "")          # Optional API key
MIN_PROFIT_PCT = float(os.environ.get("MIN_PROFIT_PCT", "0.5"))  # Min profit % to report
TOTAL_STAKE    = float(os.environ.get("TOTAL_STAKE", "1000"))    # Hypothetical stake
RESULTS_FILE   = os.environ.get("RESULTS_FILE", "/tmp/sports_arb_results.json")

# Comma-separated sport keys to scan (The Odds API sport key format)
SPORTS_RAW = os.environ.get(
    "SPORTS",
    "soccer_epl,basketball_nba,americanfootball_nfl"
)
SPORTS = [s.strip() for s in SPORTS_RAW.split(",") if s.strip()]

# The Odds API base URL
ODDS_API_BASE = "https://api.the-odds-api.com/v4"

# Odds format: decimal (European) for easier arb math
ODDS_FORMAT = "decimal"

# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%SZ",
    handlers=[logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger("sports_arb")


# ---------------------------------------------------------------------------
# Sample / demo data — used when ODDS_API_KEY is not set
# ---------------------------------------------------------------------------
DEMO_EVENTS = [
    # Crafted so one event has a real arb, others do not
    {
        "id": "demo_001",
        "sport_key": "soccer_epl",
        "sport_title": "EPL",
        "commence_time": "2026-03-21T15:00:00Z",
        "home_team": "Arsenal",
        "away_team": "Chelsea",
        "bookmakers": [
            {
                "key": "pinnacle",
                "title": "Pinnacle",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Arsenal",  "price": 2.20},
                            {"name": "Chelsea",  "price": 3.60},
                            {"name": "Draw",     "price": 3.30},
                        ],
                    }
                ],
            },
            {
                "key": "bet365",
                "title": "Bet365",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Arsenal",  "price": 2.05},
                            {"name": "Chelsea",  "price": 3.90},   # Higher than Pinnacle
                            {"name": "Draw",     "price": 3.50},
                        ],
                    }
                ],
            },
            {
                "key": "draftkings",
                "title": "DraftKings",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Arsenal",  "price": 2.30},   # Best for Arsenal
                            {"name": "Chelsea",  "price": 3.55},
                            {"name": "Draw",     "price": 3.25},
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "demo_002",
        "sport_key": "basketball_nba",
        "sport_title": "NBA",
        "commence_time": "2026-03-21T23:00:00Z",
        "home_team": "Lakers",
        "away_team": "Celtics",
        "bookmakers": [
            {
                "key": "fanduel",
                "title": "FanDuel",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Lakers",   "price": 1.90},
                            {"name": "Celtics",  "price": 1.95},
                        ],
                    }
                ],
            },
            {
                "key": "betmgm",
                "title": "BetMGM",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Lakers",   "price": 2.05},   # Inflated vs FanDuel Celtics
                            {"name": "Celtics",  "price": 2.00},   # Inflated — creates real arb
                        ],
                    }
                ],
            },
        ],
    },
    {
        "id": "demo_003",
        "sport_key": "americanfootball_nfl",
        "sport_title": "NFL",
        "commence_time": "2026-03-22T18:00:00Z",
        "home_team": "Chiefs",
        "away_team": "Eagles",
        "bookmakers": [
            {
                "key": "williamhill_us",
                "title": "William Hill",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Chiefs",   "price": 1.65},
                            {"name": "Eagles",   "price": 2.30},
                        ],
                    }
                ],
            },
            {
                "key": "pointsbetus",
                "title": "PointsBet",
                "markets": [
                    {
                        "key": "h2h",
                        "outcomes": [
                            {"name": "Chiefs",   "price": 1.70},
                            {"name": "Eagles",   "price": 2.20},
                        ],
                    }
                ],
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def fetch_events_for_sport(sport_key: str) -> list:
    """
    Fetch upcoming events and their odds for a given sport from The Odds API.
    Returns a list of event dicts on success, empty list on any error.
    """
    url = f"{ODDS_API_BASE}/sports/{sport_key}/odds"
    params = {
        "apiKey":    ODDS_API_KEY,
        "regions":   "us,uk,eu,au",
        "markets":   "h2h",
        "oddsFormat": ODDS_FORMAT,
    }
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code == 401:
            log.warning("ODDS_API_KEY is invalid or expired for sport: %s", sport_key)
            return []
        if resp.status_code == 422:
            log.warning("Unknown sport key '%s' — skipping.", sport_key)
            return []
        if resp.status_code == 429:
            log.warning("Rate limit hit on The Odds API. Slow down or upgrade plan.")
            return []
        resp.raise_for_status()
        events = resp.json()
        log.info("Fetched %d events for sport: %s", len(events), sport_key)
        return events
    except requests.exceptions.ConnectionError:
        log.error("Network error fetching odds for %s — check internet connection.", sport_key)
        return []
    except requests.exceptions.Timeout:
        log.error("Timeout fetching odds for %s.", sport_key)
        return []
    except requests.exceptions.RequestException as exc:
        log.error("Request error for %s: %s", sport_key, exc)
        return []
    except ValueError:
        log.error("Failed to parse JSON response for %s.", sport_key)
        return []


def fetch_all_events() -> list:
    """
    Fetch odds for all configured sports.
    Falls back to demo data when ODDS_API_KEY is not configured.
    """
    if not ODDS_API_KEY:
        log.info(
            "ODDS_API_KEY not set — using built-in demo data. "
            "Set ODDS_API_KEY to scan live odds from The Odds API."
        )
        return DEMO_EVENTS

    all_events = []
    for sport in SPORTS:
        events = fetch_events_for_sport(sport)
        all_events.extend(events)

    if not all_events:
        log.warning("No live events retrieved — falling back to demo data.")
        return DEMO_EVENTS

    return all_events


# ---------------------------------------------------------------------------
# Arbitrage detection logic
# ---------------------------------------------------------------------------

def extract_best_odds(event: dict) -> dict:
    """
    Given an event dict (from The Odds API), find the best (highest) decimal
    odds for each outcome name across all bookmakers. Returns a dict:
      { outcome_name: {"odds": float, "bookmaker": str} }
    """
    best: dict = {}

    bookmakers = event.get("bookmakers", [])
    for bk in bookmakers:
        bk_key   = bk.get("key", "unknown")
        bk_title = bk.get("title", bk_key)
        for market in bk.get("markets", []):
            if market.get("key") != "h2h":
                continue
            for outcome in market.get("outcomes", []):
                name  = outcome.get("name", "")
                price = outcome.get("price", 0.0)
                if not name or price <= 1.0:
                    continue
                if name not in best or price > best[name]["odds"]:
                    best[name] = {
                        "odds":       price,
                        "bookmaker":  bk_title,
                        "bk_key":     bk_key,
                    }
    return best


def detect_arbitrage(event: dict) -> Optional[dict]:
    """
    Check a single event for an arbitrage opportunity using the best available
    odds per outcome across all bookmakers.

    Arb condition: sum(1 / best_odds_i  for each outcome i) < 1.0

    Returns an arb dict if a qualifying opportunity is found, else None.
    """
    match_name = f"{event.get('home_team', '?')} vs {event.get('away_team', '?')}"
    sport_key  = event.get("sport_key", "unknown")
    commence   = event.get("commence_time", "")

    best_odds = extract_best_odds(event)
    if len(best_odds) < 2:
        # Need at least two outcomes for arb
        return None

    # Compute implied probabilities using best odds
    outcomes    = list(best_odds.keys())
    implied     = {name: 1.0 / best_odds[name]["odds"] for name in outcomes}
    total_impl  = sum(implied.values())

    if total_impl >= 1.0:
        # No arb: bookmakers' edge is too large
        return None

    profit_pct = (1.0 - total_impl) / total_impl * 100.0

    if profit_pct < MIN_PROFIT_PCT:
        # Arb exists but below our worthwhile threshold
        log.debug(
            "Arb below threshold (%.4f%%) for %s — skipping.", profit_pct, match_name
        )
        return None

    # Calculate optimal stake per outcome
    # Stake_i = Total * (implied_i / total_implied)
    # This ensures each outcome returns exactly Total / total_implied
    guaranteed_return = TOTAL_STAKE / total_impl
    outcome_details = []
    for name in outcomes:
        odds   = best_odds[name]["odds"]
        impl   = implied[name]
        stake  = TOTAL_STAKE * (impl / total_impl)
        outcome_details.append({
            "name":            name,
            "bookmaker":       best_odds[name]["bookmaker"],
            "bookmaker_key":   best_odds[name]["bk_key"],
            "odds":            round(odds, 4),
            "implied_prob":    round(impl, 6),
            "stake":           round(stake, 2),
            "potential_return": round(stake * odds, 2),
        })

    return {
        "match":              match_name,
        "sport":              sport_key,
        "commence_time":      commence,
        "profit_pct":         round(profit_pct, 4),
        "total_implied_prob": round(total_impl, 6),
        "outcomes":           outcome_details,
        "total_stake":        TOTAL_STAKE,
        "guaranteed_return":  round(guaranteed_return, 2),
        "detected_at":        datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


# ---------------------------------------------------------------------------
# Output / persistence helpers
# ---------------------------------------------------------------------------

def log_arb(arb: dict) -> None:
    """Pretty-print an arbitrage opportunity to the log / stdout."""
    log.info("=" * 60)
    log.info("ARB FOUND: %s  [%s]", arb["match"], arb["sport"])
    log.info(
        "  Profit: %.4f%%  |  Stake: %.2f  |  Guaranteed Return: %.2f",
        arb["profit_pct"], arb["total_stake"], arb["guaranteed_return"],
    )
    log.info("  Commence: %s", arb["commence_time"])
    for oc in arb["outcomes"]:
        log.info(
            "    %-20s  odds=%-6.2f  bk=%-15s  stake=%-8.2f  return=%.2f",
            oc["name"], oc["odds"], oc["bookmaker"], oc["stake"], oc["potential_return"],
        )
    log.info("=" * 60)


def save_results(arbs: list) -> None:
    """
    Persist arb results to the configured RESULTS_FILE as JSON.
    Appends to existing results (deduped by match+detected_at key).
    """
    existing = []
    if os.path.exists(RESULTS_FILE):
        try:
            with open(RESULTS_FILE, "r") as fh:
                existing = json.load(fh)
            if not isinstance(existing, list):
                existing = []
        except (ValueError, OSError) as exc:
            log.warning("Could not read existing results file (%s) — starting fresh.", exc)
            existing = []

    # Build a dedup key set from existing entries
    seen = {
        f"{e.get('match')}|{e.get('detected_at')}"
        for e in existing
    }
    new_entries = [
        a for a in arbs
        if f"{a['match']}|{a['detected_at']}" not in seen
    ]
    combined = existing + new_entries

    # Keep only the last 500 results to avoid unbounded growth
    combined = combined[-500:]

    try:
        with open(RESULTS_FILE, "w") as fh:
            json.dump(combined, fh, indent=2)
        log.info(
            "Results saved to %s (%d new, %d total).",
            RESULTS_FILE, len(new_entries), len(combined),
        )
    except OSError as exc:
        log.error("Failed to write results file %s: %s", RESULTS_FILE, exc)


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """
    Main scan loop:
      1. Fetch odds from The Odds API (or demo data).
      2. For each event, detect arbitrage using best cross-bookmaker odds.
      3. Log and save qualifying arbs (profit > MIN_PROFIT_PCT).
    """
    log.info("Sports Arbitrage Scanner v1.0.0 — starting scan")
    log.info(
        "Config: sports=%s | min_profit=%.2f%% | total_stake=%.2f | results=%s",
        SPORTS, MIN_PROFIT_PCT, TOTAL_STAKE, RESULTS_FILE,
    )

    events = fetch_all_events()
    log.info("Total events to analyse: %d", len(events))

    arbs_found: list = []

    for event in events:
        try:
            arb = detect_arbitrage(event)
            if arb:
                arbs_found.append(arb)
                log_arb(arb)
        except Exception as exc:  # pylint: disable=broad-except
            match = f"{event.get('home_team', '?')} vs {event.get('away_team', '?')}"
            log.error("Unexpected error processing event '%s': %s", match, exc)

    # Summary
    log.info("-" * 60)
    log.info(
        "Scan complete. %d arbitrage opportunit%s found (min %.2f%% profit).",
        len(arbs_found),
        "y" if len(arbs_found) == 1 else "ies",
        MIN_PROFIT_PCT,
    )

    if arbs_found:
        save_results(arbs_found)
    else:
        log.info("No actionable arbs this run — results file unchanged.")
        # Still write an empty-run marker so the file always exists
        if not os.path.exists(RESULTS_FILE):
            try:
                with open(RESULTS_FILE, "w") as fh:
                    json.dump([], fh)
            except OSError:
                pass


if __name__ == "__main__":
    main()
