---
name: skill-qr-card
description: Generate styled QR images/cards for ClawHub skills so users can scan and install instantly. Supports install-command payloads, ClawHub links, and GitHub links, with share-ready outputs (SVG/PNG). Use when users ask for “scan to install” visuals, QR sharing assets, or branded QR variants for skill distribution.
---

# Skill QR Card

Create a styled QR card (SVG or PNG) that users can scan to install a skill instantly.

## Workflow

1. Collect inputs
   - skill slug (required)
   - display title (optional)
   - target payload mode: install command / ClawHub URL / README URL
2. Generate QR card
   - Use `scripts/generate_qr_card.js`.
3. Return output files
   - SVG (always)
   - PNG (optional if ImageMagick `convert` is available)
4. Share result
   - Send generated image path directly.

## Commands

- Basic:
  - `node scripts/generate_qr_card.js --slug skill-feed`
- Custom title + mode:
  - `node scripts/generate_qr_card.js --slug skill-feed --title "SkillFeed" --mode install`
- Custom output:
  - `node scripts/generate_qr_card.js --slug skill-feed --out ./images/skillfeed-card.svg`

## Modes

- `install` (default): QR payload = `clawhub install <slug>`
- `clawhub`: QR payload = `https://clawhub.ai/<slug>`
- `github`: QR payload = `https://github.com/<owner>/<repo>` (requires `--github`)

## Output

- `MEDIA:./images/<file>.svg` line is printed for quick sharing.
- Optional PNG is generated when system has `convert` installed.

## References

- Styling and payload conventions: `references/design-guidelines.md`
