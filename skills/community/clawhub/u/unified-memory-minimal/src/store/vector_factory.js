/**
 * Vector Store Factory - Dual Backend Support
 * 
 * Supports two backends:
 * - 'lancedb' (default): LanceDB-based vector store (existing implementation)
 * - 'sqlite': SQLite-based vector store with sqlite-vec extension (new)
 * 
 * Usage:
 *   import { getVectorStore } from './store/vector_factory.js';
 *   
 *   // SQLite backend
 *   const sqliteStore = await getVectorStore({ type: 'sqlite', dbPath: './data/memory.db', dimensions: 768 });
 *   
 *   // LanceDB backend (default)
 *   const lancedbStore = await getVectorStore({ type: 'lancedb' });
 * 
 * Environment variables:
 *   VECTOR_STORE_TYPE=lancedb|sqlite
 *   SQLITE_DB_PATH=./data/memory.db
 */

import { config } from '../config.js';

const TAG = "[memory-unified][vector-factory]";

/**
 * Get the active VectorStore instance based on configuration.
 * 
 * @param {Object} [options]
 * @param {string} [options.type] - Backend type: 'lancedb' or 'sqlite'. Defaults to VECTOR_STORE_TYPE env var or 'lancedb'.
 * @param {string} [options.dbPath] - SQLite DB path (only used for sqlite backend)
 * @param {number} [options.dimensions] - Vector dimensions (only used for sqlite backend)
 * @param {Object} [options.logger] - Logger instance
 * @returns {Promise<Object>} VectorStore instance
 */
export async function getVectorStore(options = {}) {
  const type = options.type || process.env.VECTOR_STORE_TYPE || config.VECTOR_STORE_TYPE || 'lancedb';
  const logger = options.logger || console;

  if (type === 'sqlite') {
    logger.info(`${TAG} Initializing SQLite Vector Store backend`);
    
    const { VectorStore } = await import('./vector_sqlite.js');
    
    const dbPath = options.dbPath || process.env.SQLITE_DB_PATH || config.SQLITE_DB_PATH || './data/memory.db';
    const dimensions = options.dimensions || config.localEmbedding?.dimensions || 768;
    
    const store = new VectorStore(dbPath, dimensions, logger);
    
    // Get embedding provider info from config
    const embedProvider = config.activeEmbedProvider;
    const providerInfo = embedProvider ? {
      provider: embedProvider.name,
      model: embedProvider.model,
      dimensions,
    } : undefined;
    
    const initResult = store.init(providerInfo);
    
    if (initResult.needsReindex) {
      logger.info(`${TAG} Vector store requires reindex: ${initResult.reason}`);
    }
    
    return store;
  }

  // Default: LanceDB backend
  logger.info(`${TAG} Initializing LanceDB Vector Store backend (default)`);
  
  const { VectorMemory } = await import('../vector_lancedb.js');
  const vm = new VectorMemory();
  await vm.initialize();
  
  return vm;
}

/**
 * Get the default dimensions for the configured embed provider.
 * @returns {number}
 */
export function getDefaultDimensions() {
  const embedProvider = config.activeEmbedProvider;
  if (embedProvider) {
    // Common dimension sizes
    const dims = {
      'text-embedding-3-small': 1536,
      'text-embedding-3-large': 3072,
      'text-embedding-ada-002': 1536,
      'nomic-embed-text': 768,
      'jina-embeddings-v3': 1024,
      'BAAI/bge-m3': 1024,
    };
    if (dims[embedProvider.model]) return dims[embedProvider.model];
  }
  return 768; // default
}

/**
 * List available vector store backends.
 * @returns {string[]}
 */
export function listBackends() {
  return ['lancedb', 'sqlite'];
}

// Re-export both store classes for direct access
export { VectorStore } from './vector_sqlite.js';
export { VectorMemory } from '../vector_lancedb.js';

// Re-export embedding-related utilities
export { buildFtsQuery, tokenizeForFts, bm25RankToScore } from './vector_sqlite.js';
export { createEmbeddingService, LocalEmbeddingService, OpenAIEmbeddingService, EmbeddingNotReadyError } from './embedding.js';
