# Agent Reliability

Agent 可靠性框架，解决多步工作流中准确率递减问题。

## 功能特性

### 1. 错误率监控
- 实时错误率追踪
- 历史趋势分析
- 异常检测告警
- 错误分类统计

### 2. 自动回退机制
- 失败检测触发
- 回退策略配置
- 状态恢复
- 优雅降级

### 3. 置信度评估
- 单步置信度计算
- 累积置信度追踪
- 阈值告警
- 置信度可视化

### 4. 多 Agent 投票共识
- 投票策略（简单多数/加权/一致）
- 冲突解决
- 共识达成判定

## 安装

```bash
npm install
```

## 使用方法

### ReliabilityMonitor

```javascript
const { ReliabilityMonitor } = require('./src');

const monitor = new ReliabilityMonitor({
  errorThreshold: 0.15,
  confidenceThreshold: 0.85,
  historyWindow: 100
});

// 记录执行结果
monitor.record({
  stepId: 'step-1',
  success: true,
  confidence: 0.92,
  duration: 1500
});

// 获取可靠性评分
const score = monitor.getReliabilityScore();
console.log(score); // { overall: 0.87, byStep: {...}, trend: 'improving' }
```

### FallbackManager

```javascript
const { FallbackManager } = require('./src');

const fallback = new FallbackManager({
  maxRetries: 3,
  backoffStrategy: 'exponential'
});

const result = await fallback.execute(async () => {
  return await riskyOperation();
}, {
  fallback: async () => await safeOperation()
});
```

### VotingConsensus

```javascript
const { VotingConsensus } = require('./src');

const consensus = new VotingConsensus({
  strategy: 'weighted-majority',
  minAgreement: 0.7
});

consensus.vote('agent-1', { decision: 'approve', confidence: 0.9, weight: 2 });
consensus.vote('agent-2', { decision: 'approve', confidence: 0.8, weight: 1 });

const result = consensus.resolve();
console.log(result); // { decision: 'approve', confidence: 0.87, agreement: 0.75 }
```

## 测试

```bash
npm test
```

## License

MIT
