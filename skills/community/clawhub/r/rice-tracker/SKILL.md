---
name: rice-tracker
description: >
  大米采购管理系统 v2.0。记录每个客户的分批进货、消耗追踪、欠款追踪与对账管理。
  支持分批进货、欠款追踪、对公/对私转账、月底对账提醒。
  适用于：大米卖家追踪客户库存与应收款、团购组织者管理库存、家庭食材管理。
  Keywords: 大米, 库存管理, 采购提醒, 欠款追踪, 对账管理, 分批进货
version: 2.0.0
homepage: https://clawhub.com/skills/rice-tracker
author: 你的名字
tags: [实用工具, 库存管理, 采购提醒, 欠款管理, 对账]
---

# 🍚 大米采购管理系统 v2.0

记录每个客户的大米进货、消耗与应收款，自动计算库存剩余天数，支持分批进货、欠款追踪、月底对账提醒。

## v2.0 新功能

- ✅ **分批进货**：支持客户多次进货，自动汇总总库存
- ✅ **欠款追踪**：记录每笔进货的单价、金额、付款状态
- ✅ **对公/对私**：区分对私（微信/支付宝）和对公（公户转账）
- ✅ **月底结账**：设置结账日期，到期自动提醒收款
- ✅ **月度对账**：按月份统计每个客户的进货量、金额、已付、欠款
- ✅ **双提醒**：库存提醒 + 对账到期提醒

## 功能特性

### 📦 库存追踪
- 添加客户（姓名、手机号、人口、消耗频率）
- 自动汇总所有进货的总库存
- 计算剩余天数、预计吃完日期
- 状态标签：已耗尽（红）/ 即将耗尽（橙）/ 注意（蓝）/ 充足（绿）

### 📝 进货记录
- 支持分批多次进货
- 记录：日期、斤数、单价、金额
- 账户类型：对私（微信/支付宝）/ 对公（公户转账）
- 结账日期：设置月底结账日
- 一键标记已付款

### 💰 对账管理
- 按月份查看对账单
- 统计每个客户：进货量、总金额、已付、欠款
- 到期未付款自动提醒（逾期天数）
- 支持对公/对私分别统计

### 🔔 自动提醒（双重提醒）
- **库存提醒**：大米即将吃完时提醒采购
- **对账提醒**：结账日期到期但未付款时提醒收款

## 使用方式

### 📋 常用操作（告诉 AI 即可）

| 操作 | 示例 |
|:---|:---|
| 添加客户 | "添加客户：张三，手机13800138001，家里3口人" |
| 添加进货 | "张三又买了500斤，3.4元/斤，未付款，4月底结账" |
| 标记已付 | "张三那笔3400元的已付款了" |
| 查看库存 | "查看大米库存" |
| 查看对账 | "查看3月对账单" |
| 删除客户 | "删除张三的记录" |
| 测试提醒 | "运行一次大米检查" |

### 🌐 Web 界面

```bash
python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/app.py
```

- **电脑浏览器**：`http://localhost:5001`
- **手机浏览器**：`http://<本机IP>:5001`

界面包含 3 个 Tab：
1. **📦 库存追踪** - 客户库存状态一览
2. **📝 进货记录** - 添加/查看进货明细
3. **💰 对账管理** - 月度对账单与到期提醒

### 🔔 自动提醒

每天 20:00（Asia/Shanghai）自动检查，有提醒会自动推送：
- 📦 库存提醒：哪些客户大米快吃完
- 💰 对账提醒：哪些账目到期未付

## 文件结构

```
rice-tracker/
├── SKILL.md
└── scripts/
    ├── app.py              # Flask Web 主程序 (v2.0)
    └── check_alerts.py     # 每日检查脚本 (v2.0)
```

## 数据结构

```json
{
  "owner": "张三",
  "phone": "13800138001",
  "people": 3,
  "daily_rate": 0.4,
  "frequency": "daily",
  "purchases": [
    {
      "date": "2026-03-04",
      "quantity": 1000,
      "price_per_jin": 3.4,
      "total_amount": 3400,
      "paid": false,
      "settle_date": "2026-04-30",
      "account_type": "corporate",
      "note": "食堂第一批货"
    }
  ]
}
```

## 启动服务

```bash
# 启动 Web 服务（后台运行）
nohup python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/app.py \
  > ~/.openclaw/workspace/skills/rice-tracker/app.log 2>&1 &

# 测试提醒脚本
python3 ~/.openclaw/workspace/skills/rice-tracker/scripts/check_alerts.py
```

## 定时提醒配置

```bash
# 每天 20:00 自动检查并推送提醒
openclaw cron add --name "大米系统每日检查" \
  --schedule "0 20 * * *" \
  --timezone "Asia/Shanghai" \
  --message "请运行以下命令检查：\npython3 ~/.openclaw/workspace/skills/rice-tracker/scripts/check_alerts.py\n运行后将结果整理成消息发送给我。" \
  --channel webchat
```
