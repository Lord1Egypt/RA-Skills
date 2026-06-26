# Wedding Invitation Generator

Design elegant AI wedding invitations, save-the-dates, RSVP cards, bridal shower invites, and engagement announcements from text descriptions. Generate beautiful watercolor florals, botanical illustrations, minimalist modern layouts, rustic barn themes, romantic garden scenes, boho chic designs, classic gold-accented stationery, and custom wedding suite artwork — all from a short prompt describing the style you want.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

```bash
npx skills add omactiengartelle/wedding-invitation-generator
```

Or via ClawHub:

```bash
clawhub install wedding-invitation-generator
```

## Usage

```bash
node weddinginvitationgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate an elegant watercolor floral invitation:

```bash
node weddinginvitationgenerator.js \
  "elegant wedding invitation design, soft watercolor botanical florals in blush pink and ivory, delicate gold foil accents, romantic garden aesthetic, cream paper texture" \
  --token YOUR_TOKEN
```

Minimalist modern save-the-date in landscape:

```bash
node weddinginvitationgenerator.js \
  "minimalist modern save-the-date card, clean typography, single sprig of eucalyptus, soft beige background, refined stationery" \
  --size landscape \
  --token YOUR_TOKEN
```

Rustic barn-themed engagement announcement with a reference image:

```bash
node weddinginvitationgenerator.js \
  "rustic barn wedding engagement announcement, warm earth tones, wildflowers, kraft paper texture, hand-lettered script" \
  --ref 123e4567-e89b-12d3-a456-426614174000 \
  --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `<prompt>` (positional) | Text description of the invitation you want | built-in wedding prompt |
| `--size` | `portrait`, `landscape`, `square`, or `tall` | `portrait` |
| `--token` | Your Neta API token (required) | — |
| `--ref` | Reference image UUID for style inheritance | — |

### Size dimensions

| Size | Width × Height |
| --- | --- |
| `square` | 1024 × 1024 |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `tall` | 704 × 1408 |

## Output

Returns a direct image URL.

## Token setup

This skill requires a Neta API token. You can get a free trial token at <https://www.neta.art/open/>.

Pass your token on every invocation using the `--token` flag:

```bash
node weddinginvitationgenerator.js "your prompt" --token YOUR_TOKEN
```

Shell expansion works if you prefer to keep the token in your shell session:

```bash
node weddinginvitationgenerator.js "your prompt" --token "$NETA_TOKEN"
```

The `--token` flag is the only way to provide your token to this script.

