/**
 * Workflow Engine - DAG 执行器
 * 支持有向无环图（DAG）的工作流编排
 */

import { EventEmitter } from 'events';
import fs from 'fs/promises';
import path from 'path';

/**
 * 工作流节点
 */
export class WorkflowNode {
  constructor(config) {
    this.id = config.id;
    this.type = config.type || 'task'; // 'task' | 'condition' | 'parallel' | 'start' | 'end'
    this.name = config.name || this.id;
    this.description = config.description || '';
    
    // 执行函数
    this.execute = config.execute || (async () => {});
    
    // 条件分支（仅 condition 类型）
    this.condition = config.condition;
    this.branches = config.branches || {}; // { 'true': nextId, 'false': nextId }
    
    // 并行任务（仅 parallel 类型）
    this.parallelTasks = config.parallelTasks || [];
    
    // 重试配置
    this.retry = config.retry || { count: 0, delay: 1000 };
    
    // 超时配置
    this.timeout = config.timeout || 30000;
    
    // 元数据
    this.metadata = config.metadata || {};
  }
}

/**
 * 工作流 DAG
 */
export class WorkflowDAG extends EventEmitter {
  constructor(config = {}) {
    super();
    this.id = config.id || `dag_${Date.now()}`;
    this.name = config.name || 'Unnamed Workflow';
    this.description = config.description || '';
    
    this.nodes = new Map(); // id -> WorkflowNode
    this.edges = new Map(); // fromId -> [toIds]
    this.reverseEdges = new Map(); // toId -> [fromIds]
    
    this.startNode = null;
    this.endNodes = new Set();
  }

  /**
   * 添加节点
   */
  addNode(node) {
    if (!(node instanceof WorkflowNode)) {
      node = new WorkflowNode(node);
    }
    
    this.nodes.set(node.id, node);
    
    // 自动识别开始和结束节点
    if (node.type === 'start') {
      this.startNode = node.id;
    }
    if (node.type === 'end') {
      this.endNodes.add(node.id);
    }
    
    return node;
  }

  /**
   * 添加边（依赖关系）
   */
  addEdge(fromId, toId) {
    if (!this.edges.has(fromId)) {
      this.edges.set(fromId, []);
    }
    if (!this.edges.get(fromId).includes(toId)) {
      this.edges.get(fromId).push(toId);
    }
    
    // 反向边
    if (!this.reverseEdges.has(toId)) {
      this.reverseEdges.set(toId, []);
    }
    if (!this.reverseEdges.get(toId).includes(fromId)) {
      this.reverseEdges.get(toId).push(fromId);
    }
  }

  /**
   * 获取节点的依赖（前置节点）
   */
  getDependencies(nodeId) {
    return this.reverseEdges.get(nodeId) || [];
  }

  /**
   * 获取节点的下游节点
   */
  getDownstream(nodeId) {
    return this.edges.get(nodeId) || [];
  }

  /**
   * 检测循环依赖
   */
  detectCycle() {
    const visited = new Set();
    const recursionStack = new Set();

    const dfs = (nodeId) => {
      visited.add(nodeId);
      recursionStack.add(nodeId);

      const downstream = this.getDownstream(nodeId);
      for (const nextId of downstream) {
        if (!visited.has(nextId)) {
          if (dfs(nextId)) return true;
        } else if (recursionStack.has(nextId)) {
          return true; // 发现循环
        }
      }

      recursionStack.delete(nodeId);
      return false;
    };

    for (const nodeId of this.nodes.keys()) {
      if (!visited.has(nodeId)) {
        if (dfs(nodeId)) return true;
      }
    }

    return false;
  }

  /**
   * 拓扑排序
   */
  topologicalSort() {
    if (this.detectCycle()) {
      throw new Error('Workflow contains cycle');
    }

    const inDegree = new Map();
    for (const nodeId of this.nodes.keys()) {
      inDegree.set(nodeId, this.getDependencies(nodeId).length);
    }

    const queue = [];
    for (const [nodeId, degree] of inDegree) {
      if (degree === 0) {
        queue.push(nodeId);
      }
    }

    const result = [];
    while (queue.length > 0) {
      const nodeId = queue.shift();
      result.push(nodeId);

      const downstream = this.getDownstream(nodeId);
      for (const nextId of downstream) {
        inDegree.set(nextId, inDegree.get(nextId) - 1);
        if (inDegree.get(nextId) === 0) {
          queue.push(nextId);
        }
      }
    }

    if (result.length !== this.nodes.size) {
      throw new Error('Topological sort failed');
    }

    return result;
  }

  /**
   * 获取执行顺序（考虑并行）
   */
  getExecutionLevels() {
    const sorted = this.topologicalSort();
    const levels = [];
    const completed = new Set();

    while (completed.size < sorted.length) {
      const currentLevel = [];
      
      for (const nodeId of sorted) {
        if (completed.has(nodeId)) continue;
        
        const deps = this.getDependencies(nodeId);
        const allDepsCompleted = deps.every(dep => completed.has(dep));
        
        if (allDepsCompleted) {
          currentLevel.push(nodeId);
        }
      }

      if (currentLevel.length === 0) {
        throw new Error('Cannot determine execution order');
      }

      levels.push(currentLevel);
      currentLevel.forEach(id => completed.add(id));
    }

    return levels;
  }

  /**
   * 导出为 JSON
   */
  toJSON() {
    return {
      id: this.id,
      name: this.name,
      description: this.description,
      nodes: Array.from(this.nodes.values()).map(n => ({
        id: n.id,
        type: n.type,
        name: n.name,
        description: n.description,
        retry: n.retry,
        timeout: n.timeout,
        metadata: n.metadata
      })),
      edges: Array.from(this.edges.entries()).map(([from, tos]) => ({
        from,
        to: tos
      }))
    };
  }

  /**
   * 从 JSON 导入
   */
  static fromJSON(json) {
    const dag = new WorkflowDAG({
      id: json.id,
      name: json.name,
      description: json.description
    });

    for (const nodeData of json.nodes) {
      dag.addNode(new WorkflowNode(nodeData));
    }

    for (const edge of json.edges) {
      for (const toId of edge.to) {
        dag.addEdge(edge.from, toId);
      }
    }

    return dag;
  }

  /**
   * 保存到文件
   */
  async save(filePath) {
    const json = this.toJSON();
    await fs.writeFile(filePath, JSON.stringify(json, null, 2), 'utf-8');
  }

  /**
   * 从文件加载
   */
  static async load(filePath) {
    const content = await fs.readFile(filePath, 'utf-8');
    const json = JSON.parse(content);
    return WorkflowDAG.fromJSON(json);
  }
}

export default WorkflowDAG;
