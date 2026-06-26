/**
 * Context Chunking - Text segmentation for memory chunks
 * Part of Unified Memory v2 Observability
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories, saveMemories } from '../storage.js';
import { createEmbedding } from '../embedding_providers.js';

const HOME = process.env.HOME || '/root';
const WORKSPACE = join(HOME, '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const CHUNKS_FILE = join(MEMORY_DIR, 'chunks.json');

// ── Sentence splitting ──────────────────────────────────────────────────────

const SENTENCE_DELIMITERS = /([.!?。！？]+[\s\n]*)/;
const SENTENCE_JOINER = '__SENT__';

/**
 * Split long paragraph into sentences
 * @param {string} text
 * @returns {string[]}
 */
function splitIntoSentences(text) {
  const trimmed = text.trim();
  if (!trimmed) return [];

  // Split by common sentence delimiters
  const parts = trimmed.split(SENTENCE_DELIMITERS);
  const sentences = [];
  let current = '';

  for (let i = 0; i < parts.length; i++) {
    const part = parts[i];
    const isDelimiter = SENTENCE_DELIMITERS.test(part) && part.trim().length > 0;

    if (isDelimiter) {
      current += part;
      if (current.trim()) sentences.push(current.trim());
      current = '';
    } else {
      current += part;
    }
  }
  if (current.trim()) sentences.push(current.trim());

  return sentences;
}

/**
 * Merge short sentences into chunks not exceeding maxChunkSize
 * @param {string[]} sentences
 * @param {number} maxChunkSize
 * @returns {string[]}
 */
function mergeSentences(sentences, maxChunkSize) {
  const chunks = [];
  let currentChunk = [];

  for (const sentence of sentences) {
    const sentenceSize = sentence.length;
    const currentSize = currentChunk.join(' ').length;

    if (currentSize + sentenceSize + 1 <= maxChunkSize) {
      currentChunk.push(sentence);
    } else {
      if (currentChunk.length > 0) {
        chunks.push(currentChunk.join(' '));
      }
      // If single sentence exceeds limit, split it further
      if (sentenceSize > maxChunkSize) {
        // Break at word boundaries roughly
        const words = sentence.split(/\s+/);
        let subChunk = [];
        let subSize = 0;
        for (const word of words) {
          if (subSize + word.length + 1 > maxChunkSize) {
            if (subChunk.length > 0) {
              chunks.push(subChunk.join(' '));
            }
            subChunk = [word];
            subSize = word.length;
          } else {
            subChunk.push(word);
            subSize += word.length + 1;
          }
        }
        if (subChunk.length > 0) {
          chunks.push(subChunk.join(' '));
        }
      } else {
        currentChunk = [sentence];
      }
    }
  }

  if (currentChunk.length > 0) {
    chunks.push(currentChunk.join(' '));
  }

  return chunks;
}

// ── Chunk storage ──────────────────────────────────────────────────────────

function loadChunks() {
  if (!existsSync(CHUNKS_FILE)) return [];
  try {
    return JSON.parse(readFileSync(CHUNKS_FILE, 'utf-8'));
  } catch { return []; }
}

function saveChunks(chunks) {
  mkdirSync(MEMORY_DIR, { recursive: true });
  writeFileSync(CHUNKS_FILE, JSON.stringify(chunks, null, 2), 'utf-8');
}

// ── Core chunking ───────────────────────────────────────────────────────────

/**
 * Chunk a single piece of text
 * @param {string} text - Raw text to chunk
 * @param {string} memoryId - Memory ID this text belongs to
 * @param {number} index - Index of this memory in the list
 * @param {number} maxChunkSize - Max characters per chunk (default 500)
 * @returns {Array<{chunk_id: string, memory_id: string, index: number, text: string, embedding: any|null}>}
 */
export function chunkText(text, memoryId = '', index = 0, maxChunkSize = 500) {
  const chunks = [];

  // Split by double newlines (paragraphs)
  const paragraphs = text.split(/\n\n+/).filter(p => p.trim().length > 0);
  let chunkIndex = 0;

  for (const para of paragraphs) {
    const trimmedPara = para.trim();
    if (!trimmedPara) continue;

    // If paragraph fits within limit, emit as-is
    if (trimmedPara.length <= maxChunkSize) {
      chunks.push({
        chunk_id: `${memoryId}_${index}_${chunkIndex}`,
        memory_id: memoryId,
        index: chunkIndex,
        text: trimmedPara,
        embedding: null, // computed lazily
      });
      chunkIndex++;
      continue;
    }

    // Split long paragraph into sentences, then merge
    const sentences = splitIntoSentences(trimmedPara);
    const mergedChunks = mergeSentences(sentences, maxChunkSize);

    for (const chunkText of mergedChunks) {
      if (chunkText.trim()) {
        chunks.push({
          chunk_id: `${memoryId}_${index}_${chunkIndex}`,
          memory_id: memoryId,
          index: chunkIndex,
          text: chunkText.trim(),
          embedding: null,
        });
        chunkIndex++;
      }
    }
  }

  return chunks;
}

/**
 * Generate an embedding for a chunk (best-effort)
 * @param {string} text
 * @returns {Promise<any|null>}
 */
export async function embedChunk(text) {
  try {
    if (typeof createEmbedding === 'function') {
      return await createEmbedding(text);
    }
    // fallback: simple hash as pseudo-embedding
    const { createHash } = await import('crypto');
    const hash = createHash('sha256').update(text).digest('base64');
    return { text, hash, model: 'none' };
  } catch {
    return null;
  }
}

/**
 * Re-chunk all memories and persist to chunks.json
 * Returns array of all chunks
 * @param {number} maxChunkSize
 * @returns {Array}
 */
export async function chunkAllMemories(maxChunkSize = 500) {
  const memories = getAllMemories();
  const allChunks = [];

  for (let i = 0; i < memories.length; i++) {
    const mem = memories[i];
    const text = mem.text || mem.content || '';
    if (!text.trim()) continue;

    const memChunks = chunkText(text, mem.id || `mem_${i}`, i, maxChunkSize);

    // Compute embeddings lazily (best-effort)
    for (const chunk of memChunks) {
      chunk.embedding = await embedChunk(chunk.text);
    }

    allChunks.push(...memChunks);
  }

  saveChunks(allChunks);
  return allChunks;
}

/**
 * Get chunks for a specific memory
 * @param {string} memoryId
 * @returns {Array}
 */
export function getChunksForMemory(memoryId) {
  const all = loadChunks();
  return all.filter(c => c.memory_id === memoryId || c.memory_id?.startsWith(memoryId));
}

/**
 * Search chunks for a specific memory
 * @param {string} query
 * @param {string} memoryId
 * @returns {Array}
 */
export function searchChunksInMemory(query, memoryId) {
  const chunks = getChunksForMemory(memoryId);
  const q = query.toLowerCase();
  return chunks.filter(c => (c.text || '').toLowerCase().includes(q));
}

/**
 * Get all chunks (lazy-loaded)
 * @returns {Array}
 */
export function getAllChunks() {
  return loadChunks();
}
