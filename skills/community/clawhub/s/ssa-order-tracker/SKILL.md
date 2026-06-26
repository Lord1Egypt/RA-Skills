---
name: order-tracker
description: "Track and manage sales orders with status updates, notifications, and dashboard reporting. Supports order creation, status transitions (pending/confirmed/shipped/delivered), email/Discord notifications, and order history visualization. Use when you need to monitor order fulfillment, send shipping updates to customers, or generate order analytics."
---
# Order Tracker Skill

## Description

本地订单跟踪系统，提供手动订单状态管理、客户邮件通知和命令行看板功能。适用于 Farreach Electronic 外贸订单生命周期管理（从生产到交付），无需对接工厂 ERP 或物流 API。

## When to Use

- 查询某个订单的当前状态
- 更新订单状态（生产中 → 待发货 → 已发货 → 已完成）
- 向客户发送订单状态变更邮件通知
- 查看所有在途订单的看板汇总
- 检测逾期或紧急（≤7 天）订单

## Prerequisites

- Node.js v16+
- 已配置 `imap-smtp-email` skill 的 SMTP `.env` 文件（用于发送通知邮件）
- 依赖安装：`npm install`（在 skill 目录下执行）

## Skills Directory

`skills/order-tracker/`

## How to Invoke

All scripts are run from the `scripts/` subdirectory.

### 1. View Order Dashboard

```bash
cd skills/order-tracker/scripts

# 查看所有订单（按状态分组）
node order-dashboard.js

# 按状态过滤
node order-dashboard.js --status in_production
node order-dashboard.js --status shipped

# 查看单个订单详情
node order-dashboard.js --order-id ORD-20260324-001

# 输出格式（table / compact / json）
node order-dashboard.js --format json
```

### 2. Update Order Status

```bash
cd skills/order-tracker/scripts

# 预览（dry-run，不写入）
node update-order-status.js --order-id ORD-20260324-001 --status ready_to_ship --dry-run

# 更新状态
node update-order-status.js \
  --order-id ORD-20260324-001 \
  --status shipped \
  --notes "DHL Express, 单号: 1234567890, ETA: 4月25日"

# 更新状态 + 标记需要发通知
node update-order-status.js \
  --order-id ORD-20260324-001 \
  --status in_production \
  --notes "工厂已排期" \
  --trigger-notification
```

### 3. Send Customer Notification Email

```bash
cd skills/order-tracker/scripts

# 预览邮件（不发送）
node send-order-notification.js --order-id ORD-20260324-001 --dry-run

# 发送通知（使用订单当前状态的邮件模板）
node send-order-notification.js --order-id ORD-20260324-001

# 指定状态模板发送
node send-order-notification.js --order-id ORD-20260324-001 --status shipped
```

## Order Status Model

6 状态机：

```
pending_production → in_production → ready_to_ship → shipped → completed
                                                              ↘ cancelled（任意阶段可取消）
```

| 状态 | 中文 | 说明 |
|------|------|------|
| `pending_production` | 待生产 | 订单确认，等待生产 |
| `in_production` | 生产中 | 工厂生产中 |
| `ready_to_ship` | 待发货 | 生产完成，等待发货 |
| `shipped` | 已发货 | 货物已发出 |
| `completed` | 已完成 | 客户确认收货 |
| `cancelled` | 已取消 | 订单取消 |

## Email Templates

通知脚本支持 5 种双语（EN/ZH）邮件模板：
- `in_production` — 生产进度通知
- `ready_to_ship` — 准备发货通知
- `shipped` — 发货确认（含物流单号）
- `completed` — 订单完成确认
- `cancelled` — 取消通知

## Typical Workflow Example

```bash
BASE=skills/order-tracker/scripts
ORDER=ORD-20260324-001

# 开始生产 + 通知客户
node $BASE/update-order-status.js --order-id $ORDER --status in_production --notes "工厂已排期"
node $BASE/send-order-notification.js --order-id $ORDER

# 发货 + 通知客户
node $BASE/update-order-status.js --order-id $ORDER --status shipped --notes "DHL 单号: 1234567890"
node $BASE/send-order-notification.js --order-id $ORDER

# 查看看板
node $BASE/order-dashboard.js
```

## Data Files

| 文件 | 路径 | 说明 |
|------|------|------|
| 订单数据 | `data/orders.json` | 所有订单（手动维护） |
| 订单 Schema | `config/order-schema.json` | JSON Schema 验证定义 |
| 状态变更日志 | `logs/status-changes.log` | 每次状态更新记录 |
| 通知日志 | `logs/notifications.log` | 邮件发送记录 |

## Constraints

- 不对接工厂 ERP/MES 系统
- 不抓取物流 API
- 状态手动更新
- 数据存储本地 JSON 文件

## Source

- Task: task-005（Phase 3）
- Implemented by: IRON (bailian/qwen3.5-plus)
- Reviewed by: WILSON (aiberm/claude-sonnet-4-6)
- Completed: 2026-03-24
