---
name: temu-ecommerce-image-generation-editing
description: "Create and edit Temu product submission images, variant sets, package-content graphics, feature galleries and multi-market campaign bases. Use this skill for Temu商品图、跨境商品主图、工厂批量SKU、白底图、规格图、套装清单、多国家本地化、商品精修和广告测图；supports reference-guided AI Hive production."
---

# Temu Ecommerce Image Generation and Editing

Support high-volume catalog production while keeping factory item, variant and package facts traceable. A generated image is only acceptable when it can be mapped back to a verified product master and SKU row.

## Product master

Create one source record containing model number, dimensions, materials, color codes, package contents, accessories, labels, country-specific restrictions and approved claims. Choose multi-angle reference photos. Do not start a batch until one master image passes manual product review.

## Production flow

1. Generate a clean product master.
2. Validate structure, label, color and included parts.
3. Derive variant images with one controlled change per task.
4. Generate use, scale and package-content images separately.
5. Add localized specifications, prices and campaign text only from approved feeds.

## Scenarios and commands

### 1. Submission master image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Temu catalog master image for the supplied factory item. Preserve exact model, shape, materials, color, label, package and accessories. Complete product centered on a clean background with accurate edges and shadow. Do not add a bundle, price, discount, review, certification or unprovided feature.' \
  --image /path/to/front.jpg \
  --image /path/to/back.jpg
```

### 2. Controlled variant production

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Produce images for three confirmed SKU colors using the approved master. Lock geometry, camera, scale, background, label, packaging and accessories; change only the requested color. Keep every output as one standalone SKU and never merge variants.' \
  --image /path/to/approved-master.png \
  --batch 3
```

### 3. Package-content verification image

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Top-down package-content image based strictly on the reference: place the main item, cable, two adapters and instruction sheet in separate clear positions, each appearing once. Preserve connectors, quantities and labels. Do not create a gift, replacement part or extra accessory.' \
  --image /path/to/package-list.jpg
```

### 4. Size and use context base

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a realistic scale-and-use image for the reference product in a normal apartment. Keep product dimensions visually plausible and operation correct; reserve blank measurement callouts for verified data. Do not generate numeric dimensions, capacity or performance.' \
  --image /path/to/product.png
```

### 5. Multi-market campaign backgrounds

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create three campaign-ready background variants for US, Germany and Japan while keeping the exact product unchanged. Adapt only environment, styling and copy-safe layout. Leave prices, discounts, units, certification and localized claims blank for approved post-production.' \
  --image /path/to/product.png \
  --batch 3
```

## Batch gates

- Every output maps to a verified product master and SKU.
- Geometry, materials, labels, color and included quantities are correct.
- Variant changes are isolated; no hybrid SKU is created.
- Measurements and localized text come from approved structured data.
- No generated deal, review, badge, certification or performance claim.
- Recheck current Temu seller requirements for the product category and market.

## Run

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name temu-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

The image CLI supports multiple references, batch count, live model parameters, routing, output directory and `--no-download`. Confirm one SKU and live cost before scaling.
