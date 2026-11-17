---
name: quick-summarize
description: Quickly summarize any text, URL, or file content into a concise structured brief. Use when the user wants a TL;DR, executive summary, or needs to distill long content into key points without reading the full source.
metadata:
  openclaw:
    emoji: "📝"
---

# Quick Summarize

Produce a concise, structured summary of any input text, web page, or file.

## When to Use

- User asks for a summary, TL;DR, or "give me the gist"
- User pastes a long article and wants key takeaways
- User provides a URL and wants a brief without opening a browser
- User uploads a file and wants a quick digest

## Input Types

1. **Raw text** — user pastes content directly
2. **URL** — fetch with `web_fetch`, then summarize
3. **File** — read with `read` tool, then summarize

## Output Format

Always return:

```
**Summary**
<2-3 sentence overview>

**Key Points**
- <point 1>
- <point 2>
- <point 3>

**Action Items** (if applicable)
- <action>
```

## Guidelines

- Keep the Summary to 2-3 sentences maximum
- Key Points: 3-7 bullet points, each one line
- Action Items: only include if the content implies specific next steps
- Do not add commentary beyond the structure above
- If the content is shorter than ~200 words, return it with a "Content is already brief" note instead of summarizing
