# Yandex Direct 账户周期报告 — Excel 交付规格

> **适用场景**：用户明确要求 **Yandex 账户 + 统计区间 + Excel/xlsx**。  
> **工作流**：**P4**（与 `yandex-period-report.md` 共用拉数维度；交付形态不同）。  
> **禁止**：加载宿主「xlsx / Excel」第三方 Skill 代替本流程；**无** CLI 内置写表子命令，须 Agent 脚本（`exceljs` / `xlsx` / `openpyxl`）读落盘 JSON 写 `.xlsx`。  
> 用户未指定格式时走 `yandex-period-report.md` → `yandex-analysis render` HTML，**不要**默认走本文。

---

## 执行门禁（**全部满足后才允许写脚本**）

| #   | 门禁                  | 命令 / 动作                                                                                           |
| --- | --------------------- | ----------------------------------------------------------------------------------------------------- |
| 1   | Read 当次必读         | `agent-conventions.md`、`account-analytics.md`、`yandex-period-report.md`（本文）                     |
| 2   | **账户 ID 核验**      | `siluzan-tso list-accounts -m Yandex -k <porg-xxx> --json-out ./snap-yandex`                          |
| 3   | 确认 `currency`       | 来自 overview 落盘或 list-accounts（Yandex 常用 USD/RUB 等）                                          |
| 4   | **拉数**              | `yandex-analysis -a <已核验 id> --start … --end … --json-out <dir>`（全 8 维或用户指定 Sheet 对应维） |
| 5   | **先 outline 后脚本** | 对本次每个 section Read `*.outline.txt`；业务 JSON 仅在脚本内读取                                     |
| 6   | 写脚本                | 字段名只来自 outline；`ctr`/`conversionRate` 为 **0~1 小数**                                          |
| 7   | 交付前审阅            | 按 `agent-conventions.md` §七；xlsx 无法 Read 时贴自检表 + 脚本 stdout 摘要                           |

---

## 账户 ID

`list-accounts -m Yandex -k <porg-xxx>` 核验；全流程用同一 Client-Login。报告首行：`统计区间：YYYY-MM-DD ~ YYYY-MM-DD（货币：XXX）`。

---

## 推荐 Sheet ↔ CLI section

用户已列出 Sheet 名时以用户清单为准；未列出时可用下表默认 7 Sheet（周报由脚本从 daily 聚合，不必单独拉）：

| Sheet（建议名） | `yandex-analysis` section | 读法                            |
| --------------- | ------------------------- | ------------------------------- |
| 账户总览        | `overview`                | 对象：`totals` / `balance` …    |
| 日报表          | `daily`                   | `items[]`                       |
| 周报表          | `daily` 的 `weekly[]`     | **读落盘 weekly，禁止自行聚周** |
| Search 网络     | `search`                  | `items[]`                       |
| 广告系列        | `campaigns`               | `items[]`                       |
| 关键词          | `keywords`                | `items[]`                       |
| 搜索词          | `search-terms`            | `items[]`（区间 ≤180 天）       |
| 地域            | `geo`                     | `items[]`                       |
| 设备            | `devices`                 | `items[]`                       |

```bash
mkdir -p ./snap-yandex
siluzan-tso list-accounts -m Yandex -k <porg-xxx> --json-out ./snap-yandex

siluzan-tso yandex-analysis -a <porg-xxx> --start <S> --end <E> --json-out ./snap-yandex
```

落盘文件名以 stdout 摘要 `results[].file` 为准。

---

## 统一度量列（列表 Sheet）

| Excel 列名 | API 字段            | 说明                         |
| ---------- | ------------------- | ---------------------------- |
| 消耗       | `spend`             | 账户币种小数，2 位           |
| 展示       | `impressions`       | 整数                         |
| 点击       | `clicks`            | 整数                         |
| CTR        | `ctr`               | 0~1；单元格 `0.00%` 或文案 % |
| CPC        | `averageCpc`        | 小数                         |
| 转化       | `conversions`       | 小数/整数按 outline          |
| 转化率     | `conversionRate`    | 0~1                          |
| CPA        | `costPerConversion` | 可为 null                    |

### 维度列（按 Sheet）

| Sheet    | 维度列（API）                                                               |
| -------- | --------------------------------------------------------------------------- |
| Search   | `network`                                                                   |
| 广告系列 | `campaignId`（文本）、`campaignName`、`status`/`state`、`campaignType`      |
| 关键词   | `keyword`、`campaignName`、`criteriaType`、`adGroupId`（文本）              |
| 搜索词   | `searchQuery`、`matchedKeyword`、`campaignName`                             |
| 地域     | `locationName` / `targetingLocationName`                                    |
| 设备     | `device`                                                                    |
| 日报     | `date`                                                                      |
| 周报     | `daily.weekly[]` 的 `weekLabel`、`startDate`、`endDate`、`days`（CLI 已算） |

**账户总览 Sheet**：KPI 区（余额、本期消耗、日均、点击、CTR、CPC、转化）+ **全部叙事**（各维总结/建议、≥3 条跨维优化建议）写在本 Sheet；列表 Sheet 仅数据表。不写「一句话数据概况 / 执行摘要」。

---

## 禁止猜的字段 / 口径

| ❌ 禁止                                        | ✅ 正确                                                            |
| ---------------------------------------------- | ------------------------------------------------------------------ |
| 把 `ctr` 当已是百分数再 ÷100                   | 落盘为 0~1；Excel 用百分比格式或 `*100` 后加 `%`                   |
| 编造学习期、搜索词分类等无接口硬事实           | 无字段且算不出则不写该列；关键词翻译走 rowInsights                 |
| 自行按 `daily.date` 聚周（易出 `NaN-NaN-NaN`） | 读 `daily.weekly[]`；`date` 已是 YYYY-MM-DD，禁止再拼 `T00:00:00Z` |
| `campaignId` 写成数字                          | `String(id)` + 文本格式                                            |
| search-terms 拉超过 180 天                     | 缩短区间或排除该维                                                 |

---

## 禁止的数据探查方式

- `cat …json \| python -m json.tool \| head`
- 宿主 **Read** 打开业务 `*.json`
- 把 JSON 片段贴进对话当字段依据

**允许**：Read `*.outline.txt`；脚本 stdout 打印行数 / 汇总。

---

## 样式（必须）

脚本 `import` `report-templates/excel-style-kit.mjs`，用 `createExcelWorkbook({ accent: "yandex" })` + `titleBar`/`tableHeader`/`dataRow` 等组件搭版面，**禁止**裸写无样式单元格。规范见 `report-templates/excel-style-guide.md`。

---

## 交付前自检

- [ ] `accountId` = 用户要求的 `porg-xxx`
- [ ] 每个 Sheet 列均能在对应 outline 找到源字段
- [ ] `itemCount` 与 Excel 数据行一致（±合计行）
- [ ] 全部 ID 列为文本
- [ ] 未调用 `yandex-analysis render`（Excel 路径）
- [ ] 未使用第三方 xlsx Skill 替代拉数口径

---

## 相关文档

- `yandex-period-report.md` — 默认 HTML 四步
- `references/analytics/account-analytics.md` — 命令与日期
- `references/core/tips.md` — 摘要 → outline → 脚本
