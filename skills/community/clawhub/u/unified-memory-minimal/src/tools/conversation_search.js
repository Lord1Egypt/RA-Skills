/**
 * conversation_search tool: Agent-callable tool for searching L0 conversation records.
 *
 * Supports three search strategies with automatic degradation:
 *   1. **hybrid** (default) — FTS5 keyword + vector embedding in parallel, merged via RRF.
 *   2. **embedding** — pure vector similarity
 *   3. **fts** — pure FTS5 keyword search
 */

const TAG = "[unified-memory][tdai_conversation_search]";
const RRF_K = 60;

/**
 * @typedef {Object} ConversationSearchResultItem
 * @property {string} id
 * @property {string} session_key
 * @property {string} role
 * @property {string} content
 * @property {number} score
 * @property {string} recorded_at
 */

/**
 * @typedef {Object} ConversationSearchResult
 * @property {ConversationSearchResultItem[]} results
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
 * @param {ConversationSearchResultItem[]} ...lists
 * @returns {ConversationSearchResultItem[]}
 */
function rrfMergeL0(...lists) {
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
 * @param {string} [params.sessionKey]
 * @param {Object} [params.vectorStore]
 * @param {Object} [params.embeddingService]
 * @param {ToolLogger} [params.logger]
 * @returns {Promise<ConversationSearchResult>}
 */
export async function executeConversationSearch(params) {
  const { query, limit, sessionKey: sessionFilter, vectorStore, embeddingService, logger } = params;

  logger?.debug?.(
    `${TAG} CALLED: query="${query.slice(0, 100)}", limit=${limit}, ` +
    `sessionFilter=${sessionFilter ?? "(none)"}`,
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
      message: "Embedding service is not configured and FTS is not available. Conversation search requires an embedding provider or FTS5 support.",
    };
  }

  const candidateK = sessionFilter ? limit * 4 : limit * 3;

  const [ftsItems, vecItems] = await Promise.all([
    (async () => {
      if (!hasFts) return [];
      try {
        const ftsQuery = buildFtsQuery(query);
        if (!ftsQuery) return [];
        logger?.debug?.(`${TAG} [hybrid-fts] FTS5 query: "${ftsQuery}"`);
        const ftsResults = vectorStore.ftsSearchL0(ftsQuery, candidateK);
        return ftsResults.map((r) => ({
          id: r.record_id,
          session_key: r.session_key,
          role: r.role,
          content: r.message_text,
          score: r.score,
          recorded_at: r.recorded_at,
        }));
      } catch (err) {
        logger?.warn?.(`${TAG} [hybrid-fts] FTS5 search failed: ${err instanceof Error ? err.message : String(err)}`);
        return [];
      }
    })(),

    (async () => {
      if (!hasEmbedding) return [];
      try {
        const queryEmbedding = await embeddingService.embed(query);
        const vecResults = vectorStore.searchL0(queryEmbedding, candidateK);
        return vecResults.map((r) => ({
          id: r.record_id,
          session_key: r.session_key,
          role: r.role,
          content: r.message_text,
          score: r.score,
          recorded_at: r.recorded_at,
        }));
      } catch (err) {
        logger?.warn?.(`${TAG} [hybrid-vec] Embedding search failed: ${err instanceof Error ? err.message : String(err)}`);
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
    results = rrfMergeL0(ftsItems, vecItems);
  } else {
    results = ftsOk ? ftsItems : vecItems;
  }

  if (sessionFilter) {
    results = results.filter((r) => r.session_key === sessionFilter);
  }

  const trimmed = results.slice(0, limit);

  return { results: trimmed, total: trimmed.length, strategy };
}

/**
 * @param {ConversationSearchResult} result
 * @returns {string}
 */
export function formatConversationSearchResponse(result) {
  if (result.message) return result.message;
  if (result.results.length === 0) return "No matching conversation messages found.";

  const lines = [`Found ${result.total} matching message(s):`, ""];

  for (const item of result.results) {
    const scoreStr = typeof item.score === "number" ? ` (score: ${item.score.toFixed(3)})` : "";
    const dateStr = item.recorded_at ? ` [${item.recorded_at}]` : "";
    lines.push(`---`);
    lines.push(`**[${item.role}]** Session: ${item.session_key}${dateStr}${scoreStr}`);
    lines.push("");
    lines.push(item.content);
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
