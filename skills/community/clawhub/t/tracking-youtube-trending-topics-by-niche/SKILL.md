---
name: tracking-youtube-trending-topics-by-niche
description: >
  Tracks trending YouTube topics and video formats in a specific niche using apidojo's YouTube
  scraper on Apify. Triggers when the user asks to: find trending YouTube topics in a niche,
  discover what videos are getting views right now in a category, identify trending YouTube formats
  or themes in an industry, find high-performing YouTube video ideas from search trends, research
  what the YouTube algorithm is currently rewarding in a topic area, discover rising YouTube creators
  in a niche, or analyze what video angles perform best on YouTube in a category.
  Returns trending video titles, view counts, engagement metrics, format patterns, and topic themes.
  Ideal for YouTube content creators, video marketers, and brand video strategists.
license: Apache-2.0
metadata:
  author: apidojo
  version: "1.0"
  apify-actor: apidojo/youtube-scraper
---

# Tracking YouTube Trending Topics by Niche

Identifies what's performing on YouTube in a specific niche by analyzing recent high-view videos. Surfaces repeatable title formulas, content formats, and topic themes that the YouTube algorithm is currently favoring.

## Prerequisites

- `APIFY_TOKEN` environment variable set
- Optional: Apify MCP server installed

## Inputs

| Parameter | Type | Required | Default | Notes |
|-----------|------|----------|---------|-------|
| `startUrls` | array | Optional | `[]` | YouTube URLs — channels, playlists, Shorts, search results |
| `youtubeHandles` | array | Optional | `[]` | YouTube channel handles (e.g. `@kurzgesagt`) |
| `getTrending` | boolean | Optional | `false` | Retrieve trending videos |
| `keywords` | array | Optional | `[]` | Search keywords |
| `gl` | string | Optional | `us` | Country code for results (e.g. `US`, `GB`) |
| `hl` | string | Optional | `en` | Language code (e.g. `en`, `de`) |
| `uploadDate` | string | Optional | `all` | Upload date filter: `any`, `hour`, `today`, `week`, `month`, `year` |
| `duration` | string | Optional | `all` | Duration filter: `any`, `short`, `long` |
| `features` | string | Optional | `all` | Feature filter: `4k`, `hd`, `live`, `cc`, `3d`, `hdr`, etc. |
| `sort` | string | Optional | `r` | Sort order for search results |
| `maxItems` | number | Optional | Unlimited | Maximum videos to return |
| `customMapFunction` | string | Optional | — | JavaScript function to transform each output object |

## Workflow

```
Progress:
- [ ] Step 1: Search for recent high-performing videos in niche
- [ ] Step 2: Extract title patterns and topics
- [ ] Step 3: Score trending momentum
- [ ] Step 4: Identify format and structural patterns
- [ ] Step 5: Deliver trend brief
```

### Step 1: Search YouTube


**Recommended — run_actor.js (handles waiting, output, and file saving automatically):**
```bash
# Quick answer (prints table to chat)
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}'

# Save as CSV
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.csv --format csv

# Save as JSON
node scripts/run_actor.js \
  --actor "apidojo~youtube-scraper" \
  --input '{"param": "value"}' \
  --output YYYY-MM-DD_results.json --format json
```
> `APIFY_TOKEN` must be set in environment or `.env` file.

**If Apify MCP is available:**
```
Tool: apify:run-actor
Actor: "apidojo~youtube-scraper"
Input:
{
  "searchKeywords": ["[NICHE]", "best [NICHE]", "[NICHE] 2026", "[NICHE] for beginners"],
  "maxResults": 50,
  "type": "video"
}
```

**REST API fallback:**
```bash
curl -X POST   "https://api.apify.com/v2/acts/apidojo~youtube-scraper/runs?token=$APIFY_TOKEN"   -H "Content-Type: application/json"   -d '{"searchKeywords": ["personal finance tips", "best investing 2026", "investing for beginners"], "maxResults": 50}'
```

### Step 2: Analyze Title Patterns

Classify each video title:
```
title_formula:
  NUMBER_LIST = "Top [N]", "[N] Best", "[N] Things"
  HOW_TO = "How to", "Step-by-step", "The Complete Guide"
  VS_COMPARISON = "vs", "or", "Which is Better"
  WARNING = "Avoid", "Mistake", "Stop Doing", "Don't"
  STORY = "I tried", "What happened when", first-person
  YEAR_SPECIFIC = contains current year → high freshness signal
```

### Step 3: Score Trending Momentum

```
momentum = viewCount / days_since_published  # views per day

trend_score = (momentum / 10000, max 1) * 0.40
            + (likeCount / viewCount * 100 > 4 ? 1 : ratio/4) * 0.30
            + (commentCount / viewCount * 100 > 0.3 ? 1 : ratio/0.3) * 0.30
```

### Step 4: Edge Cases

- **All trending videos from one channel**: Likely a dominant creator in the niche — note this; it's a competitive signal, not a format trend. Look at the second and third most-viewed creators for broader signals
- **Niche is very small** (< 10 videos above threshold): Lower `min_views` to 10K; report available data
- **Year-specific content dominates**: Good sign for content with year in title — recommend "[niche] [year+1]" format as a strong ranking opportunity

## Output Format

```
# YouTube Trending Topics: [NICHE]
Videos analyzed: [N] | Above threshold ([MIN_VIEWS] views): [N] | Date: [DATE]

## Top Title Formulas (by Avg Views)
| Formula | # Videos | Avg Views | Avg Like Rate | Best Example |
|---------|---------|-----------|-------------|-------------|
| Number List | [N] | [N] | [X%] | "[title]" |
| How-To | [N] | [N] | [X%] | |

## Top Performing Videos
| Title | Views | Momentum (views/day) | Like Rate | Trend Score |
|-------|-------|---------------------|----------|------------|

## Trending Topic Themes
1. [Theme] — [N] videos, [N] total views
2. [Theme]

## Recommended Video Ideas
Based on trending patterns:
1. "[Specific video title recommendation using a winning formula]"
2. "[Video title recommendation]"
```

## Troubleshooting

**Results skewed by one old viral video**: Filter by `published_date` in the `date_range`; sort by momentum (views/day) not total views.
**Title formulas are too generic**: This is normal — YouTube title strategies are well-known. The value is in the specific topic within the formula.
**Niche has no recent high-performers**: The niche may be saturated or declining on YouTube; consider whether YouTube is the right platform for this content.

