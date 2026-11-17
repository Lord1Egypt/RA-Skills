# OKKI 周报 · Google 客户同步（运营模板）

> **触发话术（等价即可）**  
> `使用okki周报模板生成<账户名或ID>，<YYYY-MM-DD>--<YYYY-MM-DD>的投放报告`  
> 同义：`OKKI 周报`、`okki 周报模板`、`运营 OKKI 周报`。  
> **媒体**：当前模板仅规范 **Google**（`mediaCustomerId`）。其他媒体用各自 `*-period-report.md`。  
> **Excel 版式基准**：与运营样表《**数据复盘分析**》类 xlsx 对齐（如 `2025.12数据复盘分析.xlsx`）；工作簿 5 个 Sheet、顺序与表头以下文规范为准。
>
> **默认交付（硬性，缺文件 = 任务未完成）**：磁盘上的 **5 Sheet `.xlsx`**（由 `google-analysis okki-render` 生成）+ 对话内客户话术。  
> 「表格形式 / 表格 / 各维度表格 / 表 / 做成表」= **Excel `.xlsx`**，**不是**对话 Markdown 表，**不是**手写 HTML/PDF。  
> 仅当用户明确「只要话术 / 不要文件 / 不要 Excel」时才省略 xlsx。  
> **禁止**：用对话 Markdown 表、手写 HTML、PDF 代替 `.xlsx`；**禁止** Agent 手写 / 脚本写 xlsx。话术由 Agent 按下文「对外客户话术」填写，**不要**另写脚本生成话术。

## Contents

- 须先确认
- 标准四步流程（拉数 → 写 JSON → okki-render）
- 拉数（一次目录）
- xlsx 版式规范（由 CLI 锁死）
- 对外客户话术（默认 7 条，一条一行）
- 复盘小结（Excel「数据复盘」区块 / 对内补充）
- 与 `google-period-report.md` 的差异

---

识别到上述意图时：**不要**再走 `google-period-report.md` 的「默认 10 章 + 追问追加」流程；按本文固定维度拉数，`okki-render` 出 5 Sheet `.xlsx`。**先 `okki-render` 再发话术**；没有 `.xlsx` 路径不得收口。发给用户的话术默认就是下文那个代码块：只换数字，不换行首。用户本轮另给了全文或点名改某一条，才改被点名的部分。

---

## 须先确认

1. **账户**：`mediaCustomerId` 来自 `list-accounts -m Google -k <用户原样账户号>`（`928-780-1878` 可原样，CLI 去连字符），禁止猜 ID；**禁止**无 `-k` 拉默认 20 条后判定未绑定。
2. **统计区间**：`--start` / `--end`（用户未给齐时按 SKILL 反问；授权默认时可用「上一完整自然周」白名单并写明）。
3. **询盘口径**：默认使用区间内 `conversions`（转化次数，来自 `stats` 或 `overview`）。若运营定义为某类转化，须在首段脚注说明（必要时补拉 `google-analysis --sections conversion-actions` 仅作说明）。
4. **日期写法**：`2026.4.1`、`2026/4/1` 等先规范为 `YYYY-MM-DD`（如 `2026-04-01`）再传 `--start` / `--end`。
5. **交付**：默认 **客户话术 + 5 Sheet `.xlsx`（xlsx 必产，由 `okki-render` 写出）**。「表格形式」一律当 Excel。仅用户明确只要可复制话术、不要文件时，才省略 xlsx。话术按下文默认 7 条填写。

---

## 标准四步流程（拉数 → 写 JSON → okki-render）

| 步骤 | 执行者 | 动作 |
| --- | --- | --- |
| **1. 拉数** | Agent 调 CLI | 下方固定命令组合，同一 `--json-out` 目录 |
| **2. 分析** | Agent | 用 **node/python 脚本**读落盘 JSON（先 outline 再 JSON），完成筛选/聚合/洞察 |
| **3. 写 JSON** | Agent | 按 `assets/okki-weekly-report.schema.json` 撰写 `okki-weekly-report.json`：**只写 `meta` + `narrative`**；表格留给步骤 4 合并 |
| **4. 渲染 xlsx** | CLI | `google-analysis okki-render` — **校验 5 Sheet 表末分析 + 账户 Sheet 固定 5 维数据复盘**，缺项报错不生成文件；**禁止** Agent 手写 xlsx |

```bash
siluzan-tso google-analysis okki-render \
  --data ./okki-weekly-report.json \
  --snapshot-dir ./snap-okki \
  --out ./okki-weekly-report.xlsx
```

`okki-weekly-report.json` 顶层结构：

- `meta`：`accountId`（必填）/ `accountName` / `currency` / `startDate` / `endDate`；日期可由 `--snapshot-dir` 补空。
- `narrative`（**Agent 必填，唯一由 Agent 撰写的内容**）：
  - `sheetAnalysis.{campaigns,keywords,searchTerms,devices,geo}`：每个 Sheet 各 `{summary[]（≥1）, suggestions[]（≥1）}`。**表为空也必须写**（例如「本周期无搜索词，暂无加词/否词建议」）。
  - `review.{account,keywords,searchTerms,devices,geo}`：账户 Sheet「数据复盘」固定 5 维，每维 `{overview, summary, suggestion}` 均非空。
- `tables` / `kpis`：Agent 可省略；**render 以快照覆盖**。设备/国家只认 `campaign-device` / `geo-targeted`。
- `facts.devices`：render **合并后**才写入，写 JSON 时还没有这组数。设备消耗/占比必须在写 `narrative` 前由脚本从 `campaign-device` 累加（见下方「拉数」）。
- `campaign-device` 的 `deviceType` 字面量是 **`Desktop` / `Mobile` / `Tablet`**（Title Case）或中文「计算机 / 移动设备 / 平板」。**禁止** `totals.get("DESKTOP")` / `.get("MOBILE")`（键对不上就是 0，会写成「消耗¥0」）。`okki-render` **原样画出** Agent 的设备建议，不改写口吻。

**禁止**：自己写 Node/Python 出 xlsx、用 Markdown 表代替、跳过 `okki-render`。`okki-render` 失败时按 stderr 缺项补 JSON 后重跑，不得改用手写表。

---

## 拉数（一次目录）

同一目录落盘（示例 `./snap-okki`）：

```bash
mkdir -p ./snap-okki

siluzan-tso list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-okki

siluzan-tso stats -m Google -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-okki

siluzan-tso balance -m Google -a <mediaCustomerId> --json-out ./snap-okki

siluzan-tso google-analysis -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-okki \
  --sections overview,campaigns,keywords,search-terms,campaign-device,geo-targeted
```

**说明**：

- `stats`：区间消耗 / 曝光 / 点击 / 转化 / CTR / CPC，与账户级周报摘要对齐；金额用 `*Display` 或文档规定的展示字段。
- `balance`：**当前**余额（非历史快照），话术写「截至查询时点」。
- 「设备」Sheet 用 **`campaign-device`**（按系列拆行），不要用账户级 `devices`。
- 「国家」Sheet **必须**用 **`geo-targeted`**（当前仍在投放的定位，和 Google「地理位置报告」一致）。账户中途改过国家时，**不要**用 `campaign-geo-matched`（相符地理位置，会把已经删掉的国家也算进这个日期区间），也不要用 `geographic` / `campaign-geo`（后者还会带上已移除系列的历史定位）。落盘文件名为 `campaign-device-<id>.json`、`geo-targeted-<id>.json`。
- **设备合计（写 narrative 前必做）**：按 `deviceType` **分类累加** `spend` / `conversions`，不要用原始字面量当字典键。生产常见值是 `Desktop` / `Mobile`，不是 `DESKTOP` / `MOBILE`。

```js
function deviceKind(deviceType) {
  const raw = String(deviceType ?? "");
  const lower = raw.toLowerCase();
  if (raw.includes("移动") || lower.includes("mobile")) return "mobile";
  if (raw.includes("平板") || lower.includes("tablet")) return "tablet";
  if (raw.includes("计算机") || raw.includes("电脑") || lower.includes("desktop") || lower.includes("computer")) {
    return "desktop";
  }
  return "other";
}
// 正确：acc[deviceKind(row.deviceType)].spend += row.spend
// 错误：totals.get("DESKTOP") / totals["MOBILE"]  → 键对不上，得到 0
```

占比用「该类费用 ÷ 设备费用合计」，不是行数或展示次数。桌面费用 ≥ 移动时，不要写「移动端为主要消耗 / 移动端占比高」。
- TopN、占比、洞察在写 `narrative` 前由脚本对 JSON 完成，禁止心算。
- 写 JSON 前先读各 `<section>-<id>.outline.txt` 再读 `.json`。
- 合计行、CTR/CPA、日期标题、Sheet 列顺序由 `okki-render` 计算，Agent 不要往 JSON 里填表格行。

---

## xlsx 版式规范（由 CLI 锁死，Agent 不必重写）

工作簿 → Sheet 名（须完全一致）→ 版式。**不**单独建「广告系列」Sheet（系列表在 `账户报告` 内）。状态枚举若为英文须转中文。

### 数值格式（强约束）

- **所有数值列一律保留 2 位小数**：金额、CPC、每次转化费用、预算、点击率、转化率、互动率等。
- 客户话术 / 文案中的 `x%`：`(v * 100).toFixed(2) + "%"`。

### 点击率 / 转化率 / 互动率

> **2026-05 起 CLI 已统一归一**（manifest `schemaVersion ≥ 2`）：所有 `<section>-*.json` 中的 `ctr` / `conversionRate` 一律为 **0~1 小数**（如 `0.10` = 10.00%）。`schemaVersion 3` 起行数据统一在 `items[]`、汇总在 `record`。详见 `references/analytics/account-analytics.md`「指标字段对照」「落盘 JSON 统一信封」。

| 场景                                              | 处理                                                                       |
| ------------------------------------------------- | -------------------------------------------------------------------------- |
| 写入 Excel **0~1 小数列**（点击率/转化率/互动率） | 直接写入 JSON 数值（**禁止**再 ÷100）                                      |
| 写客户话术 / 文案的 `x%`                          | `(v * 100).toFixed(2) + "%"`                                               |
| `interactionRate`（字符串）                       | `parseFloat(row.interactionRate)` 后按数值字段使用（同样 0~1 小数）        |
| `interactions === 0` / `null`                     | **平均费用**（`spend / interactions`）与 **互动率** 列填 **`—`**，禁止除零 |

### 工作簿级

| 顺序 | Sheet 名   | 数据来源                                                                             |
| ---: | ---------- | ------------------------------------------------------------------------------------ |
|    1 | `账户报告` | `campaigns` + `narrative.review`（5 维复盘，`okki-render` 写入）                     |
|    2 | `关键词`   | `keywords`                                                                           |
|    3 | `搜索词`   | `search-terms`                                                                       |
|    4 | `设备`     | **`campaign-device-*.json`**（按系列/组拆行）                                        |
|    5 | `国家`     | **`geo-targeted-*.json`**（当前仍在投放的地理位置，按系列/地域拆行；不含已移除国家） |

### 各 Sheet 共同版式

- **R1（A1）**：报告标题（见各 Sheet 表）；建议合并单元格横跨该 Sheet R3 表头全部列。
- **R2（A2）**：统计区间，中文可读：`YYYY年M月D日 - YYYY年M月D日`。
- **R3**：表头（列名、顺序须与下表一致）。
- **R4 起**：数据行；列宽、自动筛选、首行冻结、降序排序为可选，**不得**因此改数。
- **表末「分析」**（强约束）：数据区（含「合计」行若有）结束后 **留白 1～2 行**，必须写入 **「分析」** 标题区块；须含 **总结**（引用**当 Sheet 表格**中的数字，可 TopN / 占比 / 与合计行对比）+ **建议**（1～3 条可执行项）；禁止编造、禁止留空；各 Sheet 具体分析要点见下表「表末「分析」」行。
- **百分比列**：样表为 0~1 小数（如 7.95% 存 `0.08`）；与运营约定二选一，**禁止**同一文件混用。
- **金额**：与 `references/analytics/account-analytics.md` 一致；`campaigns.budgetAmountYuan`、`spend`、`averageCpc`、`costPerConversion` 均为元，可直接写入。

---

### Sheet `账户报告`

| 行               | 内容                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1               | `广告系列报告`（如运营改名，可改文案但 Sheet 名仍为 `账户报告`）                                                                                                                                                                                                                                                                                                                                                |
| R2               | 统计区间                                                                                                                                                                                                                                                                                                                                                                                                        |
| R3（A→K，11 列） | `广告系列` \| `预算` \| `费用` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `所有转化次数` \| `转化次数` \| `每次转化费用` \| `转化率`                                                                                                                                                                                                                                                      |
| R4…              | 来自 `campaigns-*.json` 的 `items[]`（`schemaVersion 3` 行统一在 `items`）：`campaignName`、`budgetAmountYuan`（元）、`spend`、`impressions`、`clicks`、`ctr`（已归一直接写入「点击率」）、`averageCpc`、`allConversions`→「所有转化次数」、`conversions`→「转化次数」、`costPerConversion`、`conversionRate`（已归一直接写入「转化率」）；缺 `allConversions` 时与「转化次数」同值或填 `0` / `—`，并在脚注说明 |
| 末行「合计」     | **广告系列**列填 `总计`；**预算**列填 `--`；**展示 / 点击 / 所有转化次数 / 转化次数 / 费用** 做列求和；**点击率** = 合计点击 ÷ 合计展示；**转化率** = 合计转化 ÷ 合计点击（**禁止**用合计转化 ÷ 合计展示）；**每次转化费用** = 合计费用 ÷ 合计转化（转化为 0 时填 `—`）；禁止对各行比率取算术平均                                                                                                               |
| 表末「分析」     | **总结**：Top 消耗系列及费用占比、合计/系列 CTR·CPC·CPA 水平、预算与费用对比（预算跑满/空耗/超支系列）；可对照 stats/overview 账户级指标。**建议**：预算增减、暂停或放量具体系列（须写系列名 + 引用表中数字），1～3 条                                                                                                                                                                                          |

表下**留白若干行**后写 **「数据复盘」**（账户 Sheet 汇总向，与各 Sheet 表末「分析」互补，数字须一致）：

- 首行标题：`{结束日所在月份}月份数据复盘：`（例：`12月份数据复盘：`）。
- 5 条结构化要点（**账户 Sheet 总览**；关键词/搜索词/设备/国家细节以各 Sheet **表末「分析」** 为准，此处可摘要呼应、**不得矛盾**）：
  1. **账户层级**：整体消耗、展示、点击、点击率与 3% 基准对比、询盘/转化数、平均询盘成本（数据来自 stats/overview 与上表合计）。
     总结：
     建议：
  2. **关键词层级**（摘要；详述见 Sheet `关键词` 表末分析）：高转化词、高消耗低转化词、出价/竞争力。
     总结：
     建议：
  3. **搜索字词层级**（摘要；详述见 Sheet `搜索词` 表末分析）：高意向词、否词与加词。
     总结：
     建议：
  4. **设备层级**（摘要；详述见 Sheet `设备` 表末分析）：设备消耗/转化分布。
     总结：
     建议：
  5. **国家层级**（摘要；详述见 Sheet `国家` 表末分析）：地域消耗/转化与调价。
     总结：
     建议：

文案写入 `narrative.review`（每维 `overview` / `summary` / `suggestion`），由 `okki-render` **原样**画到账户 Sheet 底部；缺任一维会拒绝出文件。**不得编造**表中不存在的数字。设备维金额必须与脚本按 `deviceKind` 累加的结果一致。

---

### Sheet `关键词`

| 行               | 内容                                                                                                                                                                          |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1               | `搜索关键字报告`                                                                                                                                                              |
| R2               | 统计区间                                                                                                                                                                      |
| R3（A→L，12 列） | `关键字` \| `匹配类型` \| `广告系列` \| `广告组` \| `费用` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `转化次数` \| `每次转化费用` \| `转化率`          |
| R4…              | `keywords-*.json`：`keywordMatchType`→匹配类型；**关键字列由 render 按匹配类型包符号**（精确/`NEAR_EXACT`→`[词]`，词组/`NEAR_PHRASE`→`"词"`，广泛→裸词；先剥已有 `[]`/`""` 再重包，避免词组却带着 `[]`）；`campaignName` / `adGroupName` 等按 outline；`ctr` / `conversionRate` 已归一，直接写入 |
| 表末「分析」     | **总结**：Top 消耗/转化关键词、高消耗低转化或零转化词、匹配类型（广泛/词组/完全）分布。**建议**：暂停/降价、提价扩量、改匹配或拓词（须写关键词 + 表中费用/转化/CPC），1～3 条 |

---

### Sheet `搜索词`

| 行               | 内容                                                                                                                                                                                                        |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1               | `搜索字词报告`                                                                                                                                                                                              |
| R2               | 统计区间                                                                                                                                                                                                    |
| R3（A→N，14 列） | `搜索字词` \| `匹配类型` \| `已添加/已排除` \| `广告系列` \| `广告组` \| `关键字` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `费用` \| `转化次数` \| `每次转化费用` \| `转化率`       |
| R4…              | `search-terms-*.json`：`queryTargetingStatusZh`（`Added`→已添加、`Excluded`→已排除、`None`→都没有）；无该字段时读 `queryTargetingStatus` 按上表映射，仍无则「—」；**「搜索字词」不包符号**；**「关键字」列按匹配类型包符号**（同关键词 Sheet）；`ctr` / `conversionRate` 已归一，直接写入 |
| 表末「分析」     | **总结**：高意向/高转化搜索词、高消耗但未加为关键词的词、应否定的无关词（对比「已添加/已排除」列）。**建议**：加词、否词、落地页或系列调整（须写搜索词 + 表中数据），1～3 条                                |

---

### Sheet `设备`

| 行               | 内容                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1               | `设备报告`                                                                                                                                                                                                                                                                                                                                                           |
| R2               | 统计区间                                                                                                                                                                                                                                                                                                                                                             |
| R3（A→M，13 列） | `设备` \| `级别` \| `广告系列` \| `出价调整` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `费用` \| `所有转化次数` \| `转化次数` \| `每次转化费用` \| `转化率`                                                                                                                                                                                   |
| R4…              | `campaign-device-*.json`（`items[]`）：`deviceType`→设备；`campaignName` / `adGroupName`→「广告系列」等；`allConversions`→「所有转化次数」；`conversions`→「转化次数」；`ctr` / `conversionRate` 直接写入；**出价调整**：写 `bidModifierDisplay`（与 Google 后台一致：未设置=`—`，`0.6`=`-40%`）。禁止把倍率当正百分比，禁止把未设置的 `0` 写成 `-100%`；**级别**列按运营约定（如填 `广告系列` 或 `账户`，全文一致） |
| 表末「分析」     | **总结**：各设备消耗与转化占比、系列×设备高消耗组合、移动端 vs 桌面 CPA/CPC 差异。占比按 `deviceKind` 累加费用（见上文），`deviceType` 是 `Desktop`/`Mobile`，不是 `DESKTOP`/`MOBILE`。桌面费用 ≥ 移动时禁止写「移动端为主要消耗 / 移动端占比高」。**建议**：设备出价系数、落地页或系列倾斜（须引用设备类型与表中费用/转化），1～3 条；`okki-render` 不改写建议原文 |

---

### Sheet `国家`

| 行               | 内容                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| R1               | `地理位置报告`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| R2               | 统计区间                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| R3（A→M，13 列） | `地理位置` \| `广告系列` \| `展示次数` \| `互动次数` \| `互动率` \| `费用` \| `平均费用` \| `点击次数` \| `点击率` \| `所有转化次数` \| `转化次数` \| `每次转化费用` \| `转化率`                                                                                                                                                                                                                                                                                                                      |
| R4…              | `geo-targeted-*.json` 的 `items[]`（`schemaVersion 3` 行统一在 `items`）：`countryOrRegion`→地理位置；`campaignName`→「广告系列」；`allConversions`→「所有转化次数」；`conversions`→「转化次数」；**互动次数**→`interactions`，缺省/为 0 时回退 `clicks`（当前定位接口常不回 interactions）；**互动率**→`interactionRate`（字符串须解析）或 `互动次数/impressions`，回退后仍为 0 才填 `—`；**平均费用** = `spend / 互动次数`（同样先 interactions 再 clicks），分母为 0 时填 `—`；`ctr` / `conversionRate` 直接写入；其余列按 outline 映射 |
| 表末「分析」     | **总结**：Top 国家/地区消耗与转化、高消耗低转化地域、系列×地域组合。**建议**：地域加价/降价、排除或单独系列（须写国家/地区名 + 表中费用/转化/CPA），1～3 条                                                                                                                                                                                                                                                                                                                                           |

---

## 对外客户话术（默认结构，填数来自 JSON）

> 话术由 Agent 填数，**不要写脚本生成**。用户没换格式时，下面代码块就是终稿：复制行首，只替换尖括号里的内容。

**发给用户时只有两样东西：**

1. 一行文件路径（xlsx）
2. 下面这一个代码块

代码块外面不要写「本周结论 / 概览 / 发现 / 下周动作」。`agent-conventions.md` 的「结论先行」五步**不用于**这次回复。

```
您好，同步一下谷歌<中文日期>投放的情况：

1、消耗：共消耗<金额>，平均每天消耗<金额>；
2、展示点击：带来<曝光>个曝光，<点击>个点击；
3、点击率：<CTR%>，处于<优秀/正常/偏低>水平（<按下方规则选一条基准>）；
4、平均点击单价：<金额>；
5、转化：记录到网站表单+会话询盘<N>个；直接写邮件咨询和 WhatsApp 咨询无法记录，需贵司自行统计后反馈具体咨询产品和国家，方便广告及时调整；
5.1 有转化的关键词：<词（N 个，CPA 金额）>；
5.2 有转化的国家：<国家（N 个，CPA 金额）>；
6、优化建议：
① <一条可执行建议，点名对象并引用当次数字>
② <同上>
③ <同上>
7、账户余额：<金额>（截至查询时点）。
```

换行是骨架的一部分。`1`～`5`、`5.1`、`5.2`、`7` 各占一行，行末用中文分号 `；`。`6、优化建议：` 单独一行，下面 **3～5 条**用 ①②③④⑤，每条一行。日期写成 `2026年4月1日-4月7日`（同年可省略结束年份），须与 `--start` / `--end` 对应。

`meta.lang` 为 `en` 时改用下面这套行首，仍然只替换尖括号里的数字和对象。`okki-render --lang en` 只翻译 Excel 壳，话术仍由 Agent 按这个代码块填写。

```
Google Ads update for <date range>:

1. Spend: <amount> in total, <amount> per day;
2. Impressions and clicks: <impressions> impressions, <clicks> clicks;
3. CTR: <CTR%>, <strong / normal / low> (<pick one benchmark from the rules below>);
4. Average CPC: <amount>;
5. Conversions: <N> website form and chat leads recorded. Direct email and WhatsApp inquiries are not tracked here — please send back the product and country so we can adjust;
5.1 Converting keywords: <keyword (N, CPA amount)>;
5.2 Converting countries: <country (N, CPA amount)>;
6. Recommendations:
① <one action naming the object and this run's number>
② <same>
③ <same>
7. Account balance: <amount> (as of this check).
```

英文行首必须是：`Google Ads update for`、`1. Spend:`、`2. Impressions and clicks:`、`3. CTR:`、`4. Average CPC:`、`5. Conversions:`、`5.1 Converting keywords:`、`5.2 Converting countries:`、单独一行 `6. Recommendations:`、`7. Account balance:`。

**发出去之前对一下行首**（用户本轮没换格式时，缺一条或改了一个行首都重写这块，不要解释）：

| 行首 | 必须长这样 |
| --- | --- |
| 开头 | `您好，同步一下谷歌` |
| 1 | `1、消耗：` |
| 2 | `2、展示点击：` |
| 3 | `3、点击率：` |
| 4 | `4、平均点击单价：` |
| 5 | `5、转化：` |
| 5.1 | `5.1` 且含「有转化的关键词」 |
| 5.2 | `5.2` 且含「有转化的国家」 |
| 6 | 单独一行 `6、优化建议：`，①②③ 不写在这一行 |
| 7 | `7、账户余额：` |

**这些都算没按格式，改回上面的行首再发：**

- 合成一段，或把 ①②③ 写进第 6 行
- 「一、本周概览」「二、本周发现」「三、下周优化」「四、需要您配合」
- 代码块前先写一段结论、要点、核心发现
- 沿用上一轮、另一个账户、或对话里见过的另一套话术

**用户要换格式时很好改：** 本轮粘贴了全文，或点名「不要 5.1」「第 3 条改成…」，就按用户的写，只动被点名的行。没点名的行仍用默认行首。数字仍来自当次 JSON，缺数写 `[数据不可用：原因]`。不要因为上一轮换过格式，这一轮就继续用旧骨架。

### 填数规则

| 条目 | 数据来源 / 计算 |
| --- | --- |
| 1 消耗 / 日均 | 区间 `spend`；日均 = `总消耗 ÷ 区间日历天数`（含起止日） |
| 2 曝光 / 点击 | `impressions`、`clicks` |
| 3 点击率 | 已是 **0~1 小数**时写 `(ctr * 100).toFixed(2) + "%"`，禁止直接打印成 `0.10%` |
| 3 水平判定 | **搜索消耗 ≥60%**：`<3%` 偏低，`3%～5%` 正常，`>5%` 优秀，括号写「搜索正常水平 3%～5%」。**展示消耗 ≥60%**：`<1%` 偏低，`1%～2%` 正常，`>2%` 优秀，括号写「展示正常水平 1%～2%」。其余写「整体」，并说明依据（如搜索消耗占比）。括号里只留这一句判定，不要把本表规则贴给客户 |
| 4 CPC | `averageCpc`，或 `cost / clicks` |
| 5 转化数 | 默认 `conversions` |
| 5.1 / 5.2 | `keywords` / `geo-targeted` 中 `conversions > 0`，按词或国家合计，最多 5 个，写成「名称（N 个，CPA 金额）」；没有则写「本周期暂无带转化关键词」或「本周期暂无带转化国家/地区」 |
| 6 优化建议 | 同批 JSON，3～5 条，每条单独一行；不额外拉数。用户若限定「只写预算/否词」，按该范围写，条数仍各自成行 |
| 7 余额 | `balance` 当前余额，标注截至查询时点 |

金额、百分比一律 2 位小数。CNY 用 `￥`，USD 用 `$`。

### 用户本轮改骨架时

| 用户说法 | Agent 行为 |
| --- | --- |
| 未提话术样式 / 「按默认 OKKI 话术」 | 用上方 7 条，一条一行 |
| 「话术用我这份：…」（本轮粘贴全文） | 以这份全文为骨架填数；缺项不擅自补回默认条目 |
| 「不要 5.1 / 5.2，其它不变」 | 仍是默认 7 条，只删 5.1、5.2 |
| 「第 3 条只写搜索点击率，基准 4%」 | 只改第 3 条的判定句，数值仍来自 JSON |
| 「按上次那个账户的四段式」 | 仅当用户**本轮**这样说才换骨架；不要自己从历史里捡 |

---

## 复盘小结（Excel「数据复盘」区块 / 对内补充）

每个 Sheet **数据表格末尾**须写当 Sheet **表末「分析」**（见上文各 Sheet 规范）；Sheet `账户报告` 另含跨维度 **「数据复盘」** 总览。

基于同一批 JSON 撰写；与对外话术 **第 6 条优化建议** 可呼应但 **Excel 内须更细**，各 Sheet 数字不得矛盾。

---

## 与 `google-period-report.md` 的差异

| 项       | `google-period-report.md` | 本文 OKKI 周报                                                                                                 |
| -------- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 默认维度 | 8 维 + 主动追问追加       | **固定** `overview,campaigns,keywords,search-terms,campaign-device,geo-targeted` + `stats` + `balance` |
| 输出形态 | 长文分析报告（默认 HTML，`google-analysis render`） | **必产** 5 Sheet `.xlsx`（`google-analysis okki-render`）+ 客户话术（默认 7 条、一条一行）；「表格形式」= Excel；**禁止**对话 Markdown 表 / 手写 HTML / Agent 手写 xlsx / 另写一套话术标题 |
| 典型用户 | 内部分析                  | **发客户**的同步简报                                                                                           |
