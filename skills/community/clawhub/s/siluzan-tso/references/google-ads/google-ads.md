# Google 广告（导航）

> `SKILL.md` / 工作流已指向子文件时，**直接 Read 子文件**。本文件含共享 Gotchas。

## 支持的广告类型（硬边界）

| 类型                        | CLI / Skill   | 说明                                                                      |
| --------------------------- | ------------- | ------------------------------------------------------------------------- |
| **搜索广告（Search）**      | ✅ 支持       | 方案、`campaign-validate` / `campaign-create`、组/RSA/关键词 CRUD、扩展等 |
| **Performance Max（PMax）** | ✅ 支持       | `pmax-validate` / `pmax-create` 及存量 PMax 管理（见 `pmax-api.md`）      |
| **Demand Gen（需求开发）**  | ✅ 支持       | `ad demand-gen`（见 `demand-gen-api.md`）。不是 Display，也不是 PMax      |
| **展示广告（Display）**     | ❌ **不支持** | 含独立 Display 系列、自适应展示广告（RDA）等；**禁止**创建或伪装创建      |

用户明确要求展示广告时：如实告知不支持，可改推 Search 或 PMax；**禁止**用搜索系列 JSON / `ad-create`（RSA）冒充 Display。

Meta / Facebook 线索广告走 **`meta-ad`（W13）**，**禁止**用本命令族的 `ad`。TikTok / Bing / Yandex **没有**广告搭建命令。

> 账户内若已有 Display 系列，`ad campaigns` 等**只读列表**仍可能见到（`channelTypeV2` 含 `DISPLAY`）；本 Skill **不对**其做方案/创建/精细写管理。

## 何时 Read

| 任务                                        | Read                                                                   |
| ------------------------------------------- | ---------------------------------------------------------------------- |
| 查系列/组/创意/关键词/搜索词/地理           | [`google-ads-read.md`](google-ads-read.md)                             |
| 创建/编辑/启停/否词/附加信息/PMax/设备出价  | [`google-ads-write.md`](google-ads-write.md)                           |
| batch 流水线、`ad batch`、AI 智投草稿（W4） | [`google-ads-batch.md`](google-ads-batch.md)                           |
| 搜索系列 7 步方案与门禁                     | [`google-ads-campaign-plan.md`](google-ads-campaign-plan.md)           |
| PMax 网关路径                               | [`pmax-api.md`](pmax-api.md)                                           |
| Demand Gen 创建 / 修改 / 看数               | [`demand-gen-api.md`](demand-gen-api.md)                               |
| 优化/合规 SOP                               | [`rules/README.md`](rules/README.md)（只读索引 → 再读一个 rules 文件） |

## Gotchas

- **广告类型**：Search、PMax、Demand Gen。**不支持 Display**。Demand Gen 用 `ad demand-gen`，不要用 `campaign-edit` / `pmax-edit`。
- **Search 改字段**：`campaign-status`、`campaign-edit` 的名称/预算/出价/投放网络、`adgroup-status` / `adgroup-rename` / `adgroup-edit`、`keyword-status`、`keyword-edit` 的状态/出价/网址、`ad-status` / `ad-edit` 都是字段级 PATCH，只写本次参数。词面和匹配类型仍是批量 PUT。关闭搜索合作伙伴或展示网络传 `--search-network false` / `--content-network false`。PMax 用 `pmax-edit`，不要用 `campaign-edit`。
- **命令名**：系列列表是 `ad campaigns`（别名 `campaign-list`），**禁止** `ad-campaigns` / `campaign list`。`balance`/`stats` 须 `-m Google`。`adgroup-edit` / `keyword-edit` / `ad-edit` 没有 `--json-out`。`ad campaigns|groups|keywords|list` 没有 `--id`。
- **列表金额**：`ad campaigns` 的 `budget`、`targetSpendBidCeilingYuan`、`targetCpaAmountYuan` 是元，与 `--budget` / `--bid-ceiling` / `--target-cpa` 同口径。同对象的 `targetSpend_BidCeilingAmount`、`targetCpa_BidingAmount` 仍是分（`1` = 0.01 元），禁止填回写参数。`ad groups` 只读 `maxCPCAmountYuan` / `targetCpaAmountYuan`。`pmax-get` 的 `budget` 仍是分（`500` = 5 元），`pmax-edit --budget` 填元。`demand-gen list/get` 的 `budget` 也是分，看 `budgetYuan`；`demand-gen edit --budget` 和创建 JSON 填元。两套字段同时在时以 `*Yuan` 为准。
- **关键词改价回读**：`keyword-edit` 报「列表仍是」时，列表缓存约 60 秒且没有 `--fresh`。不要立刻重跑，不要删词重建。等约 60 秒再看 `maxCPCYuan`。`--max-cpc 0` 是清空并回到广告组出价。广告组 `--target-cpa 0` 同样是清空；`--max-cpc` 必须大于 0。
- **日期 500**：列表默认近 30 天。区间过长返回 500 且正文含 `authToken` 时，不是登录失效，缩短区间再查，不要据此 `reauth`。
- **Google 客户 ID（CID）带连字符**：UI / 用户口述常为 `123-456-7890`，平台 `mediaCustomerId` 与 Google 网关路径需要 `1234567890`。`ad campaigns` / `ad groups` / `ad list` 等 `-a` 与 JSON 顶层 `account` **可带连字符**（CLI 自动去掉）。若错误为 `HTTP 403：123-456-7890`（回显带横杠），先换纯数字重试，**禁止**据此直接判断 OAuth 过期或 `reauth`。
- **禁止臆测授权过期**：`ad *` / geo / 拉数出现 403/500 时，**禁止**对用户说「授权可能过期」。须核验 ID 后执行 `account check-access -a <mediaCustomerId>`，仅当 `reauth_required`（或与 `invalidOAuthToken=true` 交叉确认）才走重授权；无激活字段时禁止谈套餐。见 [`accounts-permissions.md`](../accounts/accounts-permissions.md)。
- **预算投放**：`BudgetBudgetDeliveryMethodV2` 默认用 `STANDARD`；`ACCELERATED` 多数账户会被 Google 拒（validate 警告）。
- **STRUCTURED_SNIPPET**：`StructuredSnippetHeaderValue.Key` 须为合法英文标头（`ad extension snippet-headers`）；`Features` 等非法值 validate 会拦（建议 `Amenities`）。
- **batch get**：读 `agentWorkflow`——无 `campaignId` 的 Failed/HasFailed **禁止**跑 `batch diff`，按 `agentHint` 改 JSON 重提。
- **创建失败不删系列、不试系列**：政策违规、名称占用、半成品系列残留时，**禁止**自行建测试系列逐地域排查或 `campaign-delete`；先报告并等用户选（见 [`google-ads-write.md`](google-ads-write.md)「创建失败时禁止的做法」）。删系列须用户同意 + `--i-confirm`。本轮 `ad ad-create` 试出来的残缺 RSA 用 `ad ad-delete` 清掉，不要只暂停。
- **失败只改报错项**：`batch get` 带 `--config-file` 时 `agentWorkflow.failedOperations[]` 把 `mutate_operations[N]` 映射到 JSON 路径；只改这些项，**禁止**整类清空否词/排除地域/投放国家后重提（见 [`rules/google-ads-plan-source-fidelity.md`](rules/google-ads-plan-source-fidelity.md)「创建失败后」）。
- **batch diff 交付**：把 stdout 中 `BEGIN_USER_DELIVERY_MARKDOWN`…`END`（或 `reportMarkdownFile`）**全文以 Markdown 发给用户**（先于补建）；**禁止**只说「未发现缺失 / 详情已交付」。
- `-a` 必须是 `list-accounts -m Google` 的 `ma.mediaCustomerId`，**禁止**传 `entityId`（UUID）。

## 金额单位（全局重要）

> **所有 CLI 金额参数均按「主币种金额」传入**（如 `1.5` = ¥1.50 / $1.50）；CLI 写入网关前对「分」字段 ×100（含 `ad keyword-edit --max-cpc` → `maxCPC`）。
> **禁止** 按 Google micros（×1,000,000）填写任何金额参数。

---

## ID 来源速查

| 需要的 ID           | 获取命令                                                                |
| ------------------- | ----------------------------------------------------------------------- |
| `accountId`（`-a`） | `siluzan-tso list-accounts --json-out ./snap` → `mediaCustomerId`       |
| 广告系列 `id`       | `siluzan-tso ad campaigns -a <accountId> --json-out ./snap` → `id`      |
| 广告组 `id`、`name` | `siluzan-tso ad groups -a <accountId> --json-out ./snap` → `id`、`name` |
| 广告 `id`           | `siluzan-tso ad list -a <accountId> --json-out ./snap` → `id`           |
| 关键词 `id`         | `siluzan-tso ad keywords -a <accountId> --json-out ./snap` → `id`       |

---
