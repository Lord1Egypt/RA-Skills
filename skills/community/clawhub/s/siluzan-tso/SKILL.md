---
name: siluzan-tso
description: 丝路赞 TSO 广告平台（Google/Bing/Yandex/TikTok/Kwai/MetaAd），凡涉及丝路赞/TSO、投广告、出价预算、广告账户管理须加载本 skill。【§零·最高优先】网址/域名/官网/链接/落地页+诊断/检测/监测/评估/体检/报告等词（含用户混说的「网络诊断/网络检测/网络监测」）→直接P8 website-diagnosis，禁止走P9行业分析或P1账户诊断、禁止A/B/C/D追问；细则见 references/core/intent-routing.md §零。【报告/诊断消歧】其余报告类话术禁止默认某一CLI——行业/市场/战略→P9 market-analysis；Google账户ID+健康诊断→P1 google-ads-diagnosis；账户ID+周期/月度→P4；Meta/TikTok/Bing周期→P4/P4-FB；多账户对比→P3/P5；OKKI周报→P6；Google询盘→P7；官网+明确要搜索广告方案/关键词表→W3；平台优化报告列表/推送→W7；对象仍不清→Read intent-routing.md。【账户】列表/余额/消耗/激活账单（W1）、多账户余额预警 balance-scan（P2）、多户消耗汇总 accounts-digest（P3）、六大媒体开户与进度（W2）、分享/解绑/MCC/BC/BM/权限（W9）。【投放】Google搜索系列方案与 campaign-validate/create（W3）、系列/组/广告/关键词 CRUD/拒审、PMax 创建与素材、AI智投草稿 batch（W4）、拓词 keyword suggest（W5）、AI广告优化 optimize（W6）、优化合规 SOP。【财务】充值/钱包、转账记录、发票/开票/抬头（W8）；写操作审计与 restore。【运营】智能预警 forewarning 创建/启停/记录（W10）、TikTok/Meta 线索 clue（W11）、日周巡检（W12）、宿主编排/投放自控/异常监控（hosted-automation）。【其他】RAG 知识库检索、Meta/Facebook 周期与诊断 HTML、Google/Meta 周期 Excel、多账户 google-analysis-batch。
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
> **报告 / 分析类统一消歧（必读）**：用户话术含「报告 / 诊断 / 分析 / 检测 / 监测 / 月报 / 周报」等，或对象不清（只有「帮我出份报告」）→ **必须先 Read `references/core/intent-routing.md`**。**§零 优先**：**网址/域名/官网/链接 + 诊断类词**（含用户说的「网络诊断/网络检测」）→ **直接 P8**，禁止走 P9/P1；再按 §一 定唯一工作流。**禁止**见「报告」就默认 P4 周期或 P1 诊断。
>
> **默认交付格式**：用户未指定格式时，网站诊断 P8、Meta 周期 P4-FB、战略市场 P9、**Google 广告诊断 P1** 默认 **HTML**（各自 `render` 子命令），Google 周期 P4 默认 HTML；**禁止**仅交付 Markdown 摘要或纯 JSON 充当终稿。

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

**Agent 三步法**：① **网址+诊断类词（含「网络诊断」）→ 直接 P8**（`intent-routing.md` §零）；其余报告类若话术模糊，先 Read `references/core/intent-routing.md` → ② 在下方路由表锁定**唯一**工作流行 → ③ Read 该行「必读文档」与工作流卡片 → ④ 按卡片**编号步骤**执行，写操作前先与用户确认。

---

## 路由表（意图 → 工作流 → 必读文档）

> 首次进入任意任务前先 Read `references/core/agent-conventions.md`。**网址/域名/官网 + 诊断/检测/监测/报告**（含「网络诊断」）→ **§零 直接 P8**，见 `references/core/intent-routing.md`。**用户只说「报告 / 诊断 / 分析 / 检测 / 监测」且对象仍不清** → 必须先 Read `intent-routing.md`（P1–P9 与 W3/W7 统一消歧）。下表每行指向**唯一**工作流；找不到时查 `references/README.md`。

### 账户与财务

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 账户列表 / 有哪些 / 有多少 / 列出全部某媒体 | W1 | `references/accounts/accounts.md`（§ list-accounts 意图速查） |
| 单户实时余额 | W1 | `references/accounts/accounts.md`（balance） |
| 多账户余额 / 续航不足预警 | **P2** | `references/accounts/accounts.md`（balance-scan） |
| 单户消耗 / 投放数据 | W1 / **P1** | `references/accounts/accounts.md`（stats） |
| 多账户消耗/对比汇总 | **P3** | `references/accounts/accounts.md`（accounts-digest） |
| 激活/充值账单明细 | W1 | `references/accounts/accounts.md`（account-active-bills） |
| 开户（六大媒体）/ 开户进度 | W2 | `references/accounts/open-account-by-media.md`（**首次须列全必填项**；Google 加 `references/accounts/open-account-google-ui.md`） |
| 账户权限：分享/取消/解绑/重授权/MCC/BC/BM/关闭/提现/邮箱授权 | W9 | `references/accounts/accounts.md`（account 子命令） |
| 充值 / 钱包 | W8 | `references/accounts/finance.md`（recharge 引导网页） |
| 转账记录 / 账户间转账 | W8 | `references/accounts/finance.md`（transfer） |
| 发票 / 开票 / 发票抬头 | W8 | `references/accounts/finance.md`（invoice / invoice-info） |
| 审计 / 误操作恢复 | — | `references/accounts/write-audit-restore.md` |

### Google 广告投放

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 新建搜索系列 / 出投放方案 / **根据官网·网站·URL 生成 Google 搜索广告** / 搜索广告文案·关键词·**表格** / 写搜索广告计划 | **W3** | `references/google-ads/google-ads-campaign-plan.md` + **`assets/campaign-create-template.json`**（结构真相源，先 Read）+ `assets/campaign-create-template.md`（字段说明）；表格交付读 `references/google-ads/rules/google-ads-launch-plan-template.md`。**≠ P8 网站诊断 / ≠ P9 市场分析 / ≠ W5 仅拓词** |
| 广告系列/组/广告/关键词 CRUD / 拒审 | W3 | `references/google-ads/google-ads.md` |
| PMax 系列 | W3 | **`assets/pmax-create-template.json`**（先 Read）+ `assets/pmax-create-template.md` + `references/google-ads/pmax-api.md` |
| AI 智投草稿 list/get/update/publish | W4 | `references/google-ads/google-ads.md`（§ ad batch） |
| 拓词 / keyword / 关键词规划 | W5 | `references/analytics/keyword-planner-workflows.md`（客户背景先 `references/analytics/rag.md`） |
| AI 广告优化记录 / 建议 | W6 | `references/operations/optimize.md` |
| 优化/合规 SOP | W3 / W6 | `references/google-ads/rules/README.md` |

### 分析与报告（CLI 拉数 + Agent 撰稿）

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 单账户投放画像 / **Google 广告账户诊断** / 账户健康检查 / 投放诊断报告 / 账户体检（**含账户 ID**） | **P1** | `references/analytics/account-analytics.md`；完整 HTML 诊断加 `references/report-templates/google-ads-diagnosis.md` |
| Google 账户 **周期** / **月度** / **季度** 报告 / 月报（**非** OKKI / **非** 询盘 / **非** 强调健康诊断） | **P4** | `references/report-templates/google-period-report.md` + `references/analytics/account-analytics.md`；要 **Excel** 加 `references/report-templates/google-period-report-excel.md` |
| Meta/Facebook 周期或诊断报告 | **P4-FB** | `references/report-templates/meta-period-report.md` + `assets/meta-period-report-rules.md` + `references/analytics/facebook-analysis-guide.md`；要 Excel 加 `references/report-templates/meta-period-report-excel.md` |
| TikTok / Bing 周期报告 | **P4** | `references/analytics/account-analytics.md`（report tiktok-*/bing-*）+ 对应 `references/report-templates/*-period-report.md` |
| 多账户 × 多维度批处理 | **P5** | `references/analytics/google-analysis-batch.md` + `references/analytics/account-analytics.md` |
| OKKI 周报 | **P6** | `references/report-templates/okki-weekly-google-client.md`（全文） |
| Google 询盘分析 | **P7** | `references/report-templates/google-inquiry-analysis.md`（全文）+ `references/analytics/geo-continents.json` |
| **网址/域名/官网/落地页** + 网站或**网络**诊断·检测·监测·评估·体检·质量报告 / 落地页报告 / 官网体检 | **P8** | `references/core/intent-routing.md` **§零** + `references/analytics/website-diagnosis-guide.md` + `assets/website-diagnosis-rules.md`（**必须先** `website-diagnosis collect` + `render`，**默认交付 HTML**；**≠ P9 ≠ W3**） |
| 市场分析 / **行业分析** / **行业分析报告** / 市场调查 / 生成 **XX 行业** 报告（如电商）/ 战略市场报告 / KA 市场报告 | **P9** | `references/analytics/market-analysis-guide.md` + `assets/market-analysis-rules.md`（**必须先** `market-analysis collect` + `render`，**默认交付 HTML**；**禁止**纯 WebSearch 交 Markdown 终稿；**≠ P8**） |
| TSO 平台优化报告：列表/生成/推送 | W7 | `references/analytics/reporting.md` |
| RAG 知识库检索 | W5 | `references/analytics/rag.md` |

### 工具与运营

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 智能预警：创建/查询/启停/触发记录 | W10 | `references/operations/forewarning.md` |
| TikTok / Meta 线索表单 | W11 | `references/operations/clue.md` |
| 日/周巡检 | W12 | `references/core/workflows.md`（W12）+ `references/accounts/accounts.md` |
| 宿主编排 / 投放自控 / 异常监控 / 自动优化 | — | `references/operations/hosted-automation-user-catalog.md`（索引）→ `operations/hosted-automation-*.md` |

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

详见 `references/operations/hosted-automation-self-control.md`、`references/operations/hosted-automation-monitoring-json.md`、`references/operations/hosted-automation-optimize-index.md`。
