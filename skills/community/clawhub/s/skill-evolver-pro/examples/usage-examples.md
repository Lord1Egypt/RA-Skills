# skill-evolver 使用示例

**版本**：v0.2.0  
**更新时间**：2026-03-30

---

## 示例 1：基本事件订阅

```javascript
const { EventBus, SkillEvents, createSkillCalledEvent } = require('./src/event-bus');

// 创建事件总线
const eventBus = new EventBus();

// 订阅技能调用事件
const unsubscribe = eventBus.subscribe(SkillEvents.CALLED, (data) => {
  console.log(`📞 技能被调用：${data.skillName} by ${data.userId}`);
});

// 发布事件
eventBus.publish(SkillEvents.CALLED, {
  skillName: 'first-principle-analyzer',
  userId: 'user123',
  context: { query: '分析这个商业模式' }
});

// 取消订阅
unsubscribe();
```

---

## 示例 2：完整的技能调用追踪

```javascript
const { EventBus, SkillEvents } = require('./src/event-bus');

const eventBus = new EventBus();
const usageStats = { calls: 0, successes: 0, failures: 0 };

// 订阅所有事件
eventBus.subscribe(SkillEvents.CALLED, () => {
  usageStats.calls++;
});

eventBus.subscribe(SkillEvents.COMPLETED, (data) => {
  usageStats.successes++;
  console.log(`✅ 完成：${data.data.executionTime}ms`);
});

eventBus.subscribe(SkillEvents.FAILED, (data) => {
  usageStats.failures++;
  console.error(`❌ 失败：${data.data.error.message}`);
});

// 模拟技能调用
function callSkill(skillName, shouldSucceed = true) {
  eventBus.publish(SkillEvents.CALLED, { skillName, userId: 'user1' });
  
  setTimeout(() => {
    if (shouldSucceed) {
      eventBus.publish(SkillEvents.COMPLETED, {
        skillName,
        userId: 'user1',
        result: { success: true },
        executionTime: Math.random() * 1000
      });
    } else {
      eventBus.publish(SkillEvents.FAILED, {
        skillName,
        userId: 'user1',
        error: new Error('Something went wrong')
      });
    }
  }, 100);
}

// 运行测试
callSkill('skill-a', true);
callSkill('skill-b', false);
callSkill('skill-c', true);

setTimeout(() => {
  console.log('📊 使用统计:', usageStats);
}, 500);
```

---

## 示例 3：优化策略选择

```javascript
const { StrategySelector, FunctionEnhancementStrategy } = require('./src/strategies/optimization-strategies');

const selector = new StrategySelector();

// 场景 1：性能问题为主
const performanceShortcomings = [
  { type: 'performance', description: '执行速度慢', complexity: 'high', subtype: 'slow-execution' },
  { type: 'performance', description: '内存占用高', complexity: 'medium', subtype: 'high-memory' },
  { type: 'ux', description: '加载状态不明显', difficulty: 'easy' }
];

const strategy1 = selector.select(performanceShortcomings);
console.log('选择的策略:', strategy1.name);
// 输出：performance-optimization

const plan1 = strategy1.generatePlan(performanceShortcomings);
console.log('优化计划:', JSON.stringify(plan1, null, 2));

// 场景 2：功能缺失为主
const featureShortcomings = [
  { type: 'feature-missing', description: '缺少导出功能', impact: 'high' },
  { type: 'feature-missing', description: '缺少批量操作', impact: 'medium' }
];

const strategy2 = selector.select(featureShortcomings);
console.log('选择的策略:', strategy2.name);
// 输出：function-enhancement
```

---

## 示例 4：生成使用分析报告

```javascript
const { ReportFactory } = require('./src/factories/report-factory');

const usageData = {
  skillName: 'meta-skill-weaver',
  period: '最近 30 天',
  frequency: {
    daily: 150,
    weekly: 1050,
    monthly: 4500
  },
  successRate: {
    success: 0.92,
    failure: 0.08,
    successCount: 4140,
    failureCount: 360,
    failureTypes: [
      { type: 'timeout', count: 200, percentage: 55.6 },
      { type: 'invalid-input', count: 100, percentage: 27.8 },
      { type: 'internal-error', count: 60, percentage: 16.6 }
    ]
  },
  satisfaction: {
    average: 4.3,
    feedbackCount: 256,
    total: 256,
    distribution: {
      5: 120,
      4: 80,
      3: 40,
      2: 10,
      1: 6
    }
  },
  trends: [
    { date: '2026-03-24', calls: 140, successRate: 0.90, rating: 4.2 },
    { date: '2026-03-25', calls: 155, successRate: 0.93, rating: 4.3 },
    { date: '2026-03-26', calls: 160, successRate: 0.91, rating: 4.4 },
    { date: '2026-03-27', calls: 145, successRate: 0.94, rating: 4.3 },
    { date: '2026-03-28', calls: 150, successRate: 0.92, rating: 4.3 }
  ],
  insights: [
    { type: 'positive', description: '使用频率稳步增长，周环比 +15%' },
    { type: 'warning', description: '超时错误占失败的 55.6%，建议优化性能' },
    { type: 'info', description: '用户满意度维持在 4.3 分，表现良好' }
  ]
};

const report = ReportFactory.create('usage', usageData);
console.log(report.render());
```

---

## 示例 5：生成性能分析报告

```javascript
const { ReportFactory } = require('./src/factories/report-factory');

const performanceData = {
  skillName: 'first-principle-analyzer',
  sampleCount: 1000,
  executionTime: {
    average: 245,
    p50: 180,
    p95: 520,
    p99: 890,
    max: 1500,
    min: 50
  },
  resourceUsage: {
    memory: 128,
    memoryLimit: 512,
    memoryPercent: 25,
    cpu: 15,
    networkRequests: 5,
    diskIO: '2.5 MB/s'
  },
  bottlenecks: [
    {
      description: 'API 调用延迟高',
      severity: 'high',
      impact: '增加 200ms 平均执行时间',
      suggestion: '添加缓存层，减少重复 API 调用'
    },
    {
      description: 'JSON 解析慢',
      severity: 'medium',
      impact: '大输入时显著变慢',
      suggestion: '使用流式解析或优化数据结构'
    }
  ],
  score: {
    overall: 72,
    speed: 68,
    speedWeight: 0.4,
    efficiency: 75,
    efficiencyWeight: 0.3,
    stability: 74,
    stabilityWeight: 0.3
  },
  recommendations: [
    {
      title: '添加响应缓存',
      priority: 'high',
      expectedBenefit: '减少 40% API 调用，提升 30% 速度',
      difficulty: 'medium',
      estimatedTime: '4-6 hours'
    },
    {
      title: '优化数据结构',
      priority: 'medium',
      expectedBenefit: '减少 20% 内存占用',
      difficulty: 'low',
      estimatedTime: '2-3 hours'
    }
  ]
};

const report = ReportFactory.create('performance', performanceData);
console.log(report.render());
```

---

## 示例 6：生成版本对比报告

```javascript
const { ReportFactory } = require('./src/factories/report-factory');

const comparisonData = {
  skillName: 'meta-skill-weaver',
  versionA: 'v0.1.0',
  versionB: 'v0.2.0',
  versions: {
    a: {
      version: 'v0.1.0',
      releaseDate: '2026-03-25',
      highlights: ['基础编排功能', '任务分解'],
      status: 'stable'
    },
    b: {
      version: 'v0.2.0',
      releaseDate: '2026-03-30',
      highlights: ['Middleware 链', '并发执行', '超时控制'],
      status: 'current'
    }
  },
  differences: [
    { type: 'added', description: 'Middleware 链支持', impact: '高' },
    { type: 'added', description: '并发执行（最多 3 个）', impact: '高' },
    { type: 'added', description: '超时控制', impact: '中' },
    { type: 'changed', description: 'API 接口优化', impact: '低' }
  ],
  performance: {
    versionA: 'v0.1.0',
    versionB: 'v0.2.0',
    metrics: [
      { name: '平均执行时间', valueA: '350ms', valueB: '280ms', change: -20 },
      { name: '并发任务数', valueA: '1', valueB: '3', change: 200 },
      { name: '成功率', valueA: '92%', valueB: '94%', change: 2.2 }
    ]
  },
  dimensions: {
    versionA: 'v0.1.0',
    versionB: 'v0.2.0',
    scoresA: { T: 0.65, C: 0.60, O: 0.50, E: 0.80, M: 0.50, U: 0.55, average: 0.60 },
    scoresB: { T: 0.70, C: 0.65, O: 0.75, E: 0.85, M: 0.55, U: 0.60, average: 0.68 },
    avgA: 0.60,
    avgB: 0.68
  },
  recommendations: [
    {
      priority: 'critical',
      title: '升级到 v0.2.0',
      reason: '性能提升 20%，新增并发支持',
      benefit: '任务处理速度显著提升'
    }
  ]
};

const report = ReportFactory.create('comparison', comparisonData);
console.log(report.render());
```

---

## 示例 7：生成进化计划报告

```javascript
const { ReportFactory } = require('./src/factories/report-factory');

const evolutionData = {
  skillName: 'context-booster',
  currentVersion: 'v0.1.0',
  targetVersion: 'v0.3.0',
  currentState: {
    version: 'v0.1.0',
    scores: {
      T: 0.55, C: 0.60, O: 0.50, E: 0.40, M: 0.40, U: 0.55,
      average: 0.50
    }
  },
  targetState: {
    version: 'v0.3.0',
    targetScore: 0.75,
    goals: [
      '成为上下文管理领域的头部技能',
      '支持智能上下文压缩',
      '实现跨会话上下文共享'
    ]
  },
  gapAnalysis: {
    current: { T: 0.55, C: 0.60, O: 0.50, E: 0.40, M: 0.40, U: 0.55 },
    target: { T: 0.75, C: 0.75, O: 0.80, E: 0.70, M: 0.70, U: 0.75 }
  },
  path: [
    {
      phase: 1,
      name: '基础增强',
      actions: [
        '添加上下文优先级排序',
        '实现智能上下文过滤',
        '优化上下文存储结构'
      ],
      expectedOutcome: '六维平均达到 0.60'
    },
    {
      phase: 2,
      name: '功能扩展',
      actions: [
        '支持跨会话上下文',
        '添加上下文模板系统',
        '实现上下文版本管理'
      ],
      expectedOutcome: '六维平均达到 0.68'
    },
    {
      phase: 3,
      name: '智能化',
      actions: [
        'AI 驱动的上下文推荐',
        '自动上下文压缩',
        '上下文使用分析'
      ],
      expectedOutcome: '六维平均达到 0.75+'
    }
  ],
  timeline: {
    phases: [
      { name: 'Phase 1', startDate: '2026-04-01', endDate: '2026-04-15', milestone: 'v0.2.0 发布' },
      { name: 'Phase 2', startDate: '2026-04-16', endDate: '2026-05-01', milestone: 'v0.2.5 发布' },
      { name: 'Phase 3', startDate: '2026-05-02', endDate: '2026-05-20', milestone: 'v0.3.0 发布' }
    ]
  },
  risks: [
    {
      title: '上下文压缩算法复杂度高',
      severity: 'medium',
      probability: '40%',
      impact: '可能延迟 Phase 3',
      mitigation: '提前进行技术预研，准备简化方案'
    },
    {
      title: '跨会话上下文涉及隐私问题',
      severity: 'high',
      probability: '20%',
      impact: '可能需要重新设计',
      mitigation: '提前与用户沟通，明确隐私边界'
    }
  ]
};

const report = ReportFactory.create('evolution-plan', evolutionData);
console.log(report.render());
```

---

## 示例 8：完整工作流

```javascript
const { EventBus, SkillEvents } = require('./src/event-bus');
const { StrategySelector } = require('./src/strategies/optimization-strategies');
const { ReportFactory } = require('./src/factories/report-factory');

// 1. 创建事件总线并订阅
const eventBus = new EventBus();
const usageData = { calls: [], successes: 0, failures: 0 };

eventBus.subscribe(SkillEvents.CALLED, (data) => {
  usageData.calls.push(data);
});

eventBus.subscribe(SkillEvents.COMPLETED, () => {
  usageData.successes++;
});

eventBus.subscribe(SkillEvents.FAILED, () => {
  usageData.failures++;
});

// 2. 模拟技能调用
function simulateSkillCall(skillName, successRate = 0.9) {
  eventBus.publish(SkillEvents.CALLED, { skillName, userId: 'user1' });
  
  setTimeout(() => {
    const success = Math.random() < successRate;
    if (success) {
      eventBus.publish(SkillEvents.COMPLETED, {
        skillName,
        userId: 'user1',
        executionTime: Math.random() * 500
      });
    } else {
      eventBus.publish(SkillEvents.FAILED, {
        skillName,
        userId: 'user1',
        error: new Error('Random failure')
      });
    }
  }, 100);
}

// 运行模拟
for (let i = 0; i < 10; i++) {
  simulateSkillCall('test-skill', 0.85);
}

// 3. 等待完成后生成报告
setTimeout(() => {
  console.log('📊 使用统计:', usageData);
  
  // 4. 识别短板
  const failureRate = usageData.failures / (usageData.successes + usageData.failures);
  const shortcomings = [];
  
  if (failureRate > 0.1) {
    shortcomings.push({
      type: 'performance',
      description: `失败率过高 (${(failureRate * 100).toFixed(1)}%)`,
      complexity: 'high'
    });
  }
  
  // 5. 选择优化策略并生成计划
  if (shortcomings.length > 0) {
    const selector = new StrategySelector();
    const strategy = selector.select(shortcomings);
    const plan = strategy.generatePlan(shortcomings);
    
    console.log('\n📋 优化计划:');
    console.log(JSON.stringify(plan, null, 2));
    
    // 6. 生成进化计划报告
    const evolutionReport = ReportFactory.create('evolution-plan', {
      skillName: 'test-skill',
      currentVersion: 'v0.1.0',
      targetVersion: 'v0.2.0',
      currentState: {
        version: 'v0.1.0',
        scores: { T: 0.6, C: 0.6, O: 0.5, E: 0.5, M: 0.5, U: 0.6, average: 0.55 }
      },
      targetState: {
        version: 'v0.2.0',
        targetScore: 0.70,
        goals: ['降低失败率至 5% 以下']
      },
      gapAnalysis: {
        current: { T: 0.6, C: 0.6, O: 0.5, E: 0.5, M: 0.5, U: 0.6 },
        target: { T: 0.7, C: 0.7, O: 0.7, E: 0.7, M: 0.7, U: 0.7 }
      },
      path: [{
        phase: 1,
        name: '稳定性提升',
        actions: plan.actions.map(a => a.action + ': ' + a.target),
        expectedOutcome: '失败率降低至 5%'
      }],
      timeline: {
        phases: [{
          name: 'Phase 1',
          startDate: '2026-04-01',
          endDate: '2026-04-07',
          milestone: 'v0.2.0 发布'
        }]
      },
      risks: []
    });
    
    console.log('\n' + evolutionReport.render());
  }
}, 1000);
```

---

## 运行示例

```bash
# 运行示例 1
node examples/usage-examples.md

# 或者复制代码到 test.js 运行
node test.js
```

---

**维护者**：王的奴隶 · 严谨专业版  
**最后更新**：2026-03-30
