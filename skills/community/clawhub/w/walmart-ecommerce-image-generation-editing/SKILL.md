---
name: walmart-ecommerce-image-generation-editing
description: "Create and edit Walmart Marketplace product images, variant galleries, package-content views, dimension bases and omnichannel retail visuals. Use this skill for Walmart商品图、Walmart Marketplace listing、零售主图、包装清单、规格尺寸、SKU变体、家居场景、广告素材和线上线下一致性；supports product-reference generation through AI Hive."
---

# Walmart Ecommerce Image Generation and Editing

Create retail images that make item, variant, package and scale unambiguous. Online visuals must match what a shopper receives and must not imply a store placement, certification, price, rollback or bundle that the merchant did not supply.

## Retail item record

Collect item ID/SKU, UPC-linked variant, product angles, retail package, included pieces, dimensions, materials, approved claims, warnings and omnichannel brand rules. Use this record as the sole source of product facts.

## Scenarios and commands

### 1. Item-page primary image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Walmart Marketplace primary image for the supplied retail item. Preserve exact product, retail package, label, color, variant and included pieces. Show the complete item large on a clean background with realistic shadow and clear edges. No price, rollback, pickup badge, rating, certification or unprovided text.' \
  --image /path/to/item-front.png \
  --image /path/to/retail-package.png
```

### 2. Package-contents image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Walmart package-content image showing exactly the approved main item, two attachments, power cable and guide, each once and with correct connector and scale. Clean top-down arrangement; do not add a bonus, replacement part, multipack or warranty card.' \
  --image /path/to/package-contents.jpg
```

### 3. Dimension and scale base

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Retail dimension graphic base: accurate product shown front and side plus one realistic in-room scale view, with blank measurement arrows for merchant-approved numbers. Keep proportions consistent and do not generate dimensions, capacity, room size or performance.' \
  --image /path/to/product.png
```

### 4. Variant gallery

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create consistent Walmart listing images for the verified single, 2-pack and 4-pack variants. Lock product appearance, package design, camera, background and shadow; show the correct quantity for each variant and do not mix accessories or invent bundle savings.' \
  --image /path/to/item-and-packages.jpg \
  --batch 3
```

### 5. Omnichannel lifestyle image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Walmart product lifestyle image in a credible family home, preserving exact item and use method. Show one practical everyday benefit with realistic scale and safe caption space. Do not imply in-store availability, pickup time, price, guarantee or customer endorsement.' \
  --image /path/to/product.png
```

## Retail QA

- Item, variant, package, label and included quantity match the catalog record.
- Pack-size images cannot be mistaken for a different offer.
- Dimension callouts use approved values and units after generation.
- No generated price, rollback, pickup, rating, certification or retailer badge.
- Lifestyle scene does not imply unsupported use or store availability.
- Verify current Walmart Marketplace image and category requirements.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name walmart-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

The fixed image endpoint is `public_model_nano_banana_pro`. Use multiple references, batch, live parameters, routing, output directory and submit-only mode as needed.
