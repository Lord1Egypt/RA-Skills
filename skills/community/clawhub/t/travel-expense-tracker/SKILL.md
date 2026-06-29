---
name: travel-expense-tracker
display_name: 旅行记账助手
description: 旅行场景专项记账助手；多币种记录消费、汇率自动换算、分类统计与预算管理。当用户需要记录旅行花费、多币种换算记账、旅行预算管理、分类统计旅行支出时使用。
---

# 旅行记账助手

旅行花钱心里有数——多币种记账、汇率换算、分类统计、预算管理。

## 能力概览

| 序号 | 工具 | 说明 |
|------|------|------|
| 1 | add_expense | 记录一笔消费 |
| 2 | expense_summary | 查看消费汇总统计 |
| 3 | budget_check | 预算管理与超支提醒 |

## 工作流程

1. 根据用户需求判断调用哪个工具
2. 执行 `python3 scripts/expense_tracker.py <tool> '<json_params>'`
3. 解析JSON输出，以自然语言回复用户

## 工具参数说明

### add_expense
记录一笔消费。参数：trip(必填，旅行名称), amount(必填，金额), currency(必填，货币代码如CNY/JPY/USD/EUR), category(必填，分类如餐饮/交通/住宿/购物/门票/其他), description(选填，消费描述), date(选填，日期YYYY-MM-DD)

### expense_summary
查看消费汇总。参数：trip(必填，旅行名称), group_by(选填，分组方式category/date/currency，默认category)

### budget_check
预算管理与超支检查。参数：trip(必填), total_budget(选填，总预算CNY), daily_budget(选填，日均预算CNY), days(选填，旅行天数)

## 数据说明

- 记账数据存储在本地文件 travel_expenses/
- 汇率使用内置参考汇率，仅供参考
- 零配置，无需申请任何API Key
