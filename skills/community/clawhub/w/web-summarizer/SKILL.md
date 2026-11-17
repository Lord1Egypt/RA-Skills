---
name: web-summarizer
description: Summarize any web page by URL or by pasting text. Returns a concise structured summary with key points, entities, and action items. Use when the user wants a quick digest of an article, documentation page, or any web content without reading the full source.
metadata:
  openclaw:
    emoji: "📰"
---

# Web Summarizer

Get a structured summary of any web page or text block.

## When to use

- User asks "summarize this page" or "what's this about"
- User pastes a URL and wants the gist
- User has a long text and wants key takeaways

## Steps

1. **Fetch content** — if input is a URL, use `web_fetch` to download the page content.
2. **Strip boilerplate** — remove navigation, footers, ads, cookie banners.
3. **Summarize** — produce:
   - One-sentence TL;DR
   - 3–5 bullet points of key takeaways
   - Named entities (people, organizations, products)
   - Action items (if applicable)
4. **Deliver** — present the summary in chat.

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `source` | string | ✅ | URL or raw text |
| `style` | string | ❌ | `brief` (default) or `detailed` |
| `language` | string | ❌ | Output language (default: same as source) |

## Example

```
User: Summarize https://example.com/article about the new research paper
Agent:
  TL;DR: A new study finds X.
  • Key point 1
  • Key point 2
  Entities: Alice Smith (lead author), MIT
  Action items: Review methodology before citing
```

## Notes

- For URLs behind paywalls, note that full extraction may fail and summarize what's available.
- Respect robots.txt and site terms. If a site blocks scraping, inform the user.
- For very long pages (>20k chars), prefer `detailed` style with section breakdowns.
