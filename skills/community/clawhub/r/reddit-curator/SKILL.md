# SKILL.md - Reddit Curator

## Description
Your personal Reddit editor. Curates, summarizes, and delivers a daily digest of the best content from your favorite subreddits â no doom-scrolling, no noise, just signal.

## Price
**Free** â or **$3** to support development.

## Prerequisites
- Reddit API credentials (free via reddit.com/prefs/apps)
- Telegram or email for delivery
- Optional: OpenAI/Anthropic API for enhanced summaries

## Quick Start
1. **Get Reddit API access:**
   - Go to reddit.com/prefs/apps
   - Create "script" app
   - Note: client_id, client_secret, username, password
2. **Configure:** "Set up my Reddit curator"
3. **Add subreddits:** "Add r/AskReddit, r/technology, r/personalfinance"
4. **Set schedule:** "Deliver my digest every morning at 8am"

## Commands
- "Add r/[subreddit]" â Add to your curated list
- "Remove r/[subreddit]" â Remove from list
- "Show my subreddits" â List configured communities
- "Set digest time to [time]" â Schedule daily delivery
- "Set min upvotes to [number]" â Filter threshold
- "Add keyword filter: [word]" â Only posts containing keyword
- "Show me today's digest" â Manual delivery
- "Pause digest" â Temporarily stop
- "Resume digest" â Restart delivery

---

## Core Workflows

### 1. Daily Digest Generation

**Trigger:** Scheduled time (default: 8am) or manual request

**Process:**
1. Scan each configured subreddit (top + hot posts, last 24h)
2. Filter by:
   - Minimum upvote threshold (default: 100)
   - Keyword filters (if configured)
   - Flair filters (if configured)
   - Already-seen posts (deduplication)
3. Score each post:
   - Engagement score: (upvotes + comments Ã 2) / age_hours
   - Quality score: length, awards, crossposts
   - Relevance score: keyword matches, user preferences
4. Select top 5-10 posts across all subreddits
5. Generate summaries:
   - Title + author + subreddit
   - Key points from post text
   - Top 3 comments summary
   - Link to full post
6. Format digest with sections by subreddit
7. Deliver via configured channel

**Output Format:**
```markdown
ðï¸ Your Reddit Digest â March 4, 2025

## r/AskReddit
**1. "What's a life hack everyone should know?"** â­ 12.4k upvotes
- *Key insight:* The "two-minute rule" â if something takes <2 min, do it now
- *Top comment:* Batch similar tasks to reduce context switching
- [Read full thread](link)

## r/technology
**2. "OpenAI announces GPT-5"** â­ 8.7k upvotes
- *Summary:* New model shows 40% improvement on reasoning tasks
- *Key detail:* API pricing unchanged, rollout starts next week
- [Read full thread](link)

## r/personalfinance
**3. "I paid off $50k debt in 2 years"** â­ 5.2k upvotes
- *Strategy:* Avalanche method + side income + expense tracking
- *Top tip:* Automate all payments, treat savings as expense
- [Read full thread](link)

---
*Curated from 8 subreddits | 47 posts scanned | 12 matched your filters*
*Reply "pause" to stop | "add r/[name]" to expand | "settings" to customize*
```

### 2. Smart Filtering

**Upvote Thresholds:**
- **Casual:** 50+ upvotes (more content, some noise)
- **Curated:** 100+ upvotes (balanced, default)
- **Premium:** 500+ upvotes (only hits, less frequent)

**Keyword Filters:**
- Include: Only posts containing these words
- Exclude: Filter out posts with these words
- Example: Include "tutorial guide how-to", exclude "meme shitpost"

**Flair Filters:**
- Only show posts with specific flairs
- Example: "Discussion", "Serious", "Advice"

**Time Windows:**
- Last 24 hours (default)
- Last 7 days (weekly digest option)
- Last hour (breaking news mode)

### 3. Content Scoring Algorithm

```
Post Score = (Base Score + Engagement Bonus) Ã Quality Multiplier Ã Recency Decay

Base Score = upvotes Ã 1 + comments Ã 2
Engagement Bonus = awards Ã 50 + crossposts Ã 25
Quality Multiplier = 1.0 to 1.5 (based on post length, formatting)
Recency Decay = 1.0 (0-6h) â 0.8 (6-12h) â 0.6 (12-24h)
```

### 4. Summary Generation

**For text posts:**
- Extract 3-5 key points
- Identify main question/claim
- Summarize top comments (diverse viewpoints)

**For link posts:**
- Fetch article title + description
- Extract key quote if available
- Note: "External link â summary based on title/comments"

**For media posts:**
- Describe content type (image, video, gif)
- Summarize top comments explaining context
- Note: "Media post â see link for full content"

### 5. Delivery Options

**Telegram:**
- Formatted markdown
- Inline buttons: "Read more", "Next post", "Save for later"
- Image previews (if media post)

**Email:**
- HTML formatted digest
- Clickable links
- Mobile-responsive

**Discord:**
- Embed format
- Channel-specific delivery
- Thread creation for discussion

---

## Configuration

### curator-config.json
```json
{
  "reddit": {
    "client_id": "YOUR_CLIENT_ID",
    "client_secret": "YOUR_SECRET",
    "username": "YOUR_REDDIT_USERNAME",
    "password": "YOUR_REDDIT_PASSWORD",
    "user_agent": "RedditCurator/1.0 by YOUR_USERNAME"
  },
  "delivery": {
    "method": "telegram",
    "chat_id": "YOUR_CHAT_ID",
    "time": "08:00",
    "timezone": "America/Denver"
  },
  "filters": {
    "min_upvotes": 100,
    "max_posts_per_subreddit": 3,
    "max_total_posts": 10,
    "time_window_hours": 24,
    "include_keywords": [],
    "exclude_keywords": ["meme", "shitpost"],
    "include_flairs": [],
    "exclude_flairs": ["Meme"]
  },
  "subreddits": [
    {
      "name": "AskReddit",
      "weight": 1.0,
      "min_upvotes": 200
    },
    {
      "name": "technology",
      "weight": 1.2,
      "min_upvotes": 100
    }
  ],
  "summarization": {
    "enabled": true,
    "model": "claude-sonnet",
    "max_length": 150
  }
}
```

---

## Advanced Features

### Trend Detection
- Track which subreddits are trending up/down
- Alert on unusual activity spikes
- "r/technology is 3x more active than usual today"

### Saved Posts Sync
- Auto-save digested posts to Reddit "Saved"
- Create curated lists by topic
- Export saved posts to Notion/Obsidian

### Cross-Subreddit Analysis
- "This topic is trending across 3 of your subreddits"
- Detect emerging themes
- Surface cross-community discussions

### Weekly Roundup
- Best of the week (highest scored posts)
- Trending topics summary
- New subreddit recommendations based on interests

### Breaking News Mode
- Monitor for high-velocity posts (rising fast)
- Immediate alert for major events
- Override schedule for urgent content

---

## Examples

### Example 1: Tech Professional Setup
```
User: "Add r/programming, r/webdev, r/MachineLearning, r/technology"
User: "Set min upvotes to 200"
User: "Add keyword filter: tutorial, guide, open source"
User: "Deliver at 7am"

Result: Daily digest of high-quality tech content, 
focusing on educational posts and open source projects.
```

### Example 2: Casual Browsing
```
User: "Add r/AskReddit, r/LifeProTips, r/todayilearned"
User: "Set min upvotes to 500"
User: "Exclude keywords: politics, NSFW"

Result: Entertaining, broadly-appealing content only,
no controversial or explicit material.
```

### Example 3: Finance Focus
```
User: "Add r/personalfinance, r/investing, r/financialindependence"
User: "Add keyword filter: strategy, advice, experience"
User: "Set digest time to 6pm"

Result: Evening digest of financial wisdom and 
investment discussions to review after work.
```

---

## Guardrails

**Respect Reddit:**
- Rate limit: 1 request per second
- Cache results to minimize API calls
- Follow Reddit API terms of service
- Don't republish content commercially

**User Privacy:**
- Credentials stored encrypted
- No tracking of user reading habits
- No sharing of curated lists

**Content Warnings:**
- Flag potentially controversial content
- Respect NSFW filters
- Allow keyword-based content blocking

---

## Troubleshooting

**Error: "Reddit API rate limited"**
- Wait 10 minutes, retry
- Reduce number of subreddits
- Increase time between scans

**Error: "No posts found"**
- Lower upvote threshold
- Add more subreddits
- Check keyword filters aren't too restrictive

**Error: "Authentication failed"**
- Verify Reddit credentials
- Check 2FA isn't blocking API access
- Regenerate API keys if needed

**Digest not delivering**
- Check delivery method configuration
- Verify Telegram chat ID or email
- Check scheduled time and timezone

---

## Version History
- **V1.0:** Daily digest, basic filtering, Telegram delivery
- **V1.1:** Smart scoring, keyword filters, flair filtering
- **V1.2:** Multi-channel delivery (email, Discord), weekly roundup
- **V1.3:** Trend detection, cross-subreddit analysis, saved posts sync

---

*Curate your internet. Save your time.*
