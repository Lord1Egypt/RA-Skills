# Meta（Facebook）周期报告 — Excel 模板规格

> **适用场景**：用户**明确要求 Excel / xlsx** 交付时读本文件。  
> 用户未指定格式时，**默认交付 HTML**，走 `meta-period-report.md` 标准四步（拉数 → 分析 → 写 JSON → `facebook-analysis render`），**不要**默认走 Excel。

> 对照业务交付物：`无锡顺晟Facebook4月报告.xlsx`（5 个 Sheet）。  
> Excel 流程：CLI 拉数 → Agent 分析并写 `meta-period-report.json` → **Agent 脚本**按本规格写 `.xlsx`（**无** CLI 内置 excel 子命令）。

---

## Excel 工作簿结构（5 Sheet）

| Sheet | 中文名         | CLI `--sections` | 落盘文件             | 报告中的角色                                        |
| ----- | -------------- | ---------------- | -------------------- | --------------------------------------------------- |
| 1     | **总数据**     | `overview`       | `overview-<id>.json` | 账户级 KPI + **全部叙事分析**（唯一写文案的 Sheet） |
| 2     | **广告组数据** | `ad-sets`        | `ad-sets-<id>.json`  | 区域/广告组维度表（拉美、欧洲、亚洲等）             |
| 3     | **平台数据**   | `platform`       | `platform-<id>.json` | Facebook vs Instagram 对比表                        |
| 4     | **国家数据**   | `country`        | `country-<id>.json`  | 国家/地区排行表                                     |
| 5     | **受众数据**   | `audience`       | `audience-<id>.json` | 年龄 × 性别矩阵表                                   |

**Excel 模板不含**：创意 Sheet、`material`、按日趋势、关键词。若用户要创意章节，额外拉 `--sections creative`。

---

## 统一数据列（Sheet 2～5 及总数据 KPI 行）

Excel 导出列与 API 字段对照（撰写/渲染时统一用 API camelCase，展示用中文列名）：

| Excel 列名       | API 字段             | 说明                                      |
| ---------------- | -------------------- | ----------------------------------------- |
| 目标 / 成效类型  | `resultType`         | 如「Meta 潜在客户」                       |
| 覆盖人数         | `reach`              | 整数                                      |
| 展示次数         | `impressions`        | 整数                                      |
| 频次             | `frequency`          | 小数；>2 可提示疲劳                       |
| 归因设置         | `attributionSetting` | 如「点击后 7 天内或浏览后 1 天内」        |
| 成效             | `results`            | Meta「结果」列，**勿与 conversions 混用** |
| 已花费金额 (USD) | `spend`              | 美元，非 micros                           |
| 单次成效费用     | `costPerResult`      | CPL                                       |

### Sheet 2 额外列

| Excel 列名   | API 字段       |
| ------------ | -------------- |
| 广告系列名称 | `campaignName` |
| 广告组名称   | `adGroupName`  |

### Sheet 3 维度列

| Excel 列名 | API 字段            | 备注                                            |
| ---------- | ------------------- | ----------------------------------------------- |
| 平台       | `publisherPlatform` | 汇总时按平台聚合；版位细拆见 `platformPosition` |

### Sheet 4 维度列

| Excel 列名 | API 字段          |
| ---------- | ----------------- |
| 国家/地区  | `countryOrRegion` |

### Sheet 5 维度列

| Excel 列名 | API 字段 |
| ---------- | -------- | ----------------------------- |
| 年龄       | `age`    |
| 性别       | `gender` | `male` / `female` / `unknown` |

**受众表注意**：`gender=unknown` 或 `成效=0` 的行可保留在数据表，撰写时说明「样本不足勿扩量」。

---

## Sheet 1「总数据」— 叙事章节（Agent 必写）

总数据 Sheet 除首行 KPI 外，按**固定标题块**顺序撰写（与 Excel 版式一致）：

### 1. 整体表现

- **1 段话**，覆盖：总花费、线索数（`results`）、平均 CPL、覆盖、展示、频次。
- 示例结构：「{月}月总花费 {spend} 美元，获得 {results} 条线索，平均每条成本 {cpl} 美元。覆盖 {reach} 人，展示 {impressions} 次，频次 {frequency}。」

### 2. 区域报告

- 按 **广告组**（Sheet 2 各行）写 **3～5 句**，每段对应一个区域组（如 leads-欧洲、leads-拉美、leads-亚洲）。
- 必提：单条 CPL、线索数、覆盖/频次特征、是否「曝光不足」或「频次高转化差」。
- 数据依据：`ad-sets-<id>.json` → `adGroups[]`。

### 3. 国家报告

- **1 段话**对比 Top 国家：最低 CPL 国家、最高 CPL 国家、中间梯队。
- 数据依据：`country-<id>.json` → `countries[]`（按 `costPerResult` 或 `spend` 排序）。

### 4. 优化建议（固定 4 条 + 7 维补充）

**每条 `content` ≥150 字**，须引用当次国家名/CPL/广告组名；严重项以「强烈建议：」开头。完整规则见 **`assets/meta-period-report-rules.md`**。

| #   | 标题             | 撰写要点                                                   |
| --- | ---------------- | ---------------------------------------------------------- |
| 1   | **简化表单问题** | 点名高频次高 CPL 国家/组；字段缩减至 3 项；写预期 CPL 改善 |
| 2   | **区域调整**     | 按广告组写语言/市场策略；写清加谁、减谁、暂停谁            |
| 3   | **预算重构**     | 具体比例（如 4:3:3）、测试 7/14 天、CPL 阈值优胜劣汰       |
| 4   | **素材建议**     | 分 IG/FB、分市场；素材套数、视频时长、高花费低结果创意处理 |

**Excel 总数据 Sheet 另须**（可写在 4 条之后或单独小节）：

- `supplementaryRecommendations` 7 维表（预算/平台/地域/受众/创意/频次/接口限制）
- `priorityPlan` 高/中/低各 ≥2 条（推荐）

---

## 拉数命令（对齐 Excel 五 Sheet）

```bash
siluzan-tso facebook-analysis -a <mediaCustomerId> \
  --start <YYYY-MM-DD> --end <YYYY-MM-DD> \
  --json-out ./snap-fb \
  --sections overview,ad-sets,platform,country,audience
```

---

## Agent JSON 映射（`meta-period-report.json`）

与 Excel 模板 **一一对应** 的字段（HTML 深度分析扩展字段见 `meta-period-report.md` § HTML 扩展章节）。

```jsonc
{
  "meta": {
    "accountName": "无锡顺晟",
    "periodLabel": "2026年4月",
    "startDate": "2026-04-01",
    "endDate": "2026-04-30",
    "resultType": "Meta 潜在客户",
    "attributionSetting": "点击后7天内或浏览后1天内",
    "generatedAt": "2026/5/19 18:27:05",
  },
  // KPI 行：可省略，由 --snapshot-dir 从 overview 合并
  "kpis": {
    "spend": 473.01,
    "results": 36,
    "costPerResult": 13.14,
    "reach": 45628,
    "impressions": 72850,
    "frequency": 1.6,
  },
  // 对应 Sheet1 叙事块
  "narrative": {
    "overall": "4月总花费473美元…",
    "regional": [
      { "adGroupName": "leads-欧洲", "text": "欧洲（土耳其）成本最低…" },
      { "adGroupName": "leads-拉美", "text": "拉美成本最高…" },
      { "adGroupName": "leads-亚洲", "text": "亚洲介于两者之间…" },
    ],
    "country": "土耳其单条9.45美元，远低于其他国家…",
    "recommendations": [
      { "title": "简化表单问题", "content": "强烈建议：…（≥150字，含国家/CPL数字）" },
      { "title": "区域调整", "content": "推荐优化：…" },
      { "title": "预算重构", "content": "…" },
      { "title": "素材建议", "content": "…" },
    ],
  },
  "supplementaryRecommendations": [
    { "dimension": "预算与广告组", "issue": "…", "suggestion": "…" },
  ],
  "priorityPlan": { "high": ["…"], "medium": ["…"], "low": ["…"] },
  // 对应 Sheet2～5 表格 + 图表：可省略，由 --snapshot-dir 自动合并
  "tables": {
    "adSets": [
      /* 见 merge-snapshot */
    ],
    "platform": [
      /* publisherPlatform 汇总行 */
    ],
    "countries": [
      /* country 行 */
    ],
    "audiences": [
      /* age×gender 行 */
    ],
  },
  "charts": {
    "platform": { "labels": ["instagram", "facebook"], "cpl": [], "spend": [] },
    "country": { "labels": [], "cpl": [] },
    "audience": { "labels": [], "cpl": [], "leads": [] },
  },
}
```

完整 JSON Schema：`assets/meta-period-report.schema.json`。

---

## HTML 渲染章节（Excel 必含 vs 深度分析扩展）

| 报告章节            | Excel 必含                     | 深度 HTML 扩展（可选）                     |
| ------------------- | ------------------------------ | ------------------------------------------ |
| KPI 顶栏            | ✅                             | —                                          |
| 整体表现 / 执行摘要 | ✅ `narrative.overall`         | `executiveSummary[]` 可多段深度解读        |
| 区域报告            | ✅ `narrative.regional`        | 广告组疲劳表 + `sections.adSets.insight`   |
| 国家报告            | ✅ `narrative.country`         | 国家 CPL 图表 + `sections.country.insight` |
| 优化建议 4 条       | ✅ `narrative.recommendations` | A/B 实验、行动清单                         |
| 平台对比表/图       | ✅ Sheet3                      | `sections.platform.insight`                |
| 国家排行表/图       | ✅ Sheet4                      | —                                          |
| 受众矩阵表/图       | ✅ Sheet5                      | Top/Bottom 10、黄金画像                    |
| 账户健康诊断        | ❌                             | 三阶段 / 四问 / 红绿灯表                   |
| 落地页表单分析      | ❌（合并在「简化表单」建议）   | `sections.landingPage`                     |

**默认交付**：以 Excel 五 Sheet + 总数据叙事为准；用户明确要求「深度分析 / 总监视角」时再补 HTML 扩展章节。

---

## HTML 渲染（可选 · 非 Excel 默认路径）

用户**同时要 HTML** 或**未要 Excel、走默认流程**时，在写完 `meta-period-report.json` 后执行：

```bash
siluzan-tso facebook-analysis render \
  --data ./meta-period-report.json \
  --snapshot-dir ./snap-fb \
  --out ./meta-period-report.html
```

**仅交付 Excel** 时可跳过本节。

---

## 相关文档

| 文档                                              | 用途                                |
| ------------------------------------------------- | ----------------------------------- |
| `meta-period-report.md`                           | 周期报告总纲 + HTML 扩展 + CLI 流程 |
| `assets/meta-period-report.schema.json`           | Agent JSON 机器校验                 |
| `references/analytics/facebook-analysis-guide.md` | API 字段口径                        |
