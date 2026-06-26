---
name: steampunk-art-generator
description: AI steampunk art generator — create Victorian steampunk portraits, cyberpunk Victorian characters, brass-and-gears illustrations, cosplay reference art, and industrial fantasy scenes. Perfect for steampunk fans, cosplayers, worldbuilders, and retro-futuristic art lovers via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Steampunk Art Generator

AI steampunk art generator — create Victorian steampunk portraits, cyberpunk Victorian characters, brass-and-gears illustrations, cosplay reference art, and industrial fantasy scenes. Perfect for steampunk fans, cosplayers, worldbuilders, and retro-futuristic art lovers.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create steampunk art generator images.

## Quick start
```bash
node steampunkartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add blammectrappora/steampunk-art-generator
```
