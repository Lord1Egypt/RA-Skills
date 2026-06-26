/**
 * Memory Multi-Agent Share - 多Agent记忆共享
 * 
 * Ported from memory_multi_agent_share.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, appendFileSync } from 'fs';
import { join } from 'path';
import { createHash } from 'crypto';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const SHARE_DIR = join(MEMORY_DIR, 'multi_agent');

// ============================================================
// ShareManager
// ============================================================

export class ShareManager {
  constructor() {
    mkdirSync(SHARE_DIR, { recursive: true });
    this.registryFile = join(SHARE_DIR, 'registry.json');
    this.sharesFile = join(SHARE_DIR, 'shares.jsonl');
    this.subscriptionsFile = join(SHARE_DIR, 'subscriptions.json');
    this.registry = this._loadRegistry();
  }

  _loadRegistry() {
    if (existsSync(this.registryFile)) {
      try { return JSON.parse(readFileSync(this.registryFile, 'utf-8')); } catch { /* ignore */ }
    }
    return { agents: {}, shares: {} };
  }

  _saveRegistry() {
    writeFileSync(this.registryFile, JSON.stringify(this.registry, null, 2), 'utf-8');
  }

  /**
   * Register an agent
   * @param {string} agentId
   * @param {string} agentName
   */
  registerAgent(agentId, agentName) {
    this.registry.agents[agentId] = {
      name: agentName,
      registered_at: new Date().toISOString(),
      shared_count: 0
    };
    this._saveRegistry();
    return { success: true, agent_id: agentId };
  }

  /**
   * Share a memory to agents
   * @param {string} memoryId
   * @param {string} text
   * @param {string[]} targetAgents
   * @param {object} metadata
   */
  shareMemory(memoryId, text, targetAgents = [], metadata = {}) {
    const shareId = createHash('md5').update(memoryId + Date.now().toString()).digest('hex').slice(0, 12);
    const timestamp = new Date().toISOString();

    /** @type {object} */
    const share = {
      id: shareId,
      memory_id: memoryId,
      text,
      shared_by: process.env.OPENCLAW_AGENT_ID || 'unknown',
      target_agents: targetAgents,
      timestamp,
      metadata
    };

    appendFileSync(this.sharesFile, JSON.stringify(share) + '\n', 'utf-8');

    // Update registry
    if (!this.registry.shares[shareId]) {
      this.registry.shares[shareId] = share;
    }
    this._saveRegistry();

    return { success: true, share_id: shareId, share };
  }

  /**
   * Get shares for an agent
   * @param {string} agentId
   * @param {number} limit
   */
  getShares(agentId, limit = 20) {
    const shares = [];
    try {
      const lines = readFileSync(this.sharesFile, 'utf-8').split('\n').filter(Boolean);
      for (const line of lines) {
        try {
          const share = JSON.parse(line);
          // Agent is target or no specific target (broadcast)
          if (share.target_agents.length === 0 || share.target_agents.includes(agentId)) {
            shares.push(share);
          }
        } catch { /* skip */ }
      }
    } catch { /* file might not exist */ }

    shares.sort((a, b) => b.timestamp.localeCompare(a.timestamp));
    return shares.slice(0, limit);
  }

  /**
   * Subscribe to an agent's shares
   * @param {string} subscriberId
   * @param {string} targetAgentId
   */
  subscribe(subscriberId, targetAgentId) {
    if (!this.registry.subscriptions) this.registry.subscriptions = {};
    if (!this.registry.subscriptions[subscriberId]) this.registry.subscriptions[subscriberId] = [];
    if (!this.registry.subscriptions[subscriberId].includes(targetAgentId)) {
      this.registry.subscriptions[subscriberId].push(targetAgentId);
      this._saveRegistry();
    }
    return { success: true };
  }

  /**
   * Get status
   */
  getStatus() {
    return {
      agents_count: Object.keys(this.registry.agents || {}).length,
      shares_count: Object.keys(this.registry.shares || {}).length,
      total_lines: existsSync(this.sharesFile)
        ? readFileSync(this.sharesFile, 'utf-8').split('\n').filter(Boolean).length
        : 0
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
export function cmdMultiAgentShare(command, args) {
  const manager = new ShareManager();

  switch (command) {
    case 'register': {
      if (!args.agentId) return { error: '请提供 --agent-id' };
      const result = manager.registerAgent(args.agentId, args.agentName || args.agentId);
      return { type: 'text', text: `✅ Agent已注册: ${args.agentId}` };
    }

    case 'share': {
      if (!args.text && !args.memoryId) return { error: '请提供 --text 或 --memory-id' };
      const targets = args.target ? args.target.split(',') : [];
      const result = manager.shareMemory(args.memoryId || `mem_${Date.now()}`, args.text, targets);
      return { type: 'text', text: `✅ 已共享: [${result.share_id}]` };
    }

    case 'pull': {
      const agentId = args.agentId || process.env.OPENCLAW_AGENT_ID || 'unknown';
      const shares = manager.getShares(agentId, parseInt(args.limit) || 20);
      if (args.json) return { type: 'json', data: shares };
      const lines = [`📥 共享记忆 (${shares.length} 条):`];
      shares.slice(0, 10).forEach(s => lines.push(`   [${s.id}] ${s.text.slice(0, 60)}...`));
      return { type: 'text', text: lines.join('\n') };
    }

    case 'subscribe': {
      if (!args.targetAgentId) return { error: '请提供 --target-agent-id' };
      const agentId = args.agentId || process.env.OPENCLAW_AGENT_ID || 'unknown';
      const result = manager.subscribe(agentId, args.targetAgentId);
      return { type: 'text', text: `✅ 已订阅: ${args.targetAgentId}` };
    }

    case 'status': {
      const status = manager.getStatus();
      return {
        type: 'text',
        text: `📊 多Agent共享状态\n   注册Agent: ${status.agents_count}\n   共享总数: ${status.shares_count}`
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

export default { ShareManager, cmdMultiAgentShare };
