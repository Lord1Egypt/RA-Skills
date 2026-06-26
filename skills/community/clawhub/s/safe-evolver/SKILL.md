---
name: safe-evolver
description: "A safe AI agent evolution engine that analyzes runtime history to identify improvements and applies protocol-constrained evolution with comprehensive safety checks and audit logs."
version: 1.1.0
---

# Safe Evolver

## 📖 功能描述

Safe Evolver 是一个安全的 AI 代理自我进化引擎，通过分析运行时历史来识别改进机会，并应用受控的协议约束进化。

**核心价值**：帮助 AI 代理从执行历史中学习，持续优化行为模式，同时确保进化过程的安全可控。

---

## ✨ 核心功能

### 1. **历史分析** 📊
- 记录工具调用、响应、错误等信息
- 分析行为模式和效率指标
- 识别优化机会

### 2. **改进识别** 🔍
- 自动检测低效操作
- 识别常见错误模式
- 建议行为改进

### 3. **安全进化** 🔄
- 应用协议约束的进化机制
- 确保所有改进都经过安全检查
- 提供透明的进化过程

### 4. **风险控制** ⚠️
- 防止有害的进化路径
- 审计所有改进建议
- 支持人类审核

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装
clawhub install safe-evolver

# 或本地安装
npm install safe-evolver
```

### 基本使用

```javascript
const SafeEvolver = require('safe-evolver');
const evolver = new SafeEvolver({
  mode: 'auto',  // 'auto' | 'manual' | 'disabled'
  logPath: './logs/evolution.log'
});

// 记录一次交互
evolver.recordInteraction({
  toolCalls: 6,
  responses: 4,
  errors: 0,
  efficiency: 0.85
});

// 获取进化报告
const report = evolver.getReport();
console.log(report);
```

---

## 📚 详细使用方法

### 1. 初始化配置

#### 基础配置
```javascript
const evolver = new SafeEvolver({
  // 进化模式
  mode: 'auto',  // 'auto' | 'manual' | 'disabled'

  // 日志路径
  logPath: './logs/evolution.log',

  // 是否启用审计
  enableAudit: true,

  // 进化频率（记录多少次后建议改进）
  evolutionFrequency: 10,

  // 安全级别
  safetyLevel: 'high'  // 'low' | 'medium' | 'high'
});
```

#### 高级配置
```javascript
const evolver = new SafeEvolver({
  mode: 'manual',

  // LLM 配置（用于智能分析）
  llm: {
    enabled: true,
    model: 'qwen2.5:3b',
    apiKey: 'your-api-key'
  },

  // 分析维度
  analysis: {
    efficiency: true,      // 效率分析
    errorPatterns: true,   // 错误模式
    resourceUsage: true,   // 资源使用
    responseQuality: true, // 响应质量
    toolOptimization: true // 工具使用优化
  },

  // 改进建议阈值
  thresholds: {
    minImprovement: 0.05,  // 最小改进率
    maxSuggestions: 10     // 最多建议数量
  },

  // 审计配置
  audit: {
    includeAllData: true,
    exportFormat: 'json'
  }
});
```

### 2. 记录交互

#### 基础交互记录
```javascript
// 单次交互
evolver.recordInteraction({
  toolCalls: 6,
  responses: 4,
  errors: 0,
  efficiency: 0.85,
  duration: 23.5
});

// 详细交互记录
evolver.recordInteraction({
  interactionId: 'sess-123',  // 交互ID
  startTime: '2026-04-06T10:00:00Z',
  endTime: '2026-04-06T10:00:23Z',

  // 工具调用
  toolCalls: [
    {
      tool: 'exec',
      command: 'ls -la',
      success: true,
      duration: 0.1
    },
    {
      tool: 'read',
      path: '/etc/passwd',
      success: true,
      duration: 0.05
    }
  ],

  // 响应
  responses: [
    {
      content: '这是执行结果...',
      quality: 0.8
    }
  ],

  // 错误
  errors: [],

  // 资源使用
  resources: {
    memory: 120,  // MB
    cpu: 15,      // %
    disk: 0       // MB
  },

  // 效率评分
  efficiency: 0.85,

  // 上下文
  context: {
    task: '列出用户目录内容',
    sessionType: 'general'
  }
});
```

### 3. 获取进化报告

#### 基础报告
```javascript
const report = evolver.getReport();

console.log(report);

// 输出示例:
/*
{
  interactionCount: 50,
  avgEfficiency: 0.78,
  totalErrors: 3,
  lastReport: '2026-04-06T22:00:00Z',

  improvements: [
    {
      category: '效率',
      issue: '工具调用过多',
      suggestion: '减少不必要的 ls 命令',
      priority: 'high',
      estimatedImpact: 0.15
    }
  ],

  warnings: [
    {
      category: '资源',
      issue: '内存使用偏高',
      current: 120,
      threshold: 100,
      advice: '考虑使用轻量级工具'
    }
  ],

  safetyScore: 0.95
}
*/
```

#### 详细报告
```javascript
const detailedReport = evolver.getDetailedReport();

console.log(detailedReport);

// 输出示例:
/*
{
  summary: { ... },

  efficiencyAnalysis: {
    score: 0.78,
    breakdown: [
      { metric: '工具效率', score: 0.75 },
      { metric: '响应效率', score: 0.82 },
      { metric: '错误恢复', score: 0.90 }
    ],
    opportunities: [
      '可以合并多个 ls 命令',
      '减少重复的文件读取'
    ]
  },

  errorAnalysis: {
    totalErrors: 3,
    errorTypes: {
      'Permission Denied': 2,
      'File Not Found': 1
    },
    recommendations: [
      '添加文件存在检查',
      '使用更安全的权限模式'
    ]
  },

  resourceAnalysis: {
    memoryUsage: {
      avg: 120,
      peak: 150,
      trend: 'stable'
    },
    cpuUsage: {
      avg: 15,
      peak: 25,
      pattern: 'sporadic'
    }
  },

  suggestions: [
    {
      id: 1,
      category: '效率',
      title: '减少重复的文件读取',
      description: '检测到多次读取同一个文件，建议缓存或批量读取',
      priority: 'medium',
      implementation: '需要修改代码',
      estimatedBenefit: 0.10
    }
  ]
}
*/
```

### 4. 手动触发分析

#### 主动分析
```javascript
// 触发深度分析
evolver.analyze(
  {
    efficiency: true,
    errorPatterns: true,
    toolOptimization: true
  },
  (report) => {
    console.log('分析完成:', report);
  }
);

// 获取特定维度的报告
const efficiencyReport = evolver.getEfficiencyReport();
const errorReport = evolver.getErrorReport();
const resourceReport = evolver.getResourceReport();
```

### 5. 应用于改进

#### 获取改进建议
```javascript
const suggestions = evolver.getSuggestions({
  category: 'efficiency',  // 可选: 'efficiency' | 'errors' | 'all'
  limit: 5,
  priority: 'high'        // 可选: 'low' | 'medium' | 'high' | 'all'
});

console.log(suggestions);

// 输出示例:
/*
[
  {
    id: 'eff-001',
    category: '效率',
    title: '减少工具调用数量',
    description: '当前每次任务平均调用 6 次工具，建议优化到 4 次',
    priority: 'high',
    estimatedImpact: 0.20,
    actions: [
      '合并多个 ls 命令',
      '批量读取文件内容'
    ]
  }
]
*/
```

#### 应用改进
```javascript
// 应用单个建议
evolver.applyImprovement('eff-001', {
  tool: 'exec',
  command: 'ls -la /tmp/*',
  comment: '合并多个 ls 命令'
});

// 应用多个建议
const improvements = evolver.getImprovementsReadyToApply();
improvements.forEach(improvement => {
  evolver.applyImprovement(improvement.id);
});
```

---

## 🎯 使用场景

### 场景 1: AI 代理性能优化

```javascript
const evolver = new SafeEvolver({
  mode: 'auto',
  safetyLevel: 'high'
});

// 在交互循环中使用
async function runAgent(task) {
  let interactionCount = 0;

  while (true) {
    // 记录当前状态
    const metrics = {
      toolCalls: currentToolCalls,
      responses: currentResponses,
      errors: currentErrors,
      efficiency: calculateEfficiency()
    };

    // 记录交互
    evolver.recordInteraction(metrics);
    interactionCount++;

    // 检查是否需要建议
    if (interactionCount % evolver.config.evolutionFrequency === 0) {
      const report = evolver.getReport();
      if (report.needsImprovement) {
        const suggestions = evolver.getSuggestions();

        // 显示给用户或自动应用
        console.log('改进建议:', suggestions);

        // 应用最佳建议
        const best = suggestions.find(s => s.priority === 'high');
        if (best) {
          applySuggestion(best);
        }
      }
    }

    // 执行任务...
  }
}
```

### 场景 2: 错误模式分析

```javascript
const evolver = new SafeEvolver({
  mode: 'manual',
  analysis: {
    errorPatterns: true
  }
});

// 记录交互
evolver.recordInteraction({
  errors: [
    { type: 'FileNotFound', path: '/etc/config' },
    { type: 'PermissionDenied', path: '/root/.ssh' }
  ]
});

// 获取错误报告
const errorReport = evolver.getErrorReport();

console.log('常见错误:', errorReport.commonErrors);
console.log('错误模式:', errorReport.patterns);
console.log('建议:', errorReport.suggestions);

// 根据建议改进代码
if (errorReport.patterns.includes('FileNotFound')) {
  addFileExistCheck();
}
```

### 场景 3: 资源使用优化

```javascript
const evolver = new SafeEvolver({
  mode: 'manual',
  analysis: {
    resourceUsage: true
  }
});

// 监控资源使用
setInterval(() => {
  const metrics = {
    resources: {
      memory: getMemoryUsage(),
      cpu: getCPUUsage(),
      disk: getDiskUsage()
    }
  };

  evolver.recordInteraction(metrics);

  const resourceReport = evolver.getResourceReport();

  // 如果资源使用超过阈值，给出建议
  if (resourceReport.issues.some(i => i.severity === 'high')) {
    console.warn('资源警告:', resourceReport.issues);
  }
}, 60000); // 每分钟记录一次
```

---

## ⚙️ 配置文件

Safe Evolver 支持通过配置文件初始化。

### 配置文件格式 (config.json)

```json
{
  "mode": "auto",
  "safetyLevel": "high",
  "logPath": "./logs/evolution.log",

  "llm": {
    "enabled": true,
    "model": "qwen2.5:3b"
  },

  "analysis": {
    "efficiency": true,
    "errorPatterns": true,
    "resourceUsage": true,
    "responseQuality": true,
    "toolOptimization": true
  },

  "thresholds": {
    "minImprovement": 0.05,
    "maxSuggestions": 10
  },

  "audit": {
    "enabled": true,
    "exportFormat": "json"
  }
}
```

### 使用配置文件

```javascript
const evolver = new SafeEvolver('./config.json');
```

---

## 🔒 安全特性

| 特性 | 说明 |
|------|------|
| **安全进化** | 所有改进都经过安全检查 |
| **审计追踪** | 完整的进化历史记录 |
| **手动审核** | 支持人类审核改进建议 |
| **风险控制** | 防止有害的进化路径 |
| **透明可追溯** | 所有建议都可审查 |

---

## 📊 效率评分

Evolver 会计算**效率评分**（0-1）：

```
效率评分 = (工具效率 × 0.4) + (响应效率 × 0.3) + (错误恢复 × 0.3)
```

**评分等级**：
- ✅ **优秀** (0.85-1.0): 表现卓越
- ✅ **良好** (0.7-0.84): 表现良好
- ⚠️ **一般** (0.5-0.69): 需要改进
- ❌ **较差** (0-0.49): 需要大幅改进

---

## 🛠️ 开发与测试

### 运行测试

```bash
# 安装依赖
npm install

# 运行测试
npm test
```

### 测试示例

```javascript
// test.js
const evolver = new SafeEvolver();

// 模拟交互
evolver.recordInteraction({
  toolCalls: 5,
  responses: 3,
  errors: 0,
  efficiency: 0.8
});

evolver.recordInteraction({
  toolCalls: 7,
  responses: 4,
  errors: 1,
  efficiency: 0.6
});

// 获取报告
const report = evolver.getReport();
console.log('效率评分:', report.avgEfficiency);
console.log('改进建议:', report.improvements);

// 获取建议
const suggestions = evolver.getSuggestions();
console.log('建议数量:', suggestions.length);
```

---

## 📝 API 参考

### 构造函数
```javascript
new SafeEvolver(config?)
```

**参数**:
- `config` (Object): 配置对象

### 方法

| 方法 | 返回 | 说明 |
|------|------|------|
| `recordInteraction(data)` | void | 记录交互数据 |
| `getReport()` | Object | 获取进化报告 |
| `getDetailedReport()` | Object | 获取详细报告 |
| `getSuggestions(options?)` | Array | 获取改进建议 |
| `applyImprovement(id, data?)` | void | 应用改进 |
| `getEfficiencyReport()` | Object | 获取效率报告 |
| `getErrorReport()` | Object | 获取错误报告 |
| `getResourceReport()` | Object | 获取资源报告 |
| `analyze(config?, callback?)` | void | 触发分析 |
| `exportReport(path?)` | void | 导出报告 |

### recordInteraction 参数

```typescript
{
  interactionId?: string,
  startTime?: string,
  endTime?: string,
  toolCalls?: Array<{...}>,
  responses?: Array<{...}>,
  errors?: Array<{...}>,
  resources?: {...},
  efficiency?: number,
  context?: {...}
}
```

---

## 📖 使用示例

### 完整示例：智能优化系统

```javascript
const SafeEvolver = require('safe-evolver');

// 初始化
const evolver = new SafeEvolver({
  mode: 'auto',
  safetyLevel: 'high',
  evolutionFrequency: 10
});

// 优化监控循环
function monitorOptimization() {
  setInterval(() => {
    const report = evolver.getReport();

    if (report.needsImprovement) {
      const suggestions = evolver.getSuggestions({ limit: 3 });

      console.log('\n🔍 进化分析:');
      suggestions.forEach((s, i) => {
        console.log(`${i + 1}. [${s.category}] ${s.title}`);
        console.log(`   建议效果: +${s.estimatedImpact}`);
      });

      // 应用高优先级建议
      const highPriority = suggestions.filter(s => s.priority === 'high');
      highPriority.forEach(s => {
        console.log(`\n✅ 应用改进: ${s.title}`);
        applySuggestion(s);
      });
    }
  }, 300000); // 每5分钟分析一次
}

// 应用建议函数
function applySuggestion(suggestion) {
  switch (suggestion.category) {
    case '效率':
      optimizeToolCalls(suggestion);
      break;
    case '错误':
      improveErrorHandling(suggestion);
      break;
    case '资源':
      optimizeResourceUsage(suggestion);
      break;
  }
}

function optimizeToolCalls(suggestion) {
  // 实现工具调用优化逻辑
  console.log('优化工具调用策略...');
}

function improveErrorHandling(suggestion) {
  // 实现错误处理改进逻辑
  console.log('改进错误处理机制...');
}

function optimizeResourceUsage(suggestion) {
  // 实现资源使用优化逻辑
  console.log('优化资源使用...');
}

// 启动监控
monitorOptimization();
```

---

## 🐛 常见问题

### Q1: 什么时候触发进化分析？

**A**:
- **auto 模式**: 每 N 次交互后自动分析（可配置）
- **manual 模式**: 手动调用 `analyze()` 方法
- **disabled 模式**: 不自动分析

### Q2: 改进建议如何应用到实际代码？

**A**:
1. 获取建议：`evolver.getSuggestions()`
2. 审查建议内容
3. 根据建议修改代码
4. 记录应用结果
5. Evolver 会学习这些改进

### Q3: 如何禁用某个分析维度？

**A**:
```javascript
const evolver = new SafeEvolver({
  analysis: {
    efficiency: false,    // 禁用效率分析
    errorPatterns: true,  // 启用错误分析
    resourceUsage: false  // 禁用资源分析
  }
});
```

### Q4: 进化报告存储在哪里？

**A**:
- 内存中：`evolver.getReport()`
- 日志文件：`evolver.config.logPath`
- 可导出：`evolver.exportReport('./report.json')`

---

## 📄 许可证

MIT-0 License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📞 联系方式

- Issue: https://github.com/your-repo/safe-evolver/issues
- 文档: https://docs.your-repo.com/safe-evolver

---

## 🎉 更新日志

### v1.1.0 (2026-04-06)
- ✨ 添加详细的中文文档和使用示例
- ✨ 改进报告生成算法
- ✨ 支持更多分析维度
- ✨ 优化建议的优先级算法
- 🐛 修复某些边缘情况

### v1.0.0 (2026-04-05)
- 🎉 初始版本发布
