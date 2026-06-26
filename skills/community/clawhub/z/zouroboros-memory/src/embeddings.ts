/**
 * Vector embeddings for semantic search
 *
 * ECC-010: Memory Explosion Throttling
 *   - Rate limiting: max MAX_EMBEDDINGS_PER_MINUTE per conversation (sliding window)
 *   - Dedup: same content hash within DEDUP_COOLDOWN_MS returns cached embedding
 *   - Tail sampling: when rate limited, return last cached embedding for the conversation
 *   - Metrics: throttleCount / dedupCount exported for observability
 */

import { createHash } from 'node:crypto';
import type { MemoryConfig } from './types.js';

// ─── ECC-010 Constants ────────────────────────────────────────────────────────

const MAX_EMBEDDINGS_PER_MINUTE = 20;
const DEDUP_COOLDOWN_MS = 300_000; // 5 minutes
const TAIL_SAMPLE_K = 10;          // keep last K embeddings per conversation when limited

// ─── ECC-010 Module-Scoped State ─────────────────────────────────────────────

interface RateWindow {
  count: number;
  windowStart: number;
  /** Tail buffer: last K embeddings produced in this window */
  tail: number[][];
}

interface DedupEntry {
  embedding: number[];
  expiresAt: number;
}

/** Per-conversation sliding rate window. Key: conversationId. */
const _rateWindows = new Map<string, RateWindow>();

/** Per-content dedup cache. Key: SHA-256 hex of text. */
const _dedupCache = new Map<string, DedupEntry>();

/** Exported metrics counters — reset only on process restart. */
export const throttleMetrics = {
  throttleCount: 0,
  dedupCount: 0,
};

function contentHash(text: string): string {
  return createHash('sha256').update(text).digest('hex');
}

/**
 * ECC-010: Check rate limit for a conversation window.
 * Returns the tail-sampled embedding if over limit, or null if under limit.
 */
function checkRateLimit(conversationId: string): number[] | null {
  const now = Date.now();
  let window = _rateWindows.get(conversationId);

  if (!window || now - window.windowStart > 60_000) {
    window = { count: 0, windowStart: now, tail: [] };
    _rateWindows.set(conversationId, window);
  }

  if (window.count >= MAX_EMBEDDINGS_PER_MINUTE) {
    // Return tail sample (last produced in this window) or empty fallback
    const sample = window.tail[window.tail.length - 1] ?? [];
    throttleMetrics.throttleCount++;
    return sample;
  }

  return null;
}

/** ECC-010: Record a produced embedding in the rate window tail buffer. */
function recordInWindow(conversationId: string, embedding: number[]): void {
  const window = _rateWindows.get(conversationId);
  if (!window) return;
  window.count++;
  window.tail.push(embedding);
  if (window.tail.length > TAIL_SAMPLE_K) {
    window.tail.shift();
  }
}

/** ECC-010: Reset throttle state (for testing). */
export function resetThrottleState(): void {
  _rateWindows.clear();
  _dedupCache.clear();
  throttleMetrics.throttleCount = 0;
  throttleMetrics.dedupCount = 0;
}

// ─── Internal Ollama call ─────────────────────────────────────────────────────

async function _generateEmbeddingFromOllama(
  text: string,
  config: MemoryConfig,
): Promise<number[]> {
  const response = await fetch(`${config.ollamaUrl}/api/embeddings`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model: config.ollamaModel, prompt: text }),
  });

  if (!response.ok) {
    throw new Error(`Ollama error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json() as { embedding: number[] };
  return data.embedding;
}

/**
 * Generate embeddings for text using Ollama.
 *
 * ECC-010: Throttling applied when conversationId is provided:
 *   1. Dedup check — returns cached embedding if same content seen within 5 min
 *   2. Rate limit check — returns tail-sampled embedding if > 20/min per conversation
 *   3. Ollama call — only reached if dedup and rate limit both pass
 *
 * @param conversationId  Optional. When provided, enables per-conversation throttling.
 */
export async function generateEmbedding(
  text: string,
  config: MemoryConfig,
  conversationId?: string,
): Promise<number[]> {
  if (!config.vectorEnabled) {
    throw new Error('Vector search is disabled in configuration');
  }

  if (conversationId) {
    // Layer 1: Dedup check
    const hash = contentHash(text);
    const cached = _dedupCache.get(hash);
    if (cached && Date.now() < cached.expiresAt) {
      throttleMetrics.dedupCount++;
      return cached.embedding;
    }

    // Layer 2: Rate limit check (tail sampling on overflow)
    const sampled = checkRateLimit(conversationId);
    if (sampled !== null) {
      return sampled;
    }

    // Layer 3: Produce embedding and cache it
    const embedding = await _generateEmbeddingFromOllama(text, config);
    _dedupCache.set(hash, { embedding, expiresAt: Date.now() + DEDUP_COOLDOWN_MS });
    recordInWindow(conversationId, embedding);
    return embedding;
  }

  // No conversationId: bypass throttling (internal/system calls)
  return _generateEmbeddingFromOllama(text, config);
}

/**
 * Generate a hypothetical answer using Ollama's generate endpoint.
 * Used by HyDE to create an ideal document for embedding.
 */
export async function generateHypotheticalAnswer(
  query: string,
  config: MemoryConfig,
  options: { model?: string; maxTokens?: number } = {}
): Promise<string> {
  const model = options.model ?? 'llama3';
  const prompt = `Answer the following question concisely in 2-3 sentences as if you had perfect knowledge. Do not hedge or say "I don't know".\n\nQuestion: ${query}\n\nAnswer:`;

  const response = await fetch(`${config.ollamaUrl}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model,
      prompt,
      stream: false,
      options: { num_predict: options.maxTokens ?? 150 },
    }),
  });

  if (!response.ok) {
    throw new Error(`Ollama generate error: ${response.status} ${response.statusText}`);
  }

  const data = await response.json() as { response: string };
  return data.response.trim();
}

/**
 * Generate HyDE (Hypothetical Document Expansion) embeddings.
 *
 * 1. Embeds the original query.
 * 2. Uses an LLM to generate a hypothetical ideal answer.
 * 3. Embeds the hypothetical answer.
 * 4. Returns both embeddings so the caller can blend them.
 *
 * Falls back to duplicating the original embedding if generation fails.
 */
export async function generateHyDEExpansion(
  query: string,
  config: MemoryConfig,
  options: { generationModel?: string; maxTokens?: number } = {}
): Promise<{ original: number[]; expanded: number[]; hypothetical: string }> {
  const original = await generateEmbedding(query, config);

  let hypothetical: string;
  try {
    hypothetical = await generateHypotheticalAnswer(query, config, {
      model: options.generationModel,
      maxTokens: options.maxTokens,
    });
  } catch {
    return { original, expanded: original, hypothetical: query };
  }

  const expanded = await generateEmbedding(hypothetical, config);
  return { original, expanded, hypothetical };
}

/**
 * Blend two embeddings by weighted average.
 * Default: 40% original query, 60% hypothetical answer (HyDE sweet spot).
 */
export function blendEmbeddings(
  a: number[],
  b: number[],
  weightA: number = 0.4
): number[] {
  if (a.length !== b.length) {
    throw new Error('Embeddings must have the same dimension');
  }
  const weightB = 1 - weightA;
  return a.map((val, i) => val * weightA + b[i] * weightB);
}

/**
 * Calculate cosine similarity between two vectors
 */
export function cosineSimilarity(a: number[], b: number[]): number {
  if (a.length !== b.length) {
    throw new Error('Vectors must have the same length');
  }

  let dotProduct = 0;
  let normA = 0;
  let normB = 0;

  for (let i = 0; i < a.length; i++) {
    dotProduct += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }

  return dotProduct / (Math.sqrt(normA) * Math.sqrt(normB));
}

/**
 * Serialize embedding for SQLite storage
 */
export function serializeEmbedding(embedding: number[]): Buffer {
  // Convert to Float32Array and then to Buffer
  const floatArray = new Float32Array(embedding);
  return Buffer.from(floatArray.buffer);
}

/**
 * Deserialize embedding from SQLite storage
 */
export function deserializeEmbedding(buffer: Buffer): number[] {
  const floatArray = new Float32Array(buffer.buffer, buffer.byteOffset, buffer.length / 4);
  return Array.from(floatArray);
}

/**
 * Check if Ollama is available
 */
export async function checkOllamaHealth(config: MemoryConfig): Promise<boolean> {
  try {
    const response = await fetch(`${config.ollamaUrl}/api/tags`, {
      method: 'GET',
      signal: AbortSignal.timeout(5000),
    });
    return response.ok;
  } catch {
    return false;
  }
}

/**
 * List available models from Ollama
 */
export async function listAvailableModels(config: MemoryConfig): Promise<string[]> {
  try {
    const response = await fetch(`${config.ollamaUrl}/api/tags`);
    if (!response.ok) return [];

    const data = await response.json() as { models?: { name: string }[] };
    return data.models?.map(m => m.name) || [];
  } catch {
    return [];
  }
}
