---
name: sticker-pack-skill
description: Generate ai sticker pack generator images from text descriptions via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Sticker Pack Generator

Generate stunning ai sticker pack generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai sticker pack generator images.

## Quick start
```bash
node stickerpack.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/sticker-pack-skill
```
