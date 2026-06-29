---
slug: xiaohongshu-booster
name: Xiaohongshu Note Booster
version: 1.0.0
author: ClawHub Community
category: Content Creation
description: Generate 3 viral-ready Xiaohongshu (Little Red Book) notes from a product, scene, or topic — titles, body copy, hashtags, cover-image tips, and publish-time recommendations.
model: agent
tags:
  - xiaohongshu
  - little-red-book
  - content-creation
  - social-media
  - copywriting
  - chinese-marketing
  - viral-content
---

# 📕 Xiaohongshu Note Booster (小红书爆款笔记生成器)

Generate **3 complete, ready-to-publish Xiaohongshu notes** from a single input — a product name, restaurant review, outfit, or trending topic. Each note includes a viral-style title, structured body copy (150–300 Chinese characters), optimized hashtags, cover-image composition tips, and suggested publish time.

> **Target platform**: Xiaohongshu (小红书 / Little Red Book) — China's leading social commerce and lifestyle platform with 300M+ monthly active users.
>
> **Output format**: 3 style-differentiated variants per run, suitable for A/B testing or multi-post content calendars.

---

## Table of Contents

1. [Workflow (8 Steps)](#1-workflow-8-steps)
2. [Installation & Setup](#2-installation--setup)
3. [Usage](#3-usage)
   - [CLI Mode](#cli-mode)
   - [Agent / LLM Mode](#agent--llm-mode)
4. [Sample Prompts (5 Examples with Expected Output)](#4-sample-prompts-5-examples-with-expected-output)
5. [Real-World Task Examples (3 Scenarios)](#5-real-world-task-examples-3-scenarios)
6. [First-Success Path (30-Second Guide)](#6-first-success-path-30-second-guide)
7. [File Structure](#7-file-structure)
8. [Configuration & Customization](#8-configuration--customization)

---

## 1. Workflow (8 Steps)

### Step 1: Capture Input 🔍
Accept user's product name, scene/service, or topic. Optionally capture selling points, target audience, writing style, and content category.

**Input sources**:
- Direct CLI arguments (`--topic "..." --selling-points "...")`
- Natural language prompt ("I need a post for my new rose toner...")
- Structured JSON via agent

### Step 2: Analyze Topic & Extract Core Keywords 🏷️
Parse the input to identify:
- Core subject
- Implicit or explicit selling points (up to 5)
- Target audience signal
- Category (beauty, fashion, food, etc.)

### Step 3: Select Writing Template 📝
Choose one of 6 template archetypes based on the style parameter:
- **亲切种草** (Friendly recommendation) — default, highest engagement
- **干货分享** (Educational / tips)
- **测评对比** (Review / comparison)
- **开箱体验** (Unboxing)
- **Vlog文案** (Vlog script style)
- **教程攻略** (Tutorial)

### Step 4: Generate 3 Title Variants 🎯
Create one title per note variant using different psychological hooks:
- **Variant 1 — Pain-point driven**: Targets reader anxiety or frustration
- **Variant 2 — Emotional resonance**: Creates connection and relatability
- **Variant 3 — Contrast / curiosity**: Sparks "what changed?" intrigue

Each title: ≤20 Chinese characters, 1 emoji prefix, specific pattern template.

### Step 5: Compose Body Copy ✍️
Generate 150–300 Chinese character body following the viral XHS structure:

1. **Pain-point hook** (1–2 lines) — relatable frustration 😭😩
2. **Product introduction** (1 line) — "I found this!"
3. **Usage experience** (2–3 lines) — sensory details, texture, feel
4. **Quantifiable result** (1–2 lines) — "after X days, Y happened"
5. **Skeptic-proof detail** (1 line) — skin type, price, ingredient proof
6. **Call to action** (1 line) — comment, try it, tag a friend

### Step 6: Select Hashtags 🔗
Pick 6–9 hashtags from a curated library covering all categories:
- 1–2 broad tags (high traffic, e.g., #护肤)
- 2–3 niche tags (targeted, e.g., #敏感肌)
- 1–2 scene tags (e.g., #熬夜护肤)
- 1–2 product/brand tags (e.g., #玫瑰精华水)

### Step 7: Generate Cover Image Tip 🖼️
For each note, suggest:
- Cover description
- Composition guidance (angle, lighting, background)
- Text overlay recommendation (≤8 Chinese characters)

### Step 8: Recommend Publish Time ⏰
Suggest optimal posting time based on category:
- Beauty: 20:00–22:00 (peak browsing)
- Fashion: 12:00–13:00 (lunch break)
- Food: 17:30–19:00 (pre-dinner planning)

---

## 2. Installation & Setup

```bash
# The skill is self-contained — no external dependencies.
# Core script runs with Python 3.8+

python3 scripts/generate.py --help
```

**No API keys required.** All content is generated locally using templates and randomized selection from curated style libraries.

> For AI-assisted generation (LLM mode), connect an LLM provider (e.g., DeepSeek, GPT-4) at the agent level. The script itself is template-based for reliability and speed.

---

## 3. Usage

### CLI Mode

```bash
# Basic usage — just a topic
python3 scripts/generate.py --topic "玫瑰精华水"

# Full configuration
python3 scripts/generate.py \
  --topic "玫瑰精华水" \
  --selling-points "补水保湿,提亮肤色,敏感肌可用" \
  --audience "18-30岁女性" \
  --style "亲切种草" \
  --category beauty \
  --count 3 \
  --pretty

# Save to file
python3 scripts/generate.py \
  --topic "白色阔腿裤" \
  --selling-points "显瘦,垂坠感好,百搭" \
  --category fashion \
  --output notes.json \
  --pretty
```

### Agent / LLM Mode

```json
// Input JSON (matching schemas/input.schema.json)
{
  "topic": "玫瑰精华水",
  "selling_points": ["补水保湿", "提亮肤色", "敏感肌可用"],
  "target_audience": "18-30岁女性",
  "style": "亲切种草",
  "category": "beauty",
  "count": 3
}
```

---

## 4. Sample Prompts (5 Examples with Expected Output)

### Prompt 1: Beauty Product — Minimal Input

**Input**:
```
Topic: 玫瑰精华水
```

**Expected Output** (abbreviated — 1 of 3 variants shown):

```json
{
  "note_number": 1,
  "style_label": "数字型·痛点直击",
  "title": "💧 这瓶玫瑰水救了我的熬夜脸！素颜也能发光",
  "body": "姐妹们！！熬夜后脸真的又黄又干😭\n最近挖到这瓶玫瑰精华水，冷门但巨好用！\n质地像精华一样润，拍两遍脸就软软嫩嫩的\n坚持了一周，早上照镜子明显感觉脸亮了\n敏感肌亲测不刺痛，成分很干净\n现在化妆前用它打底，底妆都服帖很多！\n已经回购第二瓶了！你们还有什么好推荐？",
  "hashtags": ["玫瑰精华水", "护肤", "熬夜护肤", "敏感肌", "补水保湿", "成分党", "安利一个护肤品"],
  "cover_tip": {
    "description": "手拿产品对光拍摄，背景干净桌面",
    "composition": "Top-down flat lay or hand holding product in natural window light",
    "text_overlay": "熬夜脸有救了"
  },
  "publish_time": "20:00-22:00"
}
```

---

### Prompt 2: Restaurant Review

**Input**:
```
Topic: 上海静安寺日式烧肉店
Selling points: 和牛入口即化, 环境适合约会, 人均200
Category: food
```

**Expected Output**:

```json
{
  "note_number": 1,
  "style_label": "数字型·痛点直击",
  "title": "🔥 上海人均200吃到了人生烧肉🥩 约会必去",
  "body": "📍 藏在巷子里，氛围感已经赢了一半\n店内灯光暖黄，很适合约会聊天\n说说出品：\n✅ 和牛入口即化\n✅ 环境适合约会\n✅ 人均200\n服务员很贴心，会帮你掌握火候\n整体来说，如果是约会来的话，绝对不踩雷！\n💬 有人去过这家吗？评论区聊聊体验",
  "hashtags": ["上海探店", "日式烧肉", "约会餐厅", "美食探店", "宝藏店铺", "氛围感餐厅", "魔都美食"],
  "cover_tip": {
    "description": "烤架上和牛特写，火焰微光",
    "composition": "Close-up of food cooking, steam/mist visible, warm backlight",
    "text_overlay": "人均200吃和牛"
  },
  "publish_time": "17:30-19:00"
}
```

---

### Prompt 3: Fashion Item

**Input**:
```
Topic: 白色阔腿裤
Selling points: 显瘦, 垂坠感好, 百搭
Audience: 通勤女性
Category: fashion
```

**Expected Output**:

```json
{
  "note_number": 1,
  "style_label": "数字型·痛点直击",
  "title": "💯 梨形身材都去买这条白裤子！显瘦到离谱",
  "body": "本梨形身材终于找到命定白色阔腿裤了！\n找到一条合适的裤子比找对象还难😩\n但是！这条真的很🉑\n✅ 显瘦\n✅ 垂坠感好\n✅ 百搭\n上班搭衬衫，周末搭背心都好看\n已经入了第二条换着穿！\n你觉得怎么样？评论区告诉我你的身材焦虑👇",
  "hashtags": ["白色阔腿裤", "穿搭", "梨形身材", "通勤穿搭", "显瘦穿搭", "百搭单品", "OOTD"],
  "cover_tip": {
    "description": "全身穿搭照，自然光，突出裤型",
    "composition": "Full-body mirror shot in daylight, phone at chin height",
    "text_overlay": "梨形身材必买"
  },
  "publish_time": "12:00-13:00"
}
```

---

### Prompt 4: Digital Product

**Input**:
```
Topic: MacBook Air M4
Selling points: 轻薄, 续航强, 性能提升
Audience: 学生党
Category: digital
```

**Expected Output**:

```json
{
  "note_number": 1,
  "style_label": "数字型·痛点直击",
  "title": "✨ 学生党别乱买了！MacBook Air M4真的够用",
  "body": "最近一直被这个问题困扰😩\n直到发现了MacBook Air M4，真的打开了新世界！\n轻薄、续航强、性能提升，每一个都让我很满意\n用了一段时间，效果比我预期的还好\n图书馆用一天不用充电，写论文剪视频都不卡\n还在犹豫的朋友可以放心冲\n有问题评论区问我👇",
  "hashtags": ["数码好物", "数码", "好物分享", "苹果", "生产力工具", "学生党数码", "提升效率"],
  "cover_tip": {
    "description": "高颜值产品近景特写，配简洁文字",
    "composition": "Close-up hero shot, centered, clean background",
    "text_overlay": "亲测好用"
  },
  "publish_time": "20:00-22:00"
}
```

---

### Prompt 5: Empty / Minimal Input → Fallback

**Input**:
```
Topic: 周末去哪儿
Category: travel
```

**Expected Output**:

```json
{
  "note_number": 1,
  "style_label": "数字型·痛点直击",
  "title": "🌟 周末别再宅家了！这些地方真的值得去",
  "body": "最近一直被这个问题困扰😩\n直到发现了周末去哪儿，真的打开了新世界！\n每一个地方都让我很满意\n去了一次，效果比我预期的还好\n还在犹豫的朋友可以放心冲\n有问题评论区问我👇",
  "hashtags": ["旅行", "周末去哪儿", "旅行攻略", "小众景点", "旅游", "度假", "城市漫步"],
  "cover_tip": {
    "description": "高颜值产品近景特写，配简洁文字",
    "composition": "Close-up hero shot, centered, clean background",
    "text_overlay": "亲测好用"
  },
  "publish_time": "20:00-22:00"
}
```

---

## 5. Real-World Task Examples (3 Scenarios)

### Scenario 1: Beauty Brand Promotion (商家上新)

**Situation**: A beauty brand just launched a new rose essence toner. The social media manager needs 3 note variants for the next 3 days' content calendar.

**Input**:
```
Topic: 玫瑰精华水
Selling points: 补水保湿, 提亮肤色, 敏感肌可用
Target audience: 18-30岁女性
Style: 亲切种草
Category: beauty
Count: 3 (3 variants generated)
```

**Step-by-step**:

1. Parse input → extract keywords: [玫瑰精华水, 补水, 提亮, 敏感肌]
2. Select style template: **亲切种草** (pain → discovery → delight arc)
3. Generate title variants:
   - V1 (Pain-point): 💧 这瓶玫瑰水救了我的熬夜脸！素颜也能发光
   - V2 (Emotional): 💖 用了这瓶玫瑰水后，我终于敢素颜出门了
   - V3 (Contrast): 🌟 以前盲目跟风，现在只用这瓶玫瑰水就够了
4. Compose body for each variant with the beauty template
5. Attach hashtags from beauty + specific product tags
6. Generate cover tips (flat lay, hand-holding, before/after)
7. Recommend publish times (evening peak for beauty)

**Output** (3 notes, abbreviated for space):

```json
{
  "notes": [
    {
      "note_number": 1,
      "style_label": "数字型·痛点直击",
      "title": "💧 这瓶玫瑰水救了我的熬夜脸！素颜也能发光",
      "body": "姐妹们！！熬夜后脸真的又黄又干😭\n最近挖到这瓶玫瑰精华水，冷门但巨好用！\n质地像精华一样润，拍两遍脸就软软嫩嫩的\n坚持了一周，早上照镜子明显感觉脸亮了\n敏感肌亲测不刺痛，成分很干净\n现在化妆前用它打底，底妆都服帖很多！\n已经回购第二瓶了！你们还有什么好推荐？",
      "hashtags": ["玫瑰精华水", "护肤", "熬夜护肤", "敏感肌", "补水保湿", "成分党", "安利一个护肤品"],
      "cover_tip": {"description": "手拿产品对光拍摄，背景干净桌面", "composition": "Top-down flat lay or hand holding product in natural window light", "text_overlay": "熬夜脸有救了"},
      "publish_time": "20:00-22:00"
    },
    {
      "note_number": 2,
      "style_label": "情感型·共鸣种草",
      "title": "💖 敏感肌终于找到本命精华水了！相见恨晚",
      "body": "换季时候皮肤状态差到不想照镜子😩\n也是被姐妹安利的玫瑰精华水，一试就停不下来\n抹上去凉凉的，嗖一下就吸收了，完全不黏\n用了三天，化妆都不卡粉了！\n无酒精无香精，烂脸期用也没问题\n你是什么肤质？评论区聊聊",
      "hashtags": ["敏感肌", "精华水", "护肤", "精简护肤", "我的护肤日常", "换季护肤"],
      "cover_tip": {"description": "护肤品空瓶排列，展示使用痕迹", "composition": "Flat lay of empty bottles in a row, warm lighting", "text_overlay": "空瓶才有说服力"},
      "publish_time": "12:00-13:00"
    },
    {
      "note_number": 3,
      "style_label": "对比型·效果冲击",
      "title": "🌟 以前盲目跟风，现在只用这瓶玫瑰水就够了",
      "body": "素颜完全出不了门，气色差到离谱\n抱着试试的心态入了玫瑰精华水，结果真香了\n味道是淡淡的玫瑰味，每次用都很治愈\n皮肤状态稳定了好多，泛红都少了\n查了成分表，都是温和有效的成分\n姐妹们真的可以试试！评论区告诉我你的肤质",
      "hashtags": ["补水保湿", "精华水", "素颜", "好皮肤", "成分党", "护肤品推荐"],
      "cover_tip": {"description": "护肤品空瓶排列，展示使用痕迹", "composition": "Flat lay of empty bottles in a row, warm lighting", "text_overlay": "空瓶才有说服力"},
      "publish_time": "21:00-22:00"
    }
  ],
  "metadata": {
    "generated_at": "2026-06-16T10:23:00+00:00",
    "total_notes": 3,
    "input_topic": "玫瑰精华水",
    "style": "亲切种草",
    "target_audience": "18-30岁女性"
  }
}
```

---

### Scenario 2: Restaurant Promotion (探店推广)

**Situation**: A new Japanese yakiniku restaurant in Shanghai needs Instagram/XHS content. The owner provides basic info.

**Input**:
```
Topic: 上海静安寺日式烧肉店
Selling points: 和牛入口即化, 环境适合约会, 人均200
Style: 亲切种草
Category: food
```

**Steps**: Similar workflow as Scenario 1, using the food/restaurant body template, hashtags from food travel, cover tip close-up hero shot with steam.

**Key output characteristics**:
- Title includes location marker and price (essential for XHS food posts)
- Body structured as review with bullet-point highlights
- Cover emphasizes the hero dish (BBQ on grill)
- Publish time: 17:30–19:00 (pre-dinner planning window)

---

### Scenario 3: Fashion Content Calendar (穿搭日更)

**Situation**: A fashion blogger needs 3 consecutive days of outfit content for a white wide-leg pants series.

**Input**:
```
Topic: 白色阔腿裤
Selling points: 显瘦, 垂坠感好, 百搭
Target audience: 通勤女性
Category: fashion
```

**Key output characteristics**:
- Titles target a specific body type ("梨形身材" for relatability)
- Body uses the fashion template with pain-point relatability
- Hashtags mix fashion + body type + scene tags
- Cover is full-body mirror shot
- Publish times staggered (lunch, evening, morning) for reach testing

---

## 6. First-Success Path (30-Second Guide)

Get your first Xiaohongshu note in under 30 seconds:

```bash
# Step 1: Run the core script with any product or topic
# (No setup, no API key needed)
python3 /path/to/xiaohongshu-booster/scripts/generate.py \
  --topic "玫瑰精华水" \
  --selling-points "补水保湿,提亮肤色" \
  --audience "18-30岁女性" \
  --style "亲切种草" \
  --category beauty \
  --pretty

# Step 2: Copy the JSON output

# Step 3: Extract the first note's title + body + hashtags
# Paste directly into Xiaohongshu's note editor

# Step 4: Create a cover image following the cover_tip
# (hand holding product, clean desk, natural light)

# Step 5: Publish at the recommended time (20:00-22:00)
```

**Alternative: Natural-language prompt (agent mode)**:

> "I need 3 Xiaohongshu posts for my new rose toner. It's hydrating, brightening, and safe for sensitive skin. Target audience is women 18-30. Give me titles, body copy, hashtags, and cover tips."

That's it — **30 seconds from idea to ready-to-publish note**. 🚀

---

## 7. File Structure

```
xiaohongshu-booster/
├── SKILL.md                  # This document — full skill documentation
├── skill.json                # Skill metadata (MIT-0 license)
├── scripts/
│   └── generate.py           # Core generation script (Python 3)
├── schemas/
│   ├── input.schema.json     # JSON Schema for input validation
│   └── output.schema.json    # JSON Schema for output structure
└── references/
    ├── templates.md          # Writing templates & structural patterns
    ├── hashtags.md           # Curated hashtag library by category
    └── cover-tips.md         # Cover image guidelines & composition tips
```

---

## 8. Configuration & Customization

### Script Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--topic` | string | (required) | Product, scene, or topic name |
| `--selling-points` | string | None | Comma-separated selling points |
| `--audience` | string | "通用人群" | Target audience descriptor |
| `--style` | string | "亲切种草" | Writing style (6 options) |
| `--category` | string | "other" | Content category (10 options) |
| `--count` | int | 3 | Number of variants (1-5) |
| `--include-disclaimer` | flag | false | Add compliance disclaimer |
| `--output` | string | stdout | Save to file instead of stdout |
| `--pretty` | flag | false | Pretty-print JSON |

### Custom Templates

To add new title patterns or body templates, edit the `TITLE_TEMPLATES` and `GENERIC_BODIES` dicts in `scripts/generate.py`.

### Custom Hashtags

Edit `HASHTAG_LIBRARY` in `scripts/generate.py` or `references/hashtags.md` to add or modify hashtag pools.

### Adding a New Category

1. Add the category name to the `--category` choices in `scripts/generate.py`
2. Add hashtag pool in `HASHTAG_LIBRARY`
3. Add publish times in `PUBLISH_TIMES`
4. Add cover tips in `COVER_TIPS`
5. Add body template in `GENERIC_BODIES`

---

## Compliance Notes ⚠️

- **Avoid absolute language**: Do not use "best", "#1", "first" — XHS algorithm penalizes aggressive claims
- **Sensitive categories**: Skincare, supplements, and medical-adjacent products should include a disclaimer
- **No platform scraping**: This skill generates content only; it does not scrape or interact with Xiaohongshu's API
- **Individual results vary**: All generated content is for reference; actual performance depends on content quality, timing, and audience engagement

---

## License

MIT-0 — No attribution required. Free to use, modify, and distribute.
