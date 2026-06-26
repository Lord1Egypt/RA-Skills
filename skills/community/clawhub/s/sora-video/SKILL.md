---
name: sora-video
description: "Generate, edit, extend, and manage AI videos using OpenAI's Sora 2 API. Includes marketing-ready prompt templates for product demos, social ads, brand spots, and launch teasers. Requires customer-provided OPENAI_API_KEY."
version: 1.0.0
dependencies: []
tags:
  - video
  - ai-generation
  - sora
  - marketing
  - content-creation
  - openai
---

# sora-video

AI video generation skill for Stomme AI customers using OpenAI's Sora 2 API. Wraps a production-grade Python CLI with marketing-focused prompt templates for business use cases.

## Prerequisites

### OpenAI API Key (Required)
Customers need their own `OPENAI_API_KEY` from OpenAI's platform:

1. Go to [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Create a new API key with video generation permissions
3. Set it as an environment variable: `export OPENAI_API_KEY="sk-..."`
4. Ensure your OpenAI organization has Sora API access enabled

> **Important:** A ChatGPT Pro/Plus subscription does NOT provide API access to Sora. You need a separate API key with pay-per-use billing from platform.openai.com.

### Python + uv
The CLI requires Python 3.10+ and uses `uv` for dependency management (auto-installs the `openai` SDK):
```bash
# Install uv if not present
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Pricing Guide

| Model | Duration | Approximate Cost |
|-------|----------|-----------------|
| sora-2 | 4s | ~$0.10 |
| sora-2 | 8s | ~$0.20 |
| sora-2 | 12-16s | ~$0.30 |
| sora-2 | 20s | ~$0.40 |
| sora-2-pro | 4s | ~$0.25 |
| sora-2-pro | 8s | ~$0.40 |
| sora-2-pro | 12-16s | ~$0.50 |
| sora-2-pro | 20s | ~$0.60 |

Costs are per video generation attempt. Failed or cancelled jobs are not billed. Prices are approximate and may change — check [OpenAI's pricing page](https://openai.com/api/pricing/) for current rates.

## When to Use
- Generate product demo videos from text descriptions
- Create social media ad clips (Instagram, TikTok, LinkedIn)
- Produce brand identity spots and launch teasers
- Edit or extend existing generated videos
- Create reusable non-human character references for brand mascots
- Batch-generate multiple video variants for A/B testing

## Decision Tree
- **Product demo** → use `templates/product-demo.md` template + `create`
- **Social ad** → use `templates/social-ads.md` template + `create` (4-8s)
- **Brand spot** → use `templates/brand-spots.md` template + `create` or `create-and-poll`
- **Launch teaser** → use `templates/launch-teaser.md` template + `create-and-poll`
- **Character-based shots** → `create-character` first, then `create` with character IDs
- **Edit existing video** → `edit` (one targeted change per iteration)
- **Extend existing video** → `extend` (continue timeline)
- **Batch variants** → `create-batch` with JSONL input
- **Check status** → `status` or `poll`
- **Download assets** → `download` (video/thumbnail/spritesheet)

## Workflow
1. Select a template from `templates/` matching the use case (or write a custom prompt).
2. Run the CLI via `scripts/sora.py` with appropriate flags.
3. For async jobs, poll until completion (or use `create-and-poll`).
4. Download assets before URLs expire (~1 hour).
5. Iterate with `edit` (targeted changes) or `extend` (timeline continuation).

## CLI Quick Start

Set the CLI path:
```bash
export SORA_CLI="<path-to-skill>/scripts/sora.py"
```

### Generate a video
```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Close-up of a premium smartwatch on marble surface" \
  --model sora-2 \
  --size 1280x720 \
  --seconds 8
```

### Generate and auto-download
```bash
uv run --with openai python "$SORA_CLI" create-and-poll \
  --prompt "Product hero shot of wireless earbuds" \
  --model sora-2-pro \
  --size 1920x1080 \
  --seconds 4 \
  --download \
  --out hero.mp4
```

### Dry-run (no API call)
```bash
python "$SORA_CLI" create --prompt "Test prompt" --dry-run
```

Full CLI reference: `references/cli.md`

## Authentication
- `OPENAI_API_KEY` must be set for live API calls.
- Never ask customers to paste their full key in chat — have them set it locally.
- If key is missing, guide them to [platform.openai.com/api-keys](https://platform.openai.com/api-keys).
- ChatGPT subscription OAuth tokens do NOT work (missing `api.videos.*` scopes).

## Models & Defaults
- **Default model:** `sora-2` (fast, flexible)
- **Premium model:** `sora-2-pro` (higher fidelity, required for 1080p)
- **Default size:** `1280x720`
- **Default duration:** `4` seconds
- **Allowed durations:** 4, 8, 12, 16, 20 seconds

### Size Support
| Model | Sizes |
|-------|-------|
| sora-2 | 1280x720, 720x1280 |
| sora-2-pro | 1280x720, 720x1280, 1024x1792, 1792x1024, 1920x1080, 1080x1920 |

## Prompt Augmentation
The CLI automatically reformats prompts into a structured production spec. Use CLI flags instead of writing long structured prompts:

```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Premium headphones on display" \
  --use-case "product teaser" \
  --scene "dark studio, soft haze" \
  --camera "85mm, slow orbit" \
  --lighting "soft key, gentle rim" \
  --seconds 8
```

If your prompt is already structured, add `--no-augment`.

## Marketing Templates
Ready-to-use prompt templates for common business video needs:

| Template | File | Best For |
|----------|------|----------|
| Product Demos | `templates/product-demo.md` | Product launches, feature showcases |
| Social Ads | `templates/social-ads.md` | Instagram, TikTok, LinkedIn clips |
| Brand Spots | `templates/brand-spots.md` | Brand identity, company culture |
| Launch Teasers | `templates/launch-teaser.md` | Pre-launch hype, coming soon |

## Guardrails (Enforced by API)
- Only content suitable for audiences under 18
- No copyrighted characters or music
- No real people (including public figures)
- Input images with human faces are rejected
- Character uploads are for non-human subjects only

## API Limitations
- Models: `sora-2` and `sora-2-pro` only
- Duration set via `seconds` parameter (4, 8, 12, 16, 20)
- Max 2 characters per generation
- Extensions: up to 20s each, 6 times max (120s total)
- Extensions do not support characters or image references
- Video creation is async — must poll for completion
- Download URLs expire after ~1 hour
- Content restrictions enforced server-side

## Reference Map
- **`references/cli.md`** — Full CLI command reference
- **`references/video-api.md`** — API parameters and endpoints
- **`references/prompting.md`** — Prompt engineering best practices
- **`references/troubleshooting.md`** — Common errors and fixes
- **`templates/product-demo.md`** — Product demo prompt templates
- **`templates/social-ads.md`** — Social ad prompt templates
- **`templates/brand-spots.md`** — Brand identity spot templates
- **`templates/launch-teaser.md`** — Launch teaser templates
