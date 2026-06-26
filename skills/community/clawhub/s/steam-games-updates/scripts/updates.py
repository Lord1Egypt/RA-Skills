#!/usr/bin/env python3
"""Fetch recent game updates from Steam News API."""

import json
import re
import sys
import urllib.request
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
CONFIG_FILE = BASE_DIR / "skill-config.json"
STATE_FILE = DATA_DIR / ".state.json"
UPDATES_FILE = DATA_DIR / "updates.json"

STEAM_NEWS_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
STEAM_SEARCH_URL = "https://steamcommunity.com/actions/SearchApps/"
STEAM_APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"

DEFAULT_CONFIG = {
    "games": [
        {"name": "Counter-Strike 2", "appid": 730},
        {"name": "PUBG: BATTLEGROUNDS", "appid": 578080},
    ],
    "lookback_days": 3,
    "exclude_patterns": {
        "578080": ["Weekly Ban"],
    },
}


def load_config():
    config = dict(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            config.update(json.load(f))
    return config


def init_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        print(f"Created {CONFIG_FILE.name} with default games (CS2, PUBG).")
    return load_config()


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")


def fetch_json(url):
    req = urllib.request.Request(
        url, headers={"User-Agent": "steam-games-updates/1.0"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


# ---------------------------------------------------------------------------
# Game search & management
# ---------------------------------------------------------------------------


def search_games(query):
    """Search Steam for games matching a query string."""
    url = STEAM_SEARCH_URL + urllib.parse.quote(query)
    results = fetch_json(url)
    return [{"appid": int(r["appid"]), "name": r["name"]} for r in results[:10]]


def add_game(appid):
    """Add a game by appid. Fetches canonical name from Steam."""
    config = load_config()

    for game in config["games"]:
        if game["appid"] == appid:
            print(f"Already tracking: {game['name']} ({appid})")
            return

    url = f"{STEAM_APP_DETAILS_URL}?appids={appid}"
    data = fetch_json(url)
    app_data = data.get(str(appid), {})
    if not app_data.get("success"):
        print(f"Error: Could not find app {appid} on Steam.")
        sys.exit(1)

    name = app_data["data"]["name"]
    config["games"].append({"name": name, "appid": appid})
    save_config(config)
    print(f"Added: {name} ({appid})")


def remove_game(appid):
    """Remove a game from the config by appid."""
    config = load_config()
    before = len(config["games"])
    config["games"] = [g for g in config["games"] if g["appid"] != appid]

    if len(config["games"]) == before:
        print(f"Game {appid} not found in config.")
        return

    config.get("exclude_patterns", {}).pop(str(appid), None)
    save_config(config)
    print(f"Removed app {appid} from tracked games.")


def list_games():
    config = load_config()
    if not config["games"]:
        print("No games configured.")
        return
    for g in config["games"]:
        excl = config.get("exclude_patterns", {}).get(str(g["appid"]), [])
        suffix = f"  (excludes: {', '.join(excl)})" if excl else ""
        print(f"  {g['name']} ({g['appid']}){suffix}")


# ---------------------------------------------------------------------------
# News fetching
# ---------------------------------------------------------------------------


def get_since_timestamp(config):
    lookback = int(config.get("lookback_days", 3))
    cutoff = int((datetime.now(timezone.utc) - timedelta(days=lookback)).timestamp())
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            last_run = json.load(f).get("last_run", 0)
        return max(last_run, cutoff)
    return cutoff


def save_state():
    DATA_DIR.mkdir(exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump({"last_run": int(datetime.now(timezone.utc).timestamp())}, f)


def clean_content(raw):
    """Strip BBCode, Steam tokens, and HTML from news content."""
    text = re.sub(r"<br\s*/?>", "\n", raw, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    text = re.sub(r"\[/?(?:p|list|b|i|u|strike|spoiler)\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[\*\]", "- ", text)
    text = re.sub(r"\[/\*\]", "", text)
    text = re.sub(r"\[url=[^\]]*\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[/url\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[img[^\]]*\][^\[]*\[/img\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\[/?h[0-9]\]", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\{STEAM[^}]*\}", "", text)
    text = re.sub(r"https?://\S+\.(?:png|jpg|gif|jpeg|webp)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()[:500]


def should_exclude(title, appid, config):
    for pattern in config.get("exclude_patterns", {}).get(str(appid), []):
        if re.search(pattern, title, re.IGNORECASE):
            return True
    return False


def fetch_game_news(appid, since):
    url = f"{STEAM_NEWS_URL}?appid={appid}&count=15"
    try:
        data = fetch_json(url)
    except Exception:
        return []
    return [
        item
        for item in data.get("appnews", {}).get("newsitems", [])
        if item.get("date", 0) > since
        and item.get("feedname") == "steam_community_announcements"
    ]


def load_existing():
    if UPDATES_FILE.exists():
        with open(UPDATES_FILE) as f:
            return {r["url"]: r for r in json.load(f)}
    return {}


def fetch_updates():
    """Fetch updates for all configured games."""
    config = init_config()
    since = get_since_timestamp(config)
    existing = load_existing()
    now_iso = datetime.now(timezone.utc).isoformat()
    new_count = 0
    output_sections = []

    for game in config["games"]:
        appid = game["appid"]
        name = game["name"]
        items = fetch_game_news(appid, since)
        game_entries = []

        for item in items:
            if should_exclude(item["title"], appid, config):
                continue

            url = item.get("url", "")
            if url in existing:
                continue

            record = {
                "game": name,
                "appid": appid,
                "title": item["title"],
                "url": url,
                "date": datetime.fromtimestamp(
                    item["date"], tz=timezone.utc
                ).strftime("%Y-%m-%d"),
                "content": clean_content(item.get("contents", "")),
                "discovered_at": now_iso,
                "status": "active",
            }
            existing[url] = record
            game_entries.append(record)
            new_count += 1

        if game_entries:
            lines = [f"### {name}\n"]
            for entry in game_entries:
                date_display = datetime.strptime(entry["date"], "%Y-%m-%d").strftime(
                    "%b %d"
                )
                lines.append(
                    f"[**{entry['title']}**]({entry['url']}) — _{date_display}_"
                )
                lines.append(entry["content"][:300] + "\n")
            output_sections.append("\n".join(lines))

    DATA_DIR.mkdir(exist_ok=True)
    with open(UPDATES_FILE, "w") as f:
        json.dump(list(existing.values()), f, indent=2)
        f.write("\n")
    save_state()

    if output_sections:
        print("\n\n".join(output_sections))
        print(f"\n{new_count} new update(s) found.")
    else:
        print("No new updates.")

    return new_count > 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main():
    args = sys.argv[1:]

    if not args:
        success = fetch_updates()
        sys.exit(0 if success else 1)

    cmd = args[0]

    if cmd == "--search" and len(args) > 1:
        query = " ".join(args[1:])
        results = search_games(query)
        if not results:
            print(f"No games found for '{query}'.")
            sys.exit(1)
        print(json.dumps(results, indent=2))

    elif cmd == "--add" and len(args) > 1:
        try:
            appid = int(args[1])
        except ValueError:
            print("Usage: --add <appid>  (use --search to find the appid first)")
            sys.exit(1)
        add_game(appid)

    elif cmd == "--remove" and len(args) > 1:
        try:
            appid = int(args[1])
        except ValueError:
            print("Usage: --remove <appid>")
            sys.exit(1)
        remove_game(appid)

    elif cmd == "--list":
        list_games()

    else:
        print("Usage: updates.py [--search <name> | --add <appid> | --remove <appid> | --list]")
        print("  (no args)     Fetch updates for all tracked games")
        print("  --search      Search Steam for a game by name")
        print("  --add         Add a game by Steam appid")
        print("  --remove      Remove a game by Steam appid")
        print("  --list        Show tracked games")
        sys.exit(1)


if __name__ == "__main__":
    main()
