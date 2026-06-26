/**
 * confidence.js - 置信度验证器 v2.0
 * 
 * 功能:
 * - 检测过时记忆 (超过 N 天未验证)
 * - 检测矛盾记忆 (与其他记忆冲突)
 * - 标记可疑记忆，使用前需确认
 * 
 * 使用 config.ollamaUrl 和 storage.js
 */

import { getAllMemories, saveMemories } from '../storage.js';
import { config, log } from '../utils/logger.js';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { defaultDiet } from '../tools/decay.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VALIDATION_DIR = join(MEMORY_DIR, 'validation');

// 验证参数
const STALE_DAYS = 30;           // 超过 30 天未验证视为可能过时
const CONFLICT_THRESHOLD = 0.7;  // 矛盾检测阈值

// 文件路径
const VALIDATION_STATE_FILE = join(VALIDATION_DIR, 'validation_state.json');
const CONFLICTS_FILE = join(VALIDATION_DIR, 'conflicts.json');

// 确保目录存在
if (!existsSync(VALIDATION_DIR)) {
  mkdirSync(VALIDATION_DIR, { recursive: true });
}

// ============================================================
// 置信度常量
// ============================================================

export const CONFIDENCE_VERIFIED = '✅ 已验证';      // 多次确认正确
export const CONFIDENCE_STALE = '⚠️ 可能过时';      // 超过 N 天未更新
export const CONFIDENCE_CONFLICT = '❌ 矛盾';        // 与其他记忆冲突
export const CONFIDENCE_PENDING = '🔄 待更新';       // 用户行为已改变

// ============================================================
// 状态加载/保存
// ============================================================

/** @type {Map<string, object>} */
let validationState = {};
/** @type {Array<object>} */
let conflicts = [];

function loadValidationState() {
  try {
    if (existsSync(VALIDATION_STATE_FILE)) {
      validationState = JSON.parse(readFileSync(VALIDATION_STATE_FILE, 'utf8'));
    }
    if (existsSync(CONFLICTS_FILE)) {
      conflicts = JSON.parse(readFileSync(CONFLICTS_FILE, 'utf8'));
    }
  } catch (e) {
    log('WARN', '加载验证状态失败:', e.message);
  }
}

function saveValidationState() {
  try {
    writeFileSync(VALIDATION_STATE_FILE, JSON.stringify(validationState, null, 2), 'utf8');
    writeFileSync(CONFLICTS_FILE, JSON.stringify(conflicts, null, 2), 'utf8');
  } catch (e) {
    log('WARN', '保存验证状态失败:', e.message);
  }
}

// ============================================================
// 置信度验证器
// ============================================================

export class ConfidenceValidator {
  constructor() {
    loadValidationState();
  }

  /**
   * 扫描过时记忆
   * @param {Array<object>} [memories] - 可选，默认从 storage 加载
   * @returns {Array<object>}
   */
  scanStale(memories) {
    const stale = [];
    const now = new Date();

    if (!memories) {
      memories = getAllMemories();
    }

    for (const mem of memories) {
      const memId = mem.id;
      const createdAt = mem.created_at || mem.timestamp;

      if (!createdAt) continue;

      try {
        const memTime = new Date(createdAt);
        if (isNaN(memTime.getTime())) continue;

        const ageMs = now.getTime() - memTime.getTime();
        const ageDays = Math.floor(ageMs / (1000 * 60 * 60 * 24));

        if (ageDays > STALE_DAYS) {
          const valInfo = validationState[memId] || {};
          const lastValidated = valInfo.last_validated;

          if (lastValidated) {
            const lastValTime = new Date(lastValidated);
            if (!isNaN(lastValTime.getTime())) {
              const daysSinceValidation = Math.floor(
                (now.getTime() - lastValTime.getTime()) / (1000 * 60 * 60 * 24)
              );
              if (daysSinceValidation < STALE_DAYS) {
                continue; // 最近已验证
              }
            }
          }

          stale.push({
            id: memId,
            text: (mem.text || mem.content || '').slice(0, 100),
            age_days: ageDays,
            confidence: CONFIDENCE_STALE,
            last_validated: valInfo.last_validated
          });
        }
      } catch (e) {
        // skip
      }
    }

    return stale;
  }

  /**
   * 检测矛盾记忆
   * @param {Array<object>} [memories] - 可选，默认从 storage 加载
   * @returns {Array<object>}
   */
  detectConflicts(memories) {
    if (!memories) {
      memories = getAllMemories();
    }

    const newConflicts = [];
    const byTopic = new Map();

    // 按主题关键词分组
    for (const mem of memories) {
      const text = (mem.text || mem.content || '').toLowerCase();
      // 提取中文关键词 (2-4字)
      const keywords = text.match(/[\u4e00-\u9fa5]{2,4}/g) || [];
      for (const kw of keywords.slice(0, 2)) {
        if (!byTopic.has(kw)) {
          byTopic.set(kw, []);
        }
        byTopic.get(kw).push(mem);
      }
    }

    // 检测否定/肯定矛盾
    const negationWords = ['不', '没', '无', '非', '不是', '没有'];

    for (const [topic, mems] of byTopic) {
      if (mems.length < 2) continue;

      const positive = [];
      const negative = [];

      for (const mem of mems) {
        const text = (mem.text || mem.content || '').toLowerCase();
        const hasNegation = negationWords.some(neg => text.includes(neg));
        if (hasNegation) {
          negative.push(mem);
        } else {
          positive.push(mem);
        }
      }

      // 同时存在肯定和否定 → 可能矛盾
      if (positive.length > 0 && negative.length > 0) {
        const conflict = {
          topic,
          positive: positive.slice(0, 2).map(m => ({
            id: m.id,
            text: (m.text || m.content || '').slice(0, 50)
          })),
          negative: negative.slice(0, 2).map(m => ({
            id: m.id,
            text: (m.text || m.content || '').slice(0, 50)
          })),
          detected_at: new Date().toISOString()
        };
        newConflicts.push(conflict);

        // 更新记忆置信度
        for (const mem of [...positive, ...negative]) {
          if (!mem.id) continue;
          validationState[mem.id] = {
            ...validationState[mem.id],
            confidence: CONFIDENCE_CONFLICT,
            conflict_with: [...positive, ...negative]
              .filter(m => m.id !== mem.id)
              .map(m => m.id),
            last_checked: new Date().toISOString()
          };
        }
      }
    }

    conflicts.push(...newConflicts);
    saveValidationState();

    return newConflicts;
  }

  /**
   * 验证记忆
   * @param {string} memoryId
   * @param {boolean} [isCorrect=true]
   * @param {string} [note]
   */
  validate(memoryId, isCorrect = true, note = null) {
    validationState[memoryId] = {
      confidence: isCorrect ? CONFIDENCE_VERIFIED : CONFIDENCE_PENDING,
      last_validated: new Date().toISOString(),
      validation_note: note
    };
    saveValidationState();
  }

  /**
   * 获取记忆置信度
   * @param {string} memoryId
   * @returns {string}
   */
  getConfidence(memoryId) {
    if (validationState[memoryId]) {
      return validationState[memoryId].confidence || CONFIDENCE_VERIFIED;
    }
    return CONFIDENCE_VERIFIED; // 默认已验证
  }

  /**
   * 标记需要更新
   * @param {string} memoryId
   * @param {string} [reason]
   */
  markNeedsUpdate(memoryId, reason = null) {
    validationState[memoryId] = {
      ...validationState[memoryId],
      confidence: CONFIDENCE_PENDING,
      needs_update: true,
      reason,
      marked_at: new Date().toISOString()
    };
    saveValidationState();
  }

  /**
   * 获取统计
   * @returns {object}
   */
  stats() {
    /** @type {Map<string, number>} */
    const byConfidence = new Map();
    for (const val of Object.values(validationState)) {
      const conf = val.confidence || CONFIDENCE_VERIFIED;
      byConfidence.set(conf, (byConfidence.get(conf) || 0) + 1);
    }

    return {
      total_validated: Object.keys(validationState).length,
      conflicts_detected: conflicts.length,
      by_confidence: Object.fromEntries(byConfidence),
      recent_conflicts: conflicts.slice(-3)
    };
  }

  /**
   * 更新单条记忆的置信度标记
   * @param {string} memoryId
   * @param {string} status - 'verified' | 'stale' | 'conflict' | 'pending'
   */
  updateMemoryStatus(memoryId, status) {
    const confidenceMap = {
      verified: CONFIDENCE_VERIFIED,
      stale: CONFIDENCE_STALE,
      conflict: CONFIDENCE_CONFLICT,
      pending: CONFIDENCE_PENDING
    };
    const confidence = confidenceMap[status] || CONFIDENCE_VERIFIED;
    
    validationState[memoryId] = {
      ...validationState[memoryId],
      confidence,
      last_checked: new Date().toISOString()
    };
    saveValidationState();
  }
}

// ============================================================
// CLI 命令
// ============================================================

/**
 * CLI: 扫描过时记忆
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdScan(args) {
  const validator = new ConfidenceValidator();
  const memories = getAllMemories();
  const stale = validator.scanStale(memories);
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        message: `发现 ${stale.length} 条可能过时的记忆`,
        stale: stale.slice(0, 10)
      }, null, 2)
    }]
  };
}

/**
 * CLI: 验证记忆
 * @param {object} args - { memoryId, isCorrect, note }
 * @returns {Promise<object>}
 */
export async function cmdValidate(args) {
  const { memoryId, isCorrect = true, note } = args;
  
  if (!memoryId) {
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({ error: '请指定 memoryId' }, null, 2)
      }]
    };
  }
  
  const validator = new ConfidenceValidator();
  validator.validate(memoryId, isCorrect, note);
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        message: `已验证: ${memoryId}`,
        confidence: validator.getConfidence(memoryId)
      }, null, 2)
    }]
  };
}

/**
 * CLI: 检测矛盾
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdConflict(args) {
  const validator = new ConfidenceValidator();
  const memories = getAllMemories();
  const detected = validator.detectConflicts(memories);
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify({
        message: `发现 ${detected.length} 个矛盾`,
        conflicts: detected.slice(0, 5)
      }, null, 2)
    }]
  };
}

/**
 * CLI: 统计
 * @param {object} args
 * @returns {Promise<object>}
 */
export async function cmdStats(args) {
  const validator = new ConfidenceValidator();
  const stats = validator.stats();
  
  return {
    content: [{
      type: 'text',
      text: JSON.stringify(stats, null, 2)
    }]
  };
}

// 默认导出
export default new ConfidenceValidator();
