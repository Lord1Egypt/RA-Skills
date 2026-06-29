# Google 广告管理命令详解

> 所属 skill：`siluzan-tso`。

---

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

## 新建广告系列（方案 + 创建）

> **Search 流程与校验**：`references/google-ads/google-ads-campaign-plan.md`。本文件只写 **命令参数**（`campaign-validate` / `campaign-create` / `batch` 见下文各节）。

---

## 新建 Performance Max（PMax）

> **与 Search 隔离**：勿用 `campaign-create` 或 `campaign-create-template.json`。网关摘录见 `references/google-ads/pmax-api.md`。

| 步骤         | 命令                                                                                                                                                                                                    |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 模板         | 复制 `assets/pmax-create-template.json`，字段见 `assets/pmax-create-template.md`                                                                                                                        |
| **素材转换** | `siluzan-tso ad pmax-image-convert --input ./banner.jpg --output-dir ./assets --prefix <name> [--update-config ./pmax.json]`                                                                            |
| 地理 ID      | `siluzan-tso ad geo search -a <accountId> -q "<地区名>"`                                                                                                                                                |
| 校验         | `siluzan-tso ad pmax-validate --config-file ./pmax.json [--json-out ./snap-pmax]`（图片规格 + 文案超长 `lengthViolations`；超长勿自动截断，见 `references/google-ads/google-ads-campaign-plan.md` § 超长人工确认） |
| 创建         | `siluzan-tso ad pmax-create --config-file ./pmax.json [--json-out ./snap-pmax]`                                                                                                                         |
| 复核         | `siluzan-tso ad campaigns -a <accountId> --json-out ./snap` → `channelTypeV2` 为 `PERFORMANCE_MAX`                                                                                                      |

**PMax**：`ad pmax-create` **同步**返回 `campaignId`、`assetGroupId`、`budgetId`；无 `ad batch get/diff`。详见 `pmax-api.md`。

**金额**：JSON 中 `budget`、`targetCpa_BidingAmount` 填主币种**元**；CLI 提交前 ×100（与 `ad campaigns` 列表 `budget` 口径一致）。

**图片**：配置 `imagePaths`（相对 JSON 文件目录）或 `marketingImageBase64` / `squareMarketingImageBase64` / `logoImageBase64`。`pmax-validate` 会自动校验图片尺寸（最小值 / 推荐值 / 宽高比 ±2% / 文件大小 ≤5120 KB）。如需将任意图片转为合规素材，用 `ad pmax-image-convert`（`marketing` / `square` / `logo` 三种格式，sharp 处理，居中裁切）。

**视频**：`videoPath`（本地文件，经 `{googleApiUrl}/pyapi` 上传并轮询 `video_id` 后自动链接）与 `youtubeUrlOrId` **二选一**（创建时最多 1 条）；创建后追加更多视频用 `ad pmax-youtube-link`（单条）或 `ad pmax-assets-update`（批量，每资产组 ≤15 条）。

**禁止**：对已创建的 PMax 系列使用 `ad campaign-edit`（旧 PUT 会 **400**）。

### 已上线 PMax 管理（CLI）

| 能力             | 命令                                                                                                       |
| ---------------- | ---------------------------------------------------------------------------------------------------------- |
| 详情             | `ad pmax-get -a <id> --campaign-id <cid>`（读 `_brandGuidelinesActive`）                                   |
| 改活动           | `ad pmax-edit`（`--patch-file` 或 `--status` / `--budget` + `--budget-id`）                                |
| 改 Campaign 品牌 | `ad pmax-brand-assets-edit`（BG 已开启）                                                                   |
| 启用 BG          | `ad pmax-brand-guidelines-enable --config-file …`（存量活动）                                              |
| 新资产组         | `ad pmax-asset-group-create --config-file …`（BG 下自动省略品牌）                                          |
| 改资产组         | `ad pmax-asset-group-edit`                                                                                 |
| 删资产组         | `ad pmax-asset-group-edit --status REMOVED`（软删；网关无 DELETE 端点）                                    |
| 改资产           | `ad pmax-assets-update --config-file …`                                                                    |
| YouTube 追加     | `ad pmax-youtube-link`（单条 `--youtube` / `--video-path`）；批量见 `ad pmax-assets-update`                |
| 信号             | `ad pmax-signals-get` / `ad pmax-signals-set`；受众下拉 `ad pmax-audiences`                                |
| 附加资产         | `ad extension pmax-types`；`callout` / `snippet` / `lead-form` / `whatsapp`（见 `pmax-api.md` § 附加资产） |
| 图片库           | `ad pmax-image-upload`                                                                                     |
| 报表             | `ad pmax-report-asset-groups` / `ad pmax-report-geo`                                                       |
| 删活动           | `ad campaign-delete -a <id> --id <campaignId>`（与 Search 共用；勿用 `ad campaign-edit`）                  |

模板与 HTTP 对照：`references/google-ads/pmax-api.md`。

---

## 广告的编辑

已上线系列勿用 `campaign-create` 覆盖；改方案/重建见 **`references/google-ads/google-ads-campaign-plan.md`** § 已上线后的修改；分步 CRUD 用下文 `ad *-edit` 等，写后读命令复核。

### 广告新增

参考修改流程，将修改命令替换为新增命令。

### 广告优化

参考修改流程，增加新旧对照表格。

---

## ad campaigns — 广告系列管理

### 查询列表

```bash
siluzan-tso ad campaigns -a <accountId> [--start <YYYY-MM-DD>] [--end <YYYY-MM-DD>] [--json-out ./snap]
```

落盘 JSON 中 `budget` 为日预算（主币种「元」，CLI 已 ÷100），另有 `statusDisplay`（状态文案）。

### 启停

```bash
siluzan-tso ad campaign-status -a <accountId> --id <campaignId> --status <Enabled|Paused>
```

### 删除

```bash
siluzan-tso ad campaign-delete -a <accountId> --id <campaignId>
```

> 删除不可逆，建议先 `campaigns` 确认名称。

---

## 批量创建工作流（adgroup + keyword + ad + extension）

适用：从 Excel/JSON 任务清单一次性创建多个广告组及其内容。`adgroup-create` / `keyword-create` / `ad-create` / `extension <type>` 写命令均支持 **`--json-out`**，落盘响应里直接含 `id`，**无需**再 `ad groups --json-out ./snap` 反查。

**推荐节奏**（每广告组）：

```bash
# 1. 创建广告组 → 拿 adgroupId
out=$(siluzan-tso ad adgroup-create -a <accountId> \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --name "<adgroupName>" --max-cpc 2.0 --status ENABLED --json-out ./snap)
adgroupId=$(echo "$out" | jq -r '.id')

# 2. 添加关键词（已是单组批量，传逗号分隔关键词）
siluzan-tso ad keyword-create -a <accountId> \
  --adgroup-id "$adgroupId" --adgroup-name "<adgroupName>" \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --keywords "kw1,\"kw2\",[kw3]" --final-url "https://..." --json-out ./snap

# 3. 添加 RSA 广告
siluzan-tso ad ad-create -a <accountId> \
  --adgroup-id "$adgroupId" --adgroup-name "<adgroupName>" \
  --final-url "https://..." \
  --headlines "标题1,标题2,标题3,..." \
  --descriptions "描述1,描述2,..." \
  [--path1 <path1>] [--path2 <path2>] --json-out ./snap

# 4. 系列层 Sitelinks（每条 1 次调用，逐条循环）
for sitelink in "${SITELINKS[@]}"; do
  siluzan-tso ad extension sitelink -a <accountId> \
    --level Campaign --campaign-id <campaignId> \
    --text "..." --url "..." [--line2/--line3 ...] --json-out ./snap
done
```

**幂等性（Agent 侧）**：CLI 当前无 `--idempotent` 参数，请脚本侧先用 `ad groups --json-out ./snap` / `ad keywords --json-out ./snap` / `ad list --json-out ./snap` / `ad extension list --json-out ./snap` 取已有实体清单，按 `name + adgroupId` 等键过滤待创建项；HTTP 400 多半是重复创建，建议捕获并跳过。

**字符上限**（Agent 侧校验）：标题 ≤30、描述 ≤90、CALLOUT ≤25、Sitelink Text ≤25。CJK 字符按 2 计（Google 规范），`references/google-ads/rules/google-ads-compliance.md` 有详细规则。

---

## ad groups — 广告组管理

### 查询列表

```bash
siluzan-tso ad groups -a <accountId> [--start/--end <date>] [--json-out ./snap]
```

### 创建

```bash
siluzan-tso ad adgroup-create \
  -a <accountId> \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --name <adGroupName> --max-cpc <主币种金额> \
  [--status ENABLED|PAUSED] [--json-out <path>]
```

| 选项                     | 说明                                                               | 必填 |
| ------------------------ | ------------------------------------------------------------------ | ---- |
| `-a, --account <id>`     | Google mediaCustomerId                                             | ✅   |
| `--campaign-id <id>`     | 所属广告系列 ID                                                    | ✅   |
| `--campaign-name <name>` | 所属广告系列名称                                                   | ✅   |
| `--name <name>`          | 广告组名称                                                         | ✅   |
| `--max-cpc <amount>`     | 最高 CPC（主币种金额）                                             | ✅   |
| `--status`               | `ENABLED`（默认）/ `PAUSED`                                        |      |
| `--json-out`             | 输出网关返回的完整 adgroup 对象（含 `id` / `maxCPCAmountYuan` 等） |      |

**返回字段（--json-out）**：网关同步返回完整 adgroup，含 **`id`**（adgroupId）、`name`、`campaignId`、`statusV2`、`maxCPCAmountYuan`（元，CLI 已 ÷100）、`typeV2: "SEARCH_STANDARD"` 等 75+ 字段。批量创建脚本应直接读 `id`，**不需要**再次 `ad groups --json-out ./snap` 反查。

### 启停

```bash
siluzan-tso ad adgroup-status -a <accountId> --id <adGroupId> --status <Enabled|Paused>
```

### 编辑

先用 `ad groups --json-out ./snap` 查看当前值，再只改传入字段。

```bash
siluzan-tso ad adgroup-edit \
  -a <accountId> --id <adGroupId> \
  [--name <新名称>] [--max-cpc <主币种金额>] [--target-cpa <主币种金额>] \
  [--start/--end <YYYY-MM-DD>]
```

`--max-cpc` / `--target-cpa` 与 `ad groups --json-out ./snap` 中 `maxCPCAmountYuan` / `targetCpaAmountYuan` 对齐（**元**，CLI 出口已统一）。

### 删除

```bash
siluzan-tso ad adgroup-delete -a <accountId> --id <adGroupId>
```

---

## ad list — 广告创意管理

### 查询列表

```bash
siluzan-tso ad list -a <accountId> [--start/--end <date>] [--include-deleted] [--json-out ./snap]
```

`--include-deleted` 用于审计/排障，会多传 `readDeleted=true`。

### 拒审巡检（`--json-out`）

关注 `policyApprovalStatusV2`（`2`=不通过、`3`=受限）、`approvalStatusDetails`（`;` 分隔摘要）、`statusV2`（过滤 `Removed`）。同源也可用 `google-analysis --sections ads --json-out <dir>`。

### 创建（RSA）

```bash
siluzan-tso ad ad-create \
  -a <accountId> \
  --adgroup-id <adGroupId> --adgroup-name <adGroupName> \
  --final-url <url> \
  --headlines "标题1,标题2,标题3" \
  --descriptions "描述1,描述2" \
  [--path1 <≤15字符>] [--path2 <≤15字符>] \
  [--json-out <path>]
```

`--headlines` 至少 3 条（≤30字符），`--descriptions` 至少 2 条（≤90字符）。**`--json-out`** 落盘返回网关响应（含 `id` 等字段），便于批量脚本拿到 adId 后续编辑/启停。

### 启停 / 删除

```bash
siluzan-tso ad ad-status -a <accountId> --id <adId> --status <Enabled|Paused>
siluzan-tso ad ad-delete -a <accountId> --id <adId>
```

---

## ad keywords — 关键词管理

### 查询

```bash
siluzan-tso ad keywords -a <accountId> [--negative] [--start/--end <date>] [--json-out ./snap]
```

### 添加关键词

```bash
siluzan-tso ad keyword-create \
  -a <accountId> \
  --adgroup-id <adGroupId> --adgroup-name <adGroupName> \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --keywords "词1,词2,词3" [--final-url <url>] \
  [--json-out <path>]
```

`--json-out` 落盘 `{ request: { adgroupId, count }, response: ... }`，批量脚本可直接据此核对成功量。

### 否定关键词

```bash
# 添加（默认系列层级；传 --adgroup-id 则为组层级）
siluzan-tso ad keyword-negative-create \
  -a <accountId> \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --keywords "词1,词2" \
  [--adgroup-id <id> --adgroup-name <name>]

# 删除（先用 ad keywords --negative --json-out ./snap 获取 id）
siluzan-tso ad keyword-negative-delete -a <accountId> --id <negativeKeywordId>
```

---

## ad batch — 异步批量创建记录

```bash
siluzan-tso ad batch list [--state Creating|Successfully|Failed|HasFailed|Unpublished] [--customer-id <id>] [--start/--end <date>] [--json-out ./snap]
siluzan-tso ad batch get --id <recordId>
siluzan-tso ad batch update --id <recordId> [--budget <主币种>] [--url <url>] [--campaign-name <name>]
siluzan-tso ad batch publish --id <recordId>
```

`update` / `publish` 仅 `draftStatus === "Draft"` 可操作。

---

## keyword — 关键字推荐

多场景编排（竞品 URL + 种子、账户词叠市场指标、否词与建户表等）见 **`references/analytics/keyword-planner-workflows.md`**。

```bash
siluzan-tso keyword -k <搜索词> [--geo <geoTargetConstantIds>] [--url <url>] [--google-only] [--include <words>] [--exclude <words>] [--json-out <dir>]
siluzan-tso keyword geo-list [--country-code <US,CN,...>] [--name-contains <text>] [--json-out ./snap]
```

`--geo` 传多个 ID（如 `2840,2826`）时，返回的搜索量/CPC/竞争度为**跨所传地区的汇总数据**，响应中**无**按地区拆分的字段。若要分别查看各市场指标，须**多次调用**且每次 `--geo` **只传一个** ID（详见 **`references/analytics/keyword-planner-workflows.md`**「多地区 `--geo`」）。

`--url` 触发网址拓词（`websitereco`）并合并进结果；与 `--google-only` 互斥（仅 Google Keyword Planner 时用后者）。`--include`/`--exclude` 为本地过滤。仅 Google、不联网搜索的 Agent 编排见 **`references/analytics/keyword-planner-workflows.md`**「分支 B」。

---

## ad campaign-validate — 投放 JSON 校验

不提交 API；创建系列前**建议**跑。命令、选项、与 create 共用校验逻辑见 **`references/google-ads/google-ads-campaign-plan.md`** § 校验与创建（后端/Google 硬约束，不含关键词分层占比）。

**超长内容**：加 **`--json-out <dir>`**（推荐，与 create/batch 共用目录）或 `--json-out` 时响应含 `lengthViolations`（完整 `text` + JSON `path`）。Agent **勿自动截断**；须列出全部超长项与改写方案，用户确认后再改 JSON 并重跑 validate（流程见 `references/google-ads/google-ads-campaign-plan.md` § 超长人工确认）。

---

## ad campaign-create — 广告系列创建

**仅支持 JSON 配置文件**（`--config-file`）。JSON 字段名 **直接对齐后端契约**（外层 `CampaignCreationRecord`、内层 `campaign` 对应 `Samm.Domain.AdsAcctMgmt.Campaign`，**全部 PascalCase**）。CLI 不做字段重命名、camelCase 转换或结构展开。

- 默认：`draft: false` → 立即发布（`DraftStatus: Published`）
- `draft: true` → 仅保存草稿，需 `ad batch publish`

**步骤：**

- 模板：`assets/siluzan-ads/assets/campaign-create-template.json`（PascalCase 直通）
- 说明：`assets/siluzan-ads/assets/campaign-create-template.md`（逐字段含必填条件）

```bash
# 1. 复制模板并填写
#    - 外层：account / customerName / name / url / draft
#    - 内层 campaign：Name / Budget / BiddingStrategyTypeV2 / targetedLocations 等（PascalCase）
#    - 广告组在 campaign.AdGroupsForBatchJob 数组中
siluzan-tso ad campaign-create --config-file ./campaign.json

# 2. 查异步任务（Creating 时每 5–10s 轮询，直至非 Creating）
siluzan-tso ad batch get --id <taskId> --config-file ./campaign.json

# 3. 成功或部分成功后必做比对
siluzan-tso ad batch diff --batch-id <taskId> --config-file ./campaign.json
# 可选：--campaign-id <id>（ad campaigns -a <accountId> --json-out ./snap；省略时按系列名自动匹配）

# Failed：系列未创建，无需 diff；根据 get 的 reason/errors 改 JSON 后重提
# siluzan-tso ad campaign-create --config-file ./campaign.json
```

### 失败处理（Agent 必遵）

| `status`       | 含义     | 做法                                                                                                   |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------ |
| `Creating`     | 仍在执行 | 继续 `ad batch get`，勿重复 `campaign-create`                                                          |
| `Successfully` | 全部成功 | **须** `ad batch diff` 核对计划与账户一致（无缺失应 ✅）                                               |
| `Failed`       | 全部失败 | `ad batch get` 读 `reason`/`errors` → **只改 JSON** → 再 `ad campaign-create`（**不要** `batch diff`） |
| `HasFailed`    | 部分成功 | **须** `ad batch diff` 列出缺失 → 分步补建或删系列重提                                                 |

**`HasFailed` 分支：**

1. **多数广告组未建成**（`AdGroupsForBatchJob` 中多数项无 `Id`，默认 ≥50%）：  
   `ad campaign-delete -a <accountId> --id <campaignId>` → 按 `reason`/`errors` 修正 **campaign.json** → 重新 `ad campaign-create`。**不要**在脏系列上反复补建。

2. **仅少数组/资产失败**（系列与大部分组已有 `Id`）：
   - 缺组：`ad adgroup-create`（`--json-out` 取 `id`）
   - 缺词：`ad keyword-create`（词面格式同 JSON `KeywordsForBatchJob`）
   - 缺 RSA：`ad ad-create`（`--headlines` / `--descriptions` 从 JSON `AdsForBatchJob` 抄）  
     补建前可用 `ad groups` / `ad keywords` 核对账户现状。

**`ad batch diff` 比对维度：**系列是否存在 → 各 `AdGroupsForBatchJob[].Name` → 组内关键词（匹配类型+词面）→ RSA 首条标题 → 系列否定词 → 附加信息条数。默认按层级树状输出每条缺失的 **JSON 路径 + 计划内容 + 账户实况**；`--json-out` 可落盘完整结构。

**`ad batch get` 输出：**摘要表 + 后端原始 `reason` + 完整 `errors`（或 `--json-out` 整条记录）。

**CLI 在提交前只做三件事：**

1. 剥除 `_` 前缀注解键（如 `_meta`、`_comment_xxx`）；
2. 缺失 `googleDataRecordId` 时生成 UUID；
3. 把 `campaign` 子树内金额字段（`Budget`、`MaxCPCAmount`、`TargetSpend_BidCeilingAmount`、`TargetCpa_BidingAmount`、`MaxCpmAmount`、`MaxCPVAmount`、`TargetCpaAmount`、`MaxCPC`）从「元」深遍历 ×100 转为「分」。

**字段校验：**提交前自动执行 `runCampaignCreateValidation`（与 `ad campaign-validate` 相同）：后端镜像硬约束 + 词面/RSA/搜索网络等；关键词分层与匹配占比见 `google-ads-keyword-taxonomy.md`（仅 Agent 参考，CLI 不校验）。

**广告组：** 写在 `campaign.AdGroupsForBatchJob` 数组中（至少 1 项），字段名严格 PascalCase（`Name` / `MaxCPCAmount` / `KeywordsForBatchJob` / `AdsForBatchJob`）。详见 `campaign-create-template.md`。

**关键词匹配：** 写在 `KeywordsForBatchJob` 块内；同一块同匹配类型，`MatchTypeV2` 与 `KeywordText` 词面格式必须对齐（`PHRASE` 用 `"词"`、`EXACT` 用 `[词]`、`BROAD` 直写）。

广告组/关键词/创意的分步创建仍用 `adgroup-create`、`keyword-create`、`ad-create`。

---

## ad campaign-edit — 广告系列编辑

```bash
# 支持的策略枚举
siluzan-tso ad campaign-bidding-strategies [--json-out ./snap]

siluzan-tso ad campaign-edit \
  -a <accountId> --id <campaignId> \
  [--name <新名称>] [--budget <主币种>] [--bidding <策略>] \
  [--bid-ceiling <主币种>] [--target-cpa <主币种>] [--target-roas <倍数>] \
  [--manual-ecpc true|false] \
  [--search-network true|false] [--content-network true|false]
```

| `--bidding`            | 须配合                                 |
| ---------------------- | -------------------------------------- |
| `TARGET_SPEND`         | 可选 `--bid-ceiling`（0=不限）         |
| `MANUAL_CPC`           | 可选 `--manual-ecpc`                   |
| `TARGET_CPA`           | **必填** `--target-cpa`                |
| `TARGET_ROAS`          | **必填** `--target-roas`（2.5 = 250%） |
| `MAXIMIZE_CONVERSIONS` | 可选 `--target-cpa`（目标 CPA，元）    |

示例：

```bash
# 改为「尽可能争取更多点击次数」并设 CPC 上限 ¥3.5
siluzan-tso ad campaign-edit -a <accountId> --id <campaignId> \
  --bidding TARGET_SPEND --bid-ceiling 3.5

# 改为 tCPA = ¥80
siluzan-tso ad campaign-edit -a <accountId> --id <campaignId> \
  --bidding TARGET_CPA --target-cpa 80
```

相对运算：先 `ad campaigns --json-out ./snap` 读 `budget`（已为主币种元）、`biddingStrategyTypeV2`，再传入。

> PMax / 部分智能系列类型 Google 可能拒绝切换出价策略；以 API 返回错误为准。

---

## ad adgroup-rename — 广告组改名

```bash
siluzan-tso ad adgroup-rename -a <accountId> --id <adGroupId> --name <新名称>
```

---

## ad ad-edit — 广告创意编辑

先用 `ad list --json-out ./snap` 取得完整 JSON，再只修改传入字段，未改字段从列表原值带回。

`ad list --json-out ./snap` 关键字段映射：

- `headlinePart1~3` + `AddtionalHeadlines` → `--headlines`（≥3条）
- `adDescription`/`adDescription2` + `AddtionalAdDescriptions` → `--descriptions`（≥2条）
- `finalUrl` → `--final-url`；`path1`/`path2` → `--path1`/`--path2`
- `statusV2` → `--status`；`typeV2`（RSA=`RESPONSIVE_SEARCH_AD`）从列表保留勿手改

```bash
siluzan-tso ad ad-edit \
  -a <accountId> --id <adId> \
  [--headlines "标题1,标题2,..."] [--descriptions "描述1,描述2,..."] \
  [--final-url <url>] [--path1 <p1>] [--path2 <p2>] \
  [--status Enabled|Paused]
```

至少指定一项。

---

## ad keyword-delete — 搜索关键词删除

```bash
# 先查询获取 id 和 adGroupId
siluzan-tso ad keywords -a <accountId> --json-out ./snap
# 再删除
siluzan-tso ad keyword-delete -a <accountId> --id <keywordId> --adgroup-id <adGroupId>
```

---

## ad keyword-edit — 搜索关键词编辑

先用 `ad keywords --json-out ./snap` 取完整对象，再提交修改。`id` 可能与请求不一致，CLI 检测到变化会提示。

```bash
siluzan-tso ad keyword-edit \
  -a <accountId> --id <keywordId> \
  [--text <新关键词>] [--match-type Broad|Phrase|Exact] \
  [--max-cpc <n>] [--final-url <url>] [--status Enabled|Paused]
```

传 `--match-type` 时 CLI 自动规范 `keywordText` 括号/引号格式。至少传一项。`--max-cpc` 为主币种元（CLI ×100 写入 `maxCPC`「分」字段，与 `adgroup-edit --max-cpc` 同口径）。`ad keywords --json-out ./snap` 出价见 `maxCPCYuan`。`--status` 写入 `userStatusV2`（关键词级开关，非系列的 `statusV2`）。

---

## ad keyword-status — 搜索关键词状态切换

仅改 `userStatusV2`，走与 `keyword-edit` 相同的批量 PUT。与 `ad adgroup-status` 用法对称。

```bash
siluzan-tso ad keyword-status -a <accountId> --id <keywordId> --status <Enabled|Paused>
```

---

## ad keyword-negative-edit — 否词编辑

```bash
siluzan-tso ad keyword-negative-edit \
  -a <accountId> --id <negativeKeywordId> \
  [--text <新文本>] [--match-type Broad|Phrase|Exact]
```

传 `--match-type` 时 CLI 自动同步改写外层括号/引号。

---

## ad extension — 附加信息管理

Callout / Snippet / Sitelink / Call 等类型修改可**先删后建**；**Lead Form / WhatsApp** 支持 `ad extension update`（PUT；WhatsApp 成功后 **id 会变**）。所有 `extension <type>` 子命令均支持 `--json-out`，输出网关返回的扩展对象（含 `id`），批量脚本可据此回填。

```bash
# PMax 支持的类型与层级（含 LEAD_FORM）
siluzan-tso ad extension pmax-types [--json-out ./snap]

# 结构化摘要标头（按语言）
siluzan-tso ad extension snippet-headers [--json-out ./snap]

# 查询
siluzan-tso ad extension list -a <accountId> \
  [--type SITELINK|CALL|CALLOUT|STRUCTURED_SNIPPET|LEAD_FORM|BUSINESS_MESSAGE] \
  [--campaign-id <campaignId>] [--json-out ./snap]

# 附加链接
siluzan-tso ad extension sitelink -a <accountId> --text "文字" --url "https://..." \
  [--line2/--line3 <text>] [--level Account|Campaign|AdGroup] [--campaign-id <id>] [--json-out ./snap]

# 附加电话
siluzan-tso ad extension call -a <accountId> --country-code "+86" --phone "4008001234" \
  [--level Account|Campaign|AdGroup] [--json-out ./snap]

# 附加宣传信息（≤25字符）
siluzan-tso ad extension callout -a <accountId> --text "免费送货上门" [--level Account] [--json-out ./snap]

# 附加结构化摘要
siluzan-tso ad extension snippet -a <accountId> --header "Brands" --values "A,B,C" [--level Account] [--json-out ./snap]

# PMax 潜在客户表单（仅 Campaign 级；模板 assets/pmax-lead-form-template.json）
siluzan-tso ad extension lead-form -a <accountId> --config-file ./lead-form.json [--json-out ./snap]

# PMax WhatsApp 私信（BUSINESS_MESSAGE；需 Google API 白名单；模板 assets/pmax-whatsapp-template.json）
siluzan-tso ad extension whatsapp -a <accountId> --config-file ./whatsapp.json [--json-out ./snap]

# 更新 Lead Form 或 WhatsApp（配置文件含 leadForm / businessMessage；WhatsApp PUT 后 id 会变）
siluzan-tso ad extension update -a <accountId> --id <extensionId> --config-file ./lead-form.json

# 删除
siluzan-tso ad extension delete -a <accountId> --id <extensionId>
```

**PMax 约束**：仅 `Account` / `Campaign` 层级；`Ad Group` 会 400。`LEAD_FORM` 仅 Campaign。WhatsApp 每 Campaign 仅 1 个 ENABLED，须 Google API 白名单。

`--header` 常用值：`Brands`/`Services`/`Amenities`/`Types`/`Styles`/`Courses`/`Models` 等（完整列表：`ad extension snippet-headers`）。

**网关**：`ExtensionManagementController.cs` — `pmaxSupportedTypeList`、`structuredSnippetHeaders`、`extension/{accountId}` POST/PUT/DELETE。

---

## ad search-terms — 搜索字词报告

只读报告。屏蔽搜索词：先查到词，再用 `keyword-negative-create` 加否词。

```bash
siluzan-tso ad search-terms -a <accountId> [--start/--end YYYY-MM-DD] [--json-out ./snap]
```

---

## ad geo — 地理位置定向管理

```bash
# 搜索 locationId
siluzan-tso ad geo search -a <accountId> -q <地名>

# 查询已定向
siluzan-tso ad geo list -a <accountId> --mode targeted|excluded|report [--start/--end <date>]

# 添加定向
siluzan-tso ad geo add -a <accountId> --campaign-id <id> --location-id <id> [--bid-modifier 1.2] [--exclude]

# 修改已定向地区的出价调整（系列级 campaign_criterion）
siluzan-tso ad geo set-bid -a <accountId> --campaign-id <id> --location-id <id> --bid-modifier 1.2
# 或使用 list 返回的 criterion id
siluzan-tso ad geo set-bid -a <accountId> --campaign-id <id> --criterion-id <id> --bid-modifier 0.8

# 删除
siluzan-tso ad geo remove -a <accountId> --campaign-id <id> --location-id <id>
```

**`--bid-modifier` 口径（`add` / `set-bid` 均为 Google 倍率）**

| 倍率  | 含义     |
| ----- | -------- |
| `1.0` | 不调整   |
| `1.2` | 提高 20% |
| `0.8` | 降低 20% |

- `add`：写入 `PUT …/criterion/{account}` 时 CLI 会换算为后端百分比。
- `set-bid`：直接设置出价系数；与 `ad device-bid set`（系列级）同口径。
- `list` 返回的 `bidModifier` 为 Google **倍率**（如 `1.2` = +20%），不是百分比整数。

---

## ad device-bid — 设备出价调整

与 AI 优化「修改设备出价」能力同源。

| 级别             | 列表                                                                                    | 修改                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **系列**（默认） | `GET …/campaignmanagement/{id}/BidModifiers/Devices`                                    | `PUT …/campaigns/{campaignId}/Criteria/{criterionId}/BidModifier/{bidModifier}`        |
| **广告组**       | `GET …/adgroupnmanagement/bidmodifiers/{id}?campaignId&adgroupId&criteriaType=PLATFORM` | `PUT …/adgroupnmanagement/bidmodifiers/{id}?campaignId&adGroupId` + Body `Criterion[]` |

**`--bid-modifier` 口径（系列级直接透传 Google 倍率）**

| 倍率  | 含义                |
| ----- | ------------------- |
| `1.0` | 不调整              |
| `0.8` | 降低 20%            |
| `1.2` | 提高 20%            |
| `0`   | 排除该设备（-100%） |

广告组级会在 CLI 内将倍率转为后端百分比：`(倍率 - 1) × 100`。

```bash
# 系列级：账户下全部设备出价（可按系列过滤）
siluzan-tso ad device-bid list -a <accountId> [--campaign-id <id>] [--json-out ./snap]

# 广告组级
siluzan-tso ad device-bid list -a <accountId> --level adgroup --campaign-id <id> --ad-group-id <id> [--json-out ./snap]

# 修改系列设备出价（id 来自 list --json-out ./snap，或用 --device-type 自动匹配）
siluzan-tso ad device-bid set -a <accountId> --campaign-id <id> --device-type Mobile --bid-modifier 0.8

# 修改广告组设备出价
siluzan-tso ad device-bid set -a <accountId> --level adgroup --campaign-id <id> --ad-group-id <id> --device-type Desktop --bid-modifier 1.1
```

> 智能出价（tCPA/tROAS）可能覆盖设备出价调整；排除极差设备仍可用 `0`。
