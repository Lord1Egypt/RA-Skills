# Meta 周期报告撰写规则（Agent 用）

> 对照运营交付物：浅色 HTML（汇总 / 日趋势 / 国家 / 广告系列 / 受众 / 优化建议）+ 五 Sheet Excel（**汇总数据** KPI 下必须是 **一 / 二 / 三**）。  
> **禁止**只交 KPI 表或空话建议。

---

## 必写叙事

| 字段 | 要求 |
| ---- | ---- |
| `fourQuestions` | 恰好 4 问，`title` 固定：钱花得值不值？ / 谁真的想买？ / 广告还新鲜吗？ / 用户为什么不留资？ |
| 每问 `verdict` | 一句话结论，引用当次国家 / CPL / 人群 |
| 每问 `bullets` | ≥1 条证据，含数字 |
| 每问 `action` | 「怎么办」可执行动作 |
| `recommendations` | ≥3 张卡：`title` + `tag` + `items[]`（每卡 ≥1 条动作） |
| `sections.{daily,country,campaigns,audience}.insight` | 各章 `analysis[]` + `advice[]` 至少各 1 条，引用当次数字 |

数值表（`kpis` / `tables` / `charts`）由 `facebook-analysis render --snapshot-dir` 从快照覆盖，Agent 不要手填数。

---

## 禁止

- 编造按日 / 国家 / 系列数字
- 把 `creative` / `ad-sets` 各行 `results` 加总后与 overview 对比
- 手写 HTML 或用对话 Markdown 表代替终稿
- 用户要表格时不跑 `render --format xlsx`
