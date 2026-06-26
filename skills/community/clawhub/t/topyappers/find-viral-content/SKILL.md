---
name: find-viral-content
description: Discover viral TikTok content using the TopYappers API. Use when the user wants to find trending posts, viral videos, content going viral in a category or country, analyze virality patterns, find content by music/sound, or discover hooks that drive engagement.
argument-hint: "[category, country, or description of viral content to find]"
---

# Discover Viral Content

Find and analyze viral TikTok posts. Filter by category, country, view counts, virality score, date range, music/sound, and opening hooks.

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

**Tool:** `search_viral_content`
**Cost:** 1 credit per returned result

## Parameters

All parameters are optional. Combine multiple filters for targeted results.

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `categories` | string[] | Content categories | `["Fitness", "Food"]` |
| `countries` | string[] | Full country names | `["United States", "France"]` |
| `viewsMin` | integer | Minimum views | `100000` |
| `viewsMax` | integer | Maximum views | `10000000` |
| `viralityScoreMin` | number | Minimum virality score (0–1) | `0.5` |
| `viralityScoreMax` | number | Maximum virality score (0–1) | `1.0` |
| `followersMin` | integer | Minimum creator followers | `1000` |
| `followersMax` | integer | Maximum creator followers | `1000000` |
| `dateCreatedFrom` | string | Posts on or after (YYYY-MM-DD) | `"2026-01-01"` |
| `dateCreatedTo` | string | Posts on or before (YYYY-MM-DD) | `"2026-03-23"` |
| `musicTitle` | string | Music/sound title (partial match) | `"original sound"` |
| `hook` | string | Video opening hook text (partial match) | `"wait for it"` |
| `page` | integer | Page number (default: 1) | `1` |
| `pageSize` | integer | Results per page (default: 12, max: 100) | `12` |

## Understanding Virality Score

The virality score is **views ÷ followers**, normalized to 0–1. It measures how well content performed relative to the creator's audience size.

| Score Range | Meaning |
|-------------|---------|
| 0.0 – 0.2 | Normal performance |
| 0.2 – 0.5 | Above average — good engagement |
| 0.5 – 0.8 | Highly viral — significant reach beyond followers |
| 0.8 – 1.0 | Extremely viral — massive breakout content |

**Key insight:** A video with 1M views from a creator with 10K followers (score ~1.0) is far more impressive than 1M views from someone with 10M followers (score ~0.1). The score captures true virality, not just raw view counts.

**Recommended thresholds:**
- `viralityScoreMin: 0.3` — quality viral content
- `viralityScoreMin: 0.5` — highly viral only
- `viralityScoreMin: 0.7` — extreme breakout content

## Response Fields

Each result includes:
- `id` — post identifier
- `videoUrl`, `thumbnailUrl` — media URLs
- `caption` — post caption/description
- `views`, `likes`, `comments`, `shares` — engagement metrics
- `viralityScore` — virality score (0–1)
- `followers` — creator's follower count
- `category` — content category
- `country` — origin country
- `musicTitle` — sound/music used
- `creatorUsername` — creator handle
- `hook` — opening hook text
- `createdAt` — post creation timestamp

## Important Notes

- **Country names:** Use full names like `"United States"`, NOT codes like `"US"`
- **Cost control:** Use smaller `pageSize` when exploring. Default is 12, max is 100
- **Categories:** Must use exact enum values like `"Beauty & Personal Care"`, `"Crafts & DIY"`

## Example Workflows

### Find viral fitness content from the US
```
search_viral_content with:
  categories: ["Fitness"]
  countries: ["United States"]
  viralityScoreMin: 0.5
  pageSize: 10
```

### Find viral posts using a trending sound
```
search_viral_content with:
  musicTitle: "original sound"
  viewsMin: 500000
  pageSize: 20
```

### Find breakout content from micro-creators
```
search_viral_content with:
  followersMax: 50000
  viralityScoreMin: 0.7
  viewsMin: 100000
  pageSize: 10
```

### Find viral content with strong hooks
```
search_viral_content with:
  hook: "wait for it"
  viralityScoreMin: 0.3
  pageSize: 12
```

### Find recent viral content in a country
```
search_viral_content with:
  countries: ["United Kingdom"]
  dateCreatedFrom: "2026-01-01"
  viewsMin: 100000
  pageSize: 15
```

### Analyze viral patterns in a niche
1. Search with `categories: ["Beauty & Personal Care"]`, `viralityScoreMin: 0.5`
2. Analyze the results for common hooks, sounds, and engagement patterns
3. Identify what makes content go viral in this category

### Compare viral content across countries
1. Search with `countries: ["United States"]`, `viralityScoreMin: 0.5`
2. Search with `countries: ["United Kingdom"]`, `viralityScoreMin: 0.5`
3. Compare trends, categories, and engagement differences

## Available Categories

Arts, Automotive, Beauty & Personal Care, Books & Literature, Business, Finance, Career & Jobs, Collectibles & Hobbies, Community, Ecommerce, Crafts & DIY, Culture, Education, Technology, Entertainment, Environment, Family, Parenting, Fashion, Film, Fitness, Health, Food, Gaming, Gardening & Agriculture, History, Home, Humor, Law, Government, Lifestyle, Marketing, Mental Health, Music, News & Media, Outdoors, Nature, Pets, Animals, Philosophy, Spirituality, Photography, Videography, Politics, Relationships, Religion, Science, Self-Improvement, Shopping, Social Media, Social Issues & Activism, Sports, Travel, Vehicles & Transportation, Virtual Reality, Weapons & Defense, Writing, Kids
