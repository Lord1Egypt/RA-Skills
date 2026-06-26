/**
 * Memory Sync - 记忆同步引擎
 * 
 * 功能:
 * - 多Agent共享记忆
 * - 验证冲突
 * - 增量同步
 * - 审计接口
 * 
 * Ported from memory_sync.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, appendFileSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const SHARED_DIR = join(MEMORY_DIR, 'shared');
const SYNC_STATE_FILE = join(SHARED_DIR, 'sync_state.json');
const NODE_REGISTRY_FILE = join(SHARED_DIR, 'nodes.json');

// ============================================================
// ConflictDetection
// ============================================================

export class ConflictDetection {
  constructor(existingData) {
    this.data = existingData || {};
  }

  /**
   * Detect conflicts between existing and new data
   * @param {object} newData
   * @returns {Array<object>}
   */
  detect(newData) {
    /** @type {Array} */
    const conflicts = [];

    for (const [key, newVal] of Object.entries(newData)) {
      if (!(key in this.data)) continue;

      const existingVal = this.data[key];

      if (typeof existingVal === 'string' && typeof newVal === 'string') {
        if (existingVal.trim() !== newVal.trim()) {
          conflicts.push({
            key,
            existing: existingVal.slice(0, 50) + (existingVal.length > 50 ? '...' : ''),
            proposed: newVal.slice(0, 50) + (newVal.length > 50 ? '...' : ''),
            type: 'text_conflict'
          });
        }
      }
    }

    return conflicts;
  }
}

// ============================================================
// SyncManager
// ============================================================

export class SyncManager {
  constructor() {
    mkdirSync(SHARED_DIR, { recursive: true });
    this.registry = this._loadRegistry();
    this.state = this._loadState();
  }

  _loadRegistry() {
    if (existsSync(NODE_REGISTRY_FILE)) {
      try { return JSON.parse(readFileSync(NODE_REGISTRY_FILE, 'utf-8')); } catch { /* ignore */ }
    }
    return { nodes: {}, last_updated: new Date().toISOString() };
  }

  _saveRegistry() {
    this.registry.last_updated = new Date().toISOString();
    writeFileSync(NODE_REGISTRY_FILE, JSON.stringify(this.registry, null, 2), 'utf-8');
  }

  _loadState() {
    if (existsSync(SYNC_STATE_FILE)) {
      try { return JSON.parse(readFileSync(SYNC_STATE_FILE, 'utf-8')); } catch { /* ignore */ }
    }
    return {
      schema: 'memory-sync-v1',
      last_sync: null,
      active_nodes: [],
      conflicts: {},
      sync_count: 0
    };
  }

  _saveState() {
    writeFileSync(SYNC_STATE_FILE, JSON.stringify(this.state, null, 2), 'utf-8');
  }

  /**
   * Register a node
   * @param {string} nodeId
   */
  registerNode(nodeId) {
    if (!(nodeId in this.registry.nodes)) {
      this.registry.nodes[nodeId] = {
        registered_at: new Date().toISOString(),
        version: 0,
        status: 'active'
      };
      this._saveRegistry();
      return { registered: true, node_id: nodeId };
    }
    return { registered: false, node_id: nodeId, reason: 'already exists' };
  }

  /**
   * Unregister a node
   * @param {string} nodeId
   */
  unregisterNode(nodeId) {
    if (nodeId in this.registry.nodes) {
      delete this.registry.nodes[nodeId];
      this._saveRegistry();
      return { unregistered: true };
    }
    return { unregistered: false, reason: 'not found' };
  }

  /**
   * Get all registered nodes
   */
  getNodes() {
    return Object.entries(this.registry.nodes).map(([nodeId, info]) => ({
      node_id: nodeId,
      ...info
    }));
  }

  /**
   * Record data from a node
   * @param {string} nodeId
   * @param {object} data
   */
  recordData(nodeId, data) {
    // Get current memories
    let currentMemories = {};
    try {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      if (existsSync(memoryFile)) {
        const allMems = JSON.parse(readFileSync(memoryFile, 'utf-8'));
        const mems = Array.isArray(allMems) ? allMems : (allMems.memories || []);
        for (const mem of mems) {
          currentMemories[mem.id] = mem.text || '';
        }
      }
    } catch { /* ignore */ }

    // Detect conflicts
    const detector = new ConflictDetection(currentMemories);
    const conflicts = detector.detect(data);

    /** @type {object} */
    const result = {
      recorded: false,
      conflicts,
      node_id: nodeId
    };

    if (conflicts.length > 0) {
      // Record conflicts
      const timestamp = new Date().toISOString();
      if (!this.state.conflicts) this.state.conflicts = {};
      this.state.conflicts[timestamp] = { node_id: nodeId, conflicts };
      result.needs_resolution = true;
    }

    // Store to memory
    try {
      const memoryFile = join(MEMORY_DIR, 'memories.json');
      let mems = [];
      if (existsSync(memoryFile)) {
        try {
          const allMems = JSON.parse(readFileSync(memoryFile, 'utf-8'));
          mems = Array.isArray(allMems) ? allMems : (allMems.memories || []);
        } catch { mems = []; }
      }

      for (const [key, value] of Object.entries(data)) {
        const id = `sync_${createHash('md5').update(key + Date.now().toString()).digest('hex').slice(0, 12)}`;
        mems.push({
          id,
          text: typeof value === 'string' ? value : JSON.stringify(value),
          category: 'sync',
          source: nodeId,
          timestamp: new Date().toISOString(),
          importance: 0.5
        });
      }

      writeFileSync(memoryFile, JSON.stringify(mems, null, 2), 'utf-8');
      result.recorded = true;
    } catch (e) {
      result.error = e.message;
    }

    // Update node version
    if (nodeId in this.registry.nodes) {
      this.registry.nodes[nodeId].version = (this.registry.nodes[nodeId].version || 0) + 1;
      this.registry.nodes[nodeId].last_update = new Date().toISOString();
    }

    this._saveState();
    this._saveRegistry();

    return result;
  }

  /**
   * Perform sync
   * @param {string} sourceNode
   */
  sync(sourceNode = null) {
    this.state.last_sync = new Date().toISOString();
    this.state.sync_count = (this.state.sync_count || 0) + 1;
    this.state.active_nodes = Object.keys(this.registry.nodes);

    this._saveState();

    return {
      synced: true,
      timestamp: this.state.last_sync,
      nodes: this.state.active_nodes.length,
      conflicts_pending: Object.keys(this.state.conflicts || {}).length
    };
  }

  /**
   * Resolve conflicts
   * @param {string} strategy
   */
  resolveConflicts(strategy = 'last_write_wins') {
    /** @type {Array} */
    const resolved = [];

    if (this.state.conflicts) {
      for (const [timestamp, conflictData] of Object.entries(this.state.conflicts)) {
        for (const conflict of (conflictData.conflicts || [])) {
          if (strategy === 'last_write_wins') {
            resolved.push({ key: conflict.key, strategy, result: 'accepted_proposed' });
          }
        }
      }
      this.state.conflicts = {};
    }

    this._saveState();

    return { resolved: resolved.length, strategy, details: resolved };
  }

  /**
   * Get sync status
   */
  getStatus() {
    return {
      nodes: Object.keys(this.registry.nodes).length,
      active_nodes: this.state.active_nodes || [],
      last_sync: this.state.last_sync,
      sync_count: this.state.sync_count || 0,
      pending_conflicts: Object.keys(this.state.conflicts || {}).length
    };
  }
}

// ============================================================
// CLI Handler
// ============================================================

/**
 * @param {string} command
 * @param {object} args
 * @returns {object}
 */
export function cmdSync(command, args) {
  const manager = new SyncManager();

  switch (command) {
    case 'init': {
      mkdirSync(SHARED_DIR, { recursive: true });
      return { type: 'text', text: `✅ 同步初始化完成\n   共享目录: ${SHARED_DIR}` };
    }

    case 'add-node': {
      if (!args.nodeId) return { error: '请提供 --node-id' };
      const result = manager.registerNode(args.nodeId);
      return {
        type: 'text',
        text: result.registered ? `✅ 节点已注册: ${args.nodeId}` : `⚠️ 节点已存在: ${args.nodeId}`
      };
    }

    case 'remove-node': {
      if (!args.nodeId) return { error: '请提供 --node-id' };
      const result = manager.unregisterNode(args.nodeId);
      return {
        type: 'text',
        text: result.unregistered ? `✅ 节点已注销: ${args.nodeId}` : `⚠️ 节点不存在: ${args.nodeId}`
      };
    }

    case 'list-nodes': {
      const nodes = manager.getNodes();
      if (args.json) return { type: 'json', data: nodes };
      const lines = [`📋 已注册节点 (${nodes.length}):`];
      nodes.forEach(n => lines.push(`   ${n.node_id}: v${n.version || 0} [${n.status}]`));
      return { type: 'text', text: lines.join('\n') };
    }

    case 'record': {
      if (!args.nodeId) return { error: '请提供 --node-id' };
      if (!args.data) return { error: '请提供 --data (JSON)' };
      let data;
      try { data = JSON.parse(args.data); } catch { return { error: '--data 必须是有效的 JSON' }; }
      const result = manager.recordData(args.nodeId, data);
      if (result.conflicts && result.conflicts.length > 0) {
        return {
          type: 'text',
          text: `✅ 记录完成，但有 ${result.conflicts.length} 个冲突需要解决`
        };
      }
      return { type: 'text', text: '✅ 记录完成' };
    }

    case 'sync': {
      const result = manager.sync(args.nodeId);
      if (args.json) return { type: 'json', data: result };
      return {
        type: 'text',
        text: `✅ 同步完成\n   节点数: ${result.nodes}\n   待处理冲突: ${result.conflicts_pending}`
      };
    }

    case 'resolve': {
      const result = manager.resolveConflicts(args.strategy || 'last_write_wins');
      return {
        type: 'text',
        text: `✅ 冲突解决\n   策略: ${result.strategy}\n   已解决: ${result.resolved} 个`
      };
    }

    case 'status': {
      const status = manager.getStatus();
      if (args.json) return { type: 'json', data: status };
      return {
        type: 'text',
        text: `📊 同步状态\n` +
          `   节点数: ${status.nodes}\n` +
          `   同步次数: ${status.sync_count}\n` +
          `   上次同步: ${status.last_sync || '从未'}\n` +
          `   待处理冲突: ${status.pending_conflicts}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { SyncManager, ConflictDetection, cmdSync };
