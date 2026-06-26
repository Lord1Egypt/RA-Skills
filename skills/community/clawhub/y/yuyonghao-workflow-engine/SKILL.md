# Workflow Engine - OpenClaw 工作流编排引擎

**版本**: 0.1.0  
**功能**: DAG 执行器 + 条件分支 + 并行执行

## 功能特性

- **DAG 编排**: 有向无环图工作流定义
- **顺序执行**: 简单的线性任务链
- **条件分支**: 支持 if/else 条件判断
- **并行执行**: 支持并行任务执行
- **状态持久化**: 检查点机制支持断点续执行
- **事件驱动**: 完整的事件系统

## 安装

```bash
cd skills/workflow-engine
npm install
```

## 快速开始

```javascript
import { WorkflowEngine } from './src/workflow-engine.js';

// 创建工作流引擎
const engine = new WorkflowEngine({
  checkpointDir: './checkpoints',
  enableCheckpoint: true,
  maxConcurrency: 10
});

// 创建顺序工作流
const dag = engine.createSequentialWorkflow('My Workflow', [
  {
    name: 'Step 1',
    execute: async (context) => {
      console.log('Executing step 1');
      context.data = { value: 42 };
      return { success: true };
    }
  },
  {
    name: 'Step 2',
    execute: async (context) => {
      console.log('Executing step 2');
      console.log('Data from step 1:', context.data);
      return { success: true };
    }
  }
]);

// 执行工作流
const result = await engine.execute(dag.id, {});
console.log('Workflow completed:', result.status);
```

## API 参考

### WorkflowEngine

#### 构造函数
```javascript
new WorkflowEngine(config)
```

**参数**:
- `config.checkpointDir` - 检查点目录（默认：'./checkpoints'）
- `config.enableCheckpoint` - 启用检查点（默认：true）
- `config.maxConcurrency` - 最大并发数（默认：10）

#### createSequentialWorkflow(name, tasks)
创建顺序工作流

```javascript
const dag = engine.createSequentialWorkflow('Test', [
  { name: 'Task 1', execute: async () => {} },
  { name: 'Task 2', execute: async () => {} }
]);
```

#### execute(workflowId, context)
执行工作流

```javascript
const result = await engine.execute('workflow-id', {
  input: 'data'
});
// 返回: { executionId, status, context, results, duration }
```

### WorkflowDAG

#### addNode(config)
添加节点

```javascript
dag.addNode({
  id: 'task1',
  type: 'task', // 'task' | 'condition' | 'parallel' | 'start' | 'end'
  name: 'Task 1',
  execute: async (context) => { return { result: 'done' }; },
  retry: { count: 3, delay: 1000 },
  timeout: 30000
});
```

#### addEdge(fromId, toId)
添加边（依赖关系）

```javascript
dag.addEdge('start', 'task1');
dag.addEdge('task1', 'task2');
```

#### topologicalSort()
拓扑排序

```javascript
const order = dag.topologicalSort();
// 返回: ['start', 'task1', 'task2', 'end']
```

### WorkflowNode

#### 节点类型
- `start` - 开始节点
- `end` - 结束节点
- `task` - 任务节点
- `condition` - 条件节点
- `parallel` - 并行节点

#### 节点配置
```javascript
{
  id: 'unique-id',
  type: 'task',
  name: 'Task Name',
  description: 'Task description',
  execute: async (context) => { /* 执行逻辑 */ },
  retry: { count: 3, delay: 1000 },
  timeout: 30000,
  metadata: {}
}
```

## 示例

### 条件分支
```javascript
import WorkflowDAG, { WorkflowNode } from './src/dag.js';

const dag = new WorkflowDAG({ name: 'Conditional' });

dag.addNode({ id: 'start', type: 'start' });
dag.addNode({
  id: 'check',
  type: 'condition',
  condition: (ctx) => ctx.value > 10,
  branches: { 'true': 'high', 'false': 'low' }
});
dag.addNode({
  id: 'high',
  type: 'task',
  execute: async () => console.log('High value')
});
dag.addNode({
  id: 'low',
  type: 'task',
  execute: async () => console.log('Low value')
});

dag.addEdge('start', 'check');
dag.addEdge('check', 'high');
dag.addEdge('check', 'low');
```

### 并行执行
```javascript
dag.addNode({ id: 'start', type: 'start' });
dag.addNode({
  id: 'parallel',
  type: 'parallel',
  parallelTasks: ['taskA', 'taskB', 'taskC']
});
dag.addNode({ id: 'taskA', type: 'task', execute: async () => {} });
dag.addNode({ id: 'taskB', type: 'task', execute: async () => {} });
dag.addNode({ id: 'taskC', type: 'task', execute: async () => {} });
dag.addNode({ id: 'merge', type: 'task', execute: async () => {} });

dag.addEdge('start', 'parallel');
dag.addEdge('parallel', 'taskA');
dag.addEdge('parallel', 'taskB');
dag.addEdge('parallel', 'taskC');
dag.addEdge('taskA', 'merge');
dag.addEdge('taskB', 'merge');
dag.addEdge('taskC', 'merge');
```

## 事件

```javascript
engine.on('execution-started', (e) => {
  console.log('Started:', e.executionId);
});

engine.on('execution-completed', (e) => {
  console.log('Completed:', e.executionId, e.state.status);
});

engine.on('node-started', (e) => {
  console.log('Node started:', e.nodeId);
});

engine.on('node-completed', (e) => {
  console.log('Node completed:', e.nodeId);
});
```

## 测试

```bash
npm test
```

## License

MIT
