# Twitter Bookmarks Exporter

A Claude Code skill for exporting all X/Twitter bookmarks into individual Markdown files with metadata.

## Features

- **Exports all bookmarks** — Converts your entire Twitter bookmark collection to Markdown
- **Handles multiple pages** — Supports paginated API responses from browser Network tab
- **Rich metadata** — Includes title, author, date, engagement stats, and media links
- **Full content extraction** — Supports regular tweets, note tweets, articles, and quoted tweets
- **URL expansion** — Converts t.co shortlinks to real URLs
- **Markdown-ready** — Output compatible with Obsidian, Notion, and other note-taking systems
- **Organized output** — Files named sequentially (0001-title.md, 0002-title.md, etc.)

## Installation

1. In Claude Code, go to **Settings** → **Skills**
2. Click **Import** or **+** to add a custom skill
3. Select `twitter-bookmarks-exporter.skill`
4. The skill is now available

## Prerequisites

### Requirements
- Python 3.8+
- X/Twitter account with bookmarks
- Browser (Chrome or Firefox) with DevTools

## How to Use

### Step 1: Capture bookmarks from your browser

1. Log in to [https://x.com](https://x.com)
2. Open **DevTools** — press `F12` (Windows/Linux) or `Cmd+Option+I` (Mac)
3. Go to the **Network** tab
4. Navigate to [https://x.com/i/bookmarks](https://x.com/i/bookmarks)
5. Filter requests by typing `Bookmarks` in the network filter
6. **Scroll to the bottom** of your bookmarks — each scroll loads a new page
7. For each `Bookmarks?variables=...` request in the Network panel:
   - Right-click → **Copy** → **Copy Response**
   - Paste into a text editor

### Step 2: Save responses to bookmarks.json

Paste all captured API responses (one after another) into a single file named `bookmarks.json` in the `twitter-bookmarks-exporter/` folder.

**Example (two pages):**
```
{ "data": { "bookmark_timeline_v2": { ... } } }
{ "data": { "bookmark_timeline_v2": { ... } } }
```

No merging needed — just paste end-to-end and save.

### Step 3: Run the exporter

Invoke the skill in Claude Code:

```
/export-twitter-bookmarks
```

Or trigger naturally:
> "Export my Twitter bookmarks to Markdown"

The skill will:
1. Verify `bookmarks.json` exists
2. Run the exporter script
3. Generate Markdown files in `output/bookmarks/`
4. Report the total bookmarks exported

## Output Format

Each bookmark becomes a Markdown file with YAML frontmatter:

```markdown
---
title: "Example tweet text"
url: "https://x.com/username/status/123456789"
author: "@username"
saved_at: "2026-04-14"
type: "tweet"  # tweet | note | article
---

# Example tweet text

**Author:** Display Name (@username)
**Date:** 2026-04-14
**URL:** https://x.com/username/status/123456789
**Stats:** ❤️ 142 · 🔁 38 · 💬 12 · 🔖 95 · 👁 24000

Full tweet content here, with all t.co links expanded to real URLs.

![image](https://pbs.twimg.com/media/example.jpg)

> **Quoted tweet** by @otheruser
> https://x.com/otheruser/status/987654321
> Quoted tweet text here.
```

## Output Location

Files are saved to:
```
twitter-bookmarks-exporter/output/bookmarks/
```

Example filenames:
```
0001-the-thing-that-surprises-me-most-about-llms.md
0002-we-are-still-very-much-in-the-early-innings.md
0003-claude-code-features.md
```

## Tweet Types Supported

| Type | What it exports |
|------|---|
| **Regular Tweet** | Full text, t.co URLs expanded, engagement stats, media links |
| **Note Tweet** | Complete long-form text (no truncation) |
| **X Article** | Title, preview text, article link |
| **Quoted Tweet** | Original tweet + quoted tweet as blockquote |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `bookmarks.json not found` | Capture from browser Network tab (see prerequisites) |
| No bookmarks extracted | Ensure JSON is raw API response, not browser-formatted copy |
| Encoding errors | Save bookmarks.json as UTF-8 |
| Empty titles | Script auto-generates slugs from tweet content |

## Manual Execution

If you prefer to run the script directly:

```bash
python scripts/main.py
```

## Customization

Edit `scripts/main.py` to:
- Change output directory (`OUT_DIR`)
- Modify the Markdown template (`bookmark_to_markdown`)
- Add filters (by author, date range, etc.)

## Performance

- Exporting **1,000 bookmarks**: ~5-10 seconds
- Exporting **10,000 bookmarks**: ~30-60 seconds

Time depends on:
- Number of bookmarks
- System performance
- File I/O speed

## Support

For issues:
1. Check the troubleshooting section above
2. Verify `bookmarks.json` is valid JSON
3. Ensure all API responses are pasted correctly

## License

MIT License. Free to use, modify, and distribute.
