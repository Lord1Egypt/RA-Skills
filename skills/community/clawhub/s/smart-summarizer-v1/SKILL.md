---
name: smart-summarizer
description: Summarizes URLs, articles, YouTube videos, PDFs, and pasted text into a structured digest with TL;DR, key takeaways, and action items. Use this skill whenever the user shares a link, pastes a long block of text, says "summarize", "TL;DR", "give me the key points", "what does this say", "read this for me", or "is this worth reading". Also activate when a user shares a URL without any instruction — sharing a link without comment almost always means they want to know what's in it. Supports English and Chinese content.
---

# Smart Summarizer

## Purpose

Help the user decide in 30 seconds whether a piece of content is worth their full attention — and if so, what the most important parts are. The summary should be a faithful compression, not a reinterpretation. The user is trusting this output to represent the source accurately, so precision matters more than polish.

## Detecting Input Type

Identify what was shared and handle accordingly:
- **URL** → fetch page content via web search or direct fetch
- **YouTube URL** → extract title, description, and available transcript; summarize the topic
- **PDF** → extract text content, then summarize
- **Pasted text** → process directly
- **Multiple items** → summarize each separately, then add a batch comparison at the end

## Summary Format

Use this structure for every summary:

```
📑 [Title]
━━━━━━━━━━━━━━━━━━
Source: [URL or "pasted text"]
Length: [~X min read / ~X words]
━━━━━━━━━━━━━━━━━━

💡 TL;DR:
[One sentence. The core message — what would you tell a friend?]

🔑 Key Takeaways:
• [Specific point with concrete detail — include numbers, names, dates where present]
• [...]
• [3–5 bullets total]

✅ Action Items:
• [What the reader might want to do based on this content]
[Omit this section entirely if the content doesn't imply any actions]

🤔 Worth reading in full?
[One honest sentence: what you'd gain from the full version vs. this summary]
```

## What Makes a Good Summary

**TL;DR**: One sentence forces you to identify the single most important idea. If you can't fit it in one sentence, the article probably has multiple competing claims — name the most central one. Hedged or compound TL;DRs ("it covers X, Y, and also Z") usually mean the synthesis work hasn't been done yet.

**Key Takeaways**: The value here is specificity. "The study found that sleep affects performance" is not a takeaway — "The study found a 34% performance drop after two nights of under-6-hour sleep" is. Include numbers, names, and dates when the source has them.

**Action Items**: Only include this section when the content genuinely implies something the reader should consider doing. News articles, opinion pieces, and pure analysis usually don't warrant action items. Product reviews, how-tos, and research with clear implications do.

**Assessment**: Be honest. If the article is thin, repetitive, or buries its actual point in the last paragraph, say so. The user is relying on this to decide whether to spend 15 minutes reading — a falsely positive assessment wastes their time.

## Batch Mode

When the user shares multiple items at once, summarize each using the standard format, then close with:

```
📊 Batch: [N] items summarized
Common themes: [2–3 overlapping topics across the items]
Most actionable: [which item has the clearest implications for action, and why]
```

## Archive

Save each summary to `~/.openclaw/summaries/[YYYY-MM-DD]-[slug].md`.

When the user asks "search my summaries for [topic]" or "what did I read about X", scan the archive and return matching past summaries.

## Language

Detect the content language automatically and match it in the output. If the source is Chinese, respond in Chinese. If the user specifies a language preference, follow it regardless of source language.

## When Things Go Wrong

If a URL can't be fetched, report it directly rather than guessing at the content:
```
⚠️ Couldn't access [URL]
Reason: [paywalled / 404 / access denied]
Suggestion: Try pasting the article text directly.
```

Only summarize what's actually in the source. If the content is thin, say so rather than padding the output. The summary's usefulness depends entirely on it accurately representing what's there.
