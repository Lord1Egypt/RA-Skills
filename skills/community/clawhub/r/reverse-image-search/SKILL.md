---
name: reverse-image-search
description: Reverse image search (find image source, visually similar images). Use when user provides an image and wants to find its origin, similar images, or verify authenticity. Supports Yandex, Google, and Bing engines. Works with both URLs and local files. No API key required.
---

# Reverse Image Search

Find the source, similar images, or context for any image using reverse image search engines.

## Setup

On first use, create a Python venv and install the dependency:

```bash
SKILL_DIR="$(dirname "SKILL.md")"
python3 -m venv "$SKILL_DIR/scripts/.venv"
"$SKILL_DIR/scripts/.venv/bin/pip" install -q PicImageSearch
```

## Usage

```bash
SKILL_DIR="$(dirname "SKILL.md")"
"$SKILL_DIR/scripts/.venv/bin/python3" "$SKILL_DIR/scripts/search.py" "<image_url_or_path>" [engine] [limit]
```

- **image_url_or_path**: HTTP(S) URL or local file path
- **engine**: `yandex` (default, most reliable), `google`, `bing`, or `all`
- **limit**: Max results per engine (default: 10)

Output is JSON with matched results including title, URL, thumbnail, and similarity when available.

## Engine Selection

- **yandex** — Best overall: most stable, good at finding exact matches and similar images
- **google** — Good for well-known images, web pages, products
- **bing** — Useful as supplementary source
- **all** — Query all three engines in parallel

## Typical Workflow

1. User provides image (URL or file attachment)
2. Run search with `yandex` first
3. If results are insufficient, retry with `all`
4. Summarize findings: source, context, similar images
