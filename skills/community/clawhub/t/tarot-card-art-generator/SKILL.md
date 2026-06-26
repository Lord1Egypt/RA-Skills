---
name: tarot-card-art-generator
description: Generate stunning AI tarot card art and mystical oracle deck illustrations. Create custom major and minor arcana designs, divination card artwork, spiritual deck imagery, occult-themed illustrations, and fortune card visuals with ornate borders and rich symbolism via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Tarot Card Art Generator

Generate stunning AI tarot card art and mystical oracle deck illustrations. Create custom major and minor arcana designs, divination card artwork, spiritual deck imagery, occult-themed illustrations, and fortune card visuals with ornate borders and rich symbolism.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create tarot card art generator images.

## Quick start
```bash
node tarotcardartgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/tarot-card-art-generator
```
