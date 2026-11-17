"""MLB Stats API client for schedule and probable pitcher data.

Standard library only — no external dependencies.
Modeled on skills/baseball/scripts/mlb_api.py.
"""

import json
import sys
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

SCHEDULE_URL = "https://statsapi.mlb.com/api/v1/schedule/games"
TIMEOUT_SECONDS = 15

# All 30 MLB teams: abbreviation -> {id, name}
MLB_TEAMS = {
    "ARI": {"id": 109, "name": "Arizona Diamondbacks"},
    "ATL": {"id": 144, "name": "Atlanta Braves"},
    "BAL": {"id": 110, "name": "Baltimore Orioles"},
    "BOS": {"id": 111, "name": "Boston Red Sox"},
    "CHC": {"id": 112, "name": "Chicago Cubs"},
    "CWS": {"id": 145, "name": "Chicago White Sox"},
    "CIN": {"id": 113, "name": "Cincinnati Reds"},
    "CLE": {"id": 114, "name": "Cleveland Guardians"},
    "COL": {"id": 115, "name": "Colorado Rockies"},
    "DET": {"id": 116, "name": "Detroit Tigers"},
    "HOU": {"id": 117, "name": "Houston Astros"},
    "KC":  {"id": 118, "name": "Kansas City Royals"},
    "LAA": {"id": 108, "name": "Los Angeles Angels"},
    "LAD": {"id": 119, "name": "Los Angeles Dodgers"},
    "MIA": {"id": 146, "name": "Miami Marlins"},
    "MIL": {"id": 158, "name": "Milwaukee Brewers"},
    "MIN": {"id": 142, "name": "Minnesota Twins"},
    "NYM": {"id": 121, "name": "New York Mets"},
    "NYY": {"id": 147, "name": "New York Yankees"},
    "OAK": {"id": 133, "name": "Oakland Athletics"},
    "PHI": {"id": 143, "name": "Philadelphia Phillies"},
    "PIT": {"id": 134, "name": "Pittsburgh Pirates"},
    "SD":  {"id": 135, "name": "San Diego Padres"},
    "SF":  {"id": 137, "name": "San Francisco Giants"},
    "SEA": {"id": 136, "name": "Seattle Mariners"},
    "STL": {"id": 138, "name": "St. Louis Cardinals"},
    "TB":  {"id": 139, "name": "Tampa Bay Rays"},
    "TEX": {"id": 140, "name": "Texas Rangers"},
    "TOR": {"id": 141, "name": "Toronto Blue Jays"},
    "WSH": {"id": 120, "name": "Washington Nationals"},
}

# Reverse lookup: team ID -> abbreviation
_TEAM_ID_TO_ABBR = {info["id"]: abbr for abbr, info in MLB_TEAMS.items()}

# Yahoo Fantasy uses slightly different abbreviations for some teams
YAHOO_TO_MLB_ABBR = {
    "CWS": "CWS",
    "CHW": "CWS",
    "KC":  "KC",
    "LAA": "LAA",
    "LAD": "LAD",
    "SD":  "SD",
    "SF":  "SF",
    "STL": "STL",
    "TB":  "TB",
    "WSH": "WSH",
    "Was": "WSH",
    "Wsh": "WSH",
}


def normalize_team_abbr(yahoo_abbr):
    """Convert a Yahoo team abbreviation to MLB Stats API abbreviation."""
    if not yahoo_abbr:
        return ""
    upper = yahoo_abbr.upper().strip()
    # Check explicit mapping first
    for yahoo_key, mlb_key in YAHOO_TO_MLB_ABBR.items():
        if yahoo_key.upper() == upper:
            return mlb_key
    # Direct match
    if upper in MLB_TEAMS:
        return upper
    return upper


def _fetch_json(url):
    """Fetch JSON from a URL using urllib. Returns parsed dict or None on error."""
    try:
        with urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        print(f"MLB API error: HTTP {e.code} fetching {url}", file=sys.stderr)
    except URLError as e:
        print(f"MLB API error: Network error: {e.reason}", file=sys.stderr)
    except TimeoutError:
        print(f"MLB API error: Request timed out", file=sys.stderr)
    except json.JSONDecodeError:
        print(f"MLB API error: Invalid JSON response", file=sys.stderr)
    return None


def teams_playing_today(date_str=None):
    """Return a set of MLB team abbreviations with games scheduled today.

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        set of uppercase team abbreviations (e.g. {"NYY", "BOS", ...}).
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    # MLB API uses MM/DD/YYYY format
    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}"
    data = _fetch_json(url)
    if data is None:
        return set()

    playing = set()
    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            # Skip cancelled/postponed games
            if status in ("Cancelled", "Postponed"):
                continue
            away = game.get("teams", {}).get("away", {}).get("team", {})
            home = game.get("teams", {}).get("home", {}).get("team", {})
            away_id = away.get("id")
            home_id = home.get("id")
            if away_id and away_id in _TEAM_ID_TO_ABBR:
                playing.add(_TEAM_ID_TO_ABBR[away_id])
            if home_id and home_id in _TEAM_ID_TO_ABBR:
                playing.add(_TEAM_ID_TO_ABBR[home_id])

    return playing


# Game states that mean the game has NOT started yet
_NOT_STARTED_STATES = {"Scheduled", "Pre-Game", "Warmup", "Delayed Start", "Delayed"}


def teams_with_unlocked_games(date_str=None):
    """Return teams split by whether their game has started (locked by Yahoo).

    Yahoo Fantasy locks roster slots at first pitch. This function checks
    each game's detailedState to determine if a team can still be moved.

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        Tuple of (unlocked: set[str], locked: set[str]) team abbreviations.
        - unlocked: teams whose game hasn't started yet (can be moved)
        - locked: teams whose game is in progress or finished (cannot be moved)
        For doubleheaders, a team is unlocked if ANY game hasn't started.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}"
    data = _fetch_json(url)
    if data is None:
        return set(), set()

    unlocked = set()
    locked = set()

    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            if status in ("Cancelled", "Postponed"):
                continue
            away = game.get("teams", {}).get("away", {}).get("team", {})
            home = game.get("teams", {}).get("home", {}).get("team", {})
            away_id = away.get("id")
            home_id = home.get("id")

            team_abbrs = []
            if away_id and away_id in _TEAM_ID_TO_ABBR:
                team_abbrs.append(_TEAM_ID_TO_ABBR[away_id])
            if home_id and home_id in _TEAM_ID_TO_ABBR:
                team_abbrs.append(_TEAM_ID_TO_ABBR[home_id])

            if status in _NOT_STARTED_STATES:
                for abbr in team_abbrs:
                    unlocked.add(abbr)
            else:
                for abbr in team_abbrs:
                    # Only mark locked if not already unlocked (doubleheader)
                    if abbr not in unlocked:
                        locked.add(abbr)

    # Clean up: if a team is in both (doubleheader), unlocked wins
    locked -= unlocked

    return unlocked, locked


def probable_pitchers_today(date_str=None):
    """Return probable pitchers for today's games.

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        dict mapping team abbreviation -> pitcher full name.
        e.g. {"PHI": "Zack Wheeler", "NYY": "Gerrit Cole"}
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}&hydrate=probablePitcher"
    data = _fetch_json(url)
    if data is None:
        return {}

    pitchers = {}
    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            if status in ("Cancelled", "Postponed"):
                continue
            for side in ("away", "home"):
                team_data = game.get("teams", {}).get(side, {})
                team_info = team_data.get("team", {})
                team_id = team_info.get("id")
                pitcher = team_data.get("probablePitcher", {})
                pitcher_name = pitcher.get("fullName", "")
                if team_id and pitcher_name and team_id in _TEAM_ID_TO_ABBR:
                    pitchers[_TEAM_ID_TO_ABBR[team_id]] = pitcher_name

    return pitchers


def game_opponents_today(date_str=None):
    """Return a mapping of team abbreviation -> opponent abbreviation for today.

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        dict mapping team abbreviation -> opponent abbreviation.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}"
    data = _fetch_json(url)
    if data is None:
        return {}

    opponents = {}
    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            if status in ("Cancelled", "Postponed"):
                continue
            away = game.get("teams", {}).get("away", {}).get("team", {})
            home = game.get("teams", {}).get("home", {}).get("team", {})
            away_id = away.get("id")
            home_id = home.get("id")
            if away_id in _TEAM_ID_TO_ABBR and home_id in _TEAM_ID_TO_ABBR:
                away_abbr = _TEAM_ID_TO_ABBR[away_id]
                home_abbr = _TEAM_ID_TO_ABBR[home_id]
                opponents[away_abbr] = home_abbr
                opponents[home_abbr] = away_abbr

    return opponents


def game_matchups_today(date_str=None):
    """Return a mapping of team abbreviation -> matchup string (e.g. 'at SF', 'vs NYY').

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        dict mapping team abbreviation -> matchup string with home/away prefix.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}"
    data = _fetch_json(url)
    if data is None:
        return {}

    matchups = {}
    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            if status in ("Cancelled", "Postponed"):
                continue
            away = game.get("teams", {}).get("away", {}).get("team", {})
            home = game.get("teams", {}).get("home", {}).get("team", {})
            away_id = away.get("id")
            home_id = home.get("id")
            if away_id in _TEAM_ID_TO_ABBR and home_id in _TEAM_ID_TO_ABBR:
                away_abbr = _TEAM_ID_TO_ABBR[away_id]
                home_abbr = _TEAM_ID_TO_ABBR[home_id]
                matchups[away_abbr] = f"at {home_abbr}"
                matchups[home_abbr] = f"vs {away_abbr}"

    return matchups


def _parse_game_time(iso_string):
    """Parse ISO 8601 UTC datetime to local datetime."""
    if not iso_string:
        return None
    try:
        dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        return dt.astimezone()  # converts to system local timezone
    except (ValueError, TypeError):
        return None


def _format_time(dt):
    """Format datetime as short local time like '7:10 PM'."""
    if dt is None:
        return "TBD"
    return dt.strftime("%I:%M %p").lstrip("0")


def game_times_today(date_str=None):
    """Return game start times (local) for today's games.

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        Tuple of (times_dict, first_pitch_str):
        - times_dict: dict mapping team abbreviation -> formatted local time string.
        - first_pitch_str: formatted time of the earliest game, or None.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}"
    data = _fetch_json(url)
    if data is None:
        return {}, None

    times = {}
    earliest_dt = None

    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            if status in ("Cancelled", "Postponed"):
                continue
            away = game.get("teams", {}).get("away", {}).get("team", {})
            home = game.get("teams", {}).get("home", {}).get("team", {})
            away_id = away.get("id")
            home_id = home.get("id")
            game_dt = _parse_game_time(game.get("gameDate"))
            time_str = _format_time(game_dt)

            if away_id in _TEAM_ID_TO_ABBR:
                times[_TEAM_ID_TO_ABBR[away_id]] = time_str
            if home_id in _TEAM_ID_TO_ABBR:
                times[_TEAM_ID_TO_ABBR[home_id]] = time_str

            if game_dt and (earliest_dt is None or game_dt < earliest_dt):
                earliest_dt = game_dt

    first_pitch = _format_time(earliest_dt) if earliest_dt else None
    return times, first_pitch


def confirmed_lineups_today(date_str=None):
    """Return confirmed batting lineups for today's games.

    Args:
        date_str: Date in YYYY-MM-DD format. Defaults to today.

    Returns:
        dict mapping team abbreviation -> list of player full names in the lineup.
        Teams whose lineups are not yet posted will not appear in the dict.
    """
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")

    parts = date_str.split("-")
    api_date = f"{parts[1]}/{parts[2]}/{parts[0]}"

    url = f"{SCHEDULE_URL}?sportId=1&date={api_date}&hydrate=lineups"
    data = _fetch_json(url)
    if data is None:
        return {}

    lineups = {}
    for date_entry in data.get("dates", []):
        for game in date_entry.get("games", []):
            status = game.get("status", {}).get("detailedState", "")
            if status in ("Cancelled", "Postponed"):
                continue
            game_lineups = game.get("lineups", {})
            for side in ("away", "home"):
                team_data = game.get("teams", {}).get(side, {})
                team_id = team_data.get("team", {}).get("id")
                if not team_id or team_id not in _TEAM_ID_TO_ABBR:
                    continue
                players = game_lineups.get(f"{side}Players", [])
                if not players:
                    continue
                names = [p.get("fullName", "") for p in players if p.get("fullName")]
                if names:
                    lineups[_TEAM_ID_TO_ABBR[team_id]] = names

    return lineups
