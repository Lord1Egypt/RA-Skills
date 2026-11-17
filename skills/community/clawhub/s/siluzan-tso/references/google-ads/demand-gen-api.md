# Demand Gen（需求开发）

渠道 `DEMAND_GEN`。搜索广告继续接采购意图。Demand Gen 负责还没搜索时的 YouTube / Discover / Gmail / Maps 曝光。**不是展示广告（Display），也不是 PMax。** 不要用 `campaign-create`、`campaign-edit`、`pmax-create`、`pmax-edit`。`PUT /campaignmanagement/campaign/{accountId}/{campaignId}` 改 Demand Gen 会 400。

模板：`assets/demand-gen-create-template.json`。

## 网关

| 项 | 值 |
| --- | --- |
| 前缀 | `{googleApiUrl}/accounts/{accountId}/campaign/demand-gen` |
| Controller | `Sammamish/src/GoogleAPI/SemManagement/DemandGen/DemandGenCampaignManagementController.cs` |
| 写入 | `Sammamish/src/GoogleService/Service/DemandGen/DemandGenAdsService.cs` |
| 枚举 | 字符串：`"TARGET_SPEND"`、`"Paused"`。`targetCpa_BidingAmount` 的拼写就是这样 |

`accountId` 用纯数字 `mediaCustomerId`。CLI 会去掉横杠。

## 金额

| 位置 | 单位 |
| --- | --- |
| `--budget` / `--target-cpa` / 创建 JSON 的 `budget`、`targetCpa_BidingAmount` | **元**。CLI ×100 后送给网关 |
| 列表和详情里的 `budget`、`targetCpa_BidingAmount`、`minimumDailyBudget` | **分**（`500` = 5 元）。旁边有 `budgetYuan` 等 |
| 两套都在时 | 写入以 `*Yuan` 为准，避免把详情里的分再乘一次 |
| `targetRoas` | 比率。`2.5` = 250%，不是 `250` |
| 版位报表 `spend` | 账户币种浮点。不要拿去当 `budget` |
| 离线转化 `conversionValue` | 账户币种浮点，不 ×100 |

## 硬规则

1. **创建永远暂停。** `statusV2` 会被忽略。启用会花钱：`demand-gen edit --status Enabled --confirm-enable --i-confirm`。脚本和草稿确认都不要启用。
2. 开广告 / 开广告组 **不会** 开系列。
3. PATCH 只传要改的字段，不要把 `demand-gen get` 整包打回去。
4. 创建必须写 `biddingStrategyTypeV2`。先 `demand-gen conversions`。没有可出价询盘/成交就用 `TARGET_SPEND`。不要信请求里的 `hasBiddableConversion`。
5. `MAXIMIZE_CONVERSIONS` 不能带目标 CPA。`MAXIMIZE_CONVERSION_VALUE` 不能带 `targetRoas`。要目标就改用 `TARGET_CPA` / `TARGET_ROAS`。
6. 创建之后 **不能** 改成 `TARGET_SPEND` / `MAXIMIZE_CONVERSIONS` / `MAXIMIZE_CONVERSION_VALUE`。要换就新建系列。`TARGET_CPA` / `TARGET_ROAS` 可以改；账户转化不够时 Google 会 400。
7. `channelStrategy` 与 `selectedChannels` 二选一。`audienceResourceName` 与 `audienceKeywords` 二选一。
8. 地域和语言写在广告组上，创建和加组都必填。查地域 `ad geo search`，查语言 `GET /campaignmanagement/languages/{accountId}`（CLI 未另做语言子命令时，用已有语言 ID，不要猜美国英语）。
9. 展示宽度：码点 > 127 算 2。商家名 ≤ 25，标题 ≤ 40，带图片时至少一条标题 ≤ 30。长标题和描述 ≤ 90。长标题只进视频广告。
10. 创建和加组：一条视频响应式广告 + 一条多素材图片广告。Logo 必填。横图或方图至少一张。图片用 `imagePaths`，CLI 先上传再填 ID。
11. 广告组至少留 1 条广告，系列至少留 1 个广告组。只想停投用 status，不要删光。
12. 一个广告组只能绑一个 Audience。新建受众只支持搜索自定义受众（1～10 个词）。
13. 学习期约 50 次可出价转化之前，不要带 `automatic`。预算或目标 CPA 单次变动超过 15% 要 `--confirm-large-change`。
14. 离线转化只有 `conversions-validate`（`validate_only`）。不要当成已经回传成功。
15. 失败续跑：把响应里的 `budgetId` / `campaignId` / `adGroupId` 写回 JSON。顺序是预算 → 系列 → 广告组。只带系列不带预算会被拒。

不支持，不要编接口：素材组、品牌手册、素材自动化、搜索主题、共享预算、轮播、商品 Feed、线索表单、系列级品牌安全、广告主频次上限。

## 命令

| 命令 | 作用 |
| --- | --- |
| `ad demand-gen conversions -a <id>` | 有没有可出价转化 |
| `ad demand-gen minimum-budget -a <id>` | 最低日预算 |
| `ad demand-gen draft -a <id> --config-file ./draft.json` | 落地页草稿，不写 Google |
| `ad demand-gen validate -a <id> --config-file ./dg.json` | 只校验 |
| `ad demand-gen create -a <id> --config-file ./dg.json` | 创建，固定暂停 |
| `ad demand-gen confirm -a <id> --config-file ./dg.json` | 政策预审后创建，仍暂停 |
| `ad demand-gen list -a <id>` | 未删除系列 |
| `ad demand-gen get -a <id> --campaign-id <id>` | 详情 |
| `ad demand-gen edit -a <id> --campaign-id <id> …` | 改名 / 预算 / 出价 / 启停 |
| `ad demand-gen content` | 改文案素材。`--ad-id` 只改一条 |
| `ad demand-gen channels` | `--strategy` 或 `--selected` |
| `ad demand-gen adgroup-status` / `ad-status` | 只动那一层 |
| `ad demand-gen adgroup-rename` | 改组名 |
| `ad demand-gen audience` / `audience-keywords` | 换受众 / 换词 |
| `ad demand-gen add-adgroup` / `add-ad` | 再加一组或一条 |
| `ad demand-gen delete-ad` / `delete-adgroup` | 须 `--i-confirm`，且不能删光 |
| `ad demand-gen report -a <id> --campaign-id <id>` | 版位报表。投放数据分析汇总报告走 **P4-DG**（`report-templates/demand-gen-analysis-report.md`），不要用创建流程出报告 |
| `ad demand-gen conversions-validate` | 离线转化只校验 |

写操作都要 `--commit "说明"`。

详情里 `waitForReview=true` 时等审核，不要改文案、不要启用。`needsCopyFix=true` 才改文案。暂停、学习期、`NotEligible: CampaignPaused` 不是拒审。
