---
name: seedream-5-lite-image-edit
description: "使用 Seedream 5.0 Lite 按依赖顺序编辑授权图片，先锁定事实和几何，再执行移除、替换、扩展、调光与收尾，减少连带重绘。Use this skill for Seedream 5 Lite image editing、图片编辑、局部修改、移除物体、替换颜色、扩图、修复构图、照片调整、商品图编辑、广告素材改版和 AIGC 图片后期；通过 AI Hive 编辑指定参考图。"
---

# Seedream 5.0 Lite 图片编辑

固定使用 `public_model_seedream_5_0_lite`，必须提供图片。将编辑拆成有依赖关系的操作队列：事实锁定 → 几何修正 → 内容增删 → 光线匹配 → 质感收尾。一次提交只处理一个主操作，避免多个指令互相覆盖。

## 操作队列

列出原图事实、锁定区域、目标区域、主操作、允许连带调整、禁止变化和验收方式。删除物体后才能补背景；替换颜色后再统一反射；扩图完成后再放文字安全区。人物、品牌、商品结构和新闻含义默认锁定。

## 场景与代码

### 1. 移除桌面杂物

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./office-desk.jpg \
  --prompt '主操作：只移除桌面右侧的红色外卖袋，并用相邻木纹、阴影和墙面自然补全。锁定电脑、键盘、杯子、植物、屏幕内容、相机位置和整体光线；不移动其他物体、不生成新文具、文字或Logo' \
  --param aspect_ratio=16:9
```

### 2. 商品颜色替换

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-chair-blue.png \
  --prompt '主操作：把椅子软包从批准的深蓝色替换为批准的砖红色。锁定椅腿、坐垫厚度、缝线、织物纹理、Logo、相机角度、背景和阴影；允许反射与环境色随新颜色轻微调整，不改变版型或添加配饰' \
  --param aspect_ratio=4:5
```

### 3. 横幅扩图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-product-square.jpg \
  --prompt '主操作：把方形商品图向左右扩展为16:9横幅。中央产品、标签、Logo、颜色、原台面和原光线完全锁定，只延展同一背景与台面纹理，左侧形成标题安全区；不缩放移动产品，不增加道具、文字或第二件商品' \
  --param aspect_ratio=16:9
```

### 4. 人像背景干扰清理

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./authorized-portrait.jpg \
  --prompt '主操作：移除人物肩后穿过头部的电线与远处红色路牌，用原有街景景深补全。人物身份、脸、发丝、服装、姿势、肤色和光线全部锁定；不磨皮、不改变表情、不添加Logo、文字或新路人' \
  --param aspect_ratio=3:4
```

### 5. 室内日夜调整

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-room-day.jpg \
  --prompt '主操作：把室内白天氛围调整为刚入夜的暖灯场景。锁定墙体、门窗、家具位置、材质和相机视角；允许窗外天空、室内灯光、阴影和反射同步变化，不增加灯具、人物、装饰或改变空间结构' \
  --param aspect_ratio=16:9
```

## 队列验收

- 主操作完成且没有越过目标区域。
- 锁定事实、几何、身份、Logo和文字未变化。
- 补全区域的纹理、透视、景深、光向和噪点连续。
- 连带调整仅发生在事先批准范围内。
- 保存原图、操作队列、提示词、任务 ID 和差异对照。

## 助手边界

工具只上传命令中指定的图片，固定调用 Seedream 5.0 Lite 模型，查询价格、创建编辑任务并下载结果。带 Key 请求仅发往 `https://ai-hive.iclip.cn/api`，不接受自定义地址。无聊天、视频、账户或余额能力。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-image-edit
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

涉及真实人物、新闻、证据、商品缺陷和品牌素材时，应取得授权并披露实质性编辑。
