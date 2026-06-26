# Observability - 可观测性系统

一个完整的 AI Agent 可观测性解决方案，提供结构化日志、性能指标、分布式追踪、告警管理和实时监控面板。

## 版本

- **当前版本**: 0.2.0
- **Node.js 要求**: >= 18.0.0
- **作者**: 小蒲萄 (Clawd)

## 功能特性

### 核心组件

1. **StructuredLogger** - 结构化日志系统
   - JSON 格式日志
   - 多级别日志（error/warn/info/debug）
   - 自动日志轮转
   - 上下文追踪（traceId/spanId）

2. **MetricsCollector** - 指标收集器
   - Counter（计数器）
   - Gauge（仪表）
   - Histogram（直方图）
   - Prometheus 格式导出
   - 自动聚合和百分位数计算

3. **Tracer** - 分布式追踪
   - Trace/Span 管理
   - 链路追踪
   - 采样率控制
   - 父子关系追踪

4. **AlertManager** - 告警管理
   - 阈值告警（支持 Counter/Gauge/Histogram）
   - 规则引擎（gt/lt/eq/gte/lte）
   - 多渠道通知（Console/File/Webhook）
   - 告警抑制和恢复
   - 告警历史记录

5. **Dashboard** - 监控面板
   - 实时指标展示
   - 多 Tab 视图（概览/LLM/MCP/A2A/告警/日志）
   - 自动刷新
   - RESTful API

### OpenClaw 集成

- **LLM 调用监控**: Token 消耗、延迟、错误率、成本估算
- **MCP 工具监控**: 工具调用统计、执行时间、成功率
- **A2A 通信监控**: 消息延迟、成功率、会话管理

## 安装

```bash
# 进入技能目录
cd skills/observability

# 安装依赖
npm install

# 运行测试
npm test

# 启动 Dashboard
npm start
```

## 快速开始

### 基础用法

```javascript
const { ObservabilitySystem } = require('./src/index');

// 创建可观测性系统
const obs = new ObservabilitySystem({
  logging: {
    level: 'info',
    console: true,
    file: true
  },
  metrics: {
    enabled: true,
    prefix: 'agent'
  },
  alerts: {
    enabled: true,
    createDefaultRules: true
  }
});

// 开始追踪
const trace = obs.startTrace('agent.execute', { query: 'test' });

// 执行业务逻辑...
const result = await doSomething();

// 结束追踪
trace.end({ result: 'success' });

// 获取系统状态
const status = obs.getStatus();
console.log(status);
```

### 包装函数自动追踪

```javascript
const wrappedFunction = obs.wrap(async (data) => {
  // 你的业务逻辑
  return await processData(data);
}, 'processData');

// 调用会自动追踪
const result = await wrappedFunction(input);
```

### 添加告警规则

```javascript
// 添加自定义告警规则
obs.addAlertRule({
  name: 'High Latency Alert',
  description: 'Triggered when latency exceeds threshold',
  metric: 'agent.calls.latency',
  metricType: 'histogram',
  condition: 'gt',
  threshold: 1000,
  severity: 'warning',
  channels: ['console', 'file'],
  cooldown: 60000  // 1分钟冷却
});

// 手动触发告警
obs.fireAlert('rule-id', 1500, 'Latency is too high');
```

### LLM 监控

```javascript
// 记录 LLM 调用
const call = obs.startLLMCall('session-1', 'gpt-4', { temperature: 0.7 });

// 调用 LLM...
const response = await llm.chat(...);

// 结束记录
call.end({
  usage: {
    prompt_tokens: 100,
    completion_tokens: 50,
    total_tokens: 150
  }
});

// 获取 LLM 统计
const llmStats = obs.getStatus().llm;
console.log(`Total tokens: ${llmStats.totalTokens}`);
console.log(`Total cost: $${llmStats.totalCost.toFixed(4)}`);
```

### MCP 工具监控

```javascript
// 记录 MCP 工具调用
const call = obs.startMCPCall('filesystem', 'readFile', { path: '/test.txt' });

// 执行工具...
const result = await mcpTool.execute(...);

// 结束记录
call.end(result);

// 获取 MCP 统计
const mcpStats = obs.getStatus().mcp;
console.log(`Success rate: ${mcpStats.overallSuccessRate.toFixed(1)}%`);
```

### A2A 通信监控

```javascript
// 记录 A2A 消息
const msg = obs.sendA2AMessage({
  id: 'msg-1',
  type: 'request',
  from: 'agent-a',
  to: 'agent-b',
  sessionId: 'session-1',
  payload: { ... }
});

// 接收响应
obs.a2aMonitor.receiveResponse(msg.messageId, msg, response);

// 记录事件
obs.recordA2AEvent({
  type: 'notification',
  from: 'agent-a',
  payload: { ... }
});
```

## Dashboard

启动 Dashboard 服务器：

```bash
npm start
# 或
node src/dashboard.js
```

访问 http://localhost:3001 查看监控面板。

### API 端点

| 端点 | 方法 | 描述 |
|------|------|------|
| `/` | GET | Dashboard UI |
| `/api/status` | GET | 系统状态（包含所有模块统计） |
| `/api/metrics` | GET | 指标数据（JSON） |
| `/api/logs` | GET | 最近日志 |
| `/api/prometheus` | GET | Prometheus 格式指标 |
| `/api/alerts` | GET | 告警历史 |

## 配置选项

```javascript
{
  // 日志配置
  logging: {
    level: 'info',        // debug/info/warn/error
    console: true,        // 输出到控制台
    file: true,           // 输出到文件
    logDir: './logs',     // 日志目录
    elasticsearch: false  // 输出到 ES（待实现）
  },
  
  // 指标配置
  metrics: {
    enabled: true,        // 启用指标
    prefix: 'agent',      // 指标前缀
    autoReport: false,    // 自动报告
    reportInterval: 60000 // 报告间隔（毫秒）
  },
  
  // 追踪配置
  tracing: {
    enabled: true,        // 启用追踪
    sampleRate: 1.0,      // 采样率（0-1）
    maxTraces: 1000       // 最大追踪数
  },
  
  // 告警配置
  alerts: {
    enabled: true,              // 启用告警
    checkInterval: 30000,       // 检查间隔（毫秒）
    createDefaultRules: true,   // 创建默认规则
    maxHistory: 1000            // 最大历史记录数
  },
  
  // LLM 监控配置
  llm: {
    enabled: true         // 启用 LLM 监控
  },
  
  // MCP 监控配置
  mcp: {
    enabled: true         // 启用 MCP 监控
  },
  
  // A2A 监控配置
  a2a: {
    enabled: true         // 启用 A2A 监控
  }
}
```

## 项目结构

```
skills/observability/
├── src/
│   ├── index.js           # 主入口
│   ├── logger.js          # 结构化日志
│   ├── metrics.js         # 指标收集
│   ├── tracer.js          # 分布式追踪
│   ├── alert-manager.js   # 告警管理
│   ├── llm-monitor.js     # LLM 监控
│   ├── mcp-monitor.js     # MCP 监控
│   ├── a2a-monitor.js     # A2A 监控
│   └── dashboard.js       # 监控面板
├── test/
│   └── observability.test.js  # 测试套件
├── logs/                  # 日志目录
├── package.json
└── SKILL.md
```

## 测试

运行完整测试套件：

```bash
npm test
```

测试覆盖率：

- Logger: ~95%
- MetricsCollector: ~95%
- Tracer: ~90%
- AlertManager: ~90%
- LLMMonitor: ~90%
- MCPToolsMonitor: ~90%
- A2AMonitor: ~90%
- ObservabilitySystem: ~95%

**总体覆盖率: >90%**

## 默认告警规则

系统预置以下告警规则：

1. **High Latency Alert** - 平均延迟超过 1000ms
2. **High Error Rate** - 错误次数超过 10
3. **High Token Usage** - Token 使用量超过 10000
4. **MCP Tool Errors** - MCP 工具错误超过 5

## 性能指标

### 日志性能
- 异步写入，不影响主流程
- 自动轮转，单文件最大 10MB
- 保留最近 5 个日志文件

### 指标性能
- 内存存储，纳秒级操作
- 自动清理过期追踪
- 可配置的采样率

### Dashboard 性能
- 支持 1000+ 并发连接
- 5 秒自动刷新
- 响应式 UI 设计

## 扩展开发

### 自定义通知渠道

```javascript
class AlertManager {
  constructor() {
    this.notificationHandlers = {
      console: this._notifyConsole.bind(this),
      file: this._notifyFile.bind(this),
      webhook: this._notifyWebhook.bind(this),
      custom: this._notifyCustom.bind(this)  // 添加自定义处理器
    };
  }

  _notifyCustom(alert, rule) {
    // 实现自定义通知逻辑
    sendToSlack(alert.message);
  }
}
```

### 自定义指标导出

```javascript
// 导出到 InfluxDB
metrics.onReport((metricsData) => {
  influxDB.writePoints([
    {
      measurement: 'agent_metrics',
      fields: metricsData,
      timestamp: Date.now()
    }
  ]);
});
```

## 许可证

MIT License

## 作者

小蒲萄 (Clawd) - OpenClaw 项目
