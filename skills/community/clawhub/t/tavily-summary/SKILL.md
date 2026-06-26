---
name: tavily-summary
description: AI-optimized web search with structured summarization, combining Tavily Search API + proven summarization methodology from summarize.
homepage: https://tavily.com
metadata:
  clawdbot:
    emoji: "🔍"
    requires:
      bins: ["node"]
      env: ["TAVILY_API_KEY"]
    primaryEnv: "TAVILY_API_KEY"
---

# Tavily Summary

AI-optimized web search with **structured summarization methodology**, combining:
- Tavily Search API for clean, relevant search results (AI-native)
- Proven summarization rules extracted from the `summarize` project
- Output follows consistent formatting rules for readability

## Features

- Search the web with AI optimization (better than plain search engines for AI agents)
- Automatically summarizes results following structured formatting rules:
  - Strict length control, no padding
  - Automatic heading hierarchy for long content
  - Proper citation of key excerpts
  - Ad/sponsor content automatically stripped
  - Consistent Markdown formatting

## Usage

### Search

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 10
node {baseDir}/scripts/search.mjs "query" --deep
node {baseDir}/scripts/search.mjs "query" --topic news
node {baseDir}/scripts/search.mjs "query" --topic news --days 30
```

## Options

- `-n <count>`: Number of results (default: 5, max: 20)
- `--deep`: Use advanced search for deeper research (slower, more comprehensive)
- `--topic <topic>`: Search topic - `general` (default) or `news`
- `--days <n>`: For news topic, limit to last n days

## Extract content from URL

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
```

## Output Summary Rules

### Core Principles
- **Positioning**: Extract key points for users, let them quickly grasp core info and decide whether to read in depth
- **Authenticity**: 100% based on search results, never fabricate information
- **Conciseness**: Strictly control length, prefer shorter, never pad for no reason
- **Formatting**: Use Markdown formatting, long content *must* split into sections with headings

### Formatting Rules
- Content longer than 500 characters equivalent → split with `### ` prefixed Markdown headings, at least 3 headings
- Short paragraphs, use bullet points only when improves readability, don't force rigid templates
- Include 1-2 short exact excerpts (max 25 words each) as *italicized*, ignore ads/sponsors/promotions completely, treat them as if they don't exist, don't mention ignoring them

### Output Structure (for news search example)
1. One sentence opening summary of the core conclusion
2. Break into points/events, each with core idea + key data
3. (Optional) 1-2 italicized original excerpts
4. One sentence closing summary

### Absolute Prohibitions
- ❌ Never include ads/sponsors/promotions/CTAs, delete directly
- ❌ Use straight quotes only, no curly quotes
- ❌ Don't add emojis, disclaimers, unfounded speculation
- ❌ Never exceed requested length, finish early if content is short, don't pad
- ❌ Don't fabricate excerpts, omit if no suitable excerpt exists

## Requirements

- `TAVILY_API_KEY` from https://tavily.com (free plan available: 1,000 searches/month)
- Node.js 18+

## Credits

- Search API provided by [Tavily](https://tavily.com)
- Summarization methodology refined from [summarize](https://github.com/steipete/summarize)
