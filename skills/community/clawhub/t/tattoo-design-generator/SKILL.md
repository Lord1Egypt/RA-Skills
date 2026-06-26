---
name: tattoo-design-generator
description: AI tattoo design generator for creating custom tattoo concept art, ink illustrations, and tattoo reference sheets. Generate flash tattoo designs, sleeve ideas, minimalist tattoo art, tribal patterns, and fine line tattoo sketches — perfect for tattoo artists, studios, and anyone planning their next ink via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Tattoo Design Generator

AI tattoo design generator for creating custom tattoo concept art, ink illustrations, and tattoo reference sheets. Generate flash tattoo designs, sleeve ideas, minimalist tattoo art, tribal patterns, and fine line tattoo sketches — perfect for tattoo artists, studios, and anyone planning their next ink.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create tattoo design generator images.

## Quick start
```bash
node tattoodesigngenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/tattoo-design-generator
```
