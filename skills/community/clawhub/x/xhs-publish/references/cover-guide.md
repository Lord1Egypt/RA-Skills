# 小红书封面图生成详细指南

## 封面图结构（正方形 1080x1080）

```
┌──────────────────┐
│                  │
│  AI 生成图片      │  1080x1080 (1:1)
│  (卡通漫画风格)    │
│  包含标题文字      │
│                  │
└──────────────────┘
```

**⚠️ 直接使用 AI 生成的图片，不需要拼接！**

## AI 图片风格规范

**⚠️ 默认使用卡通漫画风格（Cartoon/Illustration Style）**

### 风格关键词

- **必备**：`cute cartoon illustration style, kawaii anime style`
- **场景描述**：根据文案主题描述具体场景
- **色调提示**：`soft pastel colors` + 具体色调（如 blue and white、pink and cream）
- **禁止内容**：`no text no watermark`
- **质量词**：`high quality, clean minimal background`

### Prompt 模板

```
cute cartoon illustration style, [场景描述], kawaii anime style, soft pastel [色调] colors, minimal clean background, no text no watermark, high quality, square format
```

### Prompt 示例

| 主题 | Prompt |
|------|--------|
| 科技/效率 | `cute cartoon illustration style, a friendly robot holding a magnifying glass examining a glowing blue skill card, shield icon, security check concept, kawaii anime style, soft pastel blue and white colors, minimal clean background, no text no watermark, high quality, square format` |
| 美食/烘焙 | `cute cartoon illustration style, a cheerful chef character baking cookies in a cozy kitchen, warm oven glow, kawaii anime style, soft pastel cream and brown colors, minimal clean background, no text no watermark, high quality, square format` |
| 健身/运动 | `cute cartoon illustration style, an energetic character doing yoga pose, dumbbells and yoga mat, kawaii anime style, soft pastel green and white colors, minimal clean background, no text no watermark, high quality, square format` |
| 旅行/探店 | `cute cartoon illustration style, a happy traveler with backpack taking photo, camera and map icons, kawaii anime style, soft pastel orange and blue colors, minimal clean background, no text no watermark, high quality, square format` |
| 穿搭/美妆 | `cute cartoon illustration style, a stylish character trying on outfits in front of mirror, fashion items floating around, kawaii anime style, soft pastel pink and cream colors, minimal clean background, no text no watermark, high quality, square format` |

## 配色搭配规则（重要）

Agent 必须根据主题和图片色调主动搭配底色与字色，不要用默认白底黑字。

### 原则

1. **底色与图片色调呼应**：底色应从 AI 图片的主色调中提取同色系的浅色/淡色
2. **字色与底色形成对比**：字色要在底色上清晰可读
3. **整体风格一致**：暖色主题用暖色搭配，冷色主题用冷色搭配
4. **小红书审美偏好**：偏向柔和、温暖、高级感的色调

### 配色参考库

底色必须有明显视觉辨识度，不能接近纯白。浅色底色明度控制在 75%-90% 之间。

| 风格 | 底色 | 字色 | 适用场景 | 视觉感受 |
|------|------|------|---------|---------|
| 奶油温暖 | `#F5E6D0` | `#6B4226` | 美食、烘焙、咖啡、家居 | 温馨舒适 |
| 蜜桃甜美 | `#FCDBD3` | `#D4545B` | 美妆、护肤、穿搭、恋爱 | 少女心 |
| 薄荷清新 | `#D4EDDF` | `#1B5E40` | 健身、户外、植物、环保 | 清新自然 |
| 雾蓝理性 | `#CEDAEB` | `#2B4A7C` | 科技、效率、学习、职场 | 专业冷静 |
| 薰衣草梦幻 | `#DDD0F0` | `#5A3A8A` | 旅行、艺术、香氛、冥想 | 浪漫高级 |
| 鹅黄活力 | `#F5ECC8` | `#8B6D0B` | 育儿、宠物、手工、日常 | 明亮温暖 |
| 烟粉优雅 | `#F2D5E5` | `#8B1C4E` | 婚礼、花艺、甜品、仪式感 | 精致浪漫 |
| 暗夜高级 | `#1C1C1E` | `#E8C872` | 奢侈品、数码、夜景、酒 | 高级沉稳 |
| 莫兰迪灰 | `#D5D0C8` | `#4A453F` | 极简、设计、建筑、摄影 | 高级克制 |
| 珊瑚活力 | `#FBCEC5` | `#C04030` | 运动、夏日、派对、潮流 | 热情洋溢 |

### 自定义搭配原则

- 浅色底色明度控制在 75%-90%，不能接近纯白（≥95%会显得平淡）
- 字色与底色需形成强对比，确保清晰可读
- 暗色底色（如暗夜高级）配亮色/金色字
- 底色饱和度适中（15%-35%），太低会像灰色，太高会抢 AI 图片视线
- 推荐从 AI 图片的主色调中吸色，降低饱和度作为底色

## 生成流程

### 步骤 1：生成 AI 图片

使用 Doubao（豆包）API 生成 2048x2048 正方形卡通漫画风格图片：

```bash
curl -X POST "https://ark.cn-beijing.volces.com/api/v3/images/generations" \
  -H "Authorization: Bearer $DOUBAO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "doubao-seedream-5-0-260128",
    "prompt": "cute cartoon illustration style, [场景描述], kawaii anime style, soft pastel [色调] colors, minimal clean background, no text no watermark, high quality, square format",
    "size": "2048x2048",
    "n": 1
  }'
```

### 步骤 2：输出封面

**直接使用 AI 生成的图片作为封面，不需要拼接！**

```bash
# 直接使用生成的图片
cp ai_image.jpg final_cover.jpg

# 如果需要调整尺寸
convert ai_image.jpg -resize 1080x1080^ -gravity center -extent 1080x1080 final_cover.jpg
```

## 示例

**主题**：技能安全审计

**Prompt**：
```
cute cartoon illustration style, a friendly robot holding a magnifying glass examining a glowing blue skill card, shield icon, security check concept, kawaii anime style, soft pastel blue and white colors, minimal clean background, with bold Chinese text "装这个Skill之前" on top, no watermark, high quality, square format
```

**配色**：
- 主色调：蓝色 + 白色
- 最终尺寸：1080x1080（正方形）
- **直接使用 AI 生成的图片，不需要拼接**
