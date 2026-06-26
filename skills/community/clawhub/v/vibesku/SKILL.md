---
name: vibesku
description: |
  CLI for VibeSKU — an AI-powered creative automation platform that turns product SKU photos
  into professional e-commerce visuals and marketplace-ready copy at scale.
  Use when the user wants to: (1) generate hero banners, exploded-view infographics, detail page poster sets, or listing copy
  from product photos via the command line, (2) authenticate with VibeSKU (browser login or API key),
  (3) browse or inspect generation templates (ecom-hero, kv-image-set, exploded-view, listing),
  (4) refine AI-generated outputs with edit instructions, (5) export/download image and text results,
  (6) run batch generation across a product catalog, (7) manage credits (check balance, purchase, redeem),
  (8) configure CLI settings. Triggers on mentions of "vibesku", "product visuals", "SKU photos",
  "ecommerce images", "hero banner", "listing copy", "product image generation", "batch generation",
  "VisionKV", "exploded view", "product infographic", "component breakdown", "technical diagram",
  or any VibeSKU CLI workflow.
metadata:
  openclaw:
    requires:
      env:
        - VIBESKU_API_KEY
        - VIBESKU_BASE_URL
        - NO_COLOR
      bins:
        - node
      config:
        - ~/.vibesku/config.json
    primaryEnv: VIBESKU_API_KEY
    homepage: https://www.vibesku.com
---

# VibeSKU CLI

Command-line interface for [VibeSKU](https://www.vibesku.com) — AI-powered creative automation that turns product SKU photos into agency-grade e-commerce visuals and marketplace-ready copy in seconds.

## What VibeSKU Does

VibeSKU replaces manual creative production for e-commerce teams. Upload a product photo, define brand guidelines, and receive complete multi-format visual sets. Core capabilities: VisionKV™ visual system (complete visual collections from a single product), high-fidelity product restoration (1:1 precision on textures/logos/packaging), multilingual text overlays, and omni-channel format output.

**Credit costs**: 1K/2K image = 1 credit, 4K image = 2 credits, short video = 5 credits, copy = 1 credit.

## Setup

The CLI is bundled at `bin/vibesku.js` — self-contained Node.js script, zero dependencies (requires Node >= 18).

```bash
node <skill-dir>/bin/vibesku.js --help
alias vibesku="node <skill-dir>/bin/vibesku.js"   # optional
```

## Skill Version

- Source of truth: `VERSION`
- Local version: `cat VERSION`
- Upstream repo: [UllrAI/vibesku-agent](https://github.com/UllrAI/vibesku-agent)

For version checks and auto-update workflow, see [versioning.md](references/versioning.md).

## Authentication

Two methods, resolved in priority order:

1. **CLI token** (`vibesku auth login`) — browser-based device flow, tokens at `~/.vibesku/config.json`
2. **API key** — `VIBESKU_API_KEY` env var > config file key (from `vibesku init` or `vibesku config set-key`)

```bash
vibesku auth login                # Browser login (recommended)
vibesku init vsk_<key>            # API key for CI/CD
```

---

## Template Selection Guide

VibeSKU provides 4 templates. **Read the corresponding reference file before building the generate command.**

| Need | Template | Output | Cost | Reference |
|------|----------|--------|------|-----------|
| Single product image (main photo, banner, poster) | `ecom-hero` | IMAGE | 1-2 cr/img | [ecom-hero.md](references/ecom-hero.md) |
| Coordinated detail-page poster set | `kv-image-set` | IMAGE | 1-2 cr/img × scenes | [kv-image-set.md](references/kv-image-set.md) |
| Single technical exploded infographic | `exploded-view` | IMAGE | 1-2 cr/img | [exploded-view.md](references/exploded-view.md) |
| Product listing copy (title, bullets, description) | `listing` | TEXT | 1 cr | [listing.md](references/listing.md) |

### Decision Tree

```
User wants visuals?
├── Technical exploded infographic → exploded-view
│   ├── Balanced callouts (default) → labelPlacement: balanced-callout
│   ├── Cleaner visual without labels → labelPlacement: none
│   └── Category-aware environment → backgroundMode: product-matched-scene
├── Single image (hero/banner/poster) → ecom-hero
│   ├── Product main photo → scenario: MAIN_IMAGE, aspectRatio: 1:1
│   ├── Marketing banner  → scenario: BANNER, aspectRatio: 16:9
│   └── Vertical poster   → scenario: POSTER, aspectRatio: 3:4
└── Multiple coordinated images → kv-image-set
    ├── Full detail page     → scenes: [kv-hero, lifestyle, detail-01, specs-table, ...]
    ├── Quick hero + lifestyle → scenes: [kv-hero, lifestyle]
    └── Brand storytelling   → scenes: [kv-hero, brand-story, user-review]

User wants text?
└── Product listing copy → listing
    ├── Amazon  → templateName: AMAZON_LISTING
    ├── Taobao  → templateName: TAOBAO_DETAIL
    ├── Shopify → templateName: SHOPIFY_DESC
    └── General → templateName: GENERIC
```

### Quick Style Matching (image templates)

| Product Type | ecom-hero `style` | kv-image-set `style` | exploded-view `style` |
|-------------|-------------------|---------------------|------------------------|
| Electronics, gadgets | `tech` | `tech-future` | `premium-technical` |
| Luxury, high-end | `premium` | `magazine` | `morandi-editorial` |
| Food, home goods | `lifestyle` | `retro-film` | `lifestyle-soft` |
| Organic, eco-friendly | `organic` | `organic-nature` | `material-focus` |
| Fashion, beauty | `minimal` | `nordic-minimal` | `studio-minimal` |
| Kids, sports, bold | `vibrant` | `cyberpunk` | `auto` (recommended) |
| Artisan, handmade | `studio` | `watercolor` | `material-focus` |
| Unsure / let AI decide | `auto` (default) | `auto` (default) | `auto` (default) |

---

## Typical Workflow

```bash
vibesku auth login                              # 1. Authenticate
vibesku templates                               # 2. Browse templates
vibesku templates info exploded-view            # 3. Inspect template details (optional)
vibesku credits                                 # 4. Check balance
vibesku generate -t ecom-hero \
  -n "Wireless Headphones" \
  -i product.jpg -l logo.png \
  -b "AudioTech"                                # 5. Generate visuals
vibesku status <job-id> --watch                 # 6. Monitor until complete
vibesku refine <output-uuid> -p "brighter bg"   # 7. Refine (optional)
vibesku export <job-id> -o ./output             # 8. Download results
```

## Commands Quick Reference

| Command | Purpose |
|---------|---------|
| `vibesku auth login\|logout\|status\|refresh` | Authentication management |
| `vibesku init <api-key>` | Initialize with API key |
| `vibesku config set-key\|set-url\|show\|reset` | CLI configuration |
| `vibesku templates [info <id>]` | List / inspect templates |
| `vibesku generate -t <id> [options]` | Generate visuals or copy |
| `vibesku refine <output-id> -p <prompt>` | Refine output with edit instructions |
| `vibesku status <job-id> [--watch]` | Check job progress |
| `vibesku jobs [-p <page>] [-t <template>]` | List jobs |
| `vibesku export <job-id> [-o <dir>]` | Download outputs |
| `vibesku batch <file> [--dry-run]` | Bulk generation from JSON |
| `vibesku credits [show\|buy\|redeem <code>]` | Credit management |

All commands support `--json` for machine-readable output. Full details: [commands.md](references/commands.md)

## Key Behaviors

- **Asset upload**: `-i` auto-uploads product images; `-l` uploads logo
- **Modify vs Regenerate**: Use `vibesku refine <output-id> -p "<instruction>"` to edit existing output. Use `vibesku generate` only for new creations.
- **Full UUID required for refine**: Use `vibesku status <job-id> --json` to get complete output UUIDs (table view truncates them).
- **Agent-friendly output**: Prefer `--json` flag for all commands when used by AI agents.
- **Version drift check (recommended triggers)**: Compare local `VERSION` with upstream when any of these happen: unknown template/option error, template mismatch with `vibesku templates --json`, user asks for newly added capability, or local check is older than 7 days (recommended cadence). If issues occur during execution, prioritize this check before retrying generation/refine commands. Follow [versioning.md](references/versioning.md).
- **Auto-update when outdated (recommended)**: If upstream version is newer, update skill first, then continue the user task with the updated skill.
- **Watch mode**: `--watch` polls every 5s until all runs complete.
- **Credit tracking**: Generation and refine show remaining balance on success.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `VIBESKU_API_KEY` | API key (overrides config file) |
| `VIBESKU_BASE_URL` | Custom API URL (overrides config file) |
| `NO_COLOR` | Disable colored output |
