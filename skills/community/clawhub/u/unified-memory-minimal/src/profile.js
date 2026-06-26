/**
 * profile.js — Profile Aggregator for Unified Memory
 * 
 * 实现 SuperMemory 风格的 User Profile 抽象：
 * - static: 长期稳定事实 + 偏好
 * - dynamic: 近期上下文 + 进行中的工作
 * 
 * 核心逻辑：
 * 1. 搜索某 scope 下所有 fact/preference/identity 类记忆
 * 2. 按实体分组，检测矛盾（同实体多版本）
 * 3. 按访问频率和时间分离 static vs dynamic
 * 4. 聚合返回结构化 profile
 */

import { getAllMemories } from './storage.js';
import { search } from './search.js';
import { extractEntities } from './graph/entity.js';
import { config } from './config.js';
import { log } from './logger.js';

const DEFAULT_STATIC_DAYS = 30;        // 超过 30 天无访问 → static
const DEFAULT_ACCESS_THRESHOLD = 3;   // 过去 7 天访问 ≥3 次 → dynamic
const RECENCY_WINDOW_DAYS = 7;         // 近期窗口

// ─── 实体类型黑名单：这些实体的记忆通常偏 dynamic ───────────────────────────────
const DYNAMIC_ENTITY_KEYWORDS = [
  'project', '任务', '工作', '当前', '最近', '进行中',
  'issue', 'bug', 'todo', 'roadmap', 'sprint',
];

// ─── Static 类 category/type ──────────────────────────────────────────────────
const STATIC_CATEGORIES = new Set(['preference', 'identity', 'habit', 'goal', 'skill']);
const FACT_CATEGORIES = new Set(['fact', 'decision']);

// ─── 工具函数 ────────────────────────────────────────────────────────────────

/**
 * 判断实体名是否暗示 dynamic 内容
 */
function isLikelyDynamic(entityName) {
  const lower = (entityName || '').toLowerCase();
  return DYNAMIC_ENTITY_KEYWORDS.some(kw => lower.includes(kw));
}

/**
 * 计算记忆"新鲜度"：0=完全陈旧，1=最近频繁访问
 */
function computeFreshness(mem) {
  const now = Date.now();
  const created = mem.created || now;
  const lastAccessed = mem.lastAccessed || mem.touchTime || created;
  
  const ageDays = (now - lastAccessed) / (24 * 60 * 60 * 1000);
  const accessCount = mem.accessCount || 1;
  
  // Weibull-ish 衰减：7天内频繁访问 → 高新鲜度
  const ageScore = Math.exp(-ageDays / RECENCY_WINDOW_DAYS);
  const accessScore = Math.min(1, (accessCount - 1) / 5); // 0-5次访问映射到 0-1
  
  return Math.min(1, ageScore * 0.7 + accessScore * 0.3);
}

/**
 * 合并语义相似的记忆文本（简单的关键词重叠检测）
 */
function findSimilarClusters(memories) {
  const clusters = [];
  const used = new Set();
  
  for (const mem of memories) {
    if (used.has(mem.id)) continue;
    
    const cluster = [mem];
    used.add(mem.id);
    
    const words = new Set(
      (mem.text || '')
        .toLowerCase()
        .replace(/[^\w\s]/g, ' ')
        .split(/\s+/)
        .filter(w => w.length > 2)
    );
    
    for (const other of memories) {
      if (used.has(other.id)) continue;
      const otherWords = new Set(
        (other.text || '')
          .toLowerCase()
          .replace(/[^\w\s]/g, ' ')
          .split(/\s+/)
          .filter(w => w.length > 2)
      );
      
      // Jaccard 相似度
      const intersection = [...words].filter(w => otherWords.has(w)).length;
      const union = new Set([...words, ...otherWords]).size;
      const similarity = union > 0 ? intersection / union : 0;
      
      if (similarity > 0.4) {
        cluster.push(other);
        used.add(other.id);
      }
    }
    
    clusters.push(cluster);
  }
  
  return clusters;
}

// ─── 核心 Profile 聚合 ──────────────────────────────────────────────────────

/**
 * 获取指定 scope 的用户 profile
 * 
 * @param {object} options
 * @param {string} [options.scope='user'] - 'agent' | 'user' | 'team' | 'global'
 * @param {string} [options.containerTag] - 项目标签（lane）
 * @param {string} [options.entityFilter] - 只返回某实体的 profile
 * @param {number} [options.staticDays] - 超过 N 天无访问视为 static
 * @param {number} [options.limit=100] - 最大记忆数量
 * @param {object} [options.llm] - 可选 LLM client，用于压缩
 * @returns {Promise<Profile>}
 */
export async function getProfile({
  scope = 'user',
  containerTag = null,
  entityFilter = null,
  staticDays = DEFAULT_STATIC_DAYS,
  limit = 100,
  llm = null,
} = {}) {
  const staticThresholdMs = staticDays * 24 * 60 * 60 * 1000;
  const now = Date.now();
  
  // ── Step 1: 搜索相关记忆 ──────────────────────────────────────────────────
  let allMemories = [];
  
  try {
    // 优先用 search engine（混合搜索 + BM25）
    const searchResults = await search('', {
      scope,
      categories: ['fact', 'preference', 'identity', 'habit', 'goal', 'skill', 'decision'],
      limit,
    });
    
    // search 可能返回 rank 或直接返回 memory 对象
    allMemories = searchResults.map(r => r.memory || r).filter(Boolean);
  } catch (e) {
    // fallback 到 storage 直接读取
    log('WARN', `[profile] search failed: ${e.message}, using getAllMemories`);
    const raw = await getAllMemories({ scope, category: ['fact', 'preference', 'identity'] });
    allMemories = raw.memories || [];
  }
  
  // 按 containerTag 过滤
  if (containerTag) {
    allMemories = allMemories.filter(m => 
      m.containerTag === containerTag || m.tags?.includes(containerTag)
    );
  }
  
  // ── Step 2: 实体分组 ──────────────────────────────────────────────────────
  const entityGroups = new Map(); // entityName → { entity, memories: [] }
  
  for (const mem of allMemories) {
    const text = mem.text || '';
    let entities = [];
    
    try {
      entities = extractEntities(text) || [];
    } catch (e) {
      // entity extraction 失败时用关键词兜底
      const personMatches = text.match(/@(\S+)/g) || [];
      const hashMatches = text.match(/#(\S+)/g) || [];
      entities = [
        ...personMatches.map(m => ({ name: m.slice(1), type: 'person' })),
        ...hashMatches.map(m => ({ name: m.slice(1), type: 'topic' })),
      ];
    }
    
    const primaryEntity = entities[0]?.name || '_anonymous';
    
    // entityFilter 过滤
    if (entityFilter && !primaryEntity.toLowerCase().includes(entityFilter.toLowerCase())) {
      continue;
    }
    
    if (!entityGroups.has(primaryEntity)) {
      entityGroups.set(primaryEntity, {
        entity: primaryEntity,
        entityType: entities[0]?.type || 'unknown',
        memories: [],
      });
    }
    entityGroups.get(primaryEntity).memories.push(mem);
  }
  
  // ── Step 3: 分离 static vs dynamic ──────────────────────────────────────
  const staticFacts = [];
  const dynamicFacts = [];
  
  for (const [entityName, group] of entityGroups) {
    // 实体名暗示 dynamic（如 project、进行中）
    const likelyDynamic = isLikelyDynamic(entityName);
    
    // 按时间排序，最新的在前
    const sorted = [...group.memories].sort((a, b) => {
      const aTime = b.lastAccessed || b.touchTime || b.created || 0;
      const bTime = a.lastAccessed || a.touchTime || a.created || 0;
      return bTime - aTime;
    });
    
    const latest = sorted[0];
    const age = now - (latest.lastAccessed || latest.touchTime || latest.created || now);
    
    if (likelyDynamic) {
      // 这类实体默认 dynamic
      dynamicFacts.push(...sorted);
    } else if (age >= staticThresholdMs && latest.accessCount >= DEFAULT_ACCESS_THRESHOLD) {
      // 老记忆但频繁访问 → dynamic（反复查看说明还在变化）
      dynamicFacts.push(...sorted);
    } else if (age >= staticThresholdMs) {
      // 长期稳定 → static
      staticFacts.push(latest);
    } else {
      // 新记忆 → dynamic
      dynamicFacts.push(...sorted);
    }
  }
  
  // ── Step 4: 偏好类全部进 static ──────────────────────────────────────────
  const preferenceMemories = allMemories.filter(m => STATIC_CATEGORIES.has(m.category));
  for (const p of preferenceMemories) {
    if (!staticFacts.find(s => s.id === p.id)) {
      staticFacts.push(p);
    }
  }
  
  // ── Step 5: 相似记忆合并 ──────────────────────────────────────────────────
  const mergedStatic = mergeSimilar(staticFacts);
  const mergedDynamic = mergeSimilar(dynamicFacts);
  
  // ── Step 6: 生成摘要 ──────────────────────────────────────────────────────
  let summary = '';
  if (llm && (mergedStatic.length > 10 || mergedDynamic.length > 5)) {
    try {
      summary = await compressProfileWithLLM(mergedStatic, mergedDynamic, llm);
    } catch (e) {
      log('WARN', `[profile] LLM compression failed: ${e.message}`);
    }
  }
  
  // ── Step 7: 计算置信度 ───────────────────────────────────────────────────
  const confidence = calculateConfidence(
    allMemories.length,
    mergedStatic.length,
    mergedDynamic.length
  );
  
  return {
    // 核心字段：SuperMemory 风格
    static: mergedStatic.map(m => m.text || m.content),
    dynamic: mergedDynamic.map(m => m.text || m.content),
    
    // 附加信息
    summary: summary || null,
    confidence,
    
    // 统计
    memoryCount: {
      total: allMemories.length,
      static: mergedStatic.length,
      dynamic: mergedDynamic.length,
    },
    
    // 按实体分类的 profile（可选，方便调试）
    byEntity: entityFilter ? null : Object.fromEntries(
      [...entityGroups.entries()].map(([name, g]) => [
        name,
        {
          type: g.entityType,
          count: g.memories.length,
          latestText: g.memories[0]?.text,
          isStatic: !dynamicFacts.find(d => d.id === g.memories[0]?.id),
        },
      ])
    ),
    
    lastUpdated: now,
    scope,
    containerTag,
  };
}

/**
 * 合并语义相似的记忆（simple Jaccard-based clustering）
 */
function mergeSimilar(memories) {
  const clusters = findSimilarClusters(memories);
  
  // 每个 cluster 取 importance 最高的一条
  return clusters.map(cluster => {
    cluster.sort((a, b) => (b.importance || 0.5) - (a.importance || 0.5));
    return cluster[0];
  });
}

/**
 * 置信度计算
 */
function calculateConfidence(total, staticCount, dynamicCount) {
  if (total === 0) return 0;
  
  // 覆盖度：记忆越多越可信（50 条满）
  const coverage = Math.min(1, total / 50);
  
  // 平衡度：static/dynamic 不要一边倒
  const totalClassified = staticCount + dynamicCount;
  const balance = totalClassified > 0
    ? 1 - Math.abs(staticCount - dynamicCount) / totalClassified
    : 0;
  
  // 组合
  const raw = coverage * 0.6 + balance * 0.4;
  return Math.round(Math.min(1, raw) * 100) / 100;
}

/**
 * 用 LLM 压缩超长的 profile（>20 条时触发）
 */
async function compressProfileWithLLM(staticFacts, dynamicFacts, llm) {
  const staticTexts = staticFacts.map(m => `- ${m.text}`).join('\n');
  const dynamicTexts = dynamicFacts.map(m => `- ${m.text}`).join('\n');
  
  const prompt = `你是记忆摘要助手。把下面的记忆压缩成简洁的摘要，保留关键信息。

STATIC（长期事实）:
${staticTexts}

DYNAMIC（近期上下文）:
${dynamicTexts}

输出 JSON：
{
  "static_summary": "一句话总结用户的长期特征",
  "dynamic_summary": "一句话总结用户最近在做什么",
}
`;

  const response = await llm.generate(prompt, null, null, { max_tokens: 200 });
  const content = typeof response === 'string' ? response : response.content;
  
  try {
    // 尝试解析 JSON
    const match = content.match(/\{[\s\S]*\}/);
    if (match) {
      return JSON.parse(match[0]);
    }
  } catch {
    // 解析失败返回原文
  }
  
  return content.slice(0, 500);
}

// ─── 批量 Profile（多用户/多 agent）────────────────────────────────────────

/**
 * 获取团队或所有 agent 的 profiles
 * @param {object} options
 * @param {string} options.scope
 * @returns {Promise<Map<string, Profile>>}
 */
export async function getTeamProfiles(scope = 'team') {
  const allMemories = await getAllMemories({ scope, limit: 500 });
  const memories = allMemories.memories || allMemories;
  
  // 按 creator/user 分组
  const byOwner = new Map();
  for (const mem of memories) {
    const owner = mem.creator || mem.userId || '_unknown';
    if (!byOwner.has(owner)) byOwner.set(owner, []);
    byOwner.get(owner).push(mem);
  }
  
  const results = new Map();
  for (const [owner, ownerMemories] of byOwner) {
    const profile = await getProfile({ scope, limit: 50 });
    profile.owner = owner;
    results.set(owner, profile);
  }
  
  return results;
}

// ─── 导出默认工具函数 ───────────────────────────────────────────────────────

export default { getProfile, getTeamProfiles };
