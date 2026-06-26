---
name: surreal-art-generator
description: Generate jaw-dropping surreal AI art — Dali-style melting clocks, Magritte-inspired floating objects, dreamlike landscapes, absurdist scenes, impossible architecture, and bizarre creature mashups. Perfect for viral social posts, album covers, gallery prints, concept art, and TikTok-friendly weird-internet aesthetics. Supports surrealism, dream art, absurd imagery, dadaism, and abstract surreal styles via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Surreal Art Generator

Generate jaw-dropping surreal AI art — Dali-style melting clocks, Magritte-inspired floating objects, dreamlike landscapes, absurdist scenes, impossible architecture, and bizarre creature mashups. Perfect for viral social posts, album covers, gallery prints, concept art, and TikTok-friendly weird-internet aesthetics. Supports surrealism, dream art, absurd imagery, dadaism, and abstract surreal styles.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create surreal art generator images.

## Quick start
```bash
node surrealartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `square`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/surreal-art-generator
```
