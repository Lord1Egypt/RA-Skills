import { z } from 'zod';
/**
 * Chunk Tools - Memory chunking tools
 */

import {
  chunkText,
  chunkAllMemories,
  getChunksForMemory,
  searchChunksInMemory,
  getAllChunks,
} from './chunker.js';

/**
 * List chunks for a specific memory
 * @param {string} memoryId - Memory ID
 * @returns {object} tool result
 */
export async function memory_chunk_list({ memoryId }) {
  try {
    if (!memoryId) {
      return { type: 'text', text: '❌ memoryId is required' };
    }

    const chunks = getChunksForMemory(memoryId);

    if (chunks.length === 0) {
      return {
        type: 'text',
        text: `No chunks found for memory: ${memoryId}`,
      };
    }

    const lines = [`📦 Chunks for memory \`${memoryId}\` (${chunks.length} total):\n`];
    for (const chunk of chunks) {
      lines.push(`[${chunk.index}] ${chunk.chunk_id}`);
      lines.push(`   ${(chunk.text || '').slice(0, 80)}${(chunk.text || '').length > 80 ? '…' : ''}`);
      lines.push('');
    }

    return { type: 'text', text: lines.join('\n').trim() };
  } catch (err) {
    return { type: 'text', text: `❌ Error listing chunks: ${err.message}` };
  }
}

/**
 * Search within chunks of a specific memory
 * @param {string} query - Search query
 * @param {string} memoryId - Memory ID to search within
 * @returns {object} tool result
 */
export async function memory_chunk_search({ query, memoryId }) {
  try {
    if (!query) {
      return { type: 'text', text: '❌ query is required' };
    }
    if (!memoryId) {
      return { type: 'text', text: '❌ memoryId is required' };
    }

    const results = searchChunksInMemory(query, memoryId);

    if (results.length === 0) {
      return {
        type: 'text',
        text: `No chunks matching "${query}" found in memory: ${memoryId}`,
      };
    }

    const lines = [`🔍 Search results for "${query}" in \`${memoryId}\` (${results.length} matches):\n`];
    for (const chunk of results) {
      lines.push(`[chunk ${chunk.index}] ${chunk.chunk_id}`);
      const snippet = chunk.text || '';
      const q = query.toLowerCase();
      const idx = snippet.toLowerCase().indexOf(q);
      if (idx !== -1) {
        const start = Math.max(0, idx - 30);
        const end = Math.min(snippet.length, idx + query.length + 30);
        lines.push(`   …${snippet.slice(start, end)}…`);
      } else {
        lines.push(`   ${snippet.slice(0, 80)}${snippet.length > 80 ? '…' : ''}`);
      }
      lines.push('');
    }

    return { type: 'text', text: lines.join('\n').trim() };
  } catch (err) {
    return { type: 'text', text: `❌ Error searching chunks: ${err.message}` };
  }
}

export default { memory_chunk_list, memory_chunk_search };

export function registerChunkTools(server) {
  server.registerTool('memory_chunk_list', {
    description: 'List all chunks for a given memory ID.',
    inputSchema: z.object({
      memoryId: z.string().describe('Memory ID to list chunks for'),
    }),
  }, memory_chunk_list);

  server.registerTool('memory_chunk_search', {
    description: 'Search within chunks of a specific memory.',
    inputSchema: z.object({
      query: z.string().describe('Search query'),
      memoryId: z.string().describe('Memory ID to search within'),
    }),
  }, memory_chunk_search);
}
