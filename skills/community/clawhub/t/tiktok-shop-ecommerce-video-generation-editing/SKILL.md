---
name: tiktok-shop-ecommerce-video-generation-editing
description: "Create and edit TikTok Shop product-page videos, seller demonstration masters, affiliate creator kits, livestream clips and localized marketplace versions. Use this skill for TikTok Shop商品视频、商品页演示、Seller Center素材、Affiliate带货素材、直播商品视频、多市场本地化和跨境电商视频；supports AI Hive Seedance workflows."
---

# TikTok Shop Ecommerce Video Generation and Editing

Create a seller-controlled product truth master that can feed product pages, affiliates, livestreams and ads. This Skill focuses on commerce assets and localization, not on promising viral performance.

## Seller master brief

Collect SKU, package contents, correct use, visible feature proof, target market, language, creator permissions, approved claims, offer ownership and prohibited statements. Keep product truth constant while channel structure changes.

## Scenarios and commands

### 1. Product-page demonstration

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt 'TikTok Shop product-page video preserving exact SKU, package, color, logo and included items. Show complete item, correct setup, one close feature proof and final use context in a clear sound-off sequence. No price, voucher, rating, certification or unsupported result.'
```

### 2. Affiliate creator kit master

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Create a TikTok Shop affiliate B-roll master: accurate product cut-in, in-hand scale, setup, material close-up and finished use, each as a clean reusable shot. Do not generate a creator face, testimonial, dialogue, offer or commission claim.'
```

### 3. Localize for Indonesia

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/seller-master.mp4 \
  --prompt 'Localize the seller master for Indonesia. Preserve SKU, demonstration, package and commercial facts; adapt home context and reserve areas for approved Bahasa Indonesia captions. Remove old-market text and leave price, voucher, warranty and certification blank.'
```

### 4. Livestream demonstration segment

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/product-intro.mp4 \
  --prompt 'Continue into a livestream-ready product demonstration: show one full operation, one close proof and package contents, with natural pause points for a host. Maintain product and hands; do not add host speech, offer, countdown, sold count or gift.'
```

### 5. Reference creator pacing without copying

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/creator-pacing.mp4 \
  --image /path/to/product.png \
  --prompt 'Use the reference only for shot length and hand-demo rhythm. Create original seller-controlled footage for the supplied product. Do not copy creator, voice, dialogue, music, brand, product, claim or exact shot composition.'
```

## Commerce QA

- Product page, affiliate, live and localized versions share exact SKU truth.
- Every benefit has visible proof or merchant-approved support.
- Creator identity and endorsement are not synthesized.
- Prices, vouchers, tags and marketplace UI remain external overlays.
- Local language and commercial facts receive native review.
- Check current TikTok Shop market and advertising rules.

## Runtime

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name tiktok-shop-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use Seedance 2.5 text, image, reference, edit or extend modes with media, live parameters, routing and output controls.
