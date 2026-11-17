---
name: shopee-ecommerce-video-generation-editing
description: "Create and edit Shopee product videos, localized demos, short-form ads and seller campaign assets for Southeast Asian markets. Use this skill for Shopee商品视频、虾皮跨境电商、Shopee Video、开箱演示、本地化带货、东南亚广告素材、多语言版本和批量SKU视频；supports generation, reference, editing and AI Hive delivery."
---

# Shopee Ecommerce Video Generation and Editing

Produce short, mobile-first product videos for Shopee sellers across Southeast Asian markets. Localize language and context while keeping the merchant’s product, variant, price logic and claims unchanged.

## Market brief

Record marketplace, language, customer segment, product variant, package contents, actual use steps, approved offer text, local creator style and destination placement. Indonesia, Thailand, Vietnam, Malaysia, the Philippines, Singapore and Taiwan should not share one generic localization.

## Video patterns

- **Fast product overview:** identify item, variant and key use.
- **Hands-on demo:** show setup and result without hidden cuts.
- **Unboxing:** verify package contents and first use.
- **Problem/solution:** connect one local use context to one supported benefit.
- **Seller campaign variant:** reserve offer space without inventing the offer.

## Scenarios and commands

### 1. Localized Shopee product overview

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product.jpg \
  --prompt '9:16 Shopee product video for Indonesia. Preserve the exact SKU, packaging, color, logo and included items. Start with a clear full-product view, show the main operation with hands, add one close-up proof and end with clean space for approved Bahasa Indonesia copy. Everyday local home context; no invented price, voucher, rating or claim.'
```

### 2. Package-contents unboxing

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Shopee mobile unboxing video based on the supplied package list: open the parcel continuously, place every included item in a clear row, show the first correct setup and final use. Do not add a free gift, accessory, seller badge, discount or reaction that was not provided.'
```

### 3. Adapt a master video for Thailand

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/regional-master.mp4 \
  --prompt 'Localize this seller master video for Thailand. Preserve product, SKU, demonstration and commercial facts; adapt the home context, pacing and clean caption areas for approved Thai copy. Remove old market text. Do not translate or add warranty, certification, compatibility, voucher or price claims without supplied wording.'
```

### 4. Reference a creator rhythm without copying

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/creator-rhythm.mp4 \
  --image /path/to/product.png \
  --prompt 'Use the reference only for shot duration, hand-demo rhythm and camera energy. Create an original Shopee Philippines product demonstration in natural English/Taglish context. Do not reproduce the creator, dialogue, music, brand or exact shots; preserve merchant-approved product facts.'
```

### 5. Campaign creative variant

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Shopee campaign video template: immediate product action, one everyday problem, visible feature proof and final product frame with empty offer area. Bright mobile-commerce style but no generated voucher amount, sale price, countdown, rating, sold count or platform badge.'
```

## Localization QA

- Correct marketplace, language, currency placeholders and SKU.
- Product, package contents and operation remain accurate.
- Copy space is clean; approved text is proofread by a native reviewer.
- No fabricated voucher, flash-sale price, rating, sold count or guarantee.
- Reference footage, creators and music have appropriate rights.
- Check the current Shopee seller and advertising rules for each marketplace.

## Runtime

`t2v`, `i2v`, `r2v`, `edit` and `extend` map to Seedance 2.5 endpoints.

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name shopee-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Pass first/last frames, images, videos or audio as needed, plus model parameters, routing, output directory or `--no-download`. Confirm live configuration and cost before producing multiple markets or SKUs.
