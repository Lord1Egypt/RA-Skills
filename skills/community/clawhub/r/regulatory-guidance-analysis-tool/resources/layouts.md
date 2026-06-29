# 布局目录

本文件记录 gugu-gaga 生成 HTML 时可用的所有布局模式，以及三种输出格式（pptx-model / pdf-model / single-page）各自对应的实现方式。

下方映射表是生成 HTML 时的核心参考：根据内容选择合适布局，再按"规则"列选择实现方式。single-page 的 HTML 文件位于 `templates/single-page/<name>.html`，可直接在浏览器中打开预览效果。

## 应用场景 → 三体系实现映射

规则：pptx-model / pdf-model 有专属组件的，直接使用；没有的，参考 single-page 对应布局的结构，改用当前格式的可用 class 实现。

| 应用场景 | pptx-model 实现 | pdf-model 实现 | single-page 实现 |
|---------|----------------|----------------|-----------------|
| 封面页 | `.ts-stripe` + `.ts-alert-tag` + `.ts-h1` | `.page-dot` + `.sticker` + `.h1` + `.cover-title` | `cover.html`：`.card` + `.h1` + `.kicker` + `.pill` |
| 目录页 | `.ts-grid-3` + `.ts-card` | `.stack` + `.hand-box` | `toc.html`：`.grid.g3` + `.card` |
| 分节页 | 大号 `.ts-h1` + `.ts-kicker` | `.big-emoji` + `.h2` + `.lede` | `section-divider.html`：`.h1` + `.kicker` |
| 要点列表 | `.ts-card` 纵向堆叠 | `.hand-box` 纵向堆叠 | `bullets.html`：`.card` 列表 |
| 两栏内容 | `.ts-grid-2` + `.ts-card` 并排 | 两 `.hand-box` 并排 | `two-column.html`：`.grid.g2` + `.card` |
| 三栏内容 | `.ts-grid-3` + `.ts-card` | `.stack` + `.hand-box` | `three-column.html`：`.grid.g3` + `.card` |
| 大引用 | 参考 `big-quote.html`（`.ts-h2` + `<blockquote>`） | 参考 `big-quote.html`（`.big-emoji` + `<blockquote>`） | `big-quote.html`：`.h1` + `<blockquote>` |
| 数字高亮 | 参考 `stat-highlight.html`（`.ts-h1` 大号数字 + `.ts-sub`） | 参考 `stat-highlight.html`（`.sticker` + `.h1`） | `stat-highlight.html`：`.h1` + `.counter` |
| KPI 网格 | `.ts-grid-4` + `.ts-card` | `.stack` + `.hand-box` | `kpi-grid.html`：`.grid.g4` + `.card` |
| 表格 | 参考 `table.html`（HTML `<table>` + base.css 样式） | 参考 `table.html`（HTML `<table>` + base.css 样式） | `table.html`：`<table>` + `.card` 包裹 |
| 柱状图 | 参考 `chart-bar.html`（Chart.js `<canvas>`） | 参考 `chart-bar.html`（Chart.js `<canvas>`） | `chart-bar.html`：柱状图 |
| 折线图 | 参考 `chart-line.html`（Chart.js `<canvas>`） | 参考 `chart-line.html`（Chart.js `<canvas>`） | `chart-line.html`：折线图 |
| 饼图 | 参考 `chart-pie.html`（Chart.js `<canvas>`） | 参考 `chart-pie.html`（Chart.js `<canvas>`） | `chart-pie.html`：饼图 |
| 雷达图 | 参考 `chart-radar.html`（Chart.js `<canvas>`） | 参考 `chart-radar.html`（Chart.js `<canvas>`） | `chart-radar.html`：雷达图 |
| 代码展示 | `.ts-codebox` | 参考 `code.html`（`<pre>` + `.card`） | `code.html`：highlight.js |
| 代码对比 | 参考 `diff.html`（两 `.ts-card` 并排，+/- 标注） | 参考 `diff.html`（两 `.hand-box` 并排，+/- 标注） | `diff.html`：+/- 行内标注 |
| 终端模拟 | 参考 `terminal.html`（`.ts-codebox` 模拟窗口） | 参考 `terminal.html`（`<pre>` + `.card` 模拟窗口） | `terminal.html`：窗口模拟 |
| 流程图 | 参考 `flow-diagram.html`（SVG，5 节点管线） | 参考 `flow-diagram.html`（SVG，5 节点管线） | `flow-diagram.html`：流程图 |
| 架构图 | 参考 `arch-diagram.html`（SVG，3 层架构） | 参考 `arch-diagram.html`（SVG，3 层架构） | `arch-diagram.html`：架构图 |
| 步骤图 | `.ts-grid-4` + `.ts-card` | `.num-circle` + `.hand-box` | `process-steps.html`：4 步骤卡片 |
| 思维导图 | 参考 `mindmap.html`（SVG，径向布局） | 参考 `mindmap.html`（SVG，径向布局） | `mindmap.html`：思维导图 |
| 时间线 | 参考 `timeline.html`（SVG/HTML，水平时间线） | 参考 `timeline.html`（SVG/HTML，水平时间线） | `timeline.html`：SVG 时间线 |
| 路线图 | 参考 `roadmap.html`（`.ts-grid-4` + `.ts-card`，4 栏） | 参考 `roadmap.html`（`.stack` + `.hand-box`，4 栏） | `roadmap.html`：4 栏 当前/下一步/后期/愿景 |
| 甘特图 | 参考 `gantt.html`（SVG，12 周甘特） | 参考 `gantt.html`（SVG，12 周甘特） | `gantt.html`：甘特图 |
| 对比页 | 两 `.ts-card` 并排 | 两 `.hand-box` 并排 | `comparison.html`：对比页 |
| 利弊页 | 两 `.ts-card` 并排 | 两 `.hand-box` 并排 | `pros-cons.html`：利弊页 |
| 待办清单 | `.ts-checklist` + `.ts-check` / `.ts-check.ok` | 参考 `todo-checklist.html`（`.hand-box` + ✅/☐） | `todo-checklist.html`：`.card` + checkbox |
| 大图引导 | 参考 `image-hero.html`（`.ts-stripe` + 背景图） | 参考 `image-hero.html`（`.big-emoji` + 背景图） | `image-hero.html`：全屏背景 |
| 图片网格 | `.ts-grid-3` + `<img>` | 参考 `image-grid.html`（`.stack` + `<img>`） | `image-grid.html`：图片网格 |
| 行动号召 | `.ts-alert-box` | `.big-emoji` + `.h1` + `.tag-row` | `cta.html`：大标题 + 按钮 |
| 红黄绿灯网格 | `.ts-grid-3` + `.ts-card`，每卡条文号 `<b>` + 摘要 `<p>`，gap:10px，padding:10px 12px | `.hand-box` 三列 flex-wrap 网格 + `.num-circle` + `<p>`，gap:12px，卡片尺寸 flex:0 0 calc(33% - 8px);padding:8px 10px | — |
| 结束页 | 大号 `.ts-h1` | `.big-emoji` + `.h1` | `thanks.html`：`.h1` + 动效 |

