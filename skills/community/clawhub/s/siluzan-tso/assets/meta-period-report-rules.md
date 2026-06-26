# Meta 周期报告撰写规则（Agent 用）

> 对齐 **P8 网站诊断** 的「结构化 + 全量覆盖 + 每条必有建议」思路。  
> 源：业务 Excel 模板（`无锡顺晟Facebook4月报告.xlsx`）+ `meta-period-report.html` 深度分析章节。  
> **禁止**只写 KPI 表、4 条一句话建议或空白占位后交付。

---

## 与网站诊断的对照（为何 FB 报告会显得「建议太少」）

| 网站诊断（P8）                                            | Meta 周期报告（P4-FB）                                                                 |
| --------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `website-diagnosis-rules.md` 规定 29 子项全覆盖           | 本文件规定 **5 维数据 + 叙事 + 建议** 全覆盖                                           |
| 每项 `issue` + `suggestion`（较差项以「强烈建议：」开头） | 每条建议 `content` 须 **引用当次数字** + **可执行动作**                                |
| `coreIssuesIds` + `PriorityPlan` 高/中/低                 | `priorityPlan` + `narrative.recommendations` 4 条 + `supplementaryRecommendations`     |
| HTML 由 `render` 渲染全部章节                             | HTML **必须**填 `executiveSummary`、`healthDiagnosis`、`sections.*.insight` 等（见下） |
| 交付前 Read HTML 对照章节清单                             | 交付前 Read HTML/xlsx 对照 `deliverable-preflight.md` § P4-FB                          |

**常见失误（导致建议偏少）**：

1. 只写 Excel 叙事 4 条标题、每条 1～2 句泛化话术，未引用 CPL/花费/国家名。
2. HTML 默认路径只填 `narrative`，**未填** `executiveSummary` / `healthDiagnosis` / `sections.insight`（模板原先不展示 `narrative.recommendations`，现已修复）。
3. 未按 **7 维数据驱动清单** 逐条给建议，只写「优化素材」「调整预算」等空话。

---

## JSON 结构（摘要）

完整 Schema：`assets/meta-period-report.schema.json`。  
**Excel 与 HTML 共用** `narrative`；**HTML 默认交付**还须填「深度分析扩展」字段。

---

## 一、Excel / 总数据叙事（`narrative` · 必填）

### 1. `narrative.overall`（整体表现）

| 要求     | 细则                                                                                       |
| -------- | ------------------------------------------------------------------------------------------ |
| 字数     | **≥ 120 字**（中文）                                                                       |
| 必含数字 | 花费、`results`、CPL（`costPerResult`）、`reach`、`impressions`、`frequency` **至少 5 项** |
| 必含口径 | `resultType`、`attributionSetting`（写入 `meta` 并在段中提及）                             |
| 可选     | 若有 `previousPeriod`，写 1～2 句环比（花费 ±%、CPL ±%）                                   |

### 2. `narrative.regional[]`（区域 / 广告组）

| 要求     | 细则                                                                                          |
| -------- | --------------------------------------------------------------------------------------------- |
| 条数     | **每个** `ad-sets` 中花费 >0 的广告组 **各 1 段**（不得合并成 1 句带过）                      |
| 字数     | 每段 **≥ 80 字**                                                                              |
| 必含     | 组名、花费占比或绝对值、线索数、`costPerResult`、频次；判断「曝光不足 / 频次过高 / 效率领先」 |
| 数据依据 | `ad-sets-<id>.json` → `adGroups[]`                                                            |

### 3. `narrative.country`（国家报告）

| 要求     | 细则                                                                    |
| -------- | ----------------------------------------------------------------------- |
| 字数     | **≥ 80 字**                                                             |
| 必含     | CPL **最低** 与 **最高** 国家名及具体 CPL；中间梯队 1～2 国；花费集中度 |
| 数据依据 | `country-<id>.json` → `countries[]`                                     |

### 4. `narrative.recommendations[]`（固定 4 条标题）

**必须恰好 4 条**，`title` 仅限下表枚举；`content` 须**数据驱动**，不得模板空话。

| title            | content 最低要求（每条 **≥ 150 字**）                                                                                |
| ---------------- | -------------------------------------------------------------------------------------------------------------------- |
| **简化表单问题** | 结合 **高频次 + 高 CPL** 的国家/组（写出名称与数字）；建议字段从 N 减到 3；说明预期对 CPL 的影响                     |
| **区域调整**     | 按 **具体广告组** 写语言/市场策略（如土/葡/德）；引用各组 CPL 对比；写清「加谁、减谁、暂停谁」                       |
| **预算重构**     | 给出 **具体比例**（如 4:3:3 或按 spend 占比调整）；测试周期（7/14 天）；优胜劣汰阈值（CPL > 账户均值 ×1.2 则减 30%） |
| **素材建议**     | 按 **平台**（IG/FB）与 **国家** 分述；素材套数、视频时长、形态；至少点名 1 个高花费低结果创意/版位                   |

**建议前缀（对齐网站诊断）**：

- 问题严重（CPL > 均值 1.3 倍、频次 >2.5、零成效花费 >$50）→ `content` 以 **「强烈建议：」** 开头
- 其余优化项 → **「推荐优化：」** 开头

---

## 二、数据驱动补充建议（`supplementaryRecommendations` · 必填）

在 4 条固定标题之外，**必须**再写 **7 维清单**，每条 `{ "dimension", "issue", "suggestion" }`：

| dimension    | issue（发现了什么）                               | suggestion（怎么办）                      |
| ------------ | ------------------------------------------------- | ----------------------------------------- |
| 预算与广告组 | 点名高 `spendPercentage`、差 `costPerResult` 的组 | 降预算 %、暂停、或合并受众                |
| 平台与版位   | `publisherPlatform` + `platformPosition` 组合     | 减投差版位、加码 winner 平台              |
| 地域         | 高消耗低结果国家                                  | geo 排除 / 收窄 / 单独组                  |
| 受众         | 低效 age×gender                                   | 排除或降 bid；扩量高效段                  |
| 创意         | 高花费低 `results` 的 ad                          | 关停、复制 winner 结构                    |
| 频次与疲劳   | `frequency` >2.5 且转化差                         | 扩受众、换创意、降预算                    |
| 接口限制     | 无按日/关键词等                                   | 一句说明「Meta 接口未提供」，**禁止编造** |

每条 `suggestion` **≥ 60 字**，须含 **至少 1 个当次数字或名称**。

---

## 三、优先级改进计划（`priorityPlan` · HTML 必填 · Excel 推荐）

对齐网站诊断 `PriorityPlan`：

```jsonc
{
  "priorityPlan": {
    "high": ["…", "…"], // ≥2 条，本周必须做
    "medium": ["…", "…"], // ≥2 条
    "low": ["…", "…"], // ≥2 条，持续优化
  },
}
```

每条 **≥ 40 字**，带责任维度（预算/素材/地域等）。

---

## 四、HTML 默认交付 · 深度分析扩展（必填）

用户未指定 Excel 时，除 §一～§三外 **还必须** 填写：

| 字段                               | 最低要求                                                                                                                                                                                   |
| ---------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `executiveSummary`                 | **3～5 段**，每段 **≥ 80 字**；解释「为什么」而不只报数；可拆自 `narrative.overall` 但须加深因果                                                                                           |
| `healthDiagnosis.lifecyclePhase`   | `test-market` / `find-winner` / `scale` 三选一。**可省略**：`render --snapshot-dir` 按花费与集中度自动推断；若手写须与数据一致（render 校验 `lifecyclePhase` vs `lifecyclePhaseInferred`） |
| `healthDiagnosis.lifecycleVerdict` | **≥ 60 字**，结合总花费与维度分散度；可随 phase 由 CLI 补全                                                                                                                                |
| **阶段判定（CLI 推断口径）**       | **测市场**：总花费 &lt; $200，或活跃维度 ≥4 且赢家花费占比 &lt;35%；**放量**：Top 广告组花费/结果占比 ≥55% 且 CPL ≤ 账户均值；**找赢家**：其余有优劣分化但未高度集中                       |
| `healthDiagnosis.fourQuestions`    | **恰好 4 张卡片**（钱花得值不值 / 赢在哪 / 输在哪 / 下月重点）                                                                                                                             |
| 每张 `fourQuestions[]`             | `verdict` + `evidence` **≥2 条**（含数字）+ `action` **≥ 40 字**                                                                                                                           |
| `healthDiagnosis.scorecard`        | **≥ 6 行**有效行；每行须 `item` / `data` / `signal`(green\|yellow\|red) / `signalLabel` / `advice`。**可省略**：`render --snapshot-dir` 自动补全；render 校验行数与字段完整性              |
| `sections.platform.insight`        | **≥ 200 字**                                                                                                                                                                               |
| `sections.country.insight`         | **≥ 200 字**                                                                                                                                                                               |
| `sections.adSets.insight`          | **≥ 200 字**                                                                                                                                                                               |
| `sections.audience`                | `goldenProfile` **≥3 条** + `antiProfile` **≥2 条** + `insight` **≥ 150 字**                                                                                                               |
| `sections.landingPage.rows`        | **≥ 3 行**（心理阻碍 / 数据信号 / 推演 / 优先级）                                                                                                                                          |
| `abTests`                          | **≥ 3 个**实验（变量、假设、成功标准）                                                                                                                                                     |
| `actionChecklist`                  | `today` **≥2**、`thisWeek` **≥3**、`thisMonth` **≥3** 条可执行项                                                                                                                           |

**禁止**：HTML 中大量「（待 Agent 撰写）」占位；交付前 Read HTML 确认无空节。

---

## 五、撰写流程（对齐 P8）

1. **拉数**：`facebook-analysis` + `--json-out`（默认 5 维）。
2. **脚本读盘**：聚合 KPI、Top/Bottom 国家、平台、受众、广告组（禁止 Read 业务 JSON 进对话）。
3. **先 outline 后 JSON**：列出将引用的数字与 7 维建议要点，再写 `meta-period-report.json`。
4. **渲染**：`facebook-analysis render`（HTML）或脚本写 xlsx（Excel）。
5. **Read 终稿**：对照 `deliverable-preflight.md` § P4-FB。

---

## 六、自检清单（Agent 交付前勾选）

- [ ] `narrative.recommendations` 4 条，每条 content ≥150 字且含真实数字
- [ ] `supplementaryRecommendations` 7 维齐全
- [ ] `priorityPlan` high/medium/low 各 ≥2 条
- [ ] HTML：`executiveSummary` ≥3 段、`fourQuestions` =4、`lifecyclePhase` 与快照推断一致（或省略由 CLI 补全）、`scorecard` ≥6 行且每行五字段齐全
- [ ] HTML：`sections.platform/country/adSets.insight` 各 ≥200 字
- [ ] HTML：`actionChecklist` 三列非空；`abTests` ≥3
- [ ] Excel：总数据 Sheet 叙事块 4 节齐全，无 1 句话敷衍
- [ ] 未编造 Meta 无接口维度（按日、关键词等）

---

## 相关文档

- `report-templates/meta-period-report.md` — 流程与章节
- `report-templates/meta-period-report-excel.md` — Excel 五 Sheet
- `references/analytics/facebook-analysis-guide.md` — API 字段
- `references/core/deliverable-preflight.md` — 交付审阅
- `assets/website-diagnosis-rules.md` — 网站诊断（对照参考）
