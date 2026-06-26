---
name: wedding-invitation-generator
description: Design elegant AI wedding invitations, save-the-dates, RSVP cards, bridal shower invites, and engagement announcements. Generate beautiful watercolor florals, botanical illustrations, minimalist modern layouts, rustic barn themes, romantic garden scenes, boho chic designs, classic gold-accented stationery, and custom wedding suite artwork for brides, grooms, wedding planners, stationery designers, and Etsy sellers via the Neta AI image generation API (free trial at neta.art/open).
tools: Bash
---

# Wedding Invitation Generator

Design elegant AI wedding invitations, save-the-dates, RSVP cards, bridal shower invites, and engagement announcements. Generate beautiful watercolor florals, botanical illustrations, minimalist modern layouts, rustic barn themes, romantic garden scenes, boho chic designs, classic gold-accented stationery, and custom wedding suite artwork for brides, grooms, wedding planners, stationery designers, and Etsy sellers.

## Token

Requires a Neta API token (free trial at <https://www.neta.art/open/>). Pass it via the `--token` flag.

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## When to use
Use when someone asks to generate or create ai wedding invitation design generator images.

## Quick start
```bash
node weddinginvitationgenerator.js "your description here" --token YOUR_TOKEN
```

## Options
- `--size` — `portrait`, `landscape`, `square`, `tall` (default: `portrait`)
- `--ref` — reference image UUID for style inheritance

## Install
```bash
npx skills add omactiengartelle/wedding-invitation-generator
```
