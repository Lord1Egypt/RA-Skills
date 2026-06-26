---
name: watercolor-art-generator
description: AI watercolor art generator — create stunning watercolor paintings, portraits, and illustrations instantly. Perfect for watercolor portrait commissions, digital watercolor artwork, custom watercolor gifts, social media art, and printable wall art. Also great as a watercolor painting maker, aquarelle portrait creator, and watercolor illustration generator via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Watercolor Art Generator

AI watercolor art generator — create stunning watercolor paintings, portraits, and illustrations instantly. Perfect for watercolor portrait commissions, digital watercolor artwork, custom watercolor gifts, social media art, and printable wall art. Also great as a watercolor painting maker, aquarelle portrait creator, and watercolor illustration generator.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create watercolor art generator images.

## Quick start
```bash
node watercolorartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/watercolor-art-generator
```
