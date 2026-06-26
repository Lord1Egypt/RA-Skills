# Surreal Art Generator

Generate jaw-dropping surreal AI art from text descriptions — Dali-style melting clocks, Magritte-inspired floating objects, dreamlike landscapes, absurdist scenes, impossible architecture, and bizarre creature mashups. Just describe the scene you want and the skill renders it as a high-resolution image. Perfect for viral social posts, album covers, gallery prints, concept art, and TikTok-friendly weird-internet aesthetics.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/surreal-art-generator
```

Or with ClawHub:

```bash
clawhub install surreal-art-generator
```

## Usage

```bash
node surrealartgenerator.js "a giraffe wearing a tuxedo riding a bicycle through Times Square" --token YOUR_TOKEN
```

More examples:

```bash
# Melting cathedral on the moon
node surrealartgenerator.js "a melting gothic cathedral floating above the lunar surface" --token YOUR_TOKEN

# Landscape orientation
node surrealartgenerator.js "an ocean of clouds with whales swimming through skyscrapers" --size landscape --token YOUR_TOKEN

# Style inheritance from a reference image
node surrealartgenerator.js "a clockwork octopus in a victorian library" --ref 9c1f3a2b-... --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| (positional) | The text prompt describing the surreal scene | — |
| `--size` | Image size: `square`, `portrait`, `landscape`, `tall` | `square` |
| `--token` | Your Neta API token | required |
| `--ref` | Reference image UUID for style inheritance | none |

### Sizes

| Name | Dimensions |
| --- | --- |
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Output

Returns a direct image URL.

## Token setup

This skill needs a Neta API token. Get one (free trial) at <https://www.neta.art/open/>.

Pass the token to the script with the `--token` flag:

```bash
node surrealartgenerator.js "your prompt" --token YOUR_TOKEN
```

You can also expand it from a shell variable:

```bash
node surrealartgenerator.js "your prompt" --token "$NETA_TOKEN"
```

This skill requires a Neta API token (free trial available at https://www.neta.art/open/).
