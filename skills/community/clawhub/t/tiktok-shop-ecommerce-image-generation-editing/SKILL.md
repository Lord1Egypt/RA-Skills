---
name: tiktok-shop-ecommerce-image-generation-editing
description: "Create and edit TikTok Shop product listing images, shoppable-video covers, affiliate creator packs and livestream product visuals. Use this skill for TikTok Shop商品图、TikTok带货封面、商品卡、UGC素材包、直播间商品图、跨境电商主图、多市场本地化和商品换背景；supports reference-guided image generation and AI Hive delivery."
---

# TikTok Shop Ecommerce Image Generation and Editing

Create a connected image set for the TikTok Shop purchase journey: a shopper may first see a creator cover, then a product card, then listing details or a livestream. Keep the SKU identical across every touchpoint while changing composition for the placement.

## Merchant source sheet

Collect exact SKU, product angles, packaging, variants, included items, approved claims, target market, language, creator brief and offer copy. Product facts belong to the merchant; never generate a discount, rating, certification, scarcity message or result.

## Asset map

| Placement | Image job |
|---|---|
| Product listing | identify the exact item and variant |
| Shoppable cover | stop scrolling with one real use case |
| Creator pack | provide accurate cutouts and lifestyle options |
| Livestream card | recognize the product at small size |
| Ad test | test one audience or benefit per version |

## Scenarios and commands

### 1. Listing primary image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'TikTok Shop product listing primary image for the supplied SKU. Preserve exact shape, packaging, logo, color and included items. Center the complete product on a clean background with realistic shadow and mobile-size clarity. Do not add price, voucher, rating, certification, platform badge or unprovided text.' \
  --image /path/to/product-front.png \
  --image /path/to/package.png
```

### 2. Shoppable-video cover

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Vertical TikTok Shop shoppable-video cover. Keep the reference product accurate and show it already being used in one recognizable everyday situation. Strong hand action and clear product focus, clean upper title area, safe edge spacing, native phone-content feel rather than a studio poster. No unsupported result or offer.' \
  --image /path/to/product.png
```

### 3. Affiliate creator asset pack

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create 4 accurate creator-ready images for the same TikTok Shop product: clean cutout, in-hand scale, key-detail close-up and natural home use. Preserve product and packaging across all images; give creators useful negative space without generating dialogue, testimonial, discount or claim.' \
  --image /path/to/product.png \
  --batch 4
```

### 4. Livestream product card

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'TikTok Shop livestream product card: exact SKU shown large and readable on a compact vertical composition, one visible feature detail, high contrast against the background, reserved area for seller-approved offer text. Do not generate price, countdown, sold count, voucher or host endorsement.' \
  --image /path/to/product.png
```

### 5. Market-localized lifestyle image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Adapt the product lifestyle image for a Thai urban customer while preserving exact product, packaging and commercial facts. Change environment, styling and clean caption area only. Remove old market copy; do not translate or invent warranty, compatibility, certification or price information.' \
  --image /path/to/source-market-image.jpg
```

## QA

- SKU, variant, package contents, color and logo match merchant inputs.
- Product remains recognizable in listing, cover and livestream crops.
- Creator assets show usable actions without fabricating testimony.
- Localization changes context and copy space, not product facts.
- No model-generated voucher, rating, price, badge, certification or scarcity.
- Review current TikTok Shop rules for the target market before upload.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name tiktok-shop-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

The CLI fixes `public_model_nano_banana_pro` and supports repeatable `--image`, `--batch`, `--param`, `--routing`, `--output-dir` and `--no-download`. Use live AI Hive parameters and pricing; query the original task after timeout.
