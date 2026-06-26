# Meta（Facebook）账户 — 周期分析报告

> 统计区间：`{startDate}` ~ `{endDate}`  
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）

> **默认交付物**：一份可打开的、带 ECharts 图表的 **HTML 文件**（如 `meta-period-report.html`）。  
> 用户**未指定格式**时一律走下方 **标准四步流程**；**禁止**仅 Markdown 摘要或纯 JSON 充当终稿。  
> 用户**明确要求 Excel / xlsx** 时，改走 `report-templates/meta-period-report-excel.md` 分支（见文末「Excel 分支」）。

字段口径见 `references/analytics/facebook-analysis-guide.md`。  
**内容丰富度（必读）**：`assets/meta-period-report-rules.md`（对齐 P8 网站诊断：全量建议 + 字数下限 + 7 维清单）。  
Agent JSON Schema：`assets/meta-period-report.schema.json`。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                                    |
| ---------------- | ------------ | ------------------------------------------------------------------------------------------------------- |
| **1. 拉数**      | Agent 调 CLI | `facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb`                                  |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`），完成筛选、聚合、排序与洞察           |
| **3. 写 JSON**   | Agent        | 按本纲要撰写 `meta-period-report.json`（`meta` / `narrative` / 可选 HTML 扩展字段）                     |
| **4. 渲染 HTML** | CLI          | `facebook-analysis render` — **校验 JSON 必含字段**，缺项报错不生成 HTML；**禁止** Agent 手写/拼接 HTML |

```bash
# 步骤 1
siluzan-tso facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb \
  --sections overview,ad-sets,platform,country,audience

# 步骤 4（步骤 2～3 完成后）
siluzan-tso facebook-analysis render \
  --data ./meta-period-report.json \
  --snapshot-dir ./snap-fb \
  --out ./meta-period-report.html
```

`--snapshot-dir` 与步骤 1 的 `--json-out` 同目录；CLI 自动合并 KPI、平台/国家/受众图表与表格（Agent JSON 已有字段不覆盖）。

---

## Excel 分支（仅当用户指定 Excel / xlsx）

用户说「要 Excel」「导出 xlsx」「按业务 Excel 模板」等时：

1. 步骤 1～3 **与 HTML 流程相同**（拉数 → 分析 → 写 `meta-period-report.json`）。
2. **步骤 4 改为**：Agent 执行 **node/python 脚本**（如 `openpyxl` / `exceljs`）读取快照 JSON + `meta-period-report.json`，按 `meta-period-report-excel.md` 写出 `.xlsx`。
3. **不要**调用 `facebook-analysis render`（除非用户同时要 HTML + Excel）。
4. **禁止**假设存在 `siluzan-tso … excel` 子命令。

版式与 5 Sheet 结构见 **`report-templates/meta-period-report-excel.md`**。

---

## 与原业务（TSO / Skill）对齐

| 环节              | 实现                                  |
| ----------------- | ------------------------------------- |
| CLI 拉数          | 步骤 1                                |
| Agent 分析 + 撰写 | 步骤 2～3 → `meta-period-report.json` |
| **HTML 终稿**     | 步骤 4 → `facebook-analysis render`   |
| **Excel 终稿**    | 仅用户指定时 → Agent 脚本写 xlsx      |

模板源码：

- `report-templates/meta-period-report.html` — 结构与样式（对齐深度分析月报）
- `report-templates/meta-period-report.runtime.js` — 可选外链运行时（逻辑已内联于 HTML；ECharts 渲染 + 章节 DOM 拼装）

`render` 会向输出目录写入 HTML + `meta-period-report.runtime.js`，并注入 `window.__META_PERIOD_REPORT__`。  
传 `--snapshot-dir` 时 CLI 自动从快照合并 KPI、平台/国家/受众图表数据、广告组与受众表格（Agent JSON 中已有字段不覆盖）。

---

## Excel 五 Sheet 与 CLI 维度（默认周期报告）

| #   | Excel Sheet    | 报告章节                                   | CLI `--sections`               | 后端 Section        |
| --- | -------------- | ------------------------------------------ | ------------------------------ | ------------------- |
| 1   | **总数据**     | 账户 KPI + 叙事（整体/区域/国家/优化建议） | `overview`                     | OverviewSectionData |
| 2   | **广告组数据** | 区域组对比表（leads-欧洲/拉美/亚洲）       | `ad-sets`（别名 `campaigns`）  | AdSetSectionData    |
| 3   | **平台数据**   | Facebook vs Instagram                      | `platform`（别名 `devices`）   | PlatformSectionData |
| 4   | **国家数据**   | 国家/地区排行                              | `country`（别名 `geographic`） | CountrySectionData  |
| 5   | **受众数据**   | 年龄 × 性别矩阵                            | `audience`                     | AudienceSectionData |

**Excel 默认不含、按需追加：**

| 章节       | CLI                            | 何时追加               |
| ---------- | ------------------------------ | ---------------------- |
| 广告创意   | `creative`（别名 `ads`）       | 用户要创意表或 DC 素材 |
| 原生素材   | `material`（别名 `materials`） | Dynamic Creative 账户  |
| _按日趋势_ | —                              | 接口无                 |
| _关键词_   | —                              | 不适用                 |

与 Google 8 章对照见 `facebook-analysis-guide.md`。

**可选追加（执行拉数前可询问用户）：**

| 维度        | CLI                            | 何时追加                                 |
| ----------- | ------------------------------ | ---------------------------------------- |
| DC 原生素材 | `material`（别名 `materials`） | 用户要素材 Tab 或账户为 Dynamic Creative |

---

## 拉数（默认 5 个数据维 = Excel 五 Sheet，一次批拉）

```bash
mkdir -p ./snap-fb
siluzan-tso facebook-analysis -a <mediaCustomerId> --start <s> --end <e> --json-out ./snap-fb \
  --sections overview,ad-sets,platform,country,audience
```

- 含创意：加 `creative`；全 7 数据维（含 `material`）：省略 `--sections`。
- 国家 Top 10：同上命令加 `--limit 10`。
- 账户 ID：数字或 `act_<数字>`；读 `report-manifest-<id>.json` 与各 `<section>-<id>.json`。
- **勿**用 `report meta-overview` 代替本流程（仅 legacy 单维总览）。

---

## 各章撰写要求（对齐 Excel 总数据 Sheet）

### 1. 整体表现（`narrative.overall`）

- 数据源：`overview-<id>.json` → `currentPeriod`（可选对比 `previousPeriod` 写环比）。
- **1 段话**必含：花费、**结果**（`results`）、CPL（`costPerResult`）、覆盖、展示、频次。
- 元信息注明：`resultType`、`attributionSetting`（写入 `meta`）。
- **勿写** overview 顶层 `totalCost`/`balance`/`optimizationScore`。

### 2. 区域报告（`narrative.regional[]`）

- 数据源：`ad-sets-<id>.json` → `adGroups[]`。
- **每个广告组 1 段**（如 leads-欧洲 / leads-拉美 / leads-亚洲）：CPL、线索数、覆盖、频次、效率判断。
- 表格列对齐 Excel：系列名、组名、覆盖、展示、频次、归因、成效类型、成效、花费、单次成效费用。

### 3. 国家报告（`narrative.country`）

- 数据源：`country-<id>.json` → `countries[]`。
- **1 段话**：最低/最高 CPL 国家、中间梯队；表格按花费或 CPL 排序展示。

### 4. 优化建议（`narrative.recommendations[]` + `supplementaryRecommendations` + `priorityPlan`）

**固定 4 条标题**（`narrative.recommendations[]`，每条 content **≥150 字**，须引用当次 CPL/国家/组名）：

| 标题         | 内容要点                                           |
| ------------ | -------------------------------------------------- |
| 简化表单问题 | 结合高频次高 CPL 市场；字段缩减至 3 项；写预期影响 |
| 区域调整     | 各广告组语言/市场策略（土/葡/德等）；加减仓名单    |
| 预算重构     | 具体比例（如 4:3:3）、测试周期、CPL 阈值优胜劣汰   |
| 素材建议     | 分平台/分市场；素材套数、IG 短视频、FB 形态        |

**另须** `supplementaryRecommendations` **7 维**（预算、平台、地域、受众、创意、频次、接口限制）与 `priorityPlan`（高/中/低各 ≥2 条）。细则见 **`assets/meta-period-report-rules.md`**。

### 5. 平台数据（Sheet3 表 + 可选 `sections.platform.insight`）

- 数据源：`platform-<id>.json` → 按 `publisherPlatform` 汇总（Excel 仅平台列）。
- 版位细拆（`platformPosition`）为 HTML 扩展，Excel 不要求。

### 6. 受众数据（Sheet5 表）

- 数据源：`audiences[]`；`age`、`gender`。
- 含 `unknown` 性别或零成效行时标注「样本不足」。

### 可选：广告创意 / 原生素材

- 仅当用户追加拉取 `creative` / `material`。
- **勿**加总各行 `results` 与 overview 对比。

### HTML 深度分析扩展（**默认交付必填**，Excel 不含）

用户未指定 Excel 时，除 `narrative` 外 **必须** 填写（字数见 `meta-period-report-rules.md` §四）：

- `executiveSummary[]`：**3～5 段**「为什么」解读（每段 ≥80 字）
- `healthDiagnosis`：三阶段 + **4 张四问卡片** + **≥6 行**红绿灯表（③ 该加还是该减；可省略 `scorecard`，render 时由 `--snapshot-dir` 自动补全）
- `sections.platform/country/adSets.insight`：各 **≥200 字**
- `sections.audience`：`goldenProfile` ≥3 条 + `antiProfile` ≥2 条
- `sections.landingPage.rows`：≥3 行
- `abTests`：≥3 个实验；`actionChecklist`：today/thisWeek/thisMonth 非空

---

## 口径速记

| 展示           | 字段                                |
| -------------- | ----------------------------------- |
| Meta「结果」   | `results`                           |
| 单次成效费用   | `costPerResult`                     |
| 业务转化 / CPA | `conversions` / `costPerConversion` |
| CTR            | `ctr` × 100 → %                     |

---

## Agent JSON 结构（`meta-period-report.json`）

完整 Schema：`assets/meta-period-report.schema.json`。Excel 必含字段：

| 字段                               | 必填           | 说明                                                            |
| ---------------------------------- | -------------- | --------------------------------------------------------------- |
| `meta`                             | 推荐           | 账户名、周期、`resultType`、`attributionSetting`、`generatedAt` |
| `kpis`                             | 可省略         | 账户 KPI 行；由 `--snapshot-dir` 从 `overview` 合并             |
| **`narrative.overall`**            | **Excel 必含** | 整体表现 1 段                                                   |
| **`narrative.regional[]`**         | **Excel 必含** | `{ adGroupName, text }` 区域报告                                |
| **`narrative.country`**            | **Excel 必含** | 国家对比 1 段                                                   |
| **`narrative.recommendations[]`**  | **必含**       | 固定 4 条，每条 ≥150 字                                         |
| **`supplementaryRecommendations`** | **必含**       | 7 维数据驱动建议                                                |
| **`priorityPlan`**                 | **推荐**       | 高/中/低各 ≥2 条；HTML 强烈建议填写                             |
| `tables` / `charts`                | 可省略         | Sheet2～5；由快照自动汇总                                       |
| `executiveSummary`                 | **HTML 必填**  | 3～5 段深度摘要                                                 |
| `healthDiagnosis`                  | **HTML 必填**  | 四问 + 红绿灯表（`scorecard` 可由 CLI 从快照自动补全）          |
| `sections.*.insight`               | **HTML 必填**  | 各维度 ≥200 字                                                  |
| `abTests` / `actionChecklist`      | **HTML 必填**  | ≥3 实验 + 三列行动清单                                          |

---

## 相关文档

| 文档                                                | 用途                                                |
| --------------------------------------------------- | --------------------------------------------------- |
| **`report-templates/meta-period-report-excel.md`**  | **Excel 五 Sheet 规格（业务模板基准）**             |
| `assets/meta-period-report.schema.json`             | Agent JSON Schema                                   |
| `references/analytics/facebook-analysis-guide.md`   | 字段、Google 对照、建议清单                         |
| `report-templates/meta-account-diagnosis-report.md` | 深度诊断（在可用 Section 内尽量对齐 Google 诊断章） |
| `report-templates/REPORT-WORKFLOW.md`               | 通用六步流程                                        |
