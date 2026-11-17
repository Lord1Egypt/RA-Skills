# Google 账户周期报告 — Excel 交付规格

> **终稿语言**：Sheet 名和表头跟 `meta.lang`。英文终稿用消耗→Spend、展示→Impressions、点击→Clicks、转化→Conversions，不要另起结构。
>
> **适用场景**：用户明确要求 **Google 账户 + 统计区间 + Excel/xlsx**，且**未**使用 OKKI / 询盘固定话术。  
> **工作流**：**P4**（与 `google-period-report.md` 共用拉数维度；交付形态不同）。  
> **禁止**：加载宿主「xlsx / Excel」第三方 Skill 代替本流程；**无** CLI 内置写表子命令，须 Agent 脚本（`exceljs` / `xlsx` / `openpyxl`）读落盘 JSON 写 `.xlsx`。

---

## 执行门禁（**全部满足后才允许写脚本**）

以下任一项未完成 → **禁止** `google-analysis` 之后的写 Excel 步骤：

| #   | 门禁                  | 命令 / 动作                                                                                                                     |
| --- | --------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Read 当次必读         | `references/core/agent-conventions.md`、`references/analytics/account-analytics.md`、`google-period-report.md`（本文）          |
| 2   | **账户 ID 核验**      | `siluzan-tso list-accounts -m Google -k <用户给的 mediaCustomerId> --json-out ./snap-p4`                                        |
| 3   | 确认 `currencyCode`   | 来自步骤 2 落盘 JSON 的 `items[].ma.currencyCode`（或表格列「币种」）                                                           |
| 4   | **拉数**              | `google-analysis -a <已核验的 mediaCustomerId> --start … --end … --sections … --json-out <dir>`                                 |
| 5   | **先 outline 后脚本** | 对本次 `--sections` 涉及的**每一个**维度，Read 同目录 `<section>-<accountId>_*.outline.txt`（或 stdout 摘要里的 `outlineFile`） |
| 6   | 写脚本                | 字段名**只**来自 outline 最后一行 TS 类型；业务 JSON **仅**在脚本内 `readFileSync` / `require`                                  |
| 7   | 交付前审阅            | 按 `references/core/agent-conventions.md` §七 自检；xlsx 无法 Read 时须贴自检表 + 脚本 stdout 摘要                              |

---

## 账户 ID

`list-accounts -m Google -k <id>` 核验；全流程用同一 `mediaCustomerId`（见 `agent-conventions.md`）。报告首行：`统计区间：YYYY-MM-DD ~ YYYY-MM-DD（货币：XXX）`。

---

## 用户指定 Sheet → CLI section 映射

用户已列出 Sheet 名时，**以用户清单为准**拉数（不必等追问）；未列出的 P4 默认维度（系列/设备/优化建议等）**不强行追加**，除非用户要求。

| 用户 Sheet（常见表述） | `google-analysis` section      | 读法（schemaVersion 3）    |
| ---------------------- | ------------------------------ | -------------------------- |
| 账户概览 / 执行摘要    | `overview`                     | `record`（汇总维度）       |
| 每日报告 / 每日趋势    | `daily-metrics`                | `items[]`                  |
| 关键字 / 关键词报告    | `keywords`                     | `items[]`                  |
| 搜索字词 / 搜索词报告  | `search-terms`                 | `items[]`                  |
| 国家 / 地域 / 地区报告 | `geographic`                   | `items[]`                  |
| 受众 / 受众分布        | `audience`                     | `items[]`（`audience` / `audienceName`） |
| 广告系列（若用户要）   | `campaigns`                    | `items[]`                  |
| 设备（若用户要）       | `devices` 或 `campaign-device` | `items[]`；OKKI 口径用后者 |

**一次拉齐示例**（用户要 5 Sheet：概览+每日+关键词+搜索词+国家）：

```bash
mkdir -p ./snap-p4
siluzan-tso list-accounts -m Google -k <id> --json-out ./snap-p4

siluzan-tso google-analysis -a <id> --start <S> --end <E> --json-out ./snap-p4 \
  --sections overview,daily-metrics,keywords,search-terms,geographic
```

落盘文件名以 stdout 摘要 `results[].file` 为准（常含 `_<start>-<end>` 后缀），**禁止**硬编码 `overview.json`。

---

## outline → 脚本：禁止猜的字段名

以下「直觉名」在 **schemaVersion 3** 落盘中**不存在**或易错——须以当次 `*.outline.txt` 为准：

| 维度              | ❌ 禁止猜                                            | ✅ outline 真实字段                                                                                        |
| ----------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `overview`        | `currentPeriod.activeDays`、`previousPeriod.activeDays`、`currentPeriod.averageDailyCost`、`*.conversionsValue` | `record.activeDays`、`record.averageDailyCost`（只在 **record 根**。上期活跃天数另拉上期 `daily-metrics` 数 `spend>0` 天数）。period 块没有转化价值，见「转化价值环比」 |
| `keywords`        | `keywordText`、`status`、`matchType`（单独作展示列） | `keyword`、`userStatus`、`keywordMatchTypeZh`（或 `keywordMatchType`）                                     |
| `search-terms`    | `query`                                              | `searchTermText`；匹配类型用 `matchTypeZh`；状态用 `queryTargetingStatusZh`                                |
| `geographic`      | `geoName`、`countryCriterionIdName`                  | `countryOrRegion`、`countryNameZh`、`countryCode`                                                          |
| 全维度 CTR/转化率 | 已是 0~100 的百分数                                  | `ctr` / `conversionRate` 为 **0~1 小数**；Excel 写入原值 + 单元格 `0.00%`，或文案 `(v*100).toFixed(2)+'%'` |

**数据访问统一规则**（outline 头部注释已写明）：

- `record !== null` → 读 `record`（如 `overview`）
- 否则 → 读 `items[]`

---

## 转化价值环比（核心指标必做）

`overview.currentPeriod` / `previousPeriod` **没有** `conversionsValue`。账户级「转化价值 / 单转化价值 / ROAS」只从 **`campaigns` 的 `items[]`** 汇总。消耗、点击、转化次数、CTR、CPC、CPA 的环比仍读 overview 的 `previousPeriod`。

终稿核心指标（或等价的本期 vs 上期表）出现这三行时，**必须**再拉等长上期的 `campaigns`，两期用同一公式。

**先看后台有没有返回**：以当次 `campaigns-*.outline.txt` / 行上是否出现 `conversionsValue` 为准。有字段 → 按下面公式汇总填数（值为 0 也如实写 0，不要改成「—」）；**整批都没有该字段** → 写「未返回」，禁止用转化次数×1、固定客单或其它维度去估。上期同理：上期 campaigns 有字段才填上期三格，禁止用本期去估。

**上期窗口**（与 Web `calcPrePeriodTimeRange` 相同，含首尾）：

- 本期天数 `N = end − start + 1`（日历日）
- 上期结束 = 本期开始的前一天；上期开始 = 上期结束再往前 `N − 1` 天
- 例：本期 `2026-10-16` ~ `2026-10-28`（13 天）→ 上期 `2026-10-03` ~ `2026-10-15`

```bash
mkdir -p ./snap-p4-prev
siluzan-tso google-analysis -a <id> --start <prevStart> --end <prevEnd> \
  --sections campaigns --json-out ./snap-p4-prev
```

落盘后先 Read 上期 `campaigns-*.outline.txt`，再在脚本里读 `items[]`：

```javascript
const sum = (rows, key) => rows.reduce((a, r) => a + (Number(r[key]) || 0), 0);
function valueKpis(items) {
  const value = sum(items, "conversionsValue");
  const conversions = sum(items, "conversions");
  const spend = sum(items, "spend");
  return {
    conversionsValue: value,
    // 单转化价值；转化次数为 0 时单元格写「—」
    valuePerConversion: conversions > 0 ? value / conversions : null,
    // ROAS；花费为 0 时单元格写「—」
    roas: spend > 0 ? value / spend : null,
  };
}
```

禁止对行上的 `conversionsValuePerCost` 再平均（那是行级「转化价值/费用」，不是账户 ROAS）。

关键词、搜索字词表的转化价值读各自行的 `conversionsValue`（账户币种），ROAS = 该值 / 该行 `spend`。禁止把系列汇总摊到词上，也禁止用转化次数估算。设备、每日趋势的 outline 若没有 `conversionsValue`，该列写「该维度未返回」。关键词或搜索字词当次 outline 也没有该字段时同样写「未返回」。上期 `campaigns` 拉数失败时，账户级三格写明原因，不要留空。

英文终稿表头：转化价值 → Conversion value，单转化价值 → Value / conversion，ROAS 保持 ROAS。

---

## 禁止的数据探查方式

写 Excel 脚本**之前**，不得用以下方式「预览」业务 JSON（与 `agent-conventions.md`、`tips.md` 一致）：

- `cat …json | python -m json.tool | head`
- 宿主 **Read** 打开 `keywords-*.json`、`overview-*.json` 等落盘业务文件
- 把 JSON 片段贴进对话当字段依据

**允许**：Read `*.outline.txt`；脚本 `console.log` 打印行数 / 首行抽样 / 汇总 totals（stdout 给 Agent 核对）。

---

## Excel 版式（无运营固定样表时的最小约定）

用户未指定表头时，可按业务语义建 Sheet，但须满足：

1. **Sheet 名**与用户要求一致（如 `账户概览`、`每日报告`、`关键字报告`、`搜索字词报告`、`国家报告`）。
2. **首行或 R2** 含统计区间 + 币种（与 `list-accounts` 一致）。
3. **列表 Sheet**：R1 为表头；列名与 outline 字段含义对应，不造 outline 中不存在的列。
4. **数值**：金额 2 位小数；`ctr`/`conversionRate` 按上文 0~1 口径；禁止对 JSON 比率再 ÷100。
5. **所有 ID 列写字符串（文本）**：账户/系列/组/关键词/地域等 id 用 `String(id)` + 文本格式（`exceljs` `numFmt: '@'`）；**禁止**写成数字（防科学计数法/丢精度）。见 `agent-conventions.md`。
6. 某维度拉数失败：该 Sheet 写 `[ 数据不可用：<原因> ]`，禁止留空或编造。
7. **样式（必须）**：脚本 `import` `report-templates/excel-style-kit.mjs`，用 `createExcelWorkbook({ accent: "google" })` + `titleBar`/`tableHeader`/`dataRow` 等组件搭版面，**禁止**裸写无样式单元格。规范见 `report-templates/excel-style-guide.md`。

有 OKKI 固定话术时改走 **P6**（`okki-weekly-google-client.md`），**不**用本文。

---

## 交付前自检（P4 Excel 专用）

对照 `references/core/agent-conventions.md` §七 表 A/B/C，并额外确认：

- [ ] `google-analysis` 的 `accountId`（stdout 摘要）= 用户要求的 `mediaCustomerId`
- [ ] 每个 Sheet 列均能在对应 `*.outline.txt` 中找到字段源
- [ ] 脚本 stdout 打印的 `itemCount` 与 Excel 数据行数一致（±合计行）
- [ ] 全部 ID 列为文本（非数字类型 / 无科学计数法）
- [ ] 未使用第三方 xlsx Skill 替代本 Skill 拉数与字段口径
- [ ] 核心指标若有转化价值 / 单转化价值 / ROAS：上期来自等长区间的 `campaigns` 汇总，不是 overview，也不是「—」

---

## 相关文档

- `google-period-report.md` — 默认维度与可选追加
- `okki-weekly-google-client.md` — OKKI 固定 5 Sheet（P6，`google-analysis okki-render`）
- `references/core/tips.md` — 摘要 → outline → 脚本
- `references/core/playbooks.md` — P4 步骤卡片
