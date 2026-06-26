/**
 * LLM-based reranker for memory search results.
 *
 * After hybrid search retrieves candidates, the reranker uses an LLM
 * to select and reorder the most relevant results for a given query.
 * Gracefully falls back to truncation on any failure.
 */

import type { MemoryConfig, MemorySearchResult } from './types.js';
import { llmCall } from './llm.js';

const DEFAULT_TOP_K = 6;
const DEFAULT_MODEL = 'gpt-4o-mini';
const PREVIEW_CHARS = 300;

export async function rerankResults(
  query: string,
  results: MemorySearchResult[],
  config: MemoryConfig,
  topK?: number,
): Promise<MemorySearchResult[]> {
  const k = topK ?? config.reranker?.maxContextChunks ?? DEFAULT_TOP_K;
  if (results.length <= k) return results;

  const model = config.reranker?.model ?? DEFAULT_MODEL;

  const numbered = results
    .map((r, i) => `[${i + 1}] ${r.entry.value.slice(0, PREVIEW_CHARS)}`)
    .join('\n\n');

  const prompt = `You are a relevance judge. Given a question and numbered context passages, return ONLY the numbers of the ${k} most relevant passages in order of relevance, comma-separated.

Question: ${query}

Passages:
${numbered}

Return ONLY comma-separated numbers (e.g. "3,1,5"). No explanation.`;

  try {
    const resp = await llmCall({ prompt, model, temperature: 0.0, maxTokens: 60 });
    const indices = resp.content
      .match(/\d+/g)
      ?.map(Number)
      .filter(n => n >= 1 && n <= results.length) ?? [];

    if (indices.length === 0) return results.slice(0, k);

    const seen = new Set<number>();
    const reranked: MemorySearchResult[] = [];
    for (const idx of indices) {
      if (!seen.has(idx) && reranked.length < k) {
        seen.add(idx);
        reranked.push(results[idx - 1]);
      }
    }
    for (let i = 0; i < results.length && reranked.length < k; i++) {
      if (!seen.has(i + 1)) reranked.push(results[i]);
    }
    return reranked;
  } catch {
    return results.slice(0, k);
  }
}
