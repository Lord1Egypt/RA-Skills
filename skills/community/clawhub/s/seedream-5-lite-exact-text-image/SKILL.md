---
name: seedream-5-lite-exact-text-image
description: "使用 Seedream 5.0 Lite 生成或编辑包含短标题、标签和活动文案的商业图片，并用逐字校对、字符预算和失败回退控制文字准确性。Use this skill for Seedream 5 Lite exact text image、精准文字图片、海报文字、商品卖点卡、包装标签、活动邀请、中文标题、英文标题、淘宝京东抖音小红书亚马逊 Instagram 营销图；通过 AI Hive 生成后必须人工校字。"
---

# Seedream 5.0 Lite 精准文字图片

固定使用 `public_model_seedream_5_0_lite`。将文字视为需要验收的数据，不把“看起来像字”当成正确。优先使用一条短标题和一条短副标题；法律条款、价格、日期、型号、成分、二维码和长段正文应在设计工具中后期排版。

## 文字规格单

逐项记录精确文案、语言、大小写、标点、换行、最大字符数、字体气质、对齐、颜色、位置、安全区和禁止出现文字。生成后逐字比对；若两轮仍有错字，保留无字底图并在排版工具中覆盖批准文本。

## 场景与代码

### 1. 中文活动海报标题

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成竖版春季设计市集海报，画面是抽象纸张与嫩绿色几何装置。只出现两行中文：第一行“春日造物集”，第二行“周末见”；文字必须逐字准确、无其他字符，第一行居中大字，第二行较小，四周留白，不生成日期、地址、Logo或二维码' \
  --batch 3 \
  --param aspect_ratio=3:4
```

### 2. 商品卖点卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-lunchbox.png \
  --prompt '基于参考便当盒制作1:1卖点卡，产品外观、颜色、卡扣和Logo不变。只出现标题“分格不串味”，五个汉字必须完全正确，位于左上；背景为浅米色桌面，右下放产品，不生成价格、容量、认证、英文、平台Logo或其他文字' \
  --param aspect_ratio=1:1
```

### 3. 英文包装标签概念

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '为虚构手工皂制作包装标签概念图：牛皮纸腰封与深绿色小字。只允许出现品牌占位名“FIELD SOAP”和香型“CEDAR”，保持这两个英文短语拼写和大写完全准确，不生成成分、重量、条码、认证、产地或第三段文字；该图仅作概念，不冒充可印刷包装' \
  --batch 3
```

### 4. 活动邀请卡

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --prompt '生成极简蓝白渐变邀请卡，只出现三行文字：“OPEN STUDIO”、“AUG 24”、“SHANGHAI”；拼写、空格和数字必须完全一致，三行垂直居中，现代无衬线字体，不生成具体地址、时间、Logo、二维码、装饰性假字或其他数字' \
  --param aspect_ratio=4:5
```

### 5. 多语言社媒封面

```bash
python3 "$SKILL_PATH/scripts/imagegen.py" generate \
  --image ./approved-tea-scene.jpg \
  --prompt '保持参考茶饮场景主体与色调，在顶部安全区只添加两行：中文“慢慢喝茶”，英文“SLOW TEA”。中文四字和英文拼写必须准确，英文全部大写；不改变产品、不增加价格、功效、品牌、标点、第三行文字或平台Logo' \
  --batch 2 \
  --param aspect_ratio=4:5
```

## 逐字验收

- 将实际输出转写，与规格单逐字符比较，包括空格、大小写、数字和标点。
- 检查是否出现多余假字、重复字符、镜像文字或被主体遮挡的字。
- 确认文字与背景有足够对比度，并位于渠道安全区。
- 商品、人物和品牌事实没有为了排字而被重绘。
- 精确要求失败时停止扩写提示词，改用无字底图加后期排版。

## 助手边界

工具固定使用 Seedream 5.0 Lite 图片模型，可处理纯文字生成或用户明确指定的参考图，查询路由价格、创建任务并下载结果。认证请求只发送到 `https://ai-hive.iclip.cn/api`，不接受自定义地址。`init` 可把 Key 以 `0600` 权限保存；无聊天、视频、账户或余额接口。

```bash
pip3 install requests
python3 "$SKILL_PATH/scripts/imagegen.py" init --skill-name seedream-5-lite-exact-text-image
python3 "$SKILL_PATH/scripts/imagegen.py" task --task-id <taskId>
```

涉及价格、日期、型号、成分、法规和促销条款时，以批准文案为唯一来源并进行人工终审；平台名称仅用于场景搜索。
