---
name: twitter-reader
description: Extract readable content from Twitter/X articles and tweets using jina.ai. Use when the user provides a Twitter/X link and wants to read the full content without being blocked by anti-bot measures. Supports various URL formats including x.com/username/article/id, x.com/i/status/id, and standard tweet URLs.
---

# Twitter Reader

## Quick Start

Extract content from a Twitter/X article or tweet:

```
1. Take the Twitter/X URL from the user
2. Construct the jina.ai URL: https://r.jina.ai/https://x.com/<id>
   - For x.com/<user>/article/<id>: use https://r.jina.ai/https://x.com/<user>/article/<id>
   - For x.com/i/status/<id>: use https://r.jina.ai/https://x.com/i/status/<id>
   - For x.com/<user>/status/<id>: use https://r.jina.ai/https://x.com/<user>/status/<id>
3. Use web_fetch to retrieve the content
4. Return the extracted markdown text to the user
```

## Why Use This

Twitter/X has anti-bot measures that prevent direct scraping. The jina.ai proxy bypasses these restrictions and returns clean, readable markdown content.

## URL Format Patterns

| Pattern | Example | jina.ai URL |
|---------|---------|-------------|
| Article | `https://x.com/Pluvio9yte/article/2023339861369864466` | `https://r.jina.ai/https://x.com/Pluvio9yte/article/2023339861369864466` |
| Status | `https://x.com/i/status/2023339861369864466` | `https://r.jina.ai/https://x.com/i/status/2023339861369864466` |
| User Status | `https://x.com/username/status/1234567890` | `https://r.jina.ai/https://x.com/username/status/1234567890` |

## Notes

- The extracted content will be in markdown format
- Images in the tweet will be preserved as markdown image links
- The web_fetch tool automatically handles the extraction
- If the URL is already in the correct format, use it directly with jina.ai
