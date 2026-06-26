/**
 * Agent Collaboration - 多Agent协作日志
 * Ported from Python agent_collab.py
 * 
 * 功能:
 * - 记录Agent之间的协作历史
 * - 追踪任务分配和完成
 * - 支持协作统计分析
 */

import { existsSync, mkdirSync, readFileSync, appendFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createHash } from 'crypto';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const COLLAB_DIR = join(MEMORY_DIR, 'collaboration');
const COLLAB_LOG = join(COLLAB_DIR, 'collab_log.jsonl');
const AGENTS_FILE = join(COLLAB_DIR, 'agents.json');

// Ensure dirs
function ensureDirs() {
  if (!existsSync(COLLAB_DIR)) {
    mkdirSync(COLLAB_DIR, { recursive: true });
  }
  if (!existsSync(AGENTS_FILE)) {
    writeFileSync(AGENTS_FILE, JSON.stringify({ agents: ['main', 'assistant'] }, null, 2), 'utf8');
  }
}

/**
 * 记录协作日志
 * @param {string} fromAgent
 * @param {string} toAgent
 * @param {string} action
 * @param {string} content
 * @param {object} [metadata]
 * @returns {string} entry id
 */
export function logCollab(fromAgent, toAgent, action, content, metadata = null) {
  ensureDirs();

  const timestamp = new Date().toISOString();
  const hashInput = `${timestamp}${fromAgent}${toAgent}${action}`;
  const entryId = createHash('md5').update(hashInput).digest('hex').slice(0, 12);

  /** @type {object} */
  const entry = {
    id: entryId,
    timestamp,
    from_agent: fromAgent,
    to_agent: toAgent,
    action,
    content,
    metadata: metadata || {}
  };

  appendFileSync(COLLAB_LOG, JSON.stringify(entry, null, 0) + '\n', 'utf8');
  return entryId;
}

/**
 * 获取协作历史
 * @param {string} [agent]
 * @param {number} [limit=20]
 * @returns {object[]}
 */
export function getHistory(agent = null, limit = 20) {
  if (!existsSync(COLLAB_LOG)) {
    return [];
  }

  /** @type {object[]} */
  const entries = [];

  try {
    const lines = readFileSync(COLLAB_LOG, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      try {
        const entry = JSON.parse(trimmed);
        if (agent === null || entry.from_agent === agent || entry.to_agent === agent) {
          entries.push(entry);
        }
      } catch {
        continue;
      }
    }
  } catch {
    /* ignore */
  }

  return entries.slice(-limit);
}

/**
 * 获取协作统计
 * @returns {object}
 */
export function getStats() {
  /** @type {object} */
  const stats = {
    total: 0,
    by_agent: {},
    by_action: {},
    recent: []
  };

  if (!existsSync(COLLAB_LOG)) {
    return stats;
  }

  try {
    const lines = readFileSync(COLLAB_LOG, 'utf8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      try {
        const entry = JSON.parse(trimmed);
        stats.total++;

        // 按agent统计
        for (const agent of [entry.from_agent, entry.to_agent]) {
          if (!stats.by_agent[agent]) {
            stats.by_agent[agent] = 0;
          }
          stats.by_agent[agent]++;
        }

        // 按action统计
        const action = entry.action;
        if (!stats.by_action[action]) {
          stats.by_action[action] = 0;
        }
        stats.by_action[action]++;
      } catch {
        continue;
      }
    }
  } catch {
    /* ignore */
  }

  stats.recent = getHistory(null, 5);
  return stats;
}

/**
 * 注册Agent
 * @param {string} agentId
 * @param {object} [info]
 */
export function registerAgent(agentId, info = {}) {
  ensureDirs();
  /** @type {{agents: string[], info: object}} */
  let data = { agents: [], info: {} };
  
  if (existsSync(AGENTS_FILE)) {
    try {
      data = JSON.parse(readFileSync(AGENTS_FILE, 'utf8'));
    } catch {
      data = { agents: [], info: {} };
    }
  }

  if (!data.agents.includes(agentId)) {
    data.agents.push(agentId);
  }
  
  data.info[agentId] = { ...info, registered_at: new Date().toISOString() };
  writeFileSync(AGENTS_FILE, JSON.stringify(data, null, 2), 'utf8');
}

/**
 * 获取所有已注册Agent
 * @returns {string[]}
 */
export function getRegisteredAgents() {
  ensureDirs();
  if (!existsSync(AGENTS_FILE)) {
    return ['main', 'assistant'];
  }
  try {
    const data = JSON.parse(readFileSync(AGENTS_FILE, 'utf8'));
    return data.agents || ['main', 'assistant'];
  } catch {
    return ['main', 'assistant'];
  }
}

/**
 * 分享记忆给其他Agent
 * @param {string} fromAgent
 * @param {string} toAgent
 * @param {object} memory
 * @returns {string}
 */
export function shareMemory(fromAgent, toAgent, memory) {
  return logCollab(fromAgent, toAgent, 'share_memory', memory.text || memory.content || '', {
    memory_id: memory.id,
    category: memory.category,
    importance: memory.importance
  });
}

/**
 * 请求从其他Agent同步记忆
 * @param {string} fromAgent
 * @param {string} toAgent
 * @returns {string}
 */
export function requestSync(fromAgent, toAgent) {
  return logCollab(fromAgent, toAgent, 'sync_request', '', {});
}

/**
 * 清空协作日志
 */
export async function clearLog() {
  if (existsSync(COLLAB_LOG)) {
    const { unlinkSync } = await import('fs');
    unlinkSync(COLLAB_LOG);
    console.log('🗑️ 协作日志已清空');
  }
}

/**
 * AgentCollab - 多Agent协作管理器
 */
export class AgentCollab {
  constructor(agentId = 'agent') {
    this.agentId = agentId;
    ensureDirs();
    registerAgent(agentId, { type: 'agent' });
  }

  /**
   * 分享记忆给另一个Agent
   * @param {string} toAgent
   * @param {object} memory
   * @returns {string}
   */
  shareMemoryTo(toAgent, memory) {
    return shareMemory(this.agentId, toAgent, memory);
  }

  /**
   * 请求从另一个Agent同步
   * @param {string} fromAgent
   * @returns {string}
   */
  requestSyncFrom(fromAgent) {
    return requestSync(this.agentId, fromAgent);
  }

  /**
   * 获取与某个Agent的协作历史
   * @param {string} otherAgent
   * @param {number} [limit]
   * @returns {object[]}
   */
  getHistory(otherAgent = null, limit = 20) {
    return getHistory(otherAgent, limit);
  }

  /**
   * 获取协作统计
   * @returns {object}
   */
  getStats() {
    return getStats();
  }

  /**
   * 记录一个任务协作
   * @param {string} toAgent
   * @param {string} task
   * @param {string} [status='assigned']
   */
  logTaskHandoff(toAgent, task, status = 'assigned') {
    return logCollab(this.agentId, toAgent, `task_${status}`, task, {});
  }
}

/**
 * CLI entry
 */
export async function cmdAgentCollab(args) {
  const { command, fromAgent, toAgent, action, content, agent, limit = 20, json: jsonOutput } = args;

  if (command === 'log') {
    if (!fromAgent || !toAgent || !action) {
      console.log('❌ 缺少参数: --from, --to, --action');
      return;
    }
    const id = logCollab(fromAgent, toAgent, action, content || '');
    console.log(`📝 协作日志已记录: ${fromAgent} → ${toAgent} [${action}]`);
  } else if (command === 'history') {
    const history = getHistory(agent, limit);
    if (jsonOutput) {
      console.log(JSON.stringify(history, null, 2));
    } else {
      console.log(`📜 协作历史 (共 ${history.length} 条)`);
      for (const entry of history) {
        const ts = entry.timestamp.slice(0, 16);
        console.log(`  [${ts}] ${entry.from_agent} → ${entry.to_agent}: ${entry.action}`);
      }
    }
  } else if (command === 'stats') {
    const stats = getStats();
    if (jsonOutput) {
      console.log(JSON.stringify(stats, null, 2));
    } else {
      console.log('📊 协作统计');
      console.log(`   总计: ${stats.total} 次协作`);
      console.log(`   按Agent: ${JSON.stringify(stats.by_agent)}`);
      console.log(`   按动作: ${JSON.stringify(stats.by_action)}`);
    }
  } else if (command === 'clear') {
    if (existsSync(COLLAB_LOG)) {
      const { unlinkSync } = await import('fs');
      unlinkSync(COLLAB_LOG);
      console.log('🗑️ 协作日志已清空');
    }
  } else if (command === 'agents') {
    const agents = getRegisteredAgents();
    console.log('🤖 已注册Agents:');
    for (const a of agents) {
      console.log(`   - ${a}`);
    }
  }
}
