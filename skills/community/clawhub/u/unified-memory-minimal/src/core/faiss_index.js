/**
 * FAISS-like In-Memory Vector Index
 * 
 * Provides a pure JavaScript in-memory vector index as a lightweight alternative
 * to FAISS (which is C++ only and not portable to Node.js without Python).
 * 
 * Implements:
 * - Flat L2/cosine similarity search (brute-force, equivalent to FAISS IndexFlatL2)
 * - ID-to-index mapping for memory storage
 * 
 * Note: For production with large datasets, consider:
 *   - LanceDB (vectordb npm package) - RECOMMENDED
 *   - sqlite-vec (OpenClaw built-in)
 *   - Qdrant/Weaviate/Pinecone (external services)
 * 
 * This module provides a simple fallback for small-to-medium memory stores
 * (< 10,000 vectors) without external dependencies.
 */

import { getAllMemories } from '../storage.js';
import { getEmbedding } from '../vector.js';

// In-memory index storage
let indexVectors = [];  // Float32Array of vectors
let indexIds = [];      // Corresponding memory IDs
let indexDim = 0;       // Embedding dimension
let indexBuilt = false;

/**
 * Compute cosine similarity between two vectors
 */
function cosineSimilarity(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  if (normA === 0 || normB === 0) return 0;
  return dot / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Compute L2 squared distance between two vectors
 */
function l2Squared(a, b) {
  let d = 0;
  for (let i = 0; i < a.length; i++) {
    const diff = a[i] - b[i];
    d += diff * diff;
  }
  return d;
}

/**
 * Build the in-memory index from all memories
 * Fetches embeddings for all memory texts and stores them
 */
export async function buildIndex(force = false) {
  if (indexBuilt && !force) {
    return { status: 'already_built', count: indexIds.length };
  }

  const memories = getAllMemories();
  if (memories.length === 0) {
    return { status: 'no_memories', count: 0 };
  }

  // Fetch embeddings in batches to avoid overwhelming Ollama
  const BATCH_SIZE = 10;
  const vectors = [];
  const ids = [];

  for (let i = 0; i < memories.length; i += BATCH_SIZE) {
    const batch = memories.slice(i, i + BATCH_SIZE);
    const batchVectors = await Promise.all(
      batch.map(m => getEmbedding(m.text).catch(() => null))
    );
    
    for (let j = 0; j < batch.length; j++) {
      if (batchVectors[j]) {
        vectors.push(batchVectors[j]);
        ids.push(batch[j].id);
      }
    }
    
    // Set dimension from first successful embedding
    if (indexDim === 0 && vectors.length > 0) {
      indexDim = vectors[0].length;
    }
  }

  if (vectors.length === 0) {
    return { status: 'no_embeddings', count: 0 };
  }

  // Store as flat arrays (compatible with Float32Array)
  indexVectors = vectors;
  indexIds = ids;
  indexBuilt = true;

  return { status: 'built', count: vectors.length, dimension: indexDim };
}

/**
 * Search the in-memory index for top-K nearest neighbors
 * @param {number[]} queryVector - Query embedding vector
 * @param {number} topK - Number of results to return
 * @param {string} metric - 'cosine' or 'l2' (default cosine)
 * @returns {Array<{id: string, score: number}>}
 */
export function searchIndex(queryVector, topK = 10, metric = 'cosine') {
  if (!indexBuilt || indexVectors.length === 0) {
    return [];
  }

  // Compute distances to all vectors
  const results = [];
  for (let i = 0; i < indexVectors.length; i++) {
    let score;
    if (metric === 'l2') {
      score = -l2Squared(queryVector, indexVectors[i]); // Negative L2 (higher = closer)
    } else {
      score = cosineSimilarity(queryVector, indexVectors[i]);
    }
    results.push({ id: indexIds[i], score });
  }

  // Sort by score descending (higher = better for both metrics)
  results.sort((a, b) => b.score - a.score);

  return results.slice(0, topK);
}

/**
 * Convenience: embed query text and search
 */
export async function search(queryText, topK = 10, metric = 'cosine') {
  try {
    const queryVector = await getEmbedding(queryText);
    return searchIndex(queryVector, topK, metric);
  } catch (err) {
    console.error('[faiss_index] search error:', err.message);
    return [];
  }
}

/**
 * Add a single vector to the index
 */
export function addVector(id, vector) {
  if (!indexBuilt) {
    // Initialize dimension on first add
    indexDim = vector.length;
    indexBuilt = true;
  }
  indexVectors.push(vector);
  indexIds.push(id);
}

/**
 * Remove a vector from the index by ID
 */
export function removeById(id) {
  const idx = indexIds.indexOf(id);
  if (idx !== -1) {
    indexVectors.splice(idx, 1);
    indexIds.splice(idx, 1);
    return true;
  }
  return false;
}

/**
 * Clear the entire index
 */
export function clearIndex() {
  indexVectors = [];
  indexIds = [];
  indexDim = 0;
  indexBuilt = false;
}

/**
 * Get index statistics
 */
export function getIndexStats() {
  return {
    built: indexBuilt,
    count: indexIds.length,
    dimension: indexDim,
    memoryEstimateMB: indexBuilt 
      ? (indexVectors.length * indexDim * 4) / (1024 * 1024) 
      : 0,
  };
}

/**
 * BM25 fallback - delegates to bm25.js if vector search unavailable
 * This is used when Ollama is not reachable
 */
export async function bm25Fallback(query, topK = 10) {
  try {
    const { bm25Search } = await import('../bm25.js');
    return bm25Search(query, topK);
  } catch {
    return [];
  }
}

// CLI for testing
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('\n📊 FAISS-like In-Memory Index\n');
  
  buildIndex().then(stats => {
    console.log('Build result:', stats);
    if (stats.count > 0) {
      console.log('\nSearching for "test"...');
      search('test', 3).then(results => {
        console.log('Results:', JSON.stringify(results, null, 2));
      });
    }
  }).catch(console.error);
}

export default {
  buildIndex,
  searchIndex,
  search,
  addVector,
  removeById,
  clearIndex,
  getIndexStats,
  bm25Fallback,
};
