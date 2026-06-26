---
name: vintage-poster-generator
description: AI vintage poster generator — create retro art prints, old-school travel posters, 1950s-1970s style illustrations, antique advertising art, and nostalgic wall art from any text prompt. Perfect for Etsy sellers, interior designers, and retro aesthetic lovers seeking vintage-style digital art, aged poster designs, and classic print visuals via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Vintage Poster Generator

AI vintage poster generator — create retro art prints, old-school travel posters, 1950s-1970s style illustrations, antique advertising art, and nostalgic wall art from any text prompt. Perfect for Etsy sellers, interior designers, and retro aesthetic lovers seeking vintage-style digital art, aged poster designs, and classic print visuals.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create vintage poster generator images.

## Quick start
```bash
node vintagepostergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/vintage-poster-generator
```
