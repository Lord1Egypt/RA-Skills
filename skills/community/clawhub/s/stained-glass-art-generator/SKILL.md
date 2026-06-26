---
name: stained-glass-art-generator
description: Generate stunning stained glass style art and illustrations. Create luminous jewel-toned stained glass portraits, animals, landscapes, and decorative panels — perfect for wall art, print-on-demand, posters, church window designs, and mosaic-inspired artwork via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Stained Glass Art Generator

Generate stunning stained glass style art and illustrations. Create luminous jewel-toned stained glass portraits, animals, landscapes, and decorative panels — perfect for wall art, print-on-demand, posters, church window designs, and mosaic-inspired artwork.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create stained glass art generator images.

## Quick start
```bash
node stainedglassartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/stained-glass-art-generator
```
