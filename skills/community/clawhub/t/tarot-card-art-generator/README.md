# Tarot Card Art Generator

Generate stunning AI tarot card art and mystical oracle deck illustrations from text descriptions. Create custom major and minor arcana designs, divination card artwork, spiritual deck imagery, occult-themed illustrations, and fortune card visuals with ornate borders and rich symbolism.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/tarot-card-art-generator
```

or

```bash
clawhub install tarot-card-art-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

Generate a tarot card with the default mystical style:

```bash
node tarotcardartgenerator.js "The High Priestess seated between two pillars, moonlight illuminating ancient scrolls, deep blue and silver palette" --token YOUR_TOKEN
```

Generate a landscape-oriented card:

```bash
node tarotcardartgenerator.js "The Fool stepping off a cliff into a field of stars, whimsical art nouveau style" --size landscape --token YOUR_TOKEN
```

Use a reference image for style inheritance:

```bash
node tarotcardartgenerator.js "The Tower struck by lightning, dramatic chiaroscuro" --ref PICTURE_UUID --token YOUR_TOKEN
```

Returns a direct image URL.

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--token` | Neta API token (required) | — |
| `--size` | Image size: `portrait`, `landscape`, `square`, `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Size Dimensions

| Size | Dimensions |
|------|-----------|
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
