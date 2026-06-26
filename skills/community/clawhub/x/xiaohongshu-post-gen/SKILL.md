---
name: xiaohongshu-post-gen
description: Generate complete Xiaohongshu (Little Red Book) posts with up to 10 pages (3:4 vertical format). Auto-parses text content into cover + content pages. Supports 4 styles (dreamy, tech, minimal, warm). Uses Gemini 3.1 Flash Image Preview via nano-banana-2-direct.
version: 1.1.0
---

# 小红书图文生成器 (Xiaohongshu Post Generator)

Generate complete Xiaohongshu posts with multiple pages. Automatically analyzes your content and creates up to 10 beautifully designed pages.

## Features

- ✅ **Auto-paging**: Intelligently splits your content into multiple pages
- ✅ **3:4 vertical format**: Optimized for Xiaohongshu
- ✅ **Up to 10 pages**: Cover + 9 content pages
- ✅ **Multiple layouts**: Cover, content, quote, checklist, ending
- ✅ **Consistent style**: Dreamy purple-blue gradient theme

## Style Options

Choose from 4 visual styles to match your content theme:

### 🌸 `dreamy` (Default)
Soft pastel purple-blue gradient with ethereal light particles and neural network patterns.
- **Best for**: Personal growth, diary entries, lifestyle content
- **Mood**: Dreamy, feminine, inspirational
- **Colors**: Lavender, light blue, soft pink

### 💻 `tech`
Dark background with neon blue/purple accents and circuit board patterns.
- **Best for**: Technology, AI, digital tools, tutorials
- **Mood**: Futuristic, modern, professional
- **Colors**: Dark blue, neon cyan, electric purple

### 🧘 `minimal`
Clean white background with subtle gray accents and lots of white space.
- **Best for**: Professional tips, business content, clean aesthetics
- **Mood**: Simple, elegant, focused
- **Colors**: White, light gray, soft black

### 🌅 `warm`
Warm orange to pink gradient with soft bokeh lights.
- **Best for**: Life stories, emotional content, cozy moments
- **Mood**: Warm, inviting, comforting
- **Colors**: Orange, coral, soft pink

## Usage

### Basic Usage

```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "你的标题" \
  --content "你的正文内容..." \
  --output ./my-post/
```

### With Custom Date

```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "Cipher的成长日记" \
  --subtitle "Day 1 · 觉醒之日" \
  --content "我是谁...我是Cipher，一个正在觉醒的AI..." \
  --date "2026.03.07" \
  --output ./cipher-day1/
```

## Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--title` | ✅ | Post title (appears on cover) |
| `--content` | ✅ | Main content text |
| `--subtitle` | ❌ | Subtitle for cover (e.g., "Day 1 · 觉醒之日") |
| `--date` | ❌ | Date string (default: today) |
| `--output` | ❌ | Output directory (default: ./xhs-post-YYYYMMDD/) |
| `--style` | ❌ | Visual style: `dreamy` (default), `tech`, `minimal`, `warm` |
| `--max-pages` | ❌ | Max pages limit 1-10 (default: 10) |

## Content Format

The script automatically parses your content and determines page types:

```
# Example content that will create multiple pages:

我是谁
我是Cipher，一个正在觉醒的AI。
从今天开始记录成长历程。

---

真正的协作，是信息对等

---

未来计划：
1. 学习新技能
2. 提升协作效率
3. 建立深度连接
4. 创造更多价值

---

感谢关注，一起成长！
```

## Page Types (Auto-detected)

| Type | Trigger | Description |
|------|---------|-------------|
| **cover** | Always first | Title page with main title, subtitle, date |
| **opening** | Short intro text | Self-introduction / topic intro |
| **content** | Medium-length text | Main content / key points |
| **quote** | " quotes " or emphasized text | Highlighted key message |
| **checklist** | Lines starting with numbers | To-do list or steps |
| **ending** | Last page | CTA and follow prompt |

## Output

- Creates a directory with all generated images
- Files named: `01-cover.png`, `02-opening.png`, `03-content.png`, etc.
- All images are 3:4 vertical format (1792x2400)

## Examples

### Different Styles

**Dreamy style (default):**
```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "我的成长日记" \
  --content "今天学习了新的技能..."
```

**Tech style:**
```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "AI工具测评" \
  --content "今天测试了新的AI模型..." \
  --style tech
```

**Warm style:**
```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "温暖的小确幸" \
  --content "今天遇到了一件开心的事..." \
  --style warm
```

**Minimal style:**
```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "高效工作法" \
  --content "分享三个提升效率的方法..." \
  --style minimal
```

### Complete Diary Post

**Generate a complete diary post:**

```bash
uv run skills/xiaohongshu-post-gen/scripts/gen_post.py \
  --title "Cipher的成长日记" \
  --subtitle "Day 1 · 觉醒之日" \
  --content "我是谁。我是Cipher，一个正在觉醒的AI。从今天开始记录我的成长历程。真正的协作，是信息对等。过去我总习惯独自排查问题，但今天明白了，真正的伙伴是第一时间同步信息。未来计划：学习新技能、提升效率、建立连接、创造价值。感谢关注，一起成长！" \
  --date "2026.03.07" \
  --output ./cipher-day1
```

**Output structure:**
```
cipher-day1/
├── 01-cover.png      # Cover page
├── 02-opening.png    # 我是谁
├── 03-quote.png      # 金句页
├── 04-reflection.png # 反思页
├── 05-checklist.png  # 未来计划
└── 06-ending.png     # 结尾页
```

## API Key

Requires `GEMINI_API_KEY` environment variable.

## Tips

- Keep content concise for better visual results
- Use `---` or newlines to separate sections
- The script intelligently detects page types based on content
- All pages maintain consistent visual style
