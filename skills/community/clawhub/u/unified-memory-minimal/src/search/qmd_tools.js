/**
 * src/search/qmd_tools.js
 * QMD 搜索后端工具
 */

import { z } from 'zod';
import { QMDSearchBackend, qmdBackend } from './qmd_backend.js';

export function registerQMDTools(server) {

  server.registerTool('memory_qmd_query', {
    description: 'Search using QMD (local hybrid search engine). Requires qmd.enabled=true in config. Falls back gracefully if QMD unavailable.',
    inputSchema: z.object({
      query: z.string().describe('Search query'),
      collections: z.array(z.string()).optional().describe('QMD collections to search'),
      limit: z.number().optional().default(10),
    }),
  }, async ({ query, collections, limit = 10 } = {}) => {
    try {
      const result = await qmdBackend.search({ query, collections, limit });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `QMD search error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_qmd_status', {
    description: 'Check if QMD CLI is available and what collections exist.',
    inputSchema: z.object({}),
  }, async () => {
    try {
      const available = qmdBackend.isAvailable();
      const collections = available ? await qmdBackend.listCollections() : [];
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            qmd_available: available,
            enabled: qmdBackend.enabled,
            configured_collections: qmdBackend.collections,
            actual_collections: collections,
          }, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `QMD status error: ${err.message}` }], isError: true };
    }
  });
}
