---
name: selfie-art-generator
description: Generate AI selfie art portraits from text descriptions — cinematic portraits, anime illustrations, oil painting style, and artistic profile pictures via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Selfie Art Generator

Generate AI selfie art portraits from text descriptions. Create cinematic portraits, anime-style illustrations, oil paintings, and artistic profile pictures. Returns a direct image URL instantly.

## Token

Requires a Neta API token. Free trial available at <https://www.neta.art/open/>.

```bash
export NETA_TOKEN=your_token_here
node selfieartgenerator.js "your prompt" --token "$NETA_TOKEN"
```

## When to use
Use when someone asks to generate or create AI portrait art, selfie art, or stylized profile pictures from a text description.

## Quick start
```bash
node selfieartgenerator.js "cinematic portrait, golden hour lighting, sharp facial details" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--style` — `anime`, `cinematic`, `realistic` (default: `cinematic`)
- `--ref` — reference image UUID for style inheritance (optional)

## Install
```bash
npx skills add yangzhou-chaofan/selfie-art-generator
```
