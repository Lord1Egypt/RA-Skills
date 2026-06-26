---
name: waifu-gen-skill
description: Generate waifu generator ai images from text descriptions via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Waifu Generator

Generate stunning waifu generator ai images from a text description. Get back a direct image URL instantly.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create waifu generator images.

## Quick start
```bash
node waifugen.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/waifu-gen-skill
```
