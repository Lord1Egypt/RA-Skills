/**
 * Workflow Engine - 执行引擎
 * 执行 DAG 工作流，支持条件分支、并行执行、状态持久化
 */

import WorkflowDAG, { WorkflowNode } from './dag.js';
import { EventEmitter } from 'events';
import fs from 'fs/promises';
import path from 'path';

/**
 * 工作流执行器
 */
export class WorkflowExecutor extends EventEmitter {
  constructor(config = {}) {
    super();
    this.checkpointDir = config.checkpointDir || './checkpoints';
    this.enableCheckpoint = config.enableCheckpoint !== false;
    this.maxConcurrency = config.maxConcurrency || 10;
    
    this.executions = new Map(); // executionId -> executionState
  }

  /**
   * 执行工作流
   */
  async execute(dag, context = {}, executionId = null) {
    executionId = executionId || `exec_${Date.now()}`;
    this.emit('execution-started', { executionId, dag: dag.id });

    // 检查检查点
    let state = await this.loadCheckpoint(executionId);
    
    if (!state) {
      state = {
        executionId,
        dagId: dag.id,
        status: 'running',
        context: { ...context },
        completedNodes: new Set(),
        failedNodes: new Set(),
        nodeResults: new Map(),
        startTime: Date.now(),
        endTime: null
      };
    }

    this.executions.set(executionId, state);

    try {
      const levels = dag.getExecutionLevels();
      
      for (const level of levels) {
        const promises = level.map(nodeId => this.executeNode(dag, nodeId, state));
        const results = await Promise.allSettled(promises);
        
        const failures = results.filter(r => r.status === 'rejected');
        if (failures.length > 0) {
          state.status = 'failed';
          break;
        }
      }

      if (state.status !== 'failed') {
        state.status = 'completed';
      }

    } catch (error) {
      state.status = 'failed';
      state.error = error.message;
    }

    state.endTime = Date.now();
    state.duration = state.endTime - state.startTime;

    if (this.enableCheckpoint) {
      await this.saveCheckpoint(state);
    }

    this.emit('execution-completed', { executionId, state });
    
    return {
      executionId,
      status: state.status,
      context: state.context,
      results: Object.fromEntries(state.nodeResults),
      duration: state.duration
    };
  }

  /**
   * 执行单个节点
   */
  async executeNode(dag, nodeId, state) {
    const node = dag.nodes.get(nodeId);
    if (!node) throw new Error(`Node ${nodeId} not found`);
    if (state.completedNodes.has(nodeId)) return state.nodeResults.get(nodeId);

    this.emit('node-started', { executionId: state.executionId, nodeId });

    try {
      let result;

      switch (node.type) {
        case 'start':
          result = { started: true };
          break;
        case 'end':
          result = { completed: true };
          break;
        case 'condition':
          result = await this.executeConditionNode(node, state);
          break;
        case 'parallel':
          result = await this.executeParallelNode(node, state);
          break;
        default:
          result = await this.executeTaskNode(node, state);
      }

      state.completedNodes.add(nodeId);
      state.nodeResults.set(nodeId, result);
      this.emit('node-completed', { executionId: state.executionId, nodeId, result });

      if (this.enableCheckpoint) {
        await this.saveCheckpoint(state);
      }

      return result;

    } catch (error) {
      state.failedNodes.add(nodeId);
      if (node.retry?.count > 0) {
        return this.retryNode(dag, nodeId, state, node.retry);
      }
      throw error;
    }
  }

  async executeTaskNode(node, state) {
    const timeout = node.timeout || 30000;
    return new Promise(async (resolve, reject) => {
      const timer = setTimeout(() => reject(new Error(`Timeout`)), timeout);
      try {
        const result = await node.execute(state.context, state);
        clearTimeout(timer);
        resolve(result);
      } catch (error) {
        clearTimeout(timer);
        reject(error);
      }
    });
  }

  async executeConditionNode(node, state) {
    const condition = await node.condition(state.context, state);
    const branch = condition ? 'true' : 'false';
    return { condition, branch, nextNode: node.branches[branch] };
  }

  async executeParallelNode(node, state) {
    const tasks = node.parallelTasks.map(task => task.execute(state.context, state));
    const results = await Promise.allSettled(tasks);
    return { results };
  }

  async retryNode(dag, nodeId, state, retryConfig) {
    const { count, delay } = retryConfig;
    for (let i = 0; i < count; i++) {
      await new Promise(r => setTimeout(r, delay));
      try {
        return await this.executeNode(dag, nodeId, state);
      } catch (error) {
        if (i === count - 1) throw error;
      }
    }
  }

  async saveCheckpoint(state) {
    try {
      await fs.mkdir(this.checkpointDir, { recursive: true });
      const checkpointPath = path.join(this.checkpointDir, `${state.executionId}.json`);
      const checkpoint = {
        ...state,
        completedNodes: Array.from(state.completedNodes),
        failedNodes: Array.from(state.failedNodes),
        nodeResults: Array.from(state.nodeResults.entries())
      };
      await fs.writeFile(checkpointPath, JSON.stringify(checkpoint), 'utf-8');
    } catch (error) {
      console.warn('Checkpoint save failed:', error);
    }
  }

  async loadCheckpoint(executionId) {
    try {
      const checkpointPath = path.join(this.checkpointDir, `${executionId}.json`);
      const content = await fs.readFile(checkpointPath, 'utf-8');
      const checkpoint = JSON.parse(content);
      return {
        ...checkpoint,
        completedNodes: new Set(checkpoint.completedNodes),
        failedNodes: new Set(checkpoint.failedNodes),
        nodeResults: new Map(checkpoint.nodeResults)
      };
    } catch {
      return null;
    }
  }
}

export default WorkflowExecutor;
