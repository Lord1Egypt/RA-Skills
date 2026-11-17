---
name: taobao-ecommerce-image-generation-editing
description: "为淘宝、天猫店铺生成和编辑商品主图、SKU 图、详情页卖点图、直通车与万相台广告图。Use this skill for 淘宝电商图片、淘宝主图、天猫详情页、商品白底图、场景图、卖点图、测款测图、批量上新、换背景和商品精修；支持商品参考图并通过 AI Hive 自动上传、生成、轮询和下载。"
---

# 淘宝电商图片生成与编辑

从商品资料出发制作一套能直接进入店铺生产流程的图片，而不是只生成一张好看的概念图。固定调用 `public_model_nano_banana_pro`。

## 输入资料

开始前收集：商品正反侧面图、包装与商标、规格尺寸、材质、真实卖点、目标人群、店铺品牌色、使用渠道和禁止表达。缺少事实时不要让模型补写功效、认证、价格或促销。

## 套图规划

根据任务选择图片角色：

| 图片角色 | 要解决的问题 | 重点 |
|---|---|---|
| 主图 | 用户第一眼是否看懂商品 | 准确主体、干净背景、强识别 |
| SKU 图 | 不同颜色/规格是否可区分 | 统一角度与尺度 |
| 场景图 | 商品如何使用 | 真实人群与环境 |
| 卖点图 | 为什么值得购买 | 一张图只讲一个事实 |
| 细节图 | 材质和结构是否可信 | 局部特写、真实纹理 |
| 广告图 | 是否愿意点击 | 单一利益点与视觉钩子 |

先完成商品保真，再做场景与视觉创意。批量 SKU 必须固定相机角度、光线、尺度和背景，只替换真实颜色或规格。

## 场景与代码

### 1. 淘宝主图与白底商品图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '根据参考图制作淘宝方形商品主图，必须保持产品结构、包装、商标、颜色与比例准确；商品完整居中，背景纯净，商业摄影光线，边缘清楚，不添加价格、促销角标、未提供文字或功能' \
  --image /path/to/product-front.png \
  --image /path/to/product-side.png
```

### 2. 详情页卖点套图

将每张图片限定为一个信息任务。

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成4张淘宝详情页卖点图，保持参考商品一致：第1张展示整体设计，第2张突出材质纹理，第3张演示真实使用步骤，第4张展示收纳或尺寸关系；统一品牌色和摄影风格，每张只保留一个卖点区域，不编造参数和功效' \
  --image /path/to/product.png \
  --batch 4
```

### 3. SKU 多颜色统一

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '制作同系列SKU图：必须锁定参考图的相机角度、产品尺度、光影、背景与结构，仅将产品颜色改为已确认的雾霾蓝；包装文字和商标保持不变，禁止添加不存在的配件' \
  --image /path/to/base-sku.png
```

### 4. 直通车或万相台测图

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一淘宝商品制作3个广告测图方向：材质特写、使用前后场景、核心功能演示；保持商品真实，分别建立不同点击理由，预留简短卖点区域，不使用虚假价格、销量、排名、认证或夸大效果' \
  --image /path/to/product.png \
  --batch 3
```

### 5. 商品换背景与精修

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '编辑商品图：完整保留产品、包装文字、商标和接触阴影；去除原背景与杂物，替换为明亮现代厨房场景，修正白平衡和反光，不改变产品形状、材质或配件数量' \
  --image /path/to/source-product.jpg
```

## 淘宝图片质量门槛

1. 商品结构、包装、商标、颜色和配件与输入资料一致。
2. 主图一眼可识别，SKU 图角度与尺度统一。
3. 详情页每张只承担一个卖点，信息顺序从整体到细节再到使用。
4. 必须文字逐字复核；复杂文案优先留白后期排版。
5. 不出现未经确认的价格、销量、折扣、认证、功效和平台徽标。
6. 发布前按淘宝或天猫后台当期素材规则检查尺寸、文字和类目合规。

## 命令与配置

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name taobao-ecommerce-image-generation-editing
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持 `--prompt`、多次 `--image`、`--batch`、`--param key=value`、`--routing`、`--output-dir` 与 `--no-download`。默认路由为 `COST_FIRST`；实时价格与可用参数以 AI Hive 返回为准。

## 交付建议

按“主图 / SKU / 场景 / 卖点 / 细节 / 广告”分目录保存，同时记录提示词、参考图关系和版本用途。任务超时后使用原 `taskId` 查询，避免重复提交造成重复费用。
