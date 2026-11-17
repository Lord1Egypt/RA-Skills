# Meta（Facebook）周期报告 — Excel 模板规格

> **适用场景**：用户**明确要求 Excel / xlsx / 表格形式**时读本文件。  
> 用户未指定格式时，**默认交付 HTML**，走 `meta-period-report.md` 标准四步。

> 对照业务交付物：`光盈光电7月fb广告报告.xlsx`（5 个 Sheet：**汇总数据** / 日趋势 / 国家 / 广告系列 / 受众）。  
> **由 CLI 生成**：`facebook-analysis render --format xlsx`，不要手写 xlsx，也不要假设还有别的 excel 子命令。  
> **ID 列硬规则**：账户 / 系列等 id **一律写成字符串（文本）**；见 `references/core/agent-conventions.md`。

---

## Excel 工作簿结构（5 Sheet）

| Sheet | 中文名     | CLI `--sections` | 落盘文件               | 角色                         |
| ----- | ---------- | ---------------- | ---------------------- | ---------------------------- |
| 1     | **汇总数据** | `overview`     | `overview-<id>.json`   | KPI 首行 + **一 / 二 / 三** 叙事 |
| 2     | **日趋势** | `daily`          | `daily-<id>.json`      | 按日表（`days[]`）           |
| 3     | **国家**   | `country`        | `country-<id>.json`    | 国家/地区表                  |
| 4     | **广告系列** | `campaigns`    | `campaigns-<id>.json`  | 系列表                       |
| 5     | **受众**   | `audience`       | `audience-<id>.json`   | 年龄 × 性别表                |

**Excel 模板不含**：广告组、平台、设备、创意。用户要这些维时额外拉 `--sections ad-sets,platform,device,creative`，不必塞进本工作簿。

---

## 统一数据列（Sheet 2～4 及汇总 KPI 行）

| Excel 列名           | API 字段               | 说明                         |
| -------------------- | ---------------------- | ---------------------------- |
| 目标 / 成效类型      | `resultType`           | 如「潜在客户信息（表单）量」 |
| 覆盖人数             | `reach`                | 整数                         |
| 展示次数             | `impressions`          | 整数                         |
| 频次                 | `frequency`            | 小数                         |
| 归因设置             | `attributionSetting`   | 如「点击后 7 天内或浏览后 1 天内」 |
| 成效                 | `results`              | Meta「结果」列               |
| 已花费金额 (USD)     | `spend`                | 账户币种，非 micros          |
| 单次成效费用         | `costPerResult`        | CPL                          |

Sheet 2 首列：`单日`（`date`，YYYY-MM-DD）。  
Sheet 3 首列：`国家/地区`（`countryOrRegion`）。  
Sheet 4 首列：`广告系列名称`（`campaignName`）。  
Sheet 5 另加：`年龄`（`age`）、`性别`（`gender`）。

无成效的行：成效 / 成效类型 / 单次成效费用留空，不要填 0。

---

## 汇总数据叙事（KPI 下方，格式的一部分）

空 1～2 行后，**只写三块**，标题字面必须是：

| 块 | 标题 | 内容从哪来 |
| -- | ---- | ---------- |
| **一** | `一、{账户名} {周期} Facebook 广告账户` | 系列名 + 花费/成效/单次成本（CLI 用 KPI 拼）；可接 `fourQuestions[0].verdict` |
| **二** | `二、分析与优化建议` | 下面固定 3 小节：`1. 国家/地区表现分析`、`2. 受众结构与线索质量风险`、`3. 广告频次与日趋势`（来自 `sections.country/audience/daily.insight`） |
| **三** | `三、下一步优化建议` | `recommendations[]` 按 `1. 2. 3.` 编号 |

**禁止**在 Excel 汇总数据里写「钱花得值不值？」四问标题，或 `daily 分析` / `country 建议` 这种机读标题。四问仍写在 Agent JSON 里给 HTML 用。

---

## 拉数与渲染

```bash
siluzan-tso facebook-analysis -a <mediaCustomerId> \
  --start <YYYY-MM-DD> --end <YYYY-MM-DD> \
  --json-out ./snap-fb \
  --sections overview,daily,country,campaigns,audience

siluzan-tso facebook-analysis render \
  --data ./meta-period-report.json \
  --snapshot-dir ./snap-fb \
  --format xlsx \
  --out ./meta-period-report.xlsx
```

叙事 JSON 与 HTML 相同，见 `meta-period-report.md`。

---

## 相关文档

| 文档                                    | 用途           |
| --------------------------------------- | -------------- |
| `meta-period-report.md`                 | 周期报告总纲   |
| `assets/meta-period-report.schema.json` | Agent JSON     |
| `references/analytics/facebook-analysis-guide.md` | 字段口径 |
