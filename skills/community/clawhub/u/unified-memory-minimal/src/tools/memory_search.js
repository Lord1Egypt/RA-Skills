/**
 * memory_search tool: Agent-callable tool for searching L1 memory records.
 *
 * Supports three search strategies with automatic degradation:
 *   1. **hybrid** (default) — FTS5 keyword + vector embedding in parallel, merged via RRF.
 *   2. **embedding** — pure vector similarity
 *   3. **fts** — pure FTS5 keyword search
 */

const TAG = "[unified-memory][tdai_memory_search]";
const RRF_K = 60;

/**
 * @typedef {Object} MemorySearchResultItem
 * @property {string} id
 * @property {string} content
 * @property {string} type
 * @property {number} priority
 * @property {string} scene_name
 * @property {number} score
 * @property {string} created_at
 * @property {string} updated_at
 */

/**
 * @typedef {Object} MemorySearchResult
 * @property {MemorySearchResultItem[]} results
 * @property {number} total
 * @property {string} strategy
 * @property {string} [message]
 */

/**
 * @typedef {Object} ToolLogger
 * @property {(message: string) => void} [debug]
 * @property {(message: string) => void} info
 * @property {(message: string) => void} warn
 * @property {(message: string) => void} error
 */

/**
 * @param {MemorySearchResultItem[]} ...lists
 * @returns {MemorySearchResultItem[]}
 */
function rrfMergeL1(...lists) {
  const map = new Map();

  for (const list of lists) {
    for (let rank = 0; rank < list.length; rank++) {
      const item = list[rank];
      const score = 1 / (RRF_K + rank + 1);
      const existing = map.get(item.id);
      if (existing) {
        existing.rrfScore += score;
      } else {
        map.set(item.id, { item, rrfScore: score });
      }
    }
  }

  return [...map.values()]
    .sort((a, b) => b.rrfScore - a.rrfScore)
    .map(({ item, rrfScore }) => ({ ...item, score: rrfScore }));
}

/**
 * @param {Object} params
 * @param {string} params.query
 * @param {number} params.limit
 * @param {string} [params.type]
 * @param {string} [params.scene]
 * @param {Object} [params.vectorStore]
 * @param {Object} [params.embeddingService]
 * @param {ToolLogger} [params.logger]
 * @returns {Promise<MemorySearchResult>}
 */
export async function executeMemorySearch(params) {
  const { query, limit, type: typeFilter, scene: sceneFilter, vectorStore, embeddingService, logger } = params;

  logger?.debug?.(
    `${TAG} CALLED: query="${query.slice(0, 100)}", limit=${limit}, ` +
    `typeFilter=${typeFilter ?? "(none)"}, sceneFilter=${sceneFilter ?? "(none)"}`,
  );

  if (!query || query.trim().length === 0) {
    return { results: [], total: 0, strategy: "none" };
  }

  if (!vectorStore) {
    logger?.warn?.(`${TAG} VectorStore not available`);
    return { results: [], total: 0, strategy: "none" };
  }

  const hasEmbedding = !!embeddingService;
  const hasFts = vectorStore.isFtsAvailable?.() ?? false;

  if (!hasEmbedding && !hasFts) {
    return {
      results: [],
      total: 0,
      strategy: "none",
      message: "Embedding service is not configured and FTS is not available. Memory search requires an embedding provider or FTS5 support.",
    };
  }

  const candidateK = limit * 3;

  const [ftsItems, vecItems] = await Promise.all([
    (async () => {
      if (!hasFts) return [];
      try {
        const ftsQuery = buildFtsQuery(query);
        if (!ftsQuery) return [];
        const ftsResults = vectorStore.ftsSearchL1(ftsQuery, candidateK);
        return ftsResults.map((r) => ({
          id: r.record_id,
          content: r.content,
          type: r.type,
          priority: r.priority,
          scene_name: r.scene_name,
          score: r.score,
          created_at: r.timestamp_start,
          updated_at: r.timestamp_end,
        }));
      } catch (err) {
        logger?.warn?.(`${TAG} [fts] FTS5 search failed: ${err instanceof Error ? err.message : String(err)}`);
        return [];
      }
    })(),

    (async () => {
      if (!hasEmbedding) return [];
      try {
        const queryEmbedding = await embeddingService.embed(query);
        const vecResults = vectorStore.search(queryEmbedding, candidateK);
        return vecResults.map((r) => ({
          id: r.record_id,
          content: r.content,
          type: r.type,
          priority: r.priority,
          scene_name: r.scene_name,
          score: r.score,
          created_at: r.timestamp_start,
          updated_at: r.timestamp_end,
        }));
      } catch (err) {
        logger?.warn?.(`${TAG} [vec] Embedding search failed: ${err instanceof Error ? err.message : String(err)}`);
        return [];
      }
    })(),
  ]);

  const ftsOk = ftsItems.length > 0;
  const vecOk = vecItems.length > 0;
  let strategy;

  if (ftsOk && vecOk) {
    strategy = "hybrid";
  } else if (vecOk) {
    strategy = "embedding";
  } else if (ftsOk) {
    strategy = "fts";
  } else {
    return { results: [], total: 0, strategy: hasEmbedding ? "embedding" : "fts" };
  }

  let results;
  if (strategy === "hybrid") {
    results = rrfMergeL1(ftsItems, vecItems);
  } else {
    results = ftsOk ? ftsItems : vecItems;
  }

  if (typeFilter) {
    results = results.filter((r) => r.type === typeFilter);
  }
  if (sceneFilter) {
    const normalizedScene = sceneFilter.toLowerCase();
    results = results.filter((r) => r.scene_name.toLowerCase().includes(normalizedScene));
  }

  const trimmed = results.slice(0, limit);

  return { results: trimmed, total: trimmed.length, strategy };
}

/**
 * @param {MemorySearchResult} result
 * @returns {string}
 */
export function formatSearchResponse(result) {
  if (result.message) return result.message;
  if (result.results.length === 0) return "No matching memories found.";

  const lines = [`Found ${result.total} matching memories:`, ""];

  for (const item of result.results) {
    const scoreStr = typeof item.score === "number" ? ` (score: ${item.score.toFixed(3)})` : "";
    const sceneStr = item.scene_name ? ` [scene: ${item.scene_name}]` : "";
    const priorityStr = item.priority >= 0 ? ` (priority: ${item.priority})` : " (global instruction)";
    lines.push(`- **[${item.type}]**${priorityStr}${sceneStr}${scoreStr}`);
    lines.push(`  ${item.content}`);
    lines.push("");
  }

  return lines.join("\n");
}

/**
 * @param {string} text
 * @returns {string}
 */
function buildFtsQuery(text) {
  const words = text.match(/[\w\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+/g);
  if (!words || words.length === 0) return "";
  return words.slice(0, 10).join(" OR ");
}
