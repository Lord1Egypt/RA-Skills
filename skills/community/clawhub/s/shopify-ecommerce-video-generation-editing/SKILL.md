---
name: shopify-ecommerce-video-generation-editing
description: "Create and edit Shopify PDP videos, homepage hero loops, DTC product stories, collection clips and paid-social adaptations. Use this skill for Shopify商品视频、独立站PDP视频、Hero Video、产品演示、DTC品牌故事、Meta Ads/Reels素材、邮件落地页和多市场本地化；supports generation, reference, editing, extension and AI Hive delivery."
---

# Shopify Ecommerce Video Generation and Editing

Design a reusable video system for a DTC storefront. One source product story should produce different cuts for the PDP, homepage, collection, paid social and retention channels without changing product facts or brand voice.

## Channel jobs

| Placement | Primary job |
|---|---|
| PDP video | show operation, scale and proof |
| Homepage hero | express brand promise quickly and silently |
| Collection clip | distinguish product families |
| Paid social | test one audience/problem/benefit |
| Email landing | re-engage with a focused use case |

Start with product truth, approved claims, brand motion references, site layout, required crops and loading constraints. Do not create fake testimonials, offers or results.

## Scenarios and commands

### 1. PDP product demonstration

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt 'Shopify PDP product demo. Preserve exact product, packaging, color and included items. Show full item, correct setup, one tactile detail and the real use result in a clean continuous sequence. Designed to work without sound, with room for approved captions. No price, testimonial or unsupported claim.'
```

### 2. Silent homepage hero loop

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Wide silent-loop Shopify homepage hero for a minimalist home brand: begin and end on compatible compositions, one elegant product action, restrained camera movement, clean left-side headline space, no spoken dependency, no rapid cuts, no generated copy or offer.'
```

### 3. Adapt a brand master to paid social

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/brand-master.mp4 \
  --prompt 'Create a vertical paid-social cut from the approved DTC master. Keep product, models, brand look and factual demonstration; open with the strongest use action, shorten decorative shots, add one close proof moment and reserve final CTA space. Do not add a review, sale or new claim.'
```

### 4. Match a storefront motion system

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/motion-reference.mp4 \
  --image /path/to/new-product.png \
  --prompt 'Use the reference only for transition softness, camera restraint and pacing. Create an original Shopify collection clip for the new product, preserving exact SKU and brand palette. Do not copy reference product, model, text, soundtrack or campaign concept.'
```

### 5. Extend for a product-detail proof

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/short-hero.mp4 \
  --prompt 'Continue the current product action with a close-up that proves material or mechanism, then return to a composition that can loop into the first frame. Maintain model, product, lighting and set continuity; introduce no new feature.'
```

## QA and handoff

- Product and brand remain consistent across all channel cuts.
- PDP version explains use; hero version works silently and crops safely.
- Loop endpoints do not visibly jump when intended for autoplay.
- Paid variants record audience, hook, proof and CTA hypothesis.
- No generated price, testimonial, certification, warranty or performance claim.
- Export and verify against the current theme, storefront performance and ad requirements.

## Runtime

`t2v`, `i2v`, `r2v`, `edit` and `extend` map to Seedance 2.5 endpoints.

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name shopify-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use media arguments, model parameters, routing, output directory and submit-only mode as needed. Confirm live AI Hive configuration and pricing before rendering channel variants.
