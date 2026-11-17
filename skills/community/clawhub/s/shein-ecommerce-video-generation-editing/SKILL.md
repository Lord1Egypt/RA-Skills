---
name: shein-ecommerce-video-generation-editing
description: "Create and edit SHEIN fashion try-on videos, garment movement clips, fabric details, colorway variants and outfit styling content. Use this skill for SHEIN商品视频、服装试穿、版型展示、面料动态、颜色SKU、穿搭短视频、跨境时尚广告和模特素材重制；supports Seedance video generation/editing via AI Hive."
---

# SHEIN 电商视频生成与编辑

用动作和连续镜头展示服装的版型、垂坠、细节和搭配，而不是靠改变模特身体制造效果。服装结构、颜色、图案、尺码样衣和配件必须与参考资料一致。

## 试穿底稿

记录服装正背侧面、样衣尺码、面料、颜色、领口、袖型、腰线、长度、开合、图案位置、允许搭配和模特资料。不要推断模特真实尺码或生成身体改造结果。

## 场景与代码

### 1. 服装动态试穿

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/model-and-garment.jpg \
  --prompt 'Vertical SHEIN fashion try-on video. Preserve model identity, natural body proportions and exact garment silhouette, neckline, sleeve, hem, seams, print and color. Show front walk, gentle turn, back view and seated movement under neutral light. Do not slim the body or change garment fit between shots.'
```

### 2. 面料与工艺动态细节

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt 'Fashion product detail clip: hands gently show the approved fabric drape, seam, closure and texture, then return to the complete garment. Neutral lighting and accurate color, no microscopic fantasy, fiber-content claim, stretch claim or durability result.'
```

### 3. 颜色 SKU 派生

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/approved-fit-video.mp4 \
  --image /path/to/burgundy-sku.png \
  --prompt 'Follow the approved pose sequence, camera, model, garment construction and timing, changing only to the verified burgundy colorway. Keep skin tone stable and do not create mixed colors, new prints or accessories.'
```

### 4. 穿搭短视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '9:16 street-style outfit video built around the approved garment: show one commuting look from full body to garment detail, natural walking and bag interaction, then a clean final pose. Added styling must not hide construction or use unapproved luxury logos.'
```

### 5. 重制模特素材

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/raw-try-on.mp4 \
  --prompt 'Keep the real model, garment fit, movement and color; remove repeated poses and distracting background, correct exposure, and reorder as front, side, back and detail. Do not modify body shape, garment length, waist, print or fabric behavior.'
```

## 服饰验收

- 模特身份和身体比例在镜头间连续自然。
- 服装版型、长度、缝线、图案、颜色和配件准确。
- 动态垂坠来自可见资料，不生成材料性能结论。
- 不添加身材改造、塑形承诺、价格、评分或趋势标签。
- SKU 派生只改变批准的颜色或款式属性。
- 发布前按 SHEIN 当前商品与广告规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name shein-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

CLI 支持生成、图生、参考、编辑和延长，按需传入媒体、参数、路由与输出目录。先批准一个版型视频再扩展颜色。
