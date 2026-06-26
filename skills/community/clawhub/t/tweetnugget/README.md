# TweetNugget

*A random inspirational tweet from hand-picked collections*

Curated tweets from tech leaders, founders, and philosophers — wisdom from Twitter/X delivered exactly when you need it.

[![ClawHub](https://img.shields.io/badge/ClawHub-tweetnugget-blue?logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiI+PHRleHQgeD0iMCIgeT0iMTQiIGZvbnQtc2l6ZT0iMTQiPjwxPC90ZXh0Pjwvc3ZnPg==)](https://clawhub.dev/tweetnugget)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
![Version](https://img.shields.io/badge/version-1.1.1-brightgreen.svg)
[![Quote Count](https://img.shields.io/badge/quotes-67-yellow.svg)](https://github.com/amplifier/tweetnugget)

## Install

### ClawHub (recommended)

```bash
clawhub install tweetnugget
```

Browse on [clawhub.dev/tweetnugget](https://clawhub.dev/tweetnugget)

### OpenClaw CLI

```bash
openclaw skills install tweetnugget
```

### Manual

Copy this folder to `~/.openclaw/skills/tweetnugget/`

## Quick Start

Once installed, request quotes in any chat where OpenClaw is active:
```
Give me a quote
Hit me with some wisdom
I need inspiration
Quote about AI
Something about leadership
Surprise me
```

## Why TweetNugget?

In a world of endless information, finding truly valuable insights can be challenging. TweetNugget solves this by:

- **Curated Wisdom**: Every quote is hand-picked from high-quality sources
- **Diverse Perspectives**: Insights from engineers, philosophers, entrepreneurs, and thought leaders
- **Easily Accessible**: Wisdom delivered exactly when you need it
- **Topic Filtering**: Find inspiration on specific topics that matter to you
- **Minimalist Design**: Focus on the content, not the interface

## Example Output

> "The purpose of knowledge is action." — @RyanHoliday

> "Most of coding was never about writing code. AI is just making this more obvious. You no longer need to recall syntax, function structure, boilerplate code, or even API endpoints. The hard part was never typing. It was always thinking. And it still is." — @Prathkum

> "Waste no more time arguing about what a good man should be. Be one." — @dailystoic - Marcus Aurelius

## How It Works

TweetNugget is an OpenClaw skill that delivers random inspirational tweets from curated JSON collections. When you request a quote, the skill:

1. **Filters by topic** (if specified) - matches your query against tagged quotes
2. **Selects randomly** - ensures variety and serendipity
3. **Presents beautifully** - displays the quote with attribution and source link
4. **Maintains quality** - all quotes are hand-curated for relevance and inspiration

## Collections

| Collection | Quotes | Source |
|---|---|---|
| `swlw-tweets.json` | 49 | Software Lead Weekly newsletter (issues #681-#657) |
| `twitter-quotes.json` | 12 | Curated Twitter wisdom |
| `stoic-quotes.json` | 6 | Stoic philosophy quotes |

**Total: 67 quotes across 3 collections**

## Available Tags

Filter quotes by topic: `action`, `advice`, `ai`, `anxiety`, `authorship`, `building`, `burnout`, `business`, `career`, `change`, `coding`, `confidence`, `creation`, `courage`, `decision-making`, `deliberate-practice`, `design`, `discipline`, `distribution`, `dopamine`, `early-career`, `engineering`, `excellence`, `explanation`, `finance`, `focus`, `goals`, `happiness`, `hiring`, `humor`, `identity`, `innovation`, `knowledge`, `leadership`, `learning`, `life`, `life-decisions`, `luck`, `marketing`, `meaningful-work`, `mindset`, `motivation`, `moving-on`, `passion`, `persistence`, `philosophy`, `planning`, `preparation`, `privacy`, `product`, `productivity`, `progress`, `programming`, `psychology`, `recruiting`, `relationships`, `resilience`, `satisfaction`, `simplicity`, `startups`, `stoicism`, `strategy`, `tech`, `thinking`, `time`, `time-money`, `tools`, `ux`, `vc`, `wisdom`, `work`

## Contributing

Add your own quote collections by placing new JSON files in the `references/` directory:

```json
{
  "name": "My Collection",
  "description": "A brief description",
  "quotes": [
    {
      "text": "The quote text",
      "author": "@handle",
      "url": "https://x.com/...",
      "tags": ["topic1", "topic2"]
    }
  ]
}
```

Fields:
- `text` (required): The quote text
- `author` (required): Twitter handle or attribution
- `url` (optional): Link to original tweet
- `category` (optional): Category label (e.g., "Software Engineering", "Philosophy")
- `tags` (optional): List of topic tags for filtering

## License

MIT