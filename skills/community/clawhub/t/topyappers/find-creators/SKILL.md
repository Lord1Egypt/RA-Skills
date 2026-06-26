---
name: find-creators
description: Find influencers and creators across TikTok, Instagram, and YouTube using the TopYappers API. Use when the user wants to discover creators, find influencers for a campaign, search by niche, category, country, followers, engagement rate, promoted products, or any creator-related query.
argument-hint: "[niche or description of creators to find]"
---

# Find Creators & Influencers

Search 30M+ creators across TikTok, Instagram, and YouTube using a credit-efficient two-step workflow.

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

## Workflow

### Step 1: Search (FREE)
Call `search_creators` with filters. This returns **creator IDs only**, not full profiles. It's free, so run as many searches as needed.

### Step 2: Get Profiles (1 credit each)
Pass the collected `userIds` to `get_creator_profiles` to get full profiles with followers, engagement, email, bio, niches, promoted products, and more.

## Search Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `followersMin` | integer | Minimum followers | `10000` |
| `followersMax` | integer | Maximum followers | `1000000` |
| `averageViewsMin` | integer | Minimum average views per post | `5000` |
| `averageViewsMax` | integer | Maximum average views per post | `500000` |
| `engagementRateMin` | number | Minimum engagement rate (%) | `2.5` |
| `engagementRateMax` | number | Maximum engagement rate (%) | `10` |
| `age` | string | Age group, comma-separated | `"20-29,30-39"` |
| `gender` | string | `"male"` or `"female"` | `"female"` |
| `mainCategory` | string | Content category (use exact enum values) | `"Fashion"` |
| `subCategory` | string | Sub-category, free text | `"streetwear"` |
| `bio` | string | Keywords in creator's bio | `"tiktok shop"` |
| `promotedProducts` | string | Products creator promoted | `"beef tallow"` |
| `nichesToPromote` | string | AI-analyzed niches (free text) | `"skincare"` |
| `country` | string | Full country name | `"France"` |
| `source` | string | Platform | `"instagram"` |
| `username` | string | Creator handle | `"mrbeast"` |
| `language` | string | Content language (lowercase) | `"english"` |
| `hashtags` | string | Hashtags (AND match) | `"fitness"` |
| `emailExists` | boolean | Only creators with email | `true` |
| `email` | string | Find by exact email | `"john@example.com"` |
| `page` | integer | Page number (default: 1) | `1` |
| `perPage` | integer | Results per page (default: 10, max: 100) | `20` |

## Power Filters

### nichesToPromote — The Most Powerful Filter

**Start here for every creator search.** This searches AI-analyzed niche data for each creator. The analysis is very granular — it understands specific product types, use cases, and sub-niches, not just broad categories.

It's a free-text field, so be specific and creative with your queries.

#### CRITICAL: AND Matching — Run 5+ Searches

`nichesToPromote` uses **AND logic** when comma-separated. Never pass multiple values — always search **one keyword at a time** and combine results across multiple searches. Since search is free, run at least **5 different searches with different keywords** to cast the widest net.

#### Example: Finding creators for a calorie counting app
1. `nichesToPromote=calorie counter` → collect userIds
2. `nichesToPromote=calorie tracking` → collect userIds
3. `nichesToPromote=weight loss` → collect userIds
4. `nichesToPromote=meal prep` → collect userIds
5. `nichesToPromote=fitness nutrition` → collect userIds
6. Deduplicate the combined list
7. Call `get_creator_profiles` once with the merged IDs

#### Example: Finding creators for an AI tool
1. `nichesToPromote=ai tools` → collect userIds
2. `nichesToPromote=ChatGPT` → collect userIds
3. `nichesToPromote=productivity software` → collect userIds
4. `nichesToPromote=SaaS` → collect userIds
5. `nichesToPromote=tech reviews` → collect userIds
6. Deduplicate and get profiles

#### Example: Finding creators for a skincare brand
1. `nichesToPromote=skincare` → collect userIds
2. `nichesToPromote=beauty routine` → collect userIds
3. `nichesToPromote=skin health` → collect userIds
4. `nichesToPromote=anti aging` → collect userIds
5. `nichesToPromote=dermatology` → collect userIds
6. Deduplicate and get profiles

#### What makes good search terms

Think about how creators describe their content. The niche data is very specific:

- **Specific products:** `calorie counter`, `protein powder`, `electric toothbrush`, `standing desk`
- **Use cases:** `meal prep`, `home workout`, `budget travel`, `study tips`
- **Audiences:** `new moms`, `college students`, `small business owners`
- **Verticals:** `SaaS`, `DTC`, `B2B`, `ecommerce`
- **Tools/brands:** `ChatGPT`, `Notion`, `Canva`, `Shopify`

#### Never do this:
- `nichesToPromote=skincare,beauty,wellness` → requires ALL three to match, returns nothing

### promotedProducts
Find creators who have promoted specific products. Great for finding creators experienced with products similar to yours.

Example: `promotedProducts=ChatGPT` finds creators who promoted ChatGPT.

### hashtags
The `#` prefix is optional and stripped automatically. Uses AND matching — search one at a time.

## Profile Response Fields

When you call `get_creator_profiles`, each profile includes:
- `id`, `username`, `source` — identity
- `followers`, `averageViews`, `engagementRate` — metrics
- `age`, `gender` — demographics
- `mainCategory`, `subCategory` — content classification
- `bio` — creator's bio text
- `promotedProducts` — array of products they've promoted
- `nichesToPromote` — AI-analyzed niches
- `country`, `language` — location and language
- `email` — contact email (if available)
- `hashtags` — commonly used hashtags

## Pagination

- Use `page` and `perPage` in search
- Response includes `next_page` and `total_pages`
- When `next_page` is `0`, there are no more pages

## Example Workflows

### Find skincare influencers on TikTok
1. `search_creators` with `source: "tiktok"`, `nichesToPromote: "skincare"`, `followersMin: 10000`
2. `search_creators` with `source: "tiktok"`, `nichesToPromote: "beauty"`, `followersMin: 10000`
3. Deduplicate userIds from both searches
4. `get_creator_profiles` with merged IDs

### Find tech creators in France with email
1. `search_creators` with `mainCategory: "Technology"`, `country: "France"`, `emailExists: true`
2. `get_creator_profiles` with the returned IDs

### Find creators who promoted competitor products
1. `search_creators` with `promotedProducts: "CompetitorProduct"`
2. `get_creator_profiles` to see their full profile and other promotions

### Find high-engagement micro-influencers
1. `search_creators` with `followersMin: 5000`, `followersMax: 50000`, `engagementRateMin: 5`
2. `get_creator_profiles` with the returned IDs

## Available Categories

Arts, Automotive, Beauty & Personal Care, Books & Literature, Business, Finance, Career & Jobs, Collectibles & Hobbies, Community, Ecommerce, Crafts & DIY, Culture, Education, Technology, Entertainment, Environment, Family, Parenting, Fashion, Film, Fitness, Health, Food, Gaming, Gardening & Agriculture, History, Home, Humor, Law, Government, Lifestyle, Marketing, Mental Health, Music, News & Media, Outdoors, Nature, Pets, Animals, Philosophy, Spirituality, Photography, Videography, Politics, Relationships, Religion, Science, Self-Improvement, Shopping, Social Media, Social Issues & Activism, Sports, Travel, Vehicles & Transportation, Virtual Reality, Weapons & Defense, Writing, Kids

## Available Platforms
`tiktok`, `instagram`, `youtube`

## Countries
Use **full country names** (not codes). Examples: `"United States"`, `"France"`, `"United Kingdom"`, `"Germany"`, `"Australia"`, `"Japan"`, `"Brazil"`, `"Canada"`, `"India"`, `"South Korea"`
