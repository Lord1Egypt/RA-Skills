# References 索引

> Agent 按 `SKILL.md` 路由表（意图 → 工作流 → 必读文档）定位：分析/报告类线性步骤在 `core/playbooks.md`（P1–P9），操作/管理类在 `core/workflows.md`（W1–W12），命令参数在各域 reference。

## 基础与纪律

| 文件                             | 用途                                                                                        |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| `core/setup.md`                  | 安装、登录（手机验证码优先）、配置、更新                                                    |
| `core/agent-conventions.md`      | **Agent 必读 · 唯一规则真相源**：加载纪律、数据处理协议、硬规范、时间/币种/批量、交付前自检 |
| `core/tips.md`                   | `--json-out` 脚本食谱（node -e 示例、文件命名、分页）                                       |
| `core/playbooks.md`              | **工作流目录 · 分析/报告类**（P1–P9，统一卡片：触发/必读/步骤/交付）                        |
| `core/workflows.md`              | **工作流目录 · 操作/管理类**（W1–W12，同卡片格式）                                          |
| `core/subagent-orchestration.md` | **可选**：主 Agent 自主决定是否委派 subagent（P5/P6/P7）                                    |

## 账户与财务

| 文件                                 | 用途                                                             |
| ------------------------------------ | ---------------------------------------------------------------- |
| `accounts/accounts.md`               | 列表、余额、消耗、分享、MCC/BC/BM、balance-scan、accounts-digest |
| `accounts/currency.md`               | CNY/USD 字段来源、符号、跨币种禁止求和                           |
| `accounts/open-account-by-media.md`  | 各媒体开户命令与参数                                             |
| `accounts/open-account-google-ui.md` | Google 开户字段与 Agent 流程                                     |
| `accounts/finance.md`                | 转账、开票、充值                                                 |
| `accounts/write-audit-restore.md`    | 写审计、`--commit`、restore                                      |

## Google 广告

| 文件                                     | 用途                                 |
| ---------------------------------------- | ------------------------------------ |
| `google-ads/google-ads.md`               | Google Ads CRUD、batch、拒审字段     |
| `google-ads/google-ads-campaign-plan.md` | 搜索系列 7 步流水线、validate/create |
| `google-ads/pmax-api.md`                 | PMax 网关路径、金额口径              |
| `analytics/keyword-planner-workflows.md` | keyword / google-analysis 拓词       |
| `google-ads/rules/README.md`             | 优化/合规 SOP 索引                   |

## 分析与报告

| 文件                                   | 用途                                        |
| -------------------------------------- | ------------------------------------------- |
| `analytics/account-analytics.md`       | 拉数、数据时效性、诊断模板                  |
| `analytics/website-diagnosis-guide.md` | 网站诊断 CLI、6 模块规则、对齐 tso_agent    |
| `analytics/market-analysis-guide.md`   | 战略市场分析 CLI、Agent 调研流程            |
| `assets/market-analysis-rules.md`      | 市场分析报告章节与 HTML 版式（Agent 必读）  |
| `analytics/facebook-analysis-guide.md` | Facebook 字段、与 Google 报告对照、撰写清单 |
| `analytics/google-analysis-batch.md`   | 多账户批处理 run/resume/status              |
| `analytics/reporting.md`               | TSO 优化报告生成与推送                      |
| `analytics/rag.md`                     | 知识库 list/query                           |
| `analytics/geo-continents.json`        | 国家→大洲映射（询盘分析）                   |

## 运营工具

| 文件                                              | 用途                   |
| ------------------------------------------------- | ---------------------- |
| `operations/optimize.md`                          | AI 优化建议记录        |
| `operations/forewarning.md`                       | 智能预警               |
| `operations/clue.md`                              | TikTok / Meta 线索表单 |
| `operations/hosted-automation-user-catalog.md`    | 高阶自动化能力目录     |
| `operations/hosted-automation-self-control.md`    | 预算/CPA/空耗自控 SOP  |
| `operations/hosted-automation-monitoring-json.md` | 异常监控 JSON 键名     |
| `operations/hosted-automation-optimize-index.md`  | 自动优化 SOP 索引      |
| `operations/hosted-automation-scenarios.md`       | 宿主编排场景索引       |

## Assets 模板（`../assets/`）

| 文件                                    | 用途                                  |
| --------------------------------------- | ------------------------------------- |
| `campaign-create-template.json` + `.md` | 搜索系列 batch 契约（**先 Read `.json`**，再 Read `.md`） |
| `website-diagnosis-rules.md`            | 网站诊断评分项与 JSON Schema          |
| `meta-period-report-rules.md`           | Meta 周期报告内容丰富度与建议撰写规则 |
| `meta-period-report.schema.json`        | Meta 周期报告 Agent JSON Schema       |
| `pmax-create-template.md` / `.json`     | PMax 新建契约                         |
| `pmax-asset-group-template.json`        | PMax 素材组                           |
| `pmax-signals-template.json`            | PMax 信号                             |
| `pmax-assets-update-template.json`      | PMax 素材更新                         |
| `pmax-patch-campaign-template.json`     | PMax 系列 patch                       |

## 报告模板纲要（`references/report-templates/`）

> 安装包内与 `report-templates/*.md` 同源；HTML 样式在 `report-templates/*.html`。索引见 `references/report-templates/README.md`。

| 文件                                                             | 适用场景                       |
| ---------------------------------------------------------------- | ------------------------------ |
| `google-period-report.md`                                        | Google 账户周期/月度报告（P4） |
| `google-period-report-excel.md`                                  | P4 用户要 Excel                |
| `meta-period-report.md` / `meta-period-report-excel.md`          | Meta 周期（P4-FB）             |
| `google-ads-diagnosis.md` / `google-account-diagnosis-report.md` | Google 诊断（P1）              |
| `website-diagnosis-report.md`                                    | 网站诊断（P8）                 |
| `market-analysis-report.md`                                      | 战略市场分析（P9）             |
| `okki-weekly-google-client.md`                                   | OKKI 周报（P6）                |
| `google-inquiry-analysis.md`                                     | 询盘分析（P7）                 |
| `tiktok-period-report.md` / `bing-period-report.md`              | TikTok / Bing 周期（P4）       |
| `REPORT-WORKFLOW.md`                                             | 通用六步流程                   |

样式参考 HTML 见根目录 `report-templates/README.md`。

## Handoff 模板（`../snippets/`，随 skill 安装）

| 文件                    | 用途                              |
| ----------------------- | --------------------------------- |
| `handoff-p5-batch.md`   | P5 batch 与按账户聚合 Task prompt |
| `handoff-p6-okki.md`    | P6 OKKI 拉数 / 写 xlsx            |
| `handoff-p7-inquiry.md` | P7 询盘拉数与 xlsx                |

`agent-preamble.md` 仅用于构建时注入 `SKILL.md`，不复制到 `dist/skill/snippets/`。
