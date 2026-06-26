/**
 * auto-recall hook (v3): injects relevant memories + persona into agent context
 * before the agent starts processing.
 *
 * - Searches L1 memories using configurable strategy (keyword / embedding / hybrid)
 * - L3 persona injection
 * - L2 scene navigation (full injection, LLM decides relevance)
 */

import fs from "node:fs/promises";
import path from "node:path";
import { readSceneIndex } from "../scene/scene_index.js";
import { generateSceneNavigation, stripSceneNavigation } from "../scene/scene_navigation.js";
import { sanitizeText } from "../utils/sanitize.js";

const TAG = "[unified-memory] [recall]";

const MEMORY_TOOLS_GUIDE = `<memory-tools-guide>
## 记忆工具调用指南

当上方注入的记忆片段不足以回答用户问题时，可主动调用以下工具获取更多信息：

- **tdai_memory_search**：搜索结构化记忆（L1），适用于回忆用户偏好、历史事件节点、规则等关键信息。
- **tdai_conversation_search**：搜索原始对话（L0），适用于查找具体消息原文、时间线、上下文细节；也可用于补充或校验 memory_search 的结果。
- **read_file**（Scene Navigation 中的路径）：当已定位到相关情境，且需要该场景的完整画像、事件经过或阶段结论时使用。
</memory-tools-guide>`;

/**
 * @param {string} pluginDataDir
 * @returns {string}
 */
function buildScenePathHint(pluginDataDir) {
  return `⚠️ Scene Navigation 路径提示：上方 Scene Navigation 中的 Path（如 \`scene_blocks/xxx.md\`）是相对路径，使用 read_file 读取时需拼接为绝对路径：\`${pluginDataDir}/scene_blocks/xxx.md\``;
}

/**
 * @typedef {Object} RecallLogger
 * @property {(message: string) => void} [debug]
 * @property {(message: string) => void} info
 * @property {(message: string) => void} warn
 * @property {(message: string) => void} error
 */

/**
 * @typedef {Object} RecallResult
 * @property {string} [prependContext]
 * @property {string} [appendSystemContext]
 */

/**
 * @typedef {Object} VectorSearchResult
 * @property {string} record_id
 * @property {string} content
 * @property {string} type
 * @property {number} priority
 * @property {string} scene_name
 * @property {number} score
 * @property {string} [metadata_json]
 * @property {string} [timestamp_str]
 * @property {string} session_key
 * @property {string} session_id
 */

/**
 * @typedef {Object} FtsSearchResult
 * @property {string} record_id
 * @property {string} content
 * @property {string} type
 * @property {number} priority
 * @property {string} scene_name
 * @property {number} score
 * @property {string} [metadata_json]
 * @property {string} [timestamp_str]
 * @property {string} session_key
 * @property {string} session_id
 */

/**
 * @param {Object} params
 * @param {string} params.userText
 * @param {string} params.actorId
 * @param {string} params.sessionKey
 * @param {Record<string, unknown>} params.cfg
 * @param {string} params.pluginDataDir
 * @param {RecallLogger} [params.logger]
 * @param {Object} [params.vectorStore]
 * @param {Object} [params.embeddingService]
 * @returns {Promise<RecallResult|undefined>}
 */
export async function performAutoRecall(params) {
  const { userText, cfg, pluginDataDir, logger, vectorStore, embeddingService } = params;

  let memoryLines = [];
  if (!userText || userText.length === 0) {
    logger?.debug?.(`${TAG} User text empty/undefined, skipping memory search`);
  } else {
    const strategy = cfg?.recall?.strategy ?? "hybrid";
    memoryLines = await searchMemories(userText, pluginDataDir, cfg, logger, strategy, vectorStore, embeddingService);
  }

  let personaContent;
  try {
    const personaPath = path.join(pluginDataDir, "persona.md");
    const raw = await fs.readFile(personaPath, "utf-8");
    personaContent = stripSceneNavigation(raw).trim();
    if (!personaContent) personaContent = undefined;
    logger?.debug?.(`${TAG} Persona loaded: ${personaContent ? `${personaContent.length} chars` : "empty"}`);
  } catch {
    logger?.debug?.(`${TAG} No persona file found`);
  }

  let sceneNavigation;
  try {
    const sceneIndex = await readSceneIndex(pluginDataDir);
    if (sceneIndex.length > 0) {
      sceneNavigation = generateSceneNavigation(sceneIndex);
      logger?.debug?.(`${TAG} Scene navigation generated: ${sceneIndex.length} scenes`);
    }
  } catch {
    logger?.debug?.(`${TAG} No scene index found`);
  }

  if (memoryLines.length === 0 && !personaContent && !sceneNavigation) {
    logger?.debug?.(`${TAG} No memories/persona/scenes to inject`);
    return undefined;
  }

  const systemParts = [];
  if (personaContent) {
    systemParts.push(`<user-persona>\n${personaContent}\n</user-persona>`);
  }
  if (sceneNavigation) {
    const pathHint = buildScenePathHint(pluginDataDir);
    systemParts.push(`<scene-navigation>\n${sceneNavigation}\n\n${pathHint}\n</scene-navigation>`);
  }
  if (memoryLines.length > 0) {
    systemParts.push(`<relevant-memories>\n${memoryLines.join("\n")}\n</relevant-memories>`);
  }

  if (systemParts.length > 0) {
    systemParts.push(MEMORY_TOOLS_GUIDE);
  }

  const appendSystemContext = systemParts.length > 0 ? systemParts.join("\n\n") : undefined;
  if (!appendSystemContext) return undefined;

  return { appendSystemContext };
}

// ============================
// Multi-strategy search dispatcher
// ============================

/**
 * @typedef {Object} FormatableMemory
 * @property {string} type
 * @property {string} content
 * @property {string} [scene_name]
 * @property {string} [activity_start_time]
 * @property {string} [activity_end_time]
 * @property {string} [timestamp]
 */

const RRF_K = 60;

/**
 * @param {string} userText
 * @param {string} pluginDataDir
 * @param {Record<string, unknown>} cfg
 * @param {RecallLogger} [logger]
 * @param {"keyword"|"embedding"|"hybrid"} strategy
 * @param {Object} [vectorStore]
 * @param {Object} [embeddingService]
 * @returns {Promise<string[]>}
 */
async function searchMemories(userText, pluginDataDir, cfg, logger, strategy, vectorStore, embeddingService) {
  const cleanText = sanitizeText(userText);

  if (cleanText.length < 2) {
    logger?.debug?.(`${TAG} Query too short for memory search`);
    return [];
  }

  const maxResults = cfg?.recall?.maxResults ?? 5;
  const threshold = cfg?.recall?.scoreThreshold ?? 0.3;
  const embeddingAvailable = !!vectorStore && !!embeddingService;

  let effectiveStrategy = strategy;
  if ((strategy === "embedding" || strategy === "hybrid") && !embeddingAvailable) {
    logger?.warn?.(`${TAG} Strategy "${strategy}" requested but embedding not available, falling back to keyword`);
    effectiveStrategy = "keyword";
  }

  try {
    if (effectiveStrategy === "keyword") {
      return await searchByKeyword(cleanText, maxResults, threshold, logger, vectorStore);
    }
    if (effectiveStrategy === "embedding") {
      return await searchByEmbedding(cleanText, maxResults, threshold, vectorStore, embeddingService, logger);
    }
    return await searchHybrid(cleanText, maxResults, threshold, vectorStore, embeddingService, logger);
  } catch (err) {
    logger?.warn?.(`${TAG} Memory search failed: ${err instanceof Error ? err.message : String(err)}`);
    return [];
  }
}

// ============================
// Strategy: Keyword (FTS5 BM25)
// ============================

/**
 * @param {string} userText
 * @param {number} maxResults
 * @param {number} threshold
 * @param {RecallLogger} [logger]
 * @param {Object} [vectorStore]
 * @returns {Promise<string[]>}
 */
async function searchByKeyword(userText, maxResults, threshold, logger, vectorStore) {
  if (vectorStore?.isFtsAvailable()) {
    const ftsQuery = buildFtsQuery(userText);
    if (ftsQuery) {
      logger?.debug?.(`${TAG} [keyword-fts] Using FTS5 BM25 search: query="${ftsQuery}"`);
      const ftsResults = vectorStore.ftsSearchL1(ftsQuery, maxResults * 2);
      if (ftsResults.length > 0) {
        const filtered = ftsResults.filter((r) => r.score >= threshold).slice(0, maxResults);
        if (filtered.length > 0) {
          return filtered.map((r) => formatMemoryLine(ftsResultToFormatable(r)));
        }
        if (ftsResults.length <= maxResults) {
          return ftsResults.slice(0, maxResults).map((r) => formatMemoryLine(ftsResultToFormatable(r)));
        }
      }
    }
  }
  logger?.debug?.(`${TAG} [keyword] FTS5 unavailable or no results`);
  return [];
}

// ============================
// Strategy: Embedding (VectorStore cosine)
// ============================

/**
 * @param {string} userText
 * @param {number} maxResults
 * @param {number} threshold
 * @param {Object} vectorStore
 * @param {Object} embeddingService
 * @param {RecallLogger} [logger]
 * @returns {Promise<string[]>}
 */
async function searchByEmbedding(userText, maxResults, threshold, vectorStore, embeddingService, logger) {
  logger?.debug?.(`${TAG} [embedding-search] START`);
  const queryEmbedding = await embeddingService.embed(userText);
  const vecResults = vectorStore.search(queryEmbedding, maxResults * 2);
  if (vecResults.length === 0) return [];

  const filtered = vecResults.filter((r) => r.score >= threshold).slice(0, maxResults);
  if (filtered.length > 0) {
    return filtered.map((r) => formatMemoryLine(vectorResultToFormatable(r)));
  }
  return [];
}

// ============================
// Strategy: Hybrid (Keyword + Embedding + RRF)
// ============================

/**
 * @param {string} userText
 * @param {number} maxResults
 * @param {number} threshold
 * @param {Object} vectorStore
 * @param {Object} embeddingService
 * @param {RecallLogger} [logger]
 * @returns {Promise<string[]>}
 */
async function searchHybrid(userText, maxResults, threshold, vectorStore, embeddingService, logger) {
  const candidateK = maxResults * 3;

  const [keywordResults, embeddingResults] = await Promise.all([
    (async () => {
      try {
        if (vectorStore.isFtsAvailable()) {
          const ftsQuery = buildFtsQuery(userText);
          if (ftsQuery) {
            const ftsResults = vectorStore.ftsSearchL1(ftsQuery, candidateK);
            if (ftsResults.length > 0) {
              return ftsResults.map((r) => ({ record: r, score: r.score }));
            }
          }
        }
        return [];
      } catch (err) {
        logger?.warn?.(`${TAG} Hybrid: keyword part failed: ${err instanceof Error ? err.message : String(err)}`);
        return [];
      }
    })(),
    (async () => {
      try {
        const queryEmbedding = await embeddingService.embed(userText);
        return vectorStore.search(queryEmbedding, candidateK);
      } catch (err) {
        logger?.warn?.(`${TAG} Hybrid: embedding part failed: ${err instanceof Error ? err.message : String(err)}`);
        return [];
      }
    })(),
  ]);

  if (keywordResults.length === 0 && embeddingResults.length === 0) {
    return [];
  }

  const mergedMap = new Map();

  for (let rank = 0; rank < keywordResults.length; rank++) {
    const r = keywordResults[rank];
    const id = typeof r.record === "object" ? r.record.record_id : r.record_id;
    const rrfScore = 1 / (RRF_K + rank + 1);
    const existing = mergedMap.get(id);
    if (existing) {
      existing.rrfScore += rrfScore;
    } else {
      mergedMap.set(id, { rrfScore, formatable: typeof r.record === "object" ? ftsResultToFormatable(r.record) : vectorResultToFormatable(r) });
    }
  }

  for (let rank = 0; rank < embeddingResults.length; rank++) {
    const r = embeddingResults[rank];
    const rrfScore = 1 / (RRF_K + rank + 1);
    const existing = mergedMap.get(r.record_id);
    if (existing) {
      existing.rrfScore += rrfScore;
    } else {
      mergedMap.set(r.record_id, { rrfScore, formatable: vectorResultToFormatable(r) });
    }
  }

  const sorted = [...mergedMap.entries()].sort((a, b) => b[1].rrfScore - a[1].rrfScore).slice(0, maxResults);
  if (sorted.length > 0) {
    return sorted.map(([, { formatable }]) => formatMemoryLine(formatable));
  }
  return [];
}

// ============================
// Formatters
// ============================

/**
 * @param {FormatableMemory} m
 * @returns {string}
 */
function formatMemoryLine(m) {
  const tag = m.scene_name ? `${m.type}|${m.scene_name}` : m.type;
  let line = `- [${tag}] ${m.content}`;

  const start = formatTimestamp(m.activity_start_time);
  const end = formatTimestamp(m.activity_end_time);
  const point = formatTimestamp(m.timestamp);

  if (start && end) {
    line += ` (活动时间: ${start} ~ ${end})`;
  } else if (start) {
    line += ` (活动时间: ${start}起)`;
  } else if (end) {
    line += ` (活动时间: 至${end})`;
  } else if (point) {
    line += ` (活动时间: ${point})`;
  }

  return line;
}

/**
 * @param {string} ts
 * @returns {string|undefined}
 */
function formatTimestamp(ts) {
  if (!ts) return undefined;
  const match = ts.match(/^(\d{4}-\d{2}-\d{2})(?:T(\d{2}:\d{2})(?::\d{2})?)?/);
  if (!match) return undefined;
  const datePart = match[1];
  const timePart = match[2];
  if (!timePart || timePart === "00:00") return datePart;
  return `${datePart} ${timePart}`;
}

/**
 * @param {FtsSearchResult} r
 * @returns {FormatableMemory}
 */
function ftsResultToFormatable(r) {
  let activityStart, activityEnd;
  if (r.metadata_json && r.metadata_json !== "{}") {
    try {
      const meta = JSON.parse(r.metadata_json);
      activityStart = meta?.activity_start_time;
      activityEnd = meta?.activity_end_time;
    } catch { /* ignore */ }
  }
  return {
    type: r.type,
    content: r.content,
    scene_name: r.scene_name || undefined,
    activity_start_time: activityStart,
    activity_end_time: activityEnd,
    timestamp: r.timestamp_str || undefined,
  };
}

/**
 * @param {VectorSearchResult} r
 * @returns {FormatableMemory}
 */
function vectorResultToFormatable(r) {
  let activityStart, activityEnd;
  if (r.metadata_json && r.metadata_json !== "{}") {
    try {
      const meta = JSON.parse(r.metadata_json);
      activityStart = meta?.activity_start_time;
      activityEnd = meta?.activity_end_time;
    } catch { /* ignore */ }
  }
  return {
    type: r.type,
    content: r.content,
    scene_name: r.scene_name || undefined,
    activity_start_time: activityStart,
    activity_end_time: activityEnd,
    timestamp: r.timestamp_str || undefined,
  };
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
