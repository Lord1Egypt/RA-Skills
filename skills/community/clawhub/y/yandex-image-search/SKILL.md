---
name: reverse-image-search
description: Reverse image search (find image source, visually similar images). Use when user provides an image and wants to find its origin, similar images, or verify authenticity. Supports Yandex, Google Lens, and Bing engines. Works with both URLs and local files. No API key required.
---

# Reverse Image Search

Find the source, similar images, or context for any image using reverse image search engines.

## Setup

On first use, create a Python venv and install the dependency:

```bash
SKILL_DIR="$(dirname "SKILL.md")"
python3 -m venv "$SKILL_DIR/scripts/.venv"
"$SKILL_DIR/scripts/.venv/bin/pip" install -q PicImageSearch typing_extensions
```

`typing_extensions` is included here because the current PicImageSearch import path needs it on this machine's Python 3.14 runtime.

## Usage

```bash
SKILL_DIR="$(dirname "SKILL.md")"
"$SKILL_DIR/scripts/.venv/bin/python3" "$SKILL_DIR/scripts/search.py" "<image_url_or_path>" [engine] [limit]
```

- **image_url_or_path**: HTTP(S) URL or local file path
- **engine**: `yandex` (default, most reliable), `google` (Google Lens path), `bing`, or `all`
- **limit**: Max results per engine (default: 10)

Output is JSON with matched results including title, URL, thumbnail, and similarity when available.

If every selected engine fails due to upstream scraper breakage or anti-bot responses, the script exits non-zero so the caller can retry or fall back instead of treating the run as a clean success.

For Yandex hard failures, the error object includes `attempt_log` and `diagnostics` (including `debug_html_path` files in `/tmp`) so you can inspect exactly what response variant was received.

## Engine Selection

- **yandex** — Best overall: most stable, good at finding exact matches and similar images
- **google** — Uses Google Lens via PicImageSearch; useful as a secondary source
- **bing** — Useful as supplementary source
- **all** — Run `yandex` first, then fall back to Google Lens and Bing only if Yandex is insufficient

## Typical Workflow

1. User provides image (URL or file attachment)
2. Run search with `yandex` first
3. Only if `yandex` is insufficient, retry with `all`
4. Summarize findings: source, context, similar images

Do not start with `all` unless the user explicitly asks for all engines at once.
