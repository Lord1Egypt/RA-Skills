---
name: wallpaper-claw-skill
description: Generate ai wallpaper generator images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# AI Wallpaper Generator

Generate stunning ai wallpaper generator images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai wallpaper generator images.

## Quick start
```bash
node wallpaperclaw.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `landscape`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add BarbaraLedbettergq/wallpaper-claw-skill
```
