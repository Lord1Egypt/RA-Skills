# AI Wallpaper Generator

> Powered by the **Neta AI image generation API** (`api.talesofai.com`) — the same service as [neta.art](https://www.neta.art/open/).

Generate stunning AI-powered wallpaper images from a text description in seconds. Powered by the Neta talesofai API, this skill returns a direct image URL you can use anywhere.

---

## Install

**Via npx skills:**
```bash
npx skills add BarbaraLedbettergq/wallpaper-claw-skill
```

**Via ClawHub:**
```bash
clawhub install wallpaper-claw-skill
```

---

## Usage

```bash
# Use the default prompt
node wallpaperclaw.js

# Custom prompt
node wallpaperclaw.js "misty mountain range at golden hour"

# Specify size
node wallpaperclaw.js "cyberpunk city at night" --size landscape

# Use a reference image UUID
node wallpaperclaw.js "same style, different scene" --ref <picture_uuid>

# Pass token directly
node wallpaperclaw.js "aurora borealis over a frozen lake" --token YOUR_TOKEN
```

The script prints a single image URL to stdout on success.

---

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--size` | `square`, `portrait`, `landscape`, `tall` | `landscape` | Output image dimensions |
| `--style` | `anime`, `cinematic`, `realistic` | `cinematic` | Visual style (passed in prompt) |
| `--ref` | `<picture_uuid>` | — | Reference image UUID for style inheritance |
| `--token` | `<token>` | — | Override token resolution |

### Size reference

| Name | Dimensions |
|------|------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

---

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Example Output

![Generated example](https://cdn.talesofai.com/picture/951f5a91-9be2-4af1-8429-8c79e786798d.webp)
