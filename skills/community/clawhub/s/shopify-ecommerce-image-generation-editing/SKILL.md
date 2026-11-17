---
name: shopify-ecommerce-image-generation-editing
description: "Create and edit Shopify product photography, PDP image galleries, collection banners, DTC lifestyle images and campaign creatives. Use this skill for Shopify商品图、独立站PDP、Hero Image、产品套图、DTC品牌视觉、Meta Ads素材、邮件营销、换背景、多市场本地化和批量SKU；supports reference-guided generation through AI Hive."
---

# Shopify Ecommerce Image Generation and Editing

Build a coherent image system across a Shopify storefront instead of isolated product renders. The same product should remain accurate across PDP, collection, homepage, email and paid social placements while composition changes for each channel.

## Brand and product lock

Gather product angles, packaging, variants, dimensions, materials, brand colors, typography direction, audience, approved claims and current storefront examples. Define non-negotiables: product shape, logo, color, included items and any visual identity that must remain consistent.

## Storefront image architecture

| Placement | Job | Composition |
|---|---|---|
| PDP primary | identify the product | clean, accurate, distraction-free |
| PDP gallery | answer objections | detail, scale, use and variants |
| Collection card | compare products | consistent angle and crop |
| Homepage hero | express brand promise | product plus lifestyle context |
| Paid social | earn attention | one audience and one benefit |
| Email/SMS | support a campaign | clear offer-safe layout space |

## Scenarios and commands

### 1. PDP gallery system

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a 5-image Shopify PDP gallery using the reference product: clean primary image, material close-up, scale-in-hand image, real use scene and packaging contents. Preserve exact product shape, color, logo and accessories across every image. Use one coherent lighting system and do not invent dimensions, claims or included items.' \
  --image /path/to/product-front.png \
  --image /path/to/product-side.png \
  --batch 5
```

### 2. Collection-card consistency

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a Shopify collection-card image for the supplied SKU. Match the reference collection angle, subject scale, background tone and shadow; replace only the product with this accurate SKU. Keep packaging and logo unchanged, with enough crop tolerance for responsive storefront cards.' \
  --image /path/to/new-sku.png \
  --image /path/to/collection-style.png
```

### 3. DTC homepage hero

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Wide Shopify homepage hero for a minimalist home brand. Place the accurate reference product in a credible morning routine, build a strong focal point on the right and reserve calm negative space on the left for approved headline and button. Preserve product details; no generated offer, testimonial or claim.' \
  --image /path/to/product.png
```

### 4. Meta Ads creative directions

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Generate 3 paid-social creative hypotheses for the same DTC product: problem-in-context, hands-on demonstration and material proof. Keep product and brand system consistent, but change the customer reason to stop. Reserve safe copy space and do not invent a discount, review, result or certification.' \
  --image /path/to/product.png \
  --batch 3
```

### 5. Multi-market lifestyle adaptation

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Adapt the reference lifestyle image for a Japanese urban apartment while preserving the exact product and brand color. Change only the environment, styling and available negative space; keep the use case realistic and culturally neutral. Remove old campaign copy and leave clean space for approved Japanese localization.' \
  --image /path/to/source-campaign.jpg
```

## QA and asset handoff

- Product, logo, packaging, variants and included items remain consistent.
- PDP images answer different questions instead of repeating the same beauty shot.
- Collection cards align in angle, scale, background and crop behavior.
- Responsive crops retain the product and intended copy space.
- No generated offer, review, claim, certification or legal text.
- Deliver filenames by product handle, placement, market and version; verify current Shopify theme and ad-channel requirements.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name shopify-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

The fixed image model is `public_model_nano_banana_pro`. `generate` supports repeatable `--image`, `--batch`, model `--param`, routing, output directory and submit-only mode. Use live AI Hive pricing and parameters.
