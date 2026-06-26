/**
 * Fact storage and retrieval operations
 */

import { randomUUID } from 'crypto';
import { getDatabase } from './database.js';
import { generateEmbedding, serializeEmbedding, deserializeEmbedding, generateHyDEExpansion, blendEmbeddings } from './embeddings.js';
import { invalidateGraphCache } from './graph.js';
import { rerankResults } from './reranker.js';
import type { MemoryConfig, MemoryEntry, MemorySearchResult, DecayClass } from './types.js';

// Decay class TTLs in seconds
const TTL_DEFAULTS: Record<DecayClass, number | null> = {
  permanent: null,
  long: 365 * 24 * 3600,
  medium: 90 * 24 * 3600,
  short: 30 * 24 * 3600,
};

type Category = 'preference' | 'fact' | 'decision' | 'convention' | 'other' | 'reference' | 'project';

const DEDUP_SUBSTR_LEN = 60;

/**
 * Deduplicate search results by checking for 60-char substring overlap.
 * Keeps the higher-scored entry when overlap is found.
 */
function deduplicateResults(results: MemorySearchResult[]): MemorySearchResult[] {
  const seen: string[] = [];
  return results.filter(r => {
    const val = r.entry.value;
    const substr = val.slice(0, DEDUP_SUBSTR_LEN);
    if (seen.some(s => s === substr || val.includes(s) || s.includes(substr.slice(0, 40)))) {
      return false;
    }
    seen.push(substr);
    return true;
  });
}

interface StoreFactInput {
  entity: string;
  key?: string;
  value: string;
  persona?: string;
  category?: Category;
  decay?: DecayClass;
  importance?: number;
  source?: string;
  confidence?: number;
  metadata?: Record<string, unknown>;
}

/**
 * Store a fact in memory
 */
export async function storeFact(
  input: StoreFactInput,
  config: MemoryConfig
): Promise<MemoryEntry> {
  const db = getDatabase();
  const id = randomUUID();
  const now = Math.floor(Date.now() / 1000);
  const decay = input.decay || 'medium';
  const ttl = TTL_DEFAULTS[decay];
  const expiresAt = ttl ? now + ttl : null;

  const text = input.key
    ? `${input.entity} ${input.key} ${input.value}`
    : `${input.entity} ${input.value}`;

  const entry: MemoryEntry = {
    id,
    entity: input.entity,
    key: input.key || null,
    value: input.value,
    decay,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };

  // Insert fact
  db.run(
    `INSERT INTO facts (id, persona, entity, key, value, text, category, decay_class, importance, source,
                        created_at, expires_at, confidence, metadata)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [
      id,
      input.persona || 'shared',
      input.entity,
      input.key || null,
      input.value,
      text,
      input.category || 'fact',
      decay,
      input.importance || 1.0,
      input.source || 'manual',
      now,
      expiresAt,
      input.confidence || 1.0,
      input.metadata ? JSON.stringify(input.metadata) : null,
    ]
  );

  // Generate and store embedding if vector search is enabled
  if (config.vectorEnabled) {
    try {
      const embedding = await generateEmbedding(text, config);
      const serialized = serializeEmbedding(embedding);

      db.run(
        'INSERT INTO fact_embeddings (fact_id, embedding, model) VALUES (?, ?, ?)',
        [id, serialized, config.ollamaModel]
      );
    } catch (error) {
      console.warn('Failed to generate embedding:', error);
    }
  }

  invalidateGraphCache();
  return entry;
}

/**
 * Search facts by exact match or keyword
 */
export function searchFacts(
  query: string,
  options: {
    entity?: string;
    category?: string;
    persona?: string;
    limit?: number;
  } = {}
): MemoryEntry[] {
  const db = getDatabase();
  const { entity, category, persona, limit = 10 } = options;

  let sql = `
    SELECT id, persona, entity, key, value, category, decay_class as decayClass,
           importance, source, created_at as createdAt, expires_at as expiresAt,
           confidence, metadata
    FROM facts
    WHERE (text LIKE ? OR entity LIKE ? OR value LIKE ?)
      AND (expires_at IS NULL OR expires_at > strftime('%s', 'now'))
  `;
  const params: (string | number)[] = [`%${query}%`, `%${query}%`, `%${query}%`];

  if (persona) {
    sql += ' AND (persona = ? OR persona = ?)';
    params.push(persona, 'shared');
  }

  if (entity) {
    sql += ' AND entity = ?';
    params.push(entity);
  }

  if (category) {
    sql += ' AND category = ?';
    params.push(category);
  }

  sql += ' ORDER BY importance DESC, created_at DESC LIMIT ?';
  params.push(limit);

  const rows = db.query(sql).all(...params) as Array<{
    id: string;
    entity: string;
    key: string | null;
    value: string;
    category: string;
    decayClass: DecayClass;
    importance: number;
    source: string;
    createdAt: number;
    expiresAt: number | null;
    confidence: number;
    metadata: string | null;
  }>;

  return rows.map(row => ({
    id: row.id,
    entity: row.entity,
    key: row.key,
    value: row.value,
    decay: row.decayClass,
    createdAt: new Date(row.createdAt * 1000).toISOString(),
    updatedAt: new Date(row.createdAt * 1000).toISOString(),
    tags: row.category ? [row.category] : undefined,
  }));
}

/**
 * Search facts using vector similarity
 */
export async function searchFactsVector(
  query: string,
  config: MemoryConfig,
  options: {
    limit?: number;
    threshold?: number;
    useHyDE?: boolean;
    persona?: string;
  } = {}
): Promise<MemorySearchResult[]> {
  if (!config.vectorEnabled) {
    throw new Error('Vector search is disabled. Enable it in configuration.');
  }

  const db = getDatabase();
  const { limit = 10, threshold = 0.7, useHyDE } = options;

  // Generate query embedding, optionally with HyDE expansion
  let queryEmbedding: number[];
  const shouldUseHyDE = useHyDE ?? config.hydeExpansion;

  if (shouldUseHyDE) {
    const hyde = await generateHyDEExpansion(query, config);
    queryEmbedding = blendEmbeddings(hyde.original, hyde.expanded);
  } else {
    queryEmbedding = await generateEmbedding(query, config);
  }

  // Get all facts with embeddings
  let factsSql = `
    SELECT f.id, f.entity, f.key, f.value, f.category, f.decay_class as decayClass,
           f.importance, f.created_at as createdAt, f.persona, fe.embedding
    FROM facts f
    JOIN fact_embeddings fe ON f.id = fe.fact_id
    WHERE (f.expires_at IS NULL OR f.expires_at > strftime('%s', 'now'))
  `;
  const factsParams: string[] = [];
  if (options.persona) {
    factsSql += ' AND (f.persona = ? OR f.persona = ?)';
    factsParams.push(options.persona, 'shared');
  }

  const rows = (factsParams.length > 0
    ? db.query(factsSql).all(...factsParams)
    : db.query(factsSql).all()
  ) as Array<{
    id: string;
    entity: string;
    key: string | null;
    value: string;
    category: string;
    decayClass: DecayClass;
    importance: number;
    createdAt: number;
    embedding: Buffer;
  }>;

  // Calculate similarity and filter
  const { cosineSimilarity } = await import('./embeddings.js');

  const results: MemorySearchResult[] = rows
    .map(row => {
      const embedding = deserializeEmbedding(row.embedding);
      const similarity = cosineSimilarity(queryEmbedding, embedding);

      return {
        entry: {
          id: row.id,
          entity: row.entity,
          key: row.key,
          value: row.value,
          decay: row.decayClass,
          createdAt: new Date(row.createdAt * 1000).toISOString(),
          updatedAt: new Date(row.createdAt * 1000).toISOString(),
          tags: row.category ? [row.category] : undefined,
        },
        score: similarity,
        matchType: 'semantic' as const,
      };
    })
    .filter(r => r.score >= threshold)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);

  return results;
}

/**
 * Hybrid search combining exact and vector search
 */
export async function searchFactsHybrid(
  query: string,
  config: MemoryConfig,
  options: {
    limit?: number;
    vectorWeight?: number;
    rerank?: boolean;
    persona?: string;
  } = {}
): Promise<MemorySearchResult[]> {
  const { limit = 10, vectorWeight = 0.7, persona } = options;
  const shouldRerank = options.rerank ?? config.reranker?.enabled ?? false;

  // When reranking, fetch more candidates for the reranker to choose from
  const fetchLimit = shouldRerank ? Math.max(limit * 2, 20) : limit;

  // Get exact matches
  const exactMatches = searchFacts(query, { limit: fetchLimit * 2, persona });

  // Get vector matches
  let vectorMatches: MemorySearchResult[] = [];
  if (config.vectorEnabled) {
    try {
      vectorMatches = await searchFactsVector(query, config, { limit: fetchLimit * 2, persona });
    } catch (error) {
      console.warn('Vector search failed:', error);
    }
  }

  // RRF fusion
  const k = 60;
  const scores = new Map<string, { entry: MemoryEntry; score: number }>();

  // Score exact matches
  exactMatches.forEach((entry, rank) => {
    const id = entry.id;
    const rrfScore = 1 / (k + rank + 1);
    scores.set(id, { entry, score: rrfScore * (1 - vectorWeight) });
  });

  // Score vector matches
  vectorMatches.forEach((result, rank) => {
    const id = result.entry.id;
    const rrfScore = 1 / (k + rank + 1);
    const existing = scores.get(id);

    if (existing) {
      existing.score += rrfScore * vectorWeight;
    } else {
      scores.set(id, { entry: result.entry, score: rrfScore * vectorWeight });
    }
  });

  // Sort by combined score
  let fused: MemorySearchResult[] = Array.from(scores.values())
    .sort((a, b) => b.score - a.score)
    .slice(0, fetchLimit)
    .map(r => ({
      entry: r.entry,
      score: r.score,
      matchType: 'hybrid' as const,
    }));

  // Deduplicate by 60-char substring overlap
  fused = deduplicateResults(fused);

  // LLM reranking pass
  if (shouldRerank && fused.length > 0) {
    fused = await rerankResults(query, fused, config, limit);
  } else {
    fused = fused.slice(0, limit);
  }

  return fused;
}

/**
 * Get a fact by ID
 */
export function getFact(id: string): MemoryEntry | null {
  const db = getDatabase();

  const row = db.query(`
    SELECT id, entity, key, value, category, decay_class as decayClass,
           importance, source, created_at as createdAt, expires_at as expiresAt,
           confidence, metadata
    FROM facts
    WHERE id = ?
  `).get(id) as {
    id: string;
    entity: string;
    key: string | null;
    value: string;
    category: string;
    decayClass: DecayClass;
    importance: number;
    source: string;
    createdAt: number;
    expiresAt: number | null;
    confidence: number;
    metadata: string | null;
  } | null;

  if (!row) return null;

  return {
    id: row.id,
    entity: row.entity,
    key: row.key,
    value: row.value,
    decay: row.decayClass,
    createdAt: new Date(row.createdAt * 1000).toISOString(),
    updatedAt: new Date(row.createdAt * 1000).toISOString(),
    tags: row.category ? [row.category] : undefined,
  };
}

/**
 * Delete a fact by ID
 */
export function deleteFact(id: string): boolean {
  const db = getDatabase();
  const result = db.run('DELETE FROM facts WHERE id = ?', [id]);
  if (result.changes > 0) invalidateGraphCache();
  return result.changes > 0;
}

/**
 * Update fact access time
 */
export function touchFact(id: string): void {
  const db = getDatabase();
  const now = Math.floor(Date.now() / 1000);
  db.run('UPDATE facts SET last_accessed = ? WHERE id = ?', [now, id]);
}

/**
 * Clean up expired facts
 */
export function cleanupExpiredFacts(): number {
  const db = getDatabase();
  const result = db.run(`
    DELETE FROM facts
    WHERE expires_at IS NOT NULL
      AND expires_at < strftime('%s', 'now')
  `);
  if (result.changes > 0) invalidateGraphCache();
  return result.changes;
}
