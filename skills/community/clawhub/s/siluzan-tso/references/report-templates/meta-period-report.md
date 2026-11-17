# Meta（Facebook）账户 — 周期分析报告

> **终稿语言**：叙事跟 `meta.lang`（`zh` 或 `en`），表头用该语言。`render` 必须带 `--lang`。
>
> 统计区间：`{startDate}` ~ `{endDate}`  
> 账户：`{mediaCustomerId}`（`{mediaCustomerName}`）

> **默认交付物**：一份可打开的、带 ECharts 图表的 **HTML 文件**（`meta-period-report.html`）。封面按日期写成「季度复盘」或「月度复盘」，对不上仍是「周期复盘」。不要打开 HTML 改称呼。  
> 用户**未指定格式**时一律走下方 **标准四步流程**；**禁止**仅 Markdown 摘要或纯 JSON 充当终稿。  
> 用户要 **表格 / Excel / xlsx** 时：步骤 1～3 相同，步骤 4 改 `--format xlsx`（见文末）。

字段口径见 `references/analytics/facebook-analysis-guide.md`。  
撰写要点：`assets/meta-period-report-rules.md`。  
Agent JSON Schema：`assets/meta-period-report.schema.json`。

---

## 标准四步流程（默认 · 交付 HTML）

| 步骤             | 执行者       | 动作                                                                                          |
| ---------------- | ------------ | --------------------------------------------------------------------------------------------- |
| **1. 拉数**      | Agent 调 CLI | `facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb --sections overview,daily,country,campaigns,audience` |
| **2. 分析**      | Agent        | 用 **node/python 脚本**读落盘 JSON（勿用 Read 打开业务 `*.json`），完成筛选、聚合、排序与洞察 |
| **3. 写 JSON**   | Agent        | 按本纲要撰写 `meta-period-report.json`（`fourQuestions` / `recommendations` / `sections.*.insight`） |
| **4. 渲染 HTML** | CLI          | `facebook-analysis render` — **校验必含字段**，缺项报错不生成；**禁止** Agent 手写/拼接 HTML |

```bash
# 步骤 1
siluzan-tso facebook-analysis -a <id> --start <s> --end <e> --json-out ./snap-fb \
  --sections overview,daily,country,campaigns,audience

# 步骤 4（步骤 2～3 完成后）
siluzan-tso facebook-analysis render \
  --data ./meta-period-report.json \
  --snapshot-dir ./snap-fb \
  --out ./meta-period-report.html
```

`--snapshot-dir` 与步骤 1 的 `--json-out` 同目录；CLI 自动合并 KPI、日/国家/系列/受众表格与图表（**数值一律以 CLI 快照覆盖**；`meta` 仅补空）。

---

## Excel / 表格分支（仅当用户指定）

用户说「要 Excel」「导出 xlsx」「按表格形式」等时：

```bash
siluzan-tso facebook-analysis render \
  --data ./meta-period-report.json \
  --snapshot-dir ./snap-fb \
  --format xlsx \
  --out ./meta-period-report.xlsx
```

同时要 HTML + Excel：`--format html,xlsx`。  
版式见 **`report-templates/meta-period-report-excel.md`**（5 Sheet：**汇总数据** / 日趋势 / 国家 / 广告系列 / 受众；汇总 KPI 下是 **一 / 二 / 三**）。

---

## 默认五维与 HTML 章节

| #   | HTML 章节   | CLI `--sections` | 后端 Section        | 落盘文件               |
| --- | ----------- | ---------------- | ------------------- | ---------------------- |
| 1   | 账号总览    | `overview`       | OverviewSectionData | `overview-<id>.json`   |
| 2   | 日趋势      | `daily`          | DailySectionData    | `daily-<id>.json`      |
| 3   | 国家        | `country`        | CountrySectionData  | `country-<id>.json`    |
| 4   | 广告系列    | `campaigns`      | CampaignSectionData | `campaigns-<id>.json`  |
| 5   | 受众        | `audience`       | AudienceSectionData | `audience-<id>.json`   |

按需追加：`ad-sets`（广告组）、`platform`（平台×版位）、`device`（设备）、`creative`、`material`。  
`campaigns` 现为独立系列维，**不再**映射到 `ad-sets`。广告组请显式传 `ad-sets`。

---

## Agent JSON（`meta-period-report.json`）

数值表可省略，由 `--snapshot-dir` 合并。Agent **必须**写叙事：

```jsonc
{
  "meta": {
    "accountName": "品牌名",
    "periodLabel": "2026年7月",
    "startDate": "2026-07-01",
    "endDate": "2026-07-31",
    "campaignName": "可由 snapshot 单系列自动补",
    "generatedAt": "2026/8/18 16:53:41"
  },
  "fourQuestions": [
    { "title": "钱花得值不值？", "verdict": "…", "bullets": ["…"], "action": "…" },
    { "title": "谁真的想买？", "verdict": "…", "bullets": ["…"], "action": "…" },
    { "title": "广告还新鲜吗？", "verdict": "…", "bullets": ["…"], "action": "…" },
    { "title": "用户为什么不留资？", "verdict": "…", "bullets": ["…"], "action": "…" }
  ],
  "recommendations": [
    { "title": "按国家独立拆分广告组", "tag": "优先执行", "items": ["…"] },
    { "title": "先核线索质量，再决定年龄下限", "tag": "核验后执行", "items": ["…"] },
    { "title": "更新广告素材，优先覆盖高频市场", "tag": "本周完成", "items": ["…"] }
  ],
  "sections": {
    "daily": { "insight": { "analysis": ["…"], "advice": ["…"] } },
    "country": { "insight": { "analysis": ["…"], "advice": ["…"] } },
    "campaigns": { "insight": { "analysis": ["…"], "advice": ["…"] } },
    "audience": { "insight": { "analysis": ["…"], "advice": ["…"] } }
  }
}
```

四问 `title` 必须与上表完全一致。建议至少 3 张卡。各章 `analysis` / `advice` 至少 1 条，须引用当次数字。

---

## 相关文档

| 文档                                              | 用途                     |
| ------------------------------------------------- | ------------------------ |
| `assets/meta-period-report-rules.md`              | 撰写字数与引用数字规则   |
| `assets/meta-period-report.schema.json`           | Agent JSON 机器校验      |
| `report-templates/meta-period-report-excel.md`    | 五 Sheet 列名            |
| `references/analytics/facebook-analysis-guide.md` | API 字段口径             |
