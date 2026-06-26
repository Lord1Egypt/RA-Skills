/**
 * 48h Reconsolidation
 * 
 * Periodically refresh memories that haven't been refreshed in >48h:
 * - Regenerate summary via LLM
 * - Regenerate embedding
 * - Update last_refresh timestamp
 * 
 * Throttle: max 5 memories per reconsolidation run
 */

import { config } from '../config.js';
import { loadMemories, saveMemories } from '../storage.js';
import { EmbeddingClient } from '../embedding_providers.js';

const OLLAMA_HOST = config.llmProviders?.find(p => p.name === 'ollama')?.baseURL
  || process.env.OLLAMA_BASE_URL
  || process.env.OLLAMA_HOST
  || 'http://192.168.2.155:11434';

const OLLAMA_MODEL = config.llmProviders?.find(p => p.name === 'ollama')?.model
  || process.env.OLLAMA_LLM_MODEL
  || 'qwen2.5:7b';

const REFRESH_INTERVAL_MS = 48 * 60 * 60 * 1000; // 48 hours
const MAX_PER_RUN = 5; // Throttle: max 5 per call

// ============================================================
// Refresh stats (in-memory, survives across calls within same process)
// ============================================================

const refreshStats = {
  total_refresh_count: 0,
  last_refresh_time: null, // ISO timestamp
  last_run_time: null,
  errors: [],
};

// ============================================================
// Main reconsolidation function
// ============================================================

/**
 * Check all memories and reconsolidate those older than 48h
 * 
 * @param {number} [maxItems=5] - Max items to refresh per call (throttle)
 * @returns {Promise<object>} - Summary of what was done
 */
export async function checkAndReconsolidate(maxItems = MAX_PER_RUN) {
  const memories = await loadMemories();
  if (!memories || memories.length === 0) {
    return { refreshed: 0, skipped: 0, errors: [], message: 'No memories found' };
  }

  const now = Date.now();
  const cutoff = now - REFRESH_INTERVAL_MS;

  // Find memories needing refresh
  const needsRefresh = memories.filter((m) => {
    const lastRefresh = m.last_refresh || m.updated_at || m.created_at || 0;
    return lastRefresh < cutoff;
  });

  if (needsRefresh.length === 0) {
    return {
      refreshed: 0,
      skipped: 0,
      total: memories.length,
      message: 'No memories need refresh',
    };
  }

  // Respect throttle limit
  const toRefresh = needsRefresh.slice(0, maxItems);
  const errors = [];

  const refreshedIds = [];

  for (const memory of toRefresh) {
    try {
      const updated = await reconsolidateMemory(memory);
      if (updated) {
        // Update in-place in the memories array
        const idx = memories.findIndex((m) => m.id === memory.id);
        if (idx !== -1) {
          memories[idx] = updated;
        }
        refreshedIds.push(memory.id);
      }
    } catch (err) {
      console.warn(`[Reconsolidate] Failed to refresh memory ${memory.id}: ${err.message}`);
      errors.push({ id: memory.id, error: err.message });
    }
  }

  // Save updated memories
  if (refreshedIds.length > 0) {
    saveMemories(memories);
  }

  // Update stats
  refreshStats.total_refresh_count += refreshedIds.length;
  refreshStats.last_refresh_time = new Date().toISOString();
  refreshStats.last_run_time = new Date().toISOString();
  refreshStats.errors = errors.slice(-10); // keep last 10 errors

  return {
    refreshed: refreshedIds.length,
    skipped: needsRefresh.length - refreshedIds.length,
    total: memories.length,
    refreshed_ids: refreshedIds,
    errors,
    message: `Refreshed ${refreshedIds.length} memories, skipped ${needsRefresh.length - refreshedIds.length}`,
  };
}

// ============================================================
// Single memory reconsolidation
// ============================================================

/**
 * Reconsolidate a single memory:
 * - Regenerate summary via LLM
 * - Regenerate embedding
 * - Update timestamp
 * 
 * @param {object} memory - Memory object
 * @returns {Promise<object>} - Updated memory
 */
export async function reconsolidateMemory(memory) {
  const text = memory.text || memory.content || '';

  if (!text || text.trim() === '') {
    // Nothing to reconsolidate
    return {
      ...memory,
      last_refresh: Date.now(),
    };
  }

  // Step 1: Regenerate summary via LLM
  let summary = memory.summary || '';
  try {
    summary = await generateSummary(text);
  } catch (err) {
    console.warn(`[Reconsolidate] Summary generation failed for ${memory.id}: ${err.message}`);
    // Keep existing summary on failure
  }

  // Step 2: Regenerate embedding
  let embedding = memory.embedding || null;
  try {
    const embedClient = new EmbeddingClient();
    embedding = await embedClient.embed(text);
  } catch (err) {
    console.warn(`[Reconsolidate] Embedding failed for ${memory.id}: ${err.message}`);
    // Keep existing embedding on failure
  }

  // Step 3: Return updated memory
  const updated = {
    ...memory,
    summary,
    embedding,
    last_refresh: Date.now(),
    updated_at: Date.now(),
  };

  return updated;
}

// ============================================================
// Summary generator via Ollama LLM
// ============================================================

/**
 * Generate a concise summary of text using Ollama LLM
 * @param {string} text
 * @returns {Promise<string>}
 */
async function generateSummary(text) {
  const prompt = `请为以下记忆生成一段简洁的摘要（50字以内），只输出摘要内容：

${text.slice(0, 2000)}

摘要：`; // 中文 prompt since the user appears to be Chinese

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
        temperature: 0.3,
        num_predict: 100,
      },
    }),
    signal: AbortSignal.timeout(60000),
  });

  if (!response.ok) {
    throw new Error(`Ollama returned HTTP ${response.status}`);
  }

  const data = await response.json();
  const summary = (data?.message?.content || '').trim();

  return summary;
}

// ============================================================
// Stats getter
// ============================================================

/**
 * Get reconsolidation statistics
 * @returns {object}
 */
export function getReconsolidateStats() {
  return {
    total_refresh_count: refreshStats.total_refresh_count,
    last_refresh_time: refreshStats.last_refresh_time,
    last_run_time: refreshStats.last_run_time,
    max_per_run: MAX_PER_RUN,
    refresh_interval_hours: 48,
    recent_errors: refreshStats.errors,
  };
}

export default { checkAndReconsolidate, reconsolidateMemory, getReconsolidateStats };
