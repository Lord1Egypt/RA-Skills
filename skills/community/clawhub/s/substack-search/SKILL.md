---
name: substack-news
description: >
  Scrape AI-related articles from Substack search using browser automation.
  Uses agent-browser to render Substack's JS-dependent search page,
  extract titles, authors, and summaries, and format them as a numbered digest.
  Use when: (1) user asks to search Substack for articles or news,
  (2) user wants recent Substack posts on any topic,
  (3) user mentions "Substack" + a search term + "articles/posts/news".
  NOT for: general web search, fetching a single Substack post by URL.
---

# Substack News

Collect and summarize Substack search results via browser automation.

## Workflow

### 1. Open Substack Search

Run the browser automation script:

```bash
python "${SKILL_DIR}/scripts/scrape_substack.py" "SEARCH QUERY" [--range day|week|month]
```

For environments without Python, fall back to the manual `agent-browser` commands documented in [references/browser-flow.md](references/browser-flow.md).

### 2. Output Format

Return results as a numbered list:

```
N. **Title**
   — Author · Publication · X min read — *one-line summary if available*
```

If fewer than 20 results exist on the page, report exactly what is found. No padding.

### 3. Scroll for More

The script auto-scrolls up to 3 times to capture additional results.
Substack typically returns 10-20 posts per 24-hour window.

## Notes

- Substack search is behind JS rendering; `web_fetch` cannot extract it — browser automation is required.
- Time range filter: `day` (default), `week`, `month`.
- Close the browser session after extraction: `agent-browser close`.
