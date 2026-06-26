# Sticker Pack Generator

Generate custom stickers from text descriptions using AI. Describe any character, object, or expression and instantly receive WhatsApp-ready stickers, Telegram sticker pack art, emoji-style illustrations, and kawaii chibi characters — all from a simple text prompt.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via npx:
```bash
npx skills add omactiengartelle/sticker-pack-generator
```

Via ClawHub:
```bash
clawhub install sticker-pack-generator
```

## Usage

```bash
node stickerpackgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
# Cute chibi cat sticker
node stickerpackgenerator.js "A cute expressive sticker of a cat, white background, bold clean outlines, chibi style, vibrant colors, sticker art, no text" --token "$NETA_TOKEN"

# Reaction sticker — surprised face
node stickerpackgenerator.js "A cute expressive sticker of a surprised anime girl, white background, bold clean outlines, chibi style, vibrant colors, sticker art, no text" --token "$NETA_TOKEN"

# Kawaii food character
node stickerpackgenerator.js "A kawaii smiling ramen bowl character, white background, bold clean outlines, chibi style, sticker art, no text" --token "$NETA_TOKEN"

# Portrait size for tall sticker formats
node stickerpackgenerator.js "A cute bunny holding a heart, white background, chibi style, sticker art" --token "$NETA_TOKEN" --size portrait

# Style inheritance from a reference image
node stickerpackgenerator.js "A sleepy panda sticker, chibi style, white background" --token "$NETA_TOKEN" --ref <picture_uuid>
```

### Output

Returns a direct image URL.

## Options

| Flag | Values | Default | Description |
|------|--------|---------|-------------|
| `--token` | string | — | Your Neta API token (required) |
| `--size` | `square`, `portrait`, `landscape`, `tall` | `square` | Output image dimensions |
| `--ref` | UUID string | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Dimensions |
|------|------------|
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Token setup

A Neta API token is required. Get your free trial token at <https://www.neta.art/open/>.

Pass it with the `--token` flag:

```bash
node stickerpackgenerator.js "a cute dog sticker" --token YOUR_TOKEN
```

You can store it in a shell variable for convenience:

```bash
export NETA_TOKEN="your_token_here"
node stickerpackgenerator.js "a cute dog sticker" --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
