---
name: approval-engine
description: 审批流程引擎 + 异常处理系统 — 规则驱动的多级审批、异常检测、自动恢复策略和 Discord 通知集成
---

# approval-engine Skill

## Description

审批流程引擎 + 异常处理系统。提供规则驱动的多级审批、实时异常检测、自动恢复策略（重试/降级/人工介入）和 Discord 通知集成。

## When to Use

- 需要对业务操作（报价、订单、权限变更）实施审批控制时
- 需要检测和告警系统/业务异常（超时、错误率升高、订单异常）时
- 需要配置自动恢复策略（API 失败重试、服务降级）时
- 需要通过 Discord 推送审批请求和告警时

## Location

`<approval-engine-root>/` 或 `$APPROVAL_ENGINE_ROOT`

## Modules

| 模块 | 用途 |
|------|------|
| `src/approval-engine.js` | 核心审批引擎（创建、提交、超时、升级） |
| `src/rule-evaluator.js` | 规则评估（触发条件、阈值、条件匹配） |
| `src/approval-store.js` | 审批状态 CRUD（JSON 持久化） |
| `src/exception-detector.js` | 异常检测（超时/错误/订单异常） |
| `src/alert-manager.js` | 告警发送（Discord、限流、历史） |
| `src/exception-logger.js` | 异常日志（记录、查询、解决标记） |
| `src/recovery-engine.js` | 恢复引擎（策略选择与执行） |
| `src/retry-handler.js` | 重试处理（指数退避、Jitter、统计） |
| `src/escalation-handler.js` | 升级处理（创建、确认、解决升级单） |
| `src/discord-notifier.js` | Discord 通知（消息/Embed/审批/告警） |
| `src/notification-router.js` | 通知路由（规则匹配→渠道选择） |
| `src/notification-templates.js` | 通知模板（审批/告警/升级/恢复） |

## Configuration

编辑 `config/approval-rules.json` 配置：
- `rules[]` — 审批规则列表（触发条件、审批人、超时策略）
- `thresholds` — 数值阈值（报价金额上限等）
- `auto_recovery` — 自动恢复策略映射
- `escalation_rules` — 升级规则（升级时间、升级对象）
- `notification_templates` — Discord 消息模板

所需环境变量：
- `DISCORD_BOT_TOKEN` — Discord 机器人令牌
- `DISCORD_APPROVALS_CHANNEL` — 审批通知渠道 ID
- `DISCORD_ALERTS_CHANNEL` — 告警通知渠道 ID
- `DISCORD_EXCEPTIONS_CHANNEL` — 异常通知渠道 ID
- `DISCORD_RECOVERY_CHANNEL` — 恢复通知渠道 ID

## Invocation

### 触发审批（自动匹配规则）

```javascript
const engine = require('<approval-engine-root>/src/approval-engine');
// 或使用环境变量
const engine = require(process.env.APPROVAL_ENGINE_ROOT + '/src/approval-engine');

// 提交业务数据，引擎自动评估规则
const approvals = await engine.autoCreateApprovals({
  quotation: { amount: 15000 },
  sales: { owner: 'alice' }
});
// 返回：所有被触发规则创建的审批列表
```

### 手动创建并提交审批

```javascript
const engine = require('<approval-engine-root>/src/approval-engine');
// 或使用环境变量
const engine = require(process.env.APPROVAL_ENGINE_ROOT + '/src/approval-engine');

// 创建审批
const approval = await engine.createApproval('quotation-approval', {
  quotation: { amount: 15000, no: 'QT-2026-001' }
}, { submitter: 'alice' });

// 审批人决策
await engine.submitApproval(approval.id, 'wilson', 'approved', '金额合理，已审批');

// 查询状态
const status = await engine.getApprovalStatus(approval.id);
```

### 异常检测（周期巡检）

```javascript
const detector = require('<approval-engine-root>/src/exception-detector');
// 或使用环境变量
const detector = require(process.env.APPROVAL_ENGINE_ROOT + '/src/exception-detector');

// 全量检测（返回新发现的异常列表）
const exceptions = await detector.detectAll();

// 定时周期检测（含告警推送 Discord）
await detector.runPeriodicCheck();
```

### 自动恢复

```javascript
const recovery = require('<approval-engine-root>/src/recovery-engine');

// 自动选择恢复策略并执行
const result = await recovery.recover({
  type: 'api_error',        // 异常类型
  severity: 'medium',       // 严重程度: low/medium/high/critical
  data: { endpoint: '/api/orders', error: 'timeout' }
});
// result.strategy: 'retry' | 'degrade' | 'manual_intervention'
// result.success: true/false
```

### 发送 Discord 通知

```javascript
const notifier = require('<approval-engine-root>/src/discord-notifier');

// 发送审批请求（带按钮/Embed）
await notifier.sendApprovalRequest({
  approvalId: 'APR-001',
  rule: '报价超权限审批',
  submitter: 'alice',
  amount: 15000
});

// 发送告警
await notifier.sendAlert({ title: 'API 超时', message: '订单 API 无响应', severity: 'high' });

// 发送恢复通知
await notifier.sendRecoveryNotification({ type: 'retry', success: true, attempts: 2 });
```

### 重试处理

```javascript
const retry = require('<approval-engine-root>/src/retry-handler');

// 带自动重试执行异步函数（指数退避 + Jitter）
const result = await retry.withRetry(
  async () => await fetch('https://api.example.com/orders'),
  { maxAttempts: 3, baseDelayMs: 1000, maxDelayMs: 10000 }
);
```

### 超时检测与升级

```javascript
const engine = require('<approval-engine-root>/src/approval-engine');

// 检测超时审批并自动升级
const expired = await engine.checkTimeouts();
// expired[].action: 'escalate' | 'auto_approve' | 'auto_reject'
```

## Examples

### 完整业务流程示例

```javascript
const engine = require('<approval-engine-root>/src/approval-engine');
const detector = require('<approval-engine-root>/src/exception-detector');
const recovery = require('<approval-engine-root>/src/recovery-engine');

async function processQuotation(quotationData) {
  // 1. 提交报价，自动触发审批规则
  const approvals = await engine.autoCreateApprovals(quotationData);
  
  if (approvals.length > 0) {
    console.log(`已创建 ${approvals.length} 个审批请求，等待审批中...`);
    // Discord 通知已在引擎内部自动发送
  }
  
  // 2. 运行异常检测
  const exceptions = await detector.detectAll();
  
  // 3. 对每个异常尝试自动恢复
  for (const exc of exceptions) {
    const result = await recovery.recover(exc);
    if (!result.success) {
      console.log(`异常 ${exc.type} 需要人工介入`);
    }
  }
}
```

### Cron 集成（定时巡检）

```bash
# 每 15 分钟运行一次异常检测和超时处理
*/15 * * * * node -e "
  const engine = require(process.env.APPROVAL_ENGINE_ROOT + '/src/approval-engine');
  const detector = require(process.env.APPROVAL_ENGINE_ROOT + '/src/exception-detector');
  Promise.all([engine.checkTimeouts(), detector.runPeriodicCheck()])
    .then(() => process.exit(0))
    .catch(e => { console.error(e); process.exit(1); });
" >> /tmp/approval-engine-cron.log 2>&1
```

## Testing

```bash
# 运行冒烟测试
bash $APPROVAL_ENGINE_ROOT/test/smoke-test.sh
```

## Related Skills

- `quotation-workflow` — 报价单工作流（可集成审批触发）
- `imap-smtp-email` — 邮件通知渠道（审批通知邮件发送）
- `discord` (OpenClaw built-in) — Discord 消息发送底层

## Version

1.0.0 — 2026-03-24 (task-006, Phase 3, iteration 7)
