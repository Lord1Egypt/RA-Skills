---
name: scrapling-fetch-basic
version: 1.0.0
description: 基础网页抓取工具，支持绕过反爬系统、自动定位正文区域、HTML 转 Markdown。适合抓取博客、新闻、公告等静态页面。
keywords:
  - 网页抓取
  - 爬虫
  - web scraping
  - 反爬绕过
  - markdown
  - scrapling
---

# Scrapling Fetch Basic

基础版网页抓取工具，快速高效，适合大多数场景。

## 主要功能

### 🌐 网页内容抓取
- **智能正文提取**：自动识别并提取网页正文内容，无需手动指定选择器
- **Markdown 输出**：将 HTML 自动转换为干净的 Markdown 格式
- **字符数控制**：支持自定义最大输出字符数（默认 30000）

### 🔓 反爬绕过
- **Cloudflare Turnstile**：stealth 模式可绕过 Cloudflare 反爬验证
- **浏览器指纹伪装**：隐身模式下模拟真实浏览器

### 🎯 模式选择
- **basic 模式**：快速 HTTP 抓取，适合静态页面（默认）
- **stealth 模式**：隐身浏览器抓取，适合有反爬保护的网站

## 快速开始

```bash
# 基础抓取
python3 scripts/scrapling_fetch.py https://example.com/article

# 指定字符数
python3 scripts/scrapling_fetch.py https://example.com/article 50000

# 绕过反爬保护
python3 scripts/scrapling_fetch.py https://protected-site.com --mode stealth

# JSON 输出
python3 scripts/scrapling_fetch.py https://example.com --json
```

## 正文选择器（11个）

按优先级自动尝试：

1. `article` - HTML5 article 元素
2. `main` - HTML5 main 主元素
3. `.post-content` - 博客常见内容区域
4. `.article-content` - 新闻常见内容区域
5. `.entry-content` - WordPress 常见
6. `.post-body` - 文章正文
7. `[class*='body']` - 包含 "body" 的类名
8. `[class*='content']` - 包含 "content" 的类名
9. `#content` - content ID
10. `#main` - main ID
11. `body` - 最后回退

## 依赖

| 包名 | 用途 |
|------|------|
| scrapling | 爬虫核心框架 |
| html2text | HTML 转 Markdown |
| playwright | 浏览器自动化（stealth 模式） |

## 使用场景

- ✅ 抓取博客文章
- ✅ 抓取新闻页面
- ✅ 抓取公告文档
- ✅ 绕过基础反爬保护
- ⚠️ 微信公众号文章（支持有限，建议使用专业版）

## 对比专业版

| 特性 | 基础版 | 专业版 |
|------|--------|--------|
| 抓取模式 | basic / stealth | basic / stealth / **auto** |
| 选择器数量 | 11 个 | **16 个** |
| 微信公众号 | ⚠️ 有限支持 | ✅ **完整支持** |
| 噪音清理 | ❌ | ✅ **微信专用清理** |
| 自动检测 | ❌ | ✅ **智能模式选择** |

---

**版本**: 1.0.0  
**作者**: OpenClaw
