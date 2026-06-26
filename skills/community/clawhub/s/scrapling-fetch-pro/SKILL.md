---
name: scrapling-fetch-pro
version: 1.2.0
description: 专业网页抓取工具，完整支持微信公众号文章爬取、自动模式检测、噪音清理。适合抓取博客、新闻、公告及各类有反爬保护的网站。
license: MIT
keywords:
  - 网页抓取
  - 爬虫
  - web scraping
  - 反爬绕过
  - markdown
  - scrapling
  - 微信公众号
  - 公众号文章
---

# Scrapling Fetch Pro

专业版网页抓取工具，**完整支持微信公众号文章爬取**，智能模式检测，噪音清理。

## 主要功能

### 🌐 网页内容抓取
- **智能正文提取**：自动识别并提取网页正文内容，无需手动指定选择器
- **Markdown 输出**：将 HTML 自动转换为干净的 Markdown 格式
- **字符数控制**：支持自定义最大输出字符数（默认 30000）

### 🔓 反爬绕过
- **Cloudflare Turnstile**：自动绕过 Cloudflare 反爬验证
- **浏览器指纹伪装**：隐身模式下模拟真实浏览器，避免被检测

### 📱 微信公众号支持 ⭐
- **完整爬取**：支持微信公众号文章完整内容抓取
- **噪音清理**：自动移除底部广告、工具栏等无用内容
- **标题提取**：支持微信公众号专用标题选择器

### 🎯 模式选择
- **basic 模式**：快速 HTTP 抓取，适合静态页面
- **stealth 模式**：隐身浏览器抓取，适合有反爬保护的网站
- **auto 模式**：智能自动检测，根据 URL 自动选择最佳模式 ⭐

## 快速开始

```bash
# 自动模式（推荐）
python3 scripts/scrapling_fetch.py https://example.com/article --mode auto

# 微信公众号文章（自动识别）
python3 scripts/scrapling_fetch.py https://mp.weixin.qq.com/s/xxx

# 指定字符数
python3 scripts/scrapling_fetch.py https://example.com/article 50000

# 强制 stealth 模式
python3 scripts/scrapling_fetch.py https://protected-site.com --mode stealth

# JSON 输出
python3 scripts/scrapling_fetch.py https://example.com --json
```

## 正文选择器（16个）

按优先级自动尝试：

1. `#js_content` - 微信公众号正文 ⭐
2. `.rich_media_content` - 微信公众号备选 ⭐
3. `article` - HTML5 article 元素
4. `main` - HTML5 main 主元素
5. `.post-content` - 博客常见内容区域
6. `.article-content` - 新闻常见内容区域
7. `.entry-content` - WordPress 常见
8. `.post-body` - 文章正文
9. `.content-body` - 内容正文 ⭐
10. `[class*='body']` - 包含 "body" 的类名
11. `[class*='content']` - 包含 "content" 的类名
12. `[class*='article']` - 包含 "article" 的类名 ⭐
13. `#content` - content ID
14. `#main` - main ID
15. `.content` - content 类 ⭐
16. `body` - 最后回退

## 微信公众号噪音清理 ⭐

自动移除以下内容：
- 底部广告区域
- 工具栏（分享、点赞等）
- 预览相关内容
- 推荐阅读
- 二维码关注提示

## 依赖

| 包名 | 版本 | 用途 |
|------|------|------|
| scrapling | 0.4.2 | 爬虫核心框架 |
| html2text | 2025.4.15 | HTML 转 Markdown |
| playwright | 1.58.0 | 浏览器自动化 |
| patchright | 1.58.2 | Playwright 补丁 |
| beautifulsoup4 | 4.12.3 | HTML 解析/噪音清理 ⭐ |
| lxml | 6.0.2 | XML/HTML 解析器 |

## 使用场景

- ✅ 抓取博客文章
- ✅ 抓取新闻页面
- ✅ 抓取公告文档
- ✅ **微信公众号文章（完整支持）** ⭐
- ✅ 绕过各类反爬保护
- ✅ 自动检测最佳抓取模式

## 对比基础版

| 特性 | 基础版 | 专业版 |
|------|--------|--------|
| 抓取模式 | basic / stealth | basic / stealth / **auto** |
| 选择器数量 | 11 个 | **16 个** |
| 微信公众号 | ⚠️ 有限支持 | ✅ **完整支持** |
| 噪音清理 | ❌ | ✅ **微信专用清理** |
| 自动检测 | ❌ | ✅ **智能模式选择** |

## 示例输出

```
# 文章标题

正文内容...

[已自动移除底部广告和工具栏]
```

---

**版本**: 1.2.0  
**作者**: OpenClaw  
**许可证**: MIT (需保留版权声明)

## 许可证

MIT License

Copyright (c) 2026 OpenClaw

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
