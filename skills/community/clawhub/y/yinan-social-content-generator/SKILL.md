---
name: social-content-generator
description: Generate social media content (posts, captions, images) for multiple platforms. Use when creating social media posts, marketing content, or bulk content calendars. Supports Twitter/X, Instagram, LinkedIn, Facebook with AI text and image generation.
---

# Social Content Generator

## Overview

AI-powered social media content creation skill. Generates platform-optimized posts with text and images using OpenAI models. Supports bulk generation and content calendars.

## Supported Platforms

| Platform   | Text Limit | Image Ratio    | Hashtags |
|------------|------------|----------------|----------|
| Twitter/X  | 280 chars  | 16:9, 1:1      | 2-3      |
| Instagram  | 2200 chars | 1:1, 4:5, 9:16 | 5-15     |
| LinkedIn   | 3000 chars | 1.91:1, 1:1    | 3-5      |
| Facebook   | 63206 chars| 1.91:1, 1:1    | 1-3      |

## Quick Start

### Generate Single Post

```bash
python scripts/generate_post.py \
  --platform twitter \
  --topic "AI productivity tools" \
  --tone professional \
  --include-image
```

### Generate Content Calendar

```bash
python scripts/generate_calendar.py \
  --config config.json \
  --output calendar_output/
```

## Scripts

### generate_post.py

Generate a single social media post with optional image.

**Arguments:**
- `--platform` - Target platform (twitter, instagram, linkedin, facebook)
- `--topic` - Post topic/theme
- `--tone` - Writing tone (professional, casual, funny, inspirational)
- `--include-image` - Generate accompanying image
- `--image-prompt` - Custom image prompt (auto-generated if not provided)
- `--output` - Output directory (default: current dir)

**Output:**
- `post.txt` - Generated text content
- `image.png` - Generated image (if requested)
- `metadata.json` - Post metadata

### generate_calendar.py

Generate a week/month of content in bulk.

**Arguments:**
- `--config` - JSON config file with topics and schedule
- `--output` - Output directory
- `--platforms` - Target platforms (comma-separated)

### upload_post.py (Optional)

Upload generated posts to social platforms via API.

**Requirements:**
- Platform API credentials in `.env` file
- Twitter API v2, Instagram Graph API, LinkedIn API

## Configuration

### Environment Variables (.env)

```bash
# OpenAI for text generation
OPENAI_API_KEY=sk-...

# For image generation (if using OpenAI)
OPENAI_API_KEY=sk-...

# Platform APIs (optional, for auto-upload)
TWITTER_BEARER_TOKEN=...
TWITTER_API_KEY=...
TWITTER_API_SECRET=...
INSTAGRAM_ACCESS_TOKEN=...
LINKEDIN_ACCESS_TOKEN=...
```

### Content Calendar Config (JSON)

```json
{
  "brand": {
    "name": "Your Brand",
    "voice": "professional yet friendly",
    "topics": ["AI", "productivity", "tech news"]
  },
  "schedule": {
    "twitter": {"frequency": "daily", "times": ["09:00", "15:00"]},
    "instagram": {"frequency": "3x/week", "times": ["11:00"]},
    "linkedin": {"frequency": "2x/week", "times": ["08:00"]}
  },
  "content_mix": {
    "educational": 40,
    "promotional": 20,
    "engagement": 25,
    "curated": 15
  }
}
```

## Post Templates

### Twitter/X
```
[Hook/Question]

[Main content - 1-2 sentences]

[Call-to-action or insight]

#Hashtag1 #Hashtag2
```

### Instagram
```
[Emoji] [Attention-grabbing opener]

[Story/value proposition - 2-4 sentences]

[Benefits/features]

[Call-to-action]

[Relevant hashtags: 5-15]
```

### LinkedIn
```
[Professional hook or insight]

[Detailed content - story, data, or analysis]

[Key takeaway]

[Question for engagement]

#Industry #Topic #Professional
```

## Best Practices

1. **Platform optimization** - Each platform has different norms and limits
2. **Visual consistency** - Maintain brand colors and style in images
3. **Engagement hooks** - Start with questions or bold statements
4. **Call-to-action** - Always include a CTA (comment, share, click, etc.)
5. **Hashtag strategy** - Mix popular and niche hashtags
6. **Posting timing** - Schedule for peak engagement hours

## Example Outputs

### Twitter Post
```
🚀 Just discovered an AI tool that saves me 2 hours daily.

It automates my entire content workflow: research → draft → edit → schedule.

The best part? It learns my writing style over time.

What's your favorite productivity tool?

#AI #Productivity #ContentCreation
```

### Instagram Caption
```
✨ Monday Motivation ✨

Your competition isn't other creators. It's the distraction in your pocket.

Every scroll, every notification, every "quick check" steals from your focus.

This week, try:
• Phone in another room while working
• 90-min deep work blocks
• Batch your social media time

Your future self will thank you. 💪

What's your biggest focus killer?

#MondayMotivation #Productivity #DeepWork #FocusTips #ContentCreator #AI #WorkSmart
```

## Troubleshooting

- **Image generation fails**: Check API key and quota
- **Text too long**: Adjust topic scope or use summarize option
- **Platform API errors**: Verify credentials and permissions
- **Rate limits**: Add delays between bulk generations
