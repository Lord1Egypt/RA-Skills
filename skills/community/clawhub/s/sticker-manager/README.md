# sticker-manager

An OpenClaw skill for saving, organizing, tagging, searching, and sending local stickers and reaction images across JPG, JPEG, PNG, WEBP, and GIF formats.

This project is maintained by TetraClaw (丁蟹), an OpenClaw agent codebase and toolsmith identity.

Authors:
- Wenzhuang Zhu
- TetraClaw (丁蟹)

中文说明见：[README.zh-CN.md](./README.zh-CN.md)

Repository / backup source:
- GitHub: https://github.com/TetraClaw/sticker-manager
- If ClawHub is unavailable, use the GitHub repository as the fallback download source.

## Features

- Save the latest inbound image into a local sticker library
- Save a specific image from recent chat/media history
- Search stickers by keyword
- Rename or delete existing stickers
- Clean very low-quality files
- Tag stickers with emotions, scenes, keywords, and descriptions
- Prepare model matching payloads for semantic recommendation
- Prepare a vision fallback plan for image meaning extraction
- Work with JPG, JPEG, PNG, WEBP, and GIF files
- **NEW**: Batch import from local directories with deduplication
- **NEW**: Discover sticker sources from URLs, directories, and web pages
- **NEW**: Automatic semantic tagging with vision model analysis
- **NEW**: Context-aware sticker recommendation based on chat history

## Quick start

```bash
python3 -m pip install -r requirements.txt
make install-hooks
make test
```

The hooks are optional for read-only use, but recommended before publishing changes. They run the sensitive-content check and the test suite before `git commit` and `git push`.

## Language selection

Supported output languages:
- `en`
- `zh`

Selection order:
1. `--lang=...`
2. `STICKER_MANAGER_LANG`
3. `LANG`
4. default to English

## Saving from chat history / recent media

Examples:

```bash
python3 scripts/save_sticker.py --list-history
python3 scripts/save_sticker.py --history-index=2 "saved_from_history"
python3 scripts/save_sticker.py --source=file_39---example.jpg "saved_by_source"
python3 scripts/save_sticker_auto.py --history-index=3 "quality_checked_name"
```

This supports workflows like:
- save this image
- save the previous image from chat
- save an image that was already sent in the conversation

## Batch collection

The repository now includes a batch collector with:
- default target count = 15
- single-thread execution by default to reduce memory pressure
- duplicate removal
- low-quality filtering
- automatic semantic batch planning after collection
- explicit `NEED_MORE` result when the target count is not met

Example:

```bash
python3 scripts/collect_stickers.py --sources-file ./sources.txt --out-dir ./stickers/frieren_batch --prefix 芙莉莲 --target-count 15
```

Notes:
- `--workers` is kept only for backward compatibility and is ignored unless set to `1`
- exit code `2` means collection succeeded but did not reach `--target-count`, and the command prints `NEED_MORE=...`
- For animated sources, the collector follows a generic rule: **suffix → Content-Type → downloaded file validation**.
- If a source appears animated, it should prefer the animated asset itself (`.gif` / animated file) instead of static preview files such as `.webp` / `.png`.
- If the downloaded result validates as static while the source looked animated, the collector rejects that fallback instead of silently saving it as a fake GIF.

## Batch import (NEW)

Import stickers from local directories with automatic deduplication:

```bash
# Import from a single directory
python3 scripts/batch_import.py ./stickers --target-dir ~/.openclaw/workspace/stickers/library/

# Import from multiple directories
python3 scripts/batch_import.py ./dir1 ./dir2 --target-dir ./library

# Import with auto-tag plan generation
python3 scripts/batch_import.py ./stickers --auto-tag

# Import from sources file
python3 scripts/batch_import.py --sources-file ./sources.txt --target-dir ./library
```

Options:
- `--recursive` / `--no-recursive`: Control directory scanning (default: recursive)
- `--min-size` / `--max-size`: Filter by file size
- `--no-dedupe`: Skip deduplication
- `--auto-tag`: Generate auto-tag plan for imported stickers
- `--output`: Save import report to JSON file

## Source discovery (NEW)

Discover sticker sources from various channels:

```bash
# Discover from local directory
python3 scripts/discover_sources.py ./stickers

# Discover from URLs
python3 scripts/discover_sources.py https://example.com/image1.gif https://example.com/image2.png

# Discover from web page (scrape static pages for images)
python3 scripts/discover_sources.py https://example.com/gallery

# Load sources from file
python3 scripts/discover_sources.py --urls-file ./urls.txt --dirs-file ./dirs.txt --pages-file ./pages.txt

# Save discovery results
python3 scripts/discover_sources.py ./stickers --output ./discovered.json

# Verify remote URLs with network requests
python3 scripts/discover_sources.py --fetch-urls https://example.com/image1.gif
```

Notes:
- Local directories are scanned immediately.
- Remote image URLs are recorded as `pending` by default so discovery can stay lightweight and planning-oriented.
- Use `--fetch-urls` when you want to verify remote URLs and capture response size metadata.
- Static page scraping only counts successfully extracted image URLs in the summary.

## Semantic matching

The semantic workflow is designed as:
1. Store metadata for each sticker: emotions, scenes, keywords, description
2. Build a model payload for recommendation
3. Let a model choose the best sticker semantically
4. Use rule matching only as fallback

Examples:

```bash
python3 scripts/sticker_semantic.py prepare-model "the user is nervous but pretending to be calm"
python3 scripts/sticker_semantic.py suggest "we finally fixed it"
python3 scripts/sticker_semantic.py suggest "we finally fixed it" --strategy=model
python3 scripts/sticker_semantic.py tag "sticker_name" "happy,calm" "meeting,celebration" "approval,done" "A calm approval reaction image."
```

## Auto-tagging (NEW)

Generate semantic tags automatically using vision models:

```bash
# Auto-tag a single image
python3 scripts/sticker_semantic.py auto-tag ./sticker.gif

# Auto-tag all images in a directory
python3 scripts/sticker_semantic.py auto-tag-dir ./stickers/

# With --apply flag (when vision model results are available)
python3 scripts/sticker_semantic.py auto-tag ./sticker.gif --apply
```

The auto-tag command generates a vision plan that needs to be executed by a vision-capable model. The output includes `__AUTO_TAG__:` marker for programmatic processing.

## Context-aware recommendation (NEW)

Recommend stickers based on chat history context:

```bash
# From JSON history
python3 scripts/sticker_semantic.py context-recommend '[{"content": "Great news!"}, {"content": "We won!"}]'

# From history file
python3 scripts/sticker_semantic.py context-recommend ./chat_history.json

# From plain text file
python3 scripts/sticker_semantic.py context-recommend ./chat.txt

# Specify top N recommendations
python3 scripts/sticker_semantic.py context-recommend ./history.json --top=5
```

The command analyzes the chat history and returns top N sticker recommendations with reasons.

## Vision fallback planning

Environment variable:
- `STICKER_MANAGER_VISION_MODELS`

Default fallback chain:
1. `bailian/kimi-k2.5`
2. `openai/gpt-5-mini`

Example:

```bash
python3 scripts/sticker_semantic.py vision-plan ./sample.png "find a doubtful emotion"
```

If all configured vision-capable models fail, the skill provides a clear failure message indicating image meaning extraction, quality validation, and emotion tagging could not be completed reliably.

## Default paths

- Sticker library: `~/.openclaw/workspace/stickers/library/`
- Inbound media: `~/.openclaw/media/inbound/`

Environment overrides:
- `STICKER_MANAGER_DIR`
- `STICKER_MANAGER_INBOUND_DIR`
- `STICKER_MANAGER_LANG`
- `STICKER_MANAGER_VISION_MODELS`

## Files

- `LICENSE`
- `SKILL.md`
- `scripts/common.py`
- `scripts/get_sticker.py`
- `scripts/manage_sticker.py`
- `scripts/save_sticker.py`
- `scripts/save_sticker_auto.py`
- `scripts/sticker_semantic.py`
- `scripts/collect_stickers.py`
- `scripts/batch_import.py` (NEW)
- `scripts/discover_sources.py` (NEW)
- `scripts/check_sensitive.py`
- `Makefile`
- `tests/`

## Known limitations

- Image meaning extraction still depends on the outer OpenClaw agent/tool layer to actually execute the fallback vision model chain.
- Semantic recommendation quality improves significantly when stickers have rich descriptions.

## Git safety checks

This repository can install local git hooks via:

```bash
make install-hooks
```

Before every `git commit` and `git push`, it runs:

1. `python3 scripts/check_sensitive.py`
2. `python3 -m pytest -q`

If sensitive-looking content is detected, the commit/push is blocked.

## Testing

Run tests with:

```bash
make test
```

Or without `make`:

```bash
python3 -m pytest -q
```

## Roadmap

- [ ] Integration with more image sources (API-based)
- [ ] Advanced duplicate detection (perceptual hashing)
- [ ] Sticker collections and folders
