# 📖 WeChat Article Fetch

> Extract title, body text, and URL from WeChat Official Account articles (mp.weixin.qq.com)

*[English](#english) / [中文](#中文)*

---

## ✨ Features | 功能亮点

| Feature | Description |
|---------|-------------|
| 🎯 **Title Extraction** | Extract article title from rendered page |
| 📝 **Body Text** | Extract clean text from `#js_content` |
| 🔗 **URL Resolution** | Follows redirects, returns canonical URL |
| 🌐 **Full Rendering** | Playwright/Chromium for JS-heavy pages |
| 🔒 **Privacy First** | 100% local, no upload, no external APIs |
| ⚡ **Easy Integration** | Simple JSON API, scriptable |
| 📋 **Multiple Output Formats** | Support JSON, Markdown formats |
| 🎛️ **Command Line Options** | Flexible configuration via CLI |
| 🔧 **Browser Instance Reuse** | Improved performance and resource usage |

---

## 🚀 Quick Start | 快速开始

### Installation | 安装

```bash
git clone https://github.com/write31bug/wechat-mp-fetch.git
cd wechat-mp-fetch
npm install
npx playwright install chromium
```

### Usage | 使用

#### Basic Usage | 基本使用

```bash
# 使用位置参数
node scripts/wx-article-fetch.js "https://mp.weixin.qq.com/s/xxxxx"

# 或使用命令行选项
node scripts/wx-article-fetch.js --url "https://mp.weixin.qq.com/s/xxxxx"

# 输出
{
  "success": true,
  "title": "文章标题",
  "content": "正文内容...",
  "url": "https://mp.weixin.qq.com/s/xxxxx"
}
```

#### Output Formats | 输出格式

```bash
# JSON格式（默认）
node scripts/wx-article-fetch.js --url "https://mp.weixin.qq.com/s/xxxxx" --format json

# Markdown格式
node scripts/wx-article-fetch.js --url "https://mp.weixin.qq.com/s/xxxxx" --format markdown
```

#### Other Options | 其他选项

```bash
# 设置超时时间（毫秒）
node scripts/wx-article-fetch.js --url "https://mp.weixin.qq.com/s/xxxxx" --timeout 60000

# 启用调试模式
node scripts/wx-article-fetch.js --url "https://mp.weixin.qq.com/s/xxxxx" --debug
```

### Command Line Options | 命令行选项

| Option | Description | Default |
|--------|-------------|---------|
| `-u, --url <url>` | WeChat article URL | Required |
| `-f, --format <format>` | Output format (json, markdown) | json |
| `-t, --timeout <ms>` | Timeout in milliseconds | 30000 |
| `-d, --debug` | Enable debug mode | false |
| `-h, --help` | Show help information | - |
| `-V, --version` | Show version information | - |

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

## ⚠️ Limitations | 已知限制

| Issue | Description |
|-------|-------------|
| 🔐 **Login Required** | Some articles require WeChat login |
| 💰 **Paid Content** | Paywalled articles cannot be fetched |
| 🔒 **Private Accounts** | Private official accounts inaccessible |
| 🖼️ **Images** | Text only; images keep original URLs |

---

## 🛡️ Security & Privacy | 安全与隐私

- **100% Local** — All operations in local browser, no external server
- **No Credentials** — No WeChat login required
- **No Data Storage** — Content lives only in session
- **No Tracking** — No analytics, no telemetry

---

## 📁 Project Structure | 项目结构

```
wechat-mp-fetch/
├── scripts/
│   ├── wx-article-fetch.js      # Main entry
│   ├── browser.js               # Browser management
│   ├── extractor.js             # Content extraction
│   ├── validator.js             # URL validation
│   └── formatter.js             # Output formatting
├── .gitignore
├── LICENSE
├── README.md
├── SKILL.md
├── OPTIMIZATION.md              # Optimization documentation
├── package-lock.json
└── package.json
```

---

## 🔗 Related Links | 相关链接

- **GitHub**: https://github.com/write31bug/wechat-mp-fetch
- **ClawHub**: https://clawhub.ai/skills/wechat-mp-fetch
- **npm**: https://www.npmjs.com/package/wechat-mp-fetch

---

## ⚖️ License | 许可证

MIT License
