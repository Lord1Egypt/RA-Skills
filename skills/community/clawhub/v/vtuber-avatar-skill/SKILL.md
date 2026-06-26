---
name: vtuber-avatar-skill
description: Generate vtuber avatar creator ai images with AI via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# VTuber Avatar Generator

Generate stunning vtuber avatar creator ai images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node <script> "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create vtuber avatar creator images.

## Quick start
```bash
node vtuberavatar.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `anime`)

## Install
```bash
npx skills add blammectrappora/vtuber-avatar-skill
```
