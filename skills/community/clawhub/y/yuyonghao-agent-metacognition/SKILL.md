# Agent Metacognition

元认知系统，使 Agent 具备自我监控、反思能力和学习策略调整能力。

## 功能特性

### 1. 自我监控
- 执行状态监控
- 决策过程追踪
- 置信度评估

### 2. 反思能力
- 执行后反思
- 错误分析
- 经验积累

## 安装

```bash
npm install
```

## 使用方法

### MetacognitionSystem

```javascript
const { MetacognitionSystem } = require('./src');

const meta = new MetacognitionSystem();

// 监控执行
const result = await meta.monitorExecution(async () => {
  return await agent.process(task);
}, { taskId: 'task-1' });

// 反思
const reflection = await meta.reflect('task-1');

// 获取状态
const state = meta.getMetacognitiveState();
```

## 测试

```bash
npm test
```

## License

MIT
