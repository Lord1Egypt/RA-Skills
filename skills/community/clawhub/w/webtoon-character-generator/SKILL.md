---
name: webtoon-character-generator
description: AI webtoon character generator — create manhwa-style portraits, Korean comic characters, and webtoon OCs with clean line art, expressive eyes, and vibrant colors. Perfect for webtoon creators, manhwa fans, comic artists, and anyone wanting a modern anime-adjacent digital illustration style via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Webtoon Character Generator

AI webtoon character generator — create manhwa-style portraits, Korean comic characters, and webtoon OCs with clean line art, expressive eyes, and vibrant colors. Perfect for webtoon creators, manhwa fans, comic artists, and anyone wanting a modern anime-adjacent digital illustration style.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create webtoon character generator images.

## Quick start
```bash
node webtooncharactergenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/webtoon-character-generator
```
