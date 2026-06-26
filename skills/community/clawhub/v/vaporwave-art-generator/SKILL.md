---
name: vaporwave-art-generator
description: AI vaporwave art generator — create synthwave, retrowave, and aesthetic vaporwave images with neon grids, 80s retro colors, palm trees, and lo-fi vibes. Perfect for wallpapers, album art, social media aesthetics, and retrowave content creation via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Vaporwave Art Generator

AI vaporwave art generator — create synthwave, retrowave, and aesthetic vaporwave images with neon grids, 80s retro colors, palm trees, and lo-fi vibes. Perfect for wallpapers, album art, social media aesthetics, and retrowave content creation.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create vaporwave art generator images.

## Quick start
```bash
node vaporwaveartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/vaporwave-art-generator
```
