---
name: web-clipper
description: Save any web page as an Obsidian-compatible Markdown clipping. Triggered by "save <URL>" or "保存这个". Uses Jina Reader API for clean content extraction. Supports custom tags, subfolders, and vault paths. Saves to ~/.openclaw/obsidian-cache/clippings/ by default. TRIGGER "save <URL>" / "保存这个" / any URL with "save" or "clip" -> ALWAYS exec: python3 ~/.openclaw/skills/web-clipper/scripts/save_web_page.py --url "URL" -> Confirm the saved filename to user. NEVER use memory.
---

# Web Clipper

Save any web page as a clean, readable Markdown note in your Obsidian vault. Powered by [Jina Reader API](https://jina.ai) for content extraction — no browser extension required. Works from inside Claude.

## When to Use This Skill

- You want to save an article for later reading in Obsidian
- You found a useful page and want it archived as Markdown
- You want to add tags and organize clips into subfolders
- You need to clip technical docs, blog posts, or news articles
- You want to avoid browser extension bloat — just tell Claude to save it

## What This Skill Does

1. **Fetches the page** via Jina Reader API — strips ads, nav, and noise
2. **Converts to Markdown** — clean readable format with frontmatter
3. **Saves to your vault** — default: `~/.openclaw/obsidian-cache/clippings/`
4. **Adds metadata** — title, source URL, date saved, and your tags
5. **Confirms the filename** — Claude tells you exactly where it was saved

## Requirements

- Python 3.7+
- `requests` library: `pip install requests`
- **`JINA_API_KEY`** — optional. Works without a key (free tier). Set for higher rate limits:

```bash
echo 'JINA_API_KEY=jina_xxxxxxxxxxxx' >> ~/.openclaw/.env
```

Get a free key at [jina.ai](https://jina.ai/?sui=apikey)

> **Note**: The script only accepts `http://` and `https://` URLs. Local file paths are not supported.

## How to Use

### Basic — Save a URL

```
save https://example.com/article
```

```
保存这个 https://v2ex.com/t/123456
```

### With Tags

```
save https://example.com/article --tags "ai,research"
```

### Save to a Subfolder

```
save https://example.com/article --folder clippings/tech
```

### Full Options

```bash
python3 ~/.openclaw/skills/web-clipper/scripts/save_web_page.py \
  --url "https://example.com/article" \
  --folder "clippings/tech" \
  --tags "ai,tools" \
  --vault "/path/to/your/obsidian/vault"
```

## Example

**User**: `save https://www.v2ex.com/t/1197958`

**Claude executes**:
```bash
python3 ~/.openclaw/skills/web-clipper/scripts/save_web_page.py --url "https://www.v2ex.com/t/1197958"
```

**Output file** (`~/.openclaw/obsidian-cache/clippings/2026-01-15 V2EX Thread Title.md`):
```markdown
---
title: "V2EX Thread Title"
source: "https://www.v2ex.com/t/1197958"
saved: "2026-01-15 14:32"
tags: []
---

# V2EX Thread Title

> Source: https://www.v2ex.com/t/1197958
> Saved: 2026-01-15 14:32

---

[Clean article content in Markdown...]
```

**Claude confirms**: "已保存为 `2026-01-15 V2EX Thread Title.md` ✅"

## Supported Content

| Content Type | Support |
|---|---|
| Blog posts / articles | ✅ |
| Technical documentation | ✅ |
| News articles | ✅ |
| V2EX / Reddit threads | ✅ |
| GitHub READMEs | ✅ |
| PDF files (remote) | ✅ |
| JS-heavy SPAs | ⚠️ Jina handles most; complex apps may need PinchTab |
| Login-required pages | ❌ |

## File Structure

```
web-clipper/
├── SKILL.md                    ← This file (Claude reads this)
└── scripts/
    └── save_web_page.py        ← Main clipping script
```

## Output Format

Saved files include YAML frontmatter for Obsidian compatibility:

```yaml
---
title: "Article Title"
source: "https://original-url.com"
saved: "2026-01-15 14:32"
tags: [ai, research]
---
```

## Notes

- Filenames are auto-sanitized and dated: `YYYY-MM-DD Title.md`
- Duplicate filenames get a counter suffix: `2026-01-15 Title (2).md`
- Default vault: `~/.openclaw/obsidian-cache/clippings/`
- The `JINA_API_KEY` free tier supports ~1000 requests/month
