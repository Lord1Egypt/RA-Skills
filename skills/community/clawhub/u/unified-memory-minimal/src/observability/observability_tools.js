import { z } from 'zod';
/**
 * Observability Tools - HTTP Server management tools
 */

import { startHttpServer, stopHttpServer } from './http_server.js';

/**
 * Start the memory observability HTTP server
 * @param {number} [port=3849] - Port to listen on
 * @returns {object} tool result
 */
export async function memory_http_start({ port = 3849 }) {
  try {
    const server = await startHttpServer(port);
    return {
      type: 'text',
      text: `✅ Observability HTTP server started on port ${port}`,
    };
  } catch (err) {
    return {
      type: 'text',
      text: `❌ Failed to start HTTP server: ${err.message}`,
    };
  }
}

/**
 * Stop the memory observability HTTP server
 * @returns {object} tool result
 */
export async function memory_http_stop() {
  try {
    await stopHttpServer();
    return {
      type: 'text',
      text: `✅ Observability HTTP server stopped`,
    };
  } catch (err) {
    return {
      type: 'text',
      text: `❌ Failed to stop HTTP server: ${err.message}`,
    };
  }
}

export default { memory_http_start, memory_http_stop };

export function registerObservabilityTools(server) {
  server.registerTool('memory_http_start', {
    description: 'Start the unified-memory HTTP observability server on a given port.',
    inputSchema: z.object({
      port: z.number().optional().default(3849).describe('HTTP port to listen on'),
    }),
  }, memory_http_start);

  server.registerTool('memory_http_stop', {
    description: 'Stop the unified-memory HTTP observability server.',
    inputSchema: z.object({}),
  }, memory_http_stop);
}
