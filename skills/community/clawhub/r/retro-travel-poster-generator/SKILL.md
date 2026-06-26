---
name: retro-travel-poster-generator
description: Generate vintage-style travel posters inspired by the golden age of tourism advertising (1920s-1960s WPA, art deco, mid-century modern) featuring iconic destinations, national parks, beaches, cities, landmarks, and exotic locales. Perfect for Etsy sellers, print-on-demand stores, wall art, home decor, postcards, travel agency branding, Airbnb listings, nostalgic gifts, retro aesthetic collections, and vintage tourism poster prints via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Retro Travel Poster Generator

Generate vintage-style travel posters inspired by the golden age of tourism advertising (1920s-1960s WPA, art deco, mid-century modern) featuring iconic destinations, national parks, beaches, cities, landmarks, and exotic locales. Perfect for Etsy sellers, print-on-demand stores, wall art, home decor, postcards, travel agency branding, Airbnb listings, nostalgic gifts, retro aesthetic collections, and vintage tourism poster prints.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create retro travel poster generator images.

## Quick start
```bash
node retrotravelpostergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/retro-travel-poster-generator
```
