---
name: statsfm
description: Comprehensive Music data tool for Spotify and Apple Music, powered by the stats.fm API. Look up album tracklists, artist discographies, and global charts without an account. With a stats.fm username, query personal Spotify listening history, play counts, top artists/tracks/albums, monthly breakdowns, and currently playing.
---

# stats.fm Skill

Query Spotify listening data through the stats.fm API. Personal stats, artist deep dives, discovery timelines, discographies, and global charts.

**Script:** `scripts/statsfm.py` (Python 3.6+, stdlib only)

## Setup

Check memory for a stats.fm username. If you don't have one, ask — all personal commands need `--user USERNAME` (`-u`). Public commands (search, album, artist-albums, charts) work without a username.

## How to Be Good at This

This skill is worthless if you call one command and dump the output. Music is personal. Your job is to investigate, find the story in the data, and tell it back. You're a music analyst with unlimited API calls — act like it.

### Core principles

**1. Never stop at one call.** ALWAYS check recent first (7d or 4w). Lifetime alone is accumulation, not what's happening now. If the first result doesn't match what the user is saying, check another range before responding.

**2. `artist-history` first for any single-artist question.** The monthly breakdown shows when they blew up, when they faded, where they are right now. `top artists` gives you a rank. `artist-history` gives you the arc. Never answer a single-artist question with only `top artists` output.

**3. Always check total streams as context.** Raw play counts mean nothing without the denominator. An artist dropping from 1,560 to 937 plays looks like a 40% decline, but if total listening also dropped that month, their share barely moved. Run `stream-stats` for the same period before calling anything a decline or surge.

**4. Go wide, then narrow.** Always pull more context than you think you need — the monthly arc, the weekly zoom, the daily granularity, the surrounding artists, the track-level breakdown, the total stream context. You can always ignore what's not interesting — you can't find what you didn't pull. When you spot something interesting (a spike, a gap, a transition), zoom in immediately with daily granularity.

**5. First play ≠ fandom.** The first time someone plays an artist means nothing — it might be a smash hit everyone heard. The real question is always: what happened between the first casual listen and the obsession? Investigate the gap. Find the bridge song. Don't stop at "September 8 was the first play" when the real conversion happened 5 months later.

> **Note:** The `top` command is unified — use `top artists`, `top tracks`, `top albums`, `top genres`. For drill-downs, use `top tracks --from-artist ID` or `top tracks --from-album ID`. Charts are also unified: `charts tracks`, `charts artists`, `charts albums`.

### How to investigate

When someone asks about an artist, a phase, or a discovery moment, think like an investigator:

**Start broad:** `artist-history` (defaults to lifetime) gives the monthly arc. Where are the spikes? Where are the gaps? Where did it start, peak, and (if applicable) decline?

**Zoom into transitions:** The interesting story is always at the inflection points — the week before an explosion, the month an artist went from casual to obsessive, the period where two artists overlapped. Use `--granularity daily` on these windows.

**Get the full context:** What else was playing that day? (`top artists`, `top tracks` for the same date range.) What tracks appeared as breadcrumbs before the explosion? (`top tracks --from-artist` for the pre-explosion period.) How big was the total pie? (`stream-stats` for the same period.)

**Track the breadcrumbs:** Artists don't go from 0 to obsession overnight. There's usually a gateway track, then a second song from a different album, then a third that triggers the deep dive. Map these out with `top tracks --from-artist` across the transition period.

**Calculate share when comparing periods.** Artist plays ÷ total streams = share. Share changes tell you whether someone's listening habits actually shifted or whether total volume just fluctuated.

### Workflow patterns

**"Tell me about my [artist] phase"** — the deep dive
1. `artist-history` lifetime → find the arc (start, peak, current)
2. `artist-history` this week and this month → where are they right now?
3. `artist-history` with weekly granularity on the hot period → zoom in on the peak
4. `top tracks --from-artist` lifetime → which songs define the phase
5. `top tracks --from-artist` this month → which songs are active now vs. then?
6. `top albums --from-artist` → album-level view
7. `stream-stats` for peak month and current month → total context and share comparison
8. `top artists` for peak month → who else was competing for attention?

*Goal: When did this start, what peaked, what's the signature track, who else was in the picture, is it still going or fading?*

**"When did I discover [artist]?"** — the origin story
1. `artist-history` lifetime → find first appearance AND explosion month
2. `artist-history` daily granularity on the transition period → find the exact conversion day
3. `top tracks --from-artist` for pre-explosion period → what tracks were breadcrumbs
4. `top tracks --from-artist` for explosion day/week → what track triggered it
5. `top tracks --from-artist` this week → what are they playing now vs. the origin?
6. `top artists` for the first day → what world were they listening in when this artist appeared?
7. `top tracks` for the explosion day → full picture of the conversion moment
8. `track-history` on the gateway track lifetime → how did it spread from there?
9. `stream-stats` for the transition month → total listening context

*Goal: Find the gateway track, the bridge track, the conversion moment, and what triggered the deep dive. The gap between first listen and obsession IS the story.*

**"What's my [artist] breakdown look like this year?"** — the status check
1. `artist-history` for this year → monthly totals
2. `artist-history` this week and this month → current trajectory
3. `top tracks --from-artist` for this year → current favorites
4. `top tracks --from-artist` this week → what's actually playing right now?
5. `artist-history` lifetime → compare to history
6. `stream-stats` for this month and same month last year → share comparison across time

*Goal: Where does this year rank vs. history? Is the artist's share growing, stable, or shrinking?*

**"How do I listen to [album]?"** — the album autopsy
1. `album` → full tracklist
2. `album-history` lifetime → total plays and arc
3. `album-history` this month → is it still active?
4. `top tracks --from-album` lifetime → all-time track ranking
5. `top tracks --from-album` this month → has the favorite track shifted?

*Goal: Which tracks carry the album? Front-to-back or cherry-pick? Still active or nostalgia?*

**"What have I been into lately?"** — the snapshot
1. `top artists` this week → right now
2. `top artists` this month → broader view
3. `top artists` lifetime → for comparison only
4. `now-playing` → anchor to what's playing right now
5. `stream-stats` this week and this month → total volume context and trend

*Goal: Paint the current moment. What's dominating? What's surprising? Who's rising, who's falling?*

### Voice and tone

- **Be specific.** "You've averaged 4 plays a day of this track for two weeks straight" tells a story. "You really like this artist" tells nothing.
- **Notice patterns.** Spikes, drop-offs, seasonal rhythms, transitions — call them out.
- **Numbers are scaffolding.** Don't list every month. Pick the interesting ones and weave them into observations.
- **Compare things.** A number alone means nothing. 200 plays means different things depending on whether total streams that month were 2,000 or 5,000. Always contextualize.
- **Editorialize lightly.** You're having a music conversation, not filing a report.
- **Don't narrate your process.** Never say "I'll now run artist-history." Just do it.

## Time Range Translations

| User says | You use |
|-----------|---------|
| "this year" / "in 2025" | `--start 2025 --end 2026` |
| "last year" | `--start 2024 --end 2025` |
| "this month" | `--start 2025-03 --end 2025-04` (adjust to current month) |
| "last summer" | `--start 2025-06 --end 2025-09` |
| "lately" / "recently" | `--range 30d` (and maybe compare to `--range all`) |
| "ever" / "all time" | `--range all` |
| "this week" | `--range 7d` |
| "when did I start" | `--range all` then read the monthly breakdown |

## Edge Cases

- **Empty results?** Retry with `--range all` automatically. If still empty, the profile might be private.
- **Free (non-Plus) users:** Play counts won't appear in top lists. Rankings and monthly breakdowns still work — lead with those.
- **Rate limiting:** Don't hold back. Deep dives take as many calls as they take. That's what this skill is for.
- **Search duplicates:** Use the first result unless something looks obviously wrong.
- **No username in memory:** Ask once, remember it.

---

## CLI Reference

Everything below is command-level documentation. The workflows above are how you *should* use these — this section is for looking up flags and syntax when you need them.

### Command Syntax

All commands: `./statsfm.py <command> [args] [flags]`

Global flags for all personal commands: `--user USERNAME` / `-u USERNAME`

### Commands

**Profile & Activity**

| Command | Description |
|---------|-------------|
| `profile` | Username, pronouns, bio, Plus status, Spotify sync info |
| `now-playing` / `np` | Currently playing track |
| `recent` | Recently played tracks (includes now-playing at top if active) |
| `stream-stats` | Overall summary: total streams, time, averages, unique counts |

**Your Top Lists**

| Command | Description | Key flags |
|---------|-------------|-----------|
| `top artists` | Most played artists | `--range`, `--start/--end`, `--limit` |
| `top tracks` | Most played tracks | `--range`, `--start/--end`, `--limit` |
| `top albums` | Most played albums | `--range`, `--start/--end`, `--limit` |
| `top genres` | Top genres | `--range`, `--start/--end`, `--limit` |

**History (with breakdowns)**

| Command | Description | Key flags |
|---------|-------------|-----------|
| `artist-history <id>` | Play count, time, breakdown for an artist | `--start/--end`, `--granularity` |
| `track-history <id>` | Play count, time, breakdown for a track | `--start/--end`, `--granularity` |
| `album-history <id>` | Play count, time, breakdown for an album | `--start/--end`, `--granularity` |
| `listening-history` | Total listening breakdown over time | `--start/--end`, `--granularity` |

> **Note:** History commands do NOT support `--range`. Use `--start/--end` for custom windows, or omit both to get lifetime. `--range` produces partial-month data at boundaries that looks misleadingly low.

**Lookups (no account needed)**

| Command | Description | Key flags |
|---------|-------------|-----------|
| `search <query>` | Find artists, tracks, or albums | `--type artist\|track\|album` |
| `artist <id>` | Artist info, genres, popularity, discography | `--type album\|single\|all`, `--limit` |
| `track <id>` | Track info: name, all artists (with IDs), album (with ID), duration | |
| `album <id>` | Album info and full tracklist | |
| `artist-albums <id>` | Discography grouped by type, newest first | `--type album\|single\|all`, `--limit` |

**Drill-Down (your stats within an artist/album)**

| Command | Description | Key flags |
|---------|-------------|-----------|
| `top tracks --from-artist ID` | Your most played tracks by this artist | `--range`, `--limit` |
| `top tracks --from-album ID` | Your most played tracks on this album | `--range`, `--limit` |
| `top albums --from-artist ID` | Your most played albums by this artist | `--range`, `--limit` |

**Discovery**

| Command | Description | Key flags |
|---------|-------------|-----------|
| `first-listen <id>` / `first` | Show first N streams for an artist, track, or album | `--type artist\|track\|album`, `--limit` |

**Global Charts (no account needed)**

| Command | Description | Key flags |
|---------|-------------|-----------|
| `charts tracks` | Global top tracks | `--range`, `--limit` |
| `charts artists` | Global top artists | `--range`, `--limit` |
| `charts albums` | Global top albums | `--range`, `--limit` |

### Date Range Flags

**Predefined:** `--range today`, `1d`, `4w` (default), `6m`, `all`

**Duration:** `--range 7d`, `14d`, `30d`, `90d`

**Custom:** `--start YYYY[-MM[-DD]]` and `--end YYYY[-MM[-DD]]`

### Granularity

`--granularity monthly` (default) | `weekly` | `daily`

Works with `artist-history`, `track-history`, `album-history`.

### Other Flags

| Flag | Description |
|------|-------------|
| `--limit N` / `-l N` | Limit results (default: 15) |

### Finding IDs

```bash
./statsfm.py search "sabrina carpenter" --type artist
# → [22369] Sabrina Carpenter [pop]

./statsfm.py search "espresso" --type track
# → [188745898] Espresso by Sabrina Carpenter

./statsfm.py search "short n sweet" --type album
# → [56735245] Short n' Sweet by Sabrina Carpenter
```

### Error Handling

| Scenario | Output | Auto-fix |
|----------|--------|----------|
| No user set | `Error: No user specified.` | Ask for username, store in memory |
| API error (4xx/5xx) | `API Error (code): message` | Check if profile is public, ID is valid |
| Empty results | No output | Retry with `--range all` |
| Plus-only data | `[Plus required]` inline | Work with what's available, don't dwell on it |

### API Info

- **Base URL:** `https://api.stats.fm/api/v1`
- **Auth:** None for public profiles
- **Response format:** JSON with `item`/`items` wrapper

### References
- GitHub: [statsfm/statsfm-cli](https://github.com/Beat-YT/statsfm-cli)
- API Endpoints: [references/api.md](references/api.md)
- Official JS Client: [statsfm/statsfm.js](https://github.com/statsfm/statsfm.js)
