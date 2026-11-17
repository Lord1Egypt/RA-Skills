# 工作流目录 · 操作 / 管理类（W1–W13）

> **范围**：调接口 / 写操作类业务（账户读取、开户、广告 CRUD、智投、拓词、优化、报告推送、财务、权限、预警、线索、巡检）。分析/报告类（拉数 → 撰稿 → 交付）见 `references/core/playbooks.md`（P1–P9）。
> **广告搭建**：仅 **W3**（Google Search/PMax）与 **W13**（Meta Instant Form）。TikTok / BingV2 / Yandex **没有**搭建工作流。
> **通用纪律见 `references/core/agent-conventions.md`**（写操作确认 + `--commit`、写后成败报告、ID 口径）；各卡片只写线性步骤。卡片字段：`触发 / 必读 / 步骤 / 产物`。完整参数表见「必读」指向的命令文档。

| 编号 | 业务                            | 必读                                                                                |
| ---- | ------------------------------- | ----------------------------------------------------------------------------------- |
| W1   | 账户查询（列表/余额/消耗/账单） | `references/accounts/accounts-list.md` + `accounts-balance-stats.md`                |
| W2   | 开户申请（五大媒体）            | `references/accounts/open-account-by-media.md`                                      |
| W3   | Google 广告创建与精细管理       | `google-ads-campaign-plan.md` + `google-ads-write.md` / `google-ads-read.md`        |
| W4   | AI 智投草稿 → 发布              | `references/google-ads/google-ads-batch.md`                                         |
| W5   | 拓词 / RAG                      | `references/analytics/keyword-planner-workflows.md` + `references/analytics/rag.md` |
| W6   | AI 广告优化记录查看与执行       | `references/operations/optimize.md`                                                 |
| W7   | TSO 优化报告生成 → 推送         | `references/analytics/reporting.md`                                                 |
| W8   | 财务：充值 / 转账 / 开票        | `references/accounts/finance.md`                                                    |
| W9   | 账户权限管理                    | `references/accounts/accounts-permissions.md`                                       |
| W10  | 智能预警规则管理                | `references/operations/forewarning.md`                                              |
| W11  | 广告线索提取                    | `references/operations/clue.md`                                                     |
| W12  | 日 / 周巡检                     | `references/accounts/accounts-balance-stats.md` + 各域                              |
| W13  | Meta Instant Form 线索广告      | `meta-ads.md` + **`meta-lead-launch-plan-template.md`** + `meta-ads-write.md` / `read` |

---

## W1 · 账户查询（列表 / 余额 / 消耗 / 账单）

- **触发**：账户列表/有多少、单户余额、单户消耗、激活充值账单。
- **必读**：`references/accounts/accounts-list.md` + `accounts-balance-stats.md`。
- **步骤**：
  1. 列表/数量：`list-accounts -m <媒体> --page-size 999 --json-out ./snap`，脚本读 `list-accounts-*.json` 的 `total` / `items[]`（**禁止**默认 20 条再翻页）。
  2. 单户余额：`balance -m <媒体> -a <mediaCustomerId>`（Yandex 用 `porg-…`，**不是** `entityId`）。
  3. 单户消耗：`stats -m <媒体> -a <mediaCustomerId> --start <S> --end <D>`（用户已给账户号则原样入 `-a`；空/`403` 先核验 ID，见 `accounts-balance-stats.md`；按日 Excel → **P4-DAILY**；多账户对比 → **P3**）。
  4. 激活账单：先取 `entityId` → `account-active-bills -m <媒体> --id <entityId> --json-out ./snap`。
- **产物**：多账户余额预警走 **P2**、消耗汇总走 **P3**。

---

## W2 · 开户申请（Google / TikTok / Yandex / BingV2 / MetaAd）

- **触发**：申请开户、新开广告账户、查开户进度。
- **必读**：`references/accounts/open-account-by-media.md`（各媒体必填业务项，**含 §「首次响应硬规范」：首次进入开户话题必须先列全必填清单；对用户禁止展示 CLI 参数名**）；Google 字段加 `references/accounts/open-account-google-ui.md`。所有媒体均**无需**手动查 magKey，CLI 按公司名自动创建/关联广告主组。
- **步骤**：
  1. 用业务语言列出必填项（勿贴 `--flag`）→ 收集资料（TikTok/Bing 需营业执照图片本地路径；CLI 无 OCR）。
  2. 前置查询（按需）：TikTok `open-account tiktok-areas/-industries/-timezones`；Bing `open-account bing-industries`；Google `open-account google-timezones`。
  3. 提交非交互命令 `open-account <media> …`（**禁用** `google-wizard`，需真实 TTY）。MetaAd 无表单，用 `open-account meta` 拉官方 OE 链接引导网页。
  4. 轮询审核：`account-history -m <媒体>`。
- **产物**：审核状态处理——

  | 状态       | 下一步                                                 |
  | ---------- | ------------------------------------------------------ |
  | `Pending`  | 等待，可反复轮询                                       |
  | `Approved` | `list-accounts` 确认账户出现 → 按 **W8** 引导充值激活  |
  | `Rejected` | 看落盘 `reason` 字段，改资料重提；原因不明引导联系客服 |

---

## W3 · Google 广告创建与精细管理

- **触发**：新建搜索系列、出投放方案、**按 Excel/表格投放方案创建**、**根据官网/网站/URL 生成 Google 搜索广告（含「表格格式」）**、搜索广告文案/关键词/计划表、系列/组/广告/关键词 CRUD、PMax、Demand Gen、拒审处理、日常调价/启停。
- **类型边界**：本工作流支持 Google **搜索广告（Search）**、**PMax**、**Demand Gen**；**不支持展示广告（Display）**（含 RDA / 独立 Display 系列）。用户要做展示广告 → 明确告知不支持，可改推 Search / PMax / Demand Gen；**禁止**用本卡片流程伪装创建 Display。Demand Gen 只用 `ad demand-gen`，见 `demand-gen-api.md`。
- **勿误判**：仅给官网 URL 且目标是「写/生成搜索广告」→ **本卡片（W3）**，不是 P8 网站诊断、不是 P9 市场分析；若用户只要拓词无系列结构 → **W5**。
- **仅出方案（默认优先）**：用户说「出方案 / 规划 / 表格 / 先别创建·开户·投钱」，或**未给账户且未要求创建** → 按 `google-ads-campaign-plan.md` §「仅出方案 vs 创建」：落盘 JSON + **写代码投影完整审查稿**（默认 MD；用户指定则 Excel 等），`account`=`[PENDING_ACCOUNT]`；**禁止**先要广告账户再开工；跳过 `list-accounts` / `geo resolve` / validate / create，直到用户确认创建。
- **必读**：方案与门禁 `references/google-ads/google-ads-campaign-plan.md` + **`assets/campaign-create-template.json`**（先 Read）+ `assets/campaign-create-template.md` + `rules/google-ads-launch-plan-template.md`；**有 Excel/表格方案时另读** `references/google-ads/rules/google-ads-plan-source-fidelity.md`；写命令参数 `references/google-ads/google-ads-write.md`；查询/拒审 `google-ads-read.md`；batch 补建 `google-ads-batch.md`；PMax 加 **`assets/pmax-create-template.json`** + `assets/pmax-create-template.md` + `rules/google-ads-pmax-launch-plan-template.md` + `references/google-ads/pmax-api.md`。
- **创建路径选择**：
  - 已有 AI 智投草稿 → 走 **W4**。
  - **PMax 出方案/创建** → **`assets/pmax-create-template.json`**（先 Read）+ `pmax-create-template.md` + `google-ads-pmax-launch-plan-template.md` + `pmax-api.md`：JSON →（创建阶段 `pmax-validate`）→ **写代码投影完整审查稿** → 用户确认 → `pmax-create`（**勿**用 Search `campaign-create`）。
  - **Demand Gen** → `demand-gen-api.md` + `assets/demand-gen-create-template.json`：`demand-gen conversions` → `validate` → 用户确认 → `create`。创建固定暂停。**勿**用 `campaign-create` / `pmax-create`，**勿**自行启用系列。
  - **用户给了 Excel/表格方案** → **方案源轨**：见 `google-ads-plan-source-fidelity.md`——Agent **写脚本**转 JSON；投影完整审查稿后停住或再创建；要创建再 **`ad geo resolve`** → validate → 确认 → create（**禁止**对话手填完整 JSON）。
  - 搜索系列从零出方案 → `google-ads-campaign-plan.md` + `google-ads-launch-plan-template.md`：JSON → 写代码投影审查稿；要创建再 `campaign-validate` → 用户确认 → `campaign-create`。
  - 已有完整结构化 JSON 且要创建 → validate → **写代码投影审查稿** → 用户确认 → create。
- **步骤（Search · 仅出方案，无账户）**：
  1. Read `campaign-create-template.json`；官网/RAG 归纳产品与落地页。
  2. 填系列/组/词/RSA/预算假设；`account`=`[PENDING_ACCOUNT]`；地域用国家名占位（勿编造 geo 数字 id）；JSON 落盘。
  3. **写代码**按 `google-ads-launch-plan-template.md` 从 JSON 投影完整审查稿（默认 MD；用户要表格则出 Excel）→ 交给用户；说明「选定账户后可继续 validate/create」。
  4. **停**；勿追问账户为前置条件；**禁止**只交概览表。
- **步骤（PMax 方案 → 创建）**：
  1. **创建阶段**账户：`list-accounts -m Google -k <id>`；落地页与品牌从官网/RAG 归纳。仅出方案跳过本步。
  2. 地域/语言：多国用 `ad geo resolve`，单国用 `ad geo search`；语言 id 写入 JSON。
  3. 复制 `pmax-create-template.json` 填文案/预算/图片并落盘；**必须**含 `campaignExtensions`（至少 callouts + structuredSnippets）；**Lead Gen/B2B 默认** `campaignExtensions.leadForm`。
  4. 创建阶段门禁：`ad pmax-validate --config-file ./pmax.json --json-out ./snap-pmax`。
  5. **写代码**按 `google-ads-pmax-launch-plan-template.md` 从 JSON 投影完整审查稿 → 用户审查确认 → `ad pmax-create --commit "…"`。
  6. 复核：`ad campaigns` / `ad pmax-get`；缺表单时 `ad extension lead-form` 补挂。
  7. **向用户交付创建详情**（系列名/`campaignId`、资产组/扩展是否齐全、失败原因）；禁止只说「已创建」。
- **步骤（Search · 方案文件 → 创建）**：
  1. Read `campaign-create-template.json`；Agent 写转换脚本读 Excel → 写出 `campaign.json`（匹配类型按方案分块）。
  2. `ad geo resolve -a <id> --from-file ./locations.json --json-out ./snap-geo`，把 id 写回 JSON。
  3. `ad campaign-validate`；**有不合规 → 询问「您自己改还是我帮您改？」**（见 `google-ads-plan-source-fidelity.md`）→ **写代码投影完整审查稿** → 用户确认 → `campaign-create` → `batch get` / `batch diff` / 自动补扩展 → **必出系列创建详情报告**；若 Agent 代改过 → 详情中**另附**修改表（创建清单 + 从 xxx→xxx + 原因）。
- **步骤（Search 一体化创建，无现成方案文件）**：0. **最小清单**（详见 `google-ads-campaign-plan.md` §创建前最小命令清单）：`list-accounts -m Google -k …` → `account check-access` → geo → validate → 审查稿 → create → `batch get`（看 `agentWorkflow`）→ **仅有 campaignId 时** `batch diff`。命令是 `ad campaigns`（禁 `ad-campaigns`/`campaign list`）；geo/ad 失败禁臆测授权过期；仅当列表输出含激活字段且未激活时才先处理激活。
  1. 地域：多国 `ad geo resolve --json-out`；单国 `ad geo search -a <id> -q "United States" --json-out`（读 `picked`/`targetedLocations`；仍禁止编造）。
  2. 门禁：`ad campaign-validate --config-file ./campaign.json --json-out …`（必跑；STRUCTURED_SNIPPET Key 须合法英文标头；ACCELERATED 预算看 warnings）。
  3. **写代码**按 `google-ads-launch-plan-template.md` 从 JSON 投影完整审查稿 → 用户确认。
  4. 创建：`ad campaign-create --config-file ./campaign.json`，记录返回 taskId。
  5. 轮询：`ad batch get --id <taskId> --config-file … --json-out …` 直至非 Creating；**读落盘 `agentWorkflow`**：`shouldRunBatchDiff===false` 或无 `campaignId` → **不要**跑 diff，按 `agentHint` 改 JSON 重提。
  6. **有 campaignId 时必做** `ad batch diff`（含投放国家）；`ok===false` / exit 2 时按 `missing[].remediateCommand` **自动** `ad geo add` / `ad extension *` 补建，勿反问用户（见 `google-ads-campaign-plan.md` § batch diff 后自动补建）。
  7. 复核：`ad campaigns` / `ad extension list` 确认系列与扩展齐全。
  8. **向用户发送 Markdown 创建详情**（硬性）：`ad batch diff … --lang <zh|en>` 后把 **`reportMarkdown` 全文**发给用户（`--md-out` / `reportMarkdownFile`）；多系列各一份；**禁止**只说「创建完成」。代改过方案时另附修改表（`google-ads-plan-source-fidelity.md`）。见 `agent-conventions.md` §四。
- **精细管理与日常运营**：`ad adgroup-create` / `ad keyword-create` / `ad keyword-negative-create` / `ad ad-create`（拓词辅助见 **W5**）；调整用 `ad adgroup-status` / `ad campaign-status` / `ad ad-delete` / `ad keyword-negative-delete`。完整参数见 `references/google-ads/google-ads-write.md`；列表复核见 `google-ads-read.md`。写后按 `agent-conventions.md` §四向用户汇报成败（改了什么、是否生效）。
- **产物**：系列（`ad campaigns` 可见）+ batch（`ad batch get` / `batch diff` 补齐扩展与地域）+ **面向用户的系列创建详情报告**；关键词匹配格式 `running shoes`=广泛 / `"..."`=词组 / `[...]`=精确；结构性写操作须用户确认；写后用成对读命令复核并汇报成败。

---

## W4 · AI 智投草稿 → 发布

- **触发**：查询/修改/发布 AI 智投（AICreation）已保存草稿。
- **必读**：`references/google-ads/google-ads-batch.md`。
- **步骤**：
  1. 列表找目标：`ad batch list --customer-id <mediaCustomerId>`（可 `--state Unpublished --json-out ./snap`）。
  2. 详情：`ad batch get --id <recordId>`。
  3. （可选）改字段（仅 `draftStatus=Draft` 可改）：`ad batch update --id <recordId> --budget … --campaign-name … --url …`。
  4. 发布：`ad batch publish --id <recordId>`。
  5. 跟踪：`ad batch list` 看 `Creating → Successfully / Failed`；成功后 `ad campaigns -a <id>` 验证；终态后按 **W3** / `agent-conventions.md` §四向用户交付系列创建详情（成功/失败项）。
- **产物**：草稿的**从零创建**须在网页向导完成，CLI 不支持；要纯 CLI 创建走 **W3**。发布前与用户确认；发布后须汇报成败明细。

---

## W5 · 拓词 / RAG

- **触发**：拓词、关键词规划、**Keyword Planner**、词包、否词线索；**月搜索量 / 竞争度 / 长尾关键词 / 核心词扩词**（见 `intent-routing.md` **§零·C**）；**阅读 URL/文章 + 针对核心词出 Google 词表**；或写文案/方案需客户产品背景。
- **必读**：`references/analytics/keyword-planner-workflows.md`；客户/品牌背景先 `references/analytics/rag.md`。
- **步骤**：
  1. （可选）WebFetch 读用户 URL/文章 **仅归纳种子词**；或 RAG：`rag list --rag-only --json-out ./snap` → `rag query … --json-out ./snap`。
  2. 拓词（**必 `--google-only`**，种子放进同一次 `-k`）：`keyword -k "种子1,种子2,..." [--url "<落地页>"] [--geo <id>] --google-only [--min-monthly-search <下限>]`。用户要有搜索热度时下限用 `1`。用户没点名国家时不要 `--geo`，也不要 `keyword geo-list`。
  3. 命令打印的表就是交付物（含 `montlySearch` / `averageCpc` / `competition`）。不要再写脚本按品牌洗词。某个种子没有量时只为它再补一次 `-k`。标注 **数据来源：Google Keyword Planner**。传了 `--geo` 时写明 **目标市场（不是全球）**，抄 `targetMarket.label`。
- **产物**：表格列含英文词、中文翻译、所属核心词、月搜索量、竞争度、**目标市场**（`targetMarket.label`，并写明不是全球）。指标**仅**来自 CLI；联网/文章语境与 Planner 指标**分列标注**；账户内 `google-analysis keywords` 表现**不可**与市场侧拓词合并。完整 campaign 见 **W3**。

---

## W6 · AI 广告优化记录查看与执行

- **触发**：查看 AI 优化建议/记录，并按建议执行。
- **必读**：`references/operations/optimize.md`；执行写操作参数见 `references/google-ads/google-ads-write.md`。
- **步骤**：
  1. 账户级列表（仍托管）：`optimize list -a <mediaCustomerId>`；**已脱管**改 `optimize list --match-media-customer-id <Google客户号> [--start …] --json-out ./snap` 取 `items[].id`。
  2. 系列级记录：`optimize records --start <S>`；明细 `optimize children --parent-id <id>`；单条 `optimize get --id <uuid>`。
  3. 按建议执行（如暂停低效组）：`ad adgroup-status … --status Paused`；加词 `ad keyword-create …`（写操作先确认）。
- **产物**：脱管账户**勿**依赖 `-a`（常 0 条）；优化建议的完整执行方案 CLI 不全提供，复杂项引导用户在平台优化详情页查看。

---

## W7 · TSO 优化报告生成 → 推送

- **触发**：TSO 平台「优化报告」列表/生成/删除、邮件推送配置与记录（**非** Agent 撰写的分析报告，那走 P1/P4）。
- **必读**：`references/analytics/reporting.md`。
- **步骤**：
  1. 账户：`list-accounts -m Google --json-out ./snap`。
  2. 生成：`report create -m Google -a <mediaCustomerId,...> -t Daily --start <S> --end <D>`（`-a` 传 mediaCustomerId）。
  3. 轮询：`report list -m Google --status true`，取 `viewUrl`（已含在输出，无需拼接）。
  4. 推送配置：`report push list/create/update/start/stop/delete`（`--media-accounts` 与 `--id` 传 **entityId**）；记录 `report push history`；历史收件箱 `report push receive-emails`。
  5. 清理：`report delete --ids id1,id2`。
- **产物**：删除/停推为写操作，先确认。查看链接拼接规则见 `reporting.md`。

---

## W8 · 财务：充值 / 转账 / 开票

- **触发**：充值、钱包、账户间转账、转账记录、开票、发票抬头。
- **必读**：`references/accounts/finance.md`。
- **步骤**：
  1. 充值/钱包：CLI 不支持；**当轮** `config show` 取 `webUrl`，仅按 `finance.md` 路径表拼接后贴完整链接（**禁止**凭记忆编 URL；Yandex 无充值页，引导联系客服）。
  2. 转账：记录 `transfer list -m <媒体>`；同媒体账户间 `transfer create -m <媒体> --out <id> --in <id> --amount <n>`（写操作先确认）。
  3. 开票：`invoice billable -m <媒体> -c <币种> --json-out ./snap` 取订单 `entityId` → 选发票抬头（`invoice-info list`，查重后再 `create`）→ `invoice apply --bill-ids … --invoice-type <PI|VATI|VATSI> …`。CNY 订单仅增值税票、外币仅 PI。
- **产物**：开票分步引导（先选订单、再选抬头、最后申请）；**禁止**不展示 `invoice billable` 就让用户手写 id；保留 CLI 币种校验。

---

## W9 · 账户权限管理

- **触发**：分享/取消分享、解绑、OAuth 重授权、Google MCC 绑定/解绑、TikTok BC 绑定/解绑、Meta BM 绑定、TikTok 关闭账户、Google 被封提现、Google 邮箱授权管理。
- **必读**：`references/accounts/accounts-permissions.md`（各 `account` 子命令参数与 ID 口径）。
- **步骤（按场景）**：
  - **分享**：`list-accounts --json-out` 取 `entityId` → `account share --id <entityId> --phone <手机号>`（`--phone` 裸 11 位补 `+86`，已有国家码则不补；见 `accounts-permissions.md` § share）；查 `account share-detail --customer-id <mediaCustomerId>`；取消 `account unshare --id <entityId> --account-id <userId>`。
  - **解绑**：`account delink --id <entityId> --i-confirm --commit "…"` / `--ids id1,id2`（缺 `--i-confirm` CLI 拒绝执行）。
  - **OAuth 重授权**：`invalidOAuthToken=true` → Siluzan Agent **优先**用平台重新授权工具（如 `present_reauth`）；备选 `list-accounts --json-out` 取 `ma.entityId` → **`account reauth -m <媒体> --id <entityId>`**（内置先 delink 再 OAuth）→ `list-accounts` 验证。**禁止**对失效账户直接用 `account auth`（首次「添加授权」专用）。
  - **首次 OAuth 添加授权**：Siluzan Agent **优先**用平台授权工具；备选 `account auth -m <媒体>`（无需先 delink）。
  - **MCC**：`account mcc-bind --customers <mediaCustomerId,...> --mcc <MCC客户ID>` / `mcc-unbind`（走 `googleApiUrl`，先 `config show`）。
  - **BC（TikTok）**：`account bc-bind --customers <id> --bc-ids <id>` / `bc-unbind --bc-id <id>`（解绑一次一个）。
  - **BM（Meta）**：`account bm-bind --account-id <mediaCustomerId> --bm-id <bmId>`。
  - **TikTok 关闭**：`account close --accounts <mediaCustomerId>`（不可自助撤销，谨慎）。
  - **Google 提现（被封账户）**：`account withdraw-list` 看可提现 → `account withdraw-submit --accounts <entityId,...>`。
  - **邮箱授权**：`account email-auth-list -c <mediaCustomerId>`；邀请 `account email-auth -c … --email … [--access-role …]`；撤销 `account email-deauth -c … --invitation-id … --resource-name …`。
- **产物**：解绑/取消分享/关闭/解绑 BC·MCC/撤销邮箱授权均为破坏性操作，须用户确认；注意 `entityId`（分享/解绑/提现）与 `mediaCustomerId`（MCC/BC/邮箱/关闭）的区分。账户激活需网页完成（见 **W8**）。

---

## W10 · 智能预警规则管理

- **触发**：创建/查询/启停/删除预警规则、查触发记录（默认不主动推荐，用户提出再用）。
- **必读**：`references/operations/forewarning.md`。
- **步骤**：
  1. 通知对象：`forewarning notify-accounts` 取微信对象 `entityId`（须已关注服务号）。
  2. 监控账户：`list-accounts -m <媒体> --json-out ./snap` 取账户 `entityId`。
  3. 创建（用户确认阈值/频率后）：`forewarning create -m <媒体> --name … --accounts <账户entityId> --field cost --operator GREATER_EQUALS --value <n> --notify <微信对象entityId> …`。
  4. 管理：`forewarning list` / `get` / `update`（全字段重传）/ `start` / `stop` / `delete`。
  5. 触发记录：`forewarning records -m <媒体> [--rule-id …] [--json-out ./snap]`（**不**做投放数据类日期反问）。
- **产物**：`--notify` 传**微信对象** entityId（非账户 entityId）；`--accounts` 传**账户** entityId。创建/更新/删除为写操作，先确认。

---

## W11 · 广告线索提取

- **触发**：拉取 TikTok / Meta 广告表单**已有**留资线索（不是新建表单投放；新建走 **W13**）。
- **必读**：`references/operations/clue.md`。
- **步骤**：
  1. 确认账户：TikTok `list-accounts -m TikTok`；Meta 取 Facebook 页面 ID。
  2. TikTok：`clue -m TikTok -a <advertiserId> [--region eu|us|other|ALL] --json-out ./snap`（「最近一周」直接按默认窗口执行，不做日期反问）。
  3. Meta：`clue -m Meta -a <pageId> --start <S> --end <D> --json-out ./snap`。
- **产物**：用户要原始 JSON 时**原样**贴 `--json-out` 的完整 JSON（含失败时的 `{"ok":false,...}`）；数据量大时落盘后脚本处理。

---

## W12 · 日 / 周巡检

- **触发**：日常/每周快速了解各媒体余额、消耗、预警与报告/智投状态。
- **必读**：`references/accounts/accounts-balance-stats.md`；首页看板口径见 `references/misc/tso-home.md`。Google 超预算/空耗熔断另读 `references/operations/guard.md`。Bing / Yandex / TikTok / Facebook 只读巡检读 `hosted-automation-bing.md` / `hosted-automation-yandex.md` / `hosted-automation-tiktok.md` / `hosted-automation-facebook.md`。
- **步骤**：
  1. 余额：`list-accounts -m <媒体> --json-out ./snap` → `balance -m <媒体> -a <mediaCustomerId,...>`（多户续航预警走 **P2**）。
  2. 消耗：多户汇总走 **P3** `accounts-digest`（Bing/Yandex **今天**不要用 `stats`）。Google 判断有没有 Display / PMax（含暂停），或用户要 `channelTypeV2` 时，加 `--with-campaign-types`。行上的 `campaignTypes`、`channelTypeV2`、`hasDisplay`、`hasPmax` 就是系列类型汇总。digest 成功后用本地脚本读 JSON、写 Excel。要「启用系列有没有 PMax」或「启用但 0 展示」时改加 `--with-enabled-campaigns`，并带上余额（不要 `--skip-balance`，不要再 `balance-scan`）。可加 `--login-customer-id`。**禁止**逐户 `ad campaigns` 或把 CLI 塞进 Python。提示词若把 `balance-scan` 或逐户 `ad campaigns` 写成编号步骤，仍以这一条为准。巡检不要给 `ad campaigns` 加 `--live`。
  3. Google 当日超预算/空耗熔断（若用户要求）：`guard budget-circuit` / `guard zero-conv -m Google --json-out`（**禁止**逐户 for-loop）。
  4. Bing 巡检（若用户要求）：按 `hosted-automation-bing.md` 跑封禁/拒审/当日超预算或空耗预警（只告警，不暂停）。
  5. Yandex 巡检（若用户要求）：按 `hosted-automation-yandex.md` 跑归档/拒审/当日超预算或空耗预警（只告警，不暂停）。
  6. TikTok 巡检（若用户要求）：按 `hosted-automation-tiktok.md` 跑封禁/拒审/当日超预算或空耗预警（只告警，不暂停）。
  7. Facebook / MetaAd 巡检（若用户要求）：按 `hosted-automation-facebook.md` 跑封禁/拒审/当日超预算或空耗预警（只告警，不暂停）。
  8. 预警触发：`forewarning records -m <媒体> --start <S>`（见 **W10**）。
  9. 智投/线索（按需）：`ad batch list --state Failed/HasFailed`（**W4**）、`clue …`（**W11**）、`optimize list/records`（**W6**）。
- **产物**：要与网页首页看板数字完全一致（聚合口径）时引导打开首页（`tso-home.md`）；CLI 给的是单账户粒度的近似巡检；Google 熔断须交付命中表或显式「无命中」；Bing/Yandex/TikTok/Facebook 巡检交付告警列表（不能写成已自动暂停）。

---

## W13 · Meta Instant Form 线索广告创建与精细管理

- **触发**：新建 Facebook / Meta 线索广告、Instant Form、潜在客户表单投放；改预算/定向/启停已有线索对象。
- **勿误判**：拉**已有**表单留资 → **W11** `clue -m Meta`；Meta 周期/诊断报告 → **P4-FB**；Google 搜索/PMax → **W3**。
- **必读**：`references/meta-ads/meta-ads.md` + **`assets/meta-lead-create-template.json`**（先 Read）+ `meta-lead-create-template.md` + **`references/meta-ads/meta-lead-launch-plan-template.md`** + `meta-ads-write.md` / `meta-ads-read.md`。
- **仅出方案**（「出方案 / 只要表格」、未给账户且未说创建）：跳过 list-accounts / pages；JSON 用 `[PENDING_ACCOUNT]` / `[PENDING_PAGE]` → `meta-ad plan-render` 出运营 4 Sheet xlsx + md → **停住等确认**。**禁止** Agent 手写 Facebook 方案 xlsx。
- **步骤（创建）**：
  1. `list-accounts -m MetaAd --page-size 999 --json-out ./snap` 取 `mediaCustomerId`。
  2. `meta-ad account` / `meta-ad pages`：记下币种与 `pageId`（`--json-out` 主页在 `items[]`，须含 `ADVERTISE`）。**HTTP 403** 或主页为空则停。`spend_capDisplay` ≈ `amount_spentDisplay` → 仍可 PAUSED 创建，ACTIVE 投不出去。
  3. 落盘同构 JSON（可执行字段 + `plan` 套系/矩阵/背书）。
  4. 门禁：`meta-ad validate --config-file ./meta-lead.json --json-out ./snap`。
  5. `meta-ad plan-render --config-file ./meta-lead.json --out ./meta-lead-plan.xlsx` → 用户确认（`--commit` 代替不了这步）。
  6. `meta-ad create --config-file ./meta-lead.json --json-out ./snap --commit "…"`（默认 PAUSED；失败读已建成 ID 用原语续跑）。报「支付方式」则停，不要重头 create。
  7. 按返回 ID `meta-ad campaign/adset/ad --id` 复核。
  8. 需要投放：三个对象 `*-status --status ACTIVE --commit`。清理：`DELETED`，顺序广告→组→系列。
- **定向**：`create` / `adset-create` 会提交 `targeting_automation.advantage_audience`（默认 `1`；有非空 `flexibleSpec` 时默认 `0`，也可 JSON/`--advantage-audience` 显式指定）。`adset-edit` 不套该默认值；读不到当前 `advantage_audience` 时停下，须显式 `--advantage-audience`。国家默认整表替换，追加用 `--countries-mode append`。审查稿兴趣可只写 `plan.targeting`；要打进网关则写 `adset.flexibleSpec`。
- **出价**：建组遇到 `BID_AMOUNT_REQUIRED` 时停下。要自动改成 bid cap，须事先写 `adset.bidAmountOnRequired`，金额单独填，不要用日预算代替。
- **失败续跑**：读 `--json-out` 已建成 ID 用原语续跑；**禁止**再 `campaign-create` / 重头 `create`。
- **产物**：审查稿路径（MD 或 xlsx）+ create 的 `formId` / `imageHash` / `campaignId` / `adSetId` / `creativeId` / `adId`；写后交代成败与是否仍为 PAUSED。
