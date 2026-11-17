# Meta（Facebook）账户 — 诊断报告（模板纲要）

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> 统计区间：`{startDate}` ~ `{endDate}`
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）

在 **Facebook Ads 现有 7 个 Section** 内，尽量对齐 `google-account-diagnosis-report.md` 的章节结构；无接口的章节（健康度/系列类型/转化趋势/质量得分）在 JSON 中标注 `notAvailable: true` + `notAvailableReason`。

拉数：**一次** `facebook-analysis`（建议全 7 维或默认 6 维 + 按需 `material`）。

```bash
siluzan-tso facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb-diagnosis
```

**默认交付：HTML（`facebook-analysis diagnosis-render` 注入 Agent JSON 生成；禁止手写/拼接 HTML）**。用户指定 Excel 时 Agent 脚本写 xlsx。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                                                                                                         |
| ---------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. 拉数**      | Agent 调 CLI | `facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb-diagnosis`（全 7 维或默认 6 维 + 按需 `material`）                                                     |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`），做洞察与叙事；表格数字可由 `--snapshot-dir` 按 guide 根字段自动映射                                       |
| **3. 写 JSON**   | Agent        | 撰写 `meta-account-diagnosis-report.json`：仅 `meta.accountId` + `narrative` 为必填；`kpis`/`tables` 可省略，由 `--snapshot-dir` 自动合并                                    |
| **4. 渲染 HTML** | CLI          | `facebook-analysis diagnosis-render` — **校验 narrative 11 个分析小节必含字段**（4 个媒体未覆盖小节可标 `notAvailable`），缺项报错不生成 HTML；**禁止** Agent 手写/拼接 HTML |

> `--snapshot-dir` 自动补全 `meta` / `kpis`（仅 overview；**禁止**用 ad-sets/creative 行 results 加总对比 overview）与 `tables.*`（按 `facebook-analysis-guide.md`：`adGroups`/`networks`/`countries`/`audiences`/`creatives`/`materials`）。**数值一律以 CLI 快照覆盖**（`meta` 仅补空）。

### JSON 契约（`meta-account-diagnosis-report.json`）

```jsonc
{
  "meta": {
    "accountId": "string（必填）",
    "accountName": "string",
    "currency": "string，如 USD/CNY",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD",
    "generatedAt": "ISO8601（可省略，render 自动写入）",
  },
  "kpis": {
    "spend": "number",
    "impressions": "number",
    "clicks": "number",
    "results": "number",
    "ctr": "number（0~1 小数）",
    "cpc": "number",
    "costPerResult": "number",
    "reach": "number",
    "frequency": "number",
    "previousPeriod": "同结构可选，用于环比",
  },
  "tables": {
    "platform": "[{ publisherPlatform, platformPosition, spend, results, costPerResult }]",
    "country": "[{ countryOrRegion, spend, results, costPerResult }]",
    "audience": "[{ age, gender, spend, results, costPerResult }]",
    "creative": "[{ creativeName, spend, impressions, clicks, ctr, results, costPerResult }]",
    "material": "[{ materialName, spend, impressions, results }]（DC 专用，标准账户常为空）",
  },
  "narrative": {
    "executiveSummary": ["string，≥1 段"],
    "sections": {
      "accountProfile": { "analysis": ["string，≥1 条"], "suggestions": ["string，≥1 条"] },
      "coreMetrics": { "analysis": ["…"], "suggestions": ["…"] },
      "accountStructure": { "analysis": ["…"], "suggestions": ["…"] },
      "healthGrade": {
        "notAvailable": true,
        "notAvailableReason": "gold-account",
        "_comment": "或改为 { analysis, suggestions } 若有派生数据",
      },
      "campaignTypes": { "notAvailable": true, "notAvailableReason": "campaign-types" },
      "keyComparisons": { "analysis": ["…"], "suggestions": ["…"] },
      "conversionTrend": { "notAvailable": true, "notAvailableReason": "daily-metrics" },
      "platformGeoAudience": { "analysis": ["…"], "suggestions": ["…"] },
      "creative": { "analysis": ["…"], "suggestions": ["…"] },
      "material": { "analysis": ["…"], "suggestions": ["…"] },
      "qualityScore": { "notAvailable": true, "notAvailableReason": "ads-index" },
    },
    "recommendations": ["string 或 { title, content }，≥3 条"],
    "excludedChecks": [
      "string，≥1 条，列出已排除的 Google-only 检查项（如 gold-account/daily-metrics/ads-index）",
    ],
  },
}
```

> `healthGrade` / `campaignTypes` / `conversionTrend` / `qualityScore` 四节：Meta 无对应 API 时须写 `{ notAvailable: true, notAvailableReason: "<Google 维度名>" }`；若有派生数据（如用 `creativeType` 分布替代系列类型），则正常写 `{ analysis, suggestions }`，二者满足其一即可通过校验。

---

## 1. 账户画像

**数据呈现**：账户名：`overview` → `accountName`；`list-accounts -m MetaAd -k <id>` 补 BM/状态（若有）。写入 JSON `meta.accountName`。

- **无** Google 式落地页 Section → 写 `[ 本媒体接口未提供：final-urls ]`

**分析（必写）** → 写入 `narrative.sections.accountProfile.{analysis,suggestions}`：

- **总结**：账户基本信息、投放状态。
- **建议**：账户结构或设置层面的优化，1～3 条。

## 2. 核心指标快照

**数据呈现**：本期 vs 上期：消耗、展示、点击、CTR、CPC、转化、CPA、results、costPerResult、reach、frequency。写入 JSON `kpis`（可由 `--snapshot-dir` 自动合并）。

- **CLI**：`overview`

**分析（必写）** → 写入 `narrative.sections.coreMetrics.{analysis,suggestions}`：

- **总结**：本期 vs 上期消耗/结果/CPL 变化（仅当 previousPeriod 有数据）；覆盖与频次水平。
- **建议**：账户级预算或投放节奏（引用具体数字），1～3 条。

## 3. 账户结构

**数据呈现**：

- **无** `resource-counts` / `conversion-actions` → 用 `ad-sets` + `creative` 行数简述：「共 N 个广告组、M 条在投创意（有 spend/impressions）」。
- 按 `campaignName` 去重估算系列数（说明为派生，非 API 直出）。

**分析（必写）** → 写入 `narrative.sections.accountStructure.{analysis,suggestions}`：

- **总结**：账户结构规模、集中度。
- **建议**：结构精简或扩展方向，1～3 条。

## 4. 健康度 / 黄金账户

- `[ 本媒体接口未提供：gold-account ]` → 写入 `narrative.sections.healthGrade = { notAvailable: true, notAvailableReason: "gold-account" }`

## 5. 系列类型分布

- `[ 本媒体接口未提供：campaign-types ]`；可用 `creative` 的 `creativeType` 分布作补充 → 写入 `narrative.sections.campaignTypes`（`notAvailable` 或补充 `analysis/suggestions`）

## 6. 重点维度对比（本期 vs 上期）

**数据呈现**：总览已含环比；另可对 `ad-sets` / `country` / `platform` 做「本期排行」快照（无上期分维数据时不做分维环比）。

**分析（必写）** → 写入 `narrative.sections.keyComparisons.{analysis,suggestions}`：

- **总结**：Top 广告组/国家/平台及其效率差异。
- **建议**：预算或出价调整方向（引用具体 `name` + 数据），1～3 条。

## 7. 转化成本趋势

- `[ 本媒体接口未提供：daily-metrics ]`；勿用猜测曲线 → 写入 `narrative.sections.conversionTrend = { notAvailable: true, notAvailableReason: "daily-metrics" }`

## 8. 平台、地域、受众

**数据呈现**：

- **CLI**：`platform`、`country`、`audience`
- `platform` → `networks[]`：用 **`publisherPlatform`**（投放平台）+ **`platformPosition`**（版位）；`network` 仅等于 `platformPosition`（兼容旧版，勿当平台列）。写入 JSON `tables.platform[]` / `tables.country[]` / `tables.audience[]`。

**分析（必写）** → 写入 `narrative.sections.platformGeoAudience.{analysis,suggestions}`：

- **总结**：主力平台/国家/受众段及其效率差异；与 Google `devices` / `geographic` / `audience` 对应说明。
- **建议**：版位/地域/受众定向调整（引用具体值 + 数据），1～3 条。

## 9. 创意（替代搜索词+搜索广告）

**数据呈现**：Top 创意、低效创意；**无** `search-terms` → `[ 不适用：搜索词 ]`。写入 JSON `tables.creative[]`。

- **CLI**：`creative`

**分析（必写）** → 写入 `narrative.sections.creative.{analysis,suggestions}`：

- **总结**：Top 消耗创意、CTR/转化表现分化。
- **建议**：暂停低效创意或复制高效创意方向，1～3 条。

## 10. 素材

**数据呈现**：写入 JSON `tables.material[]`（DC 专用，标准账户常为空）。

- **CLI**：`material`（DC）；否则指向 `creative`
- **无** Google `extensions` → `[ 本媒体接口未提供：extensions ]`

**分析（必写）** → 写入 `narrative.sections.material.{analysis,suggestions}`：

- **总结**：素材表现（若为空，说明账户非 DC，改用 §9 创意结论）。
- **建议**：素材迭代方向，1～3 条。

## 11. 质量得分

- `[ 本媒体接口未提供：ads-index ]` → 写入 `narrative.sections.qualityScore = { notAvailable: true, notAvailableReason: "ads-index" }`

## 12. 总结与行动项

- 优先：高消耗低效 Ad Set、版位、国家、人群、创意。写入 JSON `narrative.recommendations[]`（≥3 条）。
- 列出已排除的 Google-only 检查项，避免读者以为漏查。写入 JSON `narrative.excludedChecks[]`（≥1 条，如 `gold-account`、`campaign-types`、`daily-metrics`、`ads-index`）。

---

字段细则：`references/analytics/facebook-analysis-guide.md`。

### 渲染 HTML

```bash
siluzan-tso facebook-analysis diagnosis-render --data ./meta-account-diagnosis-report.json --snapshot-dir ./snap-fb-diagnosis --out ./meta-account-diagnosis-report.html
```

- `--data`：Agent 撰写的诊断报告 JSON（必填）
- `--snapshot-dir`：可选，`facebook-analysis --json-out` 目录，自动补全 `meta` / `kpis` / `tables.*`
- `--out`：输出 HTML 路径（默认同 `--data` 目录）
