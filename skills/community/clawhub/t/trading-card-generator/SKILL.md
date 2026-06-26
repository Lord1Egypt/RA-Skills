---
name: trading-card-generator
description: AI trading card generator for designing custom collectible card art in MTG, Pokemon, Yu-Gi-Oh, and sports card styles. Create fantasy TCG cards, spell cards, character cards, monster cards, and original trading card illustrations with ornate borders, dramatic painterly compositions, and premium foil-style finishes for tabletop games, fan-made decks, and collectible card art via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Trading Card Generator

AI trading card generator for designing custom collectible card art in MTG, Pokemon, Yu-Gi-Oh, and sports card styles. Create fantasy TCG cards, spell cards, character cards, monster cards, and original trading card illustrations with ornate borders, dramatic painterly compositions, and premium foil-style finishes for tabletop games, fan-made decks, and collectible card art.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai trading card generator images.

## Quick start
```bash
node tradingcardgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/trading-card-generator
```
