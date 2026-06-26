---
name: siluzan-tso
description: 通过 siluzan-tso-cli 操作丝路赞 TSO 广告账户（Google/Bing/Yandex/TikTok/Kwai/MetaAd）。（账户）列表、余额、统计、消耗、激活账单、历史、余额扫描 P2、账户摘要 P3、共享/取消共享、解绑、OAuth、MCC/BC/BM 绑定解绑、邮件邀请、TikTok 关闭、暂停撤回；（开户）六大广告平台申请；（Google Ads）系列/广告组/广告/关键词 CRUD、附加信息、地理位置、PMax、搜索投放方案校验/创建、批量异步创建；（分析）google-analysis、google-analysis-batch P5、facebook-analysis P4-FB、网站诊断 P8、市场分析 P9、广告诊断；P1 账户画像、P4 周期报告、P6 OKKI 周报、P7 询盘分析；Google关键词推荐、RAG 检索、TSO 报告列表/创建/推送、智能预警、TikTok/Meta 线索、转账/发票/发票资料、审计恢复。以及当用户提及广告账户、搜索广告创建、PMAX广告创建、广告计划、广告创建、广告、余额、消耗、投放、关键词、开户、MCC/BC、报告、诊断、市场分析、开票或 TSO 等关键词时使用。
license: MIT
compatibility: 需要 Node.js 18+、已安装 siluzan-tso-cli，通过 send-login-code + login 或 config set 完成鉴权
metadata:
  requires: nodejs,siluzan-tso-cli
allowed-tools: Bash(siluzan-tso:*) Read Write
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — edit .tmpl or snippets/, then: node scripts/gen-skill-docs.mjs -->

# Siluzan TSO Skill

本 Skill 只做 **任务路由**：用一张「意图 → 工作流」表把用户需求映射到**唯一**的线性工作流。

- **每个业务都有一条线性工作流**（编号步骤）：
  - **分析 / 报告类**（拉数 → 脚本 → 交付）→ `references/core/playbooks.md`（P1–P9）
  - **操作 / 管理类**（开户、广告 CRUD、优化、预警、推送、线索、财务、权限、巡检）→ `references/core/workflows.md`（W1–W12）
- 业务细节、命令参数、字段口径以各域 `references/*.md` 为准（被工作流卡片引用，**不在本文件重复**）。

<!-- 注入到 SKILL.md.tmpl 的 {{AGENT_PREAMBLE}}；构建时由 gen-skill-docs.mjs 合并 -->

> **Agent 纪律（每个新任务必读）**：先 Read `references/core/agent-conventions.md`（唯一规则真相源：加载纪律、数据处理协议、时间/币种、批量约束、交付前自检），再按下方路由表 Read「必读文档」与对应工作流卡片。禁止跨话题复用参数记忆；数据类任务一律 `--json-out` + **仅用代码**读落盘 JSON（脚本示例见 `references/core/tips.md`）。
>
> **默认交付格式**：用户未指定格式时，网站诊断 P8、Meta 周期 P4-FB、战略市场 P9 默认 **HTML**（各自 `render` 子命令），Google 周期 P4 默认 HTML；**禁止**仅交付 Markdown 摘要或纯 JSON 充当终稿。
>
> **意图消歧（Google 搜索广告方案）**：用户说「根据官网/网站/URL 生成 Google **搜索**广告」「出搜索广告方案/计划/文案/关键词表」「要表格格式」→ **一律走 W3**（`google-ads/google-ads-campaign-plan.md`），**不是** P8 网站诊断、**不是** P9 市场分析、**不是** W5 仅拓词。**禁止**跳过 JSON + `campaign-validate` 门禁，直接凭官网内容手写一张创意/关键词表。**「表格格式」** = 按 `google-ads/rules/google-ads-launch-plan-template.md` 从已 validate 的 JSON **投影** Markdown 表格（先 JSON 代码块 → 再表格正文 → 待确认）；缺预算/地域/账户等必填项时先追问，再进入标准流水线。

---

## 一键安装

- **macOS / Linux / WSL：**
  ```bash
  bash <(curl -fsSL https://unpkg.com/siluzan-tso-cli@latest/dist/skill/scripts/install.sh)
  ```
- **Windows PowerShell：**
  ```powershell
  irm https://unpkg.com/siluzan-tso-cli@latest/dist/skill/scripts/install.ps1 | iex
  ```

Windows：部分 Agent 通过 PowerShell 代执行时可能失败，改在 [Git Bash](https://git-scm.com/download/win) 运行 Bash 版安装命令。

登录与配置见 `references/core/setup.md`。**401 换凭据时优先「手机号 + 验证码」**：`send-login-code` → `login --phone --code`。

---

## 基本使用

`siluzan-tso-cli` 只是包名，安装后可执行命令为 `siluzan-tso`。

```bash
siluzan-tso -h   # 查看帮助
```

**Agent 三步法**：① 在下方路由表按用户意图找到对应行 → ② Read 该行「必读文档」与对应工作流卡片 → ③ 按卡片**编号步骤**逐步执行，写操作前先与用户确认。

---

## 路由表（意图 → 工作流 → 必读文档）

> 首次进入任意任务前先 Read `references/core/agent-conventions.md`。下表每行指向**唯一**工作流；找不到时查 `references/README.md`。

### 账户与财务

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 账户列表 / 有哪些 / 有多少 / 列出全部某媒体 | W1 | `accounts/accounts.md`（§ list-accounts 意图速查） |
| 单户实时余额 | W1 | `accounts/accounts.md`（balance） |
| 多账户余额 / 续航不足预警 | **P2** | `accounts/accounts.md`（balance-scan） |
| 单户消耗 / 投放数据 | W1 / **P1** | `accounts/accounts.md`（stats） |
| 多账户消耗/对比汇总 | **P3** | `accounts/accounts.md`（accounts-digest） |
| 激活/充值账单明细 | W1 | `accounts/accounts.md`（account-active-bills） |
| 开户（六大媒体）/ 开户进度 | W2 | `accounts/open-account-by-media.md`（**首次须列全必填项**；Google 加 `accounts/open-account-google-ui.md`） |
| 账户权限：分享/取消/解绑/重授权/MCC/BC/BM/关闭/提现/邮箱授权 | W9 | `accounts/accounts.md`（account 子命令） |
| 充值 / 钱包 | W8 | `accounts/finance.md`（recharge 引导网页） |
| 转账记录 / 账户间转账 | W8 | `accounts/finance.md`（transfer） |
| 发票 / 开票 / 发票抬头 | W8 | `accounts/finance.md`（invoice / invoice-info） |
| 审计 / 误操作恢复 | — | `accounts/write-audit-restore.md` |

### Google 广告投放

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 新建搜索系列 / 出投放方案 / **根据官网·网站·URL 生成 Google 搜索广告** / 搜索广告文案·关键词·**表格** / 写搜索广告计划 | **W3** | `google-ads/google-ads-campaign-plan.md` + **`assets/campaign-create-template.json`**（结构真相源，先 Read）+ `assets/campaign-create-template.md`（字段说明）；表格交付读 `google-ads/rules/google-ads-launch-plan-template.md`。**≠ P8 网站诊断 / ≠ P9 市场分析 / ≠ W5 仅拓词** |
| 广告系列/组/广告/关键词 CRUD / 拒审 | W3 | `google-ads/google-ads.md` |
| PMax 系列 | W3 | **`assets/pmax-create-template.json`**（先 Read）+ `assets/pmax-create-template.md` + `google-ads/pmax-api.md` |
| AI 智投草稿 list/get/update/publish | W4 | `google-ads/google-ads.md`（§ ad batch） |
| 拓词 / keyword / 关键词规划 | W5 | `analytics/keyword-planner-workflows.md`（客户背景先 `analytics/rag.md`） |
| AI 广告优化记录 / 建议 | W6 | `operations/optimize.md` |
| 优化/合规 SOP | W3 / W6 | `google-ads/rules/README.md` |

### 分析与报告（CLI 拉数 + Agent 撰稿）

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 单账户投放画像 / 诊断 | **P1** | `analytics/account-analytics.md` |
| Google 账户周期报告 | **P4** | `references/report-templates/google-period-report.md` + `analytics/account-analytics.md`；要 **Excel** 加 `references/report-templates/google-period-report-excel.md` |
| Meta/Facebook 周期或诊断报告 | **P4-FB** | `references/report-templates/meta-period-report.md` + `assets/meta-period-report-rules.md` + `analytics/facebook-analysis-guide.md`；要 Excel 加 `references/report-templates/meta-period-report-excel.md` |
| TikTok / Bing 周期报告 | **P4** | `analytics/account-analytics.md`（report tiktok-*/bing-*）+ 对应 `references/report-templates/*-period-report.md` |
| 多账户 × 多维度批处理 | **P5** | `analytics/google-analysis-batch.md` + `analytics/account-analytics.md` |
| OKKI 周报 | **P6** | `references/report-templates/okki-weekly-google-client.md`（全文） |
| Google 询盘分析 | **P7** | `references/report-templates/google-inquiry-analysis.md`（全文）+ `analytics/geo-continents.json` |
| 网站诊断 / 落地页评分 | **P8** | `analytics/website-diagnosis-guide.md` + `assets/website-diagnosis-rules.md`（**默认交付 HTML**） |
| 市场分析 / 行业 / 战略市场报告 | **P9** | `analytics/market-analysis-guide.md` + `assets/market-analysis-rules.md`（**默认交付 HTML**） |
| Google 广告诊断 / 账户健康检查 | **P1** | `references/report-templates/google-ads-diagnosis.md` + `references/report-templates/google-account-diagnosis-report.md` |
| TSO 平台优化报告：列表/生成/推送 | W7 | `analytics/reporting.md` |
| RAG 知识库检索 | W5 | `analytics/rag.md` |

### 工具与运营

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 智能预警：创建/查询/启停/触发记录 | W10 | `operations/forewarning.md` |
| TikTok / Meta 线索表单 | W11 | `operations/clue.md` |
| 日/周巡检 | W12 | `core/workflows.md`（W12）+ `accounts/accounts.md` |
| 宿主编排 / 投放自控 / 异常监控 / 自动优化 | — | `operations/hosted-automation-user-catalog.md`（索引）→ `operations/hosted-automation-*.md` |

---

## Subagent 自主委派（可选）

宿主具备 **Task / subagent** 时：复杂报告或批处理（**P5 / P6 / P7**）、预计 CLI 输出很长 → 先 Read `references/core/subagent-orchestration.md`，按决策矩阵决定是否委派；handoff 模板在 `snippets/handoff-p{5,6,7}-*.md`。**写操作确认、`--commit`、401/`resume` 策略与对用户的最终交付始终留在主 Agent**。无此能力则跳过，按工作流卡片在主会话执行。

---

## 职责划分

| 由 **本 Skill + CLI** 保证 | 由 **宿主客户端 / 外部调度** 负责 |
| -------------------------- | --------------------------------- |
| 结构化字段拉取（`--json-out`） | 何时触发检查（cron、对话） |
| 写命令语义与读命令复核文档 | IF 条件计算与决策 |
| 金额、ID、字段口径一致 | 触达（钉钉/飞书）与工单 |
| references 与命令对齐 | 批处理循环、限速、重试；**可选** subagent 并行 |

详见 `operations/hosted-automation-self-control.md`、`operations/hosted-automation-monitoring-json.md`、`operations/hosted-automation-optimize-index.md`。
