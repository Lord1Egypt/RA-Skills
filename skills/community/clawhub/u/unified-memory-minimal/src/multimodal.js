/**
 * Multimodal Module - Unified image/audio/file analysis + MCP tool registration
 * 
 * Combines vision.js and audio.js into a single entry point.
 * Registers two new MCP tools:
 *   - memory_multimodal: analyze image/audio/file
 *   - memory_visual_search: search memories by visual content description
 */

import { z } from 'zod';
import { analyzeImage } from './core/vision.js';
import { analyzeAudio, analyzeFile } from './core/audio.js';
import { hybridSearch } from './fusion.js';
import { getAllMemories, addMemory } from './storage.js';

/**
 * Analyze image, audio, or file and optionally store as memory.
 * 
 * @param {object} params
 * @param {'image'|'audio'|'file'} params.type - Content type
 * @param {string} [params.imagePath] - Path to image (for type=image)
 * @param {string} [params.imageBase64] - Base64 image (for type=image)
 * @param {string} [params.filePath] - Path to file (for type=audio/file)
 * @param {boolean} [params.storeMemory] - Store as memory (default: true)
 * @param {number} [params.importance] - Importance 0-1 (default: 0.5)
 * @param {string[]} [params.tags] - Additional tags
 */
export async function memoryMultimodalTool({ type, imagePath, imageBase64, filePath, storeMemory = true, importance = 0.5, tags = [] }) {
  try {
    if (type === 'image') {
      const result = await analyzeImage({ imagePath, imageBase64, storeMemory, importance, tags });
      return result;
    }

    if (type === 'audio') {
      if (!filePath) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: 'filePath required for audio type' }) }], isError: true };
      }
      const result = await analyzeAudio({ filePath, storeMemory, importance, tags });
      if (result.error) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: result.error }) }], isError: true };
      }
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            type: 'audio',
            memory_id: result.memory_id,
            analysis: result.analysis,
          }, null, 2),
        }],
      };
    }

    if (type === 'file') {
      if (!filePath) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: 'filePath required for file type' }) }], isError: true };
      }
      const result = await analyzeFile({ filePath, storeMemory, importance, tags });
      if (result.error) {
        return { content: [{ type: 'text', text: JSON.stringify({ error: result.error }) }], isError: true };
      }
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            success: true,
            type: 'file',
            memory_id: result.memory_id,
            analysis: result.analysis,
          }, null, 2),
        }],
      };
    }

    return { content: [{ type: 'text', text: JSON.stringify({ error: `Unknown type: ${type}. Use image, audio, or file.` }) }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: JSON.stringify({ error: err.message }) }], isError: true };
  }
}

/**
 * Search visual/audio memories by content description.
 * 
 * Uses hybrid search on memories with category='visual' or category='audio'.
 * 
 * @param {object} params
 * @param {string} params.query - Text description to search for
 * @param {number} [params.topK] - Number of results (default: 5)
 */
export async function memoryVisualSearchTool({ query, topK = 5 }) {
  try {
    if (!query) {
      return { content: [{ type: 'text', text: JSON.stringify({ error: 'query is required' }) }], isError: true };
    }

    // First get all visual/audio memories
    const allMemories = await getAllMemories();
    const mediaMemories = allMemories.filter(
      m => m.category === 'visual' || m.category === 'audio' || m.category === 'document'
    );

    if (mediaMemories.length === 0) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ count: 0, results: [], message: 'No visual/audio memories found' }, null, 2),
        }],
      };
    }

    // Search within those memories
    const results = await hybridSearch(query, topK, 'hybrid');

    // Filter to only visual/audio memories
    const filtered = results.filter(r => {
      const cat = r.memory?.category;
      return cat === 'visual' || cat === 'audio' || cat === 'document';
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          query,
          count: filtered.length,
          results: filtered.map(r => ({
            id: r.memory.id,
            text: r.memory.text,
            category: r.memory.category,
            importance: r.memory.importance,
            score: Math.round(r.fusionScore * 1000) / 1000,
            tags: r.memory.tags || [],
            created_at: new Date(r.memory.created_at).toISOString(),
          })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: JSON.stringify({ error: err.message }) }], isError: true };
  }
}

/**
 * Register the two multimodal tools on an MCP server instance.
 * Call this after the server is created but before connecting.
 * 
 * @param {object} server - McpServer instance
 */
export function registerMultimodalTools(server) {
  server.registerTool('memory_multimodal', {
    description: 'Analyze image, audio, or file and store the extracted description as a memory. Supports image understanding (via Ollama vision model), audio transcription (via Ollama Whisper), and file content extraction.',
    inputSchema: z.object({
      type: z.enum(['image', 'audio', 'file']).describe('Content type to analyze'),
      imagePath: z.string().optional().describe('Path to image file (for type=image)'),
      imageBase64: z.string().optional().describe('Base64-encoded image data (for type=image)'),
      filePath: z.string().optional().describe('Path to audio or generic file (for type=audio or type=file)'),
      storeMemory: z.boolean().optional().default(true).describe('Store analysis as memory'),
      importance: z.number().optional().default(0.5).describe('Memory importance 0-1'),
      tags: z.array(z.string()).optional().default([]).describe('Additional tags for the memory'),
    }),
  }, async ({ type, imagePath, imageBase64, filePath, storeMemory, importance, tags }) => {
    return memoryMultimodalTool({ type, imagePath, imageBase64, filePath, storeMemory, importance, tags });
  });

  server.registerTool('memory_visual_search', {
    description: 'Search memories by visual or audio content description. Searches memories with category=visual, audio, or document using hybrid BM25+vector search. Useful for finding images, screenshots, or audio recordings by describing their content.',
    inputSchema: z.object({
      query: z.string().describe('Text description to search for in visual/audio memories'),
      topK: z.number().optional().default(5).describe('Number of results to return'),
    }),
  }, async ({ query, topK }) => {
    return memoryVisualSearchTool({ query, topK });
  });
}

export default { registerMultimodalTools, memoryMultimodalTool, memoryVisualSearchTool };
