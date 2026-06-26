/**
 * Memory Context Tree - 上下文树实现
 * 
 * 借鉴 QMD 的 Context Tree 概念，实现记忆的层级上下文关系
 * 
 * Ported from memory_context.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const CONTEXT_FILE = join(MEMORY_DIR, 'context_tree.json');

// ============================================================
// ContextNode
// ============================================================

/**
 * @typedef {Object} ContextNodeData
 * @property {string} path
 * @property {string} description
 * @property {string} parent
 * @property {string[]} children
 * @property {string[]} memories
 * @property {string} created
 * @property {string} updated
 */

export class ContextNode {
  /**
   * @param {string} path
   * @param {string} description
   * @param {string} parent
   */
  constructor(path, description = '', parent = '') {
    this.path = path;
    this.description = description;
    this.parent = parent;
    this.children = [];
    this.memories = [];
    this.created = new Date().toISOString();
    this.updated = this.created;
  }

  toDict() {
    return {
      path: this.path,
      description: this.description,
      parent: this.parent,
      children: this.children,
      memories: this.memories,
      created: this.created,
      updated: this.updated
    };
  }

  static fromDict(data) {
    const node = new ContextNode(
      data.path || '',
      data.description || '',
      data.parent || ''
    );
    node.children = data.children || [];
    node.memories = data.memories || [];
    node.created = data.created || new Date().toISOString();
    node.updated = data.updated || new Date().toISOString();
    return node;
  }
}

// ============================================================
// ContextTree
// ============================================================

export class ContextTree {
  constructor() {
    /** @type {Map<string, ContextNode>} */
    this.nodes = new Map();
    /** @type {Map<string, string>} memory_id -> context_path */
    this.memoryIndex = new Map();
    this._load();
  }

  _load() {
    if (!existsSync(CONTEXT_FILE)) {
      this._createDefaults();
      return;
    }

    try {
      const data = JSON.parse(readFileSync(CONTEXT_FILE, 'utf-8'));
      for (const [path, nodeData] of Object.entries(data.nodes || {})) {
        this.nodes.set(path, ContextNode.fromDict(nodeData));
      }
      // memoryIndex can be object or Map
      if (data.memory_index && typeof data.memory_index === 'object') {
        for (const [memId, ctxPath] of Object.entries(data.memory_index)) {
          this.memoryIndex.set(memId, ctxPath);
        }
      }
    } catch (e) {
      console.error(`⚠️ 加载 Context Tree 失败: ${e.message}`);
      this._createDefaults();
    }
  }

  _createDefaults() {
    // User contexts
    this.addContext('user:default', '默认用户', '', false);

    // Project contexts
    this.addContext('project:default', '默认项目', '', false);

    // QMD-style contexts
    this.addContext('qmd://notes', '个人笔记和想法', '', false);
    this.addContext('qmd://meetings', '会议记录和纪要', '', false);
    this.addContext('qmd://docs', '工作文档和资料', '', false);

    // Sub-contexts
    this.addContext('qmd://notes/projects', '项目相关笔记', 'qmd://notes', false);
    this.addContext('qmd://notes/ideas', '创意和想法', 'qmd://notes', false);

    this._save();
  }

  _save() {
    try {
      mkdirSync(MEMORY_DIR, { recursive: true });
      const nodesObj = {};
      for (const [path, node] of this.nodes) {
        nodesObj[path] = node.toDict();
      }
      // Convert Map to object for JSON serialization
      const memIndexObj = {};
      for (const [memId, ctxPath] of this.memoryIndex) {
        memIndexObj[memId] = ctxPath;
      }
      writeFileSync(CONTEXT_FILE, JSON.stringify({
        nodes: nodesObj,
        memory_index: memIndexObj,
        updated: new Date().toISOString()
      }, null, 2), 'utf-8');
    } catch (e) {
      console.error(`⚠️ 保存 Context Tree 失败: ${e.message}`);
    }
  }

  /**
   * Add a new context
   * @param {string} path
   * @param {string} description
   * @param {string} parent
   * @param {boolean} save
   */
  addContext(path, description = '', parent = '', save = true) {
    const node = new ContextNode(path, description, parent);
    this.nodes.set(path, node);

    if (parent && this.nodes.has(parent)) {
      const parentNode = this.nodes.get(parent);
      if (!parentNode.children.includes(path)) {
        parentNode.children.push(path);
      }
    }

    if (save) this._save();
  }

  /**
   * Get a context by path
   * @param {string} path
   * @returns {ContextNodeData|null}
   */
  getContext(path) {
    const node = this.nodes.get(path);
    return node ? node.toDict() : null;
  }

  /**
   * List all contexts
   * @returns {ContextNodeData[]}
   */
  listContexts() {
    return [...this.nodes.values()].map(n => n.toDict());
  }

  /**
   * Search contexts by query
   * @param {string} query
   * @returns {ContextNodeData[]}
   */
  searchContexts(query) {
    const results = [];
    const queryLower = query.toLowerCase();
    for (const node of this.nodes.values()) {
      if (
        node.path.toLowerCase().includes(queryLower) ||
        node.description.toLowerCase().includes(queryLower)
      ) {
        results.push(node.toDict());
      }
    }
    return results;
  }

  /**
   * Add a memory to a context
   * @param {string} contextPath
   * @param {string} memoryId
   * @param {string} content
   * @param {string} category
   */
  addMemory(contextPath, memoryId, content = '', category = '') {
    if (!this.nodes.has(contextPath)) {
      this.addContext(contextPath, `Auto-created for ${category}`);
    }

    const node = this.nodes.get(contextPath);
    if (!node.memories.includes(memoryId)) {
      node.memories.push(memoryId);
      node.updated = new Date().toISOString();
    }

    this.memoryIndex.set(memoryId, contextPath);
    this._save();
  }

  /**
   * Get context chain from root to current node
   * @param {string} path
   * @returns {string[]}
   */
  getContextChain(path) {
    const chain = [];
    let current = path;

    while (current) {
      if (this.nodes.has(current)) {
        chain.unshift(current);
      }
      const node = this.nodes.get(current);
      current = node ? node.parent : '';
    }

    return chain;
  }

  /**
   * Get all descendant memories of a context
   * @param {string} path
   * @returns {string[]}
   */
  getAllDescendantMemories(path) {
    const memories = [];

    if (this.nodes.has(path)) {
      memories.push(...this.nodes.get(path).memories);
    }

    if (this.nodes.has(path)) {
      for (const child of this.nodes.get(path).children) {
        memories.push(...this.getAllDescendantMemories(child));
      }
    }

    return memories;
  }

  /**
   * Get context description chain for enhancing search results
   * @param {string} path
   * @returns {string}
   */
  getContextDescriptionChain(path) {
    const chain = this.getContextChain(path);
    const descriptions = [];

    for (const p of chain) {
      const node = this.nodes.get(p);
      if (node && node.description) {
        descriptions.push(node.description);
      }
    }

    return descriptions.join(' > ') || path;
  }
}

// ============================================================
// Context-aware Search
// ============================================================

/**
 * Search with context chain enrichment
 * @param {string} query
 * @param {string} mode
 * @param {number} limit
 * @param {ContextTree} contextTree
 * @returns {Promise<Array>}
 */
export async function searchWithContext(query, mode = 'hybrid', limit = 5, contextTree = null) {
  if (!contextTree) {
    contextTree = new ContextTree();
  }

  // Dynamic import to avoid circular dependency
  let results = [];
  try {
    const { fallbackSearch } = await import('../utils/text.js');
    results = fallbackSearch([], query, limit);
  } catch {
    results = [];
  }

  // Enrich each result with context chain
  for (const r of results) {
    const memoryId = r.id || '';
    const contextPath = contextTree.memoryIndex.get(memoryId);

    if (contextPath) {
      r.context_path = contextPath;
      r.context_chain = contextTree.getContextChain(contextPath);
      r.context_description = contextTree.getContextDescriptionChain(contextPath);
    }
  }

  return results;
}

/**
 * Automatically match best context based on query
 * @param {string} query
 * @param {ContextTree} contextTree
 * @returns {string}
 */
export function findBestContext(query, contextTree = null) {
  if (!contextTree) {
    contextTree = new ContextTree();
  }

  const queryLower = query.toLowerCase();

  // Matching patterns
  const patterns = [
    { regex: /用户|偏好|习惯|喜欢/, prefix: 'user:' },
    { regex: /项目|进度|任务/, prefix: 'project:' },
    { regex: /会议|纪要/, prefix: 'qmd://meetings' },
    { regex: /笔记|想法|创意/, prefix: 'qmd://notes' },
    { regex: /文档|资料/, prefix: 'qmd://docs' }
  ];

  for (const { regex, prefix } of patterns) {
    if (regex.test(queryLower)) {
      for (const path of contextTree.nodes.keys()) {
        if (path.startsWith(prefix)) {
          return path;
        }
      }
    }
  }

  // Default: first context or user:default
  const first = [...contextTree.nodes.keys()][0];
  return first || 'user:default';
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} action
 * @param {object} args
 * @returns {object}
 */
export function cmdContext(action, args) {
  const tree = new ContextTree();

  switch (action) {
    case 'add': {
      const { path, description = '', parent = '' } = args;
      if (!path) return { error: '需要指定 --path' };
      tree.addContext(path, description, parent);
      return { type: 'text', text: `✅ 添加 Context: ${path}` };
    }

    case 'get': {
      const { path } = args;
      if (!path) return { error: '需要指定 --path' };
      const ctx = tree.getContext(path);
      if (!ctx) return { error: `❌ 未找到 Context: ${path}` };
      if (args.json) return { type: 'json', data: ctx };
      return {
        type: 'text',
        text: `📁 Context: ${ctx.path}\n   描述: ${ctx.description}\n` +
          `   父节点: ${ctx.parent}\n   子节点: ${JSON.stringify(ctx.children)}\n` +
          `   记忆数: ${ctx.memories.length}`
      };
    }

    case 'list': {
      const contexts = tree.listContexts();
      if (args.json) return { type: 'json', data: contexts };
      return {
        type: 'text',
        text: `📁 Context 列表 (${contexts.length} 个):\n\n` +
          contexts.map(ctx => {
            const depth = (ctx.path.match(/\//g) || []).length;
            const indent = '  '.repeat(Math.max(0, depth - 1));
            return `${indent}- ${ctx.path}: ${ctx.description}`;
          }).join('\n')
      };
    }

    case 'search': {
      if (!args.path) return { error: '需要指定搜索关键词 --path' };
      const results = tree.searchContexts(args.path);
      if (args.json) return { type: 'json', data: results };
      return {
        type: 'text',
        text: results.map(r => `- ${r.path}: ${r.description}`).join('\n')
      };
    }

    case 'chain': {
      const { path } = args;
      if (!path) return { error: '需要指定 --path' };
      const chain = tree.getContextChain(path);
      const desc = tree.getContextDescriptionChain(path);
      return {
        type: 'text',
        text: `🔗 Context 链: ${chain.join(' -> ')}\n📝 描述链: ${desc}`
      };
    }

    default:
      return { error: `未知操作: ${action}` };
  }
}

export default {
  ContextNode,
  ContextTree,
  searchWithContext,
  findBestContext,
  cmdContext
};
