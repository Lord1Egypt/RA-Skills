# Auto Optimizer

自动性能优化工具，用于监控、分析和优化 OpenClaw 技能的性能。

## 功能

1. **性能监控** - 实时监控技能执行时间和资源使用
2. **瓶颈检测** - 自动识别性能瓶颈和代码异味
3. **优化建议** - 基于分析结果生成优化建议
4. **自动应用** - 自动应用优化到代码

## 安装

```bash
# 技能已内置，无需额外安装
```

## 使用方法

### 基础用法

```javascript
const { AutoOptimizer } = require('./skills/auto-optimizer/src');

// 创建优化器实例
const optimizer = new AutoOptimizer({
  monitor: {
    executionTimeThreshold: 5000,  // 5秒
    memoryUsageThreshold: 100 * 1024 * 1024  // 100MB
  }
});

// 监控技能执行
async function runSkill() {
  const { result, metrics } = await optimizer.monitorOperation(
    'op-001',
    'my-skill',
    async () => {
      // 技能逻辑
      return await someOperation();
    }
  );
  
  console.log('Execution time:', metrics.metrics.duration + 'ms');
  return result;
}

// 分析技能性能
const analysis = optimizer.analyzeSkill('my-skill');
console.log(analysis);

// 生成优化方案
const plan = optimizer.generatePlan('my-skill');
console.log(plan);

// 应用优化
const result = await optimizer.optimizeSkill('my-skill', {
  skillPath: './skills/my-skill'
});
```

### 单独使用模块

```javascript
// 仅使用监控模块
const { PerformanceMonitor } = require('./skills/auto-optimizer/src');
const monitor = new PerformanceMonitor();

monitor.startOperation('op-1', 'skill-name');
// ... 执行操作
const metrics = monitor.endOperation('op-1', result);

// 仅使用分析模块
const { BottleneckAnalyzer } = require('./skills/auto-optimizer/src');
const analyzer = new BottleneckAnalyzer();

const analysis = analyzer.analyzeSkill('skill-name', metricsHistory);

// 仅使用优化引擎
const { OptimizationEngine } = require('./skills/auto-optimizer/src');
const engine = new OptimizationEngine();

const plan = engine.generateOptimizationPlan(analysis);

// 仅使用应用器
const { OptimizationApplier } = require('./skills/auto-optimizer/src');
const applier = new OptimizationApplier({ dryRun: true });

await applier.applyOptimizationPlan(plan);
```

## API 参考

### PerformanceMonitor

```javascript
const monitor = new PerformanceMonitor(options);

// 开始监控
monitor.startOperation(operationId, skillName, metadata);

// 结束监控
monitor.endOperation(operationId, result, error);

// 获取技能统计
monitor.getSkillStats(skillName);

// 获取所有统计
monitor.getAllStats();

// 导出报告
monitor.exportReport('json' | 'csv');
```

### BottleneckAnalyzer

```javascript
const analyzer = new BottleneckAnalyzer(options);

// 分析单个技能
analyzer.analyzeSkill(skillName, metrics);

// 分析多个技能
analyzer.analyzeMultipleSkills({ skillName: metrics[] });

// 添加自定义规则
analyzer.addRule({
  id: 'custom-rule',
  name: 'Custom Rule',
  applicableTo: ['some-bottleneck'],
  check: (metrics) => ({ detected: boolean, confidence: number })
});

// 导出分析
analyzer.exportAnalysis(analysis, 'json' | 'markdown');
```

### OptimizationEngine

```javascript
const engine = new OptimizationEngine(options);

// 生成优化方案
engine.generateOptimizationPlan(analysis);

// 生成多技能方案
engine.generateMultiSkillPlan(analyses);

// 添加自定义策略
engine.addStrategy({
  id: 'custom-strategy',
  name: 'Custom Strategy',
  applicableTo: ['bottleneck-type'],
  generate: (bottleneck, context) => ({ title, description, actions })
});

// 导出方案
engine.exportPlan(plan, 'json' | 'markdown');
```

### OptimizationApplier

```javascript
const applier = new OptimizationApplier(options);

// 应用优化方案
await applier.applyOptimizationPlan(plan, context);

// 应用单个建议
await applier.applyRecommendation(recommendation, context);

// 设置干运行模式
applier.setDryRun(true);

// 回滚优化
applier.rollback(optimizationId);
```

## 检测的瓶颈类型

1. **高执行时间** - 操作执行时间过长
2. **内存泄漏** - 内存使用持续增长
3. **高错误率** - 错误率超过阈值
4. **性能退化** - 性能随时间下降
5. **性能不稳定** - 执行时间变异系数高
6. **GC压力** - 频繁的垃圾回收

## 优化策略

1. **缓存** - 实现 LRU 缓存减少重复计算
2. **异步处理** - 转换同步操作为异步
3. **内存修复** - 修复内存泄漏，正确清理资源
4. **错误处理** - 增强错误处理和重试机制
5. **批处理** - 批量处理减少开销
6. **性能监控** - 添加详细性能监控

## 配置选项

```