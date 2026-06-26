# Waifu Generator

Generate waifu and anime-style images from text descriptions using AI. Describe the character you want and get back a direct image URL instantly.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/waifu-gen-skill
```

Or via ClawHub:

```bash
clawhub install waifu-gen-skill
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

Basic generation with default portrait size:

```bash
node waifugen.js "anime waifu character, beautiful illustration, detailed artwork" --token YOUR_TOKEN
```

Generate a landscape image:

```bash
node waifugen.js "anime girl in a flower field, sunset background" --size landscape --token YOUR_TOKEN
```

Use a reference image UUID for style inheritance:

```bash
node waifugen.js "elegant waifu, flowing hair, fantasy style" --ref PICTURE_UUID --token YOUR_TOKEN
```

Returns a direct image URL.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size Dimensions

| Size | Width | Height |
|------|-------|--------|
| `square` | 1024 | 1024 |
| `portrait` | 832 | 1216 |
| `landscape` | 1216 | 832 |
| `tall` | 704 | 1408 |

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
