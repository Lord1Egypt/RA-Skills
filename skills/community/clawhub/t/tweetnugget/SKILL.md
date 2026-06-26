---
name: tweetnugget
description: A random inspirational tweet from curated collections of hand-picked wisdom by tech leaders, founders, and philosophers.
version: 1.1.0
author: amplifier
tools:
  - bash  # Used only for: python3 script execution to read local JSON files
---

# TweetNugget

When the user asks for a quote, inspiration, or says something like "hit me with a quote" or "give me some wisdom":

## How It Works

1. Run `scripts/get_quote.py` to pick a quote from `references/` directory
2. Return the output directly to the user

## Quote Collections

The `references/` folder contains JSON files with this structure:

```json
{
  "name": "Collection Name",
  "description": "...",
  "quotes": [
    {
      "text": "The quote text",
      "author": "@handle",
      "url": "https://x.com/...",
      "tags": ["tag1", "tag2"]
    }
  ]
}
```

Available collections:
- `swlw-tweets.json` - 49 quotes from Software Lead Weekly newsletter (Dec-Jul 2025)
- `twitter-quotes.json` - 12 curated Twitter quotes
- `stoic-quotes.json` - 6 Stoic philosophy quotes

## Step-by-Step Instructions

### Basic: Get a random quote

```bash
python3 scripts/get_quote.py
```

Return the output directly to the user. Do not add commentary.

### Surprise Me: Random collection, then random quote

For variety across collections:

```bash
python3 scripts/get_quote.py --surprise
```

### Filtered: Get a quote by tag

If the user specifies a topic (e.g., "quote about AI", "something about leadership", "coding quote"):

```bash
python3 scripts/get_quote.py --tag ai
```

Replace `ai` with the user's topic. Uses partial matching (e.g., "lead" matches "leadership"). Falls back to a random quote if no match is found.

### Available Tags

Common tags across collections: `action`, `advice`, `ai`, `building`, `career`, `coding`, `courage`, `design`, `discipline`, `engineering`, `focus`, `happiness`, `humor`, `innovation`, `knowledge`, `leadership`, `learning`, `life`, `marketing`, `mindset`, `motivation`, `persistence`, `philosophy`, `product`, `programming`, `resilience`, `simplicity`, `startups`, `stoicism`, `strategy`, `thinking`, `wisdom`, `work`

## Response Format

Always return quotes in this format:

> "The quote text" — @handle

If the quote has a URL, you may optionally append it as a link. Keep responses minimal - let the quote speak for itself.

## Adding More Quotes

Users can add their own collections by placing new JSON files in the `references/` directory following the same format.
