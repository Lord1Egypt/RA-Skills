/**
 * Workflow Engine - 统一入口
 * 整合 DAG 和执行器，提供简洁的 API
 */

import WorkflowDAG, { WorkflowNode } from './dag.js';
import WorkflowExecutor from './executor.js';
import { EventEmitter } from 'events';

/**
 * 工作流引擎
 */
export class WorkflowEngine extends EventEmitter {
  constructor(config = {}) {
    super();
    this.executor = new WorkflowExecutor(config);
    this.workflows = new Map(); // workflowId -> WorkflowDAG
  }

  /**
   * 创建工作流
   */
  createWorkflow(config) {
    const dag = new WorkflowDAG(config);
    this.workflows.set(dag.id, dag);
    return dag;
  }

  /**
   * 注册工作流
   */
  registerWorkflow(dag) {
    this.workflows.set(dag.id, dag);
    return dag;
  }

  /**
   * 获取工作流
   */
  getWorkflow(id) {
    return this.workflows.get(id);
  }

  /**
   * 执行工作流
   */
  async execute(workflowId, context = {}, executionId = null) {
    const dag = this.workflows.get(workflowId);
    if (!dag) {
      throw new Error(`Workflow ${workflowId} not found`);
    }

    // 转发事件
    this.executor.on('execution-started', (e) => this.emit('execution-started', e));
    this.executor.on('execution-completed', (e) => this.emit('execution-completed', e));
    this.executor.on('node-started', (e) => this.emit('node-started', e));
    this.executor.on('node-completed', (e) => this.emit('node-completed', e));

    return await this.executor.execute(dag, context, executionId);
  }

  /**
   * 创建简单顺序工作流
   */
  createSequentialWorkflow(name, tasks) {
    const dag = this.createWorkflow({ name });
    
    // 开始节点
    dag.addNode(new WorkflowNode({
      id: 'start',
      type: 'start',
      name: 'Start'
    }));

    // 任务节点
    let prevId = 'start';
    tasks.forEach((task, index) => {
      const nodeId = `task_${index}`;
      dag.addNode(new WorkflowNode({
        id: nodeId,
        type: 'task',
        name: task.name || `Task ${index}`,
        execute: task.execute,
        timeout: task.timeout,
        retry: task.retry
      }));
      dag.addEdge(prevId, nodeId);
      prevId = nodeId;
    });

    // 结束节点
    dag.addNode(new WorkflowNode({
      id: 'end',
      type: 'end',
      name: 'End'
    }));
    dag.addEdge(prevId, 'end');

    return dag;
  }

  /**
   * 创建条件分支工作流
   */
  createConditionalWorkflow(name, config) {
    const dag = this.createWorkflow({ name });

    dag.addNode(new WorkflowNode({ id: 'start', type: 'start', name: 'Start' }));

    dag.addNode(new WorkflowNode({
      id: 'condition',
      type: 'condition',
      name: 'Condition',
      condition: config.condition,
      branches: {
        'true': 'task_true',
        'false': 'task_false'
      }
    }));

    dag.addNode(new WorkflowNode({
      id: 'task_true',
      type: 'task',
      name: 'True Branch',
      execute: config.trueBranch
    }));

    dag.addNode(new WorkflowNode({
      id: 'task_false',
      type: 'task',
      name: 'False Branch',
      execute: config.falseBranch
    }));

    dag.addNode(new WorkflowNode({ id: 'end', type: 'end', name: 'End' }));

    dag.addEdge('start', 'condition');
    dag.addEdge('task_true', 'end');
    dag.addEdge('task_false', 'end');

    return dag;
  }

  /**
   * 创建并行工作流
   */
  createParallelWorkflow(name, tasks) {
    const dag = this.createWorkflow({ name });

    dag.addNode(new WorkflowNode({ id: 'start', type: 'start', name: 'Start' }));

    dag.addNode(new WorkflowNode({
      id: 'parallel',
      type: 'parallel',
      name: 'Parallel Tasks',
      parallelTasks: tasks.map((task, i) => ({
        id: `parallel_${i}`,
        execute: task.execute
      }))
    }));

    dag.addNode(new WorkflowNode({ id: 'end', type: 'end', name: 'End' }));

    dag.addEdge('start', 'parallel');
    dag.addEdge('parallel', 'end');

    return dag;
  }
}

export { WorkflowDAG, WorkflowNode, WorkflowExecutor };
export default WorkflowEngine;
