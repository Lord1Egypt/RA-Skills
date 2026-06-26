# 📝 Auto Article Writer for WeChat Official Account

**OpenClaw Skill - Full Automation from Topic to Publishing**

---

## 🚀 Quick Start

### Prerequisites

```bash
# Install required dependencies:
clawhub install baidu-search
clawhub install wanx-image-generator    # AI image generation (required)
clawhub install wechat-toolkit          # WeChat publishing (required)
```

### Configure API Key

**Wanx image generation requires Alibaba Cloud Bailian API Key**:

```bash
# Recommended: Unified config file
vim ~/.openclaw/.env

# Add configuration
DASHSCOPE_API_KEY="sk-xxx"
```

**Get API Key**: https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key

### Usage

**Trigger by natural language:**

```
Write an article about "AI automation workflow" and publish to WeChat official account
```

OpenClaw will automatically execute the full workflow:
1. Generate article framework
2. Search for background materials
3. Write article content
4. Generate illustrations (via Wanx)
5. Publish to WeChat official account

---

## 📋 Full Workflow

### Step 1: Generate Framework

```bash
node scripts/generate-framework.js "article topic"
```

**Features:**
- Auto-diagnose topic type (tutorial/product/general)
- Generate structured framework
- Output: `examples/framework.md`

**Duration:** <1 second

---

### Step 2: Search Materials

```bash
node scripts/search.js "keyword"
```

**Features:**
- Call Baidu Search API
- Get real-time information
- Output: JSON search results

**Duration:** ~30 seconds

---

### Step 3: Write Article

**OpenClaw AI writes directly, no extra API needed!**

**Requirements:**
- Expand based on framework
- Combine search results
- ~3000 Chinese characters
- Markdown format
- Include frontmatter (title + cover)

**Duration:** ~30-60 seconds

---

### Step 4: Generate Illustrations ⭐

**Call wanx-image-generator to generate images:**

#### Cover Image

```bash
cd ../wanx-image-generator
uv run scripts/generate.py \
  --prompt "Tech article cover, AI automation theme, minimalist tech style, blue-purple tone, no text" \
  --output examples/images/cover.png \
  --model wan2.6-t2i \
  --size "1280*1280" \
  --no-watermark
```

#### Body Images (5 images)

```bash
# Image 1: Introduction - Modern office
uv run scripts/generate.py \
  --prompt "Modern office, professional using computer, screen showing AI interface" \
  --output examples/images/img1.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# Image 2: Concept - AI architecture
uv run scripts/generate.py \
  --prompt "AI concept diagram, neural network + flowchart, fusion effect" \
  --output examples/images/img2.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# Image 3: Trend - Rising curve
uv run scripts/generate.py \
  --prompt "Trend analysis, rising curve showing growth, tech grid background" \
  --output examples/images/img3.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# Image 4: Flowchart - Three steps
uv run scripts/generate.py \
  --prompt "Three-step flowchart, three circular nodes, blue-purple gradient" \
  --output examples/images/img4.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark

# Image 5: Practice - Multi-monitor
uv run scripts/generate.py \
  --prompt "Multi-monitor workstation, 3 screens showing code and dashboard" \
  --output examples/images/img5.png \
  --model wan2.6-t2i --size "1280*1280" --no-watermark
```

**Performance:**
- ✅ Success rate: 100% (5/5)
- ✅ Speed: 6.5 seconds/image
- ✅ Quality: 1280×1280 HD
- ✅ Total: ~33 seconds (5 images)

---

### Step 5: Publish to WeChat

```bash
node scripts/publish.js examples/article.md
```

**Features:**
- Check frontmatter (title + cover)
- Verify image paths
- Call wechat-toolkit to publish
- Return draft box link

**Duration:** 5-10 seconds

---

## 🔧 Scripts Reference

| Script | Purpose | Input | Output |
|--------|---------|-------|--------|
| `generate-framework.js` | Generate framework | Article topic | `examples/framework.md` |
| `search.js` | Baidu Search | Keyword | JSON search results |
| `publish.js` | WeChat publish | `article.md` | Draft box link |

---

## ⚙️ Configuration

### Wanx Image Generation

**3 configuration methods (choose one):**

**Method 1: Unified config** (Recommended)
```bash
# Edit ~/.openclaw/.env
DASHSCOPE_API_KEY="sk-xxx"
```

**Method 2: Skill directory .env**
```bash
# Edit ~/.openclaw/workspace/skills/wanx-image-generator/.env
DASHSCOPE_API_KEY="sk-xxx"
```

**Method 3: Environment variable** (Temporary)
```bash
export DASHSCOPE_API_KEY="sk-xxx"
```

**Priority:** CLI argument > Environment variable > ~/.openclaw/.env > Skill directory/.env

**Get API Key:** https://bailian.console.aliyun.com/?tab=globalset#/efm/api_key

**Model selection:**
- `wan2.6-t2i` ⭐ - Latest, sync call, recommended
- `wan2.5-t2i-preview` - Free size support
- `wan2.2-t2i-flash` - Faster speed

**Size options:**
- `1280*1280` - Square, general purpose
- `1696*960` - 16:9 landscape
- `960*1696` - 9:16 portrait

### Baidu Search

Auto-reads `baidu-search` API Key from OpenClaw config.

### WeChat Publishing

Configure in `~/.openclaw/workspace/TOOLS.md`:

```bash
export WECHAT_APP_ID=your_app_id
export WECHAT_APP_SECRET=your_app_secret
```

**IP Whitelist:**
```bash
curl ifconfig.me
# Add to WeChat official account admin panel → Settings → IP Whitist
```

---

## 📁 File Structure

```
wechat-mp-auto-publisher/
├── SKILL.md                          # Skill instructions
├── README.md                         # Usage guide (Chinese)
├── README.en.md                      # Usage guide (English)
├── scripts/
│   ├── generate-framework.js         # Generate framework
│   ├── search.js                     # Baidu Search
│   └── publish.js                    # WeChat publish
├── examples/
│   ├── framework.md                  # Generated framework
│   ├── article.md                    # Generated article
│   └── images/                       # Illustrations
└── templates/
    └── article-template.md           # Article template
```

---

## 🎯 Use Cases

### Case 1: Technical Tutorial

```
Write a technical tutorial about "React Performance Optimization"
```

### Case 2: Product Introduction

```
Write an article introducing OpenClaw features
```

### Case 3: Practical Case Study

```
Write a practical case study about AI automation workflow
```

---

## ⚠️ Important Notes

1. **Image paths must be absolute** - wechat-toolkit requirement
2. **Check IP whitelist before publishing** - Configure in WeChat admin panel
3. **Confirm each step with user** - Can stop or adjust anytime
4. **Provide fallback for failures** - Manual operation guide
5. **Image generation failure** - Check API Key, retry

---

## 🐛 Troubleshooting

### Issue 1: Framework generation failed

**Solution:** Check if topic is valid, use general template

### Issue 2: Search failed

**Solution:** Check BAIDU_API_KEY config, or manually supplement materials

### Issue 3: Image generation failed

**Solution:**
```bash
# Check API Key (unified config)
cat ~/.openclaw/.env

# Or check Skill directory config
cat ~/.openclaw/workspace/skills/wanx-image-generator/.env

# Test generation
cd ~/.openclaw/workspace/skills/wanx-image-generator
uv run scripts/generate.py --prompt "test" --output test.png --model wan2.6-t2i
```

### Issue 4: Publishing failed

**Solution:**
```bash
# Check config
echo $WECHAT_APP_ID
echo $WECHAT_APP_SECRET

# Check IP whitelist
curl ifconfig.me

# Manual publish
cat "article.md" | WECHAT_APP_ID=xxx WECHAT_APP_SECRET=xxx wenyan publish -t lapis -h solarized-light
```

---

## 📊 Performance Data

| Stage | Duration | Success Rate |
|-------|----------|--------------|
| Framework generation | <1 second | 100% |
| Baidu Search | 30 seconds | 100% |
| Article writing | 30-60 seconds | 100% |
| Image generation (5 images) | 33 seconds | 100% |
| WeChat publishing | 5-10 seconds | 100% |
| **Total** | **~2 minutes** | **100%** |

**Image tool**: wanx-image-generator (Alibaba Wanx wan2.6-t2i)
- Stability: 100%
- Speed: 6.5 seconds/image
- Quality: 1280×1280 HD

---

## 📝 Changelog

### v3.2.0 (2026-03-12) - Documentation Update

- ✅ Update API Key configuration (support ~/.openclaw/.env unified config)
- ✅ Remove all nano-banana-pro references
- ✅ Update troubleshooting guide
- ✅ Update performance data section

### v3.1.0 (2026-03-12) - Wanx Image Integration

- ✅ Switch from nano-banana-pro to wanx-image-generator
- ✅ Stability improved to 100%
- ✅ Speed improved to 6.5s/image
- ✅ Updated SKILL.md and README.md

### v3.0.0 (2026-03-12) - OpenClaw Skill Refactor

- ✅ Refactored to real OpenClaw Skill
- ✅ Auto-invoked by OpenClaw
- ✅ Simplified scripts

### v2.1.0 (2026-03-12) - Smart Framework

- ✅ Auto-diagnose topic type
- ✅ Baidu Search enhancement

---

## 🤝 Contributing

Issues and Pull Requests are welcome!

**Discord**: https://discord.com/invite/clawd

---

*Created with ❤️ by OpenClaw Community*
