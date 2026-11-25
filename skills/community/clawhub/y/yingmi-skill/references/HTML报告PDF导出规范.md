# HTML 报告 PDF 导出规范（全场景共用）

## 定位

本规范与 [`HTML视觉模板.md`](HTML视觉模板.md)、[`demo-report.html`](demo-report.html) 配套使用：

- **屏幕浏览**：沿用 [`demo-report.html`](demo-report.html) 屏幕态规则（默认间距与字号）。
- **PDF / 打印**：HTML 内嵌 demo 的 `@media print` 提供**基准**紧凑样式；**真正决定页数与留白**的是导出脚本在转 PDF 前**自动缩放字号/图表高度**（见下文「导出时自动紧凑」）。

**权责边界**：

- [`demo-report.html`](demo-report.html)：CSS、壳层 DOM、**`@media print` 基准**、`.card-splittable` / `.print-segment` / `.footer-block`。
- **本文件**：分页策略、`card-splittable` 用法、ECharts 重绘、**导出时自动紧凑算法**、Playwright / `RenderHtmlToPdf` 流程。
- 仓库脚本：[`scripts/html-to-pdf.mjs`](../../../scripts/html-to-pdf.mjs) — 本地 Playwright 导出**必须**走此脚本（或等价实现）。
- 各场景 Skill / 模板：只写章节与数据，**不得**另写一套 PDF 字号。

---

## 何时必须遵守

1. 用户明确要求 **PDF / 下载 / 打印**。
2. 交付物含在线 PDF（`RenderHtmlToPdf`）。
3. Agent 本地 Playwright 导出。

凡 HTML 交付都须复制 demo 的 `@media print`（仅影响打印媒体，不改变屏幕态），无论用户当次是否要 PDF。

---

## 核心原则

### 1. 屏幕与 PDF 分离

- PDF 基准样式在 `@media print` 内。
- **禁止**为 PDF 改屏幕态主样式。
- **紧凑排版主要由导出脚本在运行时缩放**（`html.pdf-export-compact` + `--pdf-scale`），不是让用户手改 HTML。

### 2. 分页：避免「整卡抬到下一页」造成大块空白

| 类型 | class | 分页 |
|------|-------|------|
| Hero / AI 卡 / 页脚 | `.hero-card`、`.card.ai-card`、`.footer-block` | 尽量不拆 |
| 普通章节 | `.card` | **允许**在卡内自然分页（`break-inside: auto`） |
| 长章节 | `.card.card-splittable` + `.print-segment` | 段间可分页；段内图表/表尽量不拆 |
| 并排双图 | `.charts-grid` | 打印时保持 **两列**，整组 `avoid` |

> 旧版「所有 `.card` 一律 `break-inside: avoid`」已废弃，会导致 PDF 页尾大面积留白。

### 3. 页脚不拆

免责声明与页脚包在 `.footer-block` 内，结构见 demo。

### 4. 说明文字用 class

`.body-text`、`.note-text`、`.quote-callout` — 勿用 inline 字号控制 PDF。

---

## 导出时自动紧凑（强制）

**原则**：转 PDF 时由脚本根据**内容总高度**自动试探字号比例，在可读前提下减少页数与页尾空白；**不要**指望只改 HTML 里的固定 `font-size` 就能适配每份报告。

### 流程（`scripts/html-to-pdf.mjs`）

0. **预检**：若 HTML 含 `echarts.init`，先运行 `inline_echarts.py`，并用 `--check-only` 确认 ECharts 5.5.0 已内嵌（见 [`HTML视觉模板.md`](HTML视觉模板.md)「ECharts 库内嵌」）；CDN、相对路径或本机绝对路径均直接 exit 1。
1. `goto(file://…)`，等待 `echarts` 与 `initCharts` / `renderAll`。
2. 注入 **`pdf-export-layout-guard`**（布局守卫）：A4 打印页宽约 768px，会误触发 HTML 内 `@media(max-width:768px)` 的移动端规则（KPI 变 2×2、双列图表变单列）。脚本在 `<html>` 上加 class 并注入守卫 CSS，强制恢复 `.kpi-grid` 四列、`.charts-grid` 双列等桌面/打印布局。
3. `emulateMedia({ media: 'print' })`。
4. **`applyPdfCompactScale()`**（核心）：
   - 给 `<html>` 加 class `pdf-export-compact`，设置 CSS 变量 `--pdf-scale`（默认从 `1` 递减，步长 `0.04`，下限 `0.78`）。
   - 按 scale 缩放：`body` 字号、`.section-title` / `.sub-title`、表格、`.card` 间距、`.chart-box` / `.chart-full` 高度；然后 **重新 `initCharts()` + `resize()`**。
   - 用 `.container` 的 `scrollHeight` 与 A4 可打印高度（约 **1050px**）估算页数；取 **页数最少** 中 **scale 最大**（最可读）的一档再导出。
5. `page.pdf({ …, scale: renderScale })`（见下「两层缩放」）。

### 打印布局守卫（脚本自动注入）

| 问题 | 原因 | 守卫行为 |
|------|------|----------|
| Hero KPI 变 2×2、中间横线、竖线像光标 | 打印页宽触发 `@media(max-width:768px)` | 默认 `.kpi-grid` 强制 `repeat(4,1fr)`；`.kpi-grid-2/3/5` 按 class 保留列数；清除移动端 `border-bottom` |
| 双列图表纵向堆叠 | 同上，`.charts-grid { grid-template-columns: 1fr }` | 强制 `1fr 1fr` |
| 指标卡 / 详情区变单列 | 同上 | `.indicator-grid` 四列、`.detail-grid` / `.risk-detail` 双列 |

> 各场景 HTML **仍应**在 `@media print` 内写基准紧凑样式；布局守卫是导出脚本的兜底，避免每份报告单独修 mobile 泄漏。
### 两层缩放（导出脚本自动完成）

| 层级 | 变量 | 作用 |
|------|------|------|
| **排版缩放** | `--pdf-scale` / `typographyScale` | 转 PDF 前在页面内缩小**字号、表格、卡片间距、图表容器高度**，并重绘 ECharts |
| **渲染缩放** | `page.pdf({ scale })` / `renderScale` | 按内容高度估算最少页数，取**可读前提下最大的**渲染比例（0.75–1，步长 0.05） |

> 说明：DOM 高度主要由固定像素图表与表格撑开，仅改字号往往不足以减页；**渲染缩放**用于消除「页数偏多、页尾大块空白」。脚本 stdout 会输出 `typographyScale`、`renderScale`、`domPages`、`pdfPages` 供核对。



### 命令

```bash
node scripts/html-to-pdf.mjs <input.html> [output.pdf] [--min-charts N] [--width 920]
```

依赖：`playwright`（推荐 `channel: 'msedge'`，无需单独下载 Chromium）。

### MCP `RenderHtmlToPdf`

- HTML 须含 demo 完整 `<style>`（含 `@media print`）。
- 参数：`printBackground: true`、`format: "A4"`。
- 若服务端**不做**自动紧凑且版式松散，**必须**回退本地 `html-to-pdf.mjs`。

---

## 打印样式基准（demo 内置）

复制 demo 整段 `<style>` 即含下表**基准**；导出脚本会在其上乘以 `--pdf-scale`：

| 项目 | 屏幕默认 | print 基准（scale=1） |
|------|---------|----------------------|
| 页边距 | — | A4，约 7mm × 6mm（脚本可略收紧） |
| 卡片间距 | 24px | 6px |
| 正文字号 | 14px | 13px |
| 表格 | 14px | 12px |
| chart-box（双列） | 340px | 190px（图区 152px） |
| chart-full | 380px | 248px |

---

## ECharts 与导出前重绘

1. 屏幕态先完成 `initCharts`。
2. `emulateMedia('print')` 后按当前 `--pdf-scale` **再 init + resize**。
3. 等待 canvas 数量 ≥ `--min-charts`（默认 5）再 `pdf()`。

---

## 场景 Skill 执行清单

1. 读场景 SKILL + 模板 → 章节与数据。
2. 嵌入 demo **整段** `<style>`。
3. 长章用 `card-splittable` + `print-segment`；双图用 `.charts-grid`。
4. `footer-block` + `data-theme="light"`。
5. 用户要 PDF → **`node scripts/html-to-pdf.mjs`**（自动紧凑）；失败再 `RenderHtmlToPdf`。

---

## 禁止事项

- ❌ 未含 `@media print` 就交付 PDF。
- ❌ 对所有 `.card` 一律 `break-inside: avoid`（造成大块留白）。
- ❌ 在子 Skill 复制第二套 print CSS。
- ❌ 去掉背景/水印。
- ❌ 未重绘 ECharts 就导出。
- ❌ **只**靠手调 HTML 字号做 PDF 紧凑，而不走导出脚本的自动 scale。

---

## 相关文档

- [HTML视觉模板.md](HTML视觉模板.md)
- [demo-report.html](demo-report.html)
- [MCP数据真实性零容忍.md](MCP数据真实性零容忍.md)
