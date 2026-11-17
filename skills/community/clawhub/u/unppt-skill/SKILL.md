---
name: unppt
description: 把 PowerPoint 课件一条命令转换成网页/HTML：保留动画、页面切换、音视频，效果对齐 PowerPoint；直接输入 .pptx（老格式 .ppt 先在 PowerPoint 另存为 .pptx）；支持单文件 HTML、按需加载、iframe 嵌入、postMessage 控制翻页、批量转换、字体检查、Node/云函数/浏览器内调用。当用户要求"PPT 转网页、pptx 转 HTML、ppt 转换、课件在线播放、把 PPT 放到网站上、嵌入 PPT 播放器、用代码控制 PPT 翻页、检查 PPT 字体、批量转换 PPT"时使用本技能（convert PowerPoint pptx to web page HTML, embed and control slides playback）。
agent_created: true
---

# unppt：把 .pptx 转成网页

## 概述

unppt（npm 包 `@unppt/unppt`，要求 Node.js ≥ 20.12）把 PowerPoint 课件转码成网页：浏览器打开即可播放，动画、切换、音视频保留，效果对齐 PowerPoint。产物可本地双击打开、放静态服务器/CDN、嵌进任何网页或 App，并可用代码控制翻页。

**输入格式**：直接支持 .pptx（OOXML）。老的二进制格式 .ppt 不受支持——转码器会报错"这是老格式的 .ppt 文件（或加密的 pptx），暂不支持"；遇到 .ppt 时引导用户在 PowerPoint 里"另存为 .pptx"后再转码，或（Windows + PowerPoint 环境）用 COM 自动化批量另存。加密的 pptx 同样无法转码。

本技能基于 unppt 0.3.2。完整文档见 <https://github.com/spitmaster/unppt>。

## 环境准备

执行转码前先确认 Node ≥ 20.12（`node -v`），未安装 unppt 时全局安装一次：

```bash
npm install -g @unppt/unppt
```

代码调用（脚本、服务、云函数）用项目内安装：

```bash
npm install @unppt/unppt
```

## 第一步：选择产物形式

| 场景 | 形式（`--output`） | 说明 |
|---|---|---|
| 发给别人当附件、本地双击、小课件 | `single` | 一个自包含 HTML（`convert()` API 的默认） |
| 放网站上、页数多或文件大 | `paged` | 命令行默认。入口 HTML 只有几十 KB，每页数据按需加载 |
| 还要单独打开或嵌入某一页 | `pages` | `paged` + 每页一个 `page-001.html` |
| 只要原始数据调试 | `data` | 只输出 `deck.json`，没有播放器 |

所有形式都会写 `prop.json`；默认还输出整页图 `pic/{n}.jpg` 和缩略图 `thum/{n}.jpg`（`--no-images` 关闭）。

## 常见任务

### 1. 转换并播放

```bash
unppt 课件.pptx                        # 输出到 课件/ 目录，打开课件/index.html
unppt 课件.pptx -o site/demo           # 指定输出目录
unppt 课件.pptx -o out/index.html --output single   # 单文件 HTML
```

单页渲染失败不会导致整体失败：该页输出白页并在警告里记录。退出码：0 成功；1 转码错误（或 `check` 发现必须处理的问题）；2 用法错误。

**遇到 .ppt 文件**：转码器会明确报错（错误信息会提示"请用 PowerPoint 另存为 .pptx"）。正确流程：先在 PowerPoint 中打开 → 文件 → 另存为 → .pptx，再对 .pptx 转码；批量场景可在 Windows 上用 PowerPoint COM 自动完成（`Presentations.Open(只读)` + `SaveCopyAs(目标路径, 24)`，24 = ppSaveAsOpenXMLPresentation，unppt 仓库 `tools/powerpoint/export.py` 就是这么做的）。

### 2. 批量转换一个目录

直接运行 `scripts/batch-convert.mjs`（用法见文件头注释），或按 `references/api.md` 第 4 节的脚本改写。

### 3. 检查字体（不写文件）

```bash
unppt check 课件.pptx          # 人读格式
unppt check 课件.pptx --json   # JSON，含每个字体用在哪几页、结论、替代方案
```

有 ✗（如符号字体未嵌入）时退出码 1，可用于上传时拒绝问题课件。

### 4. 嵌入网页、用代码控制播放

iframe + postMessage 或官方 `UnpptFrame` 小工具，指令有 `next` / `prev` / `goto` / `sync` / `getState`，事件有 `ready` / `change` / `end` / `link`。完整协议、URL 参数、原生 App 接法见 `references/embedding.md`。

### 5. 在代码里调用（Node 脚本 / HTTP 服务 / 云函数 / 浏览器）

`convert()` 是纯函数：字节进、`write` 回调出，不碰磁盘、不联网，可放进云函数。API 细节、大文件处理、可运行示例见 `references/api.md`。

## 必须遵守的规则

1. **`write` 回调不能互相等待**：`single` / `data` 形式会先以数据流方式写主文件，转码期间还会写 `media/…`、`pic/…` 等。每次调用独立处理，否则死锁。Node 里直接用 `fs.promises.writeFile` 即可（它接受字符串 / Uint8Array / AsyncIterable）。
2. **`convert()` 不会自己找字体和 wasm**：Node 里必须 `loadFontPack()`（从 `@unppt/unppt/node` 导入，读一次可多次共用）并传 `fontPack`；要整页图/缩略图时必须传 `rasterWasm`（读 `@unppt/unppt/resvg.wasm`）或 `rasterPool`，否则不出图只记警告。
3. **大文件按位置读取**：不要把 1GB 文件读进内存，传 `{ size, read(offset, length) }` 形式的 `RandomAccessSource`。浏览器里用 `Blob.slice()` 实现。
4. **检查结果**：转码后查看 `result.fontCheck`（字体问题）和 `result.report.warnings`（渲染警告），有 ✗ 时提醒用户在 PowerPoint 里"将字体嵌入文件"。
5. **商业字体授权**：`--system-fonts` / `fonts` 会把本机字体嵌入产物分发，使用前确认授权。

## 资源索引

| 文件 | 内容 | 何时读 |
|---|---|---|
| `references/cli.md` | 命令行全部选项、`unppt check`、常用组合、输出含义 | 用命令行转换、看不懂输出、选字体选项时 |
| `references/api.md` | `convert()` / `checkFonts()` 全部选项、write 回调、大文件、出图、字体、四类可运行示例 | 写 Node 脚本、HTTP 服务、云函数、浏览器内转码时 |
| `references/embedding.md` | iframe、postMessage 协议、`UnpptFrame`、`window.unppt`、原生 WebView、URL 参数、直播课同步 | 嵌入播放器、控制翻页、监听事件时 |
| `scripts/batch-convert.mjs` | 批量转换目录内所有 .pptx 的 Node 脚本 | 批量转换任务，可直接运行或改写 |
