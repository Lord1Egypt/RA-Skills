#!/usr/bin/env -S uv run --script
# /// script
# dependencies = []
# ///
"""snooker.py - Snooker API integration for nanobot (api.snooker.org)

Commands:
  setup --api-key KEY          Save your X-Requested-By API key
  rankings [--season N]        World rankings (current season by default)
  player <name>                Search for a player by name
  results [--days N]           Recent match results (default: 1 day)
  live                         Ongoing matches
  upcoming [--date YYYY-MM-DD] Upcoming matches (default: tomorrow)
  tournaments [--date YYYY-MM-DD] Tournaments active on a given date (default: tomorrow)
  schedule [--date YYYY-MM-DD] Matches + tournaments for a date (default: tomorrow)
  h2h <name1> <name2>          Head-to-head record between two players
"""

import json
import os
import sys
import urllib.request
from datetime import date, timedelta
from pathlib import Path

BASE_URL = "https://api.snooker.org/"
WORKSPACE = Path.home() / ".nanobot/workspace"
SNOOKER_DIR = WORKSPACE / "snooker"
CONFIG_FILE = SNOOKER_DIR / "config.json"

TOUR = "main"  # Main tour


def load_config() -> dict:
    env_key = os.environ.get("SNOOKER_API_KEY")
    if env_key:
        return {"apiKey": env_key}
    if not CONFIG_FILE.exists():
        print("Snooker API not configured. Set SNOOKER_API_KEY or run: snooker.py setup --api-key YOUR_KEY")
        print("Get a key by emailing webmaster@snooker.org")
        sys.exit(1)
    return json.loads(CONFIG_FILE.read_text())


def api_get(params: str) -> list | dict:
    config = load_config()
    url = f"{BASE_URL}?{params}"
    req = urllib.request.Request(url, headers={"X-Requested-By": config["apiKey"]})
    print(f"Fetching: {url}")
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def current_season() -> int:
    data = api_get("t=20")
    record = data[0] if isinstance(data, list) else data
    return record.get("CurrentSeason") or record.get("Season")


def all_players(season: int) -> list[dict]:
    return api_get(f"t=10&st=p&s={season}&se=m")


def find_players(name: str) -> list[dict]:
    season = current_season()
    players = all_players(season)
    name_lower = name.lower()
    return [p for p in players if name_lower in p.get("LastName", "").lower()
            or name_lower in p.get("FirstName", "").lower()
            or name_lower in f"{p.get('FirstName','')} {p.get('LastName','')}".lower()]


def format_name(p: dict) -> str:
    return f"{p.get('FirstName', '')} {p.get('LastName', '')}".strip()


def player_map(season: int) -> dict[int, str]:
    """Return {playerID: "First Last"} for the given season."""
    return {p["ID"]: format_name(p) for p in all_players(season) if "ID" in p}


def event_map(season: int) -> dict[int, str]:
    """Return {eventID: "Event Name"} for the given season."""
    events = api_get(f"t=5&s={season}&tr={TOUR}")
    return {e["ID"]: e.get("Name", str(e["ID"])) for e in events if "ID" in e}


def match_time(m: dict) -> str:
    """Extract scheduled time as 'YYYY-MM-DD HH:MM UTC' (or date-only if no time)."""
    raw = m.get("ScheduledDate") or m.get("StartDate") or ""
    if not raw:
        return ""
    # Format: 2026-03-17T02:00:00Z → "2026-03-17 02:00 UTC"
    if "T" in raw:
        date_part, time_part = raw[:10], raw[11:16]
        return f"{date_part} {time_part} UTC"
    return raw[:10]


def format_match(m: dict, players: dict[int, str], events: dict[int, str]) -> str:
    p1 = players.get(m.get("Player1ID", 0), "TBD")
    p2 = players.get(m.get("Player2ID", 0), "TBD")
    s1 = m.get("Score1", "?")
    s2 = m.get("Score2", "?")
    event = events.get(m.get("EventID", 0), f"ID:{m.get('EventID', '?')}")
    round_ = m.get("Round", "")
    return f"  {p1} {s1} – {s2} {p2}  ({event}, Rd {round_})" if round_ else f"  {p1} {s1} – {s2} {p2}  ({event})"


# --- commands ---

def cmd_setup(args: list[str]) -> None:
    SNOOKER_DIR.mkdir(parents=True, exist_ok=True)
    api_key = ""
    i = 0
    while i < len(args):
        if args[i] == "--api-key" and i + 1 < len(args):
            api_key = args[i + 1]; i += 2
        else:
            i += 1
    if not api_key:
        api_key = input("X-Requested-By API key: ").strip()

    CONFIG_FILE.write_text(json.dumps({"apiKey": api_key}, indent=2))
    print(f"Config saved to {CONFIG_FILE}")

    # Quick test
    data = api_get("t=20")
    record = data[0] if isinstance(data, list) else data
    season = record.get("CurrentSeason") or record.get("Season")
    print(f"API working — current season: {season}")


def cmd_rankings(args: list[str]) -> None:
    season = None
    if "--season" in args:
        idx = args.index("--season")
        season = int(args[idx + 1])
    if season is None:
        season = current_season()

    data = api_get(f"rt=MoneyRankings&s={season}")
    if not data:
        print(f"No rankings found for season {season}.")
        return

    print(f"World Rankings — Season {season}\n")
    for entry in data[:20]:
        pos = entry.get("Position", "?")
        name = format_name(entry)
        prize = entry.get("Sum", 0)
        print(f"  {pos:>3}.  {name:<30}  £{prize:,}")


def cmd_player(args: list[str]) -> None:
    if not args:
        print("Usage: snooker.py player <name>")
        sys.exit(1)
    name = " ".join(args)
    matches = find_players(name)

    if not matches:
        print(f"No players found matching '{name}'.")
        return

    for p in matches[:3]:
        pid = p.get("ID")
        profile = api_get(f"p={pid}")
        if isinstance(profile, list):
            profile = profile[0]

        print(f"\n{format_name(profile)}")
        print(f"  Nationality : {profile.get('Nationality', 'N/A')}")
        print(f"  Born        : {profile.get('Born', 'N/A')}")
        print(f"  Turned Pro  : {profile.get('TurnedPro', 'N/A')}")
        print(f"  World Rank  : {profile.get('WorldRanking', 'N/A')}")
        print(f"  Career prize: £{profile.get('CareerEarnings', 0):,}")
        print(f"  Career wins : {profile.get('CareerCupWins', 'N/A')}")


def cmd_results(args: list[str]) -> None:
    days = 1
    if "--days" in args:
        idx = args.index("--days")
        days = int(args[idx + 1])

    data = api_get(f"t=15&ds={days}&tr={TOUR}")
    if not data:
        print(f"No results in the last {days} day(s).")
        return

    season = current_season()
    players = player_map(season)
    events = event_map(season)

    print(f"Results — last {days} day(s):\n")
    for m in data:
        print(format_match(m, players, events))


def cmd_live(_args: list[str]) -> None:
    data = api_get(f"t=7&tr={TOUR}")
    if not data:
        print("No matches in progress.")
        return

    season = current_season()
    players = player_map(season)
    events = event_map(season)

    print("Live matches:\n")
    for m in data:
        print(format_match(m, players, events))


def parse_date_arg(args: list[str]) -> date:
    """Return date from --date YYYY-MM-DD arg, or tomorrow by default."""
    if "--date" in args:
        idx = args.index("--date")
        return date.fromisoformat(args[idx + 1])
    return date.today() + timedelta(days=1)


def match_date(m: dict) -> str:
    """Extract date string (YYYY-MM-DD) from a match record."""
    raw = m.get("ScheduledDate") or m.get("StartDate") or ""
    return raw[:10] if raw else ""


def cmd_upcoming(args: list[str]) -> None:
    # Optional --player filter
    player_name = None
    if "--player" in args:
        idx = args.index("--player")
        player_name = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    target = parse_date_arg(args)
    target_str = target.isoformat()
    data = api_get(f"t=14&tr={TOUR}")
    if not data:
        print("No upcoming matches scheduled.")
        return

    season = current_season()
    players = player_map(season)
    events = event_map(season)

    # Resolve player filter to an ID
    player_id = None
    if player_name:
        found = find_players(player_name)
        if not found:
            print(f"Player not found: {player_name}")
            return
        player_id = found[0]["ID"]
        print(f"Upcoming matches for {format_name(found[0])}:\n")
    else:
        label = "tomorrow" if target == date.today() + timedelta(days=1) else target_str
        print(f"Matches scheduled for {label} ({target_str}):\n")

    for m in data:
        if player_id:
            if m.get("Player1ID") != player_id and m.get("Player2ID") != player_id:
                continue
        elif match_date(m) != target_str:
            continue
        print(f"  {match_time(m)}  {format_match(m, players, events).strip()}")


def cmd_tournaments(args: list[str]) -> None:
    target = parse_date_arg(args)
    target_str = target.isoformat()
    season = current_season()
    data = api_get(f"t=5&s={season}&tr={TOUR}")
    if not data:
        print("No tournament data available.")
        return

    label = "tomorrow" if target == date.today() + timedelta(days=1) else target_str
    active = [
        e for e in data
        if e.get("StartDate", "") <= target_str <= e.get("EndDate", "")
    ]
    if not active:
        print(f"No tournaments active on {label} ({target_str}).")
        return

    print(f"Tournaments active on {label} ({target_str}):\n")
    for e in active:
        name = e.get("Name", "Unknown")
        city = e.get("City", "")
        country = e.get("Country", "")
        start = e.get("StartDate", "")
        end = e.get("EndDate", "")
        venue = ", ".join(filter(None, [city, country]))
        print(f"  {name}")
        print(f"    {start} – {end}  {venue}")


def cmd_schedule(args: list[str]) -> None:
    """Show both tournaments and matches for a given date."""
    target = parse_date_arg(args)
    label = "tomorrow" if target == date.today() + timedelta(days=1) else target.isoformat()
    print(f"Snooker schedule for {label} ({target.isoformat()}):\n")
    print("=== Tournaments ===")
    cmd_tournaments(args)
    print("\n=== Matches ===")
    cmd_upcoming(args)


def cmd_h2h(args: list[str]) -> None:
    if len(args) < 2:
        print("Usage: snooker.py h2h <player1> <player2>")
        sys.exit(1)

    # Split args: support "Ronnie O'Sullivan" "Mark Selby" style
    # Try splitting at "--" marker or just split half if 2+ words
    mid = len(args) // 2
    name1, name2 = " ".join(args[:mid]), " ".join(args[mid:])

    p1_list = find_players(name1)
    p2_list = find_players(name2)

    if not p1_list:
        print(f"Player not found: {name1}"); return
    if not p2_list:
        print(f"Player not found: {name2}"); return

    p1, p2 = p1_list[0], p2_list[0]
    season = current_season()
    data = api_get(f"p1={p1['ID']}&p2={p2['ID']}&s={season}&tr={TOUR}")

    if not data:
        print(f"No head-to-head data found for {format_name(p1)} vs {format_name(p2)}.")
        return

    print(f"Head-to-head: {format_name(p1)} vs {format_name(p2)}\n")
    for m in data:
        s1 = m.get("Score1", "?")
        s2 = m.get("Score2", "?")
        event = m.get("EventName", "")
        round_ = m.get("RoundName", "")
        date = m.get("ScheduledTime", m.get("InitialisedTime", ""))[:10]
        print(f"  {date}  {format_name(p1)} {s1} – {s2} {format_name(p2)}  ({event}, {round_})")


def cmd_player_id(args: list[str]) -> None:
    if not args:
        print("Usage: snooker.py player-id <id>")
        sys.exit(1)
    pid = args[0]
    profile = api_get(f"p={pid}")
    if isinstance(profile, list):
        if not profile:
            print(f"No player found with ID {pid}.")
            return
        profile = profile[0]

    print(f"\n{format_name(profile)}")
    print(f"  ID          : {profile.get('ID', 'N/A')}")
    print(f"  Nationality : {profile.get('Nationality', 'N/A')}")
    print(f"  Born        : {profile.get('Born', 'N/A')}")
    print(f"  First Pro   : {profile.get('FirstSeasonAsPro', 'N/A')}")
    print(f"  Ranking titles: {profile.get('NumRankingTitles', 'N/A')}")
    print(f"  Max breaks  : {profile.get('NumMaximums', 'N/A')}")


def cmd_event(args: list[str]) -> None:
    if not args:
        print("Usage: snooker.py event <id>")
        sys.exit(1)
    eid = args[0]
    data = api_get(f"e={eid}")
    if isinstance(data, list):
        if not data:
            print(f"No event found with ID {eid}.")
            return
        data = data[0]

    name = data.get("Name", "Unknown")
    sponsor = data.get("Sponsor", "")
    full_name = f"{sponsor} {name}".strip() if sponsor else name
    print(f"\n{full_name}")
    print(f"  ID       : {data.get('ID', 'N/A')}")
    print(f"  Type     : {data.get('Type', 'N/A')}")
    print(f"  Dates    : {data.get('StartDate', '')} – {data.get('EndDate', '')}")
    venue = ", ".join(filter(None, [data.get("Venue", ""), data.get("City", ""), data.get("Country", "")]))
    if venue:
        print(f"  Venue    : {venue}")
    print(f"  Season   : {data.get('Season', 'N/A')}")
    print(f"  Entries  : {data.get('NumCompetitors', 'N/A')}")


COMMANDS = {
    "setup": cmd_setup,
    "rankings": cmd_rankings,
    "player": cmd_player,
    "player-id": cmd_player_id,
    "results": cmd_results,
    "live": cmd_live,
    "upcoming": cmd_upcoming,
    "tournaments": cmd_tournaments,
    "schedule": cmd_schedule,
    "event": cmd_event,
    "h2h": cmd_h2h,
}


def usage() -> None:
    print("Usage: snooker.py <command> [options]\n")
    print("Commands:")
    print("  setup --api-key KEY               Save your X-Requested-By API key")
    print("  rankings [--season N]             World rankings (current season by default)")
    print("  player <name>                     Search for a player by name")
    print("  player-id <id>                    Player profile by numeric ID")
    print("  results [--days N]                Recent results (default: 1 day)")
    print("  live                              Ongoing matches")
    print("  upcoming [--date YYYY-MM-DD]      Matches on a date (default: tomorrow)")
    print("  tournaments [--date YYYY-MM-DD]   Tournaments active on a date (default: tomorrow)")
    print("  schedule [--date YYYY-MM-DD]      Matches + tournaments for a date (default: tomorrow)")
    print("  event <id>                        Event details by numeric ID")
    print("  h2h <name1> <name2>               Head-to-head between two players")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd not in COMMANDS:
        usage()
        sys.exit(1 if cmd else 0)
    COMMANDS[cmd](sys.argv[2:])
