---
name: xiaohongshu-viral-cover-image-generation
description: "生成与编辑小红书笔记首图、种草封面、好物清单封面和品牌合作视觉。Use this skill for 小红书爆款封面、XHS/RED 笔记首图、种草标题图、开箱测评封面、好物分享、蒲公英内容、聚光素材和系列账号视觉；支持人物与商品参考图、中文标题留白、批量创意方向及 AI Hive 自动下载。"
---

# 小红书爆款笔记封面生成与编辑

把一篇笔记的真实价值压缩成一张“像内容、不是硬广”的首图。固定调用 `public_model_nano_banana_pro`。不承诺爆款，不伪造体验、结果或用户评价。

## 封面简报

先确认笔记主题、目标人群、使用情境、可验证的核心结论、必须出现的商品或人物、标题文案、账号视觉和商业合作披露要求。没有正文或真实体验资料时，先完成信息梳理，不让图片代替事实。

## 选择封面类型

| 类型 | 适合内容 | 视觉重点 |
|---|---|---|
| 真实体验 | 使用心得、避坑 | 人物、情境、明确结论 |
| 好物清单 | 多商品推荐 | 统一尺度、清晰编号 |
| 开箱测评 | 新品与细节 | 包装、材质、手部动作 |
| 教程步骤 | 方法与攻略 | 结果、步骤感、留白 |
| 前后对比 | 整理、搭配、改造 | 同条件、真实可比 |

标题优先简短，封面只表达一个信息差。复杂文案留出排版区域，不强迫模型生成大段文字。

## 场景与代码

### 1. 真实体验型种草封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '小红书竖版笔记首图，主题是租房小厨房收纳，真实生活空间，年轻用户正在使用收纳商品，画面体现拥挤痛点与整理后的秩序感，上方留出一个短标题区域，手机缩略图仍能识别，生活方式摄影，不做电视广告质感，不添加虚假效果或促销信息' \
  --image /path/to/product.png
```

### 2. 好物清单封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '小红书好物清单封面，展示参考图中的三件通勤用品，保持每件商品外观、颜色、商标和比例准确；桌面俯拍，清楚分区并预留1、2、3编号位置，统一暖灰色调，画面简洁，不生成价格、排名或未提供商品' \
  --image /path/to/item-1.png \
  --image /path/to/item-2.png \
  --image /path/to/item-3.png
```

### 3. 开箱测评封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '小红书开箱测评首图，保留参考商品包装与全部配件，手部刚打开包装，主体与材质细节清晰，表情自然不过度惊讶，左上角留出短标题“开箱实测”，不增加包装内不存在的物品、认证或结论' \
  --image /path/to/unboxed-product.jpg
```

### 4. 系列账号统一封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '参考已有系列首图的色彩、人物尺度、边距和标题区域，制作新一期“小个子通勤穿搭”封面；保持参考人物身份，新服装搭配清楚，背景简洁，延续系列识别但不复制旧标题和旧动作' \
  --image /path/to/series-style.png \
  --image /path/to/person.png
```

### 5. 笔记封面 A/B 方向

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为同一篇小红书笔记生成3种真正不同的封面假设：人物真实体验、商品细节证明、使用结果对比；三版保持同一商品与品牌色，每版只有一个视觉重点，标题留白清楚，不只改变滤镜或背景色' \
  --image /path/to/product.png \
  --batch 3
```

## 交付检查

- 缩略图能读懂主题，不依赖大段小字。
- 人物与商品来自真实资料，身份、包装和结构没有变化。
- 对比图条件可比，不夸大使用结果。
- 标题、品牌字样和商品文字逐字复核。
- 商业合作、功效、价格和体验结论不由模型自行添加。
- 发布前按小红书当期社区与商业内容规则检查。

## 执行

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name xiaohongshu-viral-cover-image-generation
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

`generate` 支持 `--prompt`、多张 `--image`、`--batch`、`--param key=value`、`--routing`、`--output-dir` 和 `--no-download`。价格与模型参数以 AI Hive 实时返回为准；任务超时后继续查询原 `taskId`。
