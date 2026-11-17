---
name: twitter-bookmarks-exporter
description: Exports all X/Twitter bookmarks into individual Markdown files with metadata.
version: 1.2.0
author: Jeff Yang
tags:
  - twitter
  - bookmarks
  - export
  - markdown
  - productivity
required_tools:
  - python
min_python_version: 3.8
license: MIT
---

# Twitter Bookmarks Exporter

Extracts all bookmarked tweets from X/Twitter into clean Markdown files for Obsidian, Notion, or any note-taking system.

## What it does

1. Parses bookmarks from `bookmarks.json` (captured from browser Network tab).
2. Handles **multiple concatenated API pages** in a single file — just paste all responses end-to-end.
3. Converts each bookmark into a Markdown file with YAML frontmatter.
4. Saves files to `output/bookmarks/` folder, named sequentially like `0001-title.md`.
5. Extracts full content for all tweet types:
   - **Regular tweets** — full text, t.co URLs expanded to real URLs
   - **Note tweets** — complete long-form text (no truncation)
   - **X Articles** — title + preview text + article link
6. Includes quoted tweets as blockquotes, media image/video links, and engagement stats.

## Prerequisites

### Step 1 — Capture your bookmarks from the browser

X/Twitter does not provide a public bookmarks export API, so you need to capture the responses directly from your browser's Network tab. Follow these steps:

1. Log in to [https://x.com](https://x.com) in **Chrome** or **Firefox**.
2. Open **DevTools**: press `F12` (Windows/Linux) or `Cmd+Option+I` (Mac).
3. Click the **Network** tab.
4. Navigate to [https://x.com/i/bookmarks](https://x.com/i/bookmarks).
5. In the Network filter box, type `Bookmarks` to filter relevant requests.
6. **Scroll all the way to the bottom** of your bookmarks page. Each scroll triggers a new paginated API request — you must scroll through *all* your bookmarks to capture every page.
7. In the Network panel you will now see multiple `Bookmarks?variables=...` requests — one per page.

### Step 2 — Save the responses to `bookmarks.json`

For **each** `Bookmarks` request in the Network panel:
1. Right-click the request → **Copy** → **Copy Response**.
2. Paste the response into a text editor.

Once you have all responses, save them into a single file named `bookmarks.json` inside the `twitter-bookmarks-exporter/` folder. You can paste the responses **one after another** — the script handles multiple concatenated JSON objects automatically.

**Example with two pages:**
```
{ "data": { "bookmark_timeline_v2": { ... } } }
{ "data": { "bookmark_timeline_v2": { ... } } }
```

> No special merging needed — just paste all responses end-to-end and save.

> The script handles the current X GraphQL API response format as well as the legacy v1 format.

## How to run

```bash
python scripts/main.py
```

This generates Markdown files in `output/bookmarks/`.

## Output format

Each file follows this structure:

```markdown
---
title: "Example tweet text here"
url: "https://x.com/username/status/123456789"
author: "@username"
saved_at: "2026-04-14"
type: "tweet"  # tweet | note | article
---

# Example tweet text here

**Author:** Display Name (@username)
**Date:** 2026-04-14
**URL:** https://x.com/username/status/123456789
**Stats:** ❤️ 142 · 🔁 38 · 💬 12 · 🔖 95 · 👁 24000

Full tweet content here, with all t.co links expanded to real URLs.

![image](https://pbs.twimg.com/media/example.jpg)   <!-- if media present -->

> **Quoted tweet** by @otheruser            <!-- if quoting another tweet -->
> https://x.com/otheruser/status/987654321
> Quoted tweet text here.
```

## Example files generated

```
output/bookmarks/
├── 0001-the-thing-that-surprises-me-most-about-llms.md
├── 0002-we-are-still-very-much-in-the-early-innings.md
└── ...
```

## Usage in OpenClaw

**Agent prompt:** "Export my Twitter bookmarks to Markdown using twitter-bookmarks-exporter."

**Expected behavior:**
1. Confirm `bookmarks.json` exists in the skill folder.
2. Run `python scripts/main.py`.
3. Verify files created in `output/bookmarks/`.
4. Report completion with file count.

## Customization

Edit `scripts/main.py` to:
- Change output path (`OUT_DIR`)
- Modify Markdown template (`bookmark_to_markdown`)
- Add filters (e.g., only tweets from certain authors, by date range)

## Troubleshooting

- **No bookmarks.json**: Manually capture from browser Network tab (see Prerequisites).
- **No bookmarks found**: Ensure the JSON is the raw API response, not a browser-formatted copy.
- **Encoding issues**: Ensure the file is saved as UTF-8.
- **Empty titles**: Script auto-generates slugs from content.

## License

MIT License. Free to use, modify, and distribute.
