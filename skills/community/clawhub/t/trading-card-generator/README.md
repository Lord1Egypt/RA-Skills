# Trading Card Generator

Generate custom collectible trading card art from text descriptions — fantasy TCG cards, spell cards, character cards, monster cards, and original card illustrations in MTG, Pokemon, Yu-Gi-Oh, and sports card styles. Describe your creature, hero, or scene in plain English and the skill produces a finished image with ornate borders, dramatic painterly compositions, and premium foil-style finishes.

Powered by the Neta AI image generation API (api.talesofai.com) — the same service as neta.art/open.

## Install

Via skills CLI:

```bash
npx skills add omactiengartelle/trading-card-generator
```

Via ClawHub:

```bash
clawhub install trading-card-generator
```

## Usage

```bash
node tradingcardgenerator.js "your description here" --token YOUR_TOKEN
```

### Examples

Generate a fantasy creature card:

```bash
node tradingcardgenerator.js "ancient red dragon perched on a mountain of gold, glowing eyes, fire breath" --token YOUR_TOKEN
```

A landscape spell card:

```bash
node tradingcardgenerator.js "arcane lightning storm over a ruined castle" --size landscape --token YOUR_TOKEN
```

Inherit style from a reference card:

```bash
node tradingcardgenerator.js "elven archer in moonlit forest" --ref 1234abcd-... --token YOUR_TOKEN
```

## Options

| Flag | Description | Default |
| --- | --- | --- |
| `--token` | Neta API token (required) | — |
| `--size` | `portrait`, `landscape`, `square`, or `tall` | `portrait` |
| `--ref` | Reference image UUID for style inheritance | — |

### Sizes

| Name | Dimensions |
| --- | --- |
| `portrait` | 832 × 1216 |
| `landscape` | 1216 × 832 |
| `square` | 1024 × 1024 |
| `tall` | 704 × 1408 |

## Token setup

This skill requires a Neta API token (free trial available at <https://www.neta.art/open/>).

Pass it via the `--token` flag:

```bash
node <script> "your prompt" --token YOUR_TOKEN
```

## Output

Returns a direct image URL.

