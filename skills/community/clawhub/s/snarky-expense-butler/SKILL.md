---
name: snarky-expense-butler
description: "毒舌记账管家，支持记账、查询、预算提醒、毒舌消费分析、地域统计、趋势图。当用户提到记账、消费、花销、支出、记一笔、消费分析、预算、记个账时触发。NOT for: 股票/投资分析、记账软件推荐。"
metadata: { "openclaw": { "emoji": "💰" } }
---

# 毒舌记账管家 (Snarky Expense Butler)

纯本地 JSON 存储的个人消费记录系统，无外部依赖，无需 API Key。

## 数据路径

- 数据文件：`./expense_records.json`，可通过 `EXPENSE_DATA_FILE` 环境变量指定
- 趋势图输出：`./trends/`，可通过 `EXPENSE_TRENDS_DIR` 环境变量指定
- 首次使用自动创建数据文件

## 命令

```bash
# 记账（自动记录时间戳 + 自动提取地点 + 文件锁防并发）
python3 scripts/add_expense.py <分类> <金额> [备注] [--location 地点]

# 查询
python3 scripts/expense_query.py today|week|month|stats|list

# 报告（支持 crontab 定时推送）
python3 scripts/expense_report.py daily|weekly|monthly|yearly

# 预算检查（✅正常 ⚠️接近80% 🚨超支）
python3 scripts/expense_budget.py today|week|month

# 毒舌分析（调侃风格，非模板报告）
python3 scripts/expense_analysis.py today|YYYY-MM-DD

# 地域统计（按地点聚合，标注吞金兽🐷/省钱区💰）
python3 scripts/expense_location.py summary|top|backfill

# 趋势图（优先大模型出图，matplotlib 兜底）
python3 scripts/expense_trends.py week|month|year
```

## 分类

交通、餐饮、购物、娱乐、医疗、教育、其他

## 配置

预算在数据文件 `settings.budget` 中配置，默认值：日 ¥50 / 周 ¥350 / 月 ¥1500。

## 数据格式

每条 item 结构：
```json
{"datetime": "2026-03-18 14:05", "category": "餐饮", "amount": 17.9, "note": "午餐", "location": "福田cocopark"}
```

location 可选：支持手动指定（`--location`），或从备注自动提取（括号内优先、地标词识别）。
