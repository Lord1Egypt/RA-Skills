---
name: seedream-5-lite-product-image
description: "使用 Seedream 5.0 Lite 生成产品摄影、商品主图、场景图、细节图、包装清单和SKU系列，并保持商品结构与品牌事实准确。Use this skill for Seedream 5商品图、Seedream产品摄影、电商主图、商品套图、白底图、材质细节、使用场景、包装清单、SKU批量和新品上架；通过 AI Hive 生成。"
---

# Seedream 5.0 Lite 产品图生成

先建立商品“摄影母版”，再扩展购买信息图。固定使用 `public_model_seedream_5_0_lite`。每张图都应回答一个具体问题：是什么、大小如何、怎么用、材质怎样、包含什么。

## 摄影母版

记录商品多角度、包装、Logo、颜色、材质、配件、真实尺寸、相机角度、商品占比、背景、光源与阴影。批准母版后，所有 SKU 与套图都从母版规则派生。

## 场景与代码

### 1. 产品摄影主图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt 'Seedream产品摄影主图，保持参考商品结构、包装、Logo、颜色和配件准确；三分之四角度，干净浅灰背景，柔和侧光与真实接触阴影，主体完整清晰，不添加文字、价格、功能或道具' \
  --image /path/to/product.png
```

### 2. 材质细节套图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成三张商品细节图：表面材质、连接结构、操作部件。保持真实纹理、颜色、接口与Logo，统一光线和放大尺度，为人工说明留白，不发明材料、工艺和参数' \
  --image /path/to/details.jpg \
  --batch 3
```

### 3. 真实使用场景

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '将参考商品放入真实家庭书桌，人物按正确方式使用，商品大小与手部关系合理，保持结构与包装事实；场景展示一个真实便利点，不夸大效果、不增加配件和文字' \
  --image /path/to/product.png
```

### 4. 包装清单图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '俯拍包装清单图，严格展示参考资料中的主商品、连接线、适配器和说明书，每件只出现一次，接口和数量准确，背景统一，不添加赠品、替换件、保修卡或套装文字' \
  --image /path/to/package-contents.jpg
```

### 5. SKU 摄影统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '沿用批准摄影母版，生成当前蓝色SKU商品图：匹配相机角度、主体占比、背景、光源和阴影，保持当前SKU真实包装、Logo、颜色与标签，不复制母版的其他颜色' \
  --image /path/to/blue-sku.png \
  --image /path/to/approved-master.jpg
```

## 产品图验收

- 结构、包装、Logo、颜色、材质和配件准确。
- 主图、细节、场景和清单承担不同购买问题。
- 尺度、手物关系、透视与接触阴影合理。
- SKU 摄影标准统一但不串色、串标或串配件。
- 不生成价格、参数、功效、认证与赠品。
- 原始参考、母版与派生版本可追踪。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-product-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

批量前先批准一个母版；使用实时模型参数和价格。
