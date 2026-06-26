---
name: social-auto-publisher
description: Social media automation operations assistant. Automatically generate and publish content for Xiaohongshu, Weibo, and Twitter, with scheduled posting and interactive replies. Covers the full chain from content creation → AI illustration → scheduled publishing → interaction monitoring → data review.
---

# Social Media Automation Operations Assistant

Multi-platform content creation and publishing automation. Supports Xiaohongshu, Weibo, and Twitter across all three platforms, covering the full chain from topic selection to review.

## Use Cases

Use when users mention keywords such as social media operations, automatic publishing, scheduled posting, multi-platform publishing, social media automation, one-click posting, batch publishing, auto-reply, or social operations.

## Workflow

```
Topic Planning → Content Generation → AI Illustration → Scheduled Publishing → Interaction Monitoring → Data Review
```

## Platform Support Matrix

| Platform | Publishing Method | Content Type | Scheduled Publishing | Interactive Replies |
|----------|-------------------|-------------|----------------------|---------------------|
| Xiaohongshu | Browser automation | Image-text posts | ✅ | ✅ |
| Weibo | API / Cookie | Image-text / Plain text | ✅ | ✅ |
| Twitter | API v2 | Image-text / Plain text | ✅ | ✅ |

## Prerequisites

### General Preparation

1. Ensure `node` >= 18 is available
2. Install dependencies: `npm install axios openai`
3. AI service is available (for content generation and image creation)

### Xiaohongshu

- Logged-in browser environment (host mode)
- Creator permissions enabled: https://creator.xiaohongshu.com/publish/publish
- Refer to `references/xiaohongshu-guide.md` for the complete operation guide

### Weibo

- Weibo Open Platform App Key / Access Token
- Or browser Cookie (configured via `references/weibo-guide.md`)
- Environment variables: `WEIBO_APP_KEY`, `WEIBO_ACCESS_TOKEN`

### Twitter

- Twitter API v2 credentials
- Environment variables: `TWITTER_API_KEY`, `TWITTER_API_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_SECRET`

## Core Commands

### 1. Content Generation

```bash
# Generate multi-platform content based on a topic (title + body + tags)
node scripts/generate_content.js \
  --topic "How AI is changing content creation" \
  --platforms "xiaohongshu,weibo,twitter" \
  --tone "professional yet approachable"

# Auto-detect trending topics and generate content
node scripts/generate_content.js \
  --auto-topic \
  --platforms "xiaohongshu,weibo"
```

**Parameter Descriptions:**
- `--topic`: Content topic (mutually exclusive with `--auto-topic`)
- `--auto-topic`: Automatically track trending topics for selection
- `--platforms`: Target platforms, comma-separated (`xiaohongshu,weibo,twitter`)
- `--tone`: Tone style (`professional` / `casual` / `storytelling` / `practical`)
- `--count`: Number of candidates to generate (default 3)

**Output:** JSON format, one optimized content entry per platform, including title, body, tags, and image description.

### 2. One-Click Publishing

```bash
# Publish to a specified platform
node scripts/publish.js \
  --platform xiaohongshu \
  --content-file ./output/post_20260504.json

# Simultaneously publish to multiple platforms
node scripts/publish.js \
  --platforms "xiaohongshu,weibo,twitter" \
  --content-file ./output/post_20260504.json
```

**Parameter Descriptions:**
- `--platform` / `--platforms`: Target platform(s)
- `--content-file`: Path to the content JSON file
- `--dry-run`: Preview mode; does not actually publish

### 3. Scheduled Publishing

```bash
# Create a scheduled publishing task
node scripts/schedule_post.js \
  --content-file ./output/post_20260504.json \
  --schedule "2026-05-05 20:00" \
  --platforms "xiaohongshu,weibo,twitter"

# Batch create a weekly content schedule
node scripts/schedule_batch.js \
  --plan-file ./output/weekly_plan.json
```

### 4. Interaction Monitoring and Replies

```bash
# Monitor comments/mentions across platforms
node scripts/monitor_interactions.js \
  --platforms "xiaohongshu,weibo,twitter" \
  --since 1h

# Auto-reply (requires approval)
node scripts/auto_reply.js \
  --platform xiaohongshu \
  --strategy "warm" \
  --dry-run
```

**Reply Strategies:**
- `warm`: Warm and friendly style, suitable for fan interactions
- `professional`: Professional and concise, suitable for business accounts
- `witty`: Humorous and clever, suitable for personal brands
- `custom`: Custom template (see `references/reply-templates.md`)

## Complete Workflow Examples

### Scenario 1: From Trending Topic to Publishing (Fully Automatic)

```
1. Topic selection: node scripts/generate_content.js --auto-topic --platforms "xiaohongshu"
2. Manual review of generated content (title, body, image description)
3. Image creation: AI-generated or manually uploaded
4. Scheduled publishing: node scripts/schedule_post.js --schedule "tomorrow 20:00"
5. Run monitor_interactions.js 24 hours after publishing to view interaction data
```

### Scenario 2: Batch Schedule a Week's Content

```
1. Plan a week's topics (5-7 themes)
2. Batch generation: node scripts/generate_content.js --topic-file ./topics.txt --platforms "xiaohongshu,weibo"
3. After reviewing each entry, run schedule_batch.js to set the schedule
4. Automatic daily publishing; check data the following day
```

### Scenario 3: Crisis Monitoring and Auto-Replies

```
1. Set up scheduled monitoring: cron runs monitor_interactions.js every 30 minutes
2. Automatically flag and alert on negative comments
3. Use auto_reply.js to automatically reply to positive comments (dry-run mode requires manual confirmation)
```

## Content Compliance Key Points

**Xiaohongshu:**
- Prohibit absolute terms (best, number one, only)
- Prohibit medical efficacy claims
- Prohibit price-inducing language
- Must check the originality declaration

**Weibo:**
- Comply with the "Weibo Community Convention"
- Prohibit sensitive topics and non-compliant external links
- Marketing content must be labeled

**Twitter:**
- Comply with the Twitter Rules
- Prohibit spam behavior
- API rate limit: 300 tweets per 3-hour window

## Scheduled Task Recommendations

```bash
# Content publishing (morning and evening peak hours daily)
0 8,20 * * *   # Publish once at 8 AM and 8 PM each day

# Interaction monitoring (every 30 minutes on weekdays)
*/30 9-22 * * 1-5

# Daily data report (every night at 11 PM)
0 23 * * *
```

## File Structure

```
social-auto-publisher/
├── SKILL.md
├── scripts/
│   ├── generate_content.js    # AI content generation
│   ├── publish.js             # Unified publishing entry
│   ├── schedule_post.js       # Scheduled publishing
│   ├── schedule_batch.js      # Batch scheduling
│   ├── monitor_interactions.js # Interaction monitoring
│   ├── auto_reply.js          # Auto-reply
│   └── utils/
│       ├── xiaohongshu.js     # Xiaohongshu browser operations
│       ├── weibo.js           # Weibo API operations
│       └── twitter.js         # Twitter API operations
├── references/
│   ├── xiaohongshu-guide.md   # Complete Xiaohongshu operations guide
│   ├── weibo-guide.md         # Weibo operations guide
│   ├── twitter-guide.md       # Twitter operations guide
│   ├── reply-templates.md     # Reply template library
│   └── content-strategy.md    # Content strategy and topic selection methodology
└── assets/
    └── templates/
        └── weekly_plan.json   # Weekly plan template
```