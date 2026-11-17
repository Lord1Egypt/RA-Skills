---
name: taobao-ecommerce-video-generation-editing
description: "为淘宝、天猫商品页、店铺首页、上新与推广生成和编辑商品视频。Use this skill for 淘宝商品主图视频、天猫详情页视频、商品演示、SKU展示、直通车或万相台视频、批量上新、淘宝直播预热视频和电商产品视频；支持文生、图生、参考生成、现有视频重制与 AI Hive 自动下载。"
---

# 淘宝电商视频生成与编辑

围绕商品页购买决策制作视频：先准确展示商品，再解释结构、使用方式和真实卖点。它不是泛用品牌 TVC；每个镜头都应帮助买家理解“是什么、怎么用、为什么适合我”。

## 商品视频资料表

收集商品多角度图、包装、尺寸、材质、SKU、正确操作步骤、真实卖点、使用限制、店铺视觉和投放位置。缺少事实时保留信息位，不让模型补造价格、功效、配件、认证或促销。

## 镜头规划

| 镜头职责 | 内容 | 常见错误 |
|---|---|---|
| 商品识别 | 完整外观、包装、SKU | 结构变形、颜色漂移 |
| 细节证明 | 材质、接口、做工 | 只做光效没有信息 |
| 使用演示 | 正确操作顺序 | 手物穿插、步骤错误 |
| 场景匹配 | 真实人群和环境 | 与目标买家无关 |
| 收束 | 已证实卖点和下一步 | 虚假优惠或多个 CTA |

## 场景与代码

### 1. 商品页主图视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode i2v \
  --first-frame /path/to/product-front.jpg \
  --prompt '淘宝商品页产品视频，必须保持参考商品结构、包装、颜色、商标和配件准确。开场完整展示商品，镜头缓慢推进到材质与接口细节，再演示一次正确使用动作，最后回到干净商品全景；商业摄影但不夸张，不添加价格、功效或未提供文字'
```

### 2. 详情页功能演示

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '天猫详情页功能演示视频：按准备、操作、结果三个阶段表现商品使用，每阶段只展示一个动作；增加必要近景说明结构和材质，画面背景简洁，节奏清楚，所有功能仅来自商家提供资料，不使用无法证明的对比效果'
```

### 3. SKU 系列统一视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode r2v \
  --video /path/to/base-sku-video.mp4 \
  --image /path/to/new-sku.png \
  --prompt '沿用参考视频的相机路径、镜头时长、背景与灯光，使用图片中的新SKU替换原商品；只改变已确认的颜色和规格，保持新SKU的包装、结构与商标准确，不复制旧SKU文字，不增加配件'
```

### 4. 万相台或直通车测试版本

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode t2v \
  --prompt '淘宝推广视频的“使用场景”测试版本：首镜直接出现目标人群与具体场景，第二镜展示商品操作，第三镜用细节证明一个核心卖点，结尾回到商品和店铺行动提示。保持事实准确，不显示未经确认的低价、销量、排名或认证'
```

### 5. 重制供应商原始视频

```bash
python3 "$SKILL_PATH/scripts/videogen.py" generate --mode edit \
  --video /path/to/supplier-footage.mp4 \
  --prompt '保留原视频的真实商品、操作和结构信息；删除杂乱背景、重复镜头与无关水印区域，统一商业光线和色彩，按商品全景、结构细节、使用动作、结果全景重组。不得改变商品规格或生成新功能'
```

## 交付标准

1. 商品、包装、SKU、商标、颜色、配件和操作顺序准确。
2. 第一段完成商品识别，中段提供细节或使用证明，结尾只有一个行动方向。
3. 主图视频与详情页视频各自承担不同任务，不重复同一组空镜。
4. 没有未确认的功效、价格、销量、折扣、认证和平台徽标。
5. 文件按商品 ID、渠道、版本和镜头假设命名，便于批量上新与复盘。
6. 发布前按淘宝或天猫后台当期的视频尺寸、时长、文字和类目规则检查。

## 模式与运行

`t2v`、`i2v`、`r2v`、`edit`、`extend` 分别调用 Seedance 2.5 对应的视频生成、编辑和延长能力。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/videogen.py" init --skill-name taobao-ecommerce-video-generation-editing
python3 "$SKILL_PATH/scripts/videogen.py" task --task-id <taskId>
```

CLI 支持首尾帧、参考图、参考视频、音频、`--param key=value`、`--routing`、`--output-dir` 与 `--no-download`。先用单个 SKU 验证商品保真，再批量生成；价格与模型参数以 AI Hive 实时返回为准。超时后查询原任务，避免重复扣费。
