# Google 广告 · 写入与编辑

> 流程见 `workflows.md` **W3**。金额/ID 口径见 [google-ads.md](google-ads.md)。
> **何时 Read**：创建/编辑/启停/删词/附加信息/设备出价/PMax；写操作须用户确认与 `--commit`。

## Contents

- 新建搜索系列 / PMax
- campaign-validate / campaign-create / campaign-edit
- **ad ad-create（RSA）** / ad-edit / 组/关键词写操作
- extension / device-bid

---

## 支持范围

- ✅ **搜索广告（Search）**：`campaign-validate` / `campaign-create`、组/关键词、`ad-create`（RSA）等
- ✅ **Performance Max（PMax）**：`pmax-validate` / `pmax-create` 及存量 PMax 写命令（见 `pmax-api.md`）
- ✅ **Demand Gen**：`ad demand-gen`（见 `demand-gen-api.md`）。创建固定暂停。启用系列必须 `--confirm-enable --i-confirm`
- ❌ **展示广告（Display）**：**不支持**创建与精细管理（含 RDA）；用户要 Display 时须说明不支持并改推 Search / PMax / Demand Gen，**禁止**伪装创建

---

## 写操作硬纪律（Agent 易踩）

- **必须** `--commit "…"`；漏了会直接失败。
- 列表命令：`ad campaigns` / `ad groups` / `ad list` / `ad keywords`（**没有** `google-ads`、没有必用 `campaign-list`；`campaign-list` 仅为 `campaigns` 别名）。这四条**没有** `--id`，单条在落盘 JSON 里按 `id` 过滤。
- `--json-out <path>`：**路径必填**，JSON 落盘；禁止 `--json-out` 裸用或管道 stdout。`adgroup-edit`、`keyword-edit`、`ad-edit` **没有**这个参数，加上会在请求发出前失败。核对用对应列表。
- 系列 `statusDisplay` 含「投放期已结束」≠ 已删除；以 JSON **`statusV2`** 为准（见 `google-ads-read.md`）。
- **勿创建 Display**：`campaign-create` / `ad-create` 仅面向 Search（RSA）；PMax 走 `pmax-*`；Demand Gen 走 `ad demand-gen`。

---

## 金额单位（全局重要）

> **所有 CLI 金额参数均按「主币种金额」传入**（如 `1.5` = ¥1.50 / $1.50）；CLI 写入网关前对「分」字段 ×100（含 `ad keyword-edit --max-cpc` → `maxCPC`）。
> **禁止** 按 Google micros（×1,000,000）填写任何金额参数。

---

## ID 来源速查

| 需要的 ID                            | 获取命令                                                                                                                               |
| ------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------- |
| `accountId`（`-a`） / JSON `account` | `list-accounts -m Google` → `mediaCustomerId`（纯数字；UI 带连字符 CID 可传入，CLI 去横杠，见 [google-ads.md](google-ads.md) Gotchas） |
| 广告系列 `id`                        | `siluzan-tso ad campaigns -a <accountId> --json-out ./snap` → `id`                                                                     |
| 广告组 `id`、`name`                  | `siluzan-tso ad groups -a <accountId> --json-out ./snap` → `id`、`name`                                                                |
| 广告 `id`                            | `siluzan-tso ad list -a <accountId> --json-out ./snap` → `id`                                                                          |
| 关键词 `id`                          | `siluzan-tso ad keywords -a <accountId> --json-out ./snap` → `id`                                                                      |

---

## 新建广告系列（方案 + 创建）

> **Search 流程与校验**：`references/google-ads/google-ads-campaign-plan.md`。审查稿结构：`rules/google-ads-launch-plan-template.md`（JSON 落盘后 Agent **写代码**投影完整审查稿，用户确认再 create）。本文件只写 **命令参数**（`campaign-validate` / `campaign-create` / `batch` 见下文各节）。

---

## 新建 Demand Gen

> **与 Search / PMax 隔离**：只用 `ad demand-gen`。网关与硬规则见 `references/google-ads/demand-gen-api.md`。模板 `assets/demand-gen-create-template.json`。金额填元。创建结果永远是暂停，不要启用，除非用户明确要花钱。

| 步骤 | 命令 |
| ---- | ---- |
| 能否按转化出价 | `ad demand-gen conversions -a <accountId>`。没有可出价询盘就用 `TARGET_SPEND` |
| 最低预算 | `ad demand-gen minimum-budget -a <accountId>` |
| 地域 | `ad geo search -a <accountId> -q "<地区名>"` |
| 校验 | `ad demand-gen validate -a <accountId> --config-file ./dg.json` |
| 创建 | `ad demand-gen create -a <accountId> --config-file ./dg.json` |
| 读回 | `ad demand-gen get -a <accountId> --campaign-id <id>` |

---

## 新建 Performance Max（PMax）

> **与 Search 隔离**：勿用 `campaign-create` 或 `campaign-create-template.json`。网关摘录见 `references/google-ads/pmax-api.md`。

| 步骤         | 命令 / 动作                                                                                                                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 模板         | 复制 `assets/pmax-create-template.json`，字段见 `assets/pmax-create-template.md`                                                                                                                                   |
| **素材转换** | `siluzan-tso ad pmax-image-convert --input ./banner.jpg --output-dir ./assets --prefix <name> [--update-config ./pmax.json]`                                                                                       |
| 地理 ID      | 多国：`ad geo resolve -a <accountId> --from-file ./locations.json --json-out ./snap-geo`；单国：`ad geo search -a <accountId> -q "<地区名>"`                                                                       |
| 校验         | `siluzan-tso ad pmax-validate --config-file ./pmax.json [--json-out ./snap-pmax]`（图片规格 + 文案超长 `lengthViolations`；超长勿自动截断，见 `references/google-ads/google-ads-campaign-plan.md` § 超长人工确认） |
| **审查稿**   | Agent **写代码**读 JSON，按 `rules/google-ads-pmax-launch-plan-template.md` 投影完整文件（默认 MD；用户指定则 Excel 等）→ 用户确认；**禁止**只交概览表                                                             |
| 创建         | `siluzan-tso ad pmax-create --config-file ./pmax.json [--json-out ./snap-pmax]`                                                                                                                                    |
| 复核         | `siluzan-tso ad campaigns -a <accountId> --json-out ./snap` → `channelTypeV2` 为 `PERFORMANCE_MAX`                                                                                                                 |

**PMax**：`ad pmax-create` **同步**返回 `campaignId`、`assetGroupId`、`budgetId`；无 `ad batch get/diff`。创建接口 400 才续跑：把比这次请求多出来的非空编号写回同一份 JSON，内容不改，再执行一次。首次创建不填这三个字段。已经 200、只是扩展或视频失败时不要再 `pmax-create`。详见 `pmax-api.md`。

**金额**：JSON 中 `budget`、`targetCpa_BidingAmount` 填主币种**元**；CLI 提交前 ×100（与 `ad campaigns` 列表 `budget` 口径一致）。`pmax-get` 返回的 `budget`、`targetCpa_BidingAmount` 仍是分（`500` = 5 元）。`pmax-edit --budget` / `--target-cpa` 填元，不要把 get 里的分填回去。`pmax-edit` 退出码 0 只表示请求被接受，改完用 `pmax-get` 核对。资产组 `statusV2` 为 `Removed` 时不要再 `pmax-asset-group-edit`。

**图片**：配置 `imagePaths`（相对 JSON 文件目录）或 `marketingImageBase64` / `squareMarketingImageBase64` / `logoImageBase64`。`pmax-validate` 会自动校验图片尺寸（最小值 / 推荐值 / 宽高比 ±2% / 文件大小 ≤5120 KB）。如需将任意图片转为合规素材，用 `ad pmax-image-convert`（`marketing` / `square` / `logo` 三种格式，sharp 处理，居中裁切）。

**视频**：`videoPath`（本地文件，经 `{googleApiUrl}/pyapi` 上传并轮询 `video_id` 后自动链接）与 `youtubeUrlOrId` **二选一**（创建时最多 1 条）；创建后追加更多视频用 `ad pmax-youtube-link`（单条）或 `ad pmax-assets-update`（批量，每资产组 ≤15 条）。

**禁止**：对已创建的 PMax 系列使用 `ad campaign-edit`（旧 PUT 会 **400**）。

### 已上线 PMax 管理（CLI）

| 能力             | 命令                                                                                                                          |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 详情             | `ad pmax-get -a <id> --campaign-id <cid>`（读 `_brandGuidelinesActive`）                                                      |
| 改活动           | `ad pmax-edit`（`--patch-file` 或 `--status` / `--budget` + `--budget-id`；`assetAutomationSettings` 只改提交类型；`textGuidelines` 未传不写、传 `{}` 清空；改 `Removed` 须用户同意 + `--i-confirm`） |
| 改 Campaign 品牌 | `ad pmax-brand-assets-edit`（BG 已开启）                                                                                      |
| 启用 BG          | `ad pmax-brand-guidelines-enable --config-file …`（存量活动）                                                                 |
| 新资产组         | `ad pmax-asset-group-create --config-file …`（BG 下自动省略品牌）                                                             |
| 改资产组         | `ad pmax-asset-group-edit`                                                                                                    |
| 删资产组         | `ad pmax-asset-group-edit --status REMOVED`（软删；网关无 DELETE 端点。最后一组会 400，应暂停该组或系列）                       |
| 改资产           | `ad pmax-assets-update --config-file …`                                                                                       |
| YouTube 追加     | `ad pmax-youtube-link`（单条 `--youtube` / `--video-path`）；批量见 `ad pmax-assets-update`                                   |
| 信号             | `ad pmax-signals-get` / `ad pmax-signals-set`；受众下拉 `ad pmax-audiences`                                                   |
| 附加资产         | `ad extension pmax-types`；`callout` / `snippet` / `lead-form` / `whatsapp`（见 `pmax-api.md` § 附加资产）                    |
| 图片库           | `ad pmax-image-upload`                                                                                                        |
| 报表             | `ad pmax-report-asset-groups` / `ad pmax-report-assets` / `ad pmax-report-geo` / `ad pmax-report-channels`（单素材与素材组不必相等；素材点击可大于系列点击；渠道合计只含各网络） |
| 删活动           | 用户同意后 `ad campaign-delete -a <id> --id <campaignId> --i-confirm --commit "…"`（与 Search 共用；勿用 `ad campaign-edit`） |

模板与 HTTP 对照：`references/google-ads/pmax-api.md`。

---

## 广告的编辑

已上线系列勿用 `campaign-create` 覆盖；改方案/重建见 **`references/google-ads/google-ads-campaign-plan.md`** § 已上线后的修改；分步 CRUD 用下文 `ad *-edit` 等，写后读命令复核。

### 广告新增

参考修改流程，将修改命令替换为新增命令。

### 广告优化

参考修改流程，增加新旧对照表格。

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

# 2. 查异步任务（Creating 时每 5–10s 轮询，直至非 Creating；Agent 几乎总带 --json-out）
siluzan-tso ad batch get --id <taskId> --config-file ./campaign.json --json-out ./snap-campaign
# 读落盘 agentWorkflow：Creating → 继续 nextCommand；Successfully/HasFailed → 执行 nextCommand（batch diff）

# 3. 成功或部分成功后必做比对（含投放国家；有缺失 exit 2）
siluzan-tso ad batch diff --batch-id <taskId> --config-file ./campaign.json --json-out ./snap-campaign
# 读 ok / missing[].remediateCommand（地域 → ad geo add；扩展 → ad extension *）

# Failed：系列未创建，无需 diff；根据 get 的 reason/errors 改 JSON 后重提
# siluzan-tso ad campaign-create --config-file ./campaign.json
```

### 失败处理（Agent 必遵）

| `status`       | 含义     | 做法                                                                                                       |
| -------------- | -------- | ---------------------------------------------------------------------------------------------------------- |
| `Creating`     | 仍在执行 | 继续 `ad batch get`（带同一 `--config-file` + `--json-out`），读 `agentWorkflow`，勿重复 `campaign-create` |
| `Successfully` | 全部成功 | **须** `ad batch diff`（含投放国家）；`--json-out` 时 `ok===true` 才算齐                                   |
| `Failed`       | 全部失败 | `ad batch get` 读 `reason`/`errors` → **只改 JSON** → 再 `ad campaign-create`（**不要** `batch diff`）     |
| `HasFailed`    | 部分成功 | **须** `ad batch diff` 列出缺失 → 分步补建；需删系列重提时**先问用户**（`ok===false` / exit 2）            |

**`HasFailed` 分支：**

1. **多数广告组未建成**（`AdGroupsForBatchJob` 中多数项无 `Id`，默认 ≥50%）：  
   **停下**向用户交付：半成品系列 ID + 名称 + 失败原因（`reason`/`errors`）+ 拟修改点，给出选项「删除该系列后按修正版重建」或「保留并在其上补建」。用户明确同意删除后才执行 `ad campaign-delete -a <accountId> --id <campaignId> --i-confirm --commit "用户同意删除半成品系列…"` → 修正 **campaign.json** → 重新 `ad campaign-create`。**不要**在脏系列上反复整包补建。

2. **仅少数组/资产失败**（系列与大部分组已有 `Id`）：
   - 缺组：`ad adgroup-create`（`--json-out` 取 `id`）
   - 缺词：`ad keyword-create`（词面格式同 JSON `KeywordsForBatchJob`）
   - 缺 RSA：`ad ad-create`（`--headlines` / `--descriptions` 从 JSON `AdsForBatchJob` 抄）
   - **缺投放国家/地域**：**自动**执行 `ad geo add -a <account> --campaign-id <id> --location-id <geoId>`（`layer=location` 的 `remediateCommand`）
   - **缺附加信息（常见）**：**自动**执行 `ad extension sitelink` / `callout` / `call` / `snippet`（见下节）；`batch diff` 输出含 `补建:` 行或 `--json-out` 的 `missing[].remediateCommand`  
     补建前可用 `ad groups` / `ad keywords` / `ad geo list --mode targeted` / `ad extension list` 核对账户现状。

### 创建失败时禁止的做法（Agent 必遵）

用户确认的是「按方案创建」，**不包含**删除系列、删减方案内容或在账户里做实验。以下行为一律先问用户：

- **先定位失败项**：`ad batch get --id <taskId> --config-file <提交的 JSON> --json-out …`，读 `agentWorkflow.failedOperations[]`（`mutate_operations[N]` → JSON 路径 + 中文标签；`cascade=true` 为连带失败）。只改这些项，**禁止**整类清空否词 / 排除地域 / 投放国家或猜测式删改重提。细则见 `rules/google-ads-plan-source-fidelity.md`「创建失败后」。

- **禁止测试/探针系列**：`PolicyViolation`（如「Legal requirements」）只在部分投放地域触发时，**禁止**自行用「仅美国 / 仅亚洲 / 前 N 国」等测试系列逐批 `campaign-create` 二分排查。应停下向用户报告：触发项（`errors` 中的关键词/文案与 `mutate_operations` 下标）+ 投放地域数 + 可选方案（删该词 / 改写 / 排除可疑地域 / 申诉或豁免 / 经同意后做排查），等用户选。
- **用户同意排查时**：先列出将创建的测试系列（命名前缀 `TEST-`、`PAUSED`、地域分组）与「排查完成后删除这些测试系列」，获同意后再执行；删除前仍列出全部 ID+名称，删除命令带 `--i-confirm`。
- **禁止删除已有系列**：包括「名称已被占用」时占名的系列、`HasFailed` 留下的半成品、本会话 Agent 自己建的系列。名称冲突 → 改新系列 `campaign.Name`（及外层 `name`）重提。
- **半成品残留**：`HasFailed` 时如果预算和系列操作都没报错，`batch get` 会按账户 + 系列名自动补查系列 ID（落盘 `campaignIdSource: "lookup-by-name"`），`nextCommand` 直接是 `batch diff --campaign-id …`。只有补查失败（同名多个或查询出错）时才回退到 `ad campaigns -a <id> --fresh` 手动核对，列给用户，由用户决定删除或保留。
- 本会话中凡执行过的删除，须在写操作成败报告里逐条列出（ID、名称、原因、用户何时同意）。

### batch diff 后自动补建（Agent 必遵）

BatchJob 常漏 **附加信息**（Sitelink）与 **投放地域**；系列/组/词/RSA 往往已成功。用户确认创建时已认可 JSON → Agent **须直接补建**，**禁止**仅汇报「未创建，需要我现在补上吗？」。

1. `ad campaign-create` / `ad batch get` 的 `--json-out` 落盘含 **`agentWorkflow`**：读 `nextCommand` / `shouldRunBatchDiff` / `agentHint`（人读提示在 `--json-out` 早退时不可见）。
2. 跑 `ad batch diff`；stdout 含 `BEGIN_USER_DELIVERY_MARKDOWN`…`END`——**立刻原样发给用户**（先于补建）。
3. 对 `missing[]` 中带 `remediateCommand` 的项**直接执行**（`location` → `ad geo add`；`extension` → `ad extension *`）。
4. 扩展字段映射：`Properties.Text` + `DestinationUrl` → `ad extension sitelink`；`CALLOUT` → `callout`；`CALL` → `call`；`STRUCTURED_SNIPPET` → `snippet`。
5. 有缺失时 CLI **exit 2**；补建后再跑一次 `ad batch diff`，直到 `ok===true`；可再发更新版详情。
6. 可简短补充已补挂条数（**不能代替**步骤 2 的 Markdown 全文）。**禁止**只说「已创建成功 / 详情已交付」或只复述「未发现缺失」。见 `agent-conventions.md` §四。

完整流水线见 `references/google-ads/google-ads-campaign-plan.md` § batch diff 后自动补建。

**`ad batch diff` 比对维度：**系列是否存在 → **`targetedLocations`（投放国家/地域 id）** → 各 `AdGroupsForBatchJob[].Name` → 组内**每条**关键词（匹配类型+词面）→ RSA **每条**标题/描述（及整条 RSA）→ 系列**每条**否定词 → 附加信息条数。`--json-out` 含 `ok` / `items[]` / `statusCounts` / `missing` / **`reportMarkdown`** / **`reportMarkdownFile`** / `agentHint` / `counts`。另写 Markdown 文件（`--md-out`，默认与 json-out 同目录）。

**`ad batch get` 输出：**摘要表 + `reason`/`errors`；`--json-out` 另含 **`agentWorkflow`**（`nextCommand` 指向 batch diff 或继续轮询）。

**CLI 在提交前只做三件事：**

1. 剥除 `_` 前缀注解键（如 `_meta`、`_comment_xxx`）；
2. 缺失 `googleDataRecordId` 时生成 UUID；
3. 把 `campaign` 子树内金额字段（`Budget`、`MaxCPCAmount`、`TargetSpend_BidCeilingAmount`、`TargetCpa_BidingAmount`、`MaxCpmAmount`、`MaxCPVAmount`、`TargetCpaAmount`、`MaxCPC`）从「元」深遍历 ×100 转为「分」。

**字段校验：**提交前自动执行 `runCampaignCreateValidation`（与 `ad campaign-validate` 相同）：后端镜像硬约束 + 词面/RSA/搜索网络等；关键词分层与匹配占比见 `google-ads-keyword-taxonomy.md`（仅 Agent 参考，CLI 不校验）。

**广告组：** 写在 `campaign.AdGroupsForBatchJob` 数组中（至少 1 项），字段名严格 PascalCase（`Name` / `MaxCPCAmount` / `KeywordsForBatchJob` / `AdsForBatchJob`）。详见 `campaign-create-template.md`。

**关键词匹配：** 写在 `KeywordsForBatchJob` 块内；同一块同匹配类型，`MatchTypeV2` 与 `KeywordText` 词面格式必须对齐（`PHRASE` 用 `"词"`、`EXACT` 用 `[词]`、`BROAD` 直写）。

**多词短语：** `KeywordText` / 否词 `NegativeKeywordsForBatchJob[].KeywordText` 是 **JSON 字符串数组**，**空格多词合法**（如 `"how to make"`）。与 `keyword-negative-create` 不同，这里**没有**逗号 CLI 解析问题——**禁止**因「多词」省略否词或让用户去后台手补。

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

`TARGET_CPA` 写到 Google 的「尽可能提高转化次数」并带上目标 CPA。回读 `biddingStrategyTypeV2` 可能是 `MAXIMIZE_CONVERSIONS`，以 `targetCpa_BidingAmount` 是否等于本次金额为准。`TARGET_ROAS` 在目标回报率大于 0 时回读为 `TARGET_ROAS`；旧网关可能仍回 `MAXIMIZE_CONVERSION_VALUE`，同样以 `targetRoas` 为准。

示例：

```bash
# 改为「尽可能争取更多点击次数」并设 CPC 上限 ¥3.5
siluzan-tso ad campaign-edit -a <accountId> --id <campaignId> \
  --bidding TARGET_SPEND --bid-ceiling 3.5

# 改为 tCPA = ¥80
siluzan-tso ad campaign-edit -a <accountId> --id <campaignId> \
  --bidding TARGET_CPA --target-cpa 80
```

相对运算：先 `ad campaigns --json-out ./snap` 读 `budget`、`targetSpendBidCeilingYuan`、`targetCpaAmountYuan`（都已是元）和 `biddingStrategyTypeV2`，再传入。不要读 `targetSpend_BidCeilingAmount` / `targetCpa_BidingAmount`（仍是分）。

`campaign-edit` 的名称、预算、出价、投放网络，以及 `campaign-status`，走字段级 PATCH（`writeScope=search-field-patch`）。请求只带本次传入的字段，没传的字段保持原样。金额仍是主币种元，CLI ×100 写入网关「分」。`--search-network` / `--content-network` 传 `true` 或 `false`，关闭传 `false`，不能传空。`budgetShared=true` 时本命令直接拒绝 `--budget`，不会改共享预算。PMax 不要用本命令。

**AI Max：** 不要写系列级 `keyword_match_type`（AI Max 开启后 Google 会拒）。改单条关键词匹配类型仍用关键词命令。列表/判断渠道类型用 `channelTypeV2`，不要用旧 `channelType`。

网关还支持开始/结束时间、地区类型、地区/语言/时段/否定 IP/设备的整表替换，以及动态搜索广告域名。CLI 还没有这些参数，不要自己拼 PUT 或 PATCH。

写完会再 GET：`verification=verified` 才表示对上了本次字段；没改预算但回读预算变了则是 `partial`；读不到是 `unknown`（再查 `ad campaigns`，不要当成没改成，也不要立刻重发）。请求失败时会再 GET 一次预算：金额相对提交前变了是 `partial`（退出码 0），读不到或无法对比是 `unknown`（退出码 0），都不要立刻重发；金额没变才是失败（退出码 1）。

> PMax / 部分智能系列类型 Google 可能拒绝切换出价策略；以 API 返回错误为准。已上线 PMax 用 `ad pmax-edit`，不要用本命令。

---

## ad adgroup-rename — 广告组改名

```bash
siluzan-tso ad adgroup-rename -a <accountId> --id <adGroupId> --name <新名称>
```

---

## ad ad-create — 创建自适应搜索广告（RSA）

在已有广告组下新增 RSA。提交前 CLI **本地校验**字数/条数（超限不打 API）。

```bash
siluzan-tso ad ad-create \
  -a <accountId> \
  --adgroup-id <adGroupId> --adgroup-name <adGroupName> \
  --final-url <https://...> \
  --headlines "H1,H2,H3,..." \
  --descriptions "D1,D2[,D3,D4]" \
  [--path1 <p1>] [--path2 <p2>] \
  --commit "在 <组名> 下创建 RSA …" \
  [--json-out <path>]
```

| 约束         | 值                                             |
| ------------ | ---------------------------------------------- |
| headlines    | **3–15** 条，每条 **≤30** Google 字符（CJK×2） |
| descriptions | **2–4** 条，每条 **≤90** Google 字符（CJK×2）  |
| path1/path2  | 可选，各 **≤15**                               |

创建后暂停：`ad ad-status -a <accountId> --id <adId> --status Paused --commit "创建后暂停"`。若列表找不到新广告，给 `ad-status` / `ad list` 加宽 `--start`/`--end`。

**拒审试探留下的半成品**：同一轮里为定位哪句文案被拒而 `ad ad-create` 出来的短标题或残缺 RSA，正式那条通过后立刻删掉：

```bash
siluzan-tso ad ad-delete -a <accountId> --id <adId>
```

不要改成 `ad-status Paused` 留在组里。删完再 `ad list`，对用户报的条数用这次列表，不要按「每组 1 条」心算。只删本轮自己建的试探广告；删系列、删用户原有广告仍先问。

文案合规见 `rules/google-ads-compliance-copy.md`。

---

## ad ad-edit — 广告创意编辑

字段级 PATCH，只写本次传入的字段。标题、描述、最终网址、路径只适用于响应式搜索广告；只改 `--status` 时其它广告类型也可以。`--path1` / `--path2` 传空字符串会清空该段路径。

`ad list --json-out ./snap` 用来读当前文案，不必把未改字段再传回去：

- `headlinePart1~3` + `AddtionalHeadlines` → `--headlines`（≥3条，整表替换）
- `adDescription`/`adDescription2` + `AddtionalAdDescriptions` → `--descriptions`（≥2条，整表替换）
- `finalUrl` → `--final-url`；`path1`/`path2` → `--path1`/`--path2`
- `statusV2` → `--status`

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

只改 `--final-url` / `--max-cpc` / `--status` 时走字段级 PATCH，原地更新，`id` 与历史数据保留。`--final-url` 传空会清空关键词网址，回到广告自己的网址。改 `--text` / `--match-type`（Google 侧词面与匹配类型不可变）仍走批量 PUT，会新建并删除旧词，`id` 变化时 CLI 会提示。改 `--final-url` / `--max-cpc` / `--status` 后 CLI 会重新拉列表回读。本命令没有 `--json-out`。关键词列表按账户和日期缓存约 60 秒，且没有 `--fresh`：回读报「列表仍是」时，先等约 60 秒再看 `maxCPCYuan`。已经是目标值就当成功，**不要**立刻重跑，**不要** `keyword-delete` 后重建。等过缓存仍是旧值，再告诉用户平台未生效。

```bash
siluzan-tso ad keyword-edit \
  -a <accountId> --id <keywordId> \
  [--text <新关键词>] [--match-type Broad|Phrase|Exact] \
  [--max-cpc <n>] [--final-url <url>] [--status Enabled|Paused]
```

传 `--match-type` 时 CLI 自动规范 `keywordText` 括号/引号格式。至少传一项。`--max-cpc` 为主币种元（CLI ×100 写入 `maxCpc`「分」字段，与 `adgroup-edit --max-cpc` 同口径）。`ad keywords --json-out ./snap` 出价见 `maxCPCYuan`。列表里的 `0` 多半是未设置。`--max-cpc 0` 清空关键词出价，回到广告组出价；不要用它表示「写成 0 元」。`--status` 写入 `userStatus`（关键词级开关，非系列的 `status`）。

---

## ad keyword-status — 搜索关键词状态切换

仅改关键词状态，字段级 PATCH `userStatus`。与 `ad adgroup-status` 用法对称。

```bash
siluzan-tso ad keyword-status -a <accountId> --id <keywordId> --status <Enabled|Paused>
```

---

## ad keyword-negative-create — 否词创建（系列/组/账户三级）

```bash
# 系列级（默认）/ 组级（传 --adgroup-id）：与旧版一致
siluzan-tso ad keyword-negative-create -a <accountId> \
  --campaign-id <campaignId> --campaign-name <campaignName> \
  --keywords "词1,词2"

# 账户级（Sammamish 2026-08 新增，Google Ads「Account Settings → Negative keywords」）：
# --level Account，不传 campaign-id/adgroup-id；一次生效于整个账户所有系列
siluzan-tso ad keyword-negative-create -a <accountId> --level Account --keywords "free,jobs,DIY"
```

详见 `google-ads-read.md` §否定关键词（含 `--level` 用法与限制：账户上限约 1000 词）。

成功条数来自回执或回读里对得上的词面，不是 `--keywords` 的个数。`verification=unknown` 表示尚未核验，不要当成没加上，也不要立刻再发一次创建。

---

## ad keyword-negative-edit — 否词编辑

```bash
siluzan-tso ad keyword-negative-edit \
  -a <accountId> --id <negativeKeywordId> \
  [--text <新文本>] [--match-type Broad|Phrase|Exact]
```

传 `--match-type` 时 CLI 自动同步改写外层括号/引号。系列/组/账户三级通用，无需额外传层级参数。

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

## ad device-bid — 设备出价调整

与 AI 优化「修改设备出价」能力同源。

| 级别             | 列表                                                                                    | 修改                                                                                   |
| ---------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| **系列**（默认） | `GET …/campaignmanagement/{id}/BidModifiers/Devices`                                    | `PUT …/campaigns/{campaignId}/Criteria/{criterionId}/BidModifier/{bidModifier}`        |
| **广告组**       | `GET …/adgroupnmanagement/bidmodifiers/{id}?campaignId&adgroupId&criteriaType=PLATFORM` | `PUT …/adgroupnmanagement/bidmodifiers/{id}?campaignId&adGroupId` + Body `Criterion[]` |

**`--bid-modifier` 口径（系列级直接透传 Google 倍率）**

| 倍率  | 含义                                                                                                        |
| ----- | ----------------------------------------------------------------------------------------------------------- |
| `1.0` | 不调整                                                                                                      |
| `0.8` | 降低 20%                                                                                                    |
| `1.2` | 提高 20%                                                                                                    |
| `0`   | **写入**时排除该设备（-100%）。**列表**里网关常把「未设置」也填成 `0`，此时 Google 后台显示 `—`，不是 -100% |

**展示口径（与 Google Ads 后台「出价调整」列一致）**：`list` / `google-analysis --sections campaign-device` 已输出 `bidModifierDisplay`。写表格必须用这个字段，禁止把倍率当正百分比（不要把 `0.6` 写成 `40%`）。

| `bidModifier`   | `bidModifierSpecified` | `bidModifierDisplay` |
| --------------- | ---------------------- | -------------------- |
| `0`（未设置）   | 空 / `false`           | `—`                  |
| `0`（明确排除） | `true`                 | `-100%`              |
| `1.0`           | —                      | `0%`                 |
| `0.6`           | —                      | `-40%`               |
| `1.1`           | —                      | `+10%`               |

**系列级列表的限制**：系列级接口只返回 `bid_modifier`，不带 `bidModifierSpecified`，所以「未设置」和「已排除（-100%）」都显示为 `0`。CLI 对这类行输出 `bidModifierDisplay = "— 或 -100%（网关不区分…）"` 和 `unsetOrExcluded: true`。遇到时不要断言是哪一种：对用户说明需要到 Google Ads 后台确认。要在建系列时就确定排除某设备，在 `campaign-create` JSON 的 `targetedPlatforms` 里写 `{ "id": 30002, "bidModifier": -100 }`（见 `campaign-create-template.md`）。

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
