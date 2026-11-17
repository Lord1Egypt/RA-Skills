# References 索引

> **运行时**：按 `SKILL.md` 路由表直接 Read 列出的文件，**不要**为找路径加载本文件全文。改文档结构见 `skill-authoring.md`。

## 基础与纪律

| 文件                                          | 用途                                     |
| --------------------------------------------- | ---------------------------------------- |
| `references/core/setup.md`                    | 安装、登录（手机验证码优先）、配置、更新 |
| `references/core/agent-conventions.md`        | 通用纪律 + §十四沟通                     |
| `references/core/user-communication-guide.md` | 重定向 → `agent-conventions.md` §十四    |
| `references/core/intent-routing.md`           | 报告/分析/拓词话术消歧                   |
| `references/core/tips.md`                     | `--json-out` 脚本食谱                    |
| `references/core/playbooks.md`                | 分析/报告工作流（P1–P9）                 |
| `references/core/workflows.md`                | 操作/管理工作流（W1–W13）                |
| `references/core/subagent-orchestration.md`   | 可选：P5/P6/P7 委派 subagent             |
| `references/core/skill-authoring.md`          | 维护约定（运行时勿加载）                 |

## 账户与财务

| 文件                                            | 用途                                                              |
| ----------------------------------------------- | ----------------------------------------------------------------- |
| `references/accounts/accounts.md`               | **账户域索引**（按任务再读子文件）                                |
| `references/accounts/accounts-list.md`          | list-accounts、激活账单、开户申请历史                             |
| `references/accounts/accounts-balance-stats.md` | balance、**balance-scan（P2）**、stats、**accounts-digest（P3）** |
| `references/accounts/accounts-permissions.md`   | 分享/解绑/重授权/MCC/BC/BM/关闭/提现/邮箱授权                     |
| `references/accounts/currency.md`               | CNY/USD 字段来源、符号、跨币种禁止求和                            |
| `references/accounts/open-account-by-media.md`  | 各媒体开户命令与参数                                              |
| `references/accounts/open-account-google-ui.md` | Google 开户字段与 Agent 流程                                      |
| `references/accounts/finance.md`                | 转账、开票、充值                                                  |
| `references/accounts/write-audit-restore.md`    | 写审计、`--commit`、restore                                       |

## Google 广告

| 文件                                                | 用途                                   |
| --------------------------------------------------- | -------------------------------------- |
| `references/google-ads/google-ads.md`               | **Google Ads 索引**（金额/ID Gotchas） |
| `references/google-ads/google-ads-read.md`          | 系列/组/创意/关键词/搜索词/地理查询    |
| `references/google-ads/google-ads-write.md`         | 创建/编辑/启停/扩展/PMax/设备出价      |
| `references/google-ads/google-ads-batch.md`         | batch 流水线、ad batch、智投草稿       |
| `references/google-ads/google-ads-campaign-plan.md` | 搜索系列 7 步流水线、validate/create   |
| `references/google-ads/pmax-api.md`                 | PMax 网关路径、金额口径                |
| `references/analytics/keyword-planner-workflows.md` | keyword / google-analysis 拓词         |
| `references/google-ads/rules/README.md`             | 优化/合规 SOP 索引                     |

## Meta 广告

| 文件                                          | 用途                                      |
| --------------------------------------------- | ----------------------------------------- |
| `references/meta-ads/meta-ads.md`             | **Meta Instant Form 索引**（金额/ID）     |
| `references/meta-ads/meta-ads-read.md`        | 账户/主页/表单/按 ID 读系列组广告         |
| `references/meta-ads/meta-ads-write.md`       | validate/create 与原语写命令              |
| `references/meta-ads/meta-lead-launch-plan-template.md` | 出方案/创建前审查稿；xlsx 由 `meta-ad plan-render` 生成 |
| `assets/meta-lead-create-template.json` + `.md` | Lead Ad JSON 契约（**先 Read `.json`**） |

## 分析与报告

| 文件                                              | 用途                                        |
| ------------------------------------------------- | ------------------------------------------- |
| `references/analytics/account-analytics.md`       | 拉数、数据时效性、诊断模板                  |
| `references/analytics/website-diagnosis-guide.md` | 网站诊断 CLI、6 模块规则、对齐 tso_agent    |
| `references/analytics/market-analysis-guide.md`   | 战略市场分析 CLI、Agent 调研流程            |
| `assets/market-analysis-rules.md`                 | 市场分析报告章节与 HTML 版式（Agent 必读）  |
| `references/analytics/facebook-analysis-guide.md` | Facebook 字段、与 Google 报告对照、撰写清单 |
| `references/analytics/google-analysis-batch.md`   | 多账户批处理 run/resume/status              |
| `references/analytics/reporting.md`               | TSO 优化报告生成与推送                      |
| `references/analytics/rag.md`                     | 知识库 list/query                           |
| `references/analytics/geo-continents.json`        | 国家→大洲映射（询盘分析）                   |

## 运营工具

| 文件                                                         | 用途                   |
| ------------------------------------------------------------ | ---------------------- |
| `references/operations/optimize.md`                          | AI 优化建议记录        |
| `references/operations/forewarning.md`                       | 智能预警               |
| `references/operations/clue.md`                              | TikTok / Meta 线索表单 |
| `references/operations/hosted-automation-user-catalog.md`    | 高阶自动化能力目录     |
| `references/operations/hosted-automation-self-control.md`    | Google 预算/CPA/空耗自控 SOP |
| `references/operations/hosted-automation-monitoring-json.md` | Google 异常监控 JSON 键名 |
| `references/operations/hosted-automation-optimize-index.md`  | Google 自动优化 SOP 索引 |
| `references/operations/hosted-automation-bing.md`            | Bing 只读巡检 SOP      |
| `references/operations/hosted-automation-yandex.md`          | Yandex 只读巡检 SOP    |
| `references/operations/hosted-automation-tiktok.md`          | TikTok 只读巡检 SOP    |
| `references/operations/hosted-automation-facebook.md`        | Facebook / MetaAd 只读巡检 SOP |
| `references/operations/hosted-automation-scenarios.md`       | 宿主编排场景索引       |

## Assets 模板（`../assets/`）

| 文件                                    | 用途                                                      |
| --------------------------------------- | --------------------------------------------------------- |
| `campaign-create-template.json` + `.md` | 搜索系列 batch 契约（**先 Read `.json`**，再 Read `.md`） |
| `website-diagnosis-rules.md`            | 网站诊断评分项与 JSON Schema                              |
| `meta-period-report-rules.md`           | Meta 周期报告内容丰富度与建议撰写规则                     |
| `meta-period-report.schema.json`        | Meta 周期报告 Agent JSON Schema                           |
| `google-quarterly-report.schema.json`   | Google 季度经营报告 Agent JSON Schema                     |
| `pmax-create-template.md` / `.json`     | PMax 新建契约                                             |
| `meta-lead-create-template.json` + `.md` | Meta Instant Form Lead Ad 契约                          |
| `pmax-asset-group-template.json`        | PMax 素材组                                               |
| `pmax-signals-template.json`            | PMax 信号                                                 |
| `pmax-assets-update-template.json`      | PMax 素材更新                                             |
| `pmax-patch-campaign-template.json`     | PMax 系列 patch                                           |

## 报告模板纲要（`report-templates/`）

> 安装包内与 `report-templates/*.md` 同源；HTML 样式在 `report-templates/*.html`。索引见 `report-templates/README.md`。

| 文件                                                             | 适用场景                       |
| ---------------------------------------------------------------- | ------------------------------ |
| `google-period-report.md`                                        | Google 账户周期/月度报告（P4） |
| `demand-gen-analysis-report.md` / `demand-gen-analysis-report-excel.md` | Demand Gen 投放数据分析汇总（P4-DG） |
| `google-quarterly-report.md`                                     | Google 季度经营报告（P10）     |
| `google-quarterly-plan.md`                                       | P10 下期规划规则（九章）       |
| `google-period-report-excel.md`                                  | P4 用户要 Excel                |
| `stats-daily-excel.md`                                           | P4-DAILY 按日 Excel            |
| `meta-period-report.md` / `meta-period-report-excel.md`          | Meta 周期（P4-FB）             |
| `google-ads-diagnosis.md` / `google-account-diagnosis-report.md` | Google 诊断（P1）              |
| `website-diagnosis-report.md`                                    | 网站诊断（P8）                 |
| `market-analysis-report.md`                                      | 战略市场分析（P9）             |
| `okki-weekly-google-client.md`                                   | OKKI 周报（P6）                |
| `google-inquiry-analysis.md`                                     | 询盘分析（P7）                 |
| `tiktok-period-report.md` / `bing-period-report.md`              | TikTok / Bing 周期（P4）       |
| `yandex-period-report.md` / `yandex-period-report-excel.md`      | Yandex 周期 HTML / Excel（P4） |
| `REPORT-WORKFLOW.md`                                             | 通用六步流程                   |

样式参考 HTML 见根目录 `report-templates/README.md`。

## Handoff 模板（`../snippets/`，随 skill 安装）

| 文件                    | 用途                              |
| ----------------------- | --------------------------------- |
| `handoff-p5-batch.md`   | P5 batch 与按账户聚合 Task prompt |
| `handoff-p6-okki.md`    | P6 OKKI 拉数 / 写 JSON + okki-render |
| `handoff-p7-inquiry.md` | P7 询盘拉数与 xlsx                |

`agent-preamble.md` 仅用于构建时注入 `SKILL.md`，不复制到 `dist/skill/snippets/`。
