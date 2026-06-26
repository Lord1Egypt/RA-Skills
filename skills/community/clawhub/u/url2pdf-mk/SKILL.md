---
name: url2pdf-mk
description: |
  EN: Webpage to PDF + Markdown converter. Converts any URL (especially WeChat articles) into
  offline-readable PDF and Markdown files with complete images, preserving original layout and styles.
  Auto-creates date-named folders on desktop, filenames use publish date + title.

  ⚠️ Security Note: Browser mode (default) reuses your Chrome profile — it can access your cookies
  and logged-in sessions. Use --isolated for public content, or run in a VM/sandbox. CDP proxy
  opens a local port and writes temp state files (cdp-proxy-<user> in your temp directory).
  微信文章 / 网页抓取工具，将任意 URL 输出为含完整图片的 PDF 和 Markdown 文件。
  自动在桌面按当前日期创建目录，文件名使用文章发布日期 + 标题。
  当用户提到"网页转 PDF"、"保存微信文章"、"抓取网页内容"、"导出 PDF 和 Markdown"、
  "url2pdf"、"网页保存"、"url2pdf-mk"、"保存链接"、"离线阅读"、"网页存档"、"批量抓取"等时触发此技能。
---

# url2pdf-mk — Webpage to PDF & Markdown Converter

> One-click webpage to PDF + Markdown converter. Transforms WeChat articles and web pages into
> offline-readable documents with full images, original layout and styles preserved.

> 一键将网页（尤其是微信文章）转换为可离线阅读的 PDF 和 Markdown 文档，完整保留排版、图片、样式。

---

## 📋 概述 | Overview

**url2pdf-mk** is a professional webpage content scraping and conversion tool, designed specifically for WeChat public account articles and regular web pages. It can:

- ✅ Convert any webpage into **PDF** and **Markdown** dual-format output / 将任意网页转换为 PDF 和 Markdown 双格式输出
- ✅ Preserve complete images, layout and styles / 完整保留网页中的图片、排版、样式
- ✅ Support both single-page and batch scraping (via xlsx file) / 支持单篇抓取和批量抓取
- ✅ Auto-create date-named folders on desktop / 自动按日期在桌面创建归档目录
- ✅ Smart detection of WeChat article titles and publish dates / 智能识别微信文章标题和发布日期

---

## ⚙️ 工作机制 | How It Works

### 核心技术架构 | Core Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    url2pdf-mk Workflow                           │
│                        工作流程                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Input Sources / 输入源                                          │
│  ├── Single URL → scrape.py (Single Page)                       │
│  │   └── 单个 URL → 单篇抓取                                     │
│  ├── Multiple URLs → batch_scrape.py (Browser Batch)            │
│  │   └── 多个 URL → 批量浏览器版                                  │
│  └── xlsx file → Smart Routing (Browser/HTTP)                  │
│      └── xlsx 文件 → 智能路由                                    │
│                                                                 │
│  Scraping Engines / 抓取引擎                                      │
│  ├── Browser (CDP) ──→ Chrome DevTools Protocol                 │
│  │   ├── Launch Chrome/Chromium browser                          │
│  │   │   └── 启动浏览器                                           │
│  │   ├── Control browser via CDP protocol                        │
│  │   │   └── CDP 协议控制                                         │
│  │   ├── Render full page (including JavaScript)                │
│  │   │   └── 渲染完整页面                                         │
│  │   └── Extract DOM + screenshot to PDF                        │
│  │       └── 提取 DOM + 截图生成 PDF                               │
│  │                                                              │
│  └── HTTP (No Browser) ──→ requests library                      │
│      ├── Send HTTP requests to get HTML                         │
│      │   └── HTTP 请求获取 HTML                                   │
│      ├── Parse static HTML structure                            │
│      │   └── 解析静态 HTML                                        │
│      └── Markdown output only (no PDF)                          │
│          └── 仅输出 Markdown                                     │
│                                                                 │
│  Output Processing / 输出处理                                     │
│  ├── HTML → Markdown conversion (preserve image links)          │
│  │   └── HTML → Markdown 转换                                    │
│  ├── HTML → PDF generation (reportlab + full styles)            │
│  │   └── HTML → PDF 生成                                          │
│  └── Filename: {date}_{title}.{md/pdf}                          │
│      └── 文件命名：{发布日期}_{标题}                               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 工作流程详解 | Workflow Details

#### 1. Single Page Mode / 单篇抓取模式 (`scrape.py`)
```
URL → Launch browser → Load page → Extract content → Generate PDF + Markdown → Save to date folder
URL → 启动浏览器 → 加载页面 → 提取内容 → 生成 PDF + Markdown → 保存到日期目录
```

#### 2. Browser Batch Mode / 批量浏览器版 (`batch_scrape.py`)
```
xlsx file → Read URL list → Reuse browser instance → Scrape each → Batch output
xlsx 文件 → 读取 URL 列表 → 复用浏览器实例 → 逐个抓取 → 批量输出
```
- **Advantage / 优势**: Browser instance starts only once, high efficiency / 浏览器实例只启动一次，效率高
- **Prerequisite / 前提**: Chrome/Chromium installed / 系统已安装 Chrome/Chromium

#### 3. HTTP Batch Mode / 批量 HTTP 版 (`batch_http.py`)
```
xlsx file → Read URL list → Send HTTP requests → Parse HTML → Batch output Markdown
xlsx 文件 → 读取 URL 列表 → 发送 HTTP 请求 → 解析 HTML → 批量输出 Markdown
```
- **Advantage / 优势**: No browser needed, low resource usage / 无需浏览器，资源占用低
- **Limitation / 限制**: Cannot handle JavaScript-rendered content, no PDF output / 无法处理 JS 内容，无 PDF 输出

### 智能路由逻辑 | Smart Routing Logic

`main.py` serves as the unified entry point, automatically selecting the optimal approach based on input type:

| Input Type / 输入类型 | Chrome Available / Chrome 可用 | Chrome Unavailable / Chrome 不可用 |
|---------|------------|--------------|
| Single URL / 1 个 URL | Browser mode (PDF+MD) / 浏览器版 | HTTP mode (MD only) / HTTP 版 |
| Multiple URLs / ≥2 个 URL | Browser batch (PDF+MD) / 浏览器版批量 | HTTP batch (MD only) / HTTP 版批量 |
| xlsx file / xlsx 文件 | Browser batch (PDF+MD) / 浏览器版批量 | HTTP batch (MD only) / HTTP 版批量 |

### CDP (Chrome DevTools Protocol) / CDP 协议说明

CDP is Chrome's debugging protocol. This tool uses it to:

1. **Launch/Connect browser / 启动/连接浏览器**: Connect to existing browser or launch new instance / 支持连接已有浏览器或启动新实例
2. **Page control / 页面控制**: Navigate, wait for load, execute JavaScript / 导航、等待加载、执行 JavaScript
3. **Content extraction / 内容提取**: Get complete DOM structure and computed styles / 获取完整的 DOM 结构和计算样式
4. **PDF generation / PDF 生成**: Use browser's native PDF print function / 调用浏览器原生 PDF 打印功能

**Security measures / 安全措施**:
- CDP ports bound to `127.0.0.1` only, external network cannot access / CDP 端口仅绑定本机，外网无法访问
- WebSocket connections require Token verification / WebSocket 连接需要 Token 验证
- `--isolated` mode uses independent temporary Profile, no access to user data / `--isolated` 模式使用临时 Profile，不访问用户数据

---

## 🖥️ 适配环境 | Supported Environments

### 操作系统支持 | Operating System Support

| Operating System / 操作系统 | Status / 支持状态 | Note / 说明 |
|---------|---------|------|
| **Windows 10/11** | ✅ Full Support / 完全支持 | Chrome or Edge recommended / 推荐 Chrome 或 Edge |
| **macOS 10.15+** | ✅ Full Support / 完全支持 | Chrome, Chromium, Edge supported / 支持 Chrome、Chromium、Edge |
| **Linux** | ✅ Full Support / 完全支持 | Chrome or Chromium required / 需安装 Chrome 或 Chromium |
| **Windows 7/8** | ⚠️ Limited / 有限支持 | Upgrade recommended for best experience / 建议升级以获得最佳体验 |

### 浏览器支持 | Browser Support

| Browser / 浏览器 | Status / 支持状态 | Version / 版本要求 |
|--------|---------|---------|
| **Google Chrome** | ✅ Recommended / 推荐 | 80+ |
| **Microsoft Edge (Chromium)** | ✅ Supported / 支持 | 80+ |
| **Chromium** | ✅ Supported / 支持 | 80+ |
| **Others / 其他浏览器** | ❌ Not supported / 不支持 | Chromium-based only / 仅支持 Chromium 内核 |

### Python 环境要求 | Python Environment Requirements

| Component / 组件 | Version / 版本要求 | Purpose / 用途 |
|------|---------|------|
| **Python** | 3.7+ | Runtime environment / 运行时环境 |
| **pip** | Latest / 最新版 | Package manager / 包管理器 |

---

## 📦 基础组件依赖 | Dependencies

### Required Dependencies / 必需依赖 (must install before running)

```bash
pip install websockets openpyxl requests reportlab
```

| Package / 依赖包 | Version / 版本要求 | Purpose / 用途 |
|--------|---------|------|
| `websockets` | 10.0+ | CDP WebSocket communication / CDP WebSocket 通信 |
| `openpyxl` | 3.0+ | Read xlsx files (batch mode) / 读取 xlsx 文件（批量模式） |
| `requests` | 2.25+ | HTTP requests (HTTP mode) / HTTP 请求（HTTP 版抓取） |
| `reportlab` | 3.6+ | PDF document generation / PDF 文档生成 |

### Optional Dependencies / 可选依赖

| Package / 依赖包 | Purpose / 用途 | Note / 说明 |
|--------|------|------|
| `Pillow` | Image processing / 图片处理 | PDF image optimization (auto-installed) / PDF 图片优化（自动安装） |
| `beautifulsoup4` | HTML parsing / HTML 解析 | Enhanced content extraction (built-in) / 增强内容提取（已内置） |

### System Requirements / 系统组件要求

| Component / 组件 | Requirement / 说明 |
|------|------|
| **Chrome/Chromium/Edge** | Required for browser mode / 浏览器版抓取必需 |
| **Network / 网络连接** | Required to access target webpages / 访问目标网页必需 |
| **Disk space / 磁盘空间** | 100MB+ recommended / 建议预留 100MB+ |

### 快速环境检查 | Quick Environment Check

Run the following commands to check if the environment is ready:

```bash
# Check Python version
python3 --version  # Should show 3.7+

# 检查依赖是否已安装
python3 -c "import websockets, openpyxl, requests, reportlab; print('✅ All dependencies installed')"

# Check if Chrome is available
# Windows
where chrome
# macOS
which "Google Chrome"
# Linux
which google-chrome || which chromium-browser
```

---

## 🔒 安全说明（必读）| Security

| Mode / 模式 | Command / 命令 | Profile | Use Case / 适用场景 |
|------|------|---------|----------|
| **Isolated (Recommended) / 隔离（推荐）** | `main.py --isolated <URL>` | Temporary isolated Profile, no Cookie / 临时隔离 Profile，无 Cookie | Public content / 公开内容 |
| **Default / 默认** | `main.py <URL>` | Reuse Chrome real Profile / 复用 Chrome 真实 Profile | WeChat articles requiring login / 需登录态的微信文章 |

### 风险与缓解 | Risks & Mitigations

| Risk / 风险项 | Description / 说明 | Mitigation / 缓解措施 |
|--------|------|----------|
| Profile reuse / Profile 复用 | Can access Chrome cookies/login sessions / 可访问 Chrome Cookie/登录态 | ✅ Always use `--isolated` for public content / 公开内容一律用 `--isolated` |
| CDP remote debugging / CDP 远程调试 | Enables Chrome DevTools protocol / 开启 Chrome DevTools 协议 | Only listens on `127.0.0.1:9222~9232` (localhost) / 仅监听本机 |
| CDP Proxy | Creates local proxy daemon / 创建本地代理守护进程 | Only bound to `127.0.0.1`, external access blocked / 仅绑定本机；WS 需 Token 验证 |
| Browser launch / 浏览器启动 | May reuse existing browser window / 可能复用已有浏览器窗口 | `--isolated` always launches independent instance / 始终启动独立实例 |
| sys.path | Only adds skill directory, no external path access / 仅添加本技能目录 | ✅ Already securely isolated / 已安全隔离 |
| pip dependencies / pip 依赖 | No longer auto-install at runtime / 不再运行时自动安装 | ✅ Pre-installed + error prompt / 预装 + 报错提示 |

### 推荐规则 | Recommended Rules

> ⚠️ **Default mode reuses your real Chrome profile — it can read cookies and logged-in sessions. Always prefer `--isolated` for public content to avoid exposing your browser session.**

- **Public content / 公开内容** → **`--isolated`** (No login required, uses temporary isolated profile / 无需登录，使用临时隔离 Profile)
- **Content requiring login / 需登录的内容** → Default mode (Ensure browser is logged in / 确保浏览器已登录目标网站；或在专用/沙箱环境中运行)
- **Safest option / 最安全方案** → HTTP batch mode (`batch_http.py`) — no browser, no profile access / 无需浏览器，不访问 Profile

### ⚠️ 重要安全警告 | Important Security Warnings

> ⭐ **For maximum safety, prefer `--isolated` mode or HTTP batch mode (`batch_http.py`) so the tool never touches your real browser profile or cookies.**

1. **Cookie and Login Access / Cookie 和登录态访问**: Default mode connects to your existing Chrome instance, allowing access to browser cookies and logged-in sessions. **Only use default mode when you trust the code and need to scrape pages requiring login.**

2. **CDP Proxy — Local Port & State Files / CDP 代理 — 本地端口与状态文件**: The CDP proxy daemon opens a local listening port (default 9223) and writes PID/state files to your temp directory (named `cdp-proxy-<username>`). After each task, **manually check and delete these temp files** if auto-cleanup failed.

3. **Temporary Files / 临时文件**: Scripts create temporary files (xlsx, proxy state, pid files) in system temp directory. These are auto-cleaned after task completion. For extra security, manually check and delete relevant files in temp directory after tasks.

4. **CDP Port Security / CDP 端口安全**: CDP debugging ports are bound to `127.0.0.1` only, external network cannot access. WebSocket connections require Token verification.

5. **Don't Run as Root / 不要以 root 运行**: Run with normal user privileges recommended / 建议以普通用户权限运行此工具。

6. **VM / Sandbox / 虚拟机 / 沙箱**: If you must run browser mode with your real profile, do so inside a VM or disposable environment to limit exposure.

7. **Extra Assurance / 如需额外保证**: Modify `browser_launcher.py` to force isolated profile only.

---

## 用法 | Usage

### 统一入口（推荐）| Unified Entry (Recommended)

```bash
# Single page / 单篇
python3 scripts/main.py "https://mp.weixin.qq.com/s?__biz=..."

# Batch (multiple URLs) / 批量（多个 URL）
python3 scripts/main.py "https://url1" "https://url2" "https://url3"

# Batch (xlsx file) / 批量（xlsx 文件）
python3 scripts/main.py /path/to/urls.xlsx

# Isolated mode (no login) / 隔离模式（不使用登录态）
python3 scripts/main.py --isolated "https://..."
python3 scripts/main.py --isolated /path/to/urls.xlsx
```

### Smart Routing / 智能路由

| Input / 输入 | Processing / 处理方式 |
|------|----------|
| Single URL / 1 个 URL | Single-page full scraping (PDF + Markdown) / 单篇完整抓取 |
| Multiple URLs / ≥2 个 URL | Batch scraping: Browser mode if Chrome available, otherwise HTTP mode / Chrome 可用 → 浏览器版，否则 → HTTP 版 |
| xlsx file / xlsx 文件 | Auto-routed based on URL count / 根据 URL 数量自动路由 |

### xlsx 格式 | xlsx Format

| Column / 列 | Content / 内容 |
|----|------|
| B (2nd) / B（第2列） | Article title / 文章标题 |
| C (3rd) / C（第3列） | Publish date / 发布日期 |
| F (6th) / F（第6列） | Article URL / 文章 URL |

### 输出 | Output

```
~/Desktop/{current date}/
├── 2025-04-03_article-title.md
└── 2025-04-03_article-title.pdf
```

---

## 脚本说明 | Scripts

| Script / 脚本 | Purpose / 用途 |
|------|------|
| `main.py` | Unified entry, smart routing / 统一入口，智能路由 |
| `scrape.py` | Single-page scraping, PDF + Markdown / 单篇抓取，PDF + Markdown |
| `batch_scrape.py` | Browser batch (requires Chrome) / 批量浏览器版（需 Chrome） |
| `batch_http.py` | HTTP batch (no browser, MD only) / 批量 HTTP 版（无浏览器，仅 Markdown） |

---

## 已知限制 | Known Limitations

- **Video/Audio / 视频/音频**: PDF keeps cover, Markdown keeps links / PDF 保留封面，Markdown 保留链接
- **WeChat Mini Programs / 微信小程序**: Static content only / 仅提取静态内容
- **Anti-crawl limits / 反爬限制**: HTTP mode may fail, switch to browser mode / HTTP 版可能失败，改用浏览器版

---

## 更新日志 | Changelog

### v1.1.1（2026-04-14）— 安全描述增强

- **SKILL.md description metadata 新增安全警告**：
  - 明确告知浏览器默认模式会复用 Chrome Profile，可访问 Cookie/登录态
  - 提示 CDP 代理会打开本地端口并写入临时状态文件
  - 推荐公开内容优先使用 `--isolated`
- **推荐规则强化**：
  - 新增最安全方案：HTTP 批量模式（`batch_http.py`），无需浏览器，不访问 Profile
  - 所有推荐规则前加 ⭐ 标识
- **⚠️ 安全警告章节扩充**：
  - 新增 CDP 代理本地端口与 `cdp-proxy-<username>` 状态文件提示
  - 新增 VM / 沙箱运行建议
  - 临时文件手动清理建议

### v1.1.0（2026-04-14）— English-first bilingual formatting

- 🌐 **全面中英双语调整 / English-first throughout**:
  - All section titles adjusted to "English | 中文" format
  - All tables adjusted to English first, Chinese second
  - All descriptions adjusted to English first, Chinese second
  - Architecture diagram converted to bilingual layout
  - Security warnings, usage instructions, and known limitations all bilingual
  - description metadata: EN description placed before Chinese

### v1.0.9（2026-04-14）— 文档增强

**SKILL.md 文档大幅更新：**

- 📋 **新增「概述」章节 / Overview section**: 简要说明工具核心功能定位
- ⚙️ **新增「工作机制」/ How It Works 章节**:
  - 核心技术架构流程图
  - 工作流程详解（单篇抓取、批量浏览器版、批量 HTTP 版）
  - 智能路由逻辑表格
  - CDP 协议技术说明
- 🖥️ **新增「适配环境」/ Supported Environments 章节**:
  - 操作系统支持表（Windows/macOS/Linux）
  - 浏览器支持表（Chrome/Edge/Chromium 版本要求）
  - Python 环境要求
- 📦 **新增「基础组件依赖」/ Dependencies 章节**:
  - 必需依赖包及版本要求（websockets、openpyxl、requests、reportlab）
  - 可选依赖说明
  - 系统组件要求
  - 快速环境检查命令
  - 便于 SkillHub 平台海外用户理解工具功能

**文档结构优化：**

- 将「环境」章节整合到「基础组件依赖」中，避免重复
- 统一表格格式，提升可读性

### v1.0.8（2026-04-13）— 安全增强

- SKILL.md：新增**⚠️ 重要安全警告**章节，包含：
  - Cookie 和登录态访问警告
  - 临时文件安全说明
  - CDP 端口安全说明
  - 不要以 root 运行的建议
  - VM/disposable 环境运行建议
- main.py：临时文件清理添加日志输出，清理成功/失败都会提示

### v1.0.7（2026-04-13）— 文件名修复

- 批量抓取时，文件名（PDF + Markdown）现在使用**从网页提取的真实标题和日期**
- 修复了之前使用 xlsx 默认标题（如"文章1"）的问题
- `batch_scrape.py`：在提取网页内容后，用网页获取的真实标题覆盖 xlsx 中的标题

### v1.0.5（2026-04-13）— 安全修复

- 移除 `batch_http.py` 中的硬编码 xlsx 默认路径
- 所有脚本：pip 依赖从运行时 auto-install 改为**预装检查 + 报错提示**（安全加固）
- `batch_http.py` 新增系统目录路径安全校验
- SKILL.md：调整安全说明，`--isolated` 标记为公开内容首选

### v1.0.4（2026-04-13）

- 新增 `--isolated` 隔离模式参数
- 移除硬编码路径，必须提供 xlsx 路径
- 新增 `--output` 可指定输出目录
- 强化安全文档

### v1.0.1（2026-04-12）

- 新增批量抓取脚本
- 修复多项 bug
