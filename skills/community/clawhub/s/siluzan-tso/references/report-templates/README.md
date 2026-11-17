# 报告模板目录

本目录包含两类文件：

| 文件类型                | 用途                                            |
| ----------------------- | ----------------------------------------------- |
| `*.md`                  | 报告内容纲要：默认维度、可选维度、对应 CLI 命令 |
| `report-template*.html` | 视觉样式参考：排版/色彩/图表方案，不定义内容    |
| `excel-style-guide.md`  | Excel 通用样式规范（色板/字体/组件），所有平台共用 |
| `excel-style-kit.mjs`   | 配套代码：Agent 写 xlsx 脚本直接 `import` 使用，零依赖 |

> 冲突时以 `*.md` 的内容要求为准，样式文件仅影响排版。任何「用户要 Excel/xlsx/表格」的模板，写脚本时都按 `excel-style-guide.md` 套样式，不再裸写无样式单元格。
>
> **终稿语言**：叙事正文跟 `meta.lang`（`zh` 或 `en`），表头用该语言。文件型终稿必须带 `meta.lang`，并传给 `--lang`。询盘 8 Sheet 和用户自定义 Excel 没有 CLI 渲染器，中文用纲要里的中文表头，英文终稿换成英文同义词。

**图表库（全部 HTML 模板统一）**：ECharts 5 — `https://staticpn.siluzan.com/assets/slz/homeCDN/echarts.min.js`；初始化用 `echarts.init(el).setOption(...)`。勿使用 Chart.js。

**图表自适应**：逻辑必须写在**同一份 HTML 模板内**（`window.addEventListener('resize', … chart.resize())`，可选对容器做 `ResizeObserver`）。报告下载到本地后仍可用；禁止依赖外挂 `*.snippet.js` 或 monkey-patch CDN。

---

## 内容纲要文件

| 文件                                         | 适用场景                                                                                                                                                          |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `google-period-report.md`                    | **Google 周期分析报告（默认）**：终稿=HTML，四步流程 → `google-analysis render` 出 HTML                                                                           |
| `demand-gen-analysis-report.md`              | **Demand Gen 投放数据分析汇总报告（P4-DG）**：终稿=HTML，8 节 → `google-analysis demand-gen-render`。不是全账户 P4，也不是创建广告 |
| `demand-gen-analysis-report-excel.md`        | **仅用户要 Excel 时**：9 Sheet，Agent 脚本写 xlsx；不调用 `demand-gen-render`                                                                                    |
| `google-quarterly-report.md` / `.html`       | **Google 季度经营报告（P10）**：`google-quarterly collect`+`render`；花费三档基于本期；无行业章                                                                |
| `google-quarterly-plan.md`                   | **P10 下期规划规则**：九章 + Q01–Q30；写 `narrative.plan` 前必读                                                                                                 |
| `google-period-report-excel.md`              | **仅用户要 Excel 时**（P4 定制 Sheet）：先 `*.outline.txt` 后脚本写 xlsx；账户须 `-k` 核验，无 CLI excel 子命令                                                   |
| `stats-daily-excel.md`                       | **P4-DAILY**：账户级按日 Excel（`stats --by-day`）                                                                                                                |
| `google-account-diagnosis-report.md`         | Google 账户深度诊断（健康度/转化/结构等）                                                                                                                         |
| `google-ads-diagnosis.md`                    | Google **广告诊断**完整纲要（HTML 区块、**每日趋势 2 位小数**、**每模块必填分析/建议**）                                                                          |
| `meta-period-report.md` / `.html`            | **Meta（Facebook）周期报告（默认）**：四步流程 → `facebook-analysis render` 出 HTML，见 P4-FB                                                                     |
| `meta-period-report-excel.md`                | **仅用户要 Excel 时**：5 Sheet（**汇总数据**/日趋势/国家/广告系列/受众，汇总 KPI 下是一/二/三）；`facebook-analysis render --format xlsx`                           |
| `meta-account-diagnosis-report.md` / `.html` | **Meta（Facebook）诊断报告（默认）**：四步流程 → `facebook-analysis diagnosis-render` 出 HTML（在 7 Section 内对齐 Google 诊断结构，未覆盖小节标 `notAvailable`） |
| `tiktok-period-report.md` / `.html`          | **TikTok 广告主周期报告（默认）**：四步流程 → `tiktok-analysis render` 出 HTML                                                                                    |
| `bing-period-report.md` / `.html`            | **Bing（BingV2）分析报告（默认）**：四步流程 → `bing-analysis render` 出 HTML                                                                                     |
| `yandex-period-report.md` / `.html`          | **Yandex Direct 周期报告（默认）**：四步流程 → `yandex-analysis render` 出 HTML（样式对齐开发样例）                                                               |
| `yandex-period-report-excel.md`              | **仅用户要 Excel 时**：Agent 脚本写 xlsx；无 CLI excel 子命令                                                                                                     |
| `okki-weekly-google-client.md`               | **OKKI 周报**：写 `okki-weekly-report.json` → `google-analysis okki-render` 出 5 Sheet Excel + 客户话术（默认 7 条、一条一行），见 `references/core/playbooks.md` P6 |
| `google-inquiry-analysis.md`                 | **Google 询盘分析**：严格 3 个月 + 用户询盘 + 8 Sheet xlsx，见 `references/core/playbooks.md` P7                                                                  |
| `website-diagnosis-report.md` / `.html`      | **网站诊断**：终稿为 **HTML**（对齐 TSO `WebsiteAnalysisReport/v3`）；配合 `website-diagnosis collect`，见 P8                                                     |

---

## 样式参考文件

| 文件                            | 风格                  |
| ------------------------------- | --------------------- |
| `report-template.html`          | 商务/数据看板（默认） |
| `report-template-formal.html`   | 正式文件/对外         |
| `report-template-dark.html`     | 深色/投屏             |
| `report-template-onepager.html` | 单页摘要              |
| `report-template-mobile.html`   | 移动端                |
| `report-template-print.html`    | 打印归档              |
| `report-template-academic.html` | 学术/研究口吻         |

---

## 生成报告的规则

### 分析报告的维度确认

生成**分析报告**时：

1. 根据对应 `*.md` 的**默认维度**直接开始拉数（见各 `*.md` 首节）。
2. 同时向用户展示该文件里的**可选维度列表**，询问是否需要追加任何维度。
3. 用户追加的维度，补充拉数后追加到报告末尾。
4. 用户说「不用加」或不回复，只输出默认维度的内容。

### 禁止事项

- 不能使用 HTML 样式文件里的假数据填报告
- 不能凭印象写具体数字，所有数字来自 CLI 执行结果
- 某个维度的数据获取失败，在对应章节注明原因，不写推测内容

### 数据不可用时

在对应章节写：`[ 数据不可用：{原因} ]`，不做猜测。
