#!/usr/bin/python3
"""
Sports Ticker - Display results and upcoming fixtures for your teams.
Includes web search fallback when ESPN returns no match.
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from espn import find_team_match, format_match, get_scoreboard, FOOTBALL_LEAGUES
from config import get_teams
from cache import write_to_cache, format_cached_result


def _load_key(env_var: str, env_file_key: str) -> str:
    """Load API key from env or web-search-plus .env file."""
    key = os.environ.get(env_var, "")
    if not key:
        env_paths = [
            Path(__file__).parent.parent.parent / "web-search-plus" / ".env",
            Path(os.environ.get("HOME", "/root")) / "clawd/skills/web-search-plus/.env",
        ]
        for ep in env_paths:
            if ep.exists():
                for line in ep.read_text().splitlines():
                    if env_file_key in line and "=" in line:
                        key = line.split("=", 1)[-1].strip().strip("'\"").lstrip("export ")
                        break
    return key


def web_search_match(team_name: str, team_key: str = "") -> str:
    """Fallback: search for today's match/result. Brave first, Serper fallback.
    
    If a result is found, it is written to the score cache under `team_key`
    (defaults to `team_name` when not provided).
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    query = f"{team_name} match result {today}"
    _cache_key = team_key or team_name

    # 1. Try Brave Search (OpenClaw default) — only if key is set
    brave_key = os.environ.get("BRAVE_SEARCH_API_KEY", "")
    if brave_key:
        try:
            params = urllib.parse.urlencode({"q": query, "count": 3})
            req = urllib.request.Request(
                f"https://api.search.brave.com/res/v1/web/search?{params}",
                headers={"Accept": "application/json", "X-Subscription-Token": brave_key},
            )
            data = json.loads(urllib.request.urlopen(req, timeout=10).read())
            snippets = []
            for r in data.get("web", {}).get("results", [])[:3]:
                snippet = r.get("description", "")
                title = r.get("title", "")
                if snippet:
                    snippets.append(f"• {title}: {snippet[:120]}")
            if snippets:
                result_text = "🔍 Web:\n" + "\n".join(snippets)
                write_to_cache(_cache_key, snippets[0], source="brave_search")
                return result_text
        except Exception:
            pass  # Fall through to Serper

    # 2. Serper fallback
    serper_key = _load_key("SERPER_API_KEY", "SERPER_API_KEY")
    if serper_key:
        try:
            payload = json.dumps({"q": query, "num": 3}).encode()
            req = urllib.request.Request(
                "https://google.serper.dev/search",
                data=payload,
                headers={"X-API-KEY": serper_key, "Content-Type": "application/json"},
            )
            data = json.loads(urllib.request.urlopen(req, timeout=10).read())
            snippets = []
            for r in data.get("organic", [])[:3]:
                snippet = r.get("snippet", "")
                title = r.get("title", "")
                if snippet:
                    snippets.append(f"• {title}: {snippet[:120]}")
            if snippets:
                result_text = "🔍 Web:\n" + "\n".join(snippets)
                write_to_cache(_cache_key, snippets[0], source="serper_search")
                return result_text
        except Exception as e:
            return f"🔍 Web search failed: {e}"

    # 3. No API key — fall back to cache
    cached = format_cached_result(_cache_key)
    if cached:
        return f"📦 {cached}"

    return "🔍 No search API key — web fallback unavailable."


def team_ticker(team: dict) -> str:
    """Generate ticker for a single team."""
    lines = []
    name = team.get("name", "Unknown")
    emoji = team.get("emoji", "⚽")
    espn_id = team.get("espn_id")
    leagues = team.get("espn_leagues", ["eng.1"])
    sport = team.get("sport", "soccer")
    team_key = team.get("short_name", name)

    lines.append(f"{emoji} **{name}**\n")

    if espn_id:
        match = find_team_match(espn_id, leagues, sport)
        if match:
            result = format_match(match["event"], include_events=True,
                                  sport=sport, league=match["league"])
            lines.append(result)
            # Cache the formatted result as well
            write_to_cache(team_key, result, source="espn")
        else:
            # ESPN found nothing — web search fallback, then cache fallback
            web_result = web_search_match(name, team_key)
            lines.append(web_result)
            # If web search found nothing and cache exists, show cached result
            if "unavailable" in web_result or "failed" in web_result:
                cached = format_cached_result(team_key)
                if cached:
                    lines.append(f"\n📦 {cached}")
    else:
        # No ESPN ID — web search fallback, with cache backup
        web_result = web_search_match(name, team_key)
        lines.append(web_result)
        if "unavailable" in web_result or "failed" in web_result:
            cached = format_cached_result(team_key)
            if cached:
                lines.append(f"\n📦 {cached}")

    return "\n".join(lines)


def all_teams_ticker() -> str:
    """Generate ticker for all configured teams."""
    teams = get_teams()

    if not teams:
        return "No teams configured. Copy config.example.json to config.json and add your teams!"

    parts = []
    for team in teams:
        parts.append(team_ticker(team))

    if not parts:
        return "No teams configured."

    return ("\n" + "─" * 30 + "\n").join(parts)

def league_ticker(league: str = "eng.1", sport: str = "soccer") -> str:
    """Show all matches in a league."""
    from espn import LEAGUES
    sport_leagues = LEAGUES.get(sport, {})
    lines = [f"**{sport_leagues.get(league, league)}**\n"]

    data = get_scoreboard(sport, league)
    events = data.get("events", [])

    if not events:
        lines.append("No matches in scoreboard.")
    else:
        for event in events:
            lines.append(format_match(event, include_events=False, sport=sport, league=league))
            lines.append("")

    return "\n".join(lines)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(all_teams_ticker())
    else:
        cmd = sys.argv[1]

        if cmd == "league":
            league = sys.argv[2] if len(sys.argv) > 2 else "eng.1"
            sport = sys.argv[3] if len(sys.argv) > 3 else "soccer"
            print(league_ticker(league, sport))
        elif cmd == "all":
            print(all_teams_ticker())
        else:
            teams = get_teams()
            team_lower = cmd.lower()
            for team in teams:
                if team_lower in team.get("name", "").lower() or team_lower in team.get("short_name", "").lower():
                    print(team_ticker(team))
                    break
            else:
                print(f"Team '{cmd}' not found in config.")
