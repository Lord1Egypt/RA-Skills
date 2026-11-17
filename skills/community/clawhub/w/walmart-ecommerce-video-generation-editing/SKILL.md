---
name: walmart-ecommerce-video-generation-editing
description: "Create and edit Walmart Marketplace product videos, assembly guides, package-content demonstrations, variant clips and retail advertising bases. Use this skill for Walmart商品视频、Marketplace listing video、零售产品演示、安装教程、包装清单、SKU套装、家庭场景和广告素材；supports Seedance generation/editing through AI Hive."
---

# Walmart Ecommerce Video Generation and Editing

Create practical retail videos that match the exact item and package a shopper receives. A video must not imply an in-store location, pickup promise, rollback price, certification, bundle or performance result that is absent from the item record.

## Item truth record

Collect item/SKU, retail package, included components, variants, dimensions, correct setup, approved features, warnings and usage context. Lock this record before creating a listing master or variant video.

## Scenarios and commands

### 1. Item-page demonstration

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/item.jpg \
  --prompt 'Walmart Marketplace product video preserving exact item, retail package, variant, label and included components. Show complete product, one correct setup, feature detail and realistic family use. Clear sound-off sequence with caption space; no price, rollback, pickup, rating or unsupported claim.'
```

### 2. Assembly guide

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Retail assembly guide based only on approved instructions: display supplied parts, complete steps in order with safe hand placement, tighten the correct fasteners and show final stable use. Do not skip a warning, add a tool or change part geometry.'
```

### 3. Package and pack-size proof

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode extend \
  --video /path/to/item-intro.mp4 \
  --prompt 'Continue into package-content proof for the verified 2-pack: show two identical units and the exact shared accessories, each once, then a combined use view. Preserve quantity and packaging; do not add multipack savings, gift or alternate variant.'
```

### 4. Recut supplier footage

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/supplier-master.mp4 \
  --prompt 'Re-edit supplier footage for a Walmart item page. Keep actual product, setup and feature evidence; remove wholesale messaging, repeated beauty shots and unapproved text. Order as item identification, package contents, setup, proof and home use without changing product facts.'
```

### 5. Retail ad base

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/retail-rhythm.mp4 \
  --image /path/to/item.png \
  --prompt 'Use the reference only for concise retail pacing. Create an original ad base for the accurate item: everyday problem, correct product action, visible proof and clean final CTA area. Do not copy store branding or generate a rollback, price, pickup claim or review.'
```

## QA

- Item, variant, retail package and included quantity match the catalog record.
- Setup and safety steps are correct and complete.
- Pack-size video cannot be confused with another offer.
- No generated price, rollback, pickup, certification, rating or store availability.
- Verify current Walmart Marketplace category, media and advertising requirements.

## Runtime

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name walmart-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

Use Seedance 2.5 text, image, reference, edit or extend modes with media inputs, live parameters, routing and output controls.
