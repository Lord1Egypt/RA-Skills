---
name: trending-songs
description: Access trending song charts, track new entries, search songs, view historical performance, and compare week-over-week rankings using the TopYappers API. Use when the user asks about trending music, viral sounds, chart rankings, song performance, or wants a music trends report.
argument-hint: "[country code, song name, or description of what to find]"
---

# Trending Songs

Access trending songs data, chart rankings, and historical performance across countries. All song tools cost **10 credits per request**.

## Setup

**MCP Endpoint:** `https://mcp.topyappers.com`
**Transport:** HTTP
**Auth:** Bearer token in the `Authorization` header

Get an API key at [topyappers.com/profile](https://www.topyappers.com/profile).

### Claude Code
```
claude mcp add --transport http topyappers https://mcp.topyappers.com \
  --header "Authorization: Bearer YOUR_API_KEY"
```

### .mcp.json / Cursor / Claude Desktop
```json
{
  "mcpServers": {
    "topyappers": {
      "type": "http",
      "url": "https://mcp.topyappers.com",
      "headers": {
        "Authorization": "Bearer YOUR_API_KEY"
      }
    }
  }
}
```

## CRITICAL: Country Codes (Not Names)

Song tools use **country codes** like `"US"`, `"GB"`, `"FR"` — NOT full names like `"United States"`.

Use `get_song_countries` to discover all valid codes.

## CRITICAL: Week Format

Weeks use ISO format: `YYYY-Www`
- `YYYY` — four-digit year
- `W` — literal letter "W"
- `ww` — two-digit week number (01–53)

Examples: `"2026-W01"`, `"2026-W04"`, `"2025-W52"`

Use `get_song_weeks` with a country code to discover available weeks.

## Tools

### get_song_rankings
Get trending song chart rankings for a country or globally.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | string | Country code (e.g. `"US"`, `"GB"`). Omit for global. |
| `global_rankings` | boolean | Set `true` for worldwide rankings |
| `week` | string | Week in ISO format. Omit for latest data. |

Response includes for each song: `id`, `title`, `artist`, `rank`, `previous_rank`, `weeks_on_chart`, `peak_rank`

### get_new_song_entries
Songs that newly entered the chart for a country.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | string | **Required.** Country code |

### search_songs
Search for songs by title or artist name.

| Parameter | Type | Description |
|-----------|------|-------------|
| `q` | string | **Required.** Search query — song title or artist |

### get_song_history
Full chart performance history of a specific song over time.

| Parameter | Type | Description |
|-----------|------|-------------|
| `song_id` | string | **Required.** Song ID (from rankings or search) |
| `country_code` | string | **Required.** Country code |

### compare_song_rankings
Compare chart rankings between two different weeks.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country` | string | **Required.** Country code |
| `week1` | string | **Required.** First week (ISO format) |
| `week2` | string | **Required.** Second week (ISO format) |

### get_song_countries
Get all available countries and their codes. No parameters required.

### get_song_weeks
Get available weeks for a specific country.

| Parameter | Type | Description |
|-----------|------|-------------|
| `country_code` | string | **Required.** Country code |

## Example Workflows

### Get current trending songs in a country
```
get_song_rankings with:
  country: "US"
```
Omit `week` to get the latest data. Review top songs, ranks, and weeks on chart.

### See what's new on the charts
```
get_new_song_entries with:
  country: "US"
```
Shows songs that just entered the rankings — great for spotting emerging trends.

### Find a specific song
```
search_songs with:
  q: "Taylor Swift"
```
Returns matching songs with their IDs for further analysis.

### Track a song's chart history
1. `search_songs` with `q: "song name"` to find the `song_id`
2. `get_song_history` with `song_id` and `country_code: "US"`
3. See rank movement over weeks, peak rank, and total weeks on chart

### Analyze week-over-week chart movement
1. `get_song_weeks` with `country_code: "US"` to find available weeks
2. `compare_song_rankings` with the two most recent weeks
3. Identify biggest movers (climbers and fallers), new entries, and exits

### Generate a full trending music report
1. `get_song_rankings` with `country: "US"` — current top songs
2. `get_new_song_entries` with `country: "US"` — fresh entries
3. `compare_song_rankings` with two recent weeks — movement analysis
4. Compile insights: dominant artists, genre trends, risers, fallers, and predictions

### Compare charts across countries
1. `get_song_rankings` with `country: "US"`
2. `get_song_rankings` with `country: "GB"`
3. `get_song_rankings` with `country: "DE"`
4. Compare which songs are charting globally vs. locally

### Find the best week for a song
1. `get_song_history` with `song_id` and `country_code`
2. Analyze the history to find peak performance and total chart run

### Discover available data
1. `get_song_countries` — see all supported countries and codes
2. `get_song_weeks` with a specific country — see date range of available data
