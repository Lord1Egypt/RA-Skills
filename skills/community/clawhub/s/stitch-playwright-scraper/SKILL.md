---
name: playwright-scraper
version: 2.0.0
description: 使用 Playwright + Stealth 插件绕过反爬机制抓取页面。
---

# Playwright Stealth Scraper 🕷️

当 `web_fetch` 工具拿不到目标页面内容时（403、JS渲染、反爬），用这个技能。

## 前置条件

需要本地安装了 Playwright 和 Chromium。

```bash
# 在技能目录下安装
cd ~/.openclaw/workspace/skills/playwright-scraper
npm install playwright puppeteer-extra-plugin-stealth
npx playwright install chromium
```

**注意**：这会下载约 300MB 的 Chromium 二进制文件。

## 什么时候用这个

| 场景 | 用什么 |
|------|--------|
| 普通网页、API 返回 | `web_fetch`（内置，轻量） |
| 被 Cloudflare 等反爬拦截 | **playwright-scraper** |
| 页面需要 JS 渲染才能显示内容 | **playwright-scraper** |
| 需要登录后抓取 | **playwright-scraper** + 手动处理 cookie |

## 使用方式

### 方式一：写一个独立脚本（推荐）

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  await page.goto('目标URL', { waitUntil: 'networkidle' });
  const content = await page.content();
  // 提取你需要的内容
  console.log(content);
  await browser.close();
})();
```

### 方式二：直接用 OpenClaw 的 browser 工具

```bash
# 启动浏览器
browser action=start profile=openclaw
# 打开页面
browser action=open url=目标URL
# 获取快照
browser action=snapshot targetId=XXX
```

内置 browser 工具通常够用，playwright-scraper 主要应对特殊反爬场景。

## 注意

- 不要高频爬取，尊重 robots.txt
- 如果目标网站有登录墙，不要自动填凭据，请示老板
- 爬下来的数据存到工作区对应目录，不要丢在 /tmp
