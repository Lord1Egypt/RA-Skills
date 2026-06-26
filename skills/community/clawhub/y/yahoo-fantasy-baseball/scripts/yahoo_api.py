"""Yahoo Fantasy Sports API wrapper using yahoo-fantasy-api.

Handles OAuth authentication, config persistence, and league/team construction.
Credentials and config are stored in ~/.openclaw/credentials/yahoo-fantasy/.
"""

import json
import os
import sys
from pathlib import Path

CRED_DIR = Path.home() / ".openclaw" / "credentials" / "yahoo-fantasy"
CONFIG_FILE = CRED_DIR / "yahoo-fantasy.json"
OAUTH_FILE = CRED_DIR / "oauth2.json"
LEGACY_ENV_FILE = CRED_DIR / ".env"

GAME_CODE = "mlb"


def _ensure_cred_dir():
    """Create credential directory if it doesn't exist (0700 on Unix)."""
    CRED_DIR.mkdir(parents=True, exist_ok=True)
    if sys.platform != "win32":
        os.chmod(CRED_DIR, 0o700)


def _set_file_permissions(path):
    """Set restrictive file permissions (0600) on Unix systems.

    On Windows, file permissions are managed by the OS user-profile ACLs.
    """
    if sys.platform != "win32":
        os.chmod(path, 0o600)


def load_config():
    """Load saved config (league_id, team_id, season)."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            return json.load(f)
    return {}


def save_config(config):
    """Save config to disk."""
    _ensure_cred_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
    _set_file_permissions(CONFIG_FILE)


def _migrate_legacy_env():
    """Auto-migrate YFPY .env credentials to oauth2.json format.

    If oauth2.json already exists, does nothing. If .env exists with
    YAHOO_CONSUMER_KEY and YAHOO_CONSUMER_SECRET, creates oauth2.json
    from those values.
    """
    if OAUTH_FILE.exists():
        return
    if not LEGACY_ENV_FILE.exists():
        return

    creds = {}
    with open(LEGACY_ENV_FILE) as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                key, _, value = line.partition("=")
                creds[key.strip()] = value.strip()

    consumer_key = creds.get("YAHOO_CONSUMER_KEY")
    consumer_secret = creds.get("YAHOO_CONSUMER_SECRET")

    if consumer_key and consumer_secret:
        oauth_data = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret,
        }
        # Carry over tokens if present (YFPY stored them in .env too)
        access_token = creds.get("YAHOO_ACCESS_TOKEN")
        refresh_token = creds.get("YAHOO_REFRESH_TOKEN")
        token_type = creds.get("YAHOO_TOKEN_TYPE")
        if access_token and refresh_token:
            oauth_data["access_token"] = access_token
            oauth_data["refresh_token"] = refresh_token
            oauth_data["token_type"] = token_type or "bearer"

        with open(OAUTH_FILE, "w") as f:
            json.dump(oauth_data, f, indent=2)
        _set_file_permissions(OAUTH_FILE)
        print(f"Migrated credentials from .env to {OAUTH_FILE}", file=sys.stderr)


def run_auth():
    """Interactive OAuth setup. Prompts for consumer key/secret, runs OAuth flow."""
    _ensure_cred_dir()

    print("Yahoo Fantasy Baseball — OAuth Setup")
    print("=" * 45)
    print()
    print("You need a Yahoo Developer app to authenticate.")
    print("1. Go to https://developer.yahoo.com/apps/")
    print("2. Create an app (or use an existing one)")
    print("3. Set the Redirect URI to: oob")
    print("4. Copy the Consumer Key and Consumer Secret below")
    print()

    consumer_key = input("Consumer Key: ").strip()
    if not consumer_key:
        print("Error: Consumer Key is required.", file=sys.stderr)
        sys.exit(1)

    consumer_secret = input("Consumer Secret: ").strip()
    if not consumer_secret:
        print("Error: Consumer Secret is required.", file=sys.stderr)
        sys.exit(1)

    # Write credentials to oauth2.json for yahoo_oauth
    oauth_data = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret,
    }
    with open(OAUTH_FILE, "w") as f:
        json.dump(oauth_data, f, indent=2)
    _set_file_permissions(OAUTH_FILE)

    print()
    print("Credentials saved. Starting Yahoo OAuth flow...")
    print("Tip: Set YAHOO_CONSUMER_KEY and YAHOO_CONSUMER_SECRET as environment")
    print("variables to skip interactive setup. Note: credentials are still written")
    print("to oauth2.json for token management (file permissions set to 0600 on Unix).")
    print("A browser window will open for authorization.")
    print()

    try:
        from yahoo_oauth import OAuth2
        sc = OAuth2(None, None, from_file=str(OAUTH_FILE))
        if not sc.token_is_valid():
            print("Error: OAuth token not valid after auth flow.", file=sys.stderr)
            sys.exit(1)
        print("Authentication successful!")
    except Exception as e:
        print(f"Authentication failed: {e}", file=sys.stderr)
        print("Check your Consumer Key/Secret and try again.", file=sys.stderr)
        sys.exit(1)


def _get_oauth():
    """Return an authenticated OAuth2 session.

    Checks for YAHOO_CONSUMER_KEY / YAHOO_CONSUMER_SECRET env vars first,
    then falls back to oauth2.json file. Attempts auto-migration from
    legacy .env if oauth2.json doesn't exist.
    """
    consumer_key = os.environ.get("YAHOO_CONSUMER_KEY")
    consumer_secret = os.environ.get("YAHOO_CONSUMER_SECRET")

    if consumer_key and consumer_secret:
        # Env vars provided — write/update oauth2.json so yahoo_oauth can
        # manage token refresh. Only update if consumer key/secret changed.
        _ensure_cred_dir()
        oauth_data = {}
        if OAUTH_FILE.exists():
            with open(OAUTH_FILE) as f:
                oauth_data = json.load(f)
        if (oauth_data.get("consumer_key") != consumer_key or
                oauth_data.get("consumer_secret") != consumer_secret):
            oauth_data["consumer_key"] = consumer_key
            oauth_data["consumer_secret"] = consumer_secret
            with open(OAUTH_FILE, "w") as f:
                json.dump(oauth_data, f, indent=2)
            _set_file_permissions(OAUTH_FILE)
    else:
        _migrate_legacy_env()

    if not OAUTH_FILE.exists():
        print("Error: Not authenticated. Run 'auth' first or set", file=sys.stderr)
        print("YAHOO_CONSUMER_KEY and YAHOO_CONSUMER_SECRET env vars.", file=sys.stderr)
        sys.exit(1)

    try:
        from yahoo_oauth import OAuth2
        sc = OAuth2(None, None, from_file=str(OAUTH_FILE))
    except Exception as e:
        print(f"Error loading OAuth credentials: {e}", file=sys.stderr)
        print("Try running 'auth' again.", file=sys.stderr)
        sys.exit(1)

    if not sc.token_is_valid():
        try:
            sc.refresh_access_token()
        except Exception as e:
            print(
                "Error: Yahoo refresh token is no longer valid. "
                f"Run 'auth' to re-authenticate. ({e})",
                file=sys.stderr,
            )
            sys.exit(1)
    return sc


def _call_with_refresh(sc, fn, *args, **kwargs):
    """Call a Yahoo API function; on invalid-cookie errors, refresh once and retry."""
    try:
        return fn(*args, **kwargs)
    except RuntimeError as e:
        msg = str(e)
        if (
            "Invalid cookie" in msg
            or "token_expired" in msg
            or "please log in again" in msg
        ):
            try:
                sc.refresh_access_token()
            except Exception as refresh_err:
                print(
                    "Error: Yahoo refresh token is no longer valid. "
                    f"Run 'auth' to re-authenticate. ({refresh_err})",
                    file=sys.stderr,
                )
                sys.exit(1)
            return fn(*args, **kwargs)
        raise


def get_game(season=None):
    """Return an authenticated yfa.Game instance.

    Args:
        season: Season year (int). If provided, used to filter league_ids.

    Returns:
        (yfa.Game, OAuth2) tuple.
    """
    sc = _get_oauth()
    import yahoo_fantasy_api as yfa
    gm = yfa.Game(sc, GAME_CODE)
    return gm, sc


def get_league(league_id, season=None):
    """Return a yfa.League instance for the given league.

    Args:
        league_id: Yahoo league ID (numeric string, e.g. "12345").
        season: Season year (int). If None, uses current season.

    Returns:
        yfa.League instance.
    """
    gm, sc = get_game(season)

    # Build the full league key: {game_key}.l.{league_id}
    if season is not None:
        try:
            league_ids = _call_with_refresh(sc, gm.league_ids, seasons=[str(season)])
            for lid in league_ids:
                if lid.endswith(f".l.{league_id}"):
                    return gm.to_league(lid)
        except Exception:
            # Yahoo may return 403 "Forbidden access" if the user has no
            # leagues matching the season filter; fall through to manual key.
            pass
        # If not found in user's leagues, construct the key manually
        game_id = _call_with_refresh(sc, gm.game_id)
        league_key = f"{game_id}.l.{league_id}"
        return gm.to_league(league_key)
    else:
        # Current season — try user's leagues first
        try:
            league_ids = _call_with_refresh(sc, gm.league_ids)
            for lid in league_ids:
                if lid.endswith(f".l.{league_id}"):
                    return gm.to_league(lid)
        except Exception:
            pass
        # Construct key with current game_id
        game_id = _call_with_refresh(sc, gm.game_id)
        league_key = f"{game_id}.l.{league_id}"
        return gm.to_league(league_key)


def _parse_players_page(raw):
    """Parse a raw Yahoo API players response with percent_owned and ownership.

    Handles the ;out=percent_owned,ownership response format which the
    yahoo-fantasy-api library doesn't support natively.

    Returns:
        (num_on_page, list[dict]): Count and parsed player dicts.
    """
    try:
        players_data = raw['fantasy_content']['league'][1]['players']
    except (KeyError, IndexError):
        return (0, [])

    if not players_data or players_data.get('count', 0) == 0:
        return (0, [])

    count = players_data.get('count', 0)
    result = []

    for i in range(count):
        key = str(i)
        if key not in players_data:
            break
        parts = players_data[key]['player']
        # parts[0] = list of player info dicts, parts[1+] = subresources
        info_list = parts[0]

        plyr = {}
        for item in info_list:
            if not isinstance(item, dict):
                continue
            for k, v in item.items():
                if k == 'name':
                    plyr['name'] = v.get('full', '') if isinstance(v, dict) else str(v)
                elif k == 'player_id':
                    plyr['player_id'] = int(v)
                elif k == 'position_type':
                    plyr['position_type'] = v
                elif k == 'display_position':
                    plyr['display_position'] = v
                elif k == 'eligible_positions':
                    plyr['eligible_positions'] = [e['position'] for e in v if isinstance(e, dict)]
                elif k == 'editorial_team_abbr':
                    plyr['editorial_team_abbr'] = v
                elif k == 'status':
                    plyr['status'] = v

        if 'status' not in plyr:
            plyr['status'] = ''

        # Parse subresource parts (percent_owned, ownership)
        for part in parts[1:]:
            if not isinstance(part, dict):
                continue
            if 'percent_owned' in part:
                pct_data = part['percent_owned']
                for item in pct_data:
                    if isinstance(item, dict) and 'value' in item:
                        plyr['percent_owned'] = int(item['value'])
            if 'ownership' in part:
                own = part['ownership']
                plyr['ownership_type'] = own.get('ownership_type', '')
                plyr['owner_team_name'] = own.get('owner_team_name', '')

        # Skip players marked as not available
        if plyr.get('status') != 'NA':
            result.append(plyr)

    return (count, result)


# Common MLB stat abbreviations → Yahoo stat IDs for sorting
STAT_SORT_MAP = {
    # Batting
    "R": "7", "H": "8", "1B": "9", "2B": "10", "3B": "11",
    "HR": "12", "RBI": "13", "SB": "16", "BB": "18", "K": "21",
    "AVG": "3", "OBP": "4", "SLG": "5", "OPS": "55", "AB": "6",
    "TB": "23", "XBH": "61", "PA": "65",
    # Pitching
    "W": "28", "L": "29", "SV": "32", "HLD": "48", "SV+H": "89",
    "ERA": "26", "WHIP": "27", "IP": "50", "QS": "83",
    "K9": "57", "BB9": "78", "BSV": "84",
}


def _resolve_sort(sort):
    """Resolve a sort value — accept OR/AR/PTS/NAME directly, or map stat abbrevs to IDs."""
    if sort is None:
        return None
    upper = sort.upper()
    if upper in ("OR", "AR", "PTS", "NAME"):
        return upper
    # Try stat abbreviation
    if upper in STAT_SORT_MAP:
        return STAT_SORT_MAP[upper]
    # Already a numeric stat ID
    if sort.isdigit():
        return sort
    return sort


def fetch_players_sorted(league, status="FA", position=None, sort=None,
                         sort_type=None, sort_season=None):
    """Fetch players with sort and ownership, bypassing the library's free_agents().

    The yahoo-fantasy-api library doesn't expose Yahoo's sort params or ownership
    data, so we build the URI ourselves with custom parsing.

    Args:
        league: yfa.League instance.
        status: Player status filter — "FA", "W", "T", "A" (available=FA+W),
                "ALL" (every player: taken + available).
        position: Position filter — "B", "P", "C", "1B", "SS", "OF", "SP", etc.
        sort: Sort field — "OR" (overall rank), "AR" (actual rank), "PTS" (points),
              "NAME", or a stat abbreviation (HR, ERA, SB, etc.).
        sort_type: Sort period — "season", "lastweek", "lastmonth", "date".
        sort_season: Sort season year (e.g., 2025).

    Returns:
        list[dict]: Player dicts with name, player_id, position_type,
                    percent_owned, ownership_type, owner_team_name, etc.
    """
    sort = _resolve_sort(sort)

    # Yahoo requires sort_type when sorting by a stat ID (numeric).
    # Default to "season" so --sort IP (etc.) works without --sort-type.
    if sort and sort not in ("OR", "AR", "PTS", "NAME") and not sort_type:
        sort_type = "season"

    # "ALL" is synthetic — Yahoo has no single status for all players.
    # Fetch taken + available separately and merge by sort order.
    if status.upper() == "ALL":
        taken = _fetch_players_page_loop(
            league, "T", position, sort, sort_type, sort_season)
        available = _fetch_players_page_loop(
            league, "A", position, sort, sort_type, sort_season)
        # Deduplicate — a player can appear in both lists
        seen = set()
        combined = []
        for p in taken + available:
            pid = p.get('player_id')
            if pid and pid not in seen:
                seen.add(pid)
                combined.append(p)
        # Both lists are sorted by Yahoo. After dedup, taken players
        # appear first followed by available. Since we can't compare
        # rank across lists without stat values in the response, keep
        # the combined order as-is — Yahoo's sort_type=season with the
        # stat sort will at least give correct order within each group.
        # The caller's --count slicing still applies.
        return combined

    return _fetch_players_page_loop(
        league, status, position, sort, sort_type, sort_season)


def _fetch_players_page_loop(league, status, position, sort, sort_type,
                             sort_season):
    """Paginated fetch of players from Yahoo API with custom URI."""
    PLAYERS_PER_PAGE = 25
    all_players = []
    start = 0

    while True:
        uri = f"league/{league.league_id}/players;start={start};count={PLAYERS_PER_PAGE};status={status}"
        if position:
            uri += f";position={position}"
        if sort:
            uri += f";sort={sort}"
        if sort_type:
            uri += f";sort_type={sort_type}"
        if sort_season:
            uri += f";sort_season={sort_season}"
        uri += ";out=percent_owned,ownership"

        raw = league.yhandler.get(uri)
        num_on_page, players = _parse_players_page(raw)
        if not players:
            break
        all_players.extend(players)
        if num_on_page < PLAYERS_PER_PAGE:
            break
        start += int(num_on_page)

    return all_players


def get_team(league, team_key):
    """Return a yfa.Team instance.

    Args:
        league: yfa.League instance.
        team_key: Full team key (e.g. "422.l.12345.t.3").

    Returns:
        yfa.Team instance.
    """
    return league.to_team(team_key)


def get_roster(team, day=None, week=None):
    """Fetch roster with editorial_team_abbr included.

    The yahoo-fantasy-api library's tm.roster() doesn't extract
    editorial_team_abbr from the raw response. This wrapper does.

    Args:
        team: yfa.Team instance.
        day: Optional date object.
        week: Optional week number.

    Returns:
        List of player dicts with player_id, name, position_type,
        eligible_positions, selected_position, status, editorial_team_abbr.
    """
    import objectpath

    raw = team.yhandler.get_roster_raw(team.team_key, week=week, day=day)
    t = objectpath.Tree(raw)

    roster_obj = t.execute('$.fantasy_content.team[1].roster')
    if not roster_obj:
        return []

    players_dict = None
    for key, value in roster_obj.items():
        if isinstance(value, dict) and 'players' in value:
            players_dict = value['players']
            break

    if not players_dict:
        return []

    roster = []
    player_keys = [k for k in players_dict.keys() if k != 'count']
    player_keys.sort(key=lambda x: int(x) if x.isdigit() else float('inf'))
    for key in player_keys:
        player_entry = players_dict[key]
        if not isinstance(player_entry, dict) or 'player' not in player_entry:
            continue

        player = player_entry['player']
        if not isinstance(player, list) or len(player) < 2:
            continue

        player_data = player[0]
        selected_position_data = player[1]

        plyr = {}
        for item in player_data:
            if not isinstance(item, dict):
                continue
            if 'player_id' in item:
                plyr['player_id'] = int(item['player_id'])
            elif 'name' in item and 'full' in item['name']:
                plyr['name'] = item['name']['full']
            elif 'editorial_team_abbr' in item:
                plyr['editorial_team_abbr'] = item['editorial_team_abbr']
            elif 'position_type' in item:
                if 'player_id' not in plyr:
                    continue
                if 'position_type' not in plyr:
                    plyr['position_type'] = item['position_type']
            elif 'eligible_positions' in item:
                plyr['eligible_positions'] = [
                    p['position'] for p in item['eligible_positions']
                ]

        # Get status (skip boolean keeper status).
        plyr['status'] = ""
        for item in player_data:
            if isinstance(item, dict) and 'status' in item:
                status_value = item['status']
                if not isinstance(status_value, bool):
                    plyr['status'] = status_value
                    break

        # Extract selected_position.
        if 'selected_position' in selected_position_data:
            plyr['selected_position'] = selected_position_data['selected_position'][1]['position']

        if 'player_id' in plyr and 'name' in plyr:
            roster.append(plyr)

    return roster


def resolve_league_id(args_league, config):
    """Resolve league ID from args or config, exit with error if missing."""
    league_id = args_league or config.get("league_id")
    if not league_id:
        print("Error: No league ID. Use --league or run 'config --league <ID>'.", file=sys.stderr)
        sys.exit(1)
    return str(league_id)


def resolve_team_key(league, args_team, config):
    """Resolve team key from args, config, or auto-detect from league.

    Args:
        league: yfa.League instance.
        args_team: Team ID from command-line args (numeric, e.g. "3").
        config: Saved config dict.

    Returns:
        str: The full team key (e.g. "422.l.12345.t.3").
    """
    teams = league.teams()

    if args_team:
        # Find team by numeric ID
        for tkey, tdata in teams.items():
            if str(tdata.get("team_id")) == str(args_team):
                return tkey
        # Try constructing it
        # team_key format: {league_key}.t.{team_id}
        for tkey in teams:
            if tkey.endswith(f".t.{args_team}"):
                return tkey
        print(f"Error: Team ID {args_team} not found in league.", file=sys.stderr)
        sys.exit(1)

    if config.get("team_id"):
        team_id = str(config["team_id"])
        for tkey, tdata in teams.items():
            if str(tdata.get("team_id")) == team_id:
                return tkey
            if tkey.endswith(f".t.{team_id}"):
                return tkey

    # Auto-detect: use league.team_key() which returns the current user's team
    try:
        return league.team_key()
    except Exception:
        pass

    # Fallback: if only one team, use it
    if len(teams) == 1:
        return next(iter(teams))

    print("Error: Could not auto-detect your team. Use --team <ID>.", file=sys.stderr)
    print("Run 'teams' to see team IDs.", file=sys.stderr)
    sys.exit(1)
