/**
 * Memory V2 - 图存储模块
 * 轻量级知识图谱实现，支持实体和关系存储
 */

import { EventEmitter } from 'events';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

/**
 * 图存储类
 */
export class GraphStore extends EventEmitter {
  /**
   * @param {Object} config
   * @param {string} config.dbPath - 数据库路径
   */
  constructor(config = {}) {
    super();
    this.dbPath = config.dbPath || path.join(__dirname, '../../memory/ontology');
    this.nodesFile = path.join(this.dbPath, 'nodes.jsonl');
    this.edgesFile = path.join(this.dbPath, 'edges.jsonl');
    
    this.nodes = new Map(); // id -> node
    this.edges = new Map(); // fromId -> [{to, relation, properties}]
    this.reverseEdges = new Map(); // toId -> [{from, relation, properties}]
    this.initialized = false;
  }

  /**
   * 初始化图存储
   */
  async initialize() {
    if (this.initialized) {
      return;
    }

    this.emit('initializing');

    // 确保目录存在
    await fs.mkdir(this.dbPath, { recursive: true });

    // 加载现有数据
    await this.load();

    this.initialized = true;
    this.emit('initialized');
  }

  /**
   * 从文件加载数据
   */
  async load() {
    try {
      // 加载节点
      if (await this.fileExists(this.nodesFile)) {
        const nodesData = await fs.readFile(this.nodesFile, 'utf-8');
        const lines = nodesData.split('\n').filter(line => line.trim());
        
        for (const line of lines) {
          try {
            const node = JSON.parse(line);
            this.nodes.set(node.id, node);
          } catch (e) {
            console.warn('[GraphStore] Failed to parse node:', e);
          }
        }
        console.log(`[GraphStore] Loaded ${this.nodes.size} nodes`);
      }

      // 加载边
      if (await this.fileExists(this.edgesFile)) {
        const edgesData = await fs.readFile(this.edgesFile, 'utf-8');
        const lines = edgesData.split('\n').filter(line => line.trim());
        
        for (const line of lines) {
          try {
            const edge = JSON.parse(line);
            this.addEdgeToMaps(edge);
          } catch (e) {
            console.warn('[GraphStore] Failed to parse edge:', e);
          }
        }
        console.log(`[GraphStore] Loaded edges for ${this.edges.size} nodes`);
      }
    } catch (e) {
      console.error('[GraphStore] Failed to load:', e);
    }
  }

  /**
   * 保存数据到文件
   */
  async save() {
    try {
      // 保存节点
      const nodesData = Array.from(this.nodes.values())
        .map(node => JSON.stringify(node))
        .join('\n');
      await fs.writeFile(this.nodesFile, nodesData, 'utf-8');

      // 保存边
      const edges = [];
      for (const [fromId, edgeList] of this.edges) {
        for (const edge of edgeList) {
          edges.push({
            from: fromId,
            to: edge.to,
            relation: edge.relation,
            properties: edge.properties
          });
        }
      }
      const edgesData = edges.map(edge => JSON.stringify(edge)).join('\n');
      await fs.writeFile(this.edgesFile, edgesData, 'utf-8');

      console.log(`[GraphStore] Saved ${this.nodes.size} nodes, ${edges.length} edges`);
    } catch (e) {
      console.error('[GraphStore] Failed to save:', e);
    }
  }

  /**
   * 添加节点
   * @param {string} id - 节点 ID
   * @param {string} type - 节点类型
   * @param {Object} properties - 属性
   */
  addNode(id, type, properties = {}) {
    if (!this.initialized) {
      this.initialize();
    }

    const node = {
      id,
      type,
      properties: {
        ...properties,
        createdAt: properties.createdAt || new Date().toISOString(),
        updatedAt: new Date().toISOString()
      }
    };

    this.nodes.set(id, node);
    this.emit('node-added', { id, type });
    
    return node;
  }

  /**
   * 获取节点
   * @param {string} id - 节点 ID
   * @returns {Object|null}
   */
  getNode(id) {
    return this.nodes.get(id) || null;
  }

  /**
   * 更新节点
   * @param {string} id - 节点 ID
   * @param {Object} updates - 更新内容
   */
  updateNode(id, updates) {
    const node = this.nodes.get(id);
    if (!node) {
      throw new Error(`Node ${id} not found`);
    }

    node.type = updates.type || node.type;
    node.properties = {
      ...node.properties,
      ...updates.properties,
      updatedAt: new Date().toISOString()
    };

    this.nodes.set(id, node);
    this.emit('node-updated', { id });
  }

  /**
   * 删除节点
   * @param {string} id - 节点 ID
   */
  deleteNode(id) {
    // 删除相关边
    this.edges.delete(id);
    this.reverseEdges.delete(id);

    // 删除其他节点指向该节点的边
    for (const [fromId, edgeList] of this.edges) {
      const filtered = edgeList.filter(edge => edge.to !== id);
      if (filtered.length === 0) {
        this.edges.delete(fromId);
      } else {
        this.edges.set(fromId, filtered);
      }
    }

    // 删除节点
    this.nodes.delete(id);
    this.emit('node-deleted', { id });
  }

  /**
   * 添加边
   * @param {string} from - 起始节点 ID
   * @param {string} relation - 关系类型
   * @param {string} to - 目标节点 ID
   * @param {Object} properties - 属性
   */
  addEdge(from, relation, to, properties = {}) {
    if (!this.initialized) {
      this.initialize();
    }

    const edge = {
      to,
      relation,
      properties: {
        ...properties,
        createdAt: properties.createdAt || new Date().toISOString()
      }
    };

    this.addEdgeToMaps(edge, from);
    this.emit('edge-added', { from, relation, to });
  }

  /**
   * 添加边到内部映射
   */
  addEdgeToMaps(edge, from) {
    // 正向边
    if (!this.edges.has(from)) {
      this.edges.set(from, []);
    }
    this.edges.get(from).push(edge);

    // 反向边
    if (!this.reverseEdges.has(edge.to)) {
      this.reverseEdges.set(edge.to, []);
    }
    this.reverseEdges.get(edge.to).push({
      from,
      relation: edge.relation,
      properties: edge.properties
    });
  }

  /**
   * 获取邻居节点
   * @param {string} nodeId - 节点 ID
   * @param {number} hops - 跳数
   * @returns {Array<Object>} - 邻居节点列表
   */
  getNeighbors(nodeId, hops = 1) {
    const visited = new Set();
    const neighbors = [];
    const queue = [[nodeId, 0]];

    while (queue.length > 0) {
      const [currentId, currentHops] = queue.shift();

      if (visited.has(currentId) || currentHops > hops) {
        continue;
      }

      visited.add(currentId);

      if (currentId !== nodeId) {
        const node = this.nodes.get(currentId);
        if (node) {
          neighbors.push(node);
        }
      }

      if (currentHops < hops) {
        // 添加出边邻居
        const edges = this.edges.get(currentId) || [];
        for (const edge of edges) {
          if (!visited.has(edge.to)) {
            queue.push([edge.to, currentHops + 1]);
          }
        }

        // 添加入边邻居（可选，双向遍历）
        const inEdges = this.reverseEdges.get(currentId) || [];
        for (const edge of inEdges) {
          if (!visited.has(edge.from)) {
            queue.push([edge.from, currentHops + 1]);
          }
        }
      }
    }

    return neighbors;
  }

  /**
   * 查询关系
   * @param {string} from - 起始节点 ID
   * @param {string} to - 目标节点 ID
   * @returns {Array<string>} - 关系列表
   */
  getRelations(from, to) {
    const edges = this.edges.get(from) || [];
    return edges
      .filter(edge => edge.to === to)
      .map(edge => edge.relation);
  }

  /**
   * 搜索节点（按属性）
   * @param {Object} query - 查询条件
   * @returns {Array<Object>} - 匹配的节点
   */
  searchNodes(query) {
    const results = [];

    for (const [id, node] of this.nodes) {
      let matches = true;

      // 类型匹配
      if (query.type && node.type !== query.type) {
        matches = false;
      }

      // 属性匹配
      if (query.properties) {
        for (const [key, value] of Object.entries(query.properties)) {
          if (node.properties[key] !== value) {
            matches = false;
            break;
          }
        }
      }

      // 文本搜索（在 name 属性中）
      if (query.text && node.properties.name) {
        const name = node.properties.name.toLowerCase();
        const text = query.text.toLowerCase();
        if (!name.includes(text)) {
          matches = false;
        }
      }

      if (matches) {
        results.push(node);
      }
    }

    return results;
  }

  /**
   * 获取统计信息
   * @returns {Object}
   */
  getStats() {
    let edgeCount = 0;
    for (const edges of this.edges.values()) {
      edgeCount += edges.length;
    }

    return {
      nodeCount: this.nodes.size,
      edgeCount,
      nodeTypes: this.getNodeTypeStats()
    };
  }

  /**
   * 获取节点类型统计
   */
  getNodeTypeStats() {
    const stats = new Map();
    for (const node of this.nodes.values()) {
      const type = node.type;
      stats.set(type, (stats.get(type) || 0) + 1);
    }
    return Object.fromEntries(stats);
  }

  /**
   * 检查文件是否存在
   */
  async fileExists(filePath) {
    try {
      await fs.access(filePath);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 清空图谱
   */
  async clear() {
    this.nodes.clear();
    this.edges.clear();
    this.reverseEdges.clear();
    
    // 删除文件
    try {
      await fs.unlink(this.nodesFile);
      await fs.unlink(this.edgesFile);
    } catch (e) {
      // 文件可能不存在
    }

    this.emit('cleared');
  }

  /**
   * 关闭存储
   */
  async close() {
    await this.save();
    this.initialized = false;
    this.emit('closed');
  }
}

export default GraphStore;
