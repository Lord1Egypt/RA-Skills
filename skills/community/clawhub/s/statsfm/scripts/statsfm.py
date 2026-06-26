#!/usr/bin/env python3
"""
stats.fm CLI - Query stats.fm API for Spotify listening statistics
Usage: statsfm.py <command> [args...]
"""

import sys
import io
import json
import argparse
import os
import time

# Ensure UTF-8 output
if sys.stdout.encoding != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
if sys.stderr.encoding != "utf-8":
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
from typing import Optional, Dict, Any
from urllib.parse import quote
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from datetime import datetime, timedelta


def get_local_timezone() -> str:
    """Detect the system's IANA timezone name (e.g. Europe/Amsterdam).
    Falls back to UTC if detection fails."""
    tz = os.environ.get("TZ", "").strip()
    if tz:
        return tz
    try:
        with open("/etc/timezone") as f:
            tz = f.read().strip()
            if tz:
                return tz
    except OSError:
        pass
    try:
        link = os.path.realpath("/etc/localtime")
        marker = "/zoneinfo/"
        idx = link.find(marker)
        if idx != -1:
            return link[idx + len(marker):]
    except OSError:
        pass
    return "UTC"


BASE_URL = "https://api.stats.fm/api/v1"
DEFAULT_USER = os.environ.get("STATSFM_USER", "")
DEFAULT_RANGE = "4w"
DEFAULT_LIMIT = 15


class StatsAPI:
    """stats.fm API client"""

    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def request(self, endpoint: str) -> Dict[str, Any]:
        """Make a GET request to the API"""
        url = f"{self.base_url}{endpoint}"

        try:
            req = Request(url)
            req.add_header('User-Agent', 'statsfm-cli/1.0')
            req.add_header('Accept', 'application/json')

            with urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
                return data
        except HTTPError as e:
            error_body = e.read().decode() if e.fp else ""
            try:
                error_data = json.loads(error_body)
                message = error_data.get("message", str(e))
            except json.JSONDecodeError:
                message = str(e)

            print(f"API Error ({e.code}): {message}", file=sys.stderr)
            if e.code == 404 and "private" in message.lower():
                print("Please check your stats.fm privacy settings (Settings > Privacy)", file=sys.stderr)
            sys.exit(1)
        except URLError as e:
            print(f"Connection Error: {e.reason}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)


def format_duration(ms: int) -> str:
    """Format milliseconds as MM:SS"""
    seconds = ms // 1000
    return f"{seconds // 60}:{seconds % 60:02d}"


def format_time(ms: int) -> str:
    """Format milliseconds as minutes or hours"""
    mins = ms // 60000
    if mins >= 60:
        hours = mins // 60
        remaining_mins = mins % 60
        return f"{hours:,}h {remaining_mins}m"
    return f"{mins:,} min"


def get_user_or_exit(args) -> str:
    """Get user from args or env, exit if not found"""
    user = args.user or DEFAULT_USER
    if not user:
        print("Error: No user specified. Set STATSFM_USER or pass --user", file=sys.stderr)
        sys.exit(1)
    return quote(user, safe='')


def get_per_day_stats_with_totals(api: StatsAPI, endpoint: str) -> tuple[Dict[str, Any], int, int]:
    """Get per-day stats and calculate totals"""
    data = api.request(endpoint)
    days = data.get("items", {}).get("days", {})

    total_count = sum(day.get('count', 0) for day in days.values())
    total_ms = sum(day.get('durationMs', 0) for day in days.values())

    return days, total_count, total_ms


def show_monthly_breakdown(days_data: Dict[str, Any], limit: Optional[int] = None):
    """Display monthly breakdown from per-day stats"""
    from collections import defaultdict

    # Group by month
    monthly = defaultdict(lambda: {'count': 0, 'durationMs': 0})

    for date_str, stats in days_data.items():
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            month_key = dt.strftime("%Y-%m")
            monthly[month_key]['count'] += stats['count']
            monthly[month_key]['durationMs'] += stats['durationMs']
        except:
            continue

    # Sort by month and get only months with plays
    months_with_plays = [(month, stats) for month, stats in sorted(monthly.items()) if stats['count'] > 0]

    # Apply limit (most recent months)
    if limit and limit > 0:
        months_with_plays = months_with_plays[-limit:]

    # Display
    print("Monthly breakdown:")
    for month, stats in months_with_plays:
        print(f"  {month}: {stats['count']:>4} plays  ({format_time(stats['durationMs'])})")


def show_daily_breakdown(days_data: Dict[str, Any], limit: Optional[int] = None):
    """Display daily breakdown from per-day stats"""
    daily = []
    for date_str, stats in days_data.items():
        if stats.get('count', 0) > 0:
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                daily.append((dt, stats))
            except:
                continue

    daily.sort(key=lambda x: x[0])
    if limit and limit > 0:
        daily = daily[-limit:]

    print("Daily breakdown:")
    for dt, stats in daily:
        day_name = dt.strftime("%a")
        date_label = dt.strftime("%Y-%m-%d")
        print(f"  {date_label} ({day_name}): {stats['count']:>4} plays  ({format_time(stats['durationMs'])})")


def show_weekly_breakdown(days_data: Dict[str, Any], limit: Optional[int] = None):
    """Display weekly breakdown from per-day stats"""
    from collections import defaultdict
    import datetime as dt_module

    weekly = defaultdict(lambda: {'count': 0, 'durationMs': 0})

    for date_str, stats in days_data.items():
        if stats.get('count', 0) > 0:
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                week_key = dt.strftime("%G-W%V")
                week_start = dt - dt_module.timedelta(days=dt.weekday())
                weekly[week_key]['count'] += stats['count']
                weekly[week_key]['durationMs'] += stats['durationMs']
                weekly[week_key]['start'] = min(weekly[week_key].get('start', week_start), week_start)
            except:
                continue

    weeks_with_plays = [(wk, stats) for wk, stats in sorted(weekly.items()) if stats['count'] > 0]
    if limit and limit > 0:
        weeks_with_plays = weeks_with_plays[-limit:]

    print("Weekly breakdown:")
    for wk, stats in weeks_with_plays:
        start = stats.get('start')
        start_str = start.strftime("%b %d") if start else ""
        print(f"  {wk} ({start_str}): {stats['count']:>4} plays  ({format_time(stats['durationMs'])})")


def show_yearly_breakdown(days_data: Dict[str, Any], limit: Optional[int] = None):
    """Display yearly breakdown from per-day stats"""
    from collections import defaultdict

    yearly = defaultdict(lambda: {'count': 0, 'durationMs': 0})

    for date_str, stats in days_data.items():
        if stats.get('count', 0) > 0:
            try:
                dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                year_key = dt.strftime("%Y")
                yearly[year_key]['count'] += stats['count']
                yearly[year_key]['durationMs'] += stats['durationMs']
            except:
                continue

    years_with_plays = [(yr, stats) for yr, stats in sorted(yearly.items()) if stats['count'] > 0]
    if limit and limit > 0:
        years_with_plays = years_with_plays[-limit:]

    print("Yearly breakdown:")
    for yr, stats in years_with_plays:
        print(f"  {yr}: {stats['count']:>6} plays ({format_time(stats['durationMs'])})")


def parse_date(date_str: str) -> int:
    """Parse date string to Unix timestamp in milliseconds

    Supports formats:
    - YYYY (e.g., "2025" -> Jan 1, 2025 00:00:00)
    - YYYY-MM (e.g., "2025-06" -> Jun 1, 2025 00:00:00)
    - YYYY-MM-DD (e.g., "2025-06-15" -> Jun 15, 2025 00:00:00)
    """
    parts = date_str.split("-")
    if len(parts) == 1:  # YYYY
        dt = datetime(int(parts[0]), 1, 1)
    elif len(parts) == 2:  # YYYY-MM
        dt = datetime(int(parts[0]), int(parts[1]), 1)
    elif len(parts) == 3:  # YYYY-MM-DD
        dt = datetime(int(parts[0]), int(parts[1]), int(parts[2]))
    else:
        raise ValueError(f"Invalid date format: {date_str}")

    return int(dt.timestamp() * 1000)


def get_album_name(track: dict) -> str:
    """Extract album name from track object"""
    albums = track.get("albums", [])
    if albums:
        return albums[0]["name"]
    return "?"


def dedupe(items: list) -> list:
    """Deduplicate a list of API items by their 'id' field, preserving order."""
    seen = set()
    result = []
    for item in items:
        item_id = item.get("id")
        if item_id not in seen:
            seen.add(item_id)
            result.append(item)
    return result


def format_artists(artists: list) -> str:
    """Format artist list as comma-separated string"""
    if not artists:
        return "?"
    return ", ".join(a.get("name", "?") for a in artists)


def print_table(rows, max_width=40):
    """Print rows with dynamically computed column widths, capped at max_width."""
    if not rows:
        return
    widths = [min(max(len(row[i]) for row in rows), max_width) for i in range(len(rows[0]))]
    for row in rows:
        parts = []
        for i, cell in enumerate(row):
            cell = cell[:widths[i]] if len(cell) > widths[i] else cell
            if i == len(row) - 1:
                parts.append(cell)
            else:
                parts.append(f"{cell:<{widths[i]}}")
        print("  ".join(parts))


RANGE_MAP = {
    # Explicit aliases → API range values
    "today": "today",
    "1d": "today",
    "4w": "weeks",
    "4weeks": "weeks",
    "6m": "months",
    "6months": "months",
    "all": "lifetime",
    "lifetime": "lifetime"
}

# Relative duration ranges (resolved to custom timestamp pairs)
DURATION_RANGES = {
    "7d": 7,
    "14d": 14,
    "30d": 30,
    "90d": 90,
}

RANGE_HELP = "Time range: today/1d, 7d, 14d, 30d, 90d, 4w/4weeks (4 weeks), 6m/6months (6 months), all (lifetime)"


def resolve_range(value: str) -> Optional[str]:
    """Resolve a CLI range alias to the API range value, or None for duration ranges."""
    lower = value.lower()
    if lower in DURATION_RANGES:
        return None  # Signal that this is a duration range
    mapped = RANGE_MAP.get(lower)
    if not mapped:
        all_valid = sorted(set(list(RANGE_MAP.keys()) + list(DURATION_RANGES.keys())))
        raise SystemExit(f"Unknown range '{value}'. Valid: {', '.join(all_valid)}")
    return mapped


def build_duration_params(days: int) -> str:
    """Build after=&before= params for a relative duration in days."""
    now = datetime.now()
    start = now - timedelta(days=days)
    after_ms = int(start.timestamp() * 1000)
    before_ms = int(now.timestamp() * 1000)
    return f"after={after_ms}&before={before_ms}"



def build_date_params(args, default_range: str = "4w") -> str:
    """Build date query parameters from args (range or start/end)

    Returns query string like "range=weeks" or "after=123&before=456"
    """
    if hasattr(args, 'start') and args.start:
        # Use custom date range
        after = parse_date(args.start)
        params = f"after={after}"
        if hasattr(args, 'end') and args.end:
            before = parse_date(args.end)
            params += f"&before={before}"
        return params
    else:
        # Use predefined range or duration
        range_val = args.range if hasattr(args, 'range') and args.range else default_range
        lower = range_val.lower()
        if lower in DURATION_RANGES:
            return build_duration_params(DURATION_RANGES[lower])
        return f"range={resolve_range(range_val)}"


def cmd_profile(api: StatsAPI, args):
    """Show user profile"""
    user = get_user_or_exit(args)
    data = api.request(f"/users/{user}")
    u = data.get("item", {})

    name = u.get("displayName", "?")
    custom_id = u.get("customId", "")
    pronouns = u.get("profile", {}).get("pronouns", "")
    bio = u.get("profile", {}).get("bio", "")
    created = u.get("createdAt", "")[:10]
    timezone = u.get("timezone", "")
    recently_active = u.get("recentlyActive", False)

    badges = []
    if u.get("isPlus"):
        badges.append("Plus")
        plus_since = u.get("plusSinceAt", "")[:10]
        if plus_since:
            badges[-1] += f" since {plus_since}"
    if u.get("isPro"):
        badges.append("Pro")
    badge_str = "  [" + " | ".join(badges) + "]" if badges else ""

    handle = f" / {custom_id}" if custom_id and custom_id != name else ""
    pronoun_str = f" ({pronouns})" if pronouns else ""
    print(f"{name}{handle}{pronoun_str}{badge_str}")

    if bio:
        print(f"Bio: {bio}")

    active_str = "yes" if recently_active else "no"
    tz_str = f"  •  {timezone}" if timezone else ""
    print(f"Member since: {created}{tz_str}  •  Recently active: {active_str}")

    spotify = u.get("spotifyAuth")
    if spotify:
        sp_name = spotify.get("displayName", "")
        sp_product = spotify.get("product", "")
        sp_sync = "yes" if spotify.get("sync") else "no"
        sp_imported = "yes" if spotify.get("imported") else "no"
        name_str = f"{sp_name}  " if sp_name else ""
        product_str = f"({sp_product})  " if sp_product else ""
        print(f"Spotify: {name_str}{product_str}sync={sp_sync}  imported={sp_imported}")


def cmd_top(api: StatsAPI, args):
    """Unified top command: top {artists|tracks|albums|genres}"""
    user = get_user_or_exit(args)
    date_params = build_date_params(args)
    limit = args.limit or DEFAULT_LIMIT
    top_type = args.type

    from_artist = getattr(args, 'from_artist', None)
    from_album = getattr(args, 'from_album', None)

    # Handle --from-artist / --from-album variants
    if from_artist is not None:
        if top_type == "tracks":
            show_top_items(api, f"/users/{user}/top/artists/{from_artist}/tracks?{date_params}", "track", limit, show_album=True, show_id=True)
        elif top_type == "albums":
            show_top_items(api, f"/users/{user}/top/artists/{from_artist}/albums?{date_params}", "album", limit, show_id=True)
        else:
            print(f"Error: --from-artist not supported for '{top_type}'", file=sys.stderr)
            sys.exit(1)
        return

    if from_album is not None:
        if top_type == "tracks":
            show_top_items(api, f"/users/{user}/top/albums/{from_album}/tracks?{date_params}", "track", limit or 100)
        else:
            print(f"Error: --from-album not supported for '{top_type}'", file=sys.stderr)
            sys.exit(1)
        return

    # Standard top commands
    endpoint = f"/users/{user}/top/{top_type}?{date_params}&limit={limit}"

    if top_type == "tracks":
        show_top_items(api, endpoint, "track", limit, show_album=True, show_id=True)
    elif top_type == "albums":
        show_top_items(api, endpoint, "album", limit, show_id=True)
    elif top_type == "artists":
        data = api.request(endpoint)
        items = data.get("items", [])
        if not items:
            print("No data found.")
            return
        has_stats = items[0].get("playedMs", 0) and (items[0].get("streams") or "?") != "?"
        rows = []
        for item in items:
            artist = item["artist"]
            genres = f"[{', '.join(artist.get('genres', [])[:2])}]"
            row = [f"{item['position']:>3}.", artist["name"]]
            if has_stats:
                row += [f"{item['streams']} plays", f"({format_time(item['playedMs'])})"]
            row += [genres, f"#{artist.get('id', '?')}"]
            rows.append(row)
        print_table(rows)
    elif top_type == "genres":
        data = api.request(endpoint)
        items = data.get("items", [])
        if not items:
            print("No data found.")
            return
        has_stats = items[0].get("playedMs", 0) and (items[0].get("streams") or "?") != "?"
        rows = []
        for item in items:
            row = [f"{item['position']:>3}.", item["genre"]["tag"]]
            if has_stats:
                row += [f"{item['streams']} plays", f"({format_time(item['playedMs'])})"]
            rows.append(row)
        print_table(rows)


def cmd_now_playing(api: StatsAPI, args):
    """Show currently playing track"""
    user = args.user or DEFAULT_USER
    if not user:
        print("Error: No user specified. Set STATSFM_USER or pass --user", file=sys.stderr)
        sys.exit(1)
    user = quote(user, safe='')

    data = api.request(f"/users/{user}/streams/current")
    item = data.get("item")

    if not item:
        print("Nothing playing.")
        return

    track = item["track"]
    artists = format_artists(track["artists"])
    name = track["name"]
    album = track["albums"][0]["name"] if track.get("albums") else "?"
    album_id = track["albums"][0].get("id", "?") if track.get("albums") else "?"
    progress = item["progressMs"] // 1000
    duration = track["durationMs"] // 1000
    device = item.get("deviceName", "?")
    status = "playing" if item.get("isPlaying") else "paused"
    track_id = track.get("id", "?")
    artist_id = track["artists"][0].get("id", "?") if track.get("artists") else "?"

    print(f"Status: {status}")
    print(f"Track: {name} (#{track_id})")
    print(f"Artist: {artists} (#{artist_id})")
    print(f"Album: {album} (#{album_id})")
    print(f"Progress: {progress//60}:{progress%60:02d} / {duration//60}:{duration%60:02d}")
    print(f"Device: {device}")


def cmd_recent(api: StatsAPI, args):
    """Show recently played tracks, with now-playing at the top if active"""
    user = args.user or DEFAULT_USER
    if not user:
        print("Error: No user specified. Set STATSFM_USER or pass --user", file=sys.stderr)
        sys.exit(1)
    user = quote(user, safe='')

    limit = args.limit or DEFAULT_LIMIT

    # Check now playing
    np_data = api.request(f"/users/{user}/streams/current")
    np_item = np_data.get("item")

    rows = []
    if np_item:
        track = np_item["track"]
        label = "NOW" if np_item.get("isPlaying") else "PAUSED"
        album = get_album_name(track)[:25]
        row = [label, track.get("name", "?"), track.get("artists", [{}])[0].get("name", "?"), album, f"#{track.get('id', '?')}"]
        rows.append(row)

    data = api.request(f"/users/{user}/streams/recent")
    all_items = data.get("items", [])
    items = all_items[:limit]

    if not items and not np_item:
        print("No recent streams found.")
        return

    for stream in items:
        track = stream.get("track", {})
        end_time = stream.get("endTime", "")
        if end_time:
            try:
                dt = datetime.fromisoformat(end_time.replace("Z", "+00:00")).astimezone()
                time_str = dt.strftime("%H:%M")
            except:
                time_str = "??:??"
        else:
            time_str = "??:??"

        album = get_album_name(track)[:25]
        row = [time_str, track.get("name", "?"), track.get("artists", [{}])[0].get("name", "?"), album, f"#{track.get('id', '?')}"]
        rows.append(row)
    print_table(rows)
    remaining = len(all_items) - limit
    if remaining > 0:
        print(f"  ({remaining} more)")


def cmd_artist_stats(api: StatsAPI, args):
    """Show stats for a specific artist"""
    user = get_user_or_exit(args)

    artist_data = api.request(f"/artists/{args.artist_id}")
    artist = artist_data.get("item", {})
    genres = ", ".join(artist.get("genres", []))
    followers = artist.get("followers", 0)
    follower_str = f"{followers:,}" if followers else "?"
    print(f"{artist.get('name', '?')}  [{genres}]  {follower_str} followers")
    print()

    date_params = build_date_params(args, "lifetime")
    days, total_count, total_ms = get_per_day_stats_with_totals(
        api, f"/users/{user}/streams/artists/{args.artist_id}/stats/per-day?timeZone={quote(get_local_timezone(), safe='')}&{date_params}"
    )

    print(f"Total: {total_count} plays  ({format_time(total_ms)})")
    print()
    granularity = getattr(args, 'granularity', 'monthly') or 'monthly'
    if granularity == 'daily':
        show_daily_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'weekly':
        show_weekly_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'yearly':
        show_yearly_breakdown(days, getattr(args, 'limit', None))
    else:
        show_monthly_breakdown(days, getattr(args, 'limit', None))


def cmd_track_stats(api: StatsAPI, args):
    """Show stats for a specific track"""
    user = get_user_or_exit(args)
    timezone = quote(get_local_timezone(), safe='')

    if not args.track_id:
        print("Error: Track ID required", file=sys.stderr)
        sys.exit(1)

    # Fetch track info
    track_data = api.request(f"/tracks/{args.track_id}")
    track = track_data.get("item", {})
    track_name = track.get("name", "?")
    artists = format_artists(track.get("artists", []))
    album = track["albums"][0] if track.get("albums") else {}

    print(f"Track: {track_name}")
    print(f"Artist: {artists}")
    print(f"Album: {album.get("name")} (#{album.get("id")})")
    print()

    date_params = build_date_params(args, "lifetime")
    days, total_count, total_ms = get_per_day_stats_with_totals(
        api, f"/users/{user}/streams/tracks/{args.track_id}/stats/per-day?timeZone={timezone}&{date_params}"
    )

    print(f"Total: {total_count} plays  ({format_time(total_ms)})")
    print()
    granularity = getattr(args, 'granularity', 'monthly') or 'monthly'
    if granularity == 'daily':
        show_daily_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'weekly':
        show_weekly_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'yearly':
        show_yearly_breakdown(days, getattr(args, 'limit', None))
    else:
        show_monthly_breakdown(days, getattr(args, 'limit', None))


def cmd_album_stats(api: StatsAPI, args):
    """Show stats for a specific album"""
    user = get_user_or_exit(args)

    if not args.album_id:
        print("Error: Album ID required", file=sys.stderr)
        sys.exit(1)

    date_params = build_date_params(args, "lifetime")
    days, total_count, total_ms = get_per_day_stats_with_totals(
        api, f"/users/{user}/streams/albums/{args.album_id}/stats/per-day?timeZone={quote(get_local_timezone(), safe='')}&{date_params}"
    )

    print(f"Total: {total_count} plays  ({format_time(total_ms)})")
    print()
    granularity = getattr(args, 'granularity', 'monthly') or 'monthly'
    if granularity == 'daily':
        show_daily_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'weekly':
        show_weekly_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'yearly':
        show_yearly_breakdown(days, getattr(args, 'limit', None))
    else:
        show_monthly_breakdown(days, getattr(args, 'limit', None))


def cmd_stream_stats(api: StatsAPI, args):
    """Show overall stream statistics"""
    user = get_user_or_exit(args)

    date_params = build_date_params(args)

    data = api.request(f"/users/{user}/streams/stats?{date_params}")
    items = data.get("items", data.get("item", {}))

    count = items.get("count", "?")
    ms = items.get("durationMs", 0)

    print(f"Streams: {count:,}" if isinstance(count, int) else f"Streams: {count}")
    print(f"Total time: {format_time(ms)}")

    played = items.get("playedMs", {})
    if isinstance(played, dict) and played.get("avg"):
        print(f"Avg track: {format_duration(int(played['avg']))}")
        print(f"Shortest: {format_duration(int(played['min']))}  |  Longest: {format_duration(int(played['max']))}")

    card = items.get("cardinality", {})
    if card:
        parts = []
        if card.get("tracks"):
            parts.append(f"{card['tracks']:,} tracks")
        if card.get("artists"):
            parts.append(f"{card['artists']:,} artists")
        if card.get("albums"):
            parts.append(f"{card['albums']:,} albums")
        if parts:
            print(f"Unique: {', '.join(parts)}")


def cmd_listening_history(api: StatsAPI, args):
    """Show listening history with monthly/weekly/daily breakdown"""
    user = get_user_or_exit(args)

    date_params = build_date_params(args, "lifetime")
    tz = get_local_timezone()
    days, total_count, total_ms = get_per_day_stats_with_totals(
        api, f"/users/{user}/streams/stats/per-day?timeZone={quote(tz, safe='')}&{date_params}"
    )

    print(f"Total: {total_count:,} streams  ({format_time(total_ms)})")
    print()

    granularity = getattr(args, 'granularity', 'monthly') or 'monthly'
    if granularity == 'daily':
        show_daily_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'weekly':
        show_weekly_breakdown(days, getattr(args, 'limit', None))
    elif granularity == 'monthly':
        show_monthly_breakdown(days, getattr(args, 'limit', None))
    else:
        show_yearly_breakdown(days, getattr(args, 'limit', None))


def cmd_first_listen(api: StatsAPI, args):
    """Show first time a track/artist/album was played"""
    user = get_user_or_exit(args)
    entity_type = args.type
    entity_id = args.entity_id
    limit = getattr(args, 'limit', 5) or 5

    if entity_type == "artist":
        url = f"/users/{user}/streams/artists/{entity_id}?limit={limit}&order=asc"
    elif entity_type == "track":
        url = f"/users/{user}/streams/tracks/{entity_id}?limit={limit}&order=asc"
    elif entity_type == "album":
        url = f"/users/{user}/streams/albums/{entity_id}?limit={limit}&order=asc"
    else:
        print(f"Unknown type: {entity_type}")
        sys.exit(1)

    data = api.request(url)
    items = data.get("items", [])

    if not items:
        print("No streams found.")
        return

    # Get entity name for header
    if entity_type == "artist":
        try:
            artist_data = api.request(f"/artists/{entity_id}")
            name = artist_data.get("item", {}).get("name", f"Artist #{entity_id}")
        except Exception:
            name = f"Artist #{entity_id}"
    elif entity_type == "track":
        try:
            track_data = api.request(f"/tracks/{entity_id}")
            track_info = track_data.get("item", {})
            artists = ", ".join(a["name"] for a in track_info.get("artists", []))
            name = f"{track_info.get('name', f'Track #{entity_id}')} by {artists}" if artists else track_info.get("name", f"Track #{entity_id}")
        except Exception:
            name = items[0].get("trackName", f"Track #{entity_id}")
    elif entity_type == "album":
        try:
            album_data = api.request(f"/albums/{entity_id}")
            name = album_data.get("item", {}).get("name", f"Album #{entity_id}")
        except Exception:
            name = f"Album #{entity_id}"

    print(f"First streams: {name}")
    print()

    # Resolve album names for artist queries (not in streams response)
    album_names = {}
    if entity_type == "artist":
        album_ids = list(set(str(s.get("albumId", "")) for s in items if s.get("albumId")))
        if album_ids:
            try:
                ids_str = ",".join(album_ids)
                albums_data = api.request(f"/albums/list?ids={ids_str}")
                for a in albums_data.get("items", []):
                    album_names[a["id"]] = a.get("name", "")
            except Exception:
                pass

    for i, stream in enumerate(items, 1):
        end_time = stream.get("endTime", "")
        played_ms = stream.get("playedMs", 0)
        track_name = stream.get("trackName", "Unknown")
        album_name = album_names.get(stream.get("albumId"), "")

        # Parse and convert to local time
        if end_time:
            dt = datetime.fromisoformat(end_time.replace("Z", "+00:00")).astimezone()
            time_str = dt.strftime("%b %d, %Y at %I:%M %p")
        else:
            time_str = "Unknown"

        duration = format_time(played_ms) if played_ms else "?"
        if entity_type == "artist":
            album_str = f"  [{album_name}]" if album_name else ""
            print(f"  {i}. {track_name}{album_str}  —  {time_str}  ({duration})  #{stream.get('trackId', '')}")
        elif entity_type == "album":
            print(f"  {i}. {track_name}  —  {time_str}  ({duration})  #{stream.get('trackId', '')}")
        else:
            print(f"  {i}. {time_str}  ({duration})")


def cmd_hourly_breakdown(api: StatsAPI, args):
    """Show listening distribution by hour of day"""
    user = get_user_or_exit(args)

    date_params = build_date_params(args)
    range_val = args.range if hasattr(args, 'range') and args.range else "4w"

    tz = get_local_timezone()
    data = api.request(f"/users/{user}/streams/stats/dates?{date_params}&timeZone={tz}")
    items = data.get("items", {})
    hours = items.get("hours", {})

    if not hours:
        print("No hourly data found. Try a wider date range.")
        return

    # Find peak for scaling
    max_count = max(int(v.get("count", 0)) for v in hours.values()) or 1

    print(f"Hourly listening distribution ({range_val}):")
    print(f"{'Hour':<8} {'Plays':>6}   {'Bar'}")
    print("-" * 50)

    total_plays = 0
    hour_data = []
    for h in range(24):
        h_data = hours.get(str(h), {})
        count = h_data.get("count", 0)
        total_plays += count
        hour_data.append((h, count))

    peak_hours = sorted(hour_data, key=lambda x: x[1], reverse=True)[:3]
    peak_set = {h for h, _ in peak_hours}

    for h, count in hour_data:
        label = f"{h:02d}:00"
        bar_len = int((count / max_count) * 25)
        bar = "█" * bar_len
        peak_marker = " ← peak" if h == peak_hours[0][0] else ""
        print(f"{label:<8} {count:>6}   {bar}{peak_marker}")

    print("-" * 50)
    print(f"Total: {total_plays:,} plays")
    if peak_hours:
        top3 = ", ".join(f"{h:02d}:00 ({c} plays)" for h, c in peak_hours)
        print(f"Top hours: {top3}")

    # Night owl score: plays between 23:00-05:00 vs total
    night_plays = sum(c for h, c in hour_data if h >= 23 or h <= 5)
    if total_plays > 0:
        night_pct = night_plays / total_plays * 100
        print(f"Night owl score: {night_pct:.0f}% of plays between 23:00–05:00")


def show_top_items(api: StatsAPI, endpoint: str, item_key: str, limit: int, show_album=False, show_id=False):
    """Shared logic for top-tracks-from-artist, top-tracks-from-album, top-albums-from-artist"""
    data = api.request(endpoint)
    items = data.get("items", [])

    if not items:
        print("No data found.")
        return

    total = len(items)
    items = items[:limit]
    has_stats = items[0].get("playedMs", 0) and (items[0].get("streams") or "?") != "?"
    rows = []
    for item in items:
        entry = item[item_key]
        row = [f"{item['position']:>3}.", entry["name"]]
        if item_key == "track":
            row.append(format_artists(entry.get("artists", [])))
        if show_album:
            row.append(get_album_name(entry))
        if has_stats:
            row += [f"{item['streams']} plays", f"({format_time(item['playedMs'])})"]
        if show_id:
            row.append(f"#{entry.get('id', '?')}")
        rows.append(row)
    print_table(rows)
    remaining = total - limit
    if remaining > 0:
        print(f"  ({remaining} more)")


def cmd_charts(api: StatsAPI, args):
    """Unified charts command: charts {tracks|artists|albums}"""
    date_params = build_date_params(args, "today")
    limit = args.limit or DEFAULT_LIMIT
    charts_type = args.type

    data = api.request(f"/charts/top/{charts_type}?{date_params}")
    items = data.get("items", [])[:limit]

    if not items:
        print("No chart data found.")
        return

    rows = []
    if charts_type == "tracks":
        for item in items:
            track = item.get("track", {})
            artists = track.get("artists", [])
            artist = artists[0].get("name", "?") if artists else "?"
            row = [f"{item.get('position', '?'):>3}.", track.get("name", "?"), artist, get_album_name(track), f"{item.get('streams', 0)} streams"]
            rows.append(row)

    elif charts_type == "artists":
        for item in items:
            artist = item.get("artist", {})
            genres = f"[{', '.join(artist.get('genres', [])[:2])}]"
            rows.append([f"{item.get('position', '?'):>3}.", artist.get("name", "?"), f"{item.get('streams', 0)} streams", genres])

    elif charts_type == "albums":
        for item in items:
            album = item.get("album", {})
            artists = album.get("artists", [])
            artist = artists[0].get("name", "?") if artists else "?"
            rows.append([f"{item.get('position', '?'):>3}.", album.get("name", "?"), artist, f"{item.get('streams', 0)} streams"])

    print_table(rows)


def cmd_artist(api: StatsAPI, args):
    """Show artist info and discography"""
    data = api.request(f"/artists/{args.artist_id}")
    artist = data.get("item", {})

    name = artist.get("name", "?")
    genres = ", ".join(artist.get("genres", []))
    followers = artist.get("followers", 0)
    follower_str = f"{followers:,}" if followers else "?"
    popularity = artist.get("spotifyPopularity", 0)

    print(f"{name}  #{args.artist_id}")
    if genres:
        print(f"Genre: {genres}")
    print(f"Followers: {follower_str}")

    albums_data = api.request(f"/artists/{args.artist_id}/albums?limit=500")
    items = albums_data.get("items", [])

    if not items:
        print("\nNo albums found.")
        return

    unique = dedupe(items)
    unique.sort(key=lambda a: a.get("releaseDate", 0), reverse=True)

    groups = {}
    for a in unique:
        groups.setdefault(a.get("type", "other"), []).append(a)

    album_type = getattr(args, 'type', 'album') or 'album'
    type_order = [("album", "Albums"), ("single", "Singles & EPs"), ("compilation", "Compilations")]
    show_types = type_order if album_type == "all" else [(album_type, dict(type_order)[album_type])]
    limit = args.limit or DEFAULT_LIMIT

    for key, label in show_types:
        section = groups.get(key, [])
        if not section:
            continue
        print()
        print(f"{label}:")
        rows = []
        for album in section[:limit]:
            release_ms = album.get("releaseDate", 0)
            year = datetime.fromtimestamp(release_ms / 1000).strftime("%Y") if release_ms else "?"
            rows.append([year, album["name"], f"{album.get('totalTracks', '?')} tracks", f"#{album['id']}"])
        print_table(rows)
        remaining = len(section) - limit
        if remaining > 0:
            print(f"  ({remaining} more)")



def cmd_album(api: StatsAPI, args):
    """Show album info and tracklist"""
    data = api.request(f"/albums/{args.album_id}")
    album = data.get("item", {})

    name = album.get("name", "?")
    artists = format_artists(album.get("artists", []))
    release_ms = album.get("releaseDate", 0)
    release_date = datetime.fromtimestamp(release_ms / 1000).strftime("%Y-%m-%d") if release_ms else "?"
    label = album.get("label", "")
    genres = ", ".join(album.get("genres", []))

    print(f"{name}  #{args.album_id}")
    for a in album.get("artists", []):
        print(f"Artist: {a.get('name', '?')}  #{a.get('id', '?')}")
    print(f"Released: {release_date}  {album.get('totalTracks', '?')} tracks")
    if label:
        print(f"Label: {label}")
    if genres:
        print(f"Genre: {genres}")
    print()

    tracks_data = api.request(f"/albums/{args.album_id}/tracks")
    tracks = tracks_data.get("items", [])

    if not tracks:
        print("No tracks found.")
        return

    rows = []
    for i, track in enumerate(tracks, 1):
        tag = " [E]" if track.get("explicit") else ""
        rows.append([
            f"{i:>2}.",
            track.get("name", "?") + tag,
            format_duration(track.get("durationMs", 0)),
            f"#{track.get('id', '?')}",
        ])
    print_table(rows)


def cmd_track(api: StatsAPI, args):
    """Show track info"""
    data = api.request(f"/tracks/{args.track_id}")
    track = data.get("item", {})

    name = track.get("name", "?")
    album = track["albums"][0] if track.get("albums") else {}
    album_name = album.get("name", "?")
    album_id = album.get("id", "?")
    duration = track.get("durationMs", 0)
    explicit = " [E]" if track.get("explicit") else ""

    spotify_ids = track.get("externalIds", {}).get("spotify", [])
    spotify_url = f"https://open.spotify.com/track/{spotify_ids[0]}" if spotify_ids else None

    print(f"{name}{explicit}  #{args.track_id}")
    for a in track.get("artists", []):
        print(f"Artist: {a.get('name', '?')}  #{a.get('id', '?')}")
    print(f"Album: {album_name}  #{album_id}")
    print(f"Duration: {format_duration(duration)}")
    if spotify_url:
        print(f"Spotify: {spotify_url}")


def cmd_track_features(api: StatsAPI, args):
    """Show Spotify audio features for a track"""
    track_ids = args.track_ids
    results = []

    KEY_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    # Batch fetch all track metadata in one call
    ids_param = ",".join(str(tid) for tid in track_ids)
    tracks_data = api.request(f"/tracks/list?ids={ids_param}")
    tracks = tracks_data.get("items", [])

    # Build lookup by track ID
    track_map = {}
    for t in tracks:
        track_map[t.get("id")] = t

    # Collect Spotify IDs and fetch audio features individually
    # (stats.fm doesn't support batch audio features)
    for track_id in track_ids:
        track = track_map.get(track_id, {})
        name = track.get("name", f"Track #{track_id}")
        artists = ", ".join(a["name"] for a in track.get("artists", []))
        spotify_ids = track.get("externalIds", {}).get("spotify", [])
        if not spotify_ids:
            print(f"{name}: no Spotify ID found")
            continue

        f_data = api.request(f"/SPOTIFY/audio-features/{spotify_ids[0]}")
        f = f_data.get("item", {})
        results.append((name, artists, f))

    for name, artists, f in results:
        if len(results) > 1:
            print(f"\n{name}  by {artists}")
            print("─" * 50)
        else:
            print(f"{name}  by {artists}\n")

        def bar(val, width=20):
            filled = int(round(val * width))
            return "█" * filled + "░" * (width - filled)

        energy = f.get("energy", 0)
        dance = f.get("danceability", 0)
        valence = f.get("valence", 0)
        acoust = f.get("acousticness", 0)
        speech = f.get("speechiness", 0)
        liveness = f.get("liveness", 0)
        tempo = f.get("tempo", 0)
        loud = f.get("loudness", 0)
        key = f.get("key", -1)
        mode = f.get("mode", 1)
        sig = f.get("time_signature", 4)

        key_name = KEY_NAMES[key] if 0 <= key <= 11 else "?"
        mode_name = "major" if mode == 1 else "minor"

        print(f"  Energy      {bar(energy)} {energy:.2f}")
        print(f"  Danceability{bar(dance)} {dance:.2f}")
        print(f"  Valence     {bar(valence)} {valence:.2f}  ({'happy' if valence > 0.5 else 'sad'})")
        print(f"  Acousticness{bar(acoust)} {acoust:.2f}")
        print(f"  Speechiness {bar(speech)} {speech:.2f}")
        print(f"  Liveness    {bar(liveness)} {liveness:.2f}")
        print()
        print(f"  Tempo    {tempo:.1f} BPM   Loudness {loud:.1f} dB")
        print(f"  Key      {key_name} {mode_name}   Time sig {sig}/4")
        print()


def cmd_album_breakdown(api: StatsAPI, args):
    """Show per-track play counts for an album (your personal listening breakdown).

    Uses two API calls: album tracklist + user top tracks from album.
    Tracks with no plays show as 0 (visible gaps in listening).
    """
    user = get_user_or_exit(args)

    album_data = api.request(f"/albums/{args.album_id}")
    album = album_data.get("item", {})
    album_name = album.get("name", "?")
    artists = format_artists(album.get("artists", []))
    release_ms = album.get("releaseDate", 0) or 0
    year = datetime.fromtimestamp(release_ms / 1000).year if release_ms else "?"

    tracks_data = api.request(f"/albums/{args.album_id}/tracks")
    tracks = tracks_data.get("items", [])

    if not tracks:
        print("No tracks found.")
        return

    # Batch fetch: get all played tracks in one call
    date_params = build_date_params(args, "lifetime")
    played_data = api.request(f"/users/{user}/top/albums/{args.album_id}/tracks?{date_params}")
    played_items = played_data.get("items", [])

    # Build lookup: track_id -> {streams, playedMs}
    played_map = {}
    for item in played_items:
        track = item.get("track", {})
        tid = track.get("id")
        if tid:
            played_map[tid] = {
                "streams": item.get("streams", 0) or 0,
                "playedMs": item.get("playedMs", 0) or 0,
            }

    print(f"{album_name} by {artists}  ({year})  #{args.album_id}")
    print(f"Listening breakdown for: {user}\n")

    rows = []
    total_plays = 0
    total_ms = 0

    for i, track in enumerate(tracks, 1):
        track_id = track.get("id")
        track_name = track.get("name", "?")
        stats = played_map.get(track_id, {"streams": 0, "playedMs": 0})
        plays = stats["streams"]
        dur_ms = stats["playedMs"]
        total_plays += plays
        total_ms += dur_ms
        rows.append((i, track_name, plays, dur_ms))

    for i, name, plays, dur_ms in rows:
        mins = dur_ms // 60000
        h, m = divmod(mins, 60)
        time_str = f"{h}h {m:02d}m" if h else f"{m}m" if mins else "—"
        print(f"  {i:<3} {name:<40} {plays:>6,}  {time_str:>7}")

    total_h = total_ms / 3600000
    avg = total_plays / len(tracks) if tracks else 0
    print(f"\n  Total: {total_plays:,} plays  |  {total_h:.0f}h listened  |  {avg:.1f} avg/track")


def cmd_search(api: StatsAPI, args):
    """Search for artists, tracks, or albums"""
    if not args.query:
        print("Error: Search query required", file=sys.stderr)
        sys.exit(1)

    search_type = args.type
    limit = args.limit or 5
    encoded_query = quote(args.query)

    # Build URL: omit type param for broad search across all categories
    if search_type:
        url = f"/search?query={encoded_query}&type={search_type}&limit={limit}"
    else:
        url = f"/search?query={encoded_query}&limit={limit}"

    data = api.request(url)
    items = data.get("items", {})

    found_any = False

    # Show artists if type is artist or broad search
    if search_type in ("artist", None):
        artists = items.get("artists", [])
        if artists:
            found_any = True
            print("\nARTISTS:")
            for artist in artists[:limit]:
                aid = artist.get("id", "?")
                name = artist.get("name", "?")
                genres = ", ".join(artist.get("genres", [])[:2])
                extra = f"  [{genres}]" if genres else ""
                print(f"  [{aid}] {name}{extra}")

    # Show tracks if type is track or broad search
    if search_type in ("track", None):
        tracks = items.get("tracks", [])
        if tracks:
            found_any = True
            print("\nTRACKS:")
            for track in tracks[:limit]:
                tid = track.get("id", "?")
                name = track.get("name", "?")
                artists = format_artists(track.get("artists", []))
                print(f"  [{tid}] {name} by {artists}")

    # Show albums if type is album or broad search
    if search_type in ("album", None):
        albums = items.get("albums", [])
        if albums:
            found_any = True
            print("\nALBUMS:")
            for album in albums[:limit]:
                alb_id = album.get("id", "?")
                name = album.get("name", "?")
                artists = format_artists(album.get("artists", []))
                print(f"  [{alb_id}] {name} by {artists}")

    if not found_any:
        print("No results found.")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="stats.fm CLI - Query Spotify listening statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s top artists
  %(prog)s top tracks --range lifetime --limit 20
  %(prog)s top tracks --from-artist 123
  %(prog)s top albums --from-artist 123
  %(prog)s top tracks --from-album 456
  %(prog)s charts tracks
  %(prog)s now-playing --user <username>
  %(prog)s search "madison beer"
  %(prog)s track-history 70714270 --range lifetime

Ranges: today/1d, 4w/weeks (4 weeks), 6m/months (6 months), lifetime/all
Set STATSFM_USER environment variable for default user
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Profile command
    profile_parser = subparsers.add_parser("profile", help="Show user profile")
    profile_parser.add_argument("--user", "-u", help="stats.fm username")

    # Top command (artists, tracks, albums, genres)
    top_parser = subparsers.add_parser("top", help="Show top artists/tracks/albums/genres")
    top_parser.add_argument("type", choices=["artists", "tracks", "albums", "genres"], help="What to show")
    top_parser.add_argument("--range", "-r", help=RANGE_HELP)
    top_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    top_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    top_parser.add_argument("--limit", "-l", type=int, help="Number of results (default: 15)")
    top_parser.add_argument("--user", "-u", help="stats.fm username")
    top_parser.add_argument("--from-artist", type=int, metavar="ID", help="Show top tracks/albums from a specific artist")
    top_parser.add_argument("--from-album", type=int, metavar="ID", help="Show top tracks from a specific album")

    # Now playing command
    now_parser = subparsers.add_parser("now-playing", aliases=["now", "np"], help="Show currently playing")
    now_parser.add_argument("--user", "-u", help="stats.fm username")

    # Recent command
    recent_parser = subparsers.add_parser("recent", help="Show recently played tracks")
    recent_parser.add_argument("--limit", "-l", type=int, help="Number of results (default: 10)")
    recent_parser.add_argument("--user", "-u", help="stats.fm username")

    # Artist history command
    artist_stats_parser = subparsers.add_parser("artist-history", aliases=["artist-stats"], help="Show history for a specific artist")
    artist_stats_parser.add_argument("artist_id", type=int, help="Artist ID")
    artist_stats_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    artist_stats_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    artist_stats_parser.add_argument("--limit", "-l", type=int, help="Limit to most recent N periods")
    artist_stats_parser.add_argument("--granularity", "-g", choices=["daily", "weekly", "monthly", "yearly"], default="monthly", help="Breakdown granularity (default: monthly)")
    artist_stats_parser.add_argument("--user", "-u", help="stats.fm username")

    # Track history command
    track_stats_parser = subparsers.add_parser("track-history", aliases=["track-stats"], help="Show history for a specific track")
    track_stats_parser.add_argument("track_id", type=int, help="Track ID")
    track_stats_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    track_stats_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    track_stats_parser.add_argument("--limit", "-l", type=int, help="Limit to most recent N periods")
    track_stats_parser.add_argument("--granularity", "-g", choices=["daily", "weekly", "monthly", "yearly"], default="monthly", help="Breakdown granularity (default: monthly)")
    track_stats_parser.add_argument("--user", "-u", help="stats.fm username")

    # Album history command
    album_stats_parser = subparsers.add_parser("album-history", aliases=["album-stats"], help="Show history for a specific album")
    album_stats_parser.add_argument("album_id", type=int, help="Album ID")
    album_stats_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    album_stats_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    album_stats_parser.add_argument("--limit", "-l", type=int, help="Limit to most recent N periods")
    album_stats_parser.add_argument("--granularity", "-g", choices=["daily", "weekly", "monthly", "yearly"], default="monthly", help="Breakdown granularity (default: monthly)")
    album_stats_parser.add_argument("--user", "-u", help="stats.fm username")

    # Listening history command
    history_parser = subparsers.add_parser("listening-history", aliases=["history"], help="Show listening history with monthly/weekly/daily breakdown")
    history_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    history_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    history_parser.add_argument("--granularity", "-g", choices=["daily", "weekly", "monthly", "yearly"], default="yearly", help="Breakdown granularity")
    history_parser.add_argument("--limit", "-l", type=int, help="Max results")
    history_parser.add_argument("--user", "-u", help="stats.fm username")

    # Stream stats command
    stream_stats_parser = subparsers.add_parser("stream-stats", help="Show overall stream statistics")
    stream_stats_parser.add_argument("--range", "-r", help=RANGE_HELP)
    stream_stats_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    stream_stats_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    stream_stats_parser.add_argument("--user", "-u", help="stats.fm username")

    # First listen command
    first_parser = subparsers.add_parser("first-listen", aliases=["first"], help="Show first time a track/artist/album was played")
    first_parser.add_argument("type", choices=["artist", "track", "album"], help="Entity type")
    first_parser.add_argument("entity_id", type=int, help="Entity ID")
    first_parser.add_argument("--limit", "-l", type=int, default=5, help="Number of first streams to show (default: 5)")
    first_parser.add_argument("--user", "-u", help="stats.fm username")

    # Hourly breakdown command
    hourly_parser = subparsers.add_parser("hourly-breakdown", help="Show listening distribution by hour of day")
    hourly_parser.add_argument("--range", "-r", help=RANGE_HELP)
    hourly_parser.add_argument("--start", help="Start date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    hourly_parser.add_argument("--end", help="End date (YYYY, YYYY-MM, or YYYY-MM-DD)")
    hourly_parser.add_argument("--user", "-u", help="stats.fm username")


    # Artist lookup command
    artist_parser = subparsers.add_parser("artist", help="Show artist info and discography")
    artist_parser.add_argument("artist_id", type=int, help="Artist ID")
    artist_parser.add_argument("--type", "-t", choices=["album", "single", "all"], default="album", help="Filter by type (default: album, use 'all' to include singles)")
    artist_parser.add_argument("--limit", "-l", type=int, help="Items per section (default: 15)")

    # Charts command (global top tracks/artists/albums)
    charts_parser = subparsers.add_parser("charts", help="Show global top charts")
    charts_parser.add_argument("type", choices=["tracks", "artists", "albums"], help="What to show")
    charts_parser.add_argument("--limit", "-l", type=int, help="Number of results (default: 15)")
    charts_parser.add_argument("--range", "-r", help=RANGE_HELP)

    # Album lookup command
    album_parser = subparsers.add_parser("album", help="Show album info and tracklist")
    album_parser.add_argument("album_id", type=int, help="Album ID")

    # Track lookup command
    track_parser = subparsers.add_parser("track", help="Show track info")
    track_parser.add_argument("track_id", type=int, help="Track ID")

    # Track features command
    features_parser = subparsers.add_parser("track-features", aliases=["features"], help="Show Spotify audio features for a track")
    features_parser.add_argument("track_ids", type=int, nargs="+", help="Track ID(s)")

    # Search command
    breakdown_parser = subparsers.add_parser("album-breakdown", aliases=["breakdown"], help="Show per-track play counts for an album")
    breakdown_parser.add_argument("album_id", type=int, help="Album ID (from 'album' or 'search' command)")
    breakdown_parser.add_argument("--user", "-u", default=DEFAULT_USER, help="stats.fm username")
    breakdown_parser.set_defaults(command="album-breakdown")

    search_parser = subparsers.add_parser("search", help="Search for artists, tracks, or albums")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--type", "-t", choices=["artist", "track", "album"], help="Filter by type (omit to search all)")
    search_parser.add_argument("--limit", "-l", type=int, help="Results per category (default: 5)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    api = StatsAPI()

    # Route to appropriate command
    commands = {
        "profile": cmd_profile,
        "top": cmd_top,
        "now-playing": cmd_now_playing,
        "now": cmd_now_playing,
        "np": cmd_now_playing,
        "recent": cmd_recent,
        "artist-stats": cmd_artist_stats,
        "artist-history": cmd_artist_stats,
        "track-stats": cmd_track_stats,
        "track-history": cmd_track_stats,
        "album-stats": cmd_album_stats,
        "album-history": cmd_album_stats,
        "stream-stats": cmd_stream_stats,
        "listening-history": cmd_listening_history,
        "history": cmd_listening_history,
        "first-listen": cmd_first_listen,
        "first": cmd_first_listen,
        "hourly-breakdown": cmd_hourly_breakdown,
        "hourly": cmd_hourly_breakdown,
        "charts": cmd_charts,
        "album": cmd_album,
        "artist": cmd_artist,
        "track": cmd_track,
        "track-features": cmd_track_features,
        "features": cmd_track_features,
        "album-breakdown": cmd_album_breakdown,
        "breakdown": cmd_album_breakdown,
        "search": cmd_search,
    }

    cmd_func = commands.get(args.command)
    if cmd_func:
        cmd_func(api, args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
