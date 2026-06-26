---
name: yahoo-fantasy-baseball
description: >
  Query your Yahoo Fantasy Baseball league: view roster, standings, matchups,
  free agents, draft results, transactions, and injuries. Daily roster
  optimization detects inactive players and suggests bench swaps and IL moves.
  Read-only — no roster modifications. Use when the user asks about their
  fantasy baseball team, who to start or sit, league standings, available
  free agents, or injury updates.
metadata: {"openclaw":{"emoji":"⚾","requires":{"bins":["python3"]}}}
---

# Yahoo Fantasy Baseball

Query your Yahoo Fantasy Baseball league: view data and optimize your daily lineup via the Yahoo Fantasy Sports API. Read-only — no roster modifications are made.

## Requirements

- Python 3.10+
- `yahoo_fantasy_api` — Yahoo Fantasy Sports API wrapper

**Installation:** Before first use, run `--setup` to create a local `.deps/` virtual environment and install dependencies from `requirements.txt`. Subsequent runs reuse the existing venv. To force a clean reinstall, delete the `.deps/` directory and run `--setup` again.

```bash
python3 yahoo-fantasy-baseball.py --setup
```

## Setup

### 1. Create a Yahoo Developer App

1. Go to [https://developer.yahoo.com/apps/](https://developer.yahoo.com/apps/)
2. Click "Create an App"
3. Set **Redirect URI** to `oob` (out-of-band — Yahoo displays the auth code on screen instead of redirecting to a URL)
4. Copy the **Consumer Key** and **Consumer Secret**

### 2. Authenticate

```bash
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py auth
```

Follow the prompts to enter your Consumer Key and Secret. A browser window opens for Yahoo OAuth authorization. Tokens are cached automatically — you only need to do this once.

### 3. Find Your League

```bash
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py leagues
```

### 4. Set Defaults

```bash
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py config --league 12345
```

The skill auto-detects your team within the league. You can also set it explicitly:

```bash
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py config --league 12345 --team 3
```

## Quick Start

```bash
# View your roster
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py roster

# Daily roster status (who's playing, who's off)
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py today

# Roster status for a specific date
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py day --date 2026-03-25

# Get optimization suggestions
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py optimize

# League standings
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py standings
```

## Commands

### Data Commands (Read)

```bash
# Auth & Config
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py auth
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py config --league 12345 --team 3 --season 2026
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py config

# Leagues & Teams
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py leagues [--season YEAR]
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py teams

# Roster & Lineup
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py roster [--date YYYY-MM-DD]
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py lineup [--week N]

# Standings & Matchups
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py standings
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py matchup [--week N]
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py scoreboard [--week N]

# Players & Draft
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py players [--search NAME] [--position POS] [--status FA|A|T|W|ALL] [--sort OR|AR|PTS|NAME|HR|ERA|...] [--sort-type season|lastweek|lastmonth] [--stat-season YEAR] [--count N]
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py draft [--team ID]
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py transactions [--type add,drop,trade] [--since 3d]
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py injuries

# Lineup Check — confirmed MLB lineups vs fantasy roster
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py lineup-check [--date YYYY-MM-DD]
```

### Daily Management

```bash
# Today: roster status with MLB schedule awareness (shortcut for 'day' with today's date)
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py today

# Day: roster status for a specific date
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py day --date 2026-03-25
```

Groups your roster into ACTIVE (team playing), NOT PLAYING (team off), INJURED, and BENCH. Shows each player's eligible positions, game start times (local timezone), and flags probable starting pitchers. Displays "First pitch" time at the top so you know when to finalize your lineup. The `today` command is a shortcut for `day` with today's date.

```bash
# Standouts: yesterday's top performers across all league teams
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py standouts [--date YYYY-MM-DD] [--min-points N] [--count N]
```

Fetches daily player stats for all rostered players across every team in the league and identifies standout performances. Output is split into two sections:
1. **Top Performers** — players in active lineup slots who scored the most fantasy points
2. **Left on the Bench** — benched players with notable performances (points that didn't count)

Each player shows their fantasy points, key stat line, and achievement badges (e.g., "Multi-HR", "10+ K", "Gem", "CGSO"). Defaults to yesterday; use `--date` for a specific date.

```bash
# Lineup check: verify active players are in confirmed MLB lineups
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py lineup-check
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py lineup-check --date 2026-04-01
```

Cross-references active fantasy roster players against confirmed MLB batting lineups (from MLB Stats API `hydrate=lineups`). Flags position players who are in a starting fantasy slot but NOT in their team's confirmed real-life lineup (e.g., scratched, resting, benched vs lefty/righty). Pitchers are excluded (they don't appear in batting lineups). Players whose team's lineup hasn't been posted are NOT flagged — only players whose lineup IS posted and who are absent. Lineups are typically posted 1-3 hours before game time.

```bash
# Optimize: smart roster analysis with suggestions
python3 /home/claw/.openclaw/workspace/skills/yahoo-fantasy-baseball/yahoo-fantasy-baseball.py optimize
```

Three analysis categories:
1. **Lineup changes** — optimal batter assignment via constraint solver (position-aware, fills restrictive slots before UTIL). Outputs grouped swap instructions showing who starts (from bench), who gets benched, and any intermediate position reshuffles needed within that chain (e.g., a UTIL player sliding to 1B to make room). Pure position shuffles among active slots (without bench involvement) are omitted. Also checks confirmed MLB batting lineups — players confirmed not in their team's lineup are treated as unavailable (score 0) and will be moved to bench. Players whose games have already started are locked in place (Yahoo locks roster slots at first pitch) and excluded from the solver.
2. **Pitcher rotation** — priority-based pitcher slot optimization with swap suggestions. Relief pitchers whose teams are playing today are prioritized over non-starting SPs or pitchers whose teams are off. Probable starters get highest priority. Outputs grouped swap instructions (same format as batter swaps). Locked games are excluded.
3. **IL management** — players with IL designations (IL, IL10, IL15, IL60) not in IL slots, cleared players still in IL. DTD players are excluded since Yahoo does not allow moving them to IL.

Each move includes team, opponent, score, and (when set) Yahoo injury status (e.g. `DTD`, `IL10`) inline in the parenthetical. If a player suggested to *start* is `DTD`, a `⚠️ Day-to-day — confirm in lineup before locking.` caution is rendered beneath the line — the optimizer scores ignore status, so a higher-scoring DTD player can still surface as a swap recommendation. Moves to BN may include a `reason` indicator:
- `⚠️` — player not in confirmed MLB lineup (urgent — they won't play)
- `🔒` — player's game has already started (locked by Yahoo)
- `📅` — player's team is off today

In `--format json`, every entry in `swap_groups[].start`, `swap_groups[].bench`, `swap_groups[].reshuffle` (and the pitcher equivalents) carries a `status` field — empty string when the player has no Yahoo status. The flat `moves[]` and `pitcher_moves[]` arrays mirror the text view: they include only moves that are part of a bench-involving swap group (each tagged with a `swap_group` index). Pure active↔active reshuffles that are omitted from the text output are also omitted from JSON.

**Early-season preseason rank blending:** The optimizer blends Yahoo's preseason overall rank (OR) into player scores during the first weeks of the season, when current-year stats are too small a sample to be reliable. The blending schedule:
- **Weeks 1–2**: Full weight — preseason rank contributes up to 15 bonus points (rank 1 gets the max, last-ranked gets 0)
- **Weeks 3–6**: Linear taper — preseason influence decreases by ~20% per week
- **Week 7+**: Zero weight — scoring is based entirely on current-season stats

This prevents the optimizer from overreacting to small early-season slumps (e.g., benching a star who went 0-for-8 in the first series). The preseason ranks are fetched via one additional Yahoo API call (`sort=OR, status=T`) per optimize run.

## Common Flags

| Flag | Description |
|------|-------------|
| `--league ID` | League ID (overrides config default) |
| `--team ID` | Team ID (overrides config/auto-detect) |
| `--season YEAR` | Season year (for historical data) |
| `--week N` | Scoring week number |
| `--date` | Specific date — accepts MM/DD/YYYY, M/D/YYYY, MM-DD-YYYY, or YYYY-MM-DD (roster, day commands) |
| `--format text\|json\|discord` | Output format (default: text) |
| `--status FA\|A\|T\|W\|ALL` | Player status filter: FA (free agents), A (available=FA+W), T (taken), W (waivers), ALL (every player) |
| `--sort OR\|AR\|PTS\|NAME\|{stat}` | Sort order: OR = overall/preseason rank (default), AR = actual/current rank, PTS = points, NAME = alphabetical, or stat abbreviation. See stat sort reference below |
| `--sort-type season\|lastweek\|lastmonth` | Sort period (used with --sort) |
| `--stat-season YEAR` | Season year for stat columns (auto-detects: falls back to previous year if league hasn't started) |
| `--since 3d\|1w\|24h\|2w` | Filter transactions by time window (h=hours, d=days, w=weeks, m=months) |

### Sort Reference

Built-in sort modes:

| Value | Description |
|-------|-------------|
| `OR` | Overall Rank (preseason/projected) |
| `AR` | Actual Rank (by real performance) |
| `PTS` | Fantasy Points |
| `NAME` | Alphabetical |

Batting stats:

| Abbrev | Description |
|--------|-------------|
| `R` | Runs |
| `H` | Hits |
| `1B` | Singles |
| `2B` | Doubles |
| `3B` | Triples |
| `HR` | Home Runs |
| `RBI` | Runs Batted In |
| `SB` | Stolen Bases |
| `BB` | Walks |
| `K` | Strikeouts |
| `AVG` | Batting Average |
| `OBP` | On-base Percentage |
| `SLG` | Slugging Percentage |
| `OPS` | On-base + Slugging |
| `AB` | At Bats |
| `PA` | Plate Appearances |
| `TB` | Total Bases |
| `XBH` | Extra Base Hits |

Pitching stats:

| Abbrev | Description |
|--------|-------------|
| `W` | Wins |
| `L` | Losses |
| `SV` | Saves |
| `HLD` | Holds |
| `SV+H` | Saves + Holds |
| `BSV` | Blown Saves |
| `ERA` | Earned Run Average |
| `WHIP` | Walks + Hits per Inning Pitched |
| `IP` | Innings Pitched |
| `QS` | Quality Starts |
| `K9` | Strikeouts per 9 Innings |
| `BB9` | Walks per 9 Innings |

## Output Format

### Text (Default)

**roster:**

```
Roster — Team Name
Name                      Pos          Slot  Team   Status
----------------------------------------------------------
Aaron Judge               OF,Util      OF    NYY
Mookie Betts              SS,OF,Util   SS    LAD
Zack Wheeler              SP           IL    PHI    IL-60
```

**today / day:**

```
Today — Team Name
  First pitch: 1:10 PM

  ACTIVE (team playing today) (8)
    Aaron Judge            OF,Util        NYY  vs BOS 7:05 PM
    Gerrit Cole            SP             NYY  vs BOS 7:05 PM  [PROBABLE STARTER]

  NOT PLAYING (team off today) (3)
    Mookie Betts           SS,OF,Util     LAD

  BENCH (3)
    Jake Burger            3B,1B,Util     MIA  at ATL 1:10 PM

  INJURED LIST (1)
    Zack Wheeler           SP             PHI                   (IL-60)
```

**optimize:**

```
Roster Optimization Suggestions
==================================================

  LINEUP CHANGES (2 swaps)

    Swap 1 — 3B
      ▶ Start Jake Burger (MIA vs ATL, score: 18.3)
      ▼ Bench Josh Smith (TEX vs SEA, score: 9.2)
        ⚠️  not in confirmed MLB lineup

    Swap 2 — SS / UTIL
      ▶ Start Willy Adames at SS (SF vs PHI, score: 35.0)
      ↔ Move Mookie Betts from SS → UTIL
      ▼ Bench Tyler Fitzgerald (SF, score: 12.0)
        📅  team off today

  PITCHER ROTATION (1 swap)

    Swap 1 — P
      ▶ Start Gerrit Cole (NYY vs BOS, score: 42.1) — probable starter today
      ▼ Bench Nathan Eovaldi (TEX vs SEA, score: 39.0)
        💡  not starting today

  IL MANAGEMENT (1 suggested)
    Move Zack Wheeler (IL-60) from SP slot to IL to free a roster spot.

Total: 4 suggestion(s)
```

Players on teams whose games are already in progress or finished are locked and excluded from optimization — they will not appear in the move list.

**scoreboard:**

```
League Scoreboard — Week 1
------------------------------------------------------------
  Clanker Killerz                  6  vs  4   1% AI 99% hot gas
                                    In progress

  Mossi Possi                      1  vs  7   Normal Men
                                    In progress
```

**transactions:**

```
Recent Transactions
------------------------------------------------------------
add | 1% AI 99% hot gas | Mar 25, 07:38 PM
  Add from Free Agent:Luis Castillo (SEA - SP)

add/drop | 1% AI 99% hot gas | Mar 25, 04:14 AM
  Add from Waivers:   Josh Smith (TEX - 1B,3B,SS,OF)
  Drop:               Luis Robert Jr. (NYM - OF)
```

### JSON

All commands support `--format json` for structured output.

### Discord

All commands support `--format discord` which wraps text output in code blocks.

## Output Fields

- **name** — Player's full name
- **player_id** — Yahoo player ID (numeric)
- **positions** — Eligible fantasy positions (e.g., OF, SP, Util)
- **selected_position** — Current lineup slot
- **team** — Real MLB team abbreviation
- **status** — Injury designation (IL, IL-60, DTD, etc.)
- **game_time** — Game start time in local timezone (today/day commands)
- **first_pitch** — Earliest game start time across all games (today/day commands, JSON top-level)
- **percent_owned** — Ownership percentage (free agents)
- **player_position** — Display position (draft results)

## Limitations

- **Rate limits**: Yahoo enforces API rate limits. Avoid rapid-fire requests.
- **Season scope**: Data is scoped to the configured season. Use `--season` for historical data.
- **OAuth tokens**: Tokens auto-refresh but may eventually expire, requiring re-authentication via `auth`.
- **MLB schedule**: The `today`, `day`, `optimize`, and `lineup-check` commands use the MLB Stats API for schedule data (off days, probable pitchers, confirmed batting lineups). This data is not available from the Yahoo Fantasy API.

## Credential Storage

**Preferred: Environment variables.** Set `YAHOO_CONSUMER_KEY` and `YAHOO_CONSUMER_SECRET` via OpenClaw config or your shell environment. The skill will use these automatically — no need to run `auth`. Note: credentials are still written to `oauth2.json` on disk because the underlying `yahoo_oauth` library requires a file for token management. File permissions are set to 0600 on Unix.

**Alternative: Interactive setup.** Run the `auth` command to enter credentials interactively. Tokens are stored in `~/.openclaw/credentials/yahoo-fantasy/`:
- `oauth2.json` — OAuth consumer key/secret and tokens (managed by yahoo_oauth, file permissions set to 0600 on Unix)
- `yahoo-fantasy.json` — Default league_id, team_id, season

Legacy YFPY `.env` credentials are auto-migrated to `oauth2.json` on first use.

## Notes

- Data is sourced from the Yahoo Fantasy Sports API via the [yahoo-fantasy-api](https://github.com/spilchen/yahoo_fantasy_api) library.
- MLB schedule and probable pitcher data comes from the [MLB Stats API](https://statsapi.mlb.com/) (stdlib only, no dependencies).
- Run `--setup` to create a local venv at `.deps/` and install dependencies before first use.
- Auto-detect identifies your team using `league.team_key()`. If detection fails, use `config --team <ID>` to set it manually.
