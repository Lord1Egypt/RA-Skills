# HTML 报告视觉模板（全场景共用）

## 单一真源（写死）

| 层级 | 文件 | 职责 |
|------|------|------|
| **CSS + 壳层 DOM + 主题脚本 + PDF print** | [`demo-report.html`](demo-report.html) | **唯一**基准：整段 `<style>`（含 `@media print`）、壳层 DOM、`toggleTheme`、`.footer-block` |
| **本文件** | `HTML视觉模板.md` | 交付顺序、权责、AI 卡/章节序号（**不重复** demo 内 HTML/CSS） |
| **业务正文** | 各场景 `SKILL.md` + `references/*` | 章节、字段、MCP、图表语义 |

生成完整 HTML 时：**必读场景 `SKILL.md` → 全文读 `demo-report.html` → 原样嵌入 demo 的 `<style>` 与壳层 class**；业务板块以场景 skill 为准，禁止照抄 demo 占位数字/结论。

---

## HTML 交付铁律

**前置门禁**：本节仅在 [`输出格式确认协议.md`](输出格式确认协议.md) 的 Step 0 已弹出三行话术、且用户答复为 **B（HTML）** 或 **C 的第 2 步**时执行。确认为 A（Markdown）或尚未弹出询问时，**禁止**进入本节、禁止读 `demo-report.html`、禁止内嵌 ECharts。

1. **必读 ①** 场景 `SKILL.md` 及本任务相关 `references/*`。
2. **必读 ②** [`demo-report.html`](demo-report.html) 全文。
3. **复制** demo 整段 `<style>`（已含屏幕态 + `@media print` + `.card-splittable` / `.print-segment` / `.body-text` 等）。
4. **壳层 DOM** 与 demo 一致：`report-header`、`page-watermark`、`hero-card`、`card` / `ai-card`、`section-title`、`footer-block` 等。
5. **禁止** 自写平行 CSS/class；禁止省略水印、主题切换或 print 块。

---

## ECharts 库内嵌（强制）

凡 HTML 内含 `echarts.init` / 图表容器 `id^="chart"`，最终交付 HTML **必须内嵌 ECharts 5.5.0 完整运行时**，使单个 HTML 在断网、换电脑时仍能渲染图表。`demo-report.html` 中的 CDN 标签仅是生成阶段占位，不得原样交付。

**不触发内嵌的两种情况**：① Step 0 确认为 A（Markdown 交付，无 HTML 文件）；② 本次报告全部板块均为表格与文字、不含任何图表容器。此时不得为「以防万一」预留空图表容器再内嵌运行时。

```powershell
python skills/yingmi-skill/scripts/inline_echarts.py --html <交付.html>
python skills/yingmi-skill/scripts/inline_echarts.py --html <交付.html> --check-only
```

| 禁止 | 原因 |
|------|------|
| jsDelivr / unpkg 等外部 CDN | 目标电脑断网、公司网络拦截或 CDN 不可达 → 图表全空白 |
| `src="echarts.min.js"`、`src="./echarts.min.js"` 等相对路径 | 单独外发 HTML 时同目录未必有库文件 |
| `C:\...\echarts.min.js` / `file:///...` 绝对路径 | 只在生成电脑有效，换电脑必然失效 |
| 省略 `<script>` 却保留 `echarts.init` | 运行时报 `echarts is not defined` |
| 自改内嵌版本 | 与 demo / PDF 导出脚本等待口径不一致 |

**自检**：`inline_echarts.py --check-only` 必须返回 0；发现外部 ECharts `src`、本地路径或缺少内嵌标记时直接失败。

---

## demo 壳层速查（细节以文件为准）

| 区块 | 要点 |
|------|------|
| 水印 | `body::after` 光晕 + `.page-watermark` → `https://asset2.qieman.com/images/ba12dfed-fa69-4ec6-9a32-557035a585af.png`（透明双色 icon，`min(82vw,720px)`，`translateX(36%)`） |
| 顶栏 | `report-header` + `brand-icon` → `https://asset2.qieman.com/images/ecfb2f6c-76db-4f82-b06a-5787ae8d4e16.png`（浅色 `multiply` 去白底） |
| Hero KPI（通用场景） | `.hero-card` → `.kpi-grid` → `.kpi`；涨跌见 demo `#hero`（`.val.val-up|val-down` 直染 或 `.kpi-change` pill） |
| 风险模型三卡 | `.kpi-grid.kpi-grid-3`（风险评分 / 模型 R² / 标准误差；`fund-analyst` §四） |
| 持仓风格六卡 | `.style-grid` → `.style-card`（`.label` / `.val` / `.desc`；`fund-analyst` §六） |
| 综合评价四宫格 | `.eval-grid` → `.eval-card`（`.title` + `.badge` + `.desc`；`fund-analyst` §十） |
| 市场早报 Hero | **两段式**：`.index-close-grid`（指数收盘）+ `.temp-hero-grid`（市场温度三格）；DOM/CSS 见 `demo-report.html`，字段与布局规则见 `market-morning-brief/references/report-templates.md` §④ |
| AI 卡 | `.card.ai-card`：`ai-conclusion` + `ai-list` + `ai-risk`（须在 Hero 之后） |
| PDF 页脚 | `.footer-block` 包裹 `disclaimer` + `footer` |

---

## Hero KPI（全场景）

- **DOM / class 仅以 demo `#hero` 为准**；各场景 `report-templates.md` 只写 label 与 MCP 字段。
- **直接红/绿（图二，基金等）**：主数字用 `.val.val-up` 或 `.val.val-down`（涨红跌绿，32px 级字号）；**禁止**再套 `.kpi-change`。示例：日涨跌、近1年收益、成立以来、**策略 Hero 最大回撤**（绝对值也须 `val-down`）。
- **上黑下彩（pill）**：中性 `.val`（黑色主值）+ 仅 `.kpi-change.val-up|val-down`（圆角 pill，参考 demo「沪深300 / -2.11%」）；**禁止** `.kpi-change-sub` 小字直染。
- **中性数字（无涨跌色）**：直接用 `.val`（32px，不加 `val-up`/`val-down`），适用于金额、比例、中性指标等；**禁止**在有大数字邻格的 KPI 宫格里用 `.val.val-text`，因为其 `margin-top:auto` + `font-size:15px` 会导致文字沉底、格间高度错位。
- **`.val.val-text` 仅限**：整格无 32px 大数字、只需展示长文本/多行说明时（如降级状态文案），且该格不与 `.val` 大数字格并排。副标说明用 `.kpi-sub`（pill 样式）。
- **列数变体**：`.kpi-grid-2` / `.kpi-grid-3` / `.kpi-grid-5`（demo 已定义 `grid-template-columns`）。

### 市场早报 Hero（`market-morning-brief` 专用）

- **禁止**在 `.hero-card` 内重复展示同一批指数/温度（例如通用 `.kpi-grid-3` 与 `.index-close-grid` 并存）。
- **指数收盘**：`.index-close-grid` → `.index-close-card` — **强约束单行**：有几条 `interpretations[]` 就几张卡，**全部同一行**；`flex-wrap:nowrap`，禁止多行 grid / 禁止移动端折行堆叠（窄屏仅横向滚动）。标签 `.tag-domestic` / `.tag-overseas` → **上黑下彩**（demo 同款）：`.label` + 中性 `.val` + `.kpi-change.val-up|val-down` pill。
- **市场温度**：`.temp-hero-card` — `.label` + 中性大号 `.val` + `.kpi-sub` pill（较高估/高估 `.kpi-sub-hot`，低估/较低估 `.kpi-sub-cool`，合理纯 `.kpi-sub`）。
- **第一章仪表**：`.temp-gauge-block` + `.temp-gauge-caption`（单行解读，禁止右侧独立方框）。

> `.hero-kpi-panel` / `.kpi-grid-market` / `.kpi-grid-temp` 为历史样式，**市场早报不再使用**。

---

## PDF 导出

[`HTML报告PDF导出规范.md`](HTML报告PDF导出规范.md) 说明分页策略与导出流程。**`@media print` 已内置 demo**，复制整段 `<style>` 即可；长章节用 `.card.card-splittable` + 内层 `.print-segment`。

---

## AI 核心观点卡（强制）

位于 `hero-card` 之后；三段结构 `.ai-conclusion` / `.ai-list` / `.ai-risk` 不可省略。通用长度与禁忌见 demo `#summary`；业务维度由各场景 `report-templates` 规定。

---

## 章节标题（强制）

所有 `.section-title` 使用「一、」「二、」…中文序号 + 顿号 + 章节名；不适用 `.sub-title`、表头、KPI `.label`、`.ai-title` 等。左侧色条由 demo CSS 渲染。

## 页末风险提示块（强制）

`.risk-notice-card` 位于最后正文 `.card` 与 `.footer-block` 之间；标题用 `.risk-notice-title`（**禁止**「六、」「十一、」等章节序号）。块内每条声明为独立 `<p class="risk-notice-source">`，**禁止** `<ol>` / `<ul>` / 列表序号。详见 [`报告编排与交付公约.md`](报告编排与交付公约.md) §6。

---



## 数据来源口径（客户可见）

- 页眉 .brand-sub、免责声明末句、表格/图表脚注：**统一**写 **「数据来源：盈米MCP」**（无空格），可追加「数据截至 YYYY-MM-DD」。
- 页脚：Powered by 盈米MCP · YYYY-MM-DD（见 demo #footer）。
- 详见 [MCP数据真实性零容忍.md](MCP数据真实性零容忍.md) §0。
## 相关文档

- [`报告编排与交付公约.md`](报告编排与交付公约.md) — 编排/呈现/免责（§1–7）
- [`demo-report.html`](demo-report.html)
- [`HTML报告PDF导出规范.md`](HTML报告PDF导出规范.md)
- [`MCP数据真实性零容忍.md`](MCP数据真实性零容忍.md)
