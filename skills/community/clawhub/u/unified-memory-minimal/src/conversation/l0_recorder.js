/**
 * L0 Conversation Recorder: records raw conversation messages to local JSONL files.
 *
 * Triggered from agent_end hook. Receives the conversation messages directly from
 * the hook context (no file I/O needed), sanitizes them, filters out noise, and
 * writes to ~/.openclaw/memory/conversations/YYYY-MM-DD.jsonl
 *
 * Design decisions:
 * - Uses JSONL format (**one message per line** — flat, easy to grep/stream)
 * - One file per day (all sessions merged into the same daily file)
 * - sessionKey is stored as a field in each JSONL line, not in the filename
 * - Independent from system session files — format fully controlled by plugin
 * - Messages are sanitized to remove injected tags (prevent feedback loops)
 * - Short/long/command messages are filtered out
 */

import fs from "node:fs/promises";
import path from "node:path";
import crypto from "node:crypto";
import { sanitizeText, shouldCaptureL0 } from "../utils/sanitize.js";

// ============================
// Types
// ============================

/**
 * @typedef {Object} ConversationMessage
 * @property {string} id
 * @property {"user"|"assistant"} role
 * @property {string} content
 * @property {number} timestamp
 */

/**
 * New flat format: one message per JSONL line.
 * @typedef {Object} L0MessageRecord
 * @property {string} sessionKey
 * @property {string} sessionId
 * @property {string} recordedAt
 * @property {string} id
 * @property {"user"|"assistant"} role
 * @property {string} content
 * @property {number} timestamp
 */

/**
 * @typedef {Object} L0ConversationRecord
 * @property {string} sessionKey
 * @property {string} sessionId
 * @property {string} recordedAt
 * @property {number} messageCount
 * @property {ConversationMessage[]} messages
 */

const TAG = "[unified-memory][l0]";

// ============================
// Core function
// ============================

/**
 * Generate a short unique message ID.
 * @returns {string}
 */
function generateMessageId() {
  return `msg_${Date.now()}_${crypto.randomBytes(3).toString("hex")}`;
}

/**
 * Record a conversation round to the L0 JSONL file.
 *
 * @param {Object} params
 * @param {string} params.sessionKey
 * @param {string} [params.sessionId]
 * @param {unknown[]} params.rawMessages
 * @param {string} params.baseDir
 * @param {import("../utils/sanitize.js").Logger} [params.logger]
 * @param {string} [params.originalUserText]
 * @param {number} [params.afterTimestamp]
 * @param {number} [params.originalUserMessageCount]
 * @returns {Promise<ConversationMessage[]>}
 */
export async function recordConversation(params) {
  const {
    sessionKey, sessionId, rawMessages, baseDir, logger,
    originalUserText, afterTimestamp, originalUserMessageCount,
  } = params;

  // Step 1: Extract user/assistant messages from raw hook messages
  const allExtracted = extractUserAssistantMessages(rawMessages);
  logger?.debug?.(`${TAG} Extracted ${allExtracted.length} user/assistant messages from ${rawMessages.length} total`);

  // Step 1.5: Incremental filter — only keep messages newer than the cursor.
  const cursor = afterTimestamp ?? 0;
  const extracted = cursor > 0
    ? allExtracted.filter((m) => m.timestamp > cursor)
    : allExtracted;

  if (cursor > 0) {
    logger?.debug?.(`${TAG} Incremental filter: ${allExtracted.length} total → ${extracted.length} new (cursor=${cursor})`);
  }

  if (extracted.length === 0) {
    logger?.debug?.(`${TAG} No new user/assistant messages to record`);
    return [];
  }

  // Step 2: Replace polluted user messages with cached original prompt.
  if (originalUserText && originalUserMessageCount != null && originalUserMessageCount >= 0 && originalUserMessageCount < rawMessages.length) {
    const targetRaw = rawMessages[originalUserMessageCount];
    const targetTs = targetRaw && typeof targetRaw === "object" && typeof targetRaw.timestamp === "number" ? targetRaw.timestamp : undefined;

    if (targetTs != null) {
      let replaced = false;
      for (let i = 0; i < extracted.length; i++) {
        if (extracted[i].role === "user" && extracted[i].timestamp === targetTs) {
          extracted[i] = { ...extracted[i], content: originalUserText };
          replaced = true;
          break;
        }
      }
      if (!replaced) {
        logger?.warn?.(`${TAG} Target user message (ts=${targetTs}) not found in extracted batch — relying on sanitizeText()`);
      }
    }
  }

  // Step 3: Sanitize and filter
  const filtered = extracted
    .map((m) => ({
      id: m.id,
      role: m.role,
      content: sanitizeText(m.content),
      timestamp: m.timestamp,
    }))
    .filter((m) => shouldCaptureL0(m.content));

  logger?.debug?.(`${TAG} After sanitize+filter: ${filtered.length} messages (from ${extracted.length})`);

  if (filtered.length === 0) {
    logger?.debug?.(`${TAG} All messages filtered out, skipping L0 write`);
    return [];
  }

  // Step 4: Write to JSONL file — one message per line
  const now = new Date().toISOString();
  const lines = [];
  for (const msg of filtered) {
    const record = {
      sessionKey,
      sessionId: sessionId || "",
      recordedAt: now,
      id: msg.id,
      role: msg.role,
      content: msg.content,
      timestamp: msg.timestamp,
    };
    lines.push(JSON.stringify(record));
  }

  const shardDate = formatLocalDate(new Date());
  const outDir = path.join(baseDir, "conversations");
  const outPath = path.join(outDir, `${shardDate}.jsonl`);

  try {
    await fs.mkdir(outDir, { recursive: true });
    await fs.appendFile(outPath, lines.join("\n") + "\n", "utf-8");
    logger?.debug?.(`${TAG} Recorded ${filtered.length} messages to ${outPath}`);
  } catch (err) {
    logger?.error(`${TAG} Failed to write L0 file: ${err instanceof Error ? err.message : String(err)}`);
  }

  return filtered;
}

/**
 * Read all L0 conversation records for a session.
 * @param {string} sessionKey
 * @param {string} baseDir
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @returns {Promise<L0ConversationRecord[]>}
 */
export async function readConversationRecords(sessionKey, baseDir, logger) {
  const conversationsDir = path.join(baseDir, "conversations");
  const dateFilePattern = /^\d{4}-\d{2}-\d{2}\.jsonl$/;

  let entries;
  try {
    const dirEntries = await fs.readdir(conversationsDir, { withFileTypes: true });
    entries = dirEntries.filter((entry) => entry.isFile()).map((entry) => entry.name);
  } catch {
    return [];
  }

  const targetFiles = entries.filter((name) => dateFilePattern.test(name)).sort();
  if (targetFiles.length === 0) return [];

  const records = [];

  for (const fileName of targetFiles) {
    const filePath = path.join(conversationsDir, fileName);
    let raw;
    try {
      raw = await fs.readFile(filePath, "utf-8");
    } catch {
      logger?.warn?.(`${TAG} Failed to read L0 file: ${filePath}`);
      continue;
    }

    const lines = raw.split("\n").filter((line) => line.trim());
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      try {
        const parsed = JSON.parse(line);

        const lineSessionKey = parsed.sessionKey;
        if (lineSessionKey !== sessionKey) continue;

        if (typeof parsed.role === "string" && typeof parsed.content === "string") {
          const msg = {
            id: (typeof parsed.id === "string" && parsed.id) ? parsed.id : generateMessageId(),
            role: parsed.role,
            content: parsed.content,
            timestamp: typeof parsed.timestamp === "number" ? parsed.timestamp : Date.now(),
          };
          records.push({
            sessionKey: parsed.sessionKey || sessionKey,
            sessionId: parsed.sessionId || "",
            recordedAt: parsed.recordedAt || new Date().toISOString(),
            messageCount: 1,
            messages: [msg],
          });
        }
      } catch {
        logger?.warn?.(`${TAG} Skipping malformed JSONL line in ${filePath}:${i + 1}`);
      }
    }
  }

  records.sort((a, b) => {
    const ta = Date.parse(a.recordedAt);
    const tb = Date.parse(b.recordedAt);
    const na = Number.isFinite(ta) ? ta : Number.POSITIVE_INFINITY;
    const nb = Number.isFinite(tb) ? tb : Number.POSITIVE_INFINITY;
    return na - nb;
  });

  return records;
}

/**
 * Read L0 messages across all conversation records for a session.
 * @param {string} sessionKey
 * @param {string} baseDir
 * @param {number} [afterTimestamp]
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @param {number} [limit]
 * @returns {Promise<ConversationMessage[]>}
 */
export async function readConversationMessages(sessionKey, baseDir, afterTimestamp, logger, limit) {
  const records = await readConversationRecords(sessionKey, baseDir, logger);
  const allMessages = [];

  for (const record of records) {
    for (const msg of record.messages) {
      if (afterTimestamp && msg.timestamp <= afterTimestamp) continue;
      allMessages.push(msg);
    }
  }

  if (limit != null && limit > 0 && allMessages.length > limit) {
    return allMessages.slice(-limit);
  }

  return allMessages;
}

/**
 * @typedef {Object} SessionIdMessageGroup
 * @property {string} sessionId
 * @property {ConversationMessage[]} messages
 */

/**
 * Read L0 messages for a session, grouped by sessionId.
 * @param {string} sessionKey
 * @param {string} baseDir
 * @param {number} [afterTimestamp]
 * @param {import("../utils/sanitize.js").Logger} [logger]
 * @param {number} [limit]
 * @returns {Promise<SessionIdMessageGroup[]>}
 */
export async function readConversationMessagesGroupedBySessionId(sessionKey, baseDir, afterTimestamp, logger, limit) {
  const records = await readConversationRecords(sessionKey, baseDir, logger);

  const allMessages = [];

  for (const record of records) {
    const sid = record.sessionId || "";
    for (const msg of record.messages) {
      if (afterTimestamp && msg.timestamp <= afterTimestamp) continue;
      allMessages.push({ sessionId: sid, msg });
    }
  }

  allMessages.sort((a, b) => a.msg.timestamp - b.msg.timestamp);

  let selected = allMessages;
  if (limit != null && limit > 0 && allMessages.length > limit) {
    selected = allMessages.slice(-limit);
  }

  const groupMap = new Map();
  for (const { sessionId, msg } of selected) {
    let group = groupMap.get(sessionId);
    if (!group) {
      group = [];
      groupMap.set(sessionId, group);
    }
    group.push(msg);
  }

  const groups = [];
  for (const [sessionId, messages] of groupMap) {
    if (messages.length > 0) {
      groups.push({ sessionId, messages });
    }
  }
  groups.sort((a, b) => a.messages[0].timestamp - b.messages[0].timestamp);

  return groups;
}

// ============================
// Helpers
// ============================

/**
 * Extract user and assistant messages from raw hook message array.
 * @param {unknown[]} messages
 * @returns {ConversationMessage[]}
 */
function extractUserAssistantMessages(messages) {
  const result = [];

  for (const msg of messages) {
    if (!msg || typeof msg !== "object") continue;
    const m = msg;
    const role = m.role;

    if (role !== "user" && role !== "assistant") continue;

    let content;
    if (typeof m.content === "string") {
      content = m.content;
    } else if (Array.isArray(m.content)) {
      const textParts = [];
      for (const part of m.content) {
        if (part && typeof part === "object" && part.type === "text") {
          const text = part.text;
          if (typeof text === "string") textParts.push(text);
        }
      }
      content = textParts.join("\n");
    }

    if (content && /data:image\/[a-z+]+;base64,/i.test(content)) {
      content = content.replace(/data:image\/[a-z+]+;base64,[A-Za-z0-9+/=]+/gi, "[image]");
    }

    if (content && content.trim()) {
      const ts = typeof m.timestamp === "number" ? m.timestamp : Date.now();
      result.push({
        id: (typeof m.id === "string" && m.id) ? m.id : generateMessageId(),
        role,
        content: content.trim(),
        timestamp: ts,
      });
    }
  }

  return result;
}

/**
 * Format local date as YYYY-MM-DD.
 * @param {Date} d
 * @returns {string}
 */
function formatLocalDate(d) {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}
