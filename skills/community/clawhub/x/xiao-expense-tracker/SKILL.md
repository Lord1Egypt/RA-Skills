---
name: expense-tracker
description: 记账工具 - 收支记录、分类统计、预算管理
---

# Expense Tracker

记账工具，帮助管理个人财务。

## 功能

- ✅ 收支记录
- ✅ 分类统计
- ✅ 预算管理
- ✅ 报表导出
- ✅ 多账户支持

## 使用

```bash
# 添加支出
clawhub expense add --amount 50 --category "餐饮" --note "午餐"

# 添加收入
clawhub expense income --amount 5000 --category "工资"

# 查看统计
clawhub expense stats --month 2026-04

# 设置预算
clawhub expense budget --category "餐饮" --limit 1500
```

## 定价

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | ¥0 | 基础记账 |
| Pro 版 | ¥49 | 预算 + 报表 |
| 订阅版 | ¥12/月 | Pro+ 多账户 |
