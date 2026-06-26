---
name: steam-games-updates
description: Fetch recent game updates from Steam News. Use when the user asks about game patches, updates, or news for their tracked Steam games, or wants to add/remove games from their tracking list.
metadata: {"openclaw":{"emoji":"🎮","requires":{"bins":["python3"]}}}
---

# Steam Games Updates

Fetch and accumulate game news from the Steam News API for a configurable list of games.

## First run

On first run, `skill-config.json` is created with **Counter-Strike 2** and **PUBG: BATTLEGROUNDS** as defaults. Tell the user which games are configured and ask if they want to add or remove any.

## Usage

Fetch updates for all tracked games:

```bash
python3 {baseDir}/scripts/updates.py
```

List currently tracked games:

```bash
python3 {baseDir}/scripts/updates.py --list
```

## Adding a game

When the user asks to add a game (even with an imprecise name), search Steam to resolve it:

```bash
python3 {baseDir}/scripts/updates.py --search "game name"
```

This returns a JSON array of matches with `appid` and `name`. Show the user the top results and ask them to confirm which one. Then add it:

```bash
python3 {baseDir}/scripts/updates.py --add <appid>
```

The canonical game name is fetched automatically from Steam when adding.

## Removing a game

```bash
python3 {baseDir}/scripts/updates.py --remove <appid>
```

## Changing settings

All settings live in `{baseDir}/skill-config.json`:

```json
{
  "games": [
    {"name": "Counter-Strike 2", "appid": 730},
    {"name": "PUBG: BATTLEGROUNDS", "appid": 578080}
  ],
  "lookback_days": 3,
  "exclude_patterns": {
    "578080": ["Weekly Ban"]
  }
}
```

| Key | What it does | How to change |
|-----|-------------|---------------|
| `games` | List of tracked games with Steam appids. | Use `--add` / `--remove` commands, or edit directly. |
| `lookback_days` | Max days to look back for updates. | Set to any positive integer. |
| `exclude_patterns` | Per-game title regex filters (keyed by appid). | Add regex strings to skip unwanted posts (e.g. ban waves). |

## Data files

All data lives in `data/` (gitignored):
- `updates.json` — accumulated update records
- `.state.json` — last-run timestamp

## Notes

- No API key required. Uses the public Steam Web API (`ISteamNews`) and Steam Community search.
- Each update record contains: `game`, `appid`, `title`, `url`, `date`, `content`, `discovered_at`, `status`.
- Re-running merges new updates without duplicates.
