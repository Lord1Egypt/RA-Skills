---
name: topyappers
description: TopYappers — social media intelligence for AI agents. Discover viral TikTok content, search 30M+ creators across TikTok/Instagram/YouTube, and track trending song charts. Use when the user asks about influencers, creators, viral content, trending songs, or social media data.
---

# TopYappers MCP

Social media intelligence for AI agents. Access viral content discovery, influencer search across TikTok, Instagram & YouTube, and trending song charts — all through a single MCP connection.

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

## Available Skills

This package includes 4 specialized skills for each API domain:

- **[find-creators](find-creators/SKILL.md)** — Search 30M+ creators with 20+ filters (category, niche, followers, engagement, country, platform). Free search + paid profiles.
- **[find-viral-content](find-viral-content/SKILL.md)** — Discover viral TikTok posts by category, country, virality score, date range, music, and hooks.
- **[search-videos](search-videos/SKILL.md)** — Find videos by engagement metrics, hashtags, text search, and sort by views/likes/shares.
- **[trending-songs](trending-songs/SKILL.md)** — Chart rankings, new entries, song search, history tracking, and week-over-week comparisons across 44 countries.

## 11 MCP Tools

| Tool | Description | Cost |
|------|-------------|------|
| `search_creators` | Search influencers with 20+ filters | **Free** |
| `get_creator_profiles` | Full profiles — followers, engagement, email, bio, niches | 1 credit/creator |
| `search_viral_content` | Viral TikTok posts by category, country, virality score | 1 credit/result |
| `search_videos` | Videos by engagement, hashtags, text | 1 credit/video |
| `get_song_rankings` | Country or global chart rankings | 10 credits |
| `get_new_song_entries` | Newly charting songs | 10 credits |
| `search_songs` | Search by title/artist | 10 credits |
| `get_song_history` | Song chart performance over time | 10 credits |
| `compare_song_rankings` | Compare charts between two weeks | 10 credits |
| `get_song_countries` | Available countries for song data | 10 credits |
| `get_song_weeks` | Available weeks for a country | 10 credits |

## Quick Reference

### Country format matters
- **Creators & viral content** → full names: `"United States"`, `"France"`
- **Song tools** → country codes: `"US"`, `"FR"`, `"GB"`

### nichesToPromote is the primary creator discovery tool
The most powerful filter. It uses AI-analyzed niche data that is very granular — specific products (`calorie counter`, `standing desk`), use cases (`meal prep`, `budget travel`), audiences (`new moms`, `small business owners`), and tools (`ChatGPT`, `Notion`). Be specific and creative.

### Run 5+ niche searches per query
`nichesToPromote`, `promotedProducts`, and `hashtags` use AND logic when comma-separated — never pass multiple values. Instead, run **at least 5 searches with different keywords** from different angles, then merge and deduplicate. Since search is free, there's no cost.

### Credit-efficient creator workflow
1. `search_creators` (free) with `nichesToPromote` → run 5+ searches with different keywords
2. Deduplicate all userIds across searches
3. `get_creator_profiles` (1 credit each) → only for the ones you need

### Virality score
Views ÷ followers, normalized 0–1. Use `0.3+` for quality, `0.5+` for highly viral, `0.7+` for breakout content.

### Song week format
ISO format: `YYYY-Www` (e.g. `"2026-W04"`). Use `get_song_weeks` to discover available weeks.

## Rate Limits

60 requests per minute per API key. HTTP 429 responses include `retryAfter` in seconds.

## Links

- [TopYappers Platform](https://www.topyappers.com)
- [API Documentation](https://docs.topyappers.com)
- [MCP Documentation](https://www.topyappers.com/tools/mcp)
- [GitHub](https://github.com/topyappers/topyappers-mcp)
