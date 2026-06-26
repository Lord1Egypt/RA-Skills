# Scan to Skill

Scan a QR code and install the referenced ClawHub skill automatically.

## What it does

`scan-to-skill` provides a one-flow QR installer and supports auto-trigger flows in chat:

1. decode QR from image/screenshot
2. parse target skill slug
3. run `clawhub install <slug>`
4. return install result

## Supported QR payloads

- plain slug: `skill-feed`
- ClawHub URL: `https://clawhub.ai/<slug>` or `https://clawhub.ai/<owner>/<slug>`
- install text: `clawhub install <slug>`

## Quick start

```bash
# decode only
python3 scripts/install_from_qr.py --decode-only <image_path>

# decode + install
python3 scripts/install_from_qr.py <image_path>

# custom install dir
python3 scripts/install_from_qr.py <image_path> --dir skills
```

## Safety behavior

- Only auto-installs when payload resolves to a valid slug
- Non-ClawHub URLs are not auto-installed
- Unsupported payloads are rejected with clear error messages

## Project structure

- `SKILL.md` – workflow and safety policy
- `scripts/install_from_qr.py` – decoder + installer
- `references/slug-parsing.md` – parsing rules

## Install this skill

```bash
clawhub install scan-to-skill
```

## Decoder fallback

The script tries OpenCV first, then falls back to `zbarimg`.
