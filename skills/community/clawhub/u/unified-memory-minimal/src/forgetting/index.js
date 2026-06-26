/**
 * Forgetting Module - 遗忘机制模块入口
 * 
 * 导出：
 * - Contradiction Resolver: 矛盾检测与解决
 * - Temporal Expiry: 临时事实过期管理
 */

export {
  detectContradiction,
  detectContradictions,
  resolveContradictions,
  dedupWithContradictionResolution,
} from './contradiction_resolver.js';

export {
  isTemporalMemory,
  extractExpiryTime,
  isExpired,
  extractExpiryTimes,
  cleanExpiredMemories,
  startExpiryChecker,
} from './temporal_expiry.js';

export default {
  // Contradiction
  detectContradiction,
  detectContradictions,
  resolveContradictions,
  dedupWithContradictionResolution,
  // Temporal
  isTemporalMemory,
  extractExpiryTime,
  isExpired,
  extractExpiryTimes,
  cleanExpiredMemories,
  startExpiryChecker,
};
