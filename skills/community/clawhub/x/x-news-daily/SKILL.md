---
name: x-news-daily
description: Fetch top 10 trending news from X.com for any keyword, generate full-screen Canvas poster with Chinese summaries and send to user. Supports custom keywords. Triggers: (1) User requests X news briefing (2) Daily scheduled task (3) Manual trigger. Default keyword: OpenClaw. Auto-translates news titles to Chinese and adds summaries.
description_zh: 抓取 X.com 上指定关键词的热门新闻 Top 10，使用 Canvas 生成全屏精美海报并发送给用户。支持自定义关键词，默认关键词为 OpenClaw。会自动将新闻标题翻译成中文并添加摘要。
---

# X News Daily (X 新闻每日简报)

## English

Fetch top 10 trending news from X.com for any keyword, generate a beautiful full-screen Canvas poster with Chinese summaries, and send to user.

### Features
- **Custom Keywords**: Support any keyword search (e.g., "NBA", "上海F1", "AI")
- **Auto Translation**: Translate English titles to Chinese automatically
- **Smart Summaries**: Add 1-2 sentence summary for each news item
- **Beautiful Design**: Full-screen Canvas poster with ClawHub-inspired color scheme
- **Multi-Platform**: Send as file to any IM (QQ, Telegram, Discord, WeChat)

### Triggers
- User says "X新闻简报", "X News", "Daily Brief"
- User specifies keyword like "X新闻简报 NBA", "X News AI"
- Scheduled cron task

### Steps
1. Get keyword from user or use default "OpenClaw"
2. Visit X.com search results page (f=top for trending)
3. Extract top 10 news with titles, summaries, and engagement stats
4. Translate titles to Chinese
5. Generate full-screen HTML poster
6. Save HTML to file named with current date (e.g., "2026-03-14.html")
7. Open HTML in Chrome using file:// protocol (NOT http), fullscreen kiosk mode
8. Use macOS screencapture command to take screenshot
9. If page scrolls, capture full page or scroll and capture multiple parts
10. Send screenshot to user using appropriate tag (QQ: `<qqimg>`, Telegram: image, etc.)

### HTML Poster Design (instead of Canvas)
- Use full-screen HTML template for better rendering
- Background: Light gray gradient (#f8f9fa → #e9ecef)
- Card: White (#ffffff) with subtle shadow
- Accent color: Red (#e63946) - matching OpenClaw theme
- Headlines: 28px bold, dark black (#212529) for readability
- Summaries: 20px gray (#6c757d)
- Bottom: Skill URL + Powered by OpenClaw

### Screenshot Method
- **Option 1: Headless Chrome with print-to-pdf (Recommended)**
  ```bash
  chrome --headless --disable-gpu --print-to-pdf=output.pdf --virtual-time-budget=10000 "file:///path/to/html"
  ```
- **Option 2: Headless Chrome with large viewport**
  ```bash
  chrome --headless --disable-gpu --screenshot=output.png --window-size=1600,2400 "file:///path/to/html"
  ```
- **Option 3: Chrome kiosk mode with screencapture**
  - Open HTML in Chrome using file:// protocol (NOT http)
  - Use Chrome kiosk mode (--kiosk flag) for fullscreen
  - Use macOS screencapture command for screenshot
  - If page scrolls, capture full page or scroll and capture multiple parts
- **Important**: Headless Chrome default screenshot only captures viewport. Use --print-to-pdf or large --window-size for full page

### Notes
- Must return exactly 10 news items
- Always translate to Chinese
- Add 1-2 sentence summary for each item
- Send as file, not image link
- Add skill URL at bottom: https://clawhub.ai/skill/x-news-daily

---

## 中文

抓取 X.com 上指定关键词的热门新闻 Top 10，翻译成中文，生成全屏精美 Canvas 海报并发送给用户。

### 功能
- **自定义关键词**：支持任意关键词搜索（如 "NBA"、"上海F1"、"AI"）
- **自动翻译**：自动将英文标题翻译成中文
- **智能摘要**：每条新闻添加 1-2 句话的摘要
- **精美设计**：全屏 Canvas 海报，参考 ClawHub 配色方案
- **多平台支持**：作为文件发送到任意 IM（QQ、Telegram、Discord、微信）

### 触发方式
- 用户说 "X新闻简报"、"OpenClaw 新闻"、"每日简报"
- 用户指定关键词如 "X新闻简报 NBA"、"X新闻简报 AI"
- 定时任务触发

### 执行步骤
1. 获取用户提供的关键词，或使用默认关键词 "OpenClaw"
2. 访问 X.com 搜索结果页面（f=top 获取热门）
3. 提取 Top 10 新闻标题、摘要和互动数据
4. 将标题翻译成中文
5. 生成全屏 HTML 海报
6. 将 HTML 保存为当天日期的文件（如 "2026-03-14.html"）
7. 用 file:// 协议（不是 http）在 Chrome 中打开 HTML，全屏 kiosk 模式
8. 使用 macOS screencapture 命令截图
9. 如果页面需要滚动，截取全页或滚动后截取多部分
10. 使用对应标签发送截图给用户（QQ 用 `<qqimg>`、Telegram 直接发图片等）

### HTML 海报设计（替代 Canvas）
- 使用全屏 HTML 模板以获得更好的渲染效果
- 背景：浅灰渐变 (#f8f9fa → #e9ecef)
- 卡片：纯白 (#ffffff) + 细微阴影
- 主题色：红色 (#e63946) - 呼应 OpenClaw 主题
- 标题：28px 加粗，深黑色 (#212529)，高对比度
- 摘要：20px，灰色 (#6c757d)
- 底部：Skill 网址 + Powered by OpenClaw

### 截图方法
- **方式 1：Headless Chrome 打印 PDF（推荐）**
  ```bash
  chrome --headless --disable-gpu --print-to-pdf=output.pdf --virtual-time-budget=10000 "file:///path/to/html"
  ```
- **方式 2：Headless Chrome 大视口截图**
  ```bash
  chrome --headless --disable-gpu --screenshot=output.png --window-size=1600,2400 "file:///path/to/html"
  ```
- **方式 3：Chrome kiosk 模式 + screencapture**
  - 用 file:// 协议（不是 http）在 Chrome 中打开 HTML 文件
  - 使用 Chrome kiosk 模式（--kiosk 参数）全屏显示
  - 使用 macOS screencapture 命令截图
  - 如果页面需要滚动，截取全页或滚动后截取多部分
- **注意**：Headless Chrome 默认只截取视口范围。使用 --print-to-pdf 或大 --window-size 来截取完整页面

### 注意事项
- 必须返回恰好 10 条新闻
- 必须翻译成中文
- 每条新闻添加 1-2 句话的摘要
- 发送文件而不是图片链接
- 图片底部添加 skill 网址：https://clawhub.ai/skill/x-news-daily
