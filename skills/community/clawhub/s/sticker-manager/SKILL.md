---
name: sticker-manager
description: |
  Sticker library management for OpenClaw.

  Use this skill to save, search, tag, rename, clean up, collect, import, and recommend stickers or reaction images.
  It supports local inventory management for JPG / JPEG / PNG / WEBP / GIF files.

  Default library path: ~/.openclaw/workspace/stickers/library/
  Override with: STICKER_MANAGER_DIR
---

# Sticker Manager

Manage a local sticker / reaction-image library with keyword lookup, quality checks, semantic tags, batch import/collection workflows, and media sending support.

Authors:
- Wenzhuang Zhu
- TetraClaw (丁蟹)

Repository / backup source:
- GitHub: https://github.com/TetraClaw/sticker-manager
- If ClawHub is unavailable, use GitHub as the fallback download source.

## What this skill does

1. Save the latest inbound image or GIF into a local library
2. Save a specific image from recent chat/media history
3. Search stickers by keyword
4. Rename or delete existing stickers
5. Clean very low-quality files
6. Tag stickers with emotions / scenes / keywords / descriptions
7. Recommend a sticker based on direct text context or recent chat history
8. Batch-collect stickers toward a target count with dedupe and low-quality filtering
9. Batch-import stickers from local directories
10. Prepare vision-model plans for semantic tagging and image understanding
11. Return resolved file paths so the assistant can send matched media with the `message` tool

## Supported formats

- JPG
- JPEG
- PNG
- WEBP
- GIF

## Default paths

- Sticker library: `~/.openclaw/workspace/stickers/library/`
- Inbound media: `~/.openclaw/media/inbound/`

Environment overrides:

- `STICKER_MANAGER_DIR`
- `STICKER_MANAGER_INBOUND_DIR`
- `STICKER_MANAGER_LANG`
- `STICKER_MANAGER_VISION_MODELS`

## Typical use cases

### 1. Save a sticker

When the user sends an image/GIF and says things like:
- "save sticker"
- "store this"
- "save this image"
- "save the previous image"
- "save that image from chat history"

Basic save:

```bash
python3 scripts/save_sticker.py "custom_name"
```

Save from recent media history:

```bash
python3 scripts/save_sticker.py --list-history
python3 scripts/save_sticker.py --history-index=2 "saved_from_history"
python3 scripts/save_sticker.py --source=file_39---example.jpg "saved_by_source"
```

Quality-aware save:

```bash
python3 scripts/save_sticker_auto.py "custom_name"
python3 scripts/save_sticker_auto.py --history-index=3 "quality_checked_name"
```

If no name is provided, `save_sticker_auto.py` exits with code `2` and returns analysis markers so the assistant can ask a model to name the image.

### 2. Search a sticker

Command:

```bash
python3 scripts/get_sticker.py "keyword"
```

List all stickers:

```bash
python3 scripts/get_sticker.py
```

Matching order:
- exact filename match
- partial filename match
- fuzzy containment match

### 3. Rename / delete / clean

Rename:

```bash
python3 scripts/manage_sticker.py rename "old_name" "new_name"
```

Delete:

```bash
python3 scripts/manage_sticker.py delete "name"
```

Clean very small files:

```bash
python3 scripts/manage_sticker.py clean
```

### 4. Tag and recommend

Add tags:

```bash
python3 scripts/sticker_semantic.py tag "sticker_name" "happy,calm" "meeting,celebration" "thumbs-up,approved" "A calm approval reaction image."
```

Suggest for direct context:

```bash
python3 scripts/sticker_semantic.py suggest "we finally fixed it"
python3 scripts/sticker_semantic.py suggest "we finally fixed it" --strategy=model
```

List tag database:

```bash
python3 scripts/sticker_semantic.py list
```

Prepare model payload only:

```bash
python3 scripts/sticker_semantic.py prepare-model "the user is nervous but pretending to be calm"
```

Recommend from chat history:

```bash
python3 scripts/sticker_semantic.py context-recommend ./chat_history.json --top=5
```

### 5. Batch collect / import / discover

Collect from URLs or local files:

```bash
python3 scripts/collect_stickers.py --sources-file ./sources.txt --out-dir ./stickers/batch --prefix sticker --target-count 15
```

If the final count is below target, the command exits with code `2` and prints `NEED_MORE=...`.

Import from local directories:

```bash
python3 scripts/batch_import.py ./stickers --target-dir ~/.openclaw/workspace/stickers/library/
python3 scripts/batch_import.py ./stickers --auto-tag
```

Discover sources from directories, URLs, or pages:

```bash
python3 scripts/discover_sources.py ./stickers
python3 scripts/discover_sources.py https://example.com/image1.gif
python3 scripts/discover_sources.py https://example.com/gallery
python3 scripts/discover_sources.py --fetch-urls https://example.com/image1.gif
```

Default discovery is lightweight:
- local directories are scanned immediately
- remote image URLs are returned as `pending` unless `--fetch-urls` is used
- page discovery only counts successfully extracted image URLs

Animation rule (mandatory):
- If the source is originally animated, prefer downloading the animated asset itself.
- Use a generic decision path: **file suffix → HTTP Content-Type → downloaded file content validation**.
- Do **not** silently downgrade animated sources to static WEBP/PNG previews.
- If a source looks animated by reference/content-type but the downloaded file validates as static, reject it from the animated batch instead of pretending it is a GIF.
- Before sending or importing a GIF batch, verify the saved file is actually animated-capable rather than a static preview.

### 6. Auto-tagging and vision planning

Generate a vision plan for a single file:

```bash
python3 scripts/sticker_semantic.py auto-tag ./sticker.gif
```

Generate plans for a directory:

```bash
python3 scripts/sticker_semantic.py auto-tag-dir ./stickers/
```

Standalone vision fallback plan:

```bash
python3 scripts/sticker_semantic.py vision-plan ./sample.png "find a doubtful or suspicious emotion"
```

This returns a JSON plan with:
- image path
- candidate vision models
- prompt goal
- fallback failure message

Suggested default model order:
1. `bailian/kimi-k2.5`
2. `openai/gpt-5-mini`

## Sending workflow

After resolving a file path, send it with the `message` tool.

Example:

```python
message(
    action="send",
    channel="telegram",
    target="<chat_id>",
    media="/absolute/path/to/sticker.gif",
    caption="Here you go"
)
```

If you need to reply to a specific message, pass `replyTo="<message_id>"`.

## Quality rules

The auto-save flow checks media size before saving.

| Level | File size | Action |
|---|---:|---|
| High | >= 50KB | save directly |
| Good | >= 20KB | save directly |
| Medium | >= 10KB | save directly |
| Low | >= 5KB | usable, but lower confidence |
| Too low | < 5KB | reject unless forced |

Force-save example:

```bash
python3 scripts/save_sticker_auto.py "low_quality_name" --force
```

## Notes for agents

- Prefer semantic names over timestamp-heavy names
- Avoid platform-specific hardcoding in skill logic
- Use environment variables for library location overrides
- Keep send logic in the assistant/tool layer, not inside raw scripts when possible
- Validate file existence before sending
- For image meaning extraction, try the configured vision-capable model chain in `STICKER_MANAGER_VISION_MODELS`
- If the primary image model fails, try fallback models before giving up
- If all vision models fail, explicitly tell the user that image meaning, semantic tagging, and quality validation could not be completed reliably
- Treat `__MODEL_MATCH__`, `__AUTO_TAG__`, `__SEMANTIC_BATCH__`, `__ANALYZE_HISTORY__`, and `__CONTEXT_RECOMMEND__` markers as structured handoff payloads for the outer assistant layer

## Files

- `scripts/common.py` - shared path, i18n, and vision-plan helpers
- `scripts/get_sticker.py` - keyword lookup and inventory list
- `scripts/manage_sticker.py` - rename, delete, and cleanup
- `scripts/save_sticker.py` - basic save from inbound or history media
- `scripts/save_sticker_auto.py` - quality-aware save flow
- `scripts/sticker_semantic.py` - tagging, recommendation, auto-tag planning, and context analysis
- `scripts/collect_stickers.py` - batch collection with dedupe and semantic-plan output
- `scripts/batch_import.py` - local-directory import with optional auto-tag planning
- `scripts/discover_sources.py` - discovery from URLs, directories, and static pages
- `scripts/check_sensitive.py` - publish-safety scan for sensitive-looking content
- `tests/` - pytest coverage for CLI and workflow behaviors
