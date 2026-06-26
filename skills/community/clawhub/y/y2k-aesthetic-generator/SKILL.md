---
name: y2k-aesthetic-generator
description: Y2K aesthetic generator for nostalgic early-2000s and 2010s throwback photos — recreate the viral '2026 is the new 2016' trend with flash-photography selfies, Snapchat-era looks, low-res iPhone vibes, butterfly clips, frosted makeup, and dreamy mall-photo nostalgia. Perfect for TikTok, Instagram Reels, profile pics, retro fashion moodboards, Y2K party invites, nostalgia core content, and 2000s/2010s aesthetic edits via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Y2K Aesthetic Generator

Y2K aesthetic generator for nostalgic early-2000s and 2010s throwback photos — recreate the viral '2026 is the new 2016' trend with flash-photography selfies, Snapchat-era looks, low-res iPhone vibes, butterfly clips, frosted makeup, and dreamy mall-photo nostalgia. Perfect for TikTok, Instagram Reels, profile pics, retro fashion moodboards, Y2K party invites, nostalgia core content, and 2000s/2010s aesthetic edits.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create y2k aesthetic photo generator images.

## Quick start
```bash
node y2kaestheticgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/y2k-aesthetic-generator
```
