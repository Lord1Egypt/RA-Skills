/**
 * Active Learner - 主动学习钩子
 * Ported from Python active_learner.py
 * 
 * 在每次重要交互后自动：
 * 1. 提取关键信息存入 unified-memory
 * 2. 推送到 OpenClaw 索引
 * 3. 保持记忆新鲜度
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { extractImportantInfo } from '../tools/autostore.js';
import { addMemory, getAllMemories, saveMemories } from '../storage.js';
import { config } from '../config.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const JSON_FILE = join(MEMORY_DIR, 'active_memories.json');

// Ensure memory dir exists
if (!existsSync(MEMORY_DIR)) {
  mkdirSync(MEMORY_DIR, { recursive: true });
}

/**
 * ActiveLearner - 主动学习器
 */
export class ActiveLearner {
  constructor() {
    /** @type {Array<object>} */
    this.memories = [];
    this._load();
  }

  _load() {
    if (existsSync(JSON_FILE)) {
      try {
        this.memories = JSON.parse(readFileSync(JSON_FILE, 'utf8'));
      } catch {
        this.memories = [];
      }
    }
  }

  _save() {
    writeFileSync(JSON_FILE, JSON.stringify(this.memories, null, 2), 'utf8');
  }

  /**
   * 从文本中主动学习
   * @param {string} text - 要学习的文本
   * @param {object} [metadata] - 元数据
   * @returns {Promise<object|null>} 提取的记忆条目，如果没有新信息则返回 null
   */
  async learn(text, metadata = null) {
    const extractions = [];

    // 1. 项目/工具名 (贪婪匹配)
    const toolMatches = text.match(/(?:使用|安装|提到|关于)\s+([A-Za-z0-9\-]+)/g) || [];
    const tools = [...new Set(toolMatches.map(m => m.replace(/^(?:使用|安装|提到|关于)\s+/, '')))];
    for (const tool of tools) {
      if (tool.length > 2 && !['the', 'and', 'for', 'with'].includes(tool.toLowerCase())) {
        extractions.push(`工具相关: ${tool}`);
      }
    }

    // 2. 偏好模式: "喜欢X" / "不喜欢X"
    const likes = text.match(/喜欢\s*([^\s，,。！？]+)/g) || [];
    for (const like of likes) {
      extractions.push(`偏好(喜欢): ${like.replace(/喜欢\s*/, '')}`);
    }

    const dislikes = text.match(/不喜欢\s*([^\s，,。！？]+)/g) || [];
    for (const dislike of dislikes) {
      extractions.push(`偏好(不喜欢): ${dislike.replace(/不喜欢\s*/, '')}`);
    }

    // 3. 任务模式: "要X" / "想做X" / "需要X"
    const taskMatches = text.match(/(?:要|想做|需要|想完成|计划)\s*([^\s，,。！？]{2,20})/g) || [];
    for (const task of taskMatches) {
      extractions.push(`任务: ${task.replace(/^(?:要|想做|需要|想完成|计划)\s*/, '')}`);
    }

    // 4. 人名/称呼
    const nameMatches = text.match(/([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*(?:说|告诉|表示|提到)/g) || [];
    for (const name of nameMatches) {
      const cleanName = name.replace(/(?:说|告诉|表示|提到)/, '').trim();
      if (!['The', 'This', 'That'].includes(cleanName.split(' ')[0])) {
        extractions.push(`人物: ${cleanName}`);
      }
    }

    // 5. 时间敏感信息
    const timePatterns = [
      [/今天\s*([^\s，,。！？]+)/, '今天'],
      [/明天\s*([^\s，,。！？]+)/, '明天'],
      [/这周\s*([^\s，,。！？]+)/, '这周'],
      [/下周\s*([^\s，,。！？]+)/, '下周'],
    ];
    for (const [pattern, timeWord] of timePatterns) {
      const matches = text.match(pattern) || [];
      for (const match of matches) {
        const content = match.replace(pattern, '$1');
        extractions.push(`[${timeWord}] ${content}`);
      }
    }

    // 6. 决策/结论
    const decisionMatches = text.match(/(?:决定|结论|结果|因此|所以)\s*([^\s，,。！？]{5,50})/g) || [];
    for (const decision of decisionMatches) {
      extractions.push(`决策: ${decision.replace(/^(?:决定|结论|结果|因此|所以)\s*/, '')}`);
    }

    // 7. 问题/错误
    const errorMatches = text.match(/(?:错误|失败|问题|bug|error)\s*[:：]?\s*([^\s，,。！？]+)/gi) || [];
    for (const error of errorMatches) {
      extractions.push(`问题: ${error.replace(/(?:错误|失败|问题|bug|error)\s*[:：]?\s*/, '')}`);
    }

    // 8. 使用 autostore 的 extractImportantInfo
    try {
      const autoExtracted = extractImportantInfo(text);
      for (const item of autoExtracted) {
        if (item.text && item.text.length > 3) {
          extractions.push(`[${item.category}] ${item.text}`);
        }
      }
    } catch {
      // ignore autostore extraction errors
    }

    if (extractions.length === 0) {
      return null;
    }

    // 去重：检查是否已有相似的记忆
    const combined = extractions.join('; ');
    for (const existing of this.memories) {
      const existingContent = existing.content || '';
      if (combined.slice(0, 30) && combined.slice(0, 30).includes(existingContent.slice(0, 30)) && existingContent.length > 0) {
        // 太相似，跳过
        return null;
      }
    }

    // 创建新记忆
    const memoryId = `al_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    /** @type {object} */
    const memoryEntry = {
      id: memoryId,
      content: `[主动学习] ${combined}`,
      timestamp: new Date().toISOString(),
      metadata: {
        ...(metadata || {}),
        auto: true,
        source: 'active_learner',
        extractions: extractions.length
      }
    };

    this.memories.push(memoryEntry);
    this._save();

    // 同时存入主记忆系统
    try {
      addMemory({
        text: `[主动学习] ${combined}`,
        category: 'active_learning',
        importance: 0.5,
        tags: ['auto', 'active-learner']
      });
    } catch {
      // ignore if main storage fails
    }

    return memoryEntry;
  }

  /**
   * 检查记忆新鲜度
   * @returns {object[]} 需要更新的记忆列表
   */
  checkFreshness() {
    const now = new Date();
    const threshold = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000); // 7天前
    const needsUpdate = [];

    for (const m of this.memories) {
      const meta = m.metadata || {};
      if (meta.auto) {
        try {
          const ts = m.timestamp || '';
          if (ts) {
            const dt = new Date(ts);
            if (dt < threshold) {
              needsUpdate.push(m);
            }
          }
        } catch {
          /* ignore */
        }
      }
    }

    return needsUpdate;
  }

  /**
   * 刷新记忆 - 更新timestamp，或更新内容
   * @param {string} memoryId
   * @param {string} [newContent]
   * @returns {boolean} 是否成功
   */
  refreshMemory(memoryId, newContent = null) {
    for (const m of this.memories) {
      if (m.id === memoryId) {
        m.timestamp = new Date().toISOString();
        if (newContent) {
          m.content = newContent;
        }
        this._save();
        return true;
      }
    }
    return false;
  }

  /**
   * 获取最近记忆
   * @param {number} [limit=10]
   * @returns {object[]}
   */
  getRecent(limit = 10) {
    const sorted = [...this.memories].sort((a, b) => {
      const tsA = a.timestamp || '';
      const tsB = b.timestamp || '';
      return tsB.localeCompare(tsA);
    });
    return sorted.slice(0, limit);
  }
}

/**
 * CLI entry
 */
export async function cmdActiveLearner(args) {
  const { command, text, id, content, limit = 10 } = args;
  const learner = new ActiveLearner();

  if (command === 'learn') {
    if (!text) {
      console.log('❌ 请提供要学习的文本');
      return;
    }

    const result = await learner.learn(text);
    if (result) {
      console.log('✅ 主动学习成功:');
      console.log(`   ID: ${result.id}`);
      console.log(`   内容: ${result.content.slice(0, 80)}...`);
      console.log(`   提取项: ${result.metadata.extractions}`);
    } else {
      console.log('⚠️ 未提取到新信息（可能与已有记忆重复）');
    }
  } else if (command === 'check') {
    const needsUpdate = learner.checkFreshness();
    console.log(`📋 需要更新的记忆: ${needsUpdate.length} 条`);
    for (const m of needsUpdate.slice(0, 5)) {
      console.log(`   - ${m.content.slice(0, 50)}... (ID: ${m.id.slice(0, 8)})`);
    }
  } else if (command === 'refresh') {
    if (!id) {
      console.log('❌ 请提供记忆ID (--id)');
      return;
    }

    const success = learner.refreshMemory(id, content);
    if (success) {
      console.log(`✅ 记忆已刷新: ${id.slice(0, 8)}`);
    } else {
      console.log(`❌ 未找到记忆: ${id}`);
    }
  } else if (command === 'recent') {
    const recent = learner.getRecent(limit);
    console.log(`📝 最近 ${recent.length} 条记忆:\n`);
    for (let i = 0; i < recent.length; i++) {
      const m = recent[i];
      const ts = (m.timestamp || '').slice(0, 19);
      const content = (m.content || '').slice(0, 60);
      const meta = m.metadata || {};
      const autoTag = meta.auto ? '[A]' : '';
      console.log(`${i + 1}. ${autoTag} [${ts}] ${content}...`);
    }
  }
}

// CLI runner
const args = process.argv.slice(2);
if (args.length > 0 && !process.argv[1]?.includes('esm') && require.main === module) {
  const [command, text, extra] = args;
  cmdActiveLearner({ command, text, ...extra });
}
