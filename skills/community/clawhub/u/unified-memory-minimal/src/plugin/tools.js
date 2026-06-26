/**
 * src/plugin/tools.js
 * OpenClaw Memory Plugin 工具注册
 */

import { z } from 'zod';
import { memory_search, memory_get, memory_write } from './index.js';

/**
 * @param {McpServer} server
 */
export function registerPluginTools(server) {

  server.registerTool('phase3_memory_search', {
    description: 'OpenClaw Memory Plugin interface: search memories via unified-memory pipeline. Use this as the primary memory_search backend.',
    inputSchema: z.object({
      query: z.string().describe('Search query text'),
      scope: z.string().optional().default('agent').describe('Scope: agent/user/project/global'),
      limit: z.number().optional().default(5).describe('Number of results'),
    }),
  }, async ({ query, scope, limit }) => {
    try {
      const result = await memory_search({ query, scope, limit });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('phase3_memory_get', {
    description: 'OpenClaw Memory Plugin interface: get memory content by path (memory/YYYY-MM-DD.md or MEMORY.md).',
    inputSchema: z.object({
      path: z.string().describe('Memory file path'),
      offset: z.number().optional().default(0),
      limit: z.number().optional().default(100),
    }),
  }, async ({ path, offset, limit }) => {
    try {
      const result = await memory_get({ path, offset, limit });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('phase3_memory_write', {
    description: 'OpenClaw Memory Plugin interface: write a new memory entry.',
    inputSchema: z.object({
      content: z.string().describe('Memory content'),
      scope: z.string().optional().default('agent'),
    }),
  }, async ({ content, scope }) => {
    try {
      const result = await memory_write({ content, scope });
      return {
        content: [{ type: 'text', text: JSON.stringify(result, null, 2) }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
    }
  });
}
