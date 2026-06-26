---
name: usage-tracker
description: >
  Token 使用追踪系统。记录每个对话的输入/输出 token 消耗，累计统计，预算控制。
  当用户说"token统计"、"用量追踪"、"消耗了多少"、"花了我多少token"时触发。
---

# Usage Tracker - Token 使用追踪系统

## 核心概念

```
对话轮次 → 记录 usage → 累计统计 → 预算检查 → 超限警告
```

## 数据结构

```typescript
interface TokenUsage {
  input_tokens: number;
  output_tokens: number;
  cache_creation_input_tokens?: number;  // 缓存创建
  cache_read_input_tokens?: number;     // 缓存读取
}

interface TurnUsage {
  turn: number;
  prompt: string;
  usage: TokenUsage;
  timestamp: string;
}

interface UsageBudget {
  maxInputTokens: number;
  maxOutputTokens: number;
  maxTotalTokens: number;
  warningThreshold: number;  // 80%
}
```

## 追踪指标

| 指标 | 说明 |
|------|------|
| `input_tokens` | 输入 token 数 |
| `output_tokens` | 输出 token 数 |
| `total_tokens` | 总 token 数 |
| `cache_creation` | 缓存创建消耗 |
| `cache_read` | 缓存读取节省 |
| `turn_count` | 对话轮次 |
| `cost_estimate` | 费用估算 |

## API 使用

```javascript
const { UsageTracker } = require('./scripts/usage-tracker.mjs');

const tracker = new UsageTracker({
  maxTotalTokens: 100000,
  warningThreshold: 0.8
});

// 记录一次使用
tracker.record({
  input_tokens: 500,
  output_tokens: 200,
});

// 获取统计
const stats = tracker.getStats();
console.log(stats);
// {
//   totalInput: 1500,
//   totalOutput: 600,
//   totalTokens: 2100,
//   turnCount: 3,
//   avgInputPerTurn: 500,
//   avgOutputPerTurn: 200,
//   budgetUsedPercent: 2.1,
//   estimatedCost: 0.042
// }

// 检查是否超预算
const budget = tracker.checkBudget();
if (budget.exceeded) {
  console.log(`⚠️ 超出预算 ${budget.percent}%`);
}

// 获取历史
const history = tracker.getHistory();
```

## Token 估算（无需 API）

```javascript
// 简单估算（中英文都适用）
function estimateTokens(text) {
  // 中文约 1 token / 字符
  // 英文约 1 token / 4 字符
  const chineseChars = (text.match(/[\u4e00-\u9fff]/g) || []).length;
  const otherChars = text.length - chineseChars;
  return chineseChars + Math.ceil(otherChars / 4);
}
```

## 费用估算

基于 Claude API 定价（仅供参考）：

| 模型 | 输入 | 输出 |
|------|------|------|
| Claude 3.5 Sonnet | $3/1M | $15/1M |
| Claude 3 Opus | $15/1M | $75/1M |
| Claude 3 Haiku | $0.25/1M | $1.25/1M |

## 预算控制

```javascript
const tracker = new UsageTracker({
  maxTotalTokens: 50000,
  maxTurns: 20,
  onBudgetExceeded: (stats) => {
    console.log('⚠️ 预算超出！');
    console.log(`已用: ${stats.totalTokens} / ${stats.maxTotal}`);
  }
});
```

## 文件结构

```
usage-tracker/
├── SKILL.md              # 本文件
└── scripts/
    └── usage-tracker.mjs # 核心实现
```

---

_龙虾王子自我进化的成果 🦞_
