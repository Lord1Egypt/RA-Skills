---
name: x-search-highlights
description: Search and extract high-value posts from X (Twitter) with engagement-based ranking. Use when user asks to search X, find best posts, get highlights from Twitter/X, or extract high-engagement content on a specific topic.
---

# X Search Highlights

Search and extract high-value posts from X (Twitter) with engagement-based ranking.

## Quick Start

```bash
# Basic search
~/.openclaw/skills/x-search-highlights/scripts/x-search.sh "Claude Code"

# With filters
~/.openclaw/skills/x-search-highlights/scripts/x-search.sh "AI Agent" 10 5 1000 markdown
```

## Description

Extract valuable posts from X search results based on engagement metrics (likes, retweets, replies, views). Ideal for discovering trending discussions, finding expert insights, or curating content for research.

## When to Use

Activate when user asks to:
- Search X/Twitter for specific topics
- Find "best" or "high-value" posts on a subject
- Extract posts with engagement data
- Curate content from X discussions
- Discover trending discussions

Trigger phrases:
- "Search X for [topic]"
- "Find best posts about [topic] on Twitter"
- "Get highlights from X search"
- "Extract valuable tweets"

## Input Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `topic` | string | required | Search query (e.g., "Claude Code", "AI Agent") |
| `maxResults` | number | 5 | Maximum number of posts to return |
| `minLikes` | number | 0 | Minimum likes threshold (filter low-engagement) |
| `scrollTimes` | number | 3 | Number of scroll iterations (more = more candidates) |
| `sortBy` | string | "engagement" | Sort method: engagement, likes, views, recent |
| `outputFormat` | string | "markdown" | Output format: markdown, json, summary |

## Output Format

### Markdown (default)

```markdown
## 1. [Post Title/Summary]

- **标题**：[Content summary]
- **日期**：YYYY-MM-DD
- **标签**：#tag1 #tag2
- **亮点**：🎯 [Key insight] 💡 [Unique perspective]
- **互动**：X 回复 · X 转发 · X 点赞 · X 浏览
- **链接**：[点击阅读原文](URL)
```

### JSON

```json
{
  "total": 10,
  "posts": [
    {
      "text": "...",
      "author": "...",
      "likes": 1000,
      "retweets": 200,
      "views": 50000
    }
  ]
}
```

## Workflow

1. **Open search page**: Navigate to X search with query
2. **Load content**: Scroll N times to collect candidate posts
3. **Extract data**: Parse DOM for post content and engagement metrics
4. **Rank and filter**: Calculate engagement scores, apply filters
5. **Format output**: Return results in requested format

## Core Algorithm

**Engagement Score:**
```
Score = (likes × 2) + (retweets × 5) + (views × 0.01)
```

**Weight Rationale:**
- Retweets (×5): Strongest signal (public sharing)
- Likes (×2): Approval signal (low barrier)
- Views (×0.01): Reach indicator (easily inflated)

## Dependencies

- `bb-browser` ≥ 0.11.2
- Chrome/Chromium browser
- X.com login state (in bb-browser profile)

## Installation

```bash
# Via ClawHub (after publishing)
clawhub install x-search-highlights

# Or clone from GitHub
git clone https://github.com/Ghostwritten/x-search-highlights.git ~/.openclaw/skills/x-search-highlights
```

## Usage Examples

```bash
# Search for "OpenClaw"
scripts/x-search.sh "OpenClaw"

# Get 10 posts with min 1000 likes
scripts/x-search.sh "AI Agent" 10 3 1000

# JSON output
scripts/x-search.sh "RAG" 20 5 0 json
```

## Troubleshooting

**No posts found:**
- Check bb-browser is running: `bb-browser status`
- Verify X.com login state
- Try different search keywords

**JSON parsing errors:**
- Ensure `bb-browser` version ≥ 0.11.2
- Check Chrome/Chromium is accessible

**Rate limits:**
- Reduce `scrollTimes` parameter
- Add delays between operations

## Limitations

- X lazy loading limits initial results
- Bookmark data not available via scraping
- Rate limits may affect large-scale scraping
- Search quality depends on X algorithm
