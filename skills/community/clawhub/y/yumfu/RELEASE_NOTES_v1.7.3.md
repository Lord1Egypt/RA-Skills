# YumFu v1.7.3 — Storybook Export & Sharing Fix 📚

## Highlights

This patch release fixes real-world storybook delivery problems discovered during Telegram testing.

## What's New

### 1. Share-safe storybook HTML
- Updated `generate_storybook_v3.py`
- Storybook images are now embedded directly into the HTML as data URLs
- This makes the exported `storybook.html` portable as a single file when sent through chat platforms like Telegram

### 2. Better historical image resolution
- Improved matching for older sessions whose logged image names do not exactly match current outbound filenames
- Supports exact matches, basename matches, and fuzzy resolution across known media directories

### 3. Documented export rules
- Updated `STORYBOOK_SYSTEM.md`
- Clarified that chat-delivered HTML must not rely on local relative image paths
- Clarified that PDF export must come from a verified storybook browser tab/page

## Why this release matters

Before this patch:
- local HTML could look correct on the host machine
- but shared HTML could lose images in Telegram because recipients cannot access local relative file paths
- and a PDF could be exported from the wrong browser tab by mistake

After this patch:
- storybooks are much safer to share externally
- HTML is self-contained
- PDF export workflow is clearer and more reliable

## No breaking changes

- No save reset required
- Existing session logs remain compatible
- This is a delivery/export quality patch only

## Release Focus

**Main theme of v1.7.3:**
> Make YumFu storybooks truly portable, chat-safe, and reliable to export.
