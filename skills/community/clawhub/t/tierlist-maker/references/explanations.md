# Explanations (`detail`) — Markdown Subset

Each card may carry a `detail` string — markdown the reader sees on the
published post. Good explanations are what make a tier list worth reading. They
also help SEO: the post page server-renders card explanations as real text.

## Allowed (GitHub-Flavored Markdown subset)
- Paragraphs (blank line between).
- Headings: `#`, `##`, `###` (deeper is rarely needed; keep to 1–3 levels).
- **bold**, *italic*, ***both***, `inline code`.
- Fenced code blocks: triple backticks.
- Bullet lists: `- ` or `* `; numbered lists: `1. `.
- Blockquotes: `> `.
- Tables: GFM pipe tables.
- Links: `[text](https://...)`.
- Horizontal rule: `---`.
- Strikethrough: `~~text~~`.

## NOT allowed / won't render
- **Raw HTML** (`<div>`, `<span>`, `<img>`, …) — escaped and shown as literal
  text. Do not use it.
- **Image markdown** `![alt](url)` for rendering inside `detail` — the post does
  not render images from `detail`; cards already show their own images. (A link
  to an external image as a URL is fine, but it won't be embedded.)
- Footnotes, definition lists, math, or any non-GFM extension.

## Style guidance
- 1–4 short paragraphs per card. Tight, not a wall of text.
- Lead with the verdict, then the why: "Top-tier for X because Y."
- Avoid repeating the card label; the reader can see it.
- Keep language to the post's language (match the user's tier names — if the
  list is Chinese, write explanations in Chinese; if English, English).
- Empty/whitespace-only `detail` is dropped by the reader (treated as
  "no explanation"). That's fine — not every card needs one.
- Trim trailing whitespace; the reader trims, but keep it clean.

## The default structure (use this unless you have a reason not to)

Abstract advice like "lead with the verdict" gives uneven results across 20+
cards. This concrete shape doesn't — it came out of a finished 27-card board
where the right-hand explanation panel read cleanly on every card:

```markdown
## <tier> · <a 4-8 word verdict>
<one sentence carrying the core fact or number>

- <supporting point>
- <supporting point>
- <a tension: the controversy, the trend, or the counter-intuitive bit>
```

Why it holds up: the heading repeats the tier so the panel stands on its own, the
lead sentence hands the reader the "why" immediately, and that third bullet is
what stops every card from reading like an advertisement. Keep the same shape
across all cards in one board — the consistency is most of what makes the panel
look finished.

Vary it when a card genuinely calls for it, not for the sake of variety.

## Example
```markdown
## Why this is 夯

Multi-file refactors and long-horizon planning are consistently strong.
Cost is high, but for hard tasks it's the most reliable pick.

- Great at cross-file changes
- Strong on edge cases
- Watch the price for throwaway tasks
```
