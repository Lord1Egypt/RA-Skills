# Agent Eval Suite

Agent 评估套件，提供基准测试、A/B测试、性能回归检测和模拟环境测试。

## 功能特性

### 1. 基准测试框架
- 标准化测试用例
- 多维度评估指标
- 基准对比
- 评分系统

### 2. A/B 测试
- 对照组设计
- 随机分组
- 统计显著性检验
- 结果分析

### 3. 性能回归检测
- 历史性能对比
- 回归告警
- 性能趋势图
- 根因分析

### 4. 模拟环境测试
- 沙箱环境
- 场景模拟
- 边界条件测试
- 故障注入

## 安装

```bash
npm install
```

## 使用方法

### Benchmark

```javascript
const { Benchmark } = require('./src');

const benchmark = new Benchmark({ iterations: 100 });

benchmark.addTest('task-completion', {
  execute: async () => await agent.completeTask(task)
});

const results = await benchmark.run();
console.log(results);
```

### ABTester

```javascript
const { ABTester } = require('./src');

const ab = new ABTester({ confidenceLevel: 0.95 });

ab.createExperiment('new-prompt', {
  control: async () => await oldPrompt(),
  treatment: async () => await newPrompt()
});

const result = await ab.run('new-prompt', { sampleSize: 200 });
console.log(result); // { winner: 'treatment', confidence: 0.97 }
```

### RegressionDetector

```javascript
const { RegressionDetector } = require('./src');

const detector = new RegressionDetector({ threshold: 0.1 });

detector.record('response-time', { version: 'v1.1.0', value: 1200 });

const regressions = detector.detect();
console.log(regressions);
```

## 测试

```bash
npm test
```

## License

MIT
