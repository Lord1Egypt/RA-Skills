# Snapchat Filter Art Generator

Generate nostalgic selfie photos from text descriptions, complete with iconic Snapchat-style filters — puppy ears, flower crowns, dog tongues, sparkle overlays, and bunny noses. Perfect for the viral "2026 is the new 2016" throwback trend, early-iPhone aesthetic recreations, blown-out flash selfies, low-res phone camera vibes, TikTok throwback content, Instagram nostalgia posts, Y2K-adjacent filter art, and 2010s social media aesthetic recreations.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via the skills CLI:

```bash
npx skills add omactiengartelle/snapchat-filter-art-generator
```

Or via ClawHub:

```bash
clawhub install snapchat-filter-art-generator
```

## Token Setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Usage

Generate a default Snapchat-style throwback selfie:

```bash
node snapchatfilterartgenerator.js "selfie with puppy dog ears filter, blown-out flash, 2016 vibes" --token YOUR_TOKEN
```

Generate a flower crown selfie in landscape orientation:

```bash
node snapchatfilterartgenerator.js "mirror selfie with flower crown filter and sparkles, low-res iPhone aesthetic" --size landscape --token YOUR_TOKEN
```

Use a reference image UUID for style inheritance:

```bash
node snapchatfilterartgenerator.js "selfie with bunny nose filter" --ref abc123-uuid --token YOUR_TOKEN
```

## Options

| Flag       | Description                                                       | Default     |
|------------|-------------------------------------------------------------------|-------------|
| `--size`   | Image size: `portrait`, `landscape`, `square`, or `tall`          | `portrait`  |
| `--token`  | Neta API token (required)                                         | —           |
| `--ref`    | Reference image UUID for style inheritance                        | —           |
| `-h`, `--help` | Show help                                                     | —           |

### Size dimensions

| Size      | Width × Height |
|-----------|----------------|
| portrait  | 832 × 1216     |
| landscape | 1216 × 832     |
| square    | 1024 × 1024    |
| tall      | 704 × 1408     |

## Output

Returns a direct image URL.

## Example

```bash
$ node snapchatfilterartgenerator.js "selfie with dog tongue filter, blown-out flash, 2016 throwback" --token YOUR_TOKEN
→ Submitting task (832×1216)...
→ Task ... queued. Polling...
```

Returns a direct image URL.

