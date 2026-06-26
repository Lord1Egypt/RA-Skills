---
name: logistics-tracker
description: 物流跟踪技能，对接 17Track 批量 API，自动跟踪运单状态，向客户发送邮件通知，并在异常时告警。
---

# logistics-tracker

**物流跟踪 Skill** — 对接 17Track 批量 API，自动跟踪运单状态，向客户发送邮件通知，并在异常时告警。

---

## 概述

| 属性 | 值 |
|------|-----|
| 版本 | 1.0.0 |
| 状态 | 生产就绪 |
| 依赖 | `order-tracker`, `imap-smtp-email` |
| API | [17Track REST v2.2](https://api.17track.net/) |
| Node.js | ≥ 18 |

## 功能特性

- **17Track 批量查询** — 单次最多 40 运单，自动分批
- **智能刷新调度** — 新单每 6h，在途每 24h，临近到达加密查询
- **配额管理** — 免费版 100 次/天，四级监控 + 降级策略
- **完整状态机** — 9 种状态（待发货→运输中→清关→派送→签收 + 退回/丢失/拒收）
- **客户邮件通知** — 发货 + 签收默认推送，中间节点 opt-in，eventId 幂等
- **异常检测告警** — 超时无更新、清关滞留、退回、丢失 → Discord + 邮件双渠道
- **运单号自动提取** — 从邮件正文提取 DHL/FedEx/UPS/SF/EMS 等格式运单号
- **原子写入** — write→rename 防并发，事件 eventId 去重
- **Exponential Backoff** — 失败重试 3 次（1/5/15 分钟）

---

## 目录结构

```
logistics-tracker/
├── config/
│   └── logistics-config.json     # 全局配置
├── data/
│   ├── shipments.json            # 运单状态持久化
│   ├── shipments/                # 备份目录
│   └── alert-history.json        # 告警历史去重
├── scripts/
│   ├── tracking-api.js           # 17Track API 适配器
│   ├── shipment-store.js         # 运单状态管理
│   ├── customer-notify.js        # 客户邮件通知
│   ├── scheduler.js              # 主调度器（cron 入口）
│   ├── anomaly-detector.js       # 异常检测告警
│   └── tracking-extractor.js     # 运单号提取器
├── templates/                    # 邮件模板目录（预留）
├── package.json
└── SKILL.md                      # 本文件
```

---

## 配置说明

### 必填配置项

编辑 `config/logistics-config.json`：

```json
{
  "api": {
    "17track": {
      "apiKey": "YOUR_17TRACK_API_KEY_HERE",
      "batchSize": 40
    }
  }
}
```

> 申请 17Track API Key：https://api.17track.net/  
> 免费版：100 次/天，单次最多 40 运单

### SMTP 集成

运单通知通过 `imap-smtp-email` skill 的 SMTP 发送：

```
/Users/wilson/.openclaw/workspace/skills/imap-smtp-email/scripts/smtp.js
```

确保 `imap-smtp-email` skill 的 `.env` 已配置正确的 SMTP 凭证。

### order-tracker 集成

异常检测器从 `order-tracker` 读取已发货订单自动创建跟踪记录：

```
/Users/wilson/.openclaw/workspace/skills/order-tracker/data/orders.json
```

---

## 使用方法

### 主调度器（推荐入口）

```bash
cd /Users/wilson/.openclaw/workspace/skills/logistics-tracker

# 执行一次完整调度周期（查询 + 状态更新 + 通知 + 异常检测）
node scripts/scheduler.js

# Dry-run 模式（不实际发送通知）
node scripts/scheduler.js --dry-run

# 查看调度状态
node -e "const s = require('./scripts/scheduler'); s.getSchedulerStatus().then(console.log)"
```

### 异常检测

```bash
# 完整检测（同步订单 + 检测 + 告警）
node scripts/anomaly-detector.js

# 跳过 order-tracker 同步
node scripts/anomaly-detector.js --skip-sync

# 只检测，不发告警
node scripts/anomaly-detector.js --skip-alerts

# Dry-run
node scripts/anomaly-detector.js --dry-run
```

### 运单号提取器

```bash
# 从文本提取运单号
node scripts/tracking-extractor.js --text "Your UPS shipment 1Z999AA10123456784 has shipped"

# 从文件提取
node scripts/tracking-extractor.js --file /path/to/email.txt

# 设置最低置信度阈值
node scripts/tracking-extractor.js --text "..." --min-confidence=0.7
```

### 手动注册运单

```bash
node -e "
const store = require('./scripts/shipment-store');
store.upsertShipment({
  trackingNumber: '1Z999AA10123456784',
  carrier: 'ups',
  status: 'in_transit',
  orderId: 'ORD-001',
  customerEmail: 'customer@example.com'
}).then(() => console.log('Done'));
"
```

### 手动触发客户通知

```bash
node -e "
const notify = require('./scripts/customer-notify');
notify.sendShippedNotification({
  trackingNumber: '1Z999AA10123456784',
  carrier: 'ups',
  orderId: 'ORD-001',
  customerEmail: 'customer@example.com',
  customerName: 'John'
}).then(console.log);
"
```

---

## Cron 调度建议

在 crontab 中添加以下任务：

```bash
# 每 6 小时执行一次完整调度周期
0 */6 * * * cd /Users/wilson/.openclaw/workspace/skills/logistics-tracker && node scripts/scheduler.js >> /tmp/logistics-tracker.log 2>&1

# 每天早上 9 点执行异常检测（可独立运行，也会在 scheduler 中执行）
0 9 * * * cd /Users/wilson/.openclaw/workspace/skills/logistics-tracker && node scripts/anomaly-detector.js >> /tmp/logistics-anomaly.log 2>&1
```

> **注意：** 17Track 免费版每天 100 次配额。每 6h 跑一次（4次/天），每次最多 25 运单可安全使用。活跃运单超过 25 时，调度器会自动按优先级分配配额。

---

## API 参考

### tracking-api.js

| 函数 | 说明 |
|------|------|
| `registerTracking(trackingNumbers)` | 批量注册运单到 17Track |
| `getTrackingInfo(trackingNumbers)` | 批量查询运单状态 |
| `shouldRefresh(shipment)` | 判断运单是否需要刷新 |
| `filterForRefresh(shipments)` | 过滤需要刷新的运单列表 |
| `buildRefreshQueue(shipments)` | 构建优先级刷新队列 |
| `getQuotaStatus()` | 获取当日配额状态 |
| `incrementQuotaUsage(n)` | 增加配额计数 |
| `isQuotaExhausted()` | 检查配额是否耗尽 |

### shipment-store.js

| 函数 | 说明 |
|------|------|
| `getShipment(trackingNumber)` | 获取单个运单 |
| `upsertShipment(data)` | 创建或更新运单 |
| `addEvents(trackingNumber, events)` | 添加物流事件（自动去重） |
| `transitionStatus(trackingNumber, newStatus)` | 状态机流转 |
| `getAllShipments()` | 获取所有运单 |
| `getShipmentsByStatus(status)` | 按状态筛选 |
| `getStaleShipments(days)` | 获取超过 N 天无更新的运单 |

### customer-notify.js

| 函数 | 说明 |
|------|------|
| `sendNotification(shipment, event)` | 通用通知入口 |
| `sendShippedNotification(shipment)` | 发送发货通知 |
| `sendDeliveredNotification(shipment)` | 发送签收通知 |
| `sendEventNotification(shipment, event)` | 发送中间节点通知 |
| `processBatchNotifications(shipments)` | 批量通知处理 |
| `shouldNotify(shipment, eventType)` | 通知决策引擎 |

### anomaly-detector.js

| 函数 | 说明 |
|------|------|
| `detectAnomalies(shipments, opts)` | 批量异常检测 |
| `detectNoUpdateAnomaly(shipment)` | 超时无更新检测 |
| `detectCustomsHoldAnomaly(shipment)` | 清关滞留检测 |
| `detectReturnAnomaly(shipment)` | 退回检测 |
| `detectLostAnomaly(shipment)` | 丢失检测 |
| `sendAnomalyAlerts(anomalies, opts)` | 双渠道告警发送 |
| `syncShippedOrders(opts)` | 从 order-tracker 同步已发货订单 |
| `runFullDetection(opts)` | 完整检测流程 |

### tracking-extractor.js

| 函数 | 说明 |
|------|------|
| `extractTrackingNumbers(text, opts)` | 从文本提取所有运单号 |
| `extractFromEmail(emailObj, opts)` | 从邮件对象提取运单号 |
| `extractFromFile(filePath, opts)` | 从文件提取运单号 |
| `identifyCarrier(trackingNumber)` | 识别快递商 |
| `validateTrackingNumber(num, carrier)` | 验证运单号格式 |
| `linkToOrder(trackingNumber, ordersPath, opts)` | 关联到订单 |
| `processEmailBatch(emails, opts)` | 批量处理邮件 |

---

## 状态机

```
pending → in_transit → customs_clearance → out_for_delivery → delivered
                    ↘ returning → returned
                    ↘ lost
                    ↘ customer_rejected
```

---

## 依赖 Skills

| Skill | 路径 | 用途 |
|-------|------|------|
| `order-tracker` | `../order-tracker/` | 读取已发货订单，自动创建跟踪记录 |
| `imap-smtp-email` | `../imap-smtp-email/` | 通过 SMTP 发送客户邮件和告警通知 |

---

## 开发历史

- **Subtask 1** — 设计配置文件 `logistics-config.json`（8 快递商 + 5 阶段智能刷新 + 配额降级 + 异常阈值 + 通知幂等 + backoff 重试 + 9 状态状态机）
- **Subtask 2** — 创建 17Track API 适配器 `tracking-api.js`（批量注册+查询、3 路径响应解析、配额四级监控、pause_non_critical 降级、exponential backoff）
- **Subtask 3** — 创建状态管理 `shipment-store.js`（原子写入、9 状态状态机、eventId SHA256 去重、赔偿流程提醒）
- **Subtask 4** — 创建客户通知模块 `customer-notify.js`（3 套 HTML 模板、频率控制、决策引擎、17track 自助链接）
- **Subtask 5** — 创建主调度器 `scheduler.js`（8 步完整流程、配额预算管理、dry-run、CLI 入口）
- **Subtask 6** — 创建异常检测 `anomaly-detector.js`（4 类检测、Discord+邮件双渠道告警、order-tracker 同步、24h 去重）
- **Subtask 7** — 创建运单号提取器 `tracking-extractor.js`（8 快递商正则、置信度评分、邮件批量处理、订单关联）
