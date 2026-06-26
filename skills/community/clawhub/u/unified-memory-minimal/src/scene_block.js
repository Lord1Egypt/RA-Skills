/**
 * scene_block.js — L2 Scene Block Inductor
 * 
 * 从 L1 记忆中自动归纳场景块：
 * - 按时间窗口聚类相关记忆
 * - 提取场景主题、关键实体、行动项
 * - 生成 Markdown 格式的场景块
 * 
 * Inspired by memory-tencentdb L2 Scene Induction
 */

import { getAllMemories, getMemory } from './storage.js';
import { search } from './search.js';
import { config, llmCall } from './config.js';
import { log } from './logger.js';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ─── 配置 ───────────────────────────────────────────────────────────────────

const DEFAULT_CONFIG = {
  sceneWindowHours: 24,        // 场景时间窗口
  minMemoriesPerScene: 3,      // 最少记忆数
  maxScenes: 20,               // 最大场景数
  similarityThreshold: 0.4,    // 相似度阈值
  sceneDir: 'scene_blocks',    // 场景块目录
};

// ─── 场景块结构 ─────────────────────────────────────────────────────────────

/**
 * @typedef {Object} SceneBlock
 * @property {string} id - scene_xxx
 * @property {string} title - 场景标题
 * @property {string} summary - 摘要
 * @property {string[]} entities - 关键实体
 * @property {string[]} actions - 行动项
 * @property {string[]} memoryIds - 关联记忆 ID
 * @property {{start: number, end: number}} timeRange - 时间范围
 * @property {string[]} tags - 标签
 * @property {number} created - 创建时间
 * @property {number} updated - 更新时间
 * @property {string} scope - 范围
 */

// ─── 核心函数 ───────────────────────────────────────────────────────────────

/**
 * 从记忆中归纳场景块
 * @param {Object} options
 * @param {string} [options.scope='USER']
 * @param {{start?: number, end?: number}} [options.timeRange]
 * @param {number} [options.minMemories=3]
 * @param {number} [options.maxScenes=20]
 * @returns {Promise<SceneBlock[]>}
 */
export async function inductScenes(options = {}) {
  const {
    scope = 'USER',
    timeRange,
    minMemories = DEFAULT_CONFIG.minMemoriesPerScene,
    maxScenes = DEFAULT_CONFIG.maxScenes,
  } = options;

  log.info(`[SceneBlock] Starting scene induction for scope ${scope}`);

  // 1. 获取相关记忆
  const memories = await getMemoriesForSceneInduction(scope, timeRange);
  log.info(`[SceneBlock] Found ${memories.length} memories for induction`);

  if (memories.length < minMemories) {
    log.warn(`[SceneBlock] Not enough memories (${memories.length} < ${minMemories})`);
    return [];
  }

  // 2. 按时间窗口聚类
  const clusters = clusterByTimeWindow(memories, DEFAULT_CONFIG.sceneWindowHours);
  log.info(`[SceneBlock] Clustered into ${clusters.length} groups`);

  // 3. 对每个聚类生成场景块
  const scenes = [];
  for (const cluster of clusters) {
    if (cluster.length < minMemories) continue;

    const scene = await generateSceneBlock(cluster, scope);
    if (scene) {
      scenes.push(scene);
      log.info(`[SceneBlock] Generated scene: ${scene.title}`);
    }

    if (scenes.length >= maxScenes) break;
  }

  // 4. 保存场景块
  await saveSceneBlocks(scenes, scope);

  log.info(`[SceneBlock] Inducted ${scenes.length} scenes`);
  return scenes;
}

/**
 * 获取用于场景归纳的记忆
 */
async function getMemoriesForSceneInduction(scope, timeRange) {
  const allMemories = await getAllMemories();
  
  let filtered = allMemories.filter(m => {
    // 范围过滤
    if (m.scope && m.scope !== scope) return false;
    
    // 时间过滤
    if (timeRange) {
      if (timeRange.start && m.created < timeRange.start) return false;
      if (timeRange.end && m.created > timeRange.end) return false;
    }
    
    return true;
  });

  // 按时间排序
  filtered.sort((a, b) => (a.created || 0) - (b.created || 0));
  
  return filtered;
}

/**
 * 按时间窗口聚类记忆
 */
function clusterByTimeWindow(memories, windowHours) {
  if (memories.length === 0) return [];

  const windowMs = windowHours * 60 * 60 * 1000;
  const clusters = [];
  let currentCluster = [memories[0]];
  let windowStart = memories[0].created || Date.now();

  for (let i = 1; i < memories.length; i++) {
    const mem = memories[i];
    const memTime = mem.created || Date.now();
    const windowEnd = windowStart + windowMs;

    if (memTime <= windowEnd) {
      currentCluster.push(mem);
    } else {
      if (currentCluster.length >= DEFAULT_CONFIG.minMemoriesPerScene) {
        clusters.push(currentCluster);
      }
      currentCluster = [mem];
      windowStart = memTime;
    }
  }

  // 处理最后一个聚类
  if (currentCluster.length >= DEFAULT_CONFIG.minMemoriesPerScene) {
    clusters.push(currentCluster);
  }

  return clusters;
}

/**
 * 使用 LLM 生成场景块
 */
async function generateSceneBlock(memories, scope) {
  const memoryTexts = memories.map(m => {
    const category = m.category || 'general';
    const text = m.text || '';
    const time = new Date(m.created || Date.now()).toLocaleString('zh-CN');
    return `[${time}][${category}] ${text}`;
  }).join('\n');

  const prompt = `从以下记忆中归纳一个场景块：

${memoryTexts}

请输出 JSON 格式（不要包含 markdown 代码块）：
{
  "title": "场景标题（简短，5-10字）",
  "summary": "场景摘要（1-2句话，描述主要内容和目标）",
  "entities": ["关键实体1", "关键实体2", "关键实体3"],
  "actions": ["行动项1", "行动项2"],
  "tags": ["标签1", "标签2"]
}`;

  try {
    const response = await llmCall(prompt);
    
    // 清理响应（移除可能的 markdown 代码块）
    let cleaned = response.trim();
    if (cleaned.startsWith('```')) {
      cleaned = cleaned.replace(/^```(?:json)?\n?/, '').replace(/\n?```$/, '');
    }
    
    const parsed = JSON.parse(cleaned);
    
    return {
      id: `scene_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: parsed.title || '未命名场景',
      summary: parsed.summary || '',
      entities: parsed.entities || [],
      actions: parsed.actions || [],
      memoryIds: memories.map(m => m.id),
      timeRange: {
        start: Math.min(...memories.map(m => m.created || Date.now())),
        end: Math.max(...memories.map(m => m.created || Date.now())),
      },
      tags: parsed.tags || [],
      created: Date.now(),
      updated: Date.now(),
      scope,
    };
  } catch (err) {
    log.error('[SceneBlock] Failed to parse scene block:', err);
    
    // 降级：生成简单场景块
    return {
      id: `scene_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: `场景 ${new Date().toLocaleDateString('zh-CN')}`,
      summary: memories.map(m => m.text).join('; ').substring(0, 200),
      entities: [],
      actions: [],
      memoryIds: memories.map(m => m.id),
      timeRange: {
        start: Math.min(...memories.map(m => m.created || Date.now())),
        end: Math.max(...memories.map(m => m.created || Date.now())),
      },
      tags: [],
      created: Date.now(),
      updated: Date.now(),
      scope,
    };
  }
}

// ─── 场景块存储 ─────────────────────────────────────────────────────────────

/**
 * 获取场景块目录
 */
function getSceneDir(scope) {
  const baseDir = config.storage?.path || path.join(process.env.OPENCLAW_WORKSPACE_DIR || '~/.openclaw/workspace', 'memory');
  const sceneDir = path.join(baseDir, DEFAULT_CONFIG.sceneDir, scope);
  
  // 确保目录存在
  if (!fs.existsSync(sceneDir)) {
    fs.mkdirSync(sceneDir, { recursive: true });
  }
  
  return sceneDir;
}

/**
 * 保存场景块
 */
async function saveSceneBlocks(scenes, scope) {
  const sceneDir = getSceneDir(scope);
  
  for (const scene of scenes) {
    const filePath = path.join(sceneDir, `${scene.id}.json`);
    fs.writeFileSync(filePath, JSON.stringify(scene, null, 2), 'utf-8');
    
    // 同时生成 Markdown 文件
    const mdPath = path.join(sceneDir, `${scene.id}.md`);
    const mdContent = generateSceneMarkdown(scene);
    fs.writeFileSync(mdPath, mdContent, 'utf-8');
  }
  
  // 更新场景索引
  await updateSceneIndex(scenes, scope);
}

/**
 * 生成场景 Markdown
 */
function generateSceneMarkdown(scene) {
  return `# ${scene.title}

**摘要**: ${scene.summary}

**时间范围**: ${new Date(scene.timeRange.start).toLocaleString('zh-CN')} - ${new Date(scene.timeRange.end).toLocaleString('zh-CN')}

## 关键实体

${scene.entities.map(e => `- ${e}`).join('\n') || '无'}

## 行动项

${scene.actions.map(a => `- [ ] ${a}`).join('\n') || '无'}

## 标签

${scene.tags.map(t => '#' + t).join(' ') || '无'}

## 关联记忆

${scene.memoryIds.map(id => `- ${id}`).join('\n')}

---
*创建时间: ${new Date(scene.created).toLocaleString('zh-CN')}*
`;
}

/**
 * 更新场景索引
 */
async function updateSceneIndex(scenes, scope) {
  const sceneDir = getSceneDir(scope);
  const indexPath = path.join(sceneDir, 'index.json');
  
  let index = { scenes: [], updated: 0 };
  
  // 读取现有索引
  if (fs.existsSync(indexPath)) {
    try {
      index = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
    } catch (err) {
      log.warn('[SceneBlock] Failed to read index, creating new one');
    }
  }
  
  // 合并新场景
  const existingIds = new Set(index.scenes.map(s => s.id));
  for (const scene of scenes) {
    if (!existingIds.has(scene.id)) {
      index.scenes.push({
        id: scene.id,
        title: scene.title,
        summary: scene.summary,
        tags: scene.tags,
        timeRange: scene.timeRange,
        created: scene.created,
      });
    }
  }
  
  // 按时间排序
  index.scenes.sort((a, b) => (b.created || 0) - (a.created || 0));
  
  // 限制数量
  if (index.scenes.length > DEFAULT_CONFIG.maxScenes * 2) {
    index.scenes = index.scenes.slice(0, DEFAULT_CONFIG.maxScenes * 2);
  }
  
  index.updated = Date.now();
  
  fs.writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf-8');
}

// ─── 场景块查询 ─────────────────────────────────────────────────────────────

/**
 * 列出场景块
 */
export async function listSceneBlocks(scope = 'USER', limit = 20) {
  const sceneDir = getSceneDir(scope);
  const indexPath = path.join(sceneDir, 'index.json');
  
  if (!fs.existsSync(indexPath)) {
    return [];
  }
  
  try {
    const index = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
    return index.scenes.slice(0, limit);
  } catch (err) {
    log.error('[SceneBlock] Failed to read index:', err);
    return [];
  }
}

/**
 * 获取场景块详情
 */
export async function getSceneBlock(sceneId, scope = 'USER') {
  const sceneDir = getSceneDir(scope);
  const filePath = path.join(sceneDir, '\${sceneId}.json');
  
  if (!fs.existsSync(filePath)) {
    return null;
  }
  
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch (err) {
    log.error('[SceneBlock] Failed to read scene:', err);
    return null;
  }
}

/**
 * 删除场景块
 */
export async function deleteSceneBlock(sceneId, scope = 'USER') {
  const sceneDir = getSceneDir(scope);
  
  // 删除 JSON 和 Markdown 文件
  const jsonPath = path.join(sceneDir, '\${sceneId}.json');
  const mdPath = path.join(sceneDir, '\${sceneId}.md');
  
  if (fs.existsSync(jsonPath)) fs.unlinkSync(jsonPath);
  if (fs.existsSync(mdPath)) fs.unlinkSync(mdPath);
  
  // 更新索引
  const indexPath = path.join(sceneDir, 'index.json');
  if (fs.existsSync(indexPath)) {
    try {
      const index = JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
      index.scenes = index.scenes.filter(s => s.id !== sceneId);
      index.updated = Date.now();
      fs.writeFileSync(indexPath, JSON.stringify(index, null, 2), 'utf-8');
    } catch (err) {
      log.error('[SceneBlock] Failed to update index:', err);
    }
  }
  
  return true;
}

/**
 * 搜索场景块
 */
export async function searchSceneBlocks(query, scope = 'USER', limit = 10) {
  const scenes = await listSceneBlocks(scope, 100);
  
  const queryLower = query.toLowerCase();
  
  // 简单关键词匹配
  const matched = scenes.filter(scene => {
    const titleMatch = scene.title.toLowerCase().includes(queryLower);
    const summaryMatch = scene.summary.toLowerCase().includes(queryLower);
    const tagMatch = scene.tags.some(t => t.toLowerCase().includes(queryLower));
    
    return titleMatch || summaryMatch || tagMatch;
  });
  
  return matched.slice(0, limit);
}

/**
 * 获取场景统计
 */
export async function getSceneStats(scope = 'USER') {
  const scenes = await listSceneBlocks(scope, 1000);
  
  return {
    total: scenes.length,
    tags: [...new Set(scenes.flatMap(s => s.tags))],
    timeRange: scenes.length > 0 ? {
      start: Math.min(...scenes.map(s => s.timeRange?.start || 0)),
      end: Math.max(...scenes.map(s => s.timeRange?.end || 0)),
    } : null,
  };
}

// ─── 导出 ───────────────────────────────────────────────────────────────────

export default {
  inductScenes,
  listSceneBlocks,
  getSceneBlock,
  deleteSceneBlock,
  searchSceneBlocks,
  getSceneStats,
};
