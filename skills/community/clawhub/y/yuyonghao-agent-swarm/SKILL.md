# Agent Swarm - 群体智能核心

Agent 群体智能核心系统，实现真正的群体智能能力，包括群体协调、任务分片、自组织和涌现行为。

## 功能特性

### 1. 群体协调 (SwarmCoordinator)
- 群体生命周期管理
- 成员发现与注册
- 通信协议
- 共识机制

### 2. 任务分片 (TaskSharder)
- 任务分解
- 负载均衡
- 依赖管理
- 结果合并

### 3. 自组织 (SelfOrganizer)
- 角色分配
- 动态重组
- 故障转移
- 自适应调整

### 4. 涌现行为 (EmergentBehavior)
- 集体决策
- 模式识别
- 群体学习
- 智能涌现

### 5. Swarm 监控 (SwarmMonitor)
- 群体状态监控
- 性能指标
- 异常检测
- 可视化

## 安装

```bash
npm install
```

## 使用示例

```javascript
const { SwarmCoordinator, TaskSharder, SelfOrganizer, SwarmMonitor } = require('./src');

// 创建群体协调器
const swarm = new SwarmCoordinator({
  maxAgents: 100,
  consensusThreshold: 0.7,
  communicationProtocol: 'broadcast'
});

// 创建群体
const swarmId = swarm.createSwarm({
  name: 'code-generation-swarm',
  specialization: 'code'
});

// 添加 Agent
swarm.addAgent(swarmId, {
  id: 'agent-1',
  capabilities: ['javascript', 'python'],
  capacity: 5
});

// 执行任务
const result = await swarm.executeTask(swarmId, {
  type: 'generate-code',
  input: 'Create a web server',
  shardStrategy: 'parallel'
});
```

## API 文档

### SwarmCoordinator

#### Constructor Options
- `maxAgents` (number): 最大 Agent 数量
- `consensusThreshold` (number): 共识阈值 (0-1)
- `communicationProtocol` (string): 通信协议 ('broadcast' | 'gossip' | 'direct')

#### Methods
- `createSwarm(config)` - 创建新群体
- `destroySwarm(swarmId)` - 销毁群体
- `addAgent(swarmId, agent)` - 添加 Agent
- `removeAgent(swarmId, agentId)` - 移除 Agent
- `executeTask(swarmId, task)` - 执行任务
- `reachConsensus(swarmId, proposal)` - 达成共识

### TaskSharder

#### Methods
- `shard(taskConfig)` - 分解任务
- `assign(shards, agents)` - 分配分片
- `merge(results)` - 合并结果
- `getDependencies(shardId)` - 获取依赖

### SelfOrganizer

#### Methods
- `assignRoles(agents, config)` - 分配角色
- `adapt(swarm, config)` - 自适应调整
- `reorganize(swarmId)` - 重新组织
- `handleFailure(swarmId, agentId)` - 处理故障

### EmergentBehavior

#### Methods
- `collectiveDecision(swarm, options)` - 集体决策
- `recognizePattern(data)` - 模式识别
- `learnFromExperience(experience)` - 群体学习
- `detectEmergence(swarm)` - 检测涌现

### SwarmMonitor

#### Methods
- `getMetrics(swarmId)` - 获取指标
- `detectAnomalies(swarmId)` - 异常检测
- `getVisualization(swarmId)` - 获取可视化数据
- `exportReport(swarmId)` - 导出报告

## 测试

```bash
npm test
```

## License

MIT
