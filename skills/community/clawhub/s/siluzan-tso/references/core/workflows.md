# 工作流目录 · 操作 / 管理类（W1–W12）

> **范围**：调接口 / 写操作类业务（账户读取、开户、广告 CRUD、智投、拓词、优化、报告推送、财务、权限、预警、线索、巡检）。分析/报告类（拉数 → 撰稿 → 交付）见 `references/core/playbooks.md`（P1–P9）。
>
> **通用纪律统一见 `references/core/agent-conventions.md`**（写操作确认 + `--commit`、ID 口径、数据处理协议），各卡片不再重复。**命令参数、字段口径以「必读」指向的域 reference 为唯一真相源，本文件只给线性步骤，不重复参数表。** 每张卡片结构统一：`触发 / 必读 / 步骤 / 交付与确认`。

| 编号 | 业务                            | 必读                                                                  |
| ---- | ------------------------------- | --------------------------------------------------------------------- |
| W1   | 账户查询（列表/余额/消耗/账单） | `accounts/accounts.md`                                                |
| W2   | 开户申请（六大媒体）            | `accounts/open-account-by-media.md`                                   |
| W3   | Google 广告创建与精细管理       | `google-ads/google-ads-campaign-plan.md` + `google-ads/google-ads.md` |
| W4   | AI 智投草稿 → 发布              | `google-ads/google-ads.md`（ad batch）                                |
| W5   | 拓词 / RAG                      | `analytics/keyword-planner-workflows.md` + `analytics/rag.md`         |
| W6   | AI 广告优化记录查看与执行       | `operations/optimize.md`                                              |
| W7   | TSO 优化报告生成 → 推送         | `analytics/reporting.md`                                              |
| W8   | 财务：充值 / 转账 / 开票        | `accounts/finance.md`                                                 |
| W9   | 账户权限管理                    | `accounts/accounts.md`（account 子命令）                              |
| W10  | 智能预警规则管理                | `operations/forewarning.md`                                           |
| W11  | 广告线索提取                    | `operations/clue.md`                                                  |
| W12  | 日 / 周巡检                     | `accounts/accounts.md` + 各域                                         |

---

## W1 · 账户查询（列表 / 余额 / 消耗 / 账单）

- **触发**：账户列表/有多少、单户余额、单户消耗、激活充值账单。
- **必读**：`accounts/accounts.md`。
- **步骤**：
  1. 列表/数量：`list-accounts -m <媒体> --page-size 999 --json-out ./snap`，脚本读 `list-accounts-*.json` 的 `total` / `items[]`（**禁止**默认 20 条再翻页）。
  2. 单户余额：`balance -m <媒体> -a <mediaCustomerId>`。
  3. 单户消耗：`stats -m <媒体> -a <mediaCustomerId> --start <S> --end <D>`（多账户对比走 **P3**）。
  4. 激活账单：先取 `entityId` → `account-active-bills -m <媒体> --id <entityId> --json-out ./snap`。
- **交付/确认**：多账户余额预警走 **P2**、消耗汇总走 **P3**。

---

## W2 · 开户申请（Google / TikTok / Yandex / BingV2 / Kwai / MetaAd）

- **触发**：申请开户、新开广告账户、查开户进度。
- **必读**：`accounts/open-account-by-media.md`（各媒体必填项与参数，**含 §「首次响应硬规范」：首次进入开户话题必须先列全必填清单**）；Google 字段加 `accounts/open-account-google-ui.md`。所有媒体均**无需**手动查 magKey，CLI 按公司名自动创建/关联广告主组。
- **步骤**：
  1. 列出必填项 → 收集资料（TikTok/Bing/Kwai 需营业执照图片本地路径；CLI 无 OCR）。
  2. 前置查询（按需）：TikTok `open-account tiktok-areas/-industries/-timezones`；Bing `open-account bing-industries`；Google `open-account google-timezones`。
  3. 提交非交互命令 `open-account <media> …`（**禁用** `google-wizard`，需真实 TTY）。MetaAd 无表单，用 `open-account meta` 拉官方 OE 链接引导网页。
  4. 轮询审核：`account-history -m <媒体>`。
- **交付/确认**：审核状态处理——

  | 状态       | 下一步                                                 |
  | ---------- | ------------------------------------------------------ |
  | `Pending`  | 等待，可反复轮询                                       |
  | `Approved` | `list-accounts` 确认账户出现 → 按 **W8** 引导充值激活  |
  | `Rejected` | 看落盘 `reason` 字段，改资料重提；原因不明引导联系客服 |

---

## W3 · Google 广告创建与精细管理

- **触发**：新建搜索系列、出投放方案、**根据官网/网站/URL 生成 Google 搜索广告（含「表格格式」）**、搜索广告文案/关键词/计划表、系列/组/广告/关键词 CRUD、PMax、拒审处理、日常调价/启停。
- **勿误判**：仅给官网 URL 且目标是「写/生成搜索广告」→ **本卡片（W3）**，不是 P8 网站诊断、不是 P9 市场分析；若用户只要拓词无系列结构 → **W5**。
- **必读**：方案与门禁 `google-ads/google-ads-campaign-plan.md` + **`assets/campaign-create-template.json`**（先 Read）+ `assets/campaign-create-template.md`；命令参数 `google-ads/google-ads.md`；PMax 加 **`assets/pmax-create-template.json`** + `assets/pmax-create-template.md` + `google-ads/pmax-api.md`。
- **创建路径选择**：
  - 已有 AI 智投草稿 → 走 **W4**。
  - **PMax 出方案/创建** → **`assets/pmax-create-template.json`**（先 Read）+ `pmax-create-template.md` + `pmax-api.md`：`pmax-validate` → 用户确认 → `pmax-create`（**勿**用 Search `campaign-create`）。
  - 搜索系列出方案 → `google-ads-campaign-plan.md`：JSON → `campaign-validate` → 用户确认 → `campaign-create`。
  - 已有完整结构化 JSON → 对应 validate → create。
- **步骤（PMax 方案 → 创建）**：
  1. 账户：`list-accounts -m Google -k <id>`；落地页与品牌从官网/RAG 归纳。
  2. 地域/语言：`ad geo search` 取 location id；语言 id 写入 JSON。
  3. 复制 `pmax-create-template.json` 填文案/预算/图片；**必须**含 `campaignExtensions`（至少 callouts + structuredSnippets）；**Lead Gen/B2B 默认** `campaignExtensions.leadForm`（方案 Markdown 须单列表单节）。
  4. 门禁：`ad pmax-validate --config-file ./pmax.json --json-out ./snap-pmax`。
  5. 输出 JSON + Markdown 方案 → 用户确认 → `ad pmax-create --commit "…"`。
  6. 复核：`ad campaigns` / `ad pmax-get`；缺表单时 `ad extension lead-form` 补挂。
- **步骤（Search 一体化创建）**：
  1. 地域 ID：`ad geo search -a <id> -q "United States"` 写入 `campaign.targetedLocations[].id`。
  2. 门禁：`ad campaign-validate --config-file ./campaign.json`（必跑）。
  3. 用户确认后创建：`ad campaign-create --config-file ./campaign.json`，记录返回 taskId。
  4. 轮询：`ad batch get --id <taskId>`（Creating → Successfully）。
  5. 复核：`ad campaigns -a <id> --json-out ./snap` 取 `campaignId` 供后续精细操作。
- **精细管理与日常运营**：`ad adgroup-create` / `ad keyword-create` / `ad keyword-negative-create` / `ad ad-create`（拓词辅助见 **W5**）；调整用 `ad adgroup-status` / `ad campaign-status` / `ad ad-delete` / `ad keyword-negative-delete`。完整参数见 `google-ads/google-ads.md`。
- **交付/确认**：关键词匹配格式 `running shoes`=广泛 / `"..."`=词组 / `[...]`=精确；结构性写操作（新建/暂停/删除）须用户确认；写后用成对读命令复核。

---

## W4 · AI 智投草稿 → 发布

- **触发**：查询/修改/发布 AI 智投（AICreation）已保存草稿。
- **必读**：`google-ads/google-ads.md` § ad batch。
- **步骤**：
  1. 列表找目标：`ad batch list --customer-id <mediaCustomerId>`（可 `--state Unpublished --json-out ./snap`）。
  2. 详情：`ad batch get --id <recordId>`。
  3. （可选）改字段（仅 `draftStatus=Draft` 可改）：`ad batch update --id <recordId> --budget … --campaign-name … --url …`。
  4. 发布：`ad batch publish --id <recordId>`。
  5. 跟踪：`ad batch list` 看 `Creating → Successfully / Failed`；成功后 `ad campaigns -a <id>` 验证。
- **交付/确认**：草稿的**从零创建**须在网页向导完成，CLI 不支持；要纯 CLI 创建走 **W3**。发布前与用户确认。

---

## W5 · 拓词 / RAG

- **触发**：拓词、关键词规划、词包、否词线索；或写文案/方案需客户产品背景。
- **必读**：`analytics/keyword-planner-workflows.md`；客户/品牌背景先 `analytics/rag.md`。
- **步骤**：
  1. （需背景时）RAG：`rag list --rag-only --json-out ./snap` → `rag query -q "型号 英文类目 应用场景" --folder-id <id> --partition wiki --top-k 12 --json-out ./snap`，归纳 2–8 个种子词。
  2. 拓词：`keyword -k "种子1,种子2,..." [--geo <id>] [--url <落地页>] [--google-only] --json-out ./snap-kw`（仅 Google 数据加 `--google-only`；分市场对比每次只传一个 `--geo`）。
  3. 脚本读落盘 `items`（`montlySearch`/`averageCpc`/`competition`，币种见 `bidAmountCurrency`）→ 去重/洗词/分组/截 Top N，标注数据来源。
- **交付/确认**：联网搜索词与 Google Planner 指标**分列标注**，不混为一谈；账户内 `google-analysis keywords` 表现**不可**与市场侧拓词合并。落地否词/建户见 **W3**。

---

## W6 · AI 广告优化记录查看与执行

- **触发**：查看 AI 优化建议/记录，并按建议执行。
- **必读**：`operations/optimize.md`；执行写操作参数见 `google-ads/google-ads.md`。
- **步骤**：
  1. 账户级列表（仍托管）：`optimize list -a <mediaCustomerId>`；**已脱管**改 `optimize list --match-media-customer-id <Google客户号> [--start …] --json-out ./snap` 取 `items[].id`。
  2. 系列级记录：`optimize records --start <S>`；明细 `optimize children --parent-id <id>`；单条 `optimize get --id <uuid>`。
  3. 按建议执行（如暂停低效组）：`ad adgroup-status … --status Paused`；加词 `ad keyword-create …`（写操作先确认）。
- **交付/确认**：脱管账户**勿**依赖 `-a`（常 0 条）；优化建议的完整执行方案 CLI 不全提供，复杂项引导用户在平台优化详情页查看。

---

## W7 · TSO 优化报告生成 → 推送

- **触发**：TSO 平台「优化报告」列表/生成/删除、邮件推送配置与记录（**非** Agent 撰写的分析报告，那走 P1/P4）。
- **必读**：`analytics/reporting.md`。
- **步骤**：
  1. 账户：`list-accounts -m Google --json-out ./snap`。
  2. 生成：`report create -m Google -a <mediaCustomerId,...> -t Daily --start <S> --end <D>`（`-a` 传 mediaCustomerId）。
  3. 轮询：`report list -m Google --status true`，取 `viewUrl`（已含在输出，无需拼接）。
  4. 推送配置：`report push list/create/update/start/stop/delete`（`--media-accounts` 与 `--id` 传 **entityId**）；记录 `report push history`；历史收件箱 `report push receive-emails`。
  5. 清理：`report delete --ids id1,id2`。
- **交付/确认**：删除/停推为写操作，先确认。查看链接拼接规则见 `reporting.md`。

---

## W8 · 财务：充值 / 转账 / 开票

- **触发**：充值、钱包、账户间转账、转账记录、开票、发票抬头。
- **必读**：`accounts/finance.md`。
- **步骤**：
  1. 充值/钱包：CLI 不支持，`config show` 取 `webUrl` 后按 `finance.md` 给对应媒体充值页链接（Yandex/Kwai 无充值页，引导联系客服）。
  2. 转账：记录 `transfer list -m <媒体>`；同媒体账户间 `transfer create -m <媒体> --out <id> --in <id> --amount <n>`（写操作先确认）。
  3. 开票：`invoice billable -m <媒体> -c <币种> --json-out ./snap` 取订单 `entityId` → 选发票抬头（`invoice-info list`，查重后再 `create`）→ `invoice apply --bill-ids … --invoice-type <PI|VATI|VATSI> …`。CNY 订单仅增值税票、外币仅 PI。
- **交付/确认**：开票分步引导（先选订单、再选抬头、最后申请）；**禁止**不展示 `invoice billable` 就让用户手写 id；保留 CLI 币种校验。

---

## W9 · 账户权限管理

- **触发**：分享/取消分享、解绑、OAuth 重授权、Google MCC 绑定/解绑、TikTok BC 绑定/解绑、Meta BM 绑定、TikTok 关闭账户、Google 被封提现、Google 邮箱授权管理。
- **必读**：`accounts/accounts.md`（各 `account` 子命令参数与 ID 口径）。
- **步骤（按场景）**：
  - **分享**：`list-accounts --json-out` 取 `entityId` → `account share --id <entityId> --phone <手机号>`；查 `account share-detail --customer-id <mediaCustomerId>`；取消 `account unshare --id <entityId> --account-id <userId>`。
  - **解绑**：`account delink --id <entityId>` / `--ids id1,id2`。
  - **OAuth 重授权**：`invalidOAuthToken=true` → `account auth -m <媒体>`（浏览器授权）→ `list-accounts` 验证。
  - **MCC**：`account mcc-bind --customers <mediaCustomerId,...> --mcc <MCC客户ID>` / `mcc-unbind`（走 `googleApiUrl`，先 `config show`）。
  - **BC（TikTok）**：`account bc-bind --customers <id> --bc-ids <id>` / `bc-unbind --bc-id <id>`（解绑一次一个）。
  - **BM（Meta）**：`account bm-bind --account-id <mediaCustomerId> --bm-id <bmId>`。
  - **TikTok 关闭**：`account close --accounts <mediaCustomerId>`（不可自助撤销，谨慎）。
  - **Google 提现（被封账户）**：`account withdraw-list` 看可提现 → `account withdraw-submit --accounts <entityId,...>`。
  - **邮箱授权**：`account email-auth-list -c <mediaCustomerId>`；邀请 `account email-auth -c … --email … [--access-role …]`；撤销 `account email-deauth -c … --invitation-id … --resource-name …`。
- **交付/确认**：解绑/取消分享/关闭/解绑 BC·MCC/撤销邮箱授权均为破坏性操作，须用户确认；注意 `entityId`（分享/解绑/提现）与 `mediaCustomerId`（MCC/BC/邮箱/关闭）的区分。账户激活需网页完成（见 **W8**）。

---

## W10 · 智能预警规则管理

- **触发**：创建/查询/启停/删除预警规则、查触发记录（默认不主动推荐，用户提出再用）。
- **必读**：`operations/forewarning.md`。
- **步骤**：
  1. 通知对象：`forewarning notify-accounts` 取微信对象 `entityId`（须已关注服务号）。
  2. 监控账户：`list-accounts -m <媒体> --json-out ./snap` 取账户 `entityId`。
  3. 创建（用户确认阈值/频率后）：`forewarning create -m <媒体> --name … --accounts <账户entityId> --field cost --operator GREATER_EQUALS --value <n> --notify <微信对象entityId> …`。
  4. 管理：`forewarning list` / `get` / `update`（全字段重传）/ `start` / `stop` / `delete`。
  5. 触发记录：`forewarning records -m <媒体> [--rule-id …] [--json-out ./snap]`（**不**做投放数据类日期反问）。
- **交付/确认**：`--notify` 传**微信对象** entityId（非账户 entityId）；`--accounts` 传**账户** entityId。创建/更新/删除为写操作，先确认。

---

## W11 · 广告线索提取

- **触发**：拉取 TikTok / Meta 广告表单留资线索。
- **必读**：`operations/clue.md`。
- **步骤**：
  1. 确认账户：TikTok `list-accounts -m TikTok`；Meta 取 Facebook 页面 ID。
  2. TikTok：`clue -m TikTok -a <advertiserId> [--region eu|us|other|ALL] --json-out ./snap`（「最近一周」直接按默认窗口执行，不做日期反问）。
  3. Meta：`clue -m Meta -a <pageId> --start <S> --end <D> --json-out ./snap`。
- **交付/确认**：用户要原始 JSON 时**原样**贴 `--json-out` 的完整 JSON（含失败时的 `{"ok":false,...}`）；数据量大时落盘后脚本处理。

---

## W12 · 日 / 周巡检

- **触发**：日常/每周快速了解各媒体余额、消耗、预警与报告/智投状态。
- **必读**：`accounts/accounts.md`；首页看板口径见 `references/misc/tso-home.md`。
- **步骤**：
  1. 余额：`list-accounts -m <媒体> --json-out ./snap` → `balance -m <媒体> -a <mediaCustomerId,...>`（多户续航预警走 **P2**）。
  2. 消耗：`stats -m <媒体> -a <id> --start <昨天/上周一> --end <昨天/上周日>`（多户汇总走 **P3**）。
  3. 预警触发：`forewarning records -m <媒体> --start <S>`（见 **W10**）。
  4. 智投/线索（按需）：`ad batch list --state Failed/HasFailed`（**W4**）、`clue …`（**W11**）、`optimize list/records`（**W6**）。
- **交付/确认**：要与网页首页看板数字完全一致（聚合口径）时引导打开首页（`tso-home.md`）；CLI 给的是单账户粒度的近似巡检。
