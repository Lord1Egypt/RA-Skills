/**
 * Workflow Engine 测试套件
 */

import { WorkflowEngine } from '../src/workflow-engine.js';
import WorkflowDAG, { WorkflowNode } from '../src/dag.js';
import WorkflowExecutor from '../src/executor.js';

// 测试运行器
class TestRunner {
  constructor() {
    this.tests = [];
    this.passed = 0;
    this.failed = 0;
  }

  test(name, fn) {
    this.tests.push({ name, fn });
  }

  async run() {
    console.log('🧪 Workflow Engine Test Suite Starting...\n');
    
    for (const { name, fn } of this.tests) {
      try {
        await fn();
        console.log(`✓ ${name}`);
        this.passed++;
      } catch (error) {
        console.log(`✗ ${name}`);
        console.log(`  Error: ${error.message}`);
        this.failed++;
      }
    }
    
    console.log(`\n📊 Results: ${this.passed} passed, ${this.failed} failed`);
    return this.failed === 0;
  }
}

const runner = new TestRunner();

// === WorkflowNode Tests ===
runner.test('WorkflowNode - should create node', async () => {
  const node = new WorkflowNode({
    id: 'test_node',
    type: 'task',
    name: 'Test Node'
  });
  if (!node || node.id !== 'test_node') throw new Error('Failed to create node');
});

runner.test('WorkflowNode - should have default execute function', async () => {
  const node = new WorkflowNode({ id: 'test' });
  if (typeof node.execute !== 'function') throw new Error('Should have execute function');
});

// === WorkflowDAG Tests ===
runner.test('WorkflowDAG - should create DAG', async () => {
  const dag = new WorkflowDAG({ name: 'Test Workflow' });
  if (!dag || dag.name !== 'Test Workflow') throw new Error('Failed to create DAG');
});

runner.test('WorkflowDAG - should add node', async () => {
  const dag = new WorkflowDAG({ name: 'Test' });
  const node = dag.addNode({
    id: 'task1',
    type: 'task',
    name: 'Task 1'
  });
  if (!dag.nodes.has('task1')) throw new Error('Failed to add node');
});

runner.test('WorkflowDAG - should connect nodes', async () => {
  const dag = new WorkflowDAG({ name: 'Test' });
  dag.addNode({ id: 'start', type: 'start' });
  dag.addNode({ id: 'task1', type: 'task' });
  dag.addEdge('start', 'task1');
  
  if (!dag.edges.get('start')?.includes('task1')) {
    throw new Error('Failed to connect nodes');
  }
});

runner.test('WorkflowDAG - should detect start node', async () => {
  const dag = new WorkflowDAG({ name: 'Test' });
  dag.addNode({ id: 'start', type: 'start' });
  if (dag.startNode !== 'start') throw new Error('Should detect start node');
});

runner.test('WorkflowDAG - should get topological order', async () => {
  const dag = new WorkflowDAG({ name: 'Test' });
  dag.addNode({ id: 'start', type: 'start' });
  dag.addNode({ id: 'task1', type: 'task' });
  dag.addNode({ id: 'task2', type: 'task' });
  dag.addEdge('start', 'task1');
  dag.addEdge('task1', 'task2');
  
  const order = dag.topologicalSort();
  if (!order || order.length !== 3) throw new Error('Should get topological order');
  if (order[0] !== 'start') throw new Error('Start should be first');
});

// === WorkflowExecutor Tests ===
runner.test('WorkflowExecutor - should initialize', async () => {
  const executor = new WorkflowExecutor({});
  if (!executor) throw new Error('Failed to initialize executor');
});

runner.test('WorkflowExecutor - should execute simple workflow', async () => {
  const executor = new WorkflowExecutor({});
  const dag = new WorkflowDAG({ name: 'Simple Test' });
  
  let executed = false;
  dag.addNode({ id: 'start', type: 'start' });
  dag.addNode({
    id: 'task1',
    type: 'task',
    execute: async () => { executed = true; return { success: true }; }
  });
  dag.addEdge('start', 'task1');
  
  const result = await executor.execute(dag, {});
  if (!executed) throw new Error('Task should be executed');
  if (result.status !== 'completed') throw new Error('Execution should succeed');
});

runner.test('WorkflowExecutor - should handle task execution', async () => {
  const executor = new WorkflowExecutor({});
  const dag = new WorkflowDAG({ name: 'Task Test' });
  
  let taskExecuted = false;
  dag.addNode({ id: 'start', type: 'start' });
  dag.addNode({
    id: 'task1',
    type: 'task',
    execute: async (ctx) => { 
      taskExecuted = true; 
      ctx.result = 'done';
      return { result: 'done' }; 
    }
  });
  dag.addEdge('start', 'task1');
  
  const result = await executor.execute(dag, { input: 'test' });
  if (!taskExecuted) throw new Error('Task should be executed');
  if (result.status !== 'completed') throw new Error('Execution should complete');
});

runner.test('WorkflowExecutor - should handle task failure', async () => {
  const executor = new WorkflowExecutor({});
  const dag = new WorkflowDAG({ name: 'Failure Test' });
  
  dag.addNode({ id: 'start', type: 'start' });
  dag.addNode({
    id: 'failing_task',
    type: 'task',
    execute: async () => { throw new Error('Task failed'); }
  });
  dag.addEdge('start', 'failing_task');
  
  const result = await executor.execute(dag, {});
  if (result.status !== 'failed') throw new Error('Execution should fail');
});

// === WorkflowEngine Integration Tests ===
runner.test('WorkflowEngine - should initialize', async () => {
  const engine = new WorkflowEngine({});
  if (!engine) throw new Error('Failed to initialize engine');
});

runner.test('WorkflowEngine - should create sequential workflow', async () => {
  const engine = new WorkflowEngine({});
  const tasks = [
    { name: 'Task 1', execute: async () => ({ result: 1 }) },
    { name: 'Task 2', execute: async () => ({ result: 2 }) }
  ];
  
  const dag = engine.createSequentialWorkflow('Test', tasks);
  if (!dag || dag.nodes.size !== 4) { // start + 2 tasks + end
    throw new Error('Should create workflow with 4 nodes');
  }
});

runner.test('WorkflowEngine - should execute registered workflow', async () => {
  const engine = new WorkflowEngine({});
  const dag = engine.createSequentialWorkflow('Test', [
    { name: 'Task 1', execute: async () => ({ value: 42 }) }
  ]);
  
  const result = await engine.execute(dag.id, {});
  if (result.status !== 'completed') throw new Error('Execution should succeed');
});

// 运行测试
runner.run().then(success => {
  process.exit(success ? 0 : 1);
});
