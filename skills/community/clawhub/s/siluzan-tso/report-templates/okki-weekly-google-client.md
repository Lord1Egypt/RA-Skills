# OKKI 周报 · Google 客户同步（运营模板）

> **触发话术（等价即可）**  
> `使用okki周报模板生成<账户名或ID>，<YYYY-MM-DD>--<YYYY-MM-DD>的投放报告`  
> 同义：`OKKI 周报`、`okki 周报模板`、`运营 OKKI 周报`。  
> **媒体**：当前模板仅规范 **Google**（`mediaCustomerId`）。其他媒体用各自 `*-period-report.md`。  
> **Excel 版式基准**：与运营样表《**数据复盘分析**》类 xlsx 对齐（如 `2025.12数据复盘分析.xlsx`）；工作簿 5 个 Sheet、顺序与表头以下文规范为准。

识别到上述意图时：**不要**再走 `google-period-report.md` 的「默认 8 维 + 追问追加」流程；按本文**固定维度 + 默认客户话术（可用户自定义）**交付（数据全部来自 CLI 落盘 JSON，见 `references/analytics/account-analytics.md`）。

---

## 须先确认

1. **账户**：`mediaCustomerId` 来自 `list-accounts -m Google -k <id>`，禁止猜 ID。
2. **统计区间**：`--start` / `--end`（用户未给齐时按 SKILL 反问；授权默认时可用「上一完整自然周」白名单并写明）。
3. **询盘口径**：默认使用区间内 `conversions`（转化次数，来自 `stats` 或 `overview`）。若运营定义为某类转化，须在首段脚注说明（必要时补拉 `google-analysis --sections conversion-actions` 仅作说明）。
4. **日期写法**：`2026.4.1`、`2026/4/1` 等先规范为 `YYYY-MM-DD`（如 `2026-04-01`）再传 `--start` / `--end`。

---

## 架构约定 · Excel 由谁生成

- **`siluzan-tso` 不提供**「一键生成 OKKI Excel」的子命令，**也不要**在 CLI 里新增。
- 需交付 Excel 时：由 **Agent（含 WorkBuddy 编排）** 在下列 CLI **`--json-out` 落盘后**，自行编写 **Node.js / Python** 脚本（如 `exceljs`、`xlsx`、`openpyxl`）读取 JSON → 写 `.xlsx`。
- **数值一律来自落盘 JSON，禁止在脚本里写死业务数字。**

---

## 拉数（一次目录）

同一目录落盘（示例 `./snap-okki`）：

```bash
mkdir -p ./snap-okki

siluzan-tso list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-okki

siluzan-tso stats -m Google -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-okki

siluzan-tso balance -m Google -a <mediaCustomerId> --json-out ./snap-okki

siluzan-tso google-analysis -a <mediaCustomerId> --start <S> --end <E> --json-out ./snap-okki \
  --sections overview,campaigns,keywords,search-terms,campaign-device,campaign-geo-matched
```

**说明**：

- `stats`：区间消耗 / 曝光 / 点击 / 转化 / CTR / CPC，与账户级周报摘要对齐；金额用 `*Display` 或文档规定的展示字段。
- `balance`：**当前**余额（非历史快照），话术写「截至查询时点」。
- 「设备」「国家」两 Sheet **必须**用 **`campaign-device` / `campaign-geo-matched`**（按系列/组拆行），**不要**用账户级 `devices` / `geographic`，也**不要**用 `campaign-geo`（定向地理位置，与 OKKI「地理位置报告」口径不一致）。落盘文件名为 `campaign-device-<id>.json`、`campaign-geo-matched-<id>.json`。跨系列汇总在脚本中做。
- 可选：`campaign-geo-matched` 支持 `--cost-greater` / `--click-greater` / `--conversions-greater`（见 `references/analytics/account-analytics.md`）。
- TopN、排序、汇总均在脚本内对 JSON 完成，禁止心算。
- 写脚本前先读各 `<section>-<id>.outline.txt` 再读 `.json`。

---

## xlsx 版式规范

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
|    1 | `账户报告` | `campaigns` + 复盘文案（stats/overview 汇总后 Agent 撰写）                           |
|    2 | `关键词`   | `keywords`                                                                           |
|    3 | `搜索词`   | `search-terms`                                                                       |
|    4 | `设备`     | **`campaign-device-*.json`**（按系列/组拆行）                                        |
|    5 | `国家`     | **`campaign-geo-matched-*.json`**（相符地理位置 Matched locations，按系列/地域拆行） |

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

| 行 | 内容 |
| --- | --- |
| R1 | `广告系列报告`（如运营改名，可改文案但 Sheet 名仍为 `账户报告`） |
| R2 | 统计区间 |
| R3（A→K，11 列） | `广告系列` \| `预算` \| `费用` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `所有转化次数` \| `转化次数` \| `每次转化费用` \| `转化率` |
| R4… | 来自 `campaigns-*.json` 的 `items[]`（`schemaVersion 3` 行统一在 `items`）：`campaignName`、`budgetAmountYuan`（元）、`spend`、`impressions`、`clicks`、`ctr`（已归一直接写入「点击率」）、`averageCpc`、`allConversions`→「所有转化次数」、`conversions`→「转化次数」、`costPerConversion`、`conversionRate`（已归一直接写入「转化率」）；缺 `allConversions` 时与「转化次数」同值或填 `0` / `—`，并在脚注说明 |
| 末行「合计」 | **广告系列**列填 `总计`；**预算**列填 `--`；**展示 / 点击 / 所有转化次数 / 转化次数 / 费用** 做列求和；**点击率** = 合计点击 ÷ 合计展示；**转化率** = 合计转化 ÷ 合计点击（**禁止**用合计转化 ÷ 合计展示）；**每次转化费用** = 合计费用 ÷ 合计转化（转化为 0 时填 `—`）；禁止对各行比率取算术平均 |
| 表末「分析」 | **总结**：Top 消耗系列及费用占比、合计/系列 CTR·CPC·CPA 水平、预算与费用对比（预算跑满/空耗/超支系列）；可对照 stats/overview 账户级指标。**建议**：预算增减、暂停或放量具体系列（须写系列名 + 引用表中数字），1～3 条 |

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

文案由 Agent 据 JSON 撰写，**不得编造**表中不存在的数字。

---

### Sheet `关键词`

| 行 | 内容 |
| --- | --- |
| R1 | `搜索关键字报告` |
| R2 | 统计区间 |
| R3（A→L，12 列） | `关键字` \| `匹配类型` \| `广告系列` \| `广告组` \| `费用` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `转化次数` \| `每次转化费用` \| `转化率` |
| R4… | `keywords-*.json`：`keywordMatchType`→匹配类型；`campaignName` / `adGroupName` 等按 outline；`ctr` / `conversionRate` 已归一，直接写入 |
| 表末「分析」 | **总结**：Top 消耗/转化关键词、高消耗低转化或零转化词、匹配类型（广泛/词组/完全）分布。**建议**：暂停/降价、提价扩量、改匹配或拓词（须写关键词 + 表中费用/转化/CPC），1～3 条 |

---

### Sheet `搜索词`

| 行 | 内容 |
| --- | --- |
| R1 | `搜索字词报告` |
| R2 | 统计区间 |
| R3（A→N，14 列） | `搜索字词` \| `匹配类型` \| `已添加/已排除` \| `广告系列` \| `广告组` \| `关键字` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `费用` \| `转化次数` \| `每次转化费用` \| `转化率` |
| R4… | `search-terms-*.json`：`queryTargetingStatusZh`（`Added`→已添加、`Excluded`→已排除、`None`→都没有）；无该字段时读 `queryTargetingStatus` 按上表映射，仍无则「—」；`ctr` / `conversionRate` 已归一，直接写入 |
| 表末「分析」 | **总结**：高意向/高转化搜索词、高消耗但未加为关键词的词、应否定的无关词（对比「已添加/已排除」列）。**建议**：加词、否词、落地页或系列调整（须写搜索词 + 表中数据），1～3 条 |

---

### Sheet `设备`

| 行 | 内容 |
| --- | --- |
| R1 | `设备报告` |
| R2 | 统计区间 |
| R3（A→M，13 列） | `设备` \| `级别` \| `广告系列` \| `出价调整` \| `展示次数` \| `点击次数` \| `点击率` \| `平均每次点击费用` \| `费用` \| `所有转化次数` \| `转化次数` \| `每次转化费用` \| `转化率` |
| R4… | `campaign-device-*.json`（`devices[]`）：`deviceType`→设备；`campaignName` / `adGroupName`→「广告系列」等；`allConversions`→「所有转化次数」；`conversions`→「转化次数」；`ctr` / `conversionRate` 直接写入；**出价调整**：bidModifier（0.5 表示降低 50%，1.1 表示提高 10%，在表格中分别为 -50%、+10%）；**级别**列按运营约定（如填 `广告系列` 或 `账户`，全文一致） |
| 表末「分析」 | **总结**：各设备（Mobile/Desktop/Tablet 等）消耗与转化占比、系列×设备高消耗组合、移动端 vs 桌面 CPA/CPC 差异。**建议**：设备出价系数调整或系列预算倾斜（须引用设备类型与表中费用/转化），1～3 条 |

---

### Sheet `国家`

| 行 | 内容 |
| --- | --- |
| R1 | `地理位置报告` |
| R2 | 统计区间 |
| R3（A→M，13 列） | `地理位置` \| `广告系列` \| `展示次数` \| `互动次数` \| `互动率` \| `费用` \| `平均费用` \| `点击次数` \| `点击率` \| `所有转化次数` \| `转化次数` \| `每次转化费用` \| `转化率` |
| R4… | `campaign-geo-matched-*.json` 的 `items[]`（`schemaVersion 3` 行统一在 `items`）：`countryOrRegion`→地理位置；`campaignName`→「广告系列」；`allConversions`→「所有转化次数」；`conversions`→「转化次数」；**互动次数**→`interactions`；**互动率**→`interactionRate`（字符串须解析）或 `interactions/impressions`，`interactions` 为 0 时填 `—`；**平均费用 必须** = `spend / interactions`，`interactions` 为 0 / null / undefined 时填 `—`；`ctr` / `conversionRate` 直接写入；其余列按 outline 映射 |
| 表末「分析」 | **总结**：Top 国家/地区消耗与转化、高消耗低转化地域、系列×地域组合。**建议**：地域加价/降价、排除或单独系列（须写国家/地区名 + 表中费用/转化/CPA），1～3 条 |

---

## 对外客户话术（默认结构，填数来自 JSON）

> **默认**：用户未指定话术样式时，使用下方**默认模板**输出终稿。  
> **用户自定义**：用户可（1）粘贴自有话术骨架；（2）要求增删改某几条（如「不要 5.1」「第 3 条改成…」）；（3）指定 CTR 基准或币种展示方式。**自定义时仍须**：数值/百分比一律来自 CLI 落盘 JSON + 脚本计算，禁止编造；缺数据标 `[数据不可用：原因]`，不得留空占位符糊弄客户。

**日期写法（首行）**：`<S>` / `<E>` 转为中文可读，如 `4月1号-4月7号` 或 `2026年4月1日-4月7日`（与用户习惯一致即可，须与 `--start` / `--end` 对应）。

**默认模板**：

```
您好，同步一下谷歌<S>--<E>投放的情况：

1、消耗：共消耗<金额+币种>，平均每天消耗<金额+币种>；
2、展示点击：带来<曝光>个曝光，<点击>个点击；
3、点击率：<CTR%>，处于<优秀/正常/偏低>水平（搜索正常水平 3%～5%，展示正常水平 1%～2%；按账户实际以搜索或展示为主选基准，无法区分时写「整体」并说明依据）
4、平均点击单价：<金额+币种>
5、转化：记录到网站表单+会话询盘<N>个；直接写邮件咨询和 WhatsApp 咨询无法记录，需贵司自行统计后反馈具体咨询产品和国家，方便广告及时调整
5.1 有转化的关键词：<据 keywords / search-terms JSON 填写；无转化则写「本周期暂无带转化关键词」>
5.2 有转化的国家：<据 campaign-geo-matched JSON 填写；无转化则写「本周期暂无带转化国家/地区」>
6、优化建议：<据 campaigns / keywords / search-terms / device / geo JSON 撰写 3～5 条可执行建议，禁止编造数据>
7、账户余额：<金额+币种>（截至查询时点）
```

### 填数规则

| 条目 | 数据来源 / 计算 |
| ---- | ---------------- |
| 1 消耗 / 日均 | `stats` 或 `overview` 区间 `spend`；日均 = `总消耗 ÷ 区间日历天数`（含起止日），脚本计算 |
| 2 曝光 / 点击 | `stats` / `overview` 的 `impressions`、`clicks` |
| 3 点击率 | `overview.record.ctr` 或 `stats` 同级字段；已是 **0~1 小数**，话术 `(ctr * 100).toFixed(2) + "%"`，**禁止**直接打印得到 `0.10%` |
| 3 水平判定 | **搜索为主**（Search 系列占消耗大头）：`<3%` 偏低，`3%～5%` 正常，`>5%` 优秀；**展示为主**：`<1%` 偏低，`1%～2%` 正常，`>2%` 优秀；混合账户说明以哪类为准 |
| 4 CPC | `stats` / `overview` 的 `averageCpc` 或 `cost / clicks` |
| 5 转化数 | 默认 `conversions`（与「须先确认 §3 询盘口径」一致）；括号说明若口径不同须在首段脚注 |
| 5.1 / 5.2 | 从 `keywords` / `campaign-geo-matched` 筛 `conversions > 0`，列词或国家 + 转化数（可 TopN）；用户自定义模板时仍可保留或合并为一条 |
| 6 优化建议 | 同批 JSON，不额外拉数；用户若提供「只写预算/否词」等范围，按用户范围写 |
| 7 余额 | `balance` 当前余额，标注截至查询时点 |

- **所有金额、百分比** 一律 **2 位小数**（与 xlsx 规范一致）。
- 用户自定义模板时：**保留用户条目顺序与措辞**，仅替换 `<…>` 占位或等价位置为 JSON 实数；用户删掉的条目不再输出。

### 用户自定义示例

| 用户说法 | Agent 行为 |
| -------- | ---------- |
| 「按默认 OKKI 话术发客户」 | 用上方默认模板 |
| 「话术用我这份：…」（粘贴全文） | 以用户全文为骨架填数；缺项不擅自补回默认条目，除非用户要求 |
| 「不要 5.1 / 5.2，其它不变」 | 输出默认模板但省略 5.1、5.2 |
| 「第 3 条只写搜索点击率，基准 4%」 | 按用户基准改写判定话术，数值仍来自 JSON |
| 「优化建议只要 3 条 bullet」 | 压缩第 6 条条数，内容仍须有据 |

---

## 复盘小结（Excel「数据复盘」区块 / 对内补充）

每个 Sheet **数据表格末尾**须写当 Sheet **表末「分析」**（见上文各 Sheet 规范）；Sheet `账户报告` 另含跨维度 **「数据复盘」** 总览。

基于同一批 JSON 撰写；与对外话术 **第 6 条优化建议** 可呼应但 **Excel 内须更细**，各 Sheet 数字不得矛盾。

---

## 与 `google-period-report.md` 的差异

| 项       | `google-period-report.md` | 本文 OKKI 周报                                                                                                 |
| -------- | ------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 默认维度 | 8 维 + 主动追问追加       | **固定** `overview,campaigns,keywords,search-terms,campaign-device,campaign-geo-matched` + `stats` + `balance` |
| 输出形态 | 长文分析报告              | **默认客户话术（可自定义）** + Excel 数据复盘 + **多 Sheet Excel（Agent 脚本写）**                                                     |
| 典型用户 | 内部分析                  | **发客户**的同步简报                                                                                           |
