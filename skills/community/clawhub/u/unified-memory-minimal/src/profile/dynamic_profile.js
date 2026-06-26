/**
 * Dynamic Profile - 动态画像系统
 * 
 * 从最近 N 条记忆中提取动态画像，结合静态画像（persona.md）
 * 实现 SuperMemory 风格的 User Profile 抽象
 * 
 * 功能：
 * - static: 从 persona.md 读取长期稳定事实 + 偏好
 * - dynamic: 归纳最近活动（工作重点、关注点）
 * - 提供 `getProfile(userId)` 方法返回 `{ static, dynamic, lastUpdated }`
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { config } from '../config.js';
import { log } from '../logger.js';
import { search } from '../search.js';
import { getAllMemories } from '../storage.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ─── 默认配置 ──────────────────────────────────────────────────────────────
const DEFAULT_CONFIG = {
  recentMemoryLimit: 100,        // 最近 N 条记忆用于动态画像
  personaPath: null,              // persona.md 路径，默认自动检测
  staticCacheTimeout: 300000,    // 静态画像缓存 5 分钟
  dynamicUpdateInterval: 60000,  // 动态画像更新间隔 1 分钟
  recencyWindowDays: 7,          // 近期窗口（天）
  importanceThreshold: 0.6,      // 重要性阈值
};

// ─── 缓存 ──────────────────────────────────────────────────────────────────
const profileCache = new Map();

// ─── 工具函数 ────────────────────────────────────────────────────────────────

/**
 * 从 persona.md 读取静态画像
 */
function readPersona(personaPath) {
  const defaultPath = personaPath || join(config.memoryDir, 'persona.md');
  
  if (!existsSync(defaultPath)) {
    log('debug', '[dynamic_profile] persona.md not found, using empty static profile');
    return {
      facts: [],
      preferences: [],
      skills: [],
      goals: [],
    };
  }
  
  try {
    const content = readFileSync(defaultPath, 'utf-8');
    return parsePersonaMarkdown(content);
  } catch (e) {
    log('warn', `[dynamic_profile] Failed to read persona: ${e.message}`);
    return {
      facts: [],
      preferences: [],
      skills: [],
      goals: [],
    };
  }
}

/**
 * 解析 persona.md 内容
 * 支持 Markdown 格式，提取各部分信息
 */
function parsePersonaMarkdown(content) {
  const sections = {
    facts: [],
    preferences: [],
    skills: [],
    goals: [],
  };
  
  let currentSection = 'facts';
  const lines = content.split('\n');
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 检测 section 标题
    if (trimmed.startsWith('## ') || trimmed.startsWith('# ')) {
      const header = trimmed.replace(/^#+\s*/, '').toLowerCase();
      if (header.includes('fact') || header.includes('事实')) {
        currentSection = 'facts';
      } else if (header.includes('preference') || header.includes('偏好')) {
        currentSection = 'preferences';
      } else if (header.includes('skill') || header.includes('技能')) {
        currentSection = 'skills';
      } else if (header.includes('goal') || header.includes('目标')) {
        currentSection = 'goals';
      }
      continue;
    }
    
    // 提取列表项
    if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
      const item = trimmed.replace(/^[-*]\s*/, '');
      if (item && sections[currentSection]) {
        sections[currentSection].push(item);
      }
    }
  }
  
  return sections;
}

/**
 * 从最近记忆中提取动态画像
 */
async function extractDynamicProfile(userId, options = {}) {
  const limit = options.recentMemoryLimit || DEFAULT_CONFIG.recentMemoryLimit;
  const recencyWindow = options.recencyWindowDays || DEFAULT_CONFIG.recencyWindowDays;
  
  const now = Date.now();
  const windowStart = now - recencyWindow * 24 * 60 * 60 * 1000;
  
  // ── Step 1: 获取最近记忆 ────────────────────────────────────────────────
  let recentMemories = [];
  
  try {
    // 使用 search 获取最近记忆
    const results = await search('', {
      scope: userId ? `user:${userId}` : 'user',
      limit,
      sort: { field: 'created', desc: true },
    });
    
    recentMemories = (results || []).map(r => r.memory || r).filter(Boolean);
  } catch (e) {
    log('warn', `[dynamic_profile] search failed: ${e.message}, using storage fallback`);
    
    // Fallback: 直接从 storage 读取
    const all = await getAllMemories({ scope: userId ? `user:${userId}` : 'user' });
    recentMemories = (all.memories || all || [])
      .filter(m => (m.created || 0) >= windowStart)
      .sort((a, b) => (b.created || 0) - (a.created || 0))
      .slice(0, limit);
  }
  
  // ── Step 2: 提取关键词和主题 ────────────────────────────────────────────
  const keywords = new Map();
  const topics = new Map();
  const entities = new Map();
  const activities = [];
  
  for (const mem of recentMemories) {
    const text = mem.text || mem.content || '';
    const importance = mem.importance || 0.5;
    
    // 提取关键词（简单分词）
    const words = extractKeywords(text);
    for (const word of words) {
      keywords.set(word, (keywords.get(word) || 0) + importance);
    }
    
    // 提取主题（#标签）
    const topicMatches = text.match(/#(\S+)/g) || [];
    for (const t of topicMatches) {
      const topic = t.slice(1);
      topics.set(topic, (topics.get(topic) || 0) + 1);
    }
    
    // 提取实体（@提及）
    const entityMatches = text.match(/@(\S+)/g) || [];
    for (const e of entityMatches) {
      const entity = e.slice(1);
      entities.set(entity, (entities.get(entity) || 0) + 1);
    }
    
    // 提取活动类型
    const category = mem.category || 'other';
    if (!activities.includes(category)) {
      activities.push(category);
    }
  }
  
  // ── Step 3: 聚合动态画像 ────────────────────────────────────────────────
  const topKeywords = [...keywords.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10)
    .map(([word, score]) => ({ word, score }));
  
  const topTopics = [...topics.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([topic, count]) => ({ topic, count }));
  
  const topEntities = [...entities.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 5)
    .map(([entity, count]) => ({ entity, count }));
  
  return {
    recentMemoryCount: recentMemories.length,
    keywords: topKeywords,
    topics: topTopics,
    entities: topEntities,
    activities,
    focusAreas: inferFocusAreas(topKeywords, topTopics),
    lastUpdated: now,
  };
}

/**
 * 简单关键词提取
 */
function extractKeywords(text) {
  const stopWords = new Set([
    '的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个',
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
    'this', 'that', 'these', 'those', 'it', 'its', 'for', 'with', 'from', 'to',
  ]);
  
  return (text || '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .split(/\s+/)
    .filter(w => w.length > 2 && !stopWords.has(w));
}

/**
 * 推断关注点
 */
function inferFocusAreas(keywords, topics) {
  const areas = [];
  
  // 从关键词推断
  const workKeywords = ['project', '项目', '工作', 'task', '任务', 'issue', 'bug', 'feature'];
  const hasWork = keywords.some(k => workKeywords.some(wk => k.word.includes(wk)));
  if (hasWork) {
    areas.push('work');
  }
  
  // 从主题推断
  for (const { topic } of topics) {
    if (!areas.includes(topic)) {
      areas.push(topic);
    }
  }
  
  return areas.slice(0, 3);
}

// ─── 核心接口 ────────────────────────────────────────────────────────────────

/**
 * 获取用户画像
 * @param {string} [userId] - 用户 ID（可选）
 * @param {object} [options] - 配置选项
 * @returns {Promise<{ static: object, dynamic: object, lastUpdated: number }>}
 */
export async function getProfile(userId, options = {}) {
  const cacheKey = userId || 'default';
  const now = Date.now();
  
  // 检查缓存
  const cached = profileCache.get(cacheKey);
  const staticCacheTimeout = options.staticCacheTimeout || DEFAULT_CONFIG.staticCacheTimeout;
  
  // ── Step 1: 静态画像（缓存）─────────────────────────────────────────────
  let staticProfile;
  if (cached && (now - cached.timestamp) < staticCacheTimeout) {
    staticProfile = cached.static;
  } else {
    staticProfile = readPersona(options.personaPath);
  }
  
  // ── Step 2: 动态画像（实时）─────────────────────────────────────────────
  const dynamicProfile = await extractDynamicProfile(userId, options);
  
  // ── Step 3: 更新缓存 ──────────────────────────────────────────────────────
  profileCache.set(cacheKey, {
    static: staticProfile,
    timestamp: now,
  });
  
  return {
    static: staticProfile,
    dynamic: dynamicProfile,
    lastUpdated: now,
  };
}

/**
 * 强制刷新缓存
 */
export function invalidateCache(userId) {
  const cacheKey = userId || 'default';
  profileCache.delete(cacheKey);
  log('info', `[dynamic_profile] Cache invalidated for ${cacheKey}`);
}

/**
 * 批量获取多个用户的画像
 */
export async function getProfiles(userIds, options = {}) {
  const results = new Map();
  
  for (const userId of userIds) {
    const profile = await getProfile(userId, options);
    results.set(userId, profile);
  }
  
  return results;
}

export default {
  getProfile,
  getProfiles,
  invalidateCache,
};
