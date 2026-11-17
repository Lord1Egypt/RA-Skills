# TikTok 广告主账户 — 周期分析报告（模板纲要）

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> 统计区间：`{startDate}` ~ `{endDate}`
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）

数据块：总览、系列/组/广告、视频素材、受众（含性别/年龄/兴趣合并）（**以 `--json-out` 实际字段为准**）。

**默认交付：HTML（`tiktok-analysis render` 注入 Agent JSON 生成；禁止手写/拼接 HTML）**。用户指定 Excel 时 Agent 脚本写 xlsx。封面按日期写成「季度」或「月度」，对不上仍是「账户分析」。不要打开 HTML 改称呼。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                                                                       |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **1. 拉数**      | Agent 调 CLI | `tiktok-analysis -a <id> --start <s> --end <e> --json-out ./snap-tiktok`（见下方「日期规则」，全 12 维或 `--sections` 指定子集）           |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`），做洞察与叙事；表格数字可由 `--snapshot-dir` 按类型自动映射              |
| **3. 写 JSON**   | Agent        | 撰写 `tiktok-period-report.json`：仅 `meta.accountId` + `narrative` 为必填；`kpis`/`tables` 可省略，由 `--snapshot-dir` 按网关类型自动合并 |
| **4. 渲染 HTML** | CLI          | `tiktok-analysis render` — **校验 narrative 6 个分析小节必含字段**，缺项报错不生成 HTML；**禁止** Agent 手写/拼接 HTML                     |

> `--snapshot-dir` 自动补全 `meta` / `kpis` / `tables.*`。网关形状见 `src/types/tiktok-analysis-api.ts`（对齐前端 `periodReport/tiktok.js`）：`campaigns` 为 `{ campaigns:[] }`；ad-groups/videos/audience 为 `{ data.list[].metrics }`（snake_case）；ads 为根数组。**本期 KPI 优先 campaigns 累加**。**数值一律以 CLI 快照覆盖**（`meta` 仅补空）；Agent 只写 `narrative`。

### JSON 契约（`tiktok-period-report.json`）

```jsonc
{
  "meta": {
    "accountId": "string（必填，TikTok mediaCustomerId）",
    "accountName": "string",
    "currency": "string，如 CNY/USD",
    "startDate": "YYYY-MM-DD",
    "endDate": "YYYY-MM-DD",
    "generatedAt": "ISO8601（可省略，render 自动写入）",
  },
  "kpis": {
    "spend": "number",
    "impressions": "number",
    "clicks": "number",
    "conversions": "number",
    "ctr": "number（0~1 小数）",
    "averageCpc": "number",
    "costPerConversion": "number",
    "previousPeriod": "同结构可选，用于环比",
  },
  "tables": {
    "campaigns": "[{ campaignName, spend, impressions, clicks, ctr, conversions, costPerConversion }]",
    "adGroups": "[{ adGroupName, campaignName, spend, clicks, ctr, conversions, costPerConversion }]",
    "ads": "[{ adName, spend, clicks, ctr, conversions }]",
    "videos": "[{ videoName, spend, impressions, clicks, ctr, conversions, costPerConversion }]",
    "audienceGender": "[{ gender, spend, impressions, clicks, ctr }]",
    "audienceAge": "[{ ageRange, spend, impressions, clicks, ctr }]",
    "audienceInterest": "[{ interestCategory, spend, impressions, clicks, ctr }]",
  },
  "narrative": {
    "executiveSummary": ["string，≥1 段"],
    "sections": {
      "overview": { "analysis": ["string，≥1 条"], "suggestions": ["string，≥1 条"] },
      "campaigns": { "analysis": ["…"], "suggestions": ["…"] },
      "adGroups": { "analysis": ["…"], "suggestions": ["…"] },
      "ads": { "analysis": ["…"], "suggestions": ["…"] },
      "videos": { "analysis": ["…"], "suggestions": ["…"] },
      "audience": { "analysis": ["…"], "suggestions": ["…"] },
    },
    "recommendations": ["string 或 { title, content }，≥3 条"],
  },
}
```

---

## 1. 执行摘要（总览）

**数据呈现**：账户级消耗、展示、点击、转化、CTR、CPC 等（接口返回结构因版本可能略有差异）。写入 JSON `kpis`（Agent 从 overview 快照映射填写）。

- **CLI**：`siluzan-tso tiktok-analysis -a <mediaCustomerId> --sections overview [--start YYYY-MM-DD --end YYYY-MM-DD] --json-out <dir>`

**分析（必写）** → 写入 `narrative.sections.overview.{analysis,suggestions}`：

- **总结**：本期 vs 上期消耗/点击/转化/CTR/CPC/CPA 变化（若有 previousPeriod 数据）。
- **建议**：账户级预算或投放节奏（引用具体百分比或金额），1～3 条。

## 2. 广告结构（系列 / 广告组 / 广告）

**数据呈现**：

- 系列：`--sections campaigns` → `CampaignSectionData`（Query：`startDate`、`endDate`、`take`，默认 `take=100`）。写入 JSON `tables.campaigns[]`。**不展示状态**：网关 `campaignStatus` 恒为 null，HTML 不渲染该列。
- 广告组：`--sections ad-groups` → `AdGroupReport`。写入 JSON `tables.adGroups[]`（组名 + `metrics.campaign_name`）。
- 广告：`--sections ads` → `AdReport`。写入 JSON `tables.ads[]`。**不展示所属组**：`AdReport` 无 `adgroup_name`，HTML 不渲染该列。

**分析（必写，三个子块各写一段，不可合并为一句带过）**：

1. **系列分析 — 总结**：Top 系列及费用占比、暂停/活跃系列效果差异。**建议**：预算增减或暂停具体 `campaignName`，1～3 条。→ 写入 `narrative.sections.campaigns.{analysis,suggestions}`
2. **广告组分析 — 总结**：高消耗广告组、CPA 异常组。**建议**：出价或结构优化（写 `adGroupName` + 数据），1～3 条。→ 写入 `narrative.sections.adGroups.{analysis,suggestions}`
3. **广告分析 — 总结**：Top 消耗创意、CTR/转化表现分化。**建议**：暂停低效广告或复制高效创意方向，1～3 条。→ 写入 `narrative.sections.ads.{analysis,suggestions}`

## 3. 素材与创意（视频）

**数据呈现**：按消耗排序的视频素材表现（消耗、展示、点击、CTR、转化、CPA）。写入 JSON `tables.videos[]`。

- **CLI**：`siluzan-tso tiktok-analysis -a <id> --sections videos [--start … --end …] [--take N] --json-out <dir>`

无 `tables.videos` 行时 **仍渲染「素材/创意」节**，用客户可读空占位说明「当前广告没有视频创意素材」，禁止对客户写 VideoReport/HTTP 500 等接口术语。该维始终存在，不是删节。

**分析（必写）** → 写入 `narrative.sections.videos.{analysis,suggestions}`：

- **总结**：高消耗低转化素材、Top 转化素材的共性（时长/形式/卖点）。
- **建议**：暂停低效素材、复制高效创意方向，1～3 条。

## 4. 受众分析

**数据呈现**：

- 单维度：`--sections audience-<dimension>`，可选：`audience-gender` | `audience-age` | `audience-interest-category` | `audience-country-code` | `audience-platform` | `audience-language`
- 三块合并：`--sections audience-merged`（**固定输出合并 JSON**，含 `gender` / `age` / `interest_category`；别名 `audience`）

写入 JSON `tables.audienceGender[]` / `tables.audienceAge[]` / `tables.audienceInterest[]`。

**分析（必写）** → 写入 `narrative.sections.audience.{analysis,suggestions}`：

- **总结**：主力性别/年龄段/兴趣类目、转化或 CTR 更优的受众段。
- **建议**：受众定向调整或素材投放方向（引用维度值 + 指标），1～3 条。

## 5. 地域 / 兴趣辅助数据

- 地区代码枚举：`tiktok-analysis areacode`（解析地域报表、对照名称，非 `--sections` 批跑维度）
- 兴趣类目树：`tiktok-analysis interest-list -a <id>`（需配置 **`tiktokApiUrl`**）

## 6. 报告收尾（全账户）

在以上各 section 分析之后，须撰写 **「优化建议」**（3～5 条，写入 JSON `narrative.recommendations[]`），跨 section 归纳优先级，**须与前面各 section 分析一致、不得矛盾**。

## 7. 附录

- 日期规则：`--start` / `--end` **同传或同省略**；省略时默认**近 7 天（截至昨天）**，与 `report meta-overview`、`google-analysis` 一致。
- 鉴权：与 TSO 其他接口相同（`config show` 中 `tsoApiBaseUrl` / Token）。
- 与 steward「优化报告」区别：见 `meta-period-report.md` 末节说明；`report list/create` 为成品报告流，本模板对应**实时分析 JSON**。

---

### CLI 速查表

统一入口：`siluzan-tso tiktok-analysis -a <id> --sections <name> [--start … --end …] --json-out <dir>`（省略 `--sections` 则批跑全部 12 维）

| 数据块                 | `--sections` 取值                                                                                                                       |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 总览                   | `overview`                                                                                                                              |
| 系列                   | `campaigns`                                                                                                                             |
| 广告组                 | `ad-groups`                                                                                                                             |
| 广告                   | `ads`                                                                                                                                   |
| 视频素材               | `videos`                                                                                                                                |
| 受众（单维）           | `audience-gender` / `audience-age` / `audience-interest-category` / `audience-country-code` / `audience-platform` / `audience-language` |
| 受众（性别+年龄+兴趣） | `audience-merged`（别名 `audience`）                                                                                                    |
| 地区码                 | 子命令 `tiktok-analysis areacode`（非 `--sections`）                                                                                    |
| 兴趣列表               | 子命令 `tiktok-analysis interest-list -a <id>`（非 `--sections`）                                                                       |

### 渲染 HTML

```bash
siluzan-tso tiktok-analysis render --data ./tiktok-period-report.json --snapshot-dir ./snap-tiktok --out ./tiktok-period-report.html
```

- `--data`：Agent 撰写的报告 JSON（必填）
- `--snapshot-dir`：可选，`tiktok-analysis --json-out` 目录，自动补全 `meta` / `kpis` / `tables.*`
- `--out`：输出 HTML 路径（默认同 `--data` 目录）
