---
name: shopee-ecommerce-image-generation-editing
description: "Create and edit Shopee product listing images, variant galleries, package-content visuals, localized campaign bases and livestream product cards for Southeast Asian markets. Use this skill for Shopee商品图、虾皮主图、跨境Listing、SKU套图、多语言详情图、直播商品图、活动底图和东南亚本地化；supports AI Hive generation."
---

# Shopee Ecommerce Image Generation and Editing

Build mobile-first images for specific Shopee marketplaces without mixing language, currency, variant or package facts. Indonesia, Thailand, Vietnam, Malaysia, the Philippines, Singapore and Taiwan require separate market records and native review.

## Marketplace record

Record market, language, SKU, package, variant, materials, approved benefit, units, seller-approved offer and prohibited statements. Keep offer/UI elements separate from the generated image so prices, vouchers and badges remain current.

## Scenarios and commands

### 1. Shopee listing primary

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Shopee listing primary image for the verified SKU. Preserve exact product, variant color, retail package, logo and included pieces. Show item large and clear for mobile browse, clean background and realistic shadow. No voucher, flash-sale price, rating, sold count, seller badge or text.' \
  --image /path/to/sku.png
```

### 2. Gallery for product understanding

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create four Shopee gallery images: complete product, package contents, one correct use action and one feature close-up. Keep the same SKU, lighting and brand system, with empty areas for approved local copy. Do not invent specifications, reviews or offer information.' \
  --image /path/to/product.png \
  --batch 4
```

### 3. Livestream product card

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Vertical Shopee livestream product card: accurate product and package recognizable at small size, one visible detail, clean regions for seller-approved name and offer overlay. Do not generate price, voucher, countdown, sold count, rating, host quote or platform UI.' \
  --image /path/to/product.png
```

### 4. Market localization bases

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create Indonesian and Thai lifestyle bases for the same Shopee SKU. Preserve product, package and use method; adapt household context and caption-safe layout only. Leave language, currency, units, warranty and offer blank for local teams.' \
  --image /path/to/product.png \
  --batch 2
```

### 5. Campaign creative without fake sale

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Shopee campaign image base with accurate product on the right, energetic mobile-commerce shapes and blank left-side zones for approved event, voucher and CTA. Do not generate a campaign logo, discount, price, countdown, free shipping claim or platform badge.' \
  --image /path/to/product.png
```

## Marketplace QA

- Market, language, currency placeholder, SKU and package remain linked.
- Product and use method are unchanged across localization.
- Vouchers, prices, ratings, sold counts and UI are added in official workflows.
- Native reviewers proofread all local copy and units.
- No generated offer, seller badge, warranty or platform endorsement.
- Check current Shopee seller and campaign rules per marketplace.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name shopee-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

Use reference images, batch, live model parameters, routing and submit-only mode. Validate one marketplace before scaling.
