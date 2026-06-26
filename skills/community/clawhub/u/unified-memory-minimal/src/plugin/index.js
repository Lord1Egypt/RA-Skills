/**
 * src/plugin/index.js
 * OpenClaw Memory Plugin Interface
 * 
 * 实现 OpenClaw 规范的 memory_search 和 memory_get 接口
 * 让 unified-memory 能作为 OpenClaw 内置 memory backend 替代品
 */

import { config } from '../config.js';
import { getAllMemories, getMemory } from '../storage.js';
import { search as hybridSearch } from '../search.js';

/**
 * OpenClaw Memory Plugin: memory_search
 * @param {Object} params
 * @param {string} params.query - 搜索查询
 * @param {string} [params.scope='agent'] - 作用域: agent/user/project/global
 * @param {number} [params.limit=5] - 返回结果数
 * @returns {Promise<{memories: Array, query: string, count: number}>}
 */
export async function memory_search({ query, scope = 'agent', limit = 5 } = {}) {
  try {
    // 使用 unified-memory 的混合搜索管道
    const results = await hybridSearch({
      query,
      topK: limit,
      mode: 'hybrid',
      scope,
    });

    // 转换格式为 OpenClaw 规范
    const memories = (results.results || results || []).map(r => ({
      content: r.content || r.text || '',
      score: r.score || r.relevance || 0,
      scope: r.scope || scope,
      memory_id: r.id || r.memory_id || r._id || '',
      timestamp: r.created_at || r.timestamp || Date.now(),
    }));

    return {
      memories,
      query,
      count: memories.length,
    };
  } catch (err) {
    // OpenClaw 规范：失败返回空结果，不抛错
    return {
      memories: [],
      query,
      count: 0,
      error: err.message,
    };
  }
}

/**
 * OpenClaw Memory Plugin: memory_get
 * @param {Object} params
 * @param {string} params.path - 文件路径 (e.g., "memory/2026-03-28.md" 或 "MEMORY.md")
 * @param {number} [params.offset=0] - 行偏移
 * @param {number} [params.limit=100] - 行数限制
 * @returns {Promise<{text: string, path: string, metadata?: Object}>}
 */
export async function memory_get({ path, offset = 0, limit = 100 } = {}) {
  try {
    // path 格式: "memory/YYYY-MM-DD.md" 或 "MEMORY.md"
    // 转换为 unified-memory 的内部存储路径
    let targetPath = path;
    
    if (!path) {
      // 默认返回今天的日记
      const today = new Date().toISOString().slice(0, 10);
      targetPath = `memory/${today}.md`;
    }

    // 尝试从 unified-memory 存储中读取
    // 先尝试作为 memory_id 直接读取
    const memory = await getMemory(targetPath);
    if (memory) {
      const text = memory.content || '';
      const lines = text.split('\n');
      const slice = lines.slice(offset, offset + limit);
      return {
        text: slice.join('\n'),
        path: targetPath,
        metadata: {
          memory_id: memory.id || targetPath,
          created_at: memory.created_at,
          updated_at: memory.updated_at,
          scope: memory.scope,
        },
      };
    }

    // 降级：尝试读取文件系统中的 markdown 文件
    const { join } = await import('path');
    const { existsSync, readFileSync } = await import('fs');
    const filePath = join(config.memoryDir, targetPath);
    
    if (existsSync(filePath)) {
      const text = readFileSync(filePath, 'utf-8');
      const lines = text.split('\n');
      const slice = lines.slice(offset, offset + limit);
      return {
        text: slice.join('\n'),
        path: targetPath,
        metadata: {},
      };
    }

    // OpenClaw 规范：文件不存在也返回空文本，不抛错
    return {
      text: '',
      path: targetPath,
    };
  } catch (err) {
    return {
      text: '',
      path: path || 'unknown',
      error: err.message,
    };
  }
}

/**
 * OpenClaw Memory Plugin: memory_write (可选实现)
 * @param {Object} params
 * @param {string} params.content - 记忆内容
 * @param {string} [params.scope='agent'] - 作用域
 * @param {Object} [params.metadata] - 元数据
 * @returns {Promise<{path: string, memory_id: string}>}
 */
export async function memory_write({ content, scope = 'agent', metadata = {} } = {}) {
  try {
    const { addMemory } = await import('../storage.js');
    const memory = await addMemory({
      content,
      scope,
      ...metadata,
    });
    return {
      path: `memory/${new Date().toISOString().slice(0, 10)}.md`,
      memory_id: memory.id,
    };
  } catch (err) {
    return {
      path: '',
      memory_id: '',
      error: err.message,
    };
  }
}
