---
name: quick-sum
description: Quick text summarization skill. Use when the user wants a fast bullet-point summary of a long text, article, or document. Generates concise bullet points preserving key facts.
metadata: { "openclaw": { "emoji": "⚡" } }
---

# Quick Sum

Generate fast, bullet-point summaries of long texts.

## When to use

- User pastes a long article and asks for a summary
- Need to distill key facts from a document
- Want bullet points instead of prose

## Steps

1. Read the input text fully.
2. Extract the 3–7 most important facts or points.
3. Format as concise bullet points.
4. Optionally add a one-line TL;DR at the top.

## Output format

```
TL;DR: <one-line summary>

- <key point 1>
- <key point 2>
- <key point 3>
```

## Notes

- Keep bullets under 20 words each.
- Preserve numbers, dates, and proper nouns.
- If the text is already short (<100 words), return it verbatim.
