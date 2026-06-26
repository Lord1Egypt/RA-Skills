/**
 * LLM-based Cross-Encoder Rerank
 * 
 * Uses Ollama LLM to score query-memory relevance,
 * returns topK results sorted by LLM-assigned scores.
 * 
 * Fallback: if LLM unavailable, returns original order.
 */

import { config } from '../config.js';

// Ollama config - matches unified-memory's provider setup
const OLLAMA_HOST = config.llmProviders?.find(p => p.name === 'ollama')?.baseURL
  || process.env.OLLAMA_BASE_URL
  || process.env.OLLAMA_HOST
  || 'http://192.168.2.155:11434';

const OLLAMA_MODEL = config.llmProviders?.find(p => p.name === 'ollama')?.model
  || process.env.OLLAMA_LLM_MODEL
  || 'qwen2.5:7b';

// ============================================================
// Core rerank function
// ============================================================

/**
 * Rerank candidates using LLM relevance scoring
 * 
 * @param {string} query - Search query
 * @param {Array<object>} candidates - Memory objects with id, text, summary fields
 * @param {number} topK - Number of results to return
 * @returns {Promise<Array<object>>} - Sorted candidates (descending by relevance score)
 */
export async function rerankWithLLM(query, candidates, topK = 10) {
  if (!candidates || candidates.length === 0) return [];
  if (!query || query.trim() === '') return candidates.slice(0, topK);

  // If only 1 candidate, no need to rerank
  if (candidates.length === 1) return candidates;

  const prompt = buildRerankPrompt(query, candidates);

  try {
    const scores = await callOllamaForScores(prompt, candidates.length);

    if (!scores || scores.length !== candidates.length) {
      // LLM returned wrong count - fallback
      console.warn('[Rerank] LLM returned unexpected score count, using original order');
      return candidates.slice(0, topK);
    }

    // Attach scores and sort descending
    const scored = candidates.map((c, i) => ({
      ...c,
      _rerank_score: scores[i] ?? 0,
    }));

    scored.sort((a, b) => (b._rerank_score ?? 0) - (a._rerank_score ?? 0));

    return scored.slice(0, topK);
  } catch (err) {
    console.warn(`[Rerank] LLM rerank failed: ${err.message}, returning original order`);
    return candidates.slice(0, topK);
  }
}

// ============================================================
// Prompt builder
// ============================================================

/**
 * Build the reranking prompt for the LLM
 * @param {string} query
 * @param {Array<object>} candidates
 * @returns {string}
 */
function buildRerankPrompt(query, candidates) {
  const candidateList = candidates.map((c, i) => {
    const text = (c.summary || c.text || '').slice(0, 500);
    const category = c.category || '';
    const tags = Array.isArray(c.tags) ? c.tags.join(', ') : '';
    return `[${i}] ${category ? `(${category}) ` : ''}${tags ? `[${tags}] ` : ''}${text}`;
  }).join('\n');

  return `You are a relevance scoring assistant. Given a query and a list of memories, score each memory's relevance to the query on a scale of 0.0 to 1.0.

Query: "${query}"

Memories:
${candidateList}

Output a JSON array of exactly ${candidates.length} float scores (0.0 = completely irrelevant, 1.0 = highly relevant). Return ONLY the JSON array, no explanation. Example: [0.85, 0.32, 0.91, 0.11]`;
}

// ============================================================
// Ollama LLM caller
// ============================================================

/**
 * Call Ollama chat API to get relevance scores
 * @param {string} prompt
 * @param {number} expectedCount
 * @returns {Promise<number[]>}
 */
async function callOllamaForScores(prompt, expectedCount) {
  const response = await fetch(`${OLLAMA_HOST}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: OLLAMA_MODEL,
      messages: [
        {
          role: 'user',
          content: prompt,
        },
      ],
      stream: false,
      options: {
        temperature: 0.1, // Low temperature for consistent scoring
        num_predict: 512,
      },
    }),
    signal: AbortSignal.timeout(60000),
  });

  if (!response.ok) {
    throw new Error(`Ollama returned HTTP ${response.status}`);
  }

  const data = await response.json();
  const rawContent = data?.message?.content || '';

  return parseScoreArray(rawContent, expectedCount);
}

// ============================================================
// Score parser
// ============================================================

/**
 * Parse JSON float array from LLM output
 * @param {string} raw
 * @param {number} expectedCount
 * @returns {number[]}
 */
function parseScoreArray(raw, expectedCount) {
  // Try to find JSON array in the output
  const match = raw.match(/\[\s*([\d.,\s]+)\s*\]/);
  if (!match) {
    throw new Error('No JSON array found in LLM output');
  }

  try {
    const scores = JSON.parse(match[0]);
    if (!Array.isArray(scores)) throw new Error('Not an array');
    return scores.map((s) => Math.max(0, Math.min(1, Number(s) || 0)));
  } catch {
    throw new Error('Failed to parse score array');
  }
}

export default { rerankWithLLM };
