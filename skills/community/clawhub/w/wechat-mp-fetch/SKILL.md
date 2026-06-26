---
name: wechat-article-fetch
description: WeChat Official Account article fetcher — extracts title, body text, and final URL from mp.weixin.qq.com links via Playwright. 微信公众号文章抓取工具，提取标题、正文、原始URL，支持重定向处理。
metadata:
  claudibot:
    emoji: "📖"
    category: "content-processing"
  tags: ["wechat", "weixin", "mp.weixin", "公众号", "article", "content", "笔记"]
  requires:
    env: []
  files:
    - "scripts/*"
  homepage: "https://github.com/write31bug/wechat-mp-fetch"
---

# 📖 WeChat Article Fetch | 微信公众号文章抓取

> Extract article title, body text, and original URL from WeChat Official Account links (mp.weixin.qq.com)

---

## ✨ Features | 功能

- 🎯 **Title Extraction** — Extracts article title from rendered page
- 📝 **Body Text** — Extracts clean text content from `#js_content`
- 🔗 **URL Resolution** — Handles redirects, returns final canonical URL
- 🌐 **Full Rendering** — Uses Playwright/Chromium for JS-heavy pages
- 🔒 **Privacy First** — 100% local, no data uploaded anywhere

---

## 🚀 Quick Start

### Installation

```bash
cd <skill-path>
npm install
npx playwright install chromium
```

### Usage

```bash
node scripts/wx-article-fetch.js "https://mp.weixin.qq.com/s/xxxxx"
```

### Output

```json
{
  "success": true,
  "title": "文章标题",
  "content": "正文内容...",
  "url": "https://mp.weixin.qq.com/s/xxxxx"
}
```

---

## 💡 Usage Scenarios | 使用场景

| Scenario | Description | 场景 |
|----------|-------------|------|
| 📚 **Content Archival** | Save articles for offline reading | 文章离线保存 |
| 📝 **Note-taking** | Convert articles to notes | 文章转笔记 |
| 🔍 **Research** | Batch collect article content | 批量采集资料 |
| ✍️ **Writing Reference** | Extract key info for writing | 写作素材收集 |
| 🔄 **Content Repurposing** | Extract text for rewriting | 内容再创作 |

---

## ⚠️ Known Limitations | 已知限制

| Issue | Description |
|-------|-------------|
| 🔐 **Login Required** | Some articles require WeChat login |
| 💰 **Paid Content** | Paywalled articles cannot be fetched |
| 🔒 **Private Accounts** | Private official accounts inaccessible |
| 🖼️ **Images** | Currently extracts text only; images keep original URLs |

---

## 🔧 Technical Details | 技术细节

- **Rendering Engine**: Playwright + headless Chromium
- **Content Selector**: `#js_content` container
- **No External APIs**: All processing is 100% local
- **Browser Mode**: Headless, no UI, no state leakage

---

## 🛡️ Security & Privacy

- **100% Local** — All operations run in local browser, no external server
- **No Login Required** — No WeChat credentials needed
- **No Data Storage** — Content exists only in caller's session
- **No Tracking** — No analytics, no telemetry, no third-party deps

---

## 📁 Project Structure

```
wechat-mp-fetch/
├── _meta.json
├── SKILL.md
├── package.json
├── package-lock.json
└── scripts/
    └── wx-article-fetch.js    # Main script
```

---

## 🔗 Links

- **GitHub**: https://github.com/write31bug/wechat-mp-fetch
- **npm**: https://www.npmjs.com/package/wechat-mp-fetch
- **ClawHub**: https://clawhub.ai/skills/wechat-mp-fetch
