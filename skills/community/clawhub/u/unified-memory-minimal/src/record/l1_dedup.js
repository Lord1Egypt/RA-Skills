/**
 * L1 Memory Conflict Detection (Batch Mode)
 *
 * v4: Removed JSONL-based Jaccard fallback. Candidate recall now relies exclusively
 *     on vector search (primary) and FTS5 BM25 (degraded). If neither is available,
 *     conflict detection is skipped entirely — all memories go straight to store.
 */

import { CONFLICT_DETECTION_SYSTEM_PROMPT, formatBatchConflictPrompt } from "../prompts/l1_dedup.js";
import { CleanContextRunner } from "../utils/clean_context_runner.js";
import { sanitizeJsonForParse } from "../utils/sanitize.js";

const TAG = "[unified-memory][l1-dedup]";

/**
 * @typedef {Object} ExtractedMemory
 * @property {string} content
 * @property {string} type
 * @property {number} priority
 * @property {string[]} source_message_ids
 * @property {Object} metadata
 * @property {string} scene_name
 */

/**
 * @typedef {Object} MemoryRecord
 * @property {string} id
 * @property {string} content
 * @property {string} type
 * @property {number} priority
 * @property {string} scene_name
 * @property {string[]} source_message_ids
 * @property {Object} metadata
 * @property {string[]} timestamps
 * @property {string} createdAt
 * @property {string} updatedAt
 * @property {string} sessionKey
 * @property {string} sessionId
 */

/**
 * @typedef {Object} DedupDecision
 * @property {string} record_id
 * @property {"store"|"update"|"merge"|"skip"} action
 * @property {string[]} target_ids
 * @property {string} [merged_content]
 * @property {string} [merged_type]
 * @property {number} [merged_priority]
 * @property {string[]} [merged_timestamps]
 */

const VALID_TYPES = ["persona", "episodic", "instruction"];

/**
 * Batch conflict detection: compare all new memories against existing records
 * in a single LLM call.
 *
 * @param {Object} params
 * @param {Array<ExtractedMemory & {record_id: string}>} params.memories
 * @param {unknown} params.config
 * @param {import("../utils/sanitize.js").Logger} [params.logger]
 * @param {string} [params.model]
 * @param {Object} [params.vectorStore]
 * @param {Object} [params.embeddingService]
 * @param {number} [params.conflictRecallTopK]
 * @returns {Promise<DedupDecision[]>}
 */
export async function batchDedup(params) {
  const { memories, config, logger, model, vectorStore, embeddingService } = params;
  const topK = params.conflictRecallTopK ?? 5;

  if (memories.length === 0) return [];

  const storeAll = () =>
    memories.map((m) => ({
      record_id: m.record_id,
      action: "store",
      target_ids: [],
    }));

  const hasVectorData = vectorStore && vectorStore.count && vectorStore.count() > 0;
  const hasFts = vectorStore?.isFtsAvailable?.() ?? false;

  if (!hasVectorData && !hasFts) {
    logger?.debug?.(`${TAG} No vector data and no FTS available, skipping conflict detection for ${memories.length} memories`);
    return storeAll();
  }

  let matches;
  if (hasVectorData && embeddingService) {
    try {
      matches = await findCandidatesByVector(memories, vectorStore, embeddingService, topK, logger);
    } catch (err) {
      logger?.warn?.(`${TAG} Vector recall failed, falling back to FTS: ${err instanceof Error ? err.message : String(err)}`);
      if (hasFts) {
        matches = findCandidatesByFts(memories, vectorStore, logger);
      } else {
        return storeAll();
      }
    }
  } else if (hasFts) {
    matches = findCandidatesByFts(memories, vectorStore, logger);
  } else {
    return storeAll();
  }

  const hasAnyCandidates = matches.some((m) => m.candidates.length > 0);
  if (!hasAnyCandidates) {
    return storeAll();
  }

  return runLlmJudgment(matches, memories, config, logger, model);
}

/**
 * Phase 2: Run batch LLM judgment on candidate matches.
 * @param {Array<{newMemory: ExtractedMemory & {record_id: string}, candidates: MemoryRecord[]}>} matches
 * @param {Array<ExtractedMemory & {record_id: string}>} memories
 * @param {unknown} config
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @param {string} [model]
 * @returns {Promise<DedupDecision[]>}
 */
async function runLlmJudgment(matches, memories, config, logger, model) {
  logger?.debug?.(`${TAG} Running batch conflict detection for ${memories.length} memories`);

  try {
    const runner = new CleanContextRunner({ config, modelRef: model, enableTools: false, logger });
    const userPrompt = formatBatchConflictPrompt(matches);

    const result = await runner.run({
      prompt: userPrompt,
      systemPrompt: CONFLICT_DETECTION_SYSTEM_PROMPT,
      taskId: "l1-conflict-detection",
      timeoutMs: 180_000,
    });

    return parseBatchResult(result, memories, logger);
  } catch (err) {
    logger?.warn?.(`${TAG} Batch conflict detection failed, defaulting all to store: ${err instanceof Error ? err.message : String(err)}`);
    return memories.map((m) => ({ record_id: m.record_id, action: "store", target_ids: [] }));
  }
}

/**
 * Vector-based candidate recall.
 * @param {Array<ExtractedMemory & {record_id: string}>} memories
 * @param {Object} vectorStore
 * @param {Object} embeddingService
 * @param {number} topK
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @returns {Promise<Array<{newMemory: ExtractedMemory & {record_id: string}, candidates: MemoryRecord[]}>>}
 */
async function findCandidatesByVector(memories, vectorStore, embeddingService, topK, logger) {
  const newRecordIds = new Set(memories.map((m) => m.record_id));

  const texts = memories.map((m) => m.content);
  const embeddings = await embeddingService.embedBatch(texts);

  const matches = [];

  for (let i = 0; i < memories.length; i++) {
    const mem = memories[i];
    const queryVec = embeddings[i];
    const searchResults = vectorStore.search(queryVec, topK + memories.length);

    const candidates = searchResults
      .filter((r) => !newRecordIds.has(r.record_id))
      .slice(0, topK)
      .map((r) => ({
        id: r.record_id,
        content: r.content,
        type: r.type,
        priority: r.priority,
        scene_name: r.scene_name,
        source_message_ids: [],
        metadata: {},
        timestamps: [r.timestamp_str].filter(Boolean),
        createdAt: "",
        updatedAt: "",
        sessionKey: r.session_key,
        sessionId: r.session_id,
      }));

    matches.push({ newMemory: mem, candidates });
  }

  logger?.debug?.(`${TAG} Vector recall: ${matches.map((m) => `${m.newMemory.record_id}→${m.candidates.length}`).join(", ")}`);

  return matches;
}

/**
 * FTS5-based candidate recall.
 * @param {Array<ExtractedMemory & {record_id: string}>} memories
 * @param {Object} vectorStore
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @returns {Array<{newMemory: ExtractedMemory & {record_id: string}, candidates: MemoryRecord[]}>}
 */
function findCandidatesByFts(memories, vectorStore, logger) {
  const newRecordIds = new Set(memories.map((m) => m.record_id));
  const matches = [];

  for (const mem of memories) {
    const ftsQuery = buildFtsQuery(mem.content);
    if (ftsQuery) {
      const ftsResults = vectorStore.ftsSearchL1(ftsQuery, 10);
      const candidates = ftsResults
        .filter((r) => !newRecordIds.has(r.record_id))
        .slice(0, 5)
        .map((r) => ({
          id: r.record_id,
          content: r.content,
          type: r.type,
          priority: r.priority,
          scene_name: r.scene_name,
          source_message_ids: [],
          metadata: r.metadata_json ? (() => { try { return JSON.parse(r.metadata_json); } catch { return {}; } })() : {},
          timestamps: [r.timestamp_str].filter(Boolean),
          createdAt: "",
          updatedAt: "",
          sessionKey: r.session_key,
          sessionId: r.session_id,
        }));
      matches.push({ newMemory: mem, candidates });
    } else {
      matches.push({ newMemory: mem, candidates: [] });
    }
  }

  logger?.debug?.(`${TAG} FTS keyword recall: ${matches.map((m) => `${m.newMemory.record_id}→${m.candidates.length}`).join(", ")}`);
  return matches;
}

/**
 * Build FTS query from text (basic tokenizer).
 * @param {string} text
 * @returns {string}
 */
function buildFtsQuery(text) {
  const words = text.match(/[\w\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]+/g);
  if (!words || words.length === 0) return "";
  return words.slice(0, 10).join(" OR ");
}

/**
 * Parse the LLM's batch conflict detection JSON response.
 * @param {string} raw
 * @param {Array<ExtractedMemory & {record_id: string}>} memories
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @returns {DedupDecision[]}
 */
function parseBatchResult(raw, memories, logger) {
  try {
    let cleaned = raw.trim();
    if (cleaned.startsWith("```")) {
      cleaned = cleaned.replace(/^```(?:json)?\s*\n?/, "").replace(/\n?```\s*$/, "");
    }

    const arrayMatch = cleaned.match(/\[[\s\S]*\]/);
    if (!arrayMatch) {
      logger?.warn?.(`${TAG} No JSON array found in conflict detection response`);
      return fallbackStoreAll(memories);
    }

    const sanitized = sanitizeJsonForParse(arrayMatch[0]);
    const parsed = JSON.parse(sanitized);

    if (!Array.isArray(parsed)) {
      logger?.warn?.(`${TAG} Conflict detection response is not an array`);
      return fallbackStoreAll(memories);
    }

    const decisions = [];
    const validActions = ["store", "update", "merge", "skip"];

    for (const item of parsed) {
      if (!item || typeof item !== "object") continue;
      const d = item;

      const recordId = String(d.record_id ?? "");
      const action = String(d.action ?? "store");

      decisions.push({
        record_id: recordId,
        action: validActions.includes(action) ? action : "store",
        target_ids: Array.isArray(d.target_ids) ? d.target_ids.map(String) : [],
        merged_content: typeof d.merged_content === "string" ? d.merged_content : undefined,
        merged_type: VALID_TYPES.includes(d.merged_type) ? d.merged_type : undefined,
        merged_priority: typeof d.merged_priority === "number" ? d.merged_priority : undefined,
        merged_timestamps: Array.isArray(d.merged_timestamps) ? d.merged_timestamps.map(String) : undefined,
      });
    }

    const decidedIds = new Set(decisions.map((d) => d.record_id));
    for (const mem of memories) {
      if (!decidedIds.has(mem.record_id)) {
        decisions.push({ record_id: mem.record_id, action: "store", target_ids: [] });
      }
    }

    return decisions;
  } catch (err) {
    logger?.warn?.(`${TAG} Failed to parse conflict detection result: ${err instanceof Error ? err.message : String(err)}`);
    return fallbackStoreAll(memories);
  }
}

/**
 * Fallback: store all memories when parsing fails.
 * @param {Array<ExtractedMemory & {record_id: string}>} memories
 * @returns {DedupDecision[]}
 */
function fallbackStoreAll(memories) {
  return memories.map((m) => ({ record_id: m.record_id, action: "store", target_ids: [] }));
}
