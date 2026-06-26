# Meta（Facebook）账户 — 诊断报告（模板纲要）

> 统计区间：`{startDate}` ~ `{endDate}`  
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）

在 **Facebook Ads 现有 7 个 Section** 内，尽量对齐 `google-account-diagnosis-report.md` 的章节结构；无接口的章节保留标题并写 `[ 本媒体接口未提供：{Google 维度名} ]`。

拉数：**一次** `facebook-analysis`（建议全 7 维或默认 6 维 + 按需 `material`）。

```bash
siluzan-tso facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb-diagnosis
```

---

## 1. 账户画像

- 账户名：`overview` → `accountName`；`list-accounts -m MetaAd -k <id>` 补 BM/状态（若有）。
- **无** Google 式落地页 Section → 写 `[ 本媒体接口未提供：final-urls ]`。

## 2. 核心指标快照

- **CLI**：`overview`
- 本期 vs 上期：消耗、展示、点击、CTR、CPC、转化、CPA、results、costPerResult、reach、frequency。

## 3. 账户结构

- **无** `resource-counts` / `conversion-actions` → 用 `ad-sets` + `creative` 行数简述：「共 N 个广告组、M 条在投创意（有 spend/impressions）」。
- 按 `campaignName` 去重估算系列数（说明为派生，非 API 直出）。

## 4. 健康度 / 黄金账户

- `[ 本媒体接口未提供：gold-account ]`

## 5. 系列类型分布

- `[ 本媒体接口未提供：campaign-types ]`；可用 `creative` 的 `creativeType` 分布作补充。

## 6. 重点维度对比（本期 vs 上期）

- 总览已含环比；另可对 `ad-sets` / `country` / `platform` 做「本期排行」快照（无上期分维数据时不做分维环比）。

## 7. 转化成本趋势

- `[ 本媒体接口未提供：daily-metrics ]`；勿用猜测曲线。

## 8. 平台、地域、受众

- **CLI**：`platform`、`country`、`audience`
- `platform` → `networks[]`：用 **`publisherPlatform`**（投放平台）+ **`platformPosition`**（版位）；`network` 仅等于 `platformPosition`（兼容旧版，勿当平台列）。
- 全表或 Top 表；与 Google `devices` / `geographic` / `audience` 对应说明。

## 9. 创意（替代搜索词+搜索广告）

- **CLI**：`creative`
- Top 创意、低效创意；**无** `search-terms` → `[ 不适用：搜索词 ]`

## 10. 素材

- **CLI**：`material`（DC）；否则指向 `creative`。
- **无** Google `extensions` → `[ 本媒体接口未提供：extensions ]`

## 11. 质量得分

- `[ 本媒体接口未提供：ads-index ]`

## 12. 总结与行动项

- 优先：高消耗低效 Ad Set、版位、国家、人群、创意。
- 列出已排除的 Google-only 检查项，避免读者以为漏查。

---

字段细则：`references/analytics/facebook-analysis-guide.md`。
