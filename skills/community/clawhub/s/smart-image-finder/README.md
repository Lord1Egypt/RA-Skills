# Smart Image Finder 🖼️

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

A complete image search and download solution for AI agents — find high-quality images for articles, dashboards, and content creation.

**🚀 No browser required** — all operations run in background via CLI.

### ✨ Features

- **Three acquisition methods**: News site extraction, Brave image search, AI generation
- **11+ verified sources**: Reuters, TechCrunch, Bloomberg, BBC, NBC News, and more
- **HD parameter optimization**: Best download parameters for each source
- **Pure CLI workflow**: No browser needed, runs entirely in background
- **Complete troubleshooting**: Common issues and solutions

### 🎯 Use Cases

| Scenario | Recommended Method |
|----------|-------------------|
| Article illustrations | News site extraction / AI generation |
| News thumbnails | News site extraction |
| Dashboard display | Brave image search |
| Concept/creative images | AI generation |

### 🚀 Quick Start

#### Method 1: Extract from News Sites (No Browser)

```bash
# Extract image URL from page HTML
IMG_URL=$(curl -sL "https://www.reuters.com/article/..." | \
  grep -oE 'https://www\.reuters\.com/resizer/v2/[^"]+\.jpg' | head -1)

# Download with HD parameters
curl -sL -o photo.jpg "${IMG_URL}?width=3000&quality=100"

# Verify
file photo.jpg
```

#### Method 2: Brave Image Search (No Browser)

```bash
export BRAVE_API_KEY="your_key"

# Search and download in one line
IMG_URL=$(curl -s "https://api.search.brave.com/res/v1/images/search?q=SpaceX%20Starship%202025&count=1" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq -r '.results[0].properties.url')
curl -sL -o spacex.jpg "$IMG_URL"
```

#### Method 3: AI Generation (No Browser)

```bash
# Pollinations - completely free, no API key
curl -sL -o cover.jpg "https://image.pollinations.ai/prompt/futuristic%20AI%20concept%20minimalist%20tech%20style?width=1920&height=1080&nologo=true"
```

### 📊 Supported News Sources

#### ✅ Direct Download Works

| Source | Category | Grep Pattern |
|--------|----------|--------------|
| Reuters | Politics/International | `reuters\.com/resizer/v2/[^"]+\.jpg` |
| TechCrunch | Tech/AI | `techcrunch\.com/wp-content/uploads/[^"]+\.jpg` |
| Bloomberg | Business | `assets\.bwbx\.io/images/[^"]+\.(jpg\|webp)` |
| BBC | International | `ichef\.bbci\.co\.uk/news/[0-9]+/[^"]+\.jpg` |
| France24 | International | `s\.france24\.com/media/display/[^"]+\.jpg` |
| Spaceflight Now | Space | `spaceflightnow\.com/wp-content/uploads/[^"]+\.jpg` |
| ThePaper | Chinese | `imagepphcloud\.thepaper\.cn/pph/image/[^"]+\.jpg` |

#### ⚠️ Requires Manual Save or Alternative

| Source | Issue | Solution |
|--------|-------|----------|
| Guardian | URL signature | Use Brave search |
| The Verge | Complex CDN | Use Brave search |
| CNN | JS rendering | Use Brave search |
| AP News | Params fail | Manual save |

### 📁 File Structure

```
smart-image-finder/
├── SKILL.md          # AI Agent guide (main file)
├── README.md         # This document
└── scripts/
    ├── download.sh   # Batch download script
    └── verify.sh     # Image verification script
```

### 💡 Best Practices

#### Search Tips

```bash
# ❌ Too broad
"technology meeting"

# ✅ Add year and specific event
"Keir Starmer Xi Jinping Beijing January 2025"

# ✅ Restrict to source
"site:reuters.com Trump tariff announcement"
```

#### Image Verification

```bash
# Confirm it's an image, not HTML
file downloaded.jpg
# Should output: JPEG image data, ...

# Check dimensions (requires ImageMagick)
identify -format '%wx%h' downloaded.jpg
```

### 🔧 Requirements

- `curl` - HTTP requests
- `grep` - Pattern extraction
- `jq` - JSON parsing (for Brave search)
- `file` - File type detection

### 📄 License

MIT

---

<a name="中文"></a>
## 中文

为 AI Agent 提供的完整图片搜索与下载解决方案 —— 为文章、Dashboard、内容创作获取高质量配图。

**🚀 无需浏览器** —— 所有操作通过命令行在后台执行。

### ✨ 特性

- **三种获取方式**：新闻网站提取、Brave 图片搜索、AI 生图
- **11+ 个可靠来源**：Reuters、TechCrunch、Bloomberg、BBC、NBC News 等
- **高清参数优化**：每个来源的最佳下载参数
- **纯 CLI 工作流**：无需浏览器，完全后台运行
- **完整故障排除**：常见问题及解决方案

### 🎯 适用场景

| 场景 | 推荐方法 |
|------|----------|
| 文章配图 | 新闻网站提取 / AI 生图 |
| 新闻缩略图 | 新闻网站提取 |
| Dashboard 展示 | Brave 图片搜索 |
| 概念/创意图 | AI 生图 |

### 🚀 快速开始

#### 方法一：从新闻网站提取（无需浏览器）

```bash
# 从页面 HTML 提取图片 URL
IMG_URL=$(curl -sL "https://www.reuters.com/article/..." | \
  grep -oE 'https://www\.reuters\.com/resizer/v2/[^"]+\.jpg' | head -1)

# 用高清参数下载
curl -sL -o photo.jpg "${IMG_URL}?width=3000&quality=100"

# 验证
file photo.jpg
```

#### 方法二：Brave 图片搜索（无需浏览器）

```bash
export BRAVE_API_KEY="你的密钥"

# 一行命令搜索并下载
IMG_URL=$(curl -s "https://api.search.brave.com/res/v1/images/search?q=SpaceX%20Starship%202025&count=1" \
  -H "X-Subscription-Token: $BRAVE_API_KEY" | jq -r '.results[0].properties.url')
curl -sL -o spacex.jpg "$IMG_URL"
```

#### 方法三：AI 生图（无需浏览器）

```bash
# Pollinations - 完全免费，无需 API Key
curl -sL -o cover.jpg "https://image.pollinations.ai/prompt/futuristic%20AI%20concept%20minimalist%20tech%20style?width=1920&height=1080&nologo=true"
```

### 📊 支持的新闻来源

#### ✅ 可直接下载

| 来源 | 类别 | Grep 正则 |
|------|------|-----------|
| Reuters | 政治/国际 | `reuters\.com/resizer/v2/[^"]+\.jpg` |
| TechCrunch | 科技/AI | `techcrunch\.com/wp-content/uploads/[^"]+\.jpg` |
| Bloomberg | 商业 | `assets\.bwbx\.io/images/[^"]+\.(jpg\|webp)` |
| BBC | 国际 | `ichef\.bbci\.co\.uk/news/[0-9]+/[^"]+\.jpg` |
| France24 | 国际 | `s\.france24\.com/media/display/[^"]+\.jpg` |
| Spaceflight Now | 航天 | `spaceflightnow\.com/wp-content/uploads/[^"]+\.jpg` |
| 澎湃 | 中文 | `imagepphcloud\.thepaper\.cn/pph/image/[^"]+\.jpg` |

#### ⚠️ 需手动保存或用其他方法

| 来源 | 问题 | 解决方案 |
|------|------|----------|
| Guardian | URL 签名 | 用 Brave 搜索 |
| The Verge | CDN 格式复杂 | 用 Brave 搜索 |
| CNN | JS 渲染 | 用 Brave 搜索 |
| AP News | 参数无效 | 手动保存 |

### 📁 文件结构

```
smart-image-finder/
├── SKILL.md          # AI Agent 使用指南（主文件）
├── README.md         # 本文档
└── scripts/
    ├── download.sh   # 批量下载脚本
    └── verify.sh     # 图片验证脚本
```

### 💡 最佳实践

#### 搜索技巧

```bash
# ❌ 太泛
"technology meeting"

# ✅ 加年份和具体事件
"Keir Starmer Xi Jinping Beijing January 2025"

# ✅ 限定来源
"site:reuters.com Trump tariff announcement"
```

#### 图片验证

```bash
# 确认是图片不是 HTML
file downloaded.jpg
# 应输出：JPEG image data, ...

# 检查尺寸（需要 ImageMagick）
identify -format '%wx%h' downloaded.jpg
```

### 🔧 环境要求

- `curl` - HTTP 请求
- `grep` - 正则提取
- `jq` - JSON 解析（Brave 搜索用）
- `file` - 文件类型检测

### 📄 License

MIT

---

## 🤝 Contributing / 贡献

Issues and PRs welcome / 欢迎提交 Issue 和 PR：
- Add new verified image sources / 新增可靠图片来源
- Update outdated CDN formats / 更新失效的 CDN 格式
- Improve extraction patterns / 改进提取模式
