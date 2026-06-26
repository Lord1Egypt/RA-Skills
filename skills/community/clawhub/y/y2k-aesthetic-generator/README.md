# Y2K Aesthetic Generator

Generate nostalgic early-2000s and 2010s throwback images from text descriptions. Recreate the viral "2026 is the new 2016" trend with flash-photography selfies, Snapchat-era looks, low-res iPhone vibes, butterfly clips, frosted makeup, and dreamy mall-photo nostalgia — all from a prompt. Great for TikTok, Instagram Reels, profile pics, retro fashion moodboards, Y2K party invites, and nostalgia-core content.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/y2k-aesthetic-generator
```

Or via ClawHub:

```bash
clawhub install y2k-aesthetic-generator
```

## Usage

```bash
node y2kaestheticgenerator.js "Y2K aesthetic portrait, butterfly clips, frosted lip gloss, mall photo booth" --token YOUR_TOKEN
```

With a reference image UUID:

```bash
node y2kaestheticgenerator.js "early 2000s flash selfie, low-rise denim" --token YOUR_TOKEN --ref <picture_uuid>
```

Different size:

```bash
node y2kaestheticgenerator.js "2000s digital camera candid pose" --size landscape --token YOUR_TOKEN
```

## Options

| Option | Values | Default | Description |
| --- | --- | --- | --- |
| `--size` | `portrait`, `landscape`, `square`, `tall` | `portrait` | Output image aspect/size |
| `--token` | string | — | Neta API token (required) |
| `--ref` | picture UUID | — | Reference image UUID for style inheritance |

### Size dimensions

| Size | Dimensions |
| --- | --- |
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.

## Example

```bash
node y2kaestheticgenerator.js "Y2K aesthetic portrait, early 2000s flash, butterfly clips, frosted lip gloss, chunky sneakers, mall photo booth vibe" --token YOUR_TOKEN
```

Returns a direct image URL.

