# Order Tracker Skill

本地订单跟踪系统 — 手动状态管理 + 客户邮件通知 + 命令行看板

> 适用于 Farreach Electronic，task-005 产出物，由 IRON (qwen3.5-plus) 实现，WILSON 审阅通过。

---

## 功能概览

| 功能模块 | 脚本 | 说明 |
|----------|------|------|
| 订单状态更新 | `scripts/update-order-status.js` | 手动更新订单状态，含验证、日志、备份 |
| 客户邮件通知 | `scripts/send-order-notification.js` | 状态变更时发送双语通知邮件 |
| 订单看板 | `scripts/order-dashboard.js` | 命令行汇总视图，支持多种输出格式 |

---

## 目录结构

```
order-tracker/
├── README.md                        # 本文件
├── SKILL.md                         # AgentSkills 规范
├── package.json                     # Node.js 依赖
├── config/
│   └── order-schema.json            # 订单 JSON Schema（数据验证）
├── data/
│   └── orders.json                  # 订单数据文件（本地存储）
├── logs/
│   ├── status-changes.log           # 状态变更日志
│   └── notifications.log            # 邮件通知日志
└── scripts/
    ├── update-order-status.js       # 订单状态更新脚本
    ├── send-order-notification.js   # 客户邮件通知脚本
    └── order-dashboard.js           # 订单看板脚本
```

---

## 订单状态模型

订单生命周期共 6 个状态：

```
pending_production → in_production → ready_to_ship → shipped → completed
                                                             ↘ cancelled (任意阶段可取消)
```

| 状态 | 中文 | 说明 |
|------|------|------|
| `pending_production` | 待生产 | 订单已确认，等待生产排期 |
| `in_production` | 生产中 | 工厂已开始生产 |
| `ready_to_ship` | 待发货 | 生产完成，等待发货安排 |
| `shipped` | 已发货 | 货物已发出，提供跟踪信息 |
| `completed` | 已完成 | 客户确认收货，订单关闭 |
| `cancelled` | 已取消 | 订单取消 |

### 合法状态流转

| 当前状态 | 可流转到 |
|----------|---------|
| `pending_production` | `in_production`, `cancelled` |
| `in_production` | `ready_to_ship`, `cancelled` |
| `ready_to_ship` | `shipped`, `cancelled` |
| `shipped` | `completed`, `cancelled` |
| `completed` | _(终态)_ |
| `cancelled` | _(终态)_ |

---

## 快速开始

### 环境要求

- Node.js v16+
- 网易企业邮 SMTP 配置（`imap-smtp-email` skill 的 `.env` 文件）

### 安装依赖

```bash
cd /Users/wilson/.openclaw/workspace/skills/order-tracker
npm install
```

### 添加新订单

直接编辑 `data/orders.json`，参考现有订单格式，或使用 `config/order-schema.json` 验证结构。

---

## 使用说明

### 1. 订单状态更新

```bash
cd scripts/

# 查看帮助
node update-order-status.js --help

# 预览变更（不写入）
node update-order-status.js --order-id ORD-20260324-001 --status ready_to_ship --dry-run

# 更新状态
node update-order-status.js --order-id ORD-20260324-001 --status ready_to_ship --notes "生产完成，等待发货"

# 更新状态并标记需要发送通知
node update-order-status.js --order-id ORD-20260324-001 --status shipped \
  --notes "已通过 DHL 发出，单号 1234567890" \
  --trigger-notification

# 使用自定义数据文件路径
node update-order-status.js --order-id ORD-xxx --status completed \
  --orders-file /path/to/orders.json
```

**选项说明：**

| 参数 | 必需 | 说明 |
|------|------|------|
| `--order-id` | ✅ | 订单 ID |
| `--status` | ✅ | 新状态（见状态模型） |
| `--notes` | ❌ | 变更备注 |
| `--dry-run` | ❌ | 预览模式，不写入文件 |
| `--trigger-notification` | ❌ | 标记需要发送客户通知 |
| `--orders-file` | ❌ | 自定义 orders.json 路径 |
| `--schema-file` | ❌ | 自定义 schema 路径 |

---

### 2. 发送客户邮件通知

> **依赖：** 需要 `imap-smtp-email` skill 的 `.env` 文件，路径为  
> `/Users/wilson/.openclaw/workspace/skills/imap-smtp-email/.env`

```bash
cd scripts/

# 预览邮件（不发送）
node send-order-notification.js --order-id ORD-20260324-001 --dry-run

# 发送通知
node send-order-notification.js --order-id ORD-20260324-001

# 覆盖状态（发送指定状态的通知模板）
node send-order-notification.js --order-id ORD-20260324-001 --status shipped

# 使用自定义数据文件
node send-order-notification.js --order-id ORD-xxx --orders-file /path/to/orders.json
```

**选项说明：**

| 参数 | 必需 | 说明 |
|------|------|------|
| `--order-id` | ✅ | 订单 ID |
| `--status` | ❌ | 覆盖状态（默认用订单当前状态） |
| `--dry-run` | ❌ | 预览邮件内容，不实际发送 |
| `--orders-file` | ❌ | 自定义 orders.json 路径 |

**支持的邮件模板（5 种状态）：**
- `in_production` — 生产进度通知
- `ready_to_ship` — 准备发货通知
- `shipped` — 发货确认（含物流信息）
- `completed` — 订单完成确认
- `cancelled` — 取消通知

---

### 3. 订单看板

```bash
cd scripts/

# 显示所有订单（按状态分组）
node order-dashboard.js

# 按状态过滤
node order-dashboard.js --status in_production
node order-dashboard.js --status shipped

# 查看单个订单详情
node order-dashboard.js --order-id ORD-20260324-001

# 输出格式
node order-dashboard.js --format table    # 完整表格（默认）
node order-dashboard.js --format compact  # 紧凑表格
node order-dashboard.js --format json     # JSON 导出

# 组合使用
node order-dashboard.js --status shipped --format json
```

**看板功能：**
- 📊 订单汇总统计（总订单数、总金额、各状态分布）
- 🚨 逾期订单检测（交期已过且未完成）
- ⚡ 紧急订单检测（≤7 天交期且未完成）
- 🎨 ANSI 颜色区分状态

---

## 典型工作流

### 订单从生产到发货的完整流程

```bash
# Step 1: 生产开始，更新状态并通知客户
node update-order-status.js \
  --order-id ORD-20260324-001 \
  --status in_production \
  --notes "工厂已排期，预计4月15日完成"
node send-order-notification.js --order-id ORD-20260324-001

# Step 2: 生产完成，准备发货
node update-order-status.js \
  --order-id ORD-20260324-001 \
  --status ready_to_ship \
  --notes "生产完成，QC 通过，等待装箱"

# Step 3: 发货，更新物流信息
node update-order-status.js \
  --order-id ORD-20260324-001 \
  --status shipped \
  --notes "DHL Express, 单号: 1234567890, ETA: 4月25日"
node send-order-notification.js --order-id ORD-20260324-001

# Step 4: 确认收货
node update-order-status.js \
  --order-id ORD-20260324-001 \
  --status completed \
  --notes "客户确认收货"
node send-order-notification.js --order-id ORD-20260324-001

# 随时查看看板
node order-dashboard.js
```

---

## 数据格式

### orders.json 结构

```json
{
  "orders": [
    {
      "order_id": "ORD-20260324-001",
      "customer_name": "Michael Chen",
      "customer_email": "michael.chen@techsource.com",
      "customer_company": "TechSource Electronics Ltd",
      "product_list": [
        {
          "sku": "SKW-HDMI-2.1-2M",
          "name": "HDMI 2.1 Cable 2M",
          "quantity": 500,
          "unit_price": 8.5,
          "currency": "USD"
        }
      ],
      "quantity": 500,
      "unit_price": 8.5,
      "total_amount": 4250,
      "currency": "USD",
      "delivery_date": "2026-04-20",
      "status": "in_production",
      "status_history": [
        {
          "status": "pending_production",
          "changed_at": "2026-03-24T10:30:00+08:00",
          "changed_by": "jaden",
          "notes": "订单确认",
          "notification_sent": true
        }
      ],
      "shipping_address": "...",
      "notes": "...",
      "created_at": "2026-03-24T10:30:00+08:00",
      "updated_at": "2026-03-24T15:00:00+08:00"
    }
  ]
}
```

完整字段定义见 `config/order-schema.json`（JSON Schema draft-07）。

---

## SMTP 配置

通知脚本复用 `imap-smtp-email` skill 的 SMTP 配置，无需单独配置：

```
依赖文件：/Users/wilson/.openclaw/workspace/skills/imap-smtp-email/.env
```

`.env` 需包含：
```env
SMTP_HOST=smtphz.qiye.163.com
SMTP_PORT=465
SMTP_SECURE=true
SMTP_USER=sale-9@farreach-electronic.com
SMTP_PASS=<password>
```

---

## 日志文件

| 日志 | 路径 | 内容 |
|------|------|------|
| 状态变更 | `logs/status-changes.log` | 每次状态更新记录 |
| 邮件通知 | `logs/notifications.log` | 发送/失败的通知记录 |

---

## 约束与扩展说明

### 当前约束（task-005 设计决策）

- ❌ 不对接工厂生产系统（ERP/MES）
- ❌ 不抓取物流 API（17TRACK/顺丰等）
- ✅ 状态手动更新（CLI 脚本）
- ✅ 数据存储本地 JSON 文件

### 未来可扩展方向

- 接入工厂 ERP 系统自动同步生产状态
- 接入 17TRACK API 自动更新物流轨迹
- 添加 Web UI 界面
- 接入 OKKI CRM 同步订单数据

---

## 依赖

| 包 | 版本 | 用途 |
|----|------|------|
| `nodemailer` | ^7.0 | SMTP 邮件发送 |
| `dotenv` | ^16.0 | 环境变量加载 |

---

## 开发历史

- **2026-03-24** — task-005 完成，所有 5 个子任务通过审阅
- **2026-03-24** — WILSON 修复 `order-dashboard.js` 中 `COLORS.black` 未定义 bug
- 执行方：IRON (bailian/qwen3.5-plus)
- 审阅方：WILSON (aiberm/claude-sonnet-4-6)
