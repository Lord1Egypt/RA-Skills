/**
 * @zouroboros/memory
 *
 * Production-grade persistent memory system with hybrid search,
 * decay classes, episodic memory, cognitive profiles, and MCP server.
 * Node.js 22+ port of the Zouroboros memory subsystem.
 *
 * @module @zouroboros/memory
 */

import { initDatabase as _initDb, closeDatabase as _closeDb, runMigrations as _runMigrations, getDbStats as _getDbStats } from './database.js';
import { getEpisodeStats as _getEpisodeStats } from './episodes.js';
import { ensureProfileSchema as _ensureProfileSchema } from './profiles.js';

export const VERSION = '1.0.0';

// Database
export {
  initDatabase,
  getDatabase,
  closeDatabase,
  isInitialized,
  runMigrations,
  getDbStats,
} from './database.js';

// Embeddings
export {
  generateEmbedding,
  generateHypotheticalAnswer,
  generateHyDEExpansion,
  blendEmbeddings,
  cosineSimilarity,
  serializeEmbedding,
  deserializeEmbedding,
  checkOllamaHealth,
  listAvailableModels,
  throttleMetrics,
  resetThrottleState,
} from './embeddings.js';

// Facts
export {
  storeFact,
  searchFacts,
  searchFactsVector,
  searchFactsHybrid,
  getFact,
  deleteFact,
  touchFact,
  cleanupExpiredFacts,
} from './facts.js';

// Episodes
export {
  createEpisode,
  searchEpisodes,
  getEntityEpisodes,
  updateEpisodeOutcome,
  getEpisodeStats,
} from './episodes.js';

// Graph
export {
  buildEntityGraph,
  getRelatedEntities,
  searchFactsGraphBoosted,
  extractQueryEntities,
  invalidateGraphCache,
} from './graph.js';

// Cognitive Profiles
export {
  getProfile,
  updateTraits,
  updatePreferences,
  recordInteraction,
  getRecentInteractions,
  getProfileSummary,
  listProfiles,
  deleteProfile,
  ensureProfileSchema,
} from './profiles.js';

// MCP Server
export { handleMessage, startMcpServer } from './mcp-server.js';

// Procedures
export {
  searchProcedures,
  getProcedure,
  getProcedureVersions,
  compareProcedureVersions,
  getProcedureEpisodes,
} from './procedures.js';
export type { Procedure, ProcedureStep, ProcedureComparison, ProcedureEpisode } from './procedures.js';

// Reranker + LLM
export { rerankResults } from './reranker.js';
export { llmCall } from './llm.js';
export type { LlmCallOptions, LlmCallResult } from './llm.js';

// Types
export type {
  DecayClass,
  MemoryConfig,
  MemoryEntry,
  MemorySearchResult,
  EpisodicMemory,
  TemporalQuery,
  CognitiveProfile,
  InteractionRecord,
  GraphNode,
  GraphEdge,
  CotAnswerResult,
  DeepSearchResult,
} from './types.js';

/**
 * Initialize the memory system (database + migrations + profile schema).
 */
export function init(config: import('./types.js').MemoryConfig): void {
  _initDb(config);
  _runMigrations(config);
  _ensureProfileSchema();
}

/**
 * Shutdown the memory system gracefully.
 */
export function shutdown(): void {
  _closeDb();
}

/**
 * Get combined memory system statistics.
 */
export function getStats(config: import('./types.js').MemoryConfig): {
  database: {
    facts: number;
    episodes: number;
    procedures: number;
    openLoops: number;
    embeddings: number;
  };
  episodes: {
    total: number;
    byOutcome: Record<string, number>;
  };
} {
  return {
    database: _getDbStats(config),
    episodes: _getEpisodeStats(),
  };
}
