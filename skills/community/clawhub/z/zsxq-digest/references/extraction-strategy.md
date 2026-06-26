# Extraction strategy

## Goal

Extract only the minimum fields required to build a daily triage digest from authenticated Knowledge Planet pages.

## Recommended acquisition order

1. Logged-in browser automation
   - Best for personal use and private content.
   - Use a browser session the user has already authenticated.
   - Navigate to followed circles, recent updates, or notification feeds.

2. Local export or pasted source
   - Use when browser automation is unavailable.
   - Accept copied text, saved HTML, or structured JSON exported by another local helper.

3. API-like access
   - Only use if the user already has a legitimate local integration path.
   - Do not design the public skill around undocumented or risky credential scraping.

## Minimum capture fields

For each update capture:
- `circle_name`
- `item_id` or stable link
- `title_or_hook`
- `author`
- `published_at`
- `content_preview`
- `content_type`
- `engagement_hint` (likes/comments if visible)
- `url`

## Selector design guidance

- Prefer semantic anchors: visible headings, timestamps, link patterns, container repetition.
- Keep selectors centralized in one implementation file.
- Avoid brittle nth-child chains.
- Include a fallback capture mode that grabs visible text blocks when structure shifts.

## Anti-fragility pattern

Build the runtime in two phases:
1. acquisition: capture raw items into JSON
2. digest: normalize, score, and render markdown

This separation makes site changes cheaper to fix.

## Compliance and safety

- Never publish personal cookies or hardcoded credentials.
- Do not assume scraping stability; require user-owned login context.
- Be transparent about missing items or partial extraction.
