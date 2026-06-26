/**
 * auto-capture hook (v3): records conversation messages locally (L0),
 * then notifies the MemoryPipelineManager for L1/L2/L3 scheduling.
 *
 * Key design decisions:
 * - Always write L0 locally via l0-recorder.
 * - When VectorStore + EmbeddingService are available, also write L0 vector index.
 * - Notify MemoryPipelineManager for L1/L2/L3 trigger evaluation.
 */

import crypto from "node:crypto";
import { CheckpointManager } from "../utils/checkpoint.js";
import { recordConversation } from "../conversation/l0_recorder.js";

const TAG = "[unified-memory] [capture]";

/**
 * @typedef {Object} CaptureLogger
 * @property {(message: string) => void} [debug]
 * @property {(message: string) => void} info
 * @property {(message: string) => void} warn
 * @property {(message: string) => void} error
 */

/**
 * @typedef {Object} AutoCaptureResult
 * @property {boolean} schedulerNotified
 * @property {number} l0RecordedCount
 * @property {number} l0VectorsWritten
 * @property {Array} filteredMessages
 */

/**
 * @typedef {Object} L0VectorRecord
 * @property {string} id
 * @property {string} sessionKey
 * @property {string} sessionId
 * @property {string} role
 * @property {string} messageText
 * @property {string} recordedAt
 * @property {number} timestamp
 */

/**
 * Generate a unique L0 record ID for vector indexing.
 * @param {string} sessionKey
 * @param {number} index
 * @returns {string}
 */
function generateL0RecordId(sessionKey, index) {
  return `l0_${sessionKey}_${Date.now()}_${index}_${crypto.randomBytes(3).toString("hex")}`;
}

/**
 * @param {Object} params
 * @param {unknown[]} params.messages
 * @param {string} params.sessionKey
 * @param {string} [params.sessionId]
 * @param {Record<string, unknown>} params.cfg
 * @param {string} params.pluginDataDir
 * @param {CaptureLogger} [params.logger]
 * @param {unknown} [params.scheduler]
 * @param {string} [params.originalUserText]
 * @param {number} [params.originalUserMessageCount]
 * @param {number} [params.pluginStartTimestamp]
 * @param {Object} [params.vectorStore]
 * @param {Object} [params.embeddingService]
 * @returns {Promise<AutoCaptureResult>}
 */
export async function performAutoCapture(params) {
  const {
    messages, sessionKey, sessionId, cfg, pluginDataDir, logger,
    scheduler, originalUserText, originalUserMessageCount, pluginStartTimestamp,
    vectorStore, embeddingService,
  } = params;
  const tCaptureStart = performance.now();

  const checkpoint = new CheckpointManager(pluginDataDir, logger);

  // Step 1 + 2: L0 recording + checkpoint update (ATOMIC)
  const tL0RecordStart = performance.now();
  let filteredMessages = [];
  try {
    await checkpoint.captureAtomically(
      sessionKey,
      pluginStartTimestamp,
      async (afterTimestamp) => {
        logger?.debug?.(`${TAG} L0 capture cursor (per-session, atomic): afterTimestamp=${afterTimestamp} session=${sessionKey}`);

        if (afterTimestamp === pluginStartTimestamp && pluginStartTimestamp && pluginStartTimestamp > 0) {
          logger?.debug?.(
            `${TAG} No per-session checkpoint cursor found for session=${sessionKey} — ` +
            `using pluginStartTimestamp as floor: ` +
            `${afterTimestamp} (${new Date(afterTimestamp).toISOString()})`,
          );
        }

        filteredMessages = await recordConversation({
          sessionKey,
          sessionId,
          rawMessages: messages,
          baseDir: pluginDataDir,
          logger,
          originalUserText,
          afterTimestamp,
          originalUserMessageCount,
        });

        if (filteredMessages.length === 0) {
          return null;
        }

        logger?.debug?.(`${TAG} L0 recorded: ${filteredMessages.length} messages for session ${sessionKey}`);
        const maxTs = Math.max(...filteredMessages.map((m) => m.timestamp));
        return { maxTimestamp: maxTs, messageCount: filteredMessages.length };
      },
    );
  } catch (err) {
    logger?.error(`${TAG} L0 recording failed: ${err instanceof Error ? err.message : String(err)}`);
  }
  const tL0RecordEnd = performance.now();

  // Step 1.5: L0 vector indexing
  const tL0VecStart = performance.now();
  let l0VectorsWritten = 0;

  const l0Records = [];
  if (filteredMessages.length > 0 && vectorStore) {
    const now = new Date().toISOString();
    logger?.debug?.(`${TAG} [L0-vec-index] START indexing ${filteredMessages.length} message(s) for session ${sessionKey}`);
    for (let i = 0; i < filteredMessages.length; i++) {
      const msg = filteredMessages[i];
      try {
        const l0Record = {
          id: generateL0RecordId(sessionKey, i),
          sessionKey,
          sessionId: sessionId || "",
          role: msg.role,
          messageText: msg.content,
          recordedAt: now,
          timestamp: msg.timestamp,
        };

        const upsertOk = vectorStore.upsertL0(l0Record, undefined);
        if (upsertOk) {
          l0VectorsWritten++;
          l0Records.push({ record: l0Record, content: msg.content });
        } else {
          logger?.warn(`${TAG} [L0-vec-index] upsertL0 returned false for message ${i}`);
        }
      } catch (err) {
        logger?.warn?.(`${TAG} [L0-vec-index] FAILED for message ${i} (non-blocking): ${err instanceof Error ? err.message : String(err)}`);
      }
    }
    logger?.debug?.(`${TAG} [L0-vec-index] DONE: ${l0VectorsWritten}/${filteredMessages.length} metadata records written (sync)`);

    // Fire-and-forget: batch embed + update vectors in background
    if (l0Records.length > 0 && embeddingService) {
      const bgVectorStore = vectorStore;
      const bgEmbeddingService = embeddingService;
      const bgRecords = [...l0Records];
      const bgLogger = logger;

      void (async () => {
        const tBgStart = performance.now();
        try {
          const texts = bgRecords.map((r) => r.content);
          const embeddings = await bgEmbeddingService.embedBatch(texts);

          let bgUpdated = 0;
          for (let i = 0; i < bgRecords.length; i++) {
            try {
              const ok = bgVectorStore.updateL0Embedding(bgRecords[i].record.id, embeddings[i]);
              if (ok) bgUpdated++;
            } catch (err) {
              bgLogger?.warn?.(`${TAG} [L0-vec-index-bg] Failed to update embedding for ${bgRecords[i].record.id}: ${err instanceof Error ? err.message : String(err)}`);
            }
          }
          const bgMs = performance.now() - tBgStart;
          bgLogger?.debug?.(`${TAG} [L0-vec-index-bg] Background embedding complete: ${bgUpdated}/${bgRecords.length} vectors updated (${bgMs.toFixed(0)}ms)`);
        } catch (err) {
          const bgMs = performance.now() - tBgStart;
          bgLogger?.warn?.(`${TAG} [L0-vec-index-bg] Background embedding failed (${bgMs.toFixed(0)}ms, non-fatal): ${err instanceof Error ? err.message : String(err)}`);
        }
      })();
    }
  } else if (filteredMessages.length > 0) {
    logger?.warn(`${TAG} [L0-vec-index] SKIPPED: vectorStore not available`);
  }
  const tL0VecEnd = performance.now();

  // Step 3: Notify scheduler
  const tNotifyStart = performance.now();
  if (scheduler) {
    await scheduler.notifyConversation(sessionKey, []);
    logger?.debug?.(`${TAG} Scheduler notified of conversation round (sessionKey=${sessionKey})`);

    const totalMs = performance.now() - tCaptureStart;
    logger?.info(
      `${TAG} ⏱ Capture timing: total=${totalMs.toFixed(0)}ms, ` +
      `l0Record+checkpoint=${(tL0RecordEnd - tL0RecordStart).toFixed(0)}ms, ` +
      `l0VecIndex=${(tL0VecEnd - tL0VecStart).toFixed(0)}ms, ` +
      `notify=${(performance.now() - tNotifyStart).toFixed(0)}ms`,
    );

    return { schedulerNotified: true, l0RecordedCount: filteredMessages.length, l0VectorsWritten, filteredMessages };
  }

  const totalMs = performance.now() - tCaptureStart;
  logger?.info(
    `${TAG} ⏱ Capture timing: total=${totalMs.toFixed(0)}ms, ` +
    `l0Record+checkpoint=${(tL0RecordEnd - tL0RecordStart).toFixed(0)}ms, ` +
    `l0VecIndex=${(tL0VecEnd - tL0VecStart).toFixed(0)}ms, ` +
    `notify=${(performance.now() - tNotifyStart).toFixed(0)}ms`,
  );

  logger?.debug?.(`${TAG} No scheduler provided, skipping notification`);
  return { schedulerNotified: false, l0RecordedCount: filteredMessages.length, l0VectorsWritten, filteredMessages };
}
