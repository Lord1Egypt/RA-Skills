---
name: siluzan-tso
description: 丝路赞 TSO 广告平台（Google/Bing/Yandex/TikTok/MetaAd），凡涉及丝路赞/TSO、投广告、出价预算、广告账户管理，或需要做行业分析/市场分析/行业分析报告（含「写一份 XX 行业报告」「电商/制造/医疗等行业报告」「市场调查/战略市场/KA 市场报告」「竞品/GTM/市场格局/行业趋势」等，无论是否提及丝路赞/广告/客户）须加载本 skill。【§零·最高优先】网址/域名/官网+诊断/检测/监测/评估/体检/报告/符合投放要求/能不能投（含「网络诊断」混说）→P8 website-diagnosis collect（禁纯WebFetch/肉眼看页），禁止P9/P1/W3、禁止A/B/C/D追问；细则见 intent-routing.md §零。【§零·B·次高优先】未命中§零时，行业/市场分析报告类话术→必走P9 market-analysis collect+render出HTML，禁止纯WebSearch/WebFetch在对话里写Markdown/HTML当终稿、禁止改走P8/P1/P4/W5/google-analysis；细则见 references/core/intent-routing.md §零·B。【§零·C·关键词规划】Google Ads/谷歌广告拓词、关键词规划/推荐、Keyword Planner、长尾关键词、月搜索量/搜索量、竞争度、核心词/种子词扩词（含「阅读网址/文章/页面后针对核心词出带搜索量词表」，无论是否提及丝路赞/TSO/账户）→必走W5，一次 keyword -k … --google-only --min-monthly-search，禁止分批洗词脚本，禁止WebSearch/WebFetch编造搜索量当终稿；细则见 references/core/intent-routing.md §零·C。【报告/诊断消歧】其余报告类话术禁止默认某一CLI——行业/市场/战略/行业分析报告→P9 market-analysis（必走collect+render，禁止纯WebSearch代替）；Google账户ID+健康诊断→P1 google-ads-diagnosis；只要周期数据/8维/花费转化汇总/Excel→P4；Demand Gen/需求开发投放数据分析或汇总报告→P4-DG（demand-gen-render 出 HTML，要 Excel 走对应纲要，不是创建 W3）；Google/谷歌广告月度报告、月总结与规划、季度报告、Q3汇总、Q4规划、季度汇报、投放季报、客户版、大族模板、下月规划→P10 google-quarterly；Meta/TikTok/Bing周期→P4/P4-FB；多账户对比→P3/P5；OKKI周报→P6；Google询盘→P7；官网+明确要搜索广告方案/campaign JSON→W3；Meta Instant Form 线索广告→W13；仅要词表+搜索量/竞争度→W5；平台优化报告列表/推送→W7；对象仍不清→Read intent-routing.md。【账户】列表/余额/消耗/激活账单（W1）、多账户余额预警 balance-scan（P2）、多户消耗汇总 accounts-digest（P3）、五大媒体开户与进度（W2）、分享/解绑/MCC/BC/BM/权限（W9）。【投放】**搭建仅 Google+Meta**：Google Search/PMax/Demand Gen（W3，无 Display；Demand Gen 用 ad demand-gen；含 CRUD/PMax/batch W4）；Meta Instant Form（W13）。TikTok/Bing/Yandex **不能建广告**。另：拓词 W5、optimize W6。【财务】充值/钱包、转账记录、发票/开票/抬头（W8）；写操作审计与 restore。【运营】智能预警 forewarning 创建/启停/记录（W10）、TikTok/Meta 线索 clue（W11）、日周巡检（W12）、宿主编排/投放自控/异常监控（hosted-automation）。【其他】RAG 知识库检索、Meta/Facebook 周期与诊断 HTML、Google/Meta 周期 Excel、多账户 google-analysis-batch。
license: MIT
compatibility: 需要 Node.js 18+、已安装 siluzan-tso-cli，通过 send-login-code + login 或 config set 完成鉴权
metadata:
  requires: nodejs,siluzan-tso-cli
allowed-tools: Bash(siluzan-tso:*) Read Write
---
<!-- AUTO-GENERATED from SKILL.md.tmpl — edit .tmpl or snippets/, then: node scripts/gen-skill-docs.mjs -->

# Siluzan TSO Skill

本文件只做 **任务路由**：意图 → **唯一**工作流 → 按需 Read 子文档（参数与步骤不在此重复）。

- 分析 / 报告 → `references/core/playbooks.md`（P1–P10）
- 操作 / 管理 → `references/core/workflows.md`（W1–W13）
- 命令参数 → 路由表「必读文档」
- 通用纪律与沟通 → `references/core/agent-conventions.md`

> **加载**：按下方路由表 Read **一个**工作流卡片 + **一个**命令/报告 reference 后执行。写操作、报告交付、批量拉数、对用户写结论、或上下文被压缩时，再 Read `references/core/agent-conventions.md`（含 §十四沟通）。
>
> **报告 / 诊断 / 分析 / 拓词 / 转化成本·CPA·零询盘话术模糊**：先 Read `references/core/intent-routing.md`（含 **§零·D**：无 CRM 的转化巡检 → P3，不是 P7），再回路由表。数据任务一律 `--json-out` + 代码读盘（示例见 `references/core/tips.md`）。未指定格式时 P1/P4/P4-FB/P8/P9/P10 默认 **HTML**；**P6 默认 `okki-render` 出 5 Sheet `.xlsx`**、**P7 默认 8 Sheet `.xlsx`**（「表格形式」= xlsx，禁止 Markdown 表 / 手写 HTML / P6 Agent 手写 xlsx）。巡检类任务须交付摘要或显式失败原因。

---

## 基本使用

```bash
siluzan-tso -h
```

未安装 / 未登录 / 401 → Read `references/core/setup.md`。

**步骤**：① 报告类模糊 → Read `intent-routing.md` → ② 锁定下方**唯一**工作流行 → ③ Read 该行「必读文档」+ 工作流卡片 → ④ 按编号步骤执行；写操作前与用户确认；对用户写结论时 Read conventions §十四。**禁止** Read `report-templates/*.html`（由 CLI `render` 使用）。

---

## 即时规范

- `entityId`（UUID）≠ `mediaCustomerId`（`list-accounts` 的 `ma.mediaCustomerId`：Google/TikTok/Bing 多为数字；**Yandex=`porg-…`**；Meta 常带 `act_`，`balance`/`stats`/`balance-scan`/`accounts-digest` 裸数字会补前缀）。`stats`/`balance`/`accounts-digest`/`ad *` 的 `-a` **只传 mediaCustomerId**；空结果或 verbose 打出 403 时**先核验 ID**，禁止把 UUID/`entityId` 传给 `-a`，也**禁止**据此直接 `reauth`。
- **Google CID 特殊性**：UI 常写 `123-456-7890`（带连字符），平台 `mediaCustomerId` 为纯数字 `1234567890`。用户给了账户号时必须 `list-accounts -m Google -k <用户原样>`（带横杠也可，CLI 去连字符）；**禁止**无 `-k` 拉默认 20 条再判定未绑定/引导授权。`stats`/`balance`/`ad *`/`google-analysis` 的 `-a` 也可带横杠。**勿**把带横杠 403 误判为 OAuth 失效。
- **禁止臆测授权过期**：见 403/`HTTP 403`/拉数失败/「可能 OAuth 失效」时，**禁止**口头推断授权过期或直接 `reauth`。须先核验 ID（及 Google 连字符）。**`account check-access` 仅支持 Google**（无 `-m`，禁止对 TikTok/Meta/Bing/Yandex 调用）：Google 跑 `account check-access -a <mediaCustomerId>`，以 `accessible` / `reauth_required` / `no_permission` 为准；非 Google 看 `list-accounts` 的 `invalidOAuthToken`。仅当 `list-accounts` 输出含激活字段且可判定未激活时才跳过用其判断授权过期；细则见 `accounts-permissions.md`。
- **Google 广告命令名**：列表是 `ad campaigns`（不是 `ad-campaigns` / `campaign list`）；`balance`/`stats` 须带 `-m Google`；单国地域用 `ad geo search … --json-out`（或 `geo resolve`）。
- **广告搭建媒体边界**：仅 **Google**（`ad`，Search + PMax + Demand Gen）与 **Meta**（`meta-ad`，Instant Form 线索）。TikTok / BingV2 / Yandex **不能**创建或改广告结构；用户要搭建时须说明不支持，可改做账户分析（P4）或开户（W2）。**禁止**用 `ad` 冒充 Meta，**禁止**用 `meta-ad` 冒充 Google。Demand Gen 只用 `ad demand-gen`，不要用 `campaign-create` / `pmax-create`。
- **Google 广告类型边界**：CLI/Skill **仅支持** Google **搜索广告（Search）** 与 **Performance Max（PMax）** 的方案、创建与精细管理；**不支持展示广告（Display）**（含自适应展示广告 RDA、独立 Display 系列）。用户要做展示广告时须明确告知不支持，可改推 Search / PMax；**禁止**用 `campaign-create` / `ad-create` 伪装创建 Display。
- **删系列 / 测试系列须先问（硬性）**：「尽快创建 / 按方案搭建」不含删除授权。创建失败（政策违规、名称占用、半成品系列）时**禁止**自行建测试系列逐地域排查、**禁止**自行 `ad campaign-delete`（含 Agent 自建系列）；先报告原因与选项，用户同意后才带 `--i-confirm --commit`。也**禁止**为让创建通过而整类删减方案内容（否词/排除地域/投放国家）：按 `batch get` 的 `failedOperations[]` 只改报错项。见 `google-ads-write.md`「创建失败时禁止的做法」。
- **本轮试出来的半成品广告直接删（硬性）**：同一轮 `ad ad-create` 为排查拒审留下的短标题或残缺 RSA，正式广告通过后用 `ad ad-delete` 删掉，不要只 `ad-status Paused`。对用户报的条数以随后的 `ad list` 为准。系列和用户原有广告仍须先问。
- **创建完成后交付（硬性）**：`ad batch diff` 的 stdout 含 `BEGIN_USER_DELIVERY_MARKDOWN`…`END_USER_DELIVERY_MARKDOWN`——**立刻**把中间全文原样发给用户（可先于补建）；禁止只摘要、禁止只说「创建成功/详情已交付/未发现缺失」、禁止等全部补建结束再交付。
- **报告 render 成功即交付（硬性）**：`google-quarterly render`、`google-analysis render`、`google-ads-diagnosis render`、`website-diagnosis render`、`market-analysis render`，以及 Bing / TikTok / Yandex / Meta 的 `render`，stdout 给出 HTML 路径后**立刻**把该文件交给用户。P10 与各媒体周期报告封面的「季度 / 月度」已按日期写好（其余仍是「周期」或「账户」）。**禁止**再打开、grep 或修改这份 HTML，**禁止**为此再 render。用户没要 PDF 就不要 `html_to_pdf`；要了也只转一次，**禁止**再用 pdftotext、PyMuPDF、截图或视觉模型读 PDF/页面。细则见 `agent-conventions.md` §七。
- `list-accounts` 无余额/消耗；列全部用 `--page-size 999`。查单户必须 `-k`；`itemCount < total` 时**禁止**判定账户未绑定。
- 多户余额用 `balance-scan`（P2），多户消耗 / **转化成本·CPA 巡检**用 `accounts-digest`（P3，`--max-cpa`；**没有** `cpa-risk-scan`）。禁止外层 for-loop 逐户拉数。
- 全量扫描（`balance-scan` / `accounts-digest` / `guard` / `google-analysis-batch`）必带 `--json-out`。stdout 是 `state=paused` 时**还没扫完**：原样执行其中的 `resumeCommand`，重复到不再 paused 再交付；禁止交付半截结果，禁止加 `--fresh`。细则见 `references/core/agent-conventions.md` §八。
- **Google 多户巡检（含 D 组：CPA、零转化、余额续航、启用中有没有 PMax、启用但 0 展示）只跑一条** `accounts-digest -m Google --login-customer-id <MCC> --with-enabled-campaigns --start --end --json-out`。行上已有 `spend` / `cpa` / `balance` / `dailySpend` / `remainingDays` / `hasEnabledPmax` / `zeroImpressionEnabled`。**禁止**先 `list-accounts` 再把全部 ID 拼进 `-a`，**禁止** `--skip-balance` 后再 `balance-scan`，**禁止**逐户 `ad campaigns` 或把 `siluzan-tso` 写进 Python/bash。提示词若写了这些步骤，不要照做。只要「有没有 Display/PMax（含暂停）」才用 `--with-campaign-types`，并且不要和 `--with-enabled-campaigns` 一起开。
- `stats` 的 `spend` = **区间合计**，不是日消耗。
- 行业/市场报告禁止纯 WebSearch 当终稿；须 P9 `market-analysis collect`+`render`。
- **禁止编造平台网址**：给用户 `*.siluzan.com` / `mysiluzan.com` 链接前，**必须**当轮 `config show` 取 `webUrl`，路径**只**用已 Read 文档中的相对路径表拼接；CLI 输出的授权 URL **原样粘贴**；文档未给路径则**不拼链接**。细则见 `agent-conventions.md`。
- **W13 Meta 创建（硬性）**：首次落地只用 `meta-ad create`（会提交 `targeting_automation.advantage_audience`，默认 1）。`adset-edit` 不套这个默认值；读不到当前 `advantage_audience` 时停下，须显式 `--advantage-audience`。组失败用 `--json-out` 的 `campaignId` 跑 `adset-create`，**禁止**再 `campaign-create`。细定向写 `adset.flexibleSpec` 并设 `advantageAudience=0`。`BID_AMOUNT_REQUIRED` 停下，除非 JSON 已写 `adset.bidAmountOnRequired`。

---

## 媒体能力（搭建 vs 分析）

| 媒体 | 广告搭建 | 账户分析 | 说明 |
| ---- | -------- | -------- | ---- |
| **Google** | Search + PMax + Demand Gen（`ad`，W3/W4） | `google-analysis` | 不支持 Display |
| **MetaAd** | Instant Form 线索（`meta-ad`，W13） | `facebook-analysis` | 无视频 / Advantage+ / 系列列表 |
| **TikTok** | **不支持** | `tiktok-analysis` | 已有留资走 `clue`（W11） |
| **BingV2** | **不支持** | `bing-analysis` | 只读巡检 |
| **Yandex** | **不支持** | `yandex-analysis` | 只读巡检 |

## 路由表（意图 → 工作流 → 必读文档）

> 写操作 / 报告交付 / 批量拉数 / 对用户回复 → Read `agent-conventions.md`。找不到行 → 澄清或 Read `intent-routing.md`（勿整本加载 `references/README.md`）。

### 账户与财务

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 账户列表 / 有哪些 / 有多少 / 列出全部某媒体 | W1 | `references/accounts/accounts-list.md`（list-accounts） |
| 单户实时余额 | W1 | `references/accounts/accounts-balance-stats.md`（balance） |
| 多账户余额 / 续航不足预警 | **P2** | `references/accounts/accounts-balance-stats.md`（balance-scan） |
| 单户消耗 / 投放数据 | W1 / **P1** | `references/accounts/accounts-balance-stats.md`（stats） |
| 多账户消耗/对比汇总 / 转化成本·CPA·零转化巡检（无 CRM） | **P3** | `references/accounts/accounts-balance-stats.md`（accounts-digest）；消歧见 `intent-routing.md` **§零·D** |
| 激活/充值账单明细 | W1 | `references/accounts/accounts-list.md`（account-active-bills） |
| 开户（五大媒体）/ 开户进度 | W2 | `references/accounts/open-account-by-media.md`（**首次须列全必填项**；Google 加 `open-account-google-ui.md`） |
| 账户权限：分享/取消/解绑/重授权/MCC/BC/BM/关闭/提现/邮箱授权 | W9 | `references/accounts/accounts-permissions.md` |
| 充值 / 钱包 / 转账 / 发票 / 抬头 | W8 | `references/accounts/finance.md` |
| 审计 / 误操作恢复 | — | `references/accounts/write-audit-restore.md` |

### 不支持的广告搭建

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 建 TikTok / Bing / Yandex 广告 | — | **不支持搭建**。说明后可改做账户分析（P4）或开户（W2）；勿用 `ad` / `meta-ad` 伪装 |

### Google 广告投放

> **类型边界**：**Search** + **PMax** + **Demand Gen**；**不支持 Display（展示广告）**。详见 `references/google-ads/google-ads.md` Gotchas。

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 新建搜索系列 / 出投放方案 / Excel·表格方案 / 官网生成搜索广告 | **W3** | `references/google-ads/google-ads-campaign-plan.md`（§**仅出方案 vs 创建**）+ **`assets/campaign-create-template.json`**（先 Read）+ `assets/campaign-create-template.md` + `rules/google-ads-launch-plan-template.md`（JSON 后**写代码**投影完整审查稿）；有方案文件时加 `rules/google-ads-plan-source-fidelity.md`。**≠ P8 / ≠ P9 / ≠ W5**；**禁止**因缺账户阻塞出方案、**禁止**只交概览表 |
| Demand Gen / 需求开发 **创建·搭建·改预算·启停**（**不是**分析报告） | **W3** | `references/google-ads/demand-gen-api.md` + **`assets/demand-gen-create-template.json`**。只用 `ad demand-gen`。创建固定暂停；启用须用户同意且 `--confirm-enable --i-confirm`。**≠ Display ≠ PMax**。投放数据分析 / 汇总报告走 **P4-DG** |
| 展示广告 / Display / 自适应展示广告（RDA） | — | **不支持**。向用户说明后改推 Search、PMax 或 Demand Gen（W3）；勿创建、勿假装已支持 |
| 广告系列/组/广告/关键词 **查询** / 拒审字段 | W3 | `references/google-ads/google-ads-read.md` |
| 广告系列/组/广告/关键词 **创建·编辑·启停** | W3 | `references/google-ads/google-ads-write.md` |
| PMax 系列 | W3 | **`assets/pmax-create-template.json`**（先 Read）+ `assets/pmax-create-template.md` + `rules/google-ads-pmax-launch-plan-template.md`（**写代码**投影完整审查稿）+ `references/google-ads/pmax-api.md` + `google-ads-write.md`（PMax 节） |
| AI 智投草稿 list/get/update/publish | W4 | `references/google-ads/google-ads-batch.md` |
| 拓词 / keyword / 关键词规划 / 月搜索量 / 竞争度 / Keyword Planner | **W5** | `references/analytics/keyword-planner-workflows.md`（**§零·C**；客户背景先 `references/analytics/rag.md`） |
| AI 广告优化记录 / 建议 | W6 | `references/operations/optimize.md` |
| 优化/合规 SOP | W3 / W6 | `references/google-ads/rules/README.md`（**仅读索引表** → 再 Read **一个**具体 `rules/*.md`） |

### Meta 广告投放

> **类型边界**：仅 **Instant Form 线索广告**；无视频 / Advantage+ / 系列列表。拉已有线索走 **W11**；周期报告走 **P4-FB**。TikTok / Bing / Yandex **不能**走本表搭建。

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 新建 Meta/Facebook 线索广告 / Instant Form / 潜在客户表单投放 / **出 Facebook 线索方案或表格** | **W13** | `references/meta-ads/meta-ads.md` + **`assets/meta-lead-create-template.json`**（先 Read）+ `assets/meta-lead-create-template.md` + **`references/meta-ads/meta-lead-launch-plan-template.md`** + **`meta-ad plan-render`**（运营 4 Sheet xlsx，禁止 Agent 手写表）+ `references/meta-ads/meta-ads-write.md`。**≠ W11 ≠ P4-FB ≠ W3** |
| Meta 系列/组/广告 **查询**（按 ID）/ 主页 / 表单列表 | W13 | `references/meta-ads/meta-ads-read.md` |
| Meta 系列/组/广告 **创建·编辑·启停**（原语） | W13 | `references/meta-ads/meta-ads-write.md` |

### 分析与报告

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| Google 广告账户诊断 / 健康检查（**含账户 ID**） | **P1** | `references/analytics/account-analytics.md` + `report-templates/google-ads-diagnosis.md`（可选对照 `report-templates/google-account-diagnosis-report.md`） |
| Google 账户周期 **数据汇总**（只要花费/转化/9 章/Excel；**无**规划/客户版/大族） | **P4** | `report-templates/google-period-report.md` + `references/analytics/account-analytics.md`；Excel 加 `google-period-report-excel.md` |
| **Demand Gen / 需求开发投放数据分析、汇总报告**（客户与运营共用；**不是**创建广告） | **P4-DG** | `report-templates/demand-gen-analysis-report.md`；要 Excel 加 `demand-gen-analysis-report-excel.md`。HTML：`google-analysis demand-gen-render`。**≠ P4 全账户周期 ≠ W3 创建** |
| Google/谷歌 **月度报告** / **月总结与规划** / **季度报告** / **Q3 汇总** / **Q4 规划** / **季度汇报** / **投放季报** / 客户版 / 大族模板 / 下月规划（效率+区域询盘+国家明细） | **P10** | `report-templates/google-quarterly-report.md` + **`report-templates/google-quarterly-plan.md`**（**未带询盘表须先问并等待**，禁止不问就 collect；有表须先转 JSON 再 `--inquiries`，禁止把 xlsx 丢给 collect；`collect`+`render`；规划九章；花费三档基于本期、不是已批预算；**不做**行业数据；**render 成功立刻交付 HTML**，禁止改 HTML / 转 PDF / 截图验收） |
| Meta/Facebook 周期或诊断 | **P4-FB** | `report-templates/meta-period-report.md` + `assets/meta-period-report-rules.md` + `references/analytics/facebook-analysis-guide.md` |
| TikTok / Bing 周期报告 | **P4** | `references/analytics/account-analytics.md` + 对应 `report-templates/*-period-report.md` |
| Yandex 账户分析 / 周期 / 月报 | **P4** | `report-templates/yandex-period-report.md` + `references/analytics/account-analytics.md`；Excel 加 `yandex-period-report-excel.md` |
| 账户级按日 Excel | **P4-DAILY** | `report-templates/stats-daily-excel.md` |
| 多账户 × 多维度批处理 | **P5** | `references/analytics/google-analysis-batch.md` + `references/analytics/account-analytics.md` |
| OKKI 周报 / 表格形式（OKKI） | **P6** | `report-templates/okki-weekly-google-client.md`（写 `okki-weekly-report.json` → `google-analysis okki-render` 出 5 Sheet `.xlsx`；客户话术默认 7 条、一条一行；「表格形式」= Excel） |
| Google 询盘分析（**须 CRM 询盘资料**；口语零询盘/CPA → **P3**） | **P7** | `report-templates/google-inquiry-analysis.md` + `references/analytics/geo-continents.json` |
| 网址/域名/官网 + 诊断·检测·监测·报告 / **是否符合广告投放要求** / 能不能投 | **P8** | `references/core/intent-routing.md` §零 + `references/analytics/website-diagnosis-guide.md` + `assets/website-diagnosis-rules.md`（**必** `website-diagnosis collect`；**≠ P9 ≠ W3**；禁纯 WebFetch） |
| 市场/行业分析报告 / 战略市场 / KA 市场报告 | **P9** | `references/analytics/market-analysis-guide.md` + `assets/market-analysis-rules.md`（须 collect+render；**≠ P8**） |
| TSO 平台优化报告：列表/生成/推送 | W7 | `references/analytics/reporting.md` |
| RAG 知识库检索 | W5 | `references/analytics/rag.md` |

### 工具与运营

| 用户意图（关键词） | 工作流 | 必读文档 |
| ------------------ | ------ | -------- |
| 智能预警：创建/查询/启停/触发记录 | W10 | `references/operations/forewarning.md` |
| TikTok / Meta 线索表单 | W11 | `references/operations/clue.md` |
| 日/周巡检 | W12 | `references/core/workflows.md`（W12）+ `references/accounts/accounts-balance-stats.md`（交付物是 CLI 的 `userDelivery`，宿主 `present_files`） |
| 超预算熔断 / 空耗熔断（全户 Google） | — | `references/operations/guard.md`（`guard budget-circuit` / `guard zero-conv`；禁止逐户 for-loop） |
| Bing 自动化巡检（封禁/拒审/超预算/空耗预警） | — | `references/operations/hosted-automation-bing.md`（只读告警，不能自动暂停/改价） |
| Yandex 自动化巡检（归档/拒审/超预算/空耗预警） | — | `references/operations/hosted-automation-yandex.md`（只读告警，不能自动暂停/改价） |
| TikTok 自动化巡检（封禁/拒审/超预算/空耗预警） | — | `references/operations/hosted-automation-tiktok.md`（只读告警，不能自动暂停/改价） |
| Facebook / MetaAd 自动化巡检（封禁/拒审/超预算/空耗预警） | — | `references/operations/hosted-automation-facebook.md`（只读告警，不能自动暂停/改价） |
| 宿主编排 / 投放自控 / 异常监控 / 自动优化 | — | `references/operations/hosted-automation-user-catalog.md`（**仅当用户问自动化/巡检/熔断**；表内每行只 Read **一个** SOP；Google 熔断优先 guard.md；Bing/Yandex/TikTok/Facebook 走上四行） |

---

## Subagent 自主委派（可选）

宿主具备 Task / subagent 时：复杂报告或批处理（**P5 / P6 / P7**）、预计 CLI 输出很长 → Read `references/core/subagent-orchestration.md`；handoff 在 `snippets/handoff-p{5,6,7}-*.md`。写操作确认、`--commit`、401/`resume` 与最终交付留在主 Agent。

---

## 职责划分

| 本 Skill + CLI | 宿主 / 外部调度 |
| -------------- | --------------- |
| 结构化拉数（`--json-out`）、写命令语义、金额/ID 口径 | 触发时机、IF 决策、触达（钉钉/飞书）、批处理限速；可选 subagent 并行 |
