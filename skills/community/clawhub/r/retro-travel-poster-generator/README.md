# Retro Travel Poster Generator

Generate vintage-style travel posters from text descriptions, inspired by the golden age of tourism advertising (1920s–1960s WPA, art deco, mid-century modern). Describe any destination — national parks, beaches, cities, landmarks, exotic locales — and the skill produces a poster-style illustration with bold flat colors, stylized scenery, screen-printed texture, and nostalgic composition. Ideal for Etsy sellers, print-on-demand stores, wall art, home decor, postcards, travel agency branding, Airbnb listings, and retro aesthetic collections.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add blammectrappora/retro-travel-poster-generator
```

Or with ClawHub:

```bash
clawhub install retro-travel-poster-generator
```

## Usage

```bash
node retrotravelpostergenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

```bash
# Classic national park poster
node retrotravelpostergenerator.js "Yosemite Valley at sunset, granite cliffs, pine trees" --token YOUR_TOKEN

# Mid-century beach destination
node retrotravelpostergenerator.js "Santorini coastline, white buildings, blue domes" --size landscape --token YOUR_TOKEN

# City travel poster
node retrotravelpostergenerator.js "Paris Eiffel Tower at dusk, art deco style" --size portrait --token YOUR_TOKEN

# Use a reference image for consistent style
node retrotravelpostergenerator.js "Mount Fuji with cherry blossoms" --ref PICTURE_UUID --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--size` | Image dimensions: `portrait` (832×1216), `landscape` (1216×832), `square` (1024×1024), `tall` (704×1408) | `portrait` |
| `--token` | Your Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.

