# Skill QR Card

Generate a polished, shareable QR card image for any ClawHub skill.

## What it does

Skill QR Card creates visual QR assets that people can scan to:

- install a skill directly (`clawhub install <slug>`)
- open the skill on ClawHub
- open a GitHub repository

It is designed for "scan-to-install" sharing in chats, docs, and social posts.

## Features

- Styled QR card output (SVG)
- Optional PNG export (when ImageMagick `convert` is available)
- Multiple payload modes:
  - `install` (default)
  - `clawhub`
  - `github`
- Safe slug validation

## Quick start

```bash
cd skills/skill-qr-card

# Default: QR payload = clawhub install skill-feed
node scripts/generate_qr_card.js --slug skill-feed

# Use ClawHub URL payload
node scripts/generate_qr_card.js --slug skill-feed --mode clawhub

# Use GitHub URL payload
node scripts/generate_qr_card.js --slug skill-feed --mode github --github jackleeio/skill-feed
```

## Script options

```bash
node scripts/generate_qr_card.js \
  --slug <skill-slug> \
  [--title "Display Title"] \
  [--mode install|clawhub|github] \
  [--github <owner/repo>] \
  [--out ./images/custom.svg] \
  [--no-png]
```

## Output

- Main output: SVG card in `./images/`
- Optional output: PNG card (if `convert` exists)
- Script prints `MEDIA:./...` lines for direct chat attachment flows

## Project structure

- `SKILL.md` – skill workflow and usage
- `scripts/generate_qr_card.js` – QR card generator
- `references/design-guidelines.md` – visual and payload conventions

## Install from ClawHub

```bash
clawhub install skill-qr-card
```
