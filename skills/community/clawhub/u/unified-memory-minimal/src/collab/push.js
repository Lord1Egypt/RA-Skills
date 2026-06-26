/**
 * Memory Push - 智能推送和提醒系统 v1.0
 * 
 * 核心功能:
 * - 项目截止日期提醒
 * - 关联记忆更新通知
 * - 矛盾记忆检测提醒
 * - 新关联发现通知
 * 
 * Ported from memory_push.py
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, appendFileSync, statSync } from 'fs';
import { join, dirname } from 'path';
import { createHash } from 'crypto';
import { homedir } from 'os';

const HOME = homedir();
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const PUSH_DIR = join(MEMORY_DIR, 'push_queue');

// Ensure directories exist
try { mkdirSync(PUSH_DIR, { recursive: true }); } catch {}

// ============================================================
// Configuration
// ============================================================

const OLLAMA_URL = process.env.OLLAMA_HOST || 'http://localhost:11434';
const OLLAMA_EMBED_MODEL = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text:latest';
const OLLAMA_LLM_MODEL = process.env.OLLAMA_LLM_MODEL || 'deepseek-v3.2:cloud';

const PUSH_RULES = {
  project_deadline: {
    advance_days: 3,
    check_interval: 'daily',
    priority: 'high',
    template: '📅 项目截止提醒: {project_name} 将在 {days_left} 天后截止 ({deadline})',
  },
  memory_update: {
    notify_related: true,
    related_threshold: 0.8,
    priority: 'medium',
    template: '🔄 关联记忆更新: {related_topic} 有新信息 - {summary}',
  },
  conflict_detected: {
    require_confirm: true,
    auto_resolve: false,
    priority: 'high',
    template: '⚠️ 矛盾记忆检测: {conflict_desc} - 请确认正确信息',
  },
  new_related: {
    notify: true,
    min_similarity: 0.85,
    priority: 'low',
    template: '🔗 发现新关联: {entity_a} 与 {entity_b} 相似度 {similarity}',
  },
};

// ============================================================
// Push Message
// ============================================================

export class PushMessage {
  constructor(msgType, title, content, priority = 'medium', metadata = {}) {
    this.id = this._generateId(msgType, content);
    this.type = msgType;
    this.title = title;
    this.content = content;
    this.priority = priority;
    this.metadata = metadata;
    this.created = new Date().toISOString();
    this.read = false;
    this.readAt = null;
  }

  _generateId(msgType, content) {
    const hashInput = `${msgType}:${content}`;
    return createHash('md5').update(hashInput).digest('hex').slice(0, 12);
  }

  toJSON() {
    return {
      id: this.id,
      type: this.type,
      title: this.title,
      content: this.content,
      priority: this.priority,
      metadata: this.metadata,
      created: this.created,
      read: this.read,
      read_at: this.readAt,
    };
  }

  static fromJSON(data) {
    const msg = new PushMessage(
      data.type,
      data.title,
      data.content,
      data.priority || 'medium',
      data.metadata || {}
    );
    msg.id = data.id;
    msg.created = data.created;
    msg.read = data.read || false;
    msg.readAt = data.read_at || null;
    return msg;
  }

  toString() {
    const status = this.read ? '✅' : '🔔';
    const priorityIcons = { high: '🔴', medium: '🟡', low: '🟢' };
    const icon = priorityIcons[this.priority] || '⚪';
    return `${status} ${icon} [${this.id}] ${this.title}: ${this.content}`;
  }
}

// ============================================================
// Push State
// ============================================================

export class PushState {
  constructor() {
    this.stateFile = join(PUSH_DIR, 'push_state.json');
    /** @type {Map<string, PushMessage>} */
    this.messages = new Map();
    /** @type {Map<string, string>} */
    this.lastCheck = new Map();
    this._load();
  }

  _load() {
    if (!existsSync(this.stateFile)) return;
    try {
      const content = readFileSync(this.stateFile, 'utf-8');
      const data = JSON.parse(content);
      for (const msgData of data.messages || []) {
        const msg = PushMessage.fromJSON(msgData);
        this.messages.set(msg.id, msg);
      }
      for (const [k, v] of Object.entries(data.last_check || {})) {
        this.lastCheck.set(k, v);
      }
    } catch (e) {
      console.warn(`⚠️ 加载推送状态失败: ${e.message}`);
    }
  }

  _save() {
    try {
      const data = {
        messages: [...this.messages.values()].map(m => m.toJSON()),
        last_check: Object.fromEntries(this.lastCheck),
      };
      writeFileSync(this.stateFile, JSON.stringify(data, null, 2), 'utf-8');
    } catch (e) {
      console.warn(`⚠️ 保存推送状态失败: ${e.message}`);
    }
  }

  addMessage(msg) {
    if (this.messages.has(msg.id)) {
      return false; // Duplicate
    }
    this.messages.set(msg.id, msg);
    this._save();
    return true;
  }

  markRead(msgId) {
    const msg = this.messages.get(msgId);
    if (msg) {
      msg.read = true;
      msg.readAt = new Date().toISOString();
      this._save();
      return true;
    }
    return false;
  }

  getUnread() {
    return [...this.messages.values()].filter(m => !m.read);
  }

  getAll(limit = 50) {
    const sorted = [...this.messages.values()].sort(
      (a, b) => new Date(b.created) - new Date(a.created)
    );
    return sorted.slice(0, limit);
  }

  cleanupOld(days = 30) {
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - days);
    let count = 0;

    for (const [id, msg] of this.messages) {
      if (msg.read && new Date(msg.created) < cutoff) {
        this.messages.delete(id);
        count++;
      }
    }

    if (count > 0) this._save();
    return count;
  }

  updateLastCheck(checkType) {
    this.lastCheck.set(checkType, new Date().toISOString());
    this._save();
  }

  shouldCheck(checkType, intervalHours = 24) {
    if (!this.lastCheck.has(checkType)) return true;
    const last = new Date(this.lastCheck.get(checkType));
    const now = new Date();
    const diffHours = (now - last) / (1000 * 60 * 60);
    return diffHours >= intervalHours;
  }
}

// ============================================================
// Utilities
// ============================================================

/**
 * Get embedding from Ollama
 * @param {string} text
 * @returns {Promise<number[]|null>}
 */
export async function getEmbedding(text) {
  try {
    const response = await fetch(`${OLLAMA_URL}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model: OLLAMA_EMBED_MODEL, prompt: text }),
      signal: AbortSignal.timeout(30000),
    });
    if (response.ok) {
      const data = await response.json();
      return data.embedding || null;
    }
  } catch (e) {
    console.warn(`⚠️ Embedding 失败: ${e.message}`);
  }
  return null;
}

/**
 * Calculate cosine similarity
 * @param {number[]} vecA
 * @param {number[]} vecB
 * @returns {number}
 */
export function cosineSimilarity(vecA, vecB) {
  if (!vecA || !vecB || vecA.length !== vecB.length) return 0.0;

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < vecA.length; i++) {
    dotProduct += vecA[i] * vecB[i];
    normA += vecA[i] * vecA[i];
    normB += vecB[i] * vecB[i];
  }

  const dA = Math.sqrt(normA);
  const dB = Math.sqrt(normB);

  if (dA === 0 || dB === 0) return 0.0;
  return dotProduct / (dA * dB);
}

/**
 * Call LLM
 * @param {string} prompt
 * @param {string} model
 * @returns {Promise<string|null>}
 */
export async function callLLM(prompt, model = null) {
  const modelToUse = model || OLLAMA_LLM_MODEL;
  try {
    const response = await fetch(`${OLLAMA_URL}/api/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        model: modelToUse,
        prompt,
        stream: false,
        options: { temperature: 0.1 },
      }),
      signal: AbortSignal.timeout(60000),
    });
    if (response.ok) {
      const data = await response.json();
      return data.response || '';
    }
  } catch (e) {
    console.warn(`⚠️ LLM 调用失败: ${e.message}`);
  }
  return null;
}

/**
 * Call LLM and parse JSON
 * @param {string} prompt
 * @param {string} model
 * @returns {Promise<Object|null>}
 */
export async function callLLMJSON(prompt, model = null) {
  const response = await callLLM(prompt, model);
  if (!response) return null;

  // Try to extract JSON
  try {
    return JSON.parse(response);
  } catch {}

  // Try to extract from markdown code block
  const match = response.match(/```(?:json)?\s*([\s\S]*?)```/);
  if (match) {
    try {
      return JSON.parse(match[1]);
    } catch {}
  }

  return null;
}

// ============================================================
// Memory Loading
// ============================================================

/**
 * Load all memories from markdown files
 * @returns {Object[]}
 */
export function loadAllMemories() {
  const memories = [];
  const memoryFile = join(MEMORY_DIR, 'memories.json');

  // Try JSON first
  if (existsSync(memoryFile)) {
    try {
      const content = readFileSync(memoryFile, 'utf-8');
      const data = JSON.parse(content);
      if (Array.isArray(data)) {
        return data;
      }
      if (data.memories) {
        return data.memories;
      }
    } catch {}
  }

  // Parse markdown files
  const { readdirSync } = require('fs');
  const { extname, basename } = require('path');

  try {
    const files = readdirSync(MEMORY_DIR).filter(f => extname(f) === '.md');
    for (const file of files.sort().reverse()) {
      const filePath = join(MEMORY_DIR, file);
      const content = readFileSync(filePath, 'utf-8');
      const lines = content.split('\n');

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith('-')) continue;

        // Parse format: - [timestamp] [category] [scope] [I=importance] text
        const match = trimmed.match(
          /^- \[([^\]]+)\] \[([^\]]+)\] \[([^\]]+)\](?: \[I=([^\]]+)\])? (.+)/
        );
        if (match) {
          const [, timestampStr, category, scope, importanceStr, text] = match;
          try {
            const timestamp = new Date(timestampStr.replace(/\//g, '-'));
            const importance = importanceStr ? parseFloat(importanceStr) : 0.5;
            memories.push({
              text,
              timestamp,
              category,
              scope,
              importance,
              file: basename(file),
            });
          } catch {}
        }
      }
    }
  } catch {}

  return memories;
}

/**
 * Load ontology graph
 * @returns {{entities: Map, relations: Object[]}}
 */
export function loadOntologyGraph() {
  const entities = new Map();
  const relations = [];
  const graphFile = join(MEMORY_DIR, 'ontology', 'graph.jsonl');

  if (!existsSync(graphFile)) {
    return { entities, relations };
  }

  try {
    const content = readFileSync(graphFile, 'utf-8');
    const lines = content.split('\n').filter(Boolean);

    for (const line of lines) {
      try {
        const data = JSON.parse(line);
        if (data.op === 'create') {
          const entity = data.entity || {};
          entities.set(entity.id, entity);
        } else if (data.op === 'relate') {
          relations.push({
            from: data.from,
            rel: data.rel,
            to: data.to,
            created: data.created,
          });
        }
      } catch {}
    }
  } catch {}

  return { entities, relations };
}

// ============================================================
// Memory Pusher
// ============================================================

export class MemoryPusher {
  constructor(silent = false) {
    this.state = new PushState();
    this.silent = silent;
    /** @type {PushMessage[]} */
    this.newNotifications = [];
  }

  checkAndPush() {
    this.newNotifications = [];

    // 1. Project deadline check
    if (this.state.shouldCheck('deadline', 24)) {
      const deadlines = this._checkDeadlines();
      this.newNotifications.push(...deadlines);
      this.state.updateLastCheck('deadline');
    }

    // 2. Related memory update check
    if (this.state.shouldCheck('related_updates', 12)) {
      const related = this._checkRelatedUpdates();
      this.newNotifications.push(...related);
      this.state.updateLastCheck('related_updates');
    }

    // 3. Conflict detection check
    if (this.state.shouldCheck('conflicts', 48)) {
      const conflicts = this._checkConflicts();
      this.newNotifications.push(...conflicts);
      this.state.updateLastCheck('conflicts');
    }

    // 4. New relation discovery
    if (this.state.shouldCheck('new_related', 24)) {
      const newRelated = this._checkNewRelated();
      this.newNotifications.push(...newRelated);
      this.state.updateLastCheck('new_related');
    }

    // Add to state
    for (const msg of this.newNotifications) {
      this.state.addMessage(msg);
    }

    return this.newNotifications;
  }

  _checkDeadlines() {
    const messages = [];
    const rule = PUSH_RULES.project_deadline;
    const advanceDays = rule.advance_days;

    const memories = loadAllMemories();

    // Deadline patterns
    const deadlinePatterns = [
      /项目[：:]\s*(.+?)(?:截止|deadline|完成|$)/,
      /截止[日期]*[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})/,
      /deadline[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})/,
      /(\d{4}[-/]\d{1,2}[-/]\d{1,2})\s*(?:截止|完成|交付)/,
    ];

    const projects = new Map();

    for (const mem of memories) {
      const text = mem.text || '';

      if (text.includes('项目') || text.includes('deadline') || text.includes('截止')) {
        for (const pattern of deadlinePatterns) {
          const match = text.match(pattern);
          if (match) {
            try {
              const dateStr = match[1].replace(/\//g, '-');
              const deadline = new Date(dateStr);
              if (!isNaN(deadline.getTime())) {
                const projectMatch = text.match(/项目[：:]\s*(.+?)(?:\s|$|，|。)/);
                const projectName = projectMatch ? projectMatch[1] : dateStr;
                projects.set(projectName, deadline);
              }
            } catch {}
          }
        }
      }
    }

    // Check upcoming deadlines
    const today = new Date();
    today.setHours(0, 0, 0, 0);

    for (const [projectName, deadline] of projects) {
      const daysLeft = Math.ceil((deadline - today) / (1000 * 60 * 60 * 24));

      if (daysLeft > 0 && daysLeft <= advanceDays) {
        const content = rule.template
          .replace('{project_name}', projectName)
          .replace('{days_left}', String(daysLeft))
          .replace('{deadline}', deadline.toISOString().split('T')[0]);

        const msg = new PushMessage(
          'project_deadline',
          '项目截止提醒',
          content,
          rule.priority,
          {
            project_name: projectName,
            deadline: deadline.toISOString(),
            days_left: daysLeft,
          }
        );
        messages.push(msg);
      }
    }

    if (messages.length && !this.silent) {
      console.log(`📅 检查项目截止: 发现 ${messages.length} 个即将到期`);
    }

    return messages;
  }

  _checkRelatedUpdates() {
    const messages = [];
    const rule = PUSH_RULES.memory_update;
    const threshold = rule.related_threshold;

    // Get recent 24h memories
    const cutoff = new Date();
    cutoff.setHours(cutoff.getHours() - 24);
    const memories = loadAllMemories();
    const recentMemories = memories.filter(m => new Date(m.timestamp || m.created || 0) > cutoff);

    if (!recentMemories.length) return messages;

    // Load graph for entity relations
    const { entities } = loadOntologyGraph();

    for (const mem of recentMemories) {
      const text = mem.text || '';

      for (const [entityId, entity] of entities) {
        const props = entity.properties || {};
        const entityName = props.name || '';

        if (entityName && text.includes(entityName)) {
          const content = rule.template
            .replace('{related_topic}', entityName)
            .replace('{summary}', text.slice(0, 50) + '...');

          const msg = new PushMessage(
            'memory_update',
            '关联记忆更新',
            content,
            rule.priority,
            {
              entity_id: entityId,
              entity_name: entityName,
              memory_text: text,
            }
          );
          messages.push(msg);
          break; // One entity per memory
        }
      }
    }

    if (messages.length && !this.silent) {
      console.log(`🔄 检查关联更新: 发现 ${messages.length} 条相关更新`);
    }

    return messages;
  }

  _checkConflicts() {
    const messages = [];
    const rule = PUSH_RULES.conflict_detected;

    const memories = loadAllMemories();

    if (memories.length < 2) return messages;

    // Check recent 30 days high importance memories
    const cutoff = new Date();
    cutoff.setDate(cutoff.getDate() - 30);
    const recentMemories = memories.filter(
      m => (m.importance || 0.5) >= 0.7 && new Date(m.timestamp || m.created || 0) > cutoff
    );

    if (recentMemories.length < 2) return messages;

    // Use LLM to detect conflicts
    const memoryTexts = recentMemories.slice(0, 10).map((m, i) => `${i + 1}. ${m.text}`).join('\n');
    const prompt = `请分析以下记忆，找出可能存在的矛盾信息。返回JSON数组格式，每条矛盾包含description描述。

记忆列表：
${memoryTexts}

请返回JSON格式：
{
  "conflicts": [
    {"description": "矛盾1描述", "memory1_index": 0, "memory2_index": 1}
  ]
}`;

    callLLMJSON(prompt).then(result => {
      if (result && result.conflicts && Array.isArray(result.conflicts)) {
        for (const conflict of result.conflicts) {
          const content = rule.template.replace('{conflict_desc}', conflict.description);

          const msg = new PushMessage(
            'conflict_detected',
            '矛盾记忆检测',
            content,
            rule.priority,
            {
              description: conflict.description,
              memory_indices: [conflict.memory1_index, conflict.memory2_index],
            }
          );
          messages.push(msg);
        }
      }
    }).catch(() => {});

    return messages;
  }

  _checkNewRelated() {
    const messages = [];
    const rule = PUSH_RULES.new_related;
    const minSimilarity = rule.min_similarity;

    const { entities, relations } = loadOntologyGraph();

    if (entities.size < 2) return messages;

    // Get all pairs and check similarity
    const entityList = [...entities.values()];
    const existingPairs = new Set(relations.map(r => `${r.from}-${r.to}`));

    for (let i = 0; i < entityList.length; i++) {
      for (let j = i + 1; j < entityList.length; j++) {
        const entityA = entityList[i];
        const entityB = entityList[j];
        const pairKey = `${entityA.id}-${entityB.id}`;

        // Skip if already related
        if (existingPairs.has(pairKey)) continue;

        const nameA = (entityA.properties || {}).name || '';
        const nameB = (entityB.properties || {}).name || '';

        if (!nameA || !nameB) continue;

        // Simple name similarity
        const setA = new Set(nameA.toLowerCase().split(''));
        const setB = new Set(nameB.toLowerCase().split(''));
        const intersection = [...setA].filter(c => setB.has(c)).length;
        const union = new Set([...setA, ...setB]).size;
        const similarity = intersection / union;

        if (similarity >= minSimilarity) {
          const content = rule.template
            .replace('{entity_a}', nameA)
            .replace('{entity_b}', nameB)
            .replace('{similarity}', (similarity * 100).toFixed(0) + '%');

          const msg = new PushMessage(
            'new_related',
            '发现新关联',
            content,
            rule.priority,
            {
              entity_a: entityA.id,
              entity_b: entityB.id,
              similarity,
            }
          );
          messages.push(msg);
        }
      }
    }

    if (messages.length && !this.silent) {
      console.log(`🔗 检查新关联: 发现 ${messages.length} 个新关联`);
    }

    return messages;
  }
}

// ============================================================
// CLI Commands
// ============================================================

export async function cmdPush(command, args = {}) {
  const pusher = new MemoryPusher(args.silent);

  switch (command) {
    case 'check': {
      const notifications = pusher.checkAndPush();
      return {
        type: 'text',
        text: `检查完成，发现 ${notifications.length} 条新推送\n` +
          notifications.map(n => n.toString()).join('\n'),
      };
    }

    case 'list': {
      const messages = args.all
        ? pusher.state.getAll()
        : pusher.state.getUnread();
      return {
        type: 'text',
        text: messages.length
          ? messages.map(n => n.toString()).join('\n')
          : '暂无推送',
      };
    }

    case 'mark-read': {
      if (!args.id) return { error: '请提供消息ID' };
      const success = pusher.state.markRead(args.id);
      return {
        type: 'text',
        text: success ? `✅ 已标记 ID=${args.id} 为已读` : `❌ 未找到 ID=${args.id}`,
      };
    }

    case 'clear': {
      const count = pusher.state.cleanupOld(args.days || 30);
      return {
        type: 'text',
        text: `✅ 清理了 ${count} 条过期推送`,
      };
    }

    case 'status': {
      const state = pusher.state;
      const unread = state.getUnread();
      return {
        type: 'text',
        text: `📊 推送状态\n` +
          `   总消息: ${state.messages.size}\n` +
          `   未读: ${unread.length}\n` +
          `   最后检查:\n` +
          [...state.lastCheck.entries()]
            .map(([k, v]) => `     - ${k}: ${v}`)
            .join('\n'),
      };
    }

    default:
      return { error: `未知命令: ${command}` };
  }
}

// ============================================================
// Main
// ============================================================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'check';

  const pusher = new MemoryPusher();

  const result = await cmdPush(command, {
    silent: false,
    all: args.includes('--all'),
    id: args.find(a => a.startsWith('--id='))?.split('=')[1],
    days: parseInt(args.find(a => a.startsWith('--days='))?.split('=')[1] || '30'),
  });

  if (result.error) {
    console.error(`❌ ${result.error}`);
    process.exit(1);
  }

  console.log(result.text);
}

const isMain = process.argv[1]?.endsWith('push.js') || process.argv[1]?.endsWith('push.mjs');
if (isMain) {
  main().catch(console.error);
}

export default {
  PushMessage,
  PushState,
  MemoryPusher,
  cmdPush,
  getEmbedding,
  cosineSimilarity,
  callLLM,
  callLLMJSON,
  loadAllMemories,
  loadOntologyGraph,
};
