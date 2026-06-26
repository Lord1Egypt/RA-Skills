---
name: texture-art-generator
description: Generate stunning satisfying texture art and hyperrealistic material images — glass, crystal, liquid, jelly, wax, soap, and iridescent surfaces captured in breathtaking macro detail. Perfect for ASMR content creators, product design backgrounds, Instagram aesthetics, TikTok visual content, and short-form video thumbnails. Also known as material art generator, surface texture art, and macro texture photography via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Texture Art Generator

Generate stunning satisfying texture art and hyperrealistic material images — glass, crystal, liquid, jelly, wax, soap, and iridescent surfaces captured in breathtaking macro detail. Perfect for ASMR content creators, product design backgrounds, Instagram aesthetics, TikTok visual content, and short-form video thumbnails. Also known as material art generator, surface texture art, and macro texture photography.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create satisfying texture art generator images.

## Quick start
```bash
node textureartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/texture-art-generator
```
