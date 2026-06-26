# Agent Orchestrator

生产级 Agent 编排器，类似 Kubernetes 的 Agent 调度系统。

## 功能特性

### 1. Agent 生命周期管理
- Agent 注册/注销
- 健康检查 (Heartbeat)
- 自动故障恢复
- 优雅启停

### 2. 任务调度器
- 任务队列管理
- 负载均衡策略 (Round Robin / Least Connections / 自定义)
- 优先级调度 (low/normal/high/critical)
- 任务超时/重试

### 3. 资源管理
- CPU/内存限制
- 并发控制
- 资源配额
- 资源监控

### 4. 服务发现
- Agent 能力注册
- 动态发现
- 负载感知路由

### 5. 集群管理
- 多节点支持
- Leader 选举
- 状态同步
- 配置管理

## 安装

```bash
npm install
```

## 使用方法

### 基础用法

```javascript
const { AgentOrchestrator } = require('./src');

// 创建编排器实例
const orchestrator = new AgentOrchestrator({
  cluster: { enabled: true, nodeId: 'node-1' },
  scheduler: { strategy: 'round-robin' },
  resources: { maxAgents: 100, maxTasksPerAgent: 10 }
});

// 注册 Agent
orchestrator.registerAgent({
  id: 'agent-1',
  capabilities: ['text-generation', 'code-execution'],
  resources: { maxConcurrent: 5 }
});

// 提交任务
const task = await orchestrator.submitTask({
  type: 'code-generation',
  priority: 'high',
  payload: { prompt: 'Generate a function...' }
});

// 获取集群状态
const status = orchestrator.getClusterStatus();
console.log(status);
```

### 调度策略

```javascript
// Round Robin
const orchestrator = new AgentOrchestrator({
  scheduler: { strategy: 'round-robin' }
});

// Least Connections
const orchestrator = new AgentOrchestrator({
  scheduler: { strategy: 'least-connections' }
});

// Weighted Round Robin
const orchestrator = new AgentOrchestrator({
  scheduler: { strategy: 'weighted-round-robin', weights: { 'agent-1': 2, 'agent-2': 1 } }
});
```

### 健康检查

```javascript
// 配置健康检查
const orchestrator = new AgentOrchestrator({
  healthCheck: {
    enabled: true,
    interval: 30000,  // 30 seconds
    timeout: 5000,    // 5 seconds
    retries: 3
  }
});

// 手动检查 Agent 健康
const isHealthy = await orchestrator.healthChecker.check('agent-1');
```

### 资源管理

```javascript
// 配置资源限制
const orchestrator = new AgentOrchestrator({
  resources: {
    maxAgents: 100,
    maxTasksPerAgent: 10,
    maxMemoryPerAgent: '512MB',
    maxCpuPerAgent: '1.0'
  }
});

// 获取资源使用
const usage = orchestrator.resourceManager.getUsage();
```

## API 参考

### AgentOrchestrator

#### Constructor
```javascript
new AgentOrchestrator(options)
```

Options:
- `cluster`: 集群配置
- `scheduler`: 调度器配置
- `resources`: 资源限制
- `healthCheck`: 健康检查配置

#### Methods
- `registerAgent(agent)`: 注册 Agent
- `unregisterAgent(agentId)`: 注销 Agent
- `submitTask(task)`: 提交任务
- `cancelTask(taskId)`: 取消任务
- `getClusterStatus()`: 获取集群状态
- `getAgentStatus(agentId)`: 获取 Agent 状态

## 测试

```bash
npm test
```

## 配置选项

```javascript
{
  cluster: {
    enabled: true,
    nodeId: 'node-1',
    leaderElection: true
  },
  scheduler: {
    strategy: 'round-robin', // or 'least-connections', 'weighted-round-robin'
    priorityLevels: ['low', 'normal', 'high', 'critical']
  },
  resources: {
    maxAgents: 100,
    maxTasksPerAgent: 10,
    maxMemoryPerAgent: '512MB',
    maxCpuPerAgent: '1.0'
  },
  healthCheck: {
    enabled: true,
    interval: 30000,
    timeout: 5000,
    retries: 3
  }
}
```

## License

MIT
