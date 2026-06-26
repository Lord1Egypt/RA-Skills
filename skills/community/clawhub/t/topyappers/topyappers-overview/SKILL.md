---
name: topyappers
description: TopYappers social media intelligence — overview of all available MCP tools for discovering viral content, searching creators/influencers, and tracking trending songs across TikTok, Instagram, and YouTube. Use when the user asks about TopYappers, what tools are available, how the API works, or needs help choosing the right tool.
---

# TopYappers MCP — Overview

You have access to the TopYappers API through MCP. It provides **social media intelligence** across three domains.

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

## Domains

### 1. Viral Content Discovery
Find trending TikTok posts filtered by category, country, virality score, date range, music/sound, and opening hooks.

**Tool:** `search_viral_content` — 1 credit per result

### 2. Creators & Influencers
Search 30M+ creators across TikTok, Instagram, and YouTube using 20+ filters. Two-step workflow to save credits.

**Tools:**
- `search_creators` — **FREE** (returns IDs only)
- `get_creator_profiles` — 1 credit per creator (returns full profiles)

### 3. Trending Songs
Weekly chart rankings, new entries, song search, history, and week-over-week comparisons.

**Tools:** `get_song_rankings`, `get_new_song_entries`, `search_songs`, `get_song_history`, `compare_song_rankings`, `get_song_countries`, `get_song_weeks` — 10 credits each

## Credit Cost Summary

| Tool | Cost |
|------|------|
| `search_creators` | **Free** |
| `get_creator_profiles` | 1 credit per creator |
| `search_viral_content` | 1 credit per result |
| `search_videos` | 1 credit per video |
| All song tools | 10 credits per request |

## Critical Rules

### Country format matters
- **Creators and viral content** use full country names: `"United States"`, `"France"`
- **Song tools** use country codes: `"US"`, `"FR"`, `"GB"`

### nichesToPromote is the primary creator discovery tool
The most powerful filter. It searches AI-analyzed niche data that is very granular — it understands specific products (`calorie counter`, `standing desk`), use cases (`meal prep`, `budget travel`), audiences (`new moms`, `small business owners`), and tools (`ChatGPT`, `Notion`). Be specific and creative with search terms.

### Run 5+ niche searches per query
`nichesToPromote`, `promotedProducts`, and `hashtags` use **AND logic** when comma-separated — never pass multiple values. Instead, run **at least 5 searches with different keywords** describing the target from different angles, then merge and deduplicate results. Since search is free, there's no cost.

### Be credit-efficient
- Start with `search_creators` (free) before calling `get_creator_profiles`
- Use smaller `pageSize` / `perPage` when exploring
- Only fetch profiles for creators that match your criteria

## Available Categories (57)

Arts, Automotive, Beauty & Personal Care, Books & Literature, Business, Finance, Career & Jobs, Collectibles & Hobbies, Community, Ecommerce, Crafts & DIY, Culture, Education, Technology, Entertainment, Environment, Family, Parenting, Fashion, Film, Fitness, Health, Food, Gaming, Gardening & Agriculture, History, Home, Humor, Law, Government, Lifestyle, Marketing, Mental Health, Music, News & Media, Outdoors, Nature, Pets, Animals, Philosophy, Spirituality, Photography, Videography, Politics, Relationships, Religion, Science, Self-Improvement, Shopping, Social Media, Social Issues & Activism, Sports, Travel, Vehicles & Transportation, Virtual Reality, Weapons & Defense, Writing, Kids

## Platforms

`tiktok`, `instagram`, `youtube`

## Rate Limits

60 requests per minute per API key. HTTP 429 responses include `retryAfter` in seconds.
