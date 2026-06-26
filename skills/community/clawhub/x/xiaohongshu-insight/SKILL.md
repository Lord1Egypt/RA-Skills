---
name: xiaohongshu-insight
description: Xiaohongshu viral content data insight tool. Continuously collects 2000+ viral posts daily across the platform, based on criteria: low-follower viral posts, periodic high-engagement posts, single-day interaction spikes, and sustained interaction growth. Use for: Xiaohongshu content creation, viral content analysis, data reference, traffic trend tracking, and creative inspiration.
---

# Xiaohongshu Data Insights

## Overview

A professional data insight tool built specifically for Xiaohongshu content creation. Continuously collects over 2000+ viral posts daily across the platform, empowering creators with data references, traffic trend insights, and creative inspiration.

## Use Cases

Use when users mention Xiaohongshu viral posts, post data, traffic trends, creative inspiration, low-follower viral posts, interaction spikes, etc.

## Core Capabilities

### 1. Viral Post Collection

Automatically collects 2000+ viral posts daily based on the following criteria:

- **Low-Follower Viral Posts**: Follower count < 5000, yet post interactions exceed the category average by more than 3x
- **Periodic High-Engagement**: Like growth > 1000 within 7 days, with a clear sustained growth trend
- **Single-Day Interaction Spike**: Daily increase in likes + saves + comments > 500
- **Sustained Interaction Growth**: Interactions increase for 3 consecutive days, with average daily growth rate > 20%

### 2. Data Dimensions

Each viral post includes the following data:

| Dimension | Description |
|-----------|-------------|
| Basic Information | Title, cover image, author, publish time, category tags |
| Interaction Data | Likes, saves, comments, shares, and growth rates |
| Author Profile | Follower count, total posts, average interactions, category distribution |
| Content Features | Title keywords, cover style, content type, word count range |
| Traffic Curve | Interaction data at 24h/48h/72h/7d intervals after publishing |

### 3. Use Scenarios

**Scenario 1: Finding Creative Inspiration**
```
User: What are some recent low-follower viral posts in the beauty category?
→ Filter category=Beauty, follower count<5000, sort by interaction volume
→ Return TOP 20 viral posts with key feature analysis
```

**Scenario 2: Analyzing Traffic Trends**
```
User: What common characteristics do this week's viral fashion posts share?
→ Aggregate analysis of viral posts in Fashion category over the past 7 days
→ Extract title keywords, cover features, publishing time distribution
→ Output trend insight report
```

**Scenario 3: Competitor Account Research**
```
User: Why does this blogger consistently produce viral content?
→ Analyze the blogger's historical viral posts
→ Compare with other bloggers in the same category
→ Output success factor analysis
```

## Quick Start

### Query Viral Posts

Use `scripts/query_notes.py` to query viral post data:

```bash
python scripts/query_notes.py --category Beauty --days 7 --limit 50
```

Parameter descriptions:
- `--category`: Category (Beauty/Fashion/Food/Travel/Home/Parenting/Career/Emotions/Knowledge/Entertainment)
- `--days`: Number of days to query (default 7 days)
- `--limit`: Number of results to return (default 20)
- `--sort`: Sort field (engagement/growth/fans)
- `--min_engagement`: Minimum interaction threshold

### Analyze Trend Features

Use `scripts/analyze_trends.py` to analyze category trends:

```bash
python scripts/analyze_trends.py --category Fashion --output report.md
```

Output includes:
- TOP 20 Trending Keywords
- High-Frequency Cover Styles
- Optimal Publishing Time Windows
- Viral Title Formulas
- Engagement Rate Distribution

### Export Data

Use `scripts/export_data.py` to export data:

```bash
python scripts/export_data.py --format xlsx --output viral_data.xlsx
```

Supported formats: xlsx, csv, json

## Data Field Descriptions

See [references/data_schema.md](references/data_schema.md) for details.

## Viral Post Detection Algorithm

See [references/viral_criteria.md](references/viral_criteria.md) for details.

## Notes

1. Data is sourced from publicly available posts and is for creative reference only
2. It is recommended to selectively draw inspiration based on your own account positioning
3. Avoid directly copying content; focus on creative transformation
4. Data is updated daily; pay attention to timeliness