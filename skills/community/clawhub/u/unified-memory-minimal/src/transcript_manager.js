/**
 * transcript_manager.js - Transcript-first Memory System
 *
 * Stores full conversation transcripts as individual JSON files.
 * Provides transcript search, entity extraction, and context rebuilding.
 *
 * Storage: ~/.openclaw/workspace/memory/transcripts/transcript_<session_id>_<timestamp>.json
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync, readdirSync, statSync } from 'fs';
import { join, basename } from 'path';
import { fileURLToPath } from 'url';
import { config } from './config.js';

const __dirname = fileURLToPath(new URL('.', import.meta.url));

// Transcript storage directory
const TRANSCRIPTS_DIR = join(config.memoryDir, 'transcripts');

// Ensure directory exists
function ensureTranscriptsDir() {
  if (!existsSync(TRANSCRIPTS_DIR)) {
    mkdirSync(TRANSCRIPTS_DIR, { recursive: true });
  }
}

// ============================================================================
// Types
// ============================================================================

/**
 * @typedef {Object} TranscriptMessage
 * @property {'user'|'assistant'|'system'} role
 * @property {string} content
 * @property {string} timestamp
 * @property {string} [message_id]
 */

/**
 * @typedef {Object} Transcript
 * @property {string} id
 * @property {string} session_id
 * @property {string|null} topic
 * @property {string} started_at
 * @property {string|null} ended_at
 * @property {TranscriptMessage[]} messages
 * @property {number} message_count
 * @property {string[]} memory_ids
 * @property {string[]} entities
 * @property {'active'|'completed'|'archived'} status
 */

// ============================================================================
// File I/O
// ============================================================================

/**
 * Get the file path for a transcript
 * @param {string} transcriptId
 * @returns {string}
 */
function getTranscriptPath(transcriptId) {
  return join(TRANSCRIPTS_DIR, `transcript_${transcriptId}.json`);
}

/**
 * Load a transcript from disk
 * @param {string} transcriptId
 * @returns {Transcript|null}
 */
function loadTranscript(transcriptId) {
  const filePath = getTranscriptPath(transcriptId);
  if (!existsSync(filePath)) return null;
  try {
    return JSON.parse(readFileSync(filePath, 'utf-8'));
  } catch {
    return null;
  }
}

/**
 * Save a transcript to disk
 * @param {Transcript} transcript
 */
function saveTranscript(transcript) {
  ensureTranscriptsDir();
  const filePath = getTranscriptPath(transcript.id);
  writeFileSync(filePath, JSON.stringify(transcript, null, 2), 'utf-8');
}

/**
 * Delete a transcript file
 * @param {string} transcriptId
 * @returns {boolean}
 */
function deleteTranscriptFile(transcriptId) {
  const filePath = getTranscriptPath(transcriptId);
  if (!existsSync(filePath)) return false;
  try {
    const { unlinkSync } = require('fs');
    unlinkSync(filePath);
    return true;
  } catch {
    return false;
  }
}

// ============================================================================
// ID Generation
// ============================================================================

/**
 * Generate a unique transcript ID
 * @param {string} sessionId
 * @returns {string}
 */
function generateTranscriptId(sessionId) {
  const seed = `${sessionId}_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
  const hash = seed.split('').reduce((acc, c) => ((acc << 5) - acc + c.charCodeAt(0)) | 0, 0);
  return `t_${Math.abs(hash).toString(36).slice(0, 12)}`;
}

// ============================================================================
// Topic Extraction
// ============================================================================

/**
 * Auto-extract topic from first user message (first 50 chars)
 * @param {string|null} firstUserMessage
 * @returns {string}
 */
function extractTopicFromMessage(firstUserMessage) {
  if (!firstUserMessage) return 'Untitled Conversation';
  const cleaned = firstUserMessage.trim().slice(0, 50);
  return cleaned.length < firstUserMessage.trim().length
    ? cleaned + '...'
    : cleaned;
}

// ============================================================================
// Entity Extraction (simple keyword/NER pattern matching)
// ============================================================================

/**
 * Extract entities from transcript content using simple patterns
 * @param {string} text - Combined text from all messages
 * @returns {string[]}
 */
function extractEntitiesFromText(text) {
  const entities = new Set();

  // Capitalized phrases (2-4 words) - potential proper nouns
  const capitalizedPattern = /\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b/g;
  let match;
  while ((match = capitalizedPattern.exec(text)) !== null) {
    const phrase = match[1].trim();
    // Filter out common false positives
    if (phrase.length > 2 && !COMMON_WORDS.has(phrase.toLowerCase())) {
      entities.add(phrase);
    }
  }

  // Email addresses
  const emailPattern = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
  while ((match = emailPattern.exec(text)) !== null) {
    entities.add(match[0]);
  }

  // URLs
  const urlPattern = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/g;
  while ((match = urlPattern.exec(text)) !== null) {
    entities.add(match[0]);
  }

  // Quoted strings (potential important terms or decisions)
  const quotedPattern = /"([^"]{2,50})"/g;
  while ((match = quotedPattern.exec(text)) !== null) {
    const quoted = match[1].trim();
    if (quoted.length > 2 && !COMMON_WORDS.has(quoted.toLowerCase())) {
      entities.add(quoted);
    }
  }

  // Hashtags (potential topics/projects)
  const hashtagPattern = /#[a-zA-Z0-9_\u4e00-\u9fa5]{2,30}/g;
  while ((match = hashtagPattern.exec(text)) !== null) {
    entities.add(match[0]);
  }

  // Chinese-style entity patterns (牛人, 项目名, etc.) - Chinese capitalized or project-like
  const chinesePattern = /[\u4e00-\u9fa5]{2,10}(?:项目|产品|功能|系统|设计|技术|团队|公司|用户|客户|需求|问题|方案|计划)/g;
  while ((match = chinesePattern.exec(text)) !== null) {
    entities.add(match[0]);
  }

  return Array.from(entities).slice(0, 50); // Limit to 50 entities
}

// Common words to filter out from capitalized phrase extraction
const COMMON_WORDS = new Set([
  'the', 'this', 'that', 'these', 'those', 'there', 'here', 'where', 'when', 'what',
  'which', 'who', 'whom', 'whose', 'why', 'how', 'some', 'any', 'all', 'each',
  'every', 'both', 'few', 'more', 'most', 'other', 'such', 'no', 'nor', 'not',
  'only', 'own', 'same', 'so', 'than', 'too', 'very', 'just', 'also', 'now',
  'then', 'once', 'ever', 'never', 'always', 'often', 'usually', 'sometimes',
  'really', 'very', 'just', 'well', 'quite', 'rather', 'almost', 'actually',
  'probably', 'certainly', 'maybe', 'perhaps', 'might', 'could', 'would', 'should',
  'will', 'shall', 'may', 'must', 'need', 'dare', 'ought', 'used',
  'first', 'second', 'third', 'last', 'next', 'new', 'old', 'good', 'bad',
  'great', 'small', 'big', 'long', 'short', 'high', 'low', 'fast', 'slow',
  'yes', 'no', 'ok', 'okay', 'hey', 'hi', 'hello', 'bye', 'thanks', 'please',
  'sorry', 'excuse', 'pardon', 'apologies',
  // Chinese common words
  '什么', '这个', '那个', '这些', '那些', '一个', '我的', '你的', '他的',
  '我们', '你们', '他们', '她们', '自己', '这个', '那个', '哪个',
  '怎么', '如何', '为什么', '因为', '所以', '但是', '而且', '或者',
  '可以', '能够', '应该', '必须', '需要', '想要', '知道', '觉得',
  '没有', '有的', '一些', '所有', '每个', '其他', '一样', '已经',
  '现在', '今天', '昨天', '明天', '这里', '那里', '这么', '那么',
]);

/**
 * Extract entities from a transcript
 * @param {string} transcriptId
 * @returns {string[]}
 */
export function extractEntities(transcriptId) {
  const transcript = loadTranscript(transcriptId);
  if (!transcript) return [];

  const allText = transcript.messages.map(m => m.content).join(' ');
  return extractEntitiesFromText(allText);
}

// ============================================================================
// Public API
// ============================================================================

/**
 * Create a new transcript session
 * @param {string} [topic] - Optional topic; auto-extracted from first message if not provided
 * @param {string} [sessionId] - Optional session ID; generated if not provided
 * @returns {Transcript}
 */
export async function createTranscript(topic = null, sessionId = null) {
  ensureTranscriptsDir();

  const now = new Date().toISOString();
  const transcriptId = generateTranscriptId(sessionId || `session_${Date.now()}`);
  const resolvedSessionId = sessionId || `session_${Date.now()}`;

  /** @type {Transcript} */
  const transcript = {
    id: transcriptId,
    session_id: resolvedSessionId,
    topic: topic || null, // Will be set when first user message is logged
    started_at: now,
    ended_at: null,
    messages: [],
    message_count: 0,
    memory_ids: [],
    entities: [],
    status: 'active',
  };

  saveTranscript(transcript);
  return transcript;
}

/**
 * Log a message to a transcript
 * @param {string} transcriptId
 * @param {string} role - 'user' | 'assistant' | 'system'
 * @param {string} content - Message content
 * @param {object} [metadata] - Optional metadata (message_id, etc.)
 * @returns {Promise<TranscriptMessage>}
 */
export async function logMessage(transcriptId, role, content, metadata = {}) {
  let transcript = loadTranscript(transcriptId);

  // If transcript doesn't exist, create one
  if (!transcript) {
    transcript = await createTranscript();
  }

  const now = new Date().toISOString();

  /** @type {TranscriptMessage} */
  const message = {
    role,
    content,
    timestamp: now,
    message_id: metadata.message_id || undefined,
  };

  transcript.messages.push(message);
  transcript.message_count = transcript.messages.length;

  // Auto-extract topic from first user message if not set
  if (!transcript.topic && role === 'user') {
    transcript.topic = extractTopicFromMessage(content);
  }

  // Periodically update entities (every 5 messages or on user message)
  if (transcript.messages.length % 5 === 0 || role === 'user') {
    const allText = transcript.messages.map(m => m.content).join(' ');
    transcript.entities = extractEntitiesFromText(allText);
  }

  saveTranscript(transcript);
  return message;
}

/**
 * End a transcript session
 * @param {string} transcriptId
 * @returns {Promise<void>}
 */
export async function endTranscript(transcriptId) {
  const transcript = loadTranscript(transcriptId);
  if (!transcript) return;

  transcript.ended_at = new Date().toISOString();
  transcript.status = 'completed';

  // Final entity extraction
  const allText = transcript.messages.map(m => m.content).join(' ');
  transcript.entities = extractEntitiesFromText(allText);

  saveTranscript(transcript);
}

/**
 * Get transcript by ID
 * @param {string} transcriptId
 * @returns {Promise<Transcript|null>}
 */
export async function getTranscript(transcriptId) {
  return loadTranscript(transcriptId);
}

/**
 * List all transcripts with pagination
 * @param {object} [options]
 * @param {number} [options.limit=20]
 * @param {number} [options.offset=0]
 * @param {string} [options.status] - Filter by status: 'active' | 'completed' | 'archived'
 * @returns {Promise<Transcript[]>}
 */
export async function listTranscripts(options = {}) {
  const { limit = 20, offset = 0, status } = options;
  ensureTranscriptsDir();

  let files;
  try {
    files = readdirSync(TRANSCRIPTS_DIR).filter(f => f.startsWith('transcript_') && f.endsWith('.json'));
  } catch {
    return [];
  }

  const transcripts = [];
  for (const file of files) {
    try {
      const content = readFileSync(join(TRANSCRIPTS_DIR, file), 'utf-8');
      const transcript = JSON.parse(content);
      if (status && transcript.status !== status) continue;
      transcripts.push(transcript);
    } catch {
      // Skip invalid files
    }
  }

  // Sort by started_at desc (most recent first)
  transcripts.sort((a, b) => new Date(b.started_at) - new Date(a.started_at));

  return transcripts.slice(offset, offset + limit);
}

/**
 * Search transcripts by query (full-text search on messages)
 * @param {string} query
 * @param {object} [options]
 * @param {number} [options.limit=10]
 * @returns {Promise<Transcript[]>}
 */
export async function searchTranscripts(query, options = {}) {
  const { limit = 10 } = options;
  const lowerQuery = query.toLowerCase();

  const allTranscripts = await listTranscripts({ limit: 1000 });
  const results = allTranscripts.filter(t => {
    // Search in topic
    if (t.topic && t.topic.toLowerCase().includes(lowerQuery)) return true;
    // Search in messages
    return t.messages.some(m => m.content.toLowerCase().includes(lowerQuery));
  });

  return results.slice(0, limit);
}

/**
 * Rebuild conversational context from a transcript
 * @param {string} transcriptId
 * @returns {Promise<string>}
 */
export async function rebuildContext(transcriptId) {
  const transcript = loadTranscript(transcriptId);
  if (!transcript) return '';

  const lines = [];
  lines.push(`[Transcript: ${transcript.topic || 'Untitled'}]`);
  lines.push(`Session: ${transcript.session_id}`);
  lines.push(`Duration: ${transcript.started_at} to ${transcript.ended_at || 'ongoing'}`);
  lines.push(`Messages: ${transcript.message_count}`);
  if (transcript.entities.length > 0) {
    lines.push(`Entities: ${transcript.entities.join(', ')}`);
  }
  lines.push('');
  lines.push('--- Conversation ---');

  for (const msg of transcript.messages) {
    const role = msg.role === 'assistant' ? 'Assistant' : (msg.role === 'user' ? 'User' : 'System');
    lines.push(`[${role}] ${msg.content}`);
  }

  return lines.join('\n');
}

/**
 * Link a memory to a transcript
 * @param {string} transcriptId
 * @param {string} memoryId
 * @returns {Promise<void>}
 */
export async function linkMemory(transcriptId, memoryId) {
  const transcript = loadTranscript(transcriptId);
  if (!transcript) return;

  if (!transcript.memory_ids.includes(memoryId)) {
    transcript.memory_ids.push(memoryId);
    saveTranscript(transcript);
  }
}

// ============================================================================
// MCP Tool Handler
// ============================================================================

/**
 * Handle memory_transcript MCP tool calls
 * @param {object} args
 * @param {string} [args.action]
 * @param {string} [args.transcript_id]
 * @param {string} [args.topic]
 * @param {string} [args.session_id]
 * @param {string} [args.role]
 * @param {string} [args.content]
 * @param {string} [args.query]
 * @param {string} [args.memory_id]
 * @param {number} [args.limit]
 * @param {number} [args.offset]
 * @param {string} [args.status]
 * @param {object} [args.metadata]
 * @returns {Promise<{content: Array<{type: string, text: string}>, isError?: boolean}>}
 */
export async function memoryTranscriptTool(args) {
  const { action } = args;

  try {
    switch (action) {
      case 'create': {
        const transcript = await createTranscript(args.topic, args.session_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: true,
              transcript: {
                id: transcript.id,
                session_id: transcript.session_id,
                topic: transcript.topic,
                started_at: transcript.started_at,
                status: transcript.status,
              },
            }, null, 2),
          }],
        };
      }

      case 'log': {
        if (!args.transcript_id) {
          return { content: [{ type: 'text', text: 'Error: transcript_id is required' }], isError: true };
        }
        if (!args.role) {
          return { content: [{ type: 'text', text: 'Error: role is required' }], isError: true };
        }
        if (!args.content) {
          return { content: [{ type: 'text', text: 'Error: content is required' }], isError: true };
        }
        const message = await logMessage(args.transcript_id, args.role, args.content, args.metadata);
        const updated = loadTranscript(args.transcript_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              success: true,
              message,
              message_count: updated?.message_count || 0,
              topic: updated?.topic || null,
            }),
          }],
        };
      }

      case 'end': {
        if (!args.transcript_id) {
          return { content: [{ type: 'text', text: 'Error: transcript_id is required' }], isError: true };
        }
        await endTranscript(args.transcript_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, transcript_id: args.transcript_id, status: 'completed' }),
          }],
        };
      }

      case 'get': {
        if (!args.transcript_id) {
          return { content: [{ type: 'text', text: 'Error: transcript_id is required' }], isError: true };
        }
        const transcript = await getTranscript(args.transcript_id);
        if (!transcript) {
          return { content: [{ type: 'text', text: `Transcript ${args.transcript_id} not found` }], isError: true };
        }
        return {
          content: [{
            type: 'text',
            text: JSON.stringify(transcript, null, 2),
          }],
        };
      }

      case 'list': {
        const transcripts = await listTranscripts({
          limit: args.limit || 20,
          offset: args.offset || 0,
          status: args.status || undefined,
        });
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              count: transcripts.length,
              transcripts: transcripts.map(t => ({
                id: t.id,
                session_id: t.session_id,
                topic: t.topic,
                started_at: t.started_at,
                ended_at: t.ended_at,
                message_count: t.message_count,
                status: t.status,
                entity_count: t.entities.length,
                memory_count: t.memory_ids.length,
              })),
            }, null, 2),
          }],
        };
      }

      case 'search': {
        if (!args.query) {
          return { content: [{ type: 'text', text: 'Error: query is required' }], isError: true };
        }
        const results = await searchTranscripts(args.query, { limit: args.limit || 10 });
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              query: args.query,
              count: results.length,
              results: results.map(t => ({
                id: t.id,
                session_id: t.session_id,
                topic: t.topic,
                started_at: t.started_at,
                message_count: t.message_count,
                status: t.status,
                matched_messages: t.messages.filter(m => m.content.toLowerCase().includes(args.query.toLowerCase())).length,
              })),
            }, null, 2),
          }],
        };
      }

      case 'rebuild': {
        if (!args.transcript_id) {
          return { content: [{ type: 'text', text: 'Error: transcript_id is required' }], isError: true };
        }
        const context = await rebuildContext(args.transcript_id);
        return {
          content: [{
            type: 'text',
            text: context,
          }],
        };
      }

      case 'link_memory': {
        if (!args.transcript_id) {
          return { content: [{ type: 'text', text: 'Error: transcript_id is required' }], isError: true };
        }
        if (!args.memory_id) {
          return { content: [{ type: 'text', text: 'Error: memory_id is required' }], isError: true };
        }
        await linkMemory(args.transcript_id, args.memory_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ success: true, transcript_id: args.transcript_id, linked_memory_id: args.memory_id }),
          }],
        };
      }

      case 'extract_entities': {
        if (!args.transcript_id) {
          return { content: [{ type: 'text', text: 'Error: transcript_id is required' }], isError: true };
        }
        const entities = extractEntities(args.transcript_id);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({ transcript_id: args.transcript_id, entities, count: entities.length }, null, 2),
          }],
        };
      }

      default:
        return {
          content: [{
            type: 'text',
            text: `Error: Unknown action '${action}'. Valid actions: create, log, end, get, list, search, rebuild, link_memory, extract_entities`,
          }],
          isError: true,
        };
    }
  } catch (err) {
    return {
      content: [{ type: 'text', text: `Transcript error [${action}]: ${err.message}` }],
      isError: true,
    };
  }
}

export default { memoryTranscriptTool };
