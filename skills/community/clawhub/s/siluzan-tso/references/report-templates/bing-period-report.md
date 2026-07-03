# Bing（Microsoft Advertising / BingV2）— 账户分析报告（模板纲要）

> 统计区间：`{startDate}` ~ `{endDate}`（**不可包含今天或昨天**，见下文）  
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）  
> **默认交付**：**HTML**（Agent 脚本读落盘 JSON 生成；禁止仅 Markdown 摘要或纯 JSON 充当终稿）。用户指定 Excel 时 Agent 脚本写 xlsx，**无** CLI `render` 子命令。

数据块：总览、设备、地域、受众（年龄/性别）、系列、广告组、广告、关键词、搜索字词。

---

## 日期规则（必读）

- Bing 接口**无法**拉取过新的数据；时间范围内**任意一天**若为**今天**或**昨天**，请求会失败。
- **CLI**：`--start` / `--end` 须**同传或同省略**；省略时默认**截至前天**的近 7 天（与 `report bing-*` 实现一致）。
- 自选区间时请确保结束日 ≤ **前天**。

---

## 拉数（一次目录）

```bash
mkdir -p ./snap-bing

siluzan-tso list-accounts -m BingV2 -k <mediaCustomerId> --json-out ./snap-bing

siluzan-tso report bing-overview -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso balance -m BingV2 --accounts <mediaCustomerId> --json-out ./snap-bing
siluzan-tso report bing-campaigns -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso report bing-device -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso report bing-geographic -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso report bing-audience-merged -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso report bing-ad-groups -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso report bing-ads -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
siluzan-tso report bing-keywords -a <mediaCustomerId> --start <S> --end <E> --limit 100 --json-out ./snap-bing
siluzan-tso report bing-search-terms -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-bing
```

- 写脚本前先读各 `bing-*-<id>.outline.txt`，再读 `.json`（见 `references/core/agent-conventions.md` §三）。
- TopN、排序、汇总均在脚本内完成，禁止心算。
- 金额字段已为**元**；`ctr` / `conversionRate` 等为 **0~1 小数**，展示百分比用 `(v * 100).toFixed(2) + '%'`。

---

## 分析纪律（全章节强约束）

**每个 section 的数据表格/图表之后，必须紧跟该 section 的「分析」小节**；整份报告**禁止**只有数据、没有分析。

| 要求 | 说明 |
| --- | --- |
| **总结** | 引用**当 section 落盘 JSON** 中的数字（TopN、占比、合计、环比）；可对比账户 KPI 或 section 内均值 |
| **建议** | 1～3 条可执行项（预算、出价、暂停、否词、设备/地域调价等），须点名系列/关键词/国家/设备并引用数据 |
| **禁止** | 编造数字、空分析、全章共用一段笼统话而不分 section |
| **环比** | 仅 **总览** `currentPeriod` vs **`previousPeriod`**（CLI 可能二次拉数回填）；**previousPeriod 全 0 时不写 0% 环比** |
| **缺数据** | 某 section 拉数失败或 `items` 为空 → 分析写 `[数据不可用：<原因>]`，**仍须保留分析小节标题** |

报告 HTML 建议结构：按下方章节顺序，每章 = **标题 → 数据表/指标卡 → 「分析」**（含总结 + 建议）。

---

## 1. 执行摘要（总览）

- **CLI**：`siluzan-tso report bing-overview -a <mediaCustomerId> [--start … --end …] --json-out <dir>`

### 余额（必读 · 勿读 overview 快照）

`OverviewSectionData` 里的 `balance` / `remainingAccountBudget` **不是实时余额**，是报告生成时的快照，**常为 0 或未同步**。

| 正确做法 | 错误做法 |
| --- | --- |
| 读落盘 JSON 的 **`remainingAccountBudget`** 或 **`balance`**（CLI 已用 `GetMediaAccountInfo` 回填） | 直接相信 overview 原始响应里的 0 |
| 字段 **`_balanceSource: "GetMediaAccountInfo"`** 表示已校正 | 把 `$0.00` 写进报告而不说明 |
| 仍须独立核对：`siluzan-tso balance -m BingV2 --accounts <id> --json-out <dir>` | 用 `stats` 或 overview 推断余额 |

CLI 落盘时会：overview 余额为 0 → 调 `GetMediaAccountInfo` → 写回 `remainingAccountBudget` 与 **`balance`**（与 Web `filterOverviewData` 一致）。

### 环比（必读 · 勿读空 previousPeriod）

网关内嵌的 **`previousPeriod` 常全为 0**。CLI 若检测到为空，会按 Web `calcPrePeriodTimeRange` 规则再请求**上一周期**的 `OverviewSectionData`，将其 **`currentPeriod`** 写入 `previousPeriod`，并标注 **`_previousPeriodSource: "OverviewSectionData-second-fetch"`**。

| 场景 | 报告写法 |
| --- | --- |
| `previousPeriod.spend > 0`（含二次拉数回填） | 可写消耗/点击/转化/CTR/CPC/CPA 环比 |
| `previousPeriod` 仍为空或全 0 | **不写环比为 0%**；写「上一周期数据不可用」 |
| 有 `previousPeriodDateRange` | 分析中注明对比区间 |

### 日均消耗 / 活跃天数

Bing 网关常不返回 `averageDailyCost`、`activeDays`（或为 0）。CLI 落盘前会：① 缺 `totalCost` 时用 `currentPeriod.spend`；② 缺 `activeDays` 时用 `--start`~`--end` 含首尾日历天数；③ `averageDailyCost = totalCost / activeDays`（保留 2 位小数）。

**数据呈现**：区间消耗、展示、点击、转化、CTR、CPC、CPA、日均消耗、**实时余额**（`balance`）、优化分；**有效** `previousPeriod` 时展示环比。

**分析（必写）**：

- **总结**：本期 vs 上期消耗/点击/转化/CTR/CPC/CPA 变化（**仅当 previousPeriod 有数据**）；展示份额（`searchImpressionShare`）及预算/排名丢失份额；余额与日均消耗可支撑天数（用 **`balance` / `remainingAccountBudget`**，非 overview 快照 0）。
- **建议**：账户级预算或投放节奏（引用具体百分比或金额）；若展示份额丢失高 → 预算或出价方向；1～3 条。

---

## 2. 设备

- **CLI**：`report bing-device` → `DeviceSectionData`（行在 `devices[]`）

**数据呈现**：各 `deviceType` 的展示、点击、消耗、CTR、CPC、转化、CPA；建议附消耗占比。

**分析（必写）**：

- **总结**：主消耗设备、各设备 CPA/CPC 差异、高消耗低转化设备。
- **建议**：设备出价调整或预算向高转化设备倾斜（写设备名 + 表中数字），1～3 条。

---

## 3. 地域

- **CLI**：`report bing-geographic` → `GeographicSectionData`（常见 `countries[]`，**以 outline 为准**）

**数据呈现**：Top 国家/地区（建议 Top 10）消耗、点击、转化、CTR、CPC、CPA。

**分析（必写）**：

- **总结**：地域消耗集中度、高转化 vs 高消耗低转化国家/地区。
- **建议**：地域加价/降价/排除或单独系列（写 `countryOrRegion` + 数据），1～3 条。

---

## 4. 受众

- **CLI**：推荐 `report bing-audience-merged`（年龄+性别合并 JSON）；或分别 `bing-age-audience` / `bing-gender-audience`

**数据呈现**：年龄段、性别的展示、点击、消耗、CTR、CPC（按 `data.ageAudience.audience` / `data.genderAudience.audience`）。

**分析（必写）**：

- **总结**：主力年龄段/性别、转化或 CPA 更优的受众段、无效花费受众。
- **建议**：受众出价_modifier 或排除（引用 `audience` 字段 + 指标），1～3 条。

---

## 5. 广告结构（系列 / 广告组 / 广告）

| 层级 | CLI | 落盘 |
| --- | --- | --- |
| 系列 | `report bing-campaigns` | `bing-campaigns-*.json`（数组行） |
| 广告组 | `report bing-ad-groups` | `bing-ad-groups-*.json` |
| 广告 | `report bing-ads` | `bing-ads-*.json` |

**数据呈现**：各表按消耗降序；系列含 `campaignStatus`；广告组可含质量分相关字段（以 outline 为准）。

**分析（必写，三个子块各写一段，不可合并为一句带过）**：

1. **系列分析 — 总结**：Top 系列及费用占比、暂停/活跃系列效果差异、合计 CTR/CPC/CPA。**建议**：预算增减、暂停或放量具体 `campaignName`，1～3 条。
2. **广告组分析 — 总结**：高消耗广告组、质量分或 CPA 异常组。**建议**：出价、暂停或结构优化（写 `adGroupName` + 数据），1～3 条。
3. **广告分析 — 总结**：Top 消耗创意、CTR/转化表现分化。**建议**：暂停低效广告、复制高效创意方向，1～3 条。

---

## 6. 关键词与搜索字词

| 类型 | CLI | 说明 |
| --- | --- | --- |
| 关键词 | `report bing-keywords` | 默认 `limit=100`、`orderByCost=true` |
| 搜索字词 | `report bing-search-terms` | 同上 |

**数据呈现**：Top 关键词/搜索词表（消耗、CTR、CPC、转化、CPA、质量分/匹配类型等，以 outline 为准）。

**分析（必写，两块各写一段）**：

1. **关键词 — 总结**：高转化词、高消耗低转化或零转化词、匹配类型分布。**建议**：暂停/降价/提价/改匹配（写 `keyword` + 数据），1～3 条。
2. **搜索字词 — 总结**：高意向词、应加为关键词的词、应否定的无关词（对比触发 `keyword`）。**建议**：加词、否词（写 `searchQuery` + 数据），1～3 条。

---

## 7. 报告收尾（全账户）

在以上各 section 分析之后，可增加 **「优化建议汇总」**（3～5 条），跨 section 归纳优先级，**须与前面各 section 分析一致、不得矛盾**；可呼应对外客户话术（若用户需要）。

---

## 附录

- 鉴权：与 TSO 其他接口相同（`config show` 中 `tsoApiBaseUrl` / Token）。
- 与 steward「优化报告」区别：见 `meta-period-report.md` 末节；此处为**实时分析 JSON**。
- 交付前自检：见 `references/core/agent-conventions.md` §七（币种、区间、章节齐全、数字来自脚本 stdout）。

---

### CLI 速查表

| 数据块   | 子命令                        |
| -------- | ----------------------------- |
| 总览     | `report bing-overview`        |
| 设备     | `report bing-device`          |
| 地域     | `report bing-geographic`      |
| 年龄受众 | `report bing-age-audience`    |
| 性别受众 | `report bing-gender-audience` |
| 受众合并 | `report bing-audience-merged` |
| 系列     | `report bing-campaigns`       |
| 广告组   | `report bing-ad-groups`       |
| 广告     | `report bing-ads`             |
| 关键词   | `report bing-keywords`        |
| 搜索字词 | `report bing-search-terms`    |
