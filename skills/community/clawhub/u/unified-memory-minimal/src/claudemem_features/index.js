/**
 * Claude-Mem 风格功能模块 - 统一导出
 * 
 * 本模块集成了从 Claude-Mem 借鉴的以下功能：
 * 1. MemoryEditor - 记忆编辑系统
 * 2. PrivacyManager - 隐私控制系统
 * 3. MemoryQuality - 记忆质量评估系统
 * 4. MemoryIndex - 记忆索引系统
 */

export { MemoryEditor } from './memory_editor.js';
export { PrivacyManager } from './privacy_manager.js';
export { MemoryQuality } from './memory_quality.js';
export { MemoryIndex } from './memory_index.js';

/**
 * 创建所有 Claude-Mem 风格的功能实例
 * @param {Object} storage - 存储实例
 * @param {Object} vectorStore - 向量存储实例
 * @returns {Object} 功能实例集合
 */
export function createClaudeMemFeatures(storage, vectorStore) {
  return {
    memoryEditor: new MemoryEditor(storage, vectorStore),
    privacyManager: new PrivacyManager(storage, null), // memoryEditor 后面注入
    memoryQuality: new MemoryQuality(storage, vectorStore),
    memoryIndex: new MemoryIndex(storage, vectorStore)
  };
}

/**
 * 默认功能集合
 */
export default {
  MemoryEditor,
  PrivacyManager,
  MemoryQuality,
  MemoryIndex,
  createClaudeMemFeatures
};