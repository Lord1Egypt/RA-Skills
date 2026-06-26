---
name: travel-tracker
description: >
  管理和统计工作/生活外出记录，生成 Excel 报表，同步到 Obsidian。
  Use when: 查询外出记录、统计外出次数、生成外出 Excel 报表、同步外出数据到
  Obsidian、自动从日历提取外出、设置外出提醒。Triggers: "外出统计",
  "外出记录", "travel report", "外出天数", "外出地点", "生成外出报表",
  "同步外出", "travel tracker", "outbound"。
---

# Travel Tracker

统一管理外出记录（工作/生活分类）。

## 查询外出

```bash
# 查询外出记录
~/.openclaw/workspace/scripts/travel-query.sh [日期范围]
```

## 生成报表

```bash
# 每周外出统计
~/.openclaw/workspace/scripts/generate-weekly-travel-report.sh

# 月度 Excel（Python）
python3 ~/.openclaw/workspace/scripts/generate-travel-excel-2026-03.py

# 季度汇总
python3 ~/.openclaw/workspace/scripts/generate-travel-excel-2026-Q1.py
```

## 日历自动提取

```bash
# 从 Apple Calendar 提取外出安排
~/.openclaw/workspace/scripts/auto-travel-from-calendar.sh
```

## 同步到 Obsidian

```bash
~/.openclaw/workspace/scripts/sync-travel-to-obsidian.sh
```

## 外出提醒

```bash
# 自动验证并设置外出提醒
~/.openclaw/workspace/scripts/travel-reminder-auto-verify.sh
```

## 数据存储

- 每周统计：`memory/weekly-travel-YYYY-Www.md`
- Excel 报表：`exports/`
- Obsidian：`~/Documents/obsidiansave/外出记录/`

## 分类规则

- **工作外出**：调研/考务/会议/拍摄等
- **生活外出**：购物/聚餐/办事等
- 周报显示格式：`工作 X 次 + 生活 X 次`
