# approval-engine

> 审批流程引擎 + 异常处理系统 — 支持多级审批、异常检测、自动恢复与 Discord 通知

## 概述

`approval-engine` 是一个完整的业务审批与异常处理框架，专为 OpenClaw 工作流设计。它提供：

- **规则驱动的审批流程**：基于 JSON 配置定义触发条件、审批人层级和超时策略
- **异常检测与告警**：实时监测超时、系统错误、订单异常，自动发送分级告警
- **自动恢复策略**：支持重试、降级、人工介入三种恢复模式
- **Discord 通知集成**：所有审批请求和告警通过 Discord 实时推送

---

## 目录结构

```
approval-engine/
├── config/
│   └── approval-rules.json       # 审批规则配置（触发条件、审批人、超时策略）
├── src/
│   ├── approval-engine.js        # 核心引擎（创建/提交/超时检测/升级）
│   ├── rule-evaluator.js         # 规则评估器（触发条件、阈值判断）
│   ├── approval-store.js         # 审批状态存储（JSON 持久化）
│   ├── exception-detector.js     # 异常检测器（超时/系统错误/订单异常）
│   ├── alert-manager.js          # 告警管理（发送/限流/历史查询）
│   ├── exception-logger.js       # 异常日志（记录/查询/标记已解决）
│   ├── recovery-engine.js        # 恢复引擎（策略选择与执行）
│   ├── retry-handler.js          # 重试处理（指数退避、Jitter）
│   ├── escalation-handler.js     # 升级处理（告警升级到人工介入）
│   ├── discord-notifier.js       # Discord 通知（消息/Embed/审批请求）
│   ├── notification-router.js    # 通知路由（按规则选择通知渠道）
│   └── notification-templates.js # 通知模板（审批/告警/升级/恢复）
├── data/
│   └── approvals.json            # 审批状态持久化存储
├── logs/
│   ├── approval.log              # 审批流程日志
│   └── exceptions.json           # 异常记录存储
├── test/
│   └── smoke-test.sh             # 冒烟测试脚本
├── README.md
└── SKILL.md
```

---

## 快速开始

### 1. 触发审批流程

```javascript
const engine = require('./src/approval-engine');

// 自动评估规则并创建审批（如有规则匹配）
const result = await engine.autoCreateApprovals({
  quotation: { amount: 15000 },
  sales: { owner: 'alice' }
});

// 提交审批决策
await engine.submitApproval(approvalId, 'wilson', 'approved', '金额合理，已批准');

// 查询审批状态
const status = await engine.getApprovalStatus(approvalId);
console.log(status.status); // pending / approved / rejected / escalated
```

### 2. 异常检测

```javascript
const detector = require('./src/exception-detector');

// 运行全量检测（超时 + 系统错误 + 订单异常）
const exceptions = await detector.detectAll();

// 运行定时周期检测（通常在 cron job 里调用）
await detector.runPeriodicCheck();
```

### 3. 发送告警

```javascript
const alertMgr = require('./src/alert-manager');

// 发送告警（自动限流，避免重复告警）
await alertMgr.sendAlert({
  type: 'approval_timeout',
  severity: 'high',
  title: '审批超时',
  message: '报价 QT-001 已超时 24h，请尽快处理',
  data: { approvalId: 'APR-001' }
});
```

### 4. 自动恢复

```javascript
const recovery = require('./src/recovery-engine');

// 根据异常类型自动选择并执行恢复策略
const result = await recovery.recover({
  type: 'api_error',
  severity: 'medium',
  data: { endpoint: '/api/orders', error: 'timeout' }
});

// result.strategy: 'retry' | 'degrade' | 'manual_intervention'
```

### 5. Discord 通知

```javascript
const notifier = require('./src/discord-notifier');

// 发送审批请求到 Discord
await notifier.sendApprovalRequest({
  approvalId: 'APR-001',
  rule: '报价超权限审批',
  amount: 15000,
  submitter: 'alice'
});

// 发送告警
await notifier.sendAlert({
  title: '系统异常',
  message: 'API 连接超时',
  severity: 'high'
});
```

---

## 配置指南

### 审批规则配置 (`config/approval-rules.json`)

```json
{
  "rules": [
    {
      "id": "quotation-approval",
      "name": "报价超权限审批",
      "enabled": true,
      "trigger": {
        "type": "threshold",
        "field": "quotation.amount",
        "operator": ">",
        "reference": "thresholds.quotation_amount_limit"
      },
      "approvers": [
        {
          "level": 1,
          "role": "sales_manager",
          "user_ids": ["wilson"],
          "notification_channel": "discord"
        }
      ],
      "approval_type": "serial",
      "timeout_hours": 24,
      "timeout_action": "escalate"
    }
  ],
  "thresholds": {
    "quotation_amount_limit": 10000
  }
}
```

**关键字段说明：**

| 字段 | 说明 | 可选值 |
|------|------|--------|
| `trigger.type` | 触发类型 | `threshold` / `status` / `event` |
| `trigger.operator` | 比较运算符 | `>` `<` `>=` `<=` `==` `!=` `in` `not_in` |
| `approval_type` | 审批类型 | `serial`（串行） / `parallel`（并行） |
| `timeout_action` | 超时动作 | `escalate` / `auto_approve` / `auto_reject` |

### Discord 渠道配置

在 `src/alert-manager.js` 中的 `DISCORD_CHANNELS` 定义了渠道映射：

```javascript
const DISCORD_CHANNELS = {
  approvals: process.env.DISCORD_APPROVALS_CHANNEL,
  alerts: process.env.DISCORD_ALERTS_CHANNEL,
  exceptions: process.env.DISCORD_EXCEPTIONS_CHANNEL,
  recovery: process.env.DISCORD_RECOVERY_CHANNEL
};
```

**环境变量：**

```bash
DISCORD_BOT_TOKEN=your_bot_token
DISCORD_APPROVALS_CHANNEL=channel_id_for_approvals
DISCORD_ALERTS_CHANNEL=channel_id_for_alerts
DISCORD_EXCEPTIONS_CHANNEL=channel_id_for_exceptions
DISCORD_RECOVERY_CHANNEL=channel_id_for_recovery
```

---

## API 参考

### approval-engine.js

| 方法 | 签名 | 说明 |
|------|------|------|
| `createApproval` | `(ruleId, data, context) → approval` | 手动创建审批 |
| `submitApproval` | `(id, approver, decision, comment) → result` | 提交审批决策 |
| `getApprovalStatus` | `(id) → approval` | 查询审批状态 |
| `checkTimeouts` | `() → expired[]` | 检查并处理超时审批 |
| `triggerEscalation` | `(id, reason) → result` | 手动触发升级 |
| `autoCreateApprovals` | `(data) → approvals[]` | 自动匹配规则并创建审批 |
| `getStats` | `() → stats` | 获取统计数据 |
| `listApprovals` | `(filter) → approvals[]` | 列出审批（支持过滤） |

### exception-detector.js

| 方法 | 说明 |
|------|------|
| `detectAll()` | 运行所有检测规则 |
| `detectApprovalTimeout()` | 检测审批超时 |
| `detectSystemError()` | 检测系统错误 |
| `detectOrderAnomaly()` | 检测订单异常 |
| `runPeriodicCheck()` | 定时周期检测（含告警发送） |

### recovery-engine.js

| 方法 | 说明 |
|------|------|
| `recover(exception)` | 自动选择并执行恢复策略 |
| `getRecoveryStrategy(type, severity)` | 获取推荐恢复策略 |
| `executeStrategy(strategy, context)` | 执行指定恢复策略 |
| `getRecoveryStats()` | 获取恢复成功率统计 |

---

## 运行测试

```bash
# 冒烟测试（验证所有模块加载与基本功能）
bash test/smoke-test.sh

# 手动运行异常检测
node -e "require('./src/exception-detector').detectAll().then(console.log)"

# 查看当前审批队列
node -e "require('./src/approval-store').getPendingApprovals().then(console.log)"
```

---

## 日志与监控

- **审批日志**：`logs/approval.log` — 所有审批操作的时序日志
- **异常记录**：`logs/exceptions.json` — 结构化异常数据，支持查询和统计
- **审批数据**：`data/approvals.json` — 审批状态持久化

```bash
# 查看最近审批操作
tail -50 logs/approval.log

# 查看未解决异常
node -e "
  const logger = require('./src/exception-logger');
  logger.getExceptions({ resolved: false }).then(e => console.log(JSON.stringify(e, null, 2)));
"
```

---

## 版本信息

- **版本：** 1.0.0
- **创建时间：** 2026-03-24
- **任务 ID：** task-006 (Phase 3)
- **总代码行数：** ~3,800 LOC (JS) + 450 行配置
