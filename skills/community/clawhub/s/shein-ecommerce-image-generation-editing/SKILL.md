---
name: shein-ecommerce-image-generation-editing
description: "Create and edit SHEIN fashion product images, model try-on visuals, colorway sets, fabric details, outfit styling and campaign-ready bases. Use this skill for SHEIN商品图、服装主图、模特试穿、版型展示、面料细节、颜色SKU、穿搭图、尺码信息底图和跨境时尚电商；supports reference-guided AI Hive production."
---

# SHEIN 电商图片生成与编辑

围绕服装版型、面料、颜色和真实穿着关系制作图片。不能通过改变模特身体、夸大塑形效果或重画衣服结构来制造卖点。固定使用 `public_model_nano_banana_pro`。

## 服饰底稿

准备服装正背面、平铺与上身照片，记录颜色、面料、领口、袖型、腰线、长度、开合方式、图案位置、配件、目标模特范围和尺码表。尺码数字与材质成分由商家后期准确排版。

## 场景与代码

### 1. 服装商品主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'SHEIN fashion listing image using the reference garment. Preserve exact silhouette, neckline, sleeve, hem, seams, print placement, color and accessories. Full-body neutral model pose, clear garment front, clean background, realistic fabric drape. Do not reshape the model body or invent garment details.' \
  --image /path/to/garment-front.jpg \
  --image /path/to/garment-back.jpg
```

### 2. 正背侧版型套图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create three consistent fashion views of the same garment: front, back and side. Keep the same model identity, body proportions, garment size, color, seams, pattern and lighting; use neutral poses that reveal construction rather than changing fit.' \
  --image /path/to/garment.png \
  --batch 3
```

### 3. 面料与工艺细节

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'SHEIN product-detail image with accurate garment plus close-ups of the supplied fabric texture, stitching and closure. Keep color under neutral light and leave clean labels for merchant-approved material copy. Do not invent fiber content, stretch, thickness or craftsmanship claim.' \
  --image /path/to/fabric-detail.jpg
```

### 4. 颜色 SKU 统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Produce listing images for confirmed burgundy, charcoal and ivory colorways. Lock model, pose, garment cut, seam, print, accessories, camera and background; change only the verified garment color. Avoid skin-tone shifts and hybrid colors.' \
  --image /path/to/approved-fit.png \
  --batch 3
```

### 5. 穿搭场景图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Create a credible street-style outfit around the reference garment for an autumn commute. Preserve garment fit and construction; add only simple neutral styling pieces that do not cover key details. Natural walking pose, no impossible body shape, no luxury logo or unprovided accessory.' \
  --image /path/to/garment.png
```

## 服饰验收

- 领口、袖型、腰线、长度、缝线、图案与配件一致。
- 模特身份和身体比例自然，不因卖点发生变形。
- 颜色在统一光线下可比较，SKU 不串色。
- 面料成分、尺码、弹性和洗护信息来自商家资料。
- 不添加品牌 Logo、塑形承诺、价格、评分或趋势标签。
- 发布前按 SHEIN 当前商品与广告规范检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name shein-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

可使用多张参考图、批量、模型参数、路由和仅提交模式。先批准一个颜色和一个模特版型，再扩展 SKU。
