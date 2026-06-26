# 报告模板纲要（report-templates）

> **Agent Read 路径（推荐）**：`references/report-templates/<文件名>.md`  
> **同源副本**：`report-templates/<文件名>.md`（Skill 根目录，与 HTML 样式模板同目录）  
> **HTML 样式参考**（仅排版，不定义章节）：`report-templates/report-template*.html`、`report-templates/*-report.html`

安装包构建时会将根目录 `report-templates/*.md` **同步到本目录**，避免 Agent 按 `references/` 前缀查找时 404。

---

## 周期 / 账户报告

| 文件                               | 工作流    | 说明                                  |
| ---------------------------------- | --------- | ------------------------------------- |
| `google-period-report.md`          | **P4**    | Google 账户周期报告（默认 HTML 纲要） |
| `google-period-report-excel.md`    | **P4**    | 用户要 Excel 时全文必读               |
| `meta-period-report.md`            | **P4-FB** | Meta/Facebook 周期报告（默认 HTML）   |
| `meta-period-report-excel.md`      | **P4-FB** | Meta Excel 五 Sheet                   |
| `meta-account-diagnosis-report.md` | **P4-FB** | Meta 深度诊断                         |
| `tiktok-period-report.md`          | **P4**    | TikTok 周期报告                       |
| `bing-period-report.md`            | **P4**    | Bing 周期报告                         |

## 诊断 / 专项

| 文件                                 | 工作流 | 说明                                        |
| ------------------------------------ | ------ | ------------------------------------------- |
| `google-ads-diagnosis.md`            | **P1** | Google 广告诊断完整纲要                     |
| `google-account-diagnosis-report.md` | **P1** | Google 账户深度诊断                         |
| `website-diagnosis-report.md`        | **P8** | 网站诊断（配合 `website-diagnosis render`） |
| `market-analysis-report.md`          | **P9** | 战略市场分析交付检查清单                    |

## 客户交付 / Excel

| 文件                           | 工作流 | 说明                        |
| ------------------------------ | ------ | --------------------------- |
| `okki-weekly-google-client.md` | **P6** | OKKI 周报（全文必读）       |
| `google-inquiry-analysis.md`   | **P7** | Google 询盘分析（全文必读） |

## 通用

| 文件                 | 说明             |
| -------------------- | ---------------- |
| `REPORT-WORKFLOW.md` | 六步报告流程总览 |

章节细则另见 `references/core/playbooks.md`（P1–P9）与 `references/analytics/account-analytics.md`。
