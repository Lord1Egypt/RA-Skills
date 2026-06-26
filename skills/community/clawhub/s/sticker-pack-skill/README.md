# AI Sticker Pack Generator

Generate ai sticker pack generator images from text descriptions. Describe what you want and get back a direct image URL — no uploads, no local files, just a prompt and an image.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/sticker-pack-skill
```

or

```bash
clawhub install sticker-pack-skill
```

## Usage

```bash
node stickerpack.js "cute sticker design, white outline, transparent background ready" --token YOUR_TOKEN
```

```bash
node stickerpack.js "kawaii cat with sparkles, sticker sheet style" --token YOUR_TOKEN --size portrait
```

```bash
node stickerpack.js "retro pixel art sticker pack, bold colors" --token YOUR_TOKEN --ref PICTURE_UUID
```

Returns a direct image URL.

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image dimensions: `square`, `portrait`, `landscape`, `tall` | `square` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size reference

| Size | Dimensions |
|------|-----------|
| `square` | 1024 x 1024 |
| `portrait` | 832 x 1216 |
| `landscape` | 1216 x 832 |
| `tall` | 704 x 1408 |

## Token Setup

Get a free trial API token at [neta.art/open](https://www.neta.art/open/), then pass it with the `--token` flag:

```bash
node stickerpack.js "your prompt" --token YOUR_TOKEN
```

You can also use shell variable expansion for convenience:

```bash
export NETA_TOKEN="your-token-here"
node stickerpack.js "your prompt" --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
