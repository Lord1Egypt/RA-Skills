---
name: temu-ecommerce-video-generation-editing
description: "Create and edit Temu product catalog videos, factory demonstrations, assembly guides, variant clips and multi-market adaptations. Use this skill for Temu商品视频、跨境产品演示、工厂批量视频、套装清单、安装教程、SKU变体、广告素材和多国家本地化；supports Seedance generation/editing through AI Hive."
---

# Temu Ecommerce Video Generation and Editing

Turn verified factory product records into repeatable videos at SKU scale. The governing rule is traceability: every shown component, action, dimension or result must come from the product master or visible source footage.

## Batch design

Define a product master, approved demonstration sequence, package contents, variant table, market requirements and prohibited claims. Test one SKU before scaling. Keep a shot recipe so later variants change only the intended color, size, bundle or market context.

## Scenarios and commands

### 1. Factory product master video

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/approved-product.jpg \
  --prompt 'Temu catalog product master video. Preserve exact model, geometry, materials, color, labels, packaging and included pieces. Show full item, rotate to key structure, demonstrate one correct action and finish on package contents. Neutral commercial set; no price, discount, review, certification or invented feature.'
```

### 2. Assembly guide

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Assembly guide using only the approved instruction sequence: lay out supplied components, complete steps 1 through 4 in order with clear hand placement, show safety-critical orientation, then present the finished item. Do not skip a step, add a tool or change connector shape.'
```

### 3. Controlled SKU video variant

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/master-sku-video.mp4 \
  --image /path/to/blue-variant.png \
  --prompt 'Follow the approved master shot recipe and timing, replacing only the product with the verified blue SKU. Keep geometry, scale, package, labels, accessories, set and camera path unchanged. Do not create a hybrid color or bundle.'
```

### 4. Recut factory footage

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/factory-footage.mp4 \
  --prompt 'Re-edit verified factory footage into a Temu catalog video: remove repeated and irrelevant shots, keep authentic product structure and operation, order as complete item, detail, use, package contents. Remove unapproved text areas and do not alter specifications or outcome.'
```

### 5. Multi-market adaptation

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/catalog-master.mp4 \
  --prompt 'Create a Japanese-market visual base from the catalog master. Preserve product, SKU, setup and commercial facts; adapt room context and reserve clean areas for approved Japanese captions. Leave units, price, certification and warranty blank unless exact localized data is supplied.'
```

## Batch gates

- Master video is manually approved before variant production.
- Each output maps to product master, SKU, market and shot recipe.
- Geometry, labels, package contents, tools and operation are correct.
- Variants change only the requested attribute.
- No generated deal, review, warranty, certification or performance claim.
- Verify current Temu video requirements for category and destination market.

## Runtime

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name temu-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use the appropriate Seedance 2.5 mode with reference media, live parameters, routing, output directory or `--no-download`. Confirm one SKU and live cost before running a batch.
