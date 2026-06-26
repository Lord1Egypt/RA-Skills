/**
 * src/integrations/cloud_tools.js
 * 云备份工具注册
 */

import { z } from 'zod';
import { CloudBackupManager, getCloudBackupManager } from './cloud_backup.js';

export function registerCloudTools(server) {
  const cloudManager = getCloudBackupManager();

  server.registerTool('memory_cloud_sync', {
    description: 'Bidirectional sync memories with cloud backup. Push local, pull remote, merge (newer wins).',
    inputSchema: z.object({
      scope: z.string().optional().describe('Scope to sync (default: agent)'),
    }),
  }, async ({ scope } = {}) => {
    try {
      const result = await cloudManager.sync({ scope });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Cloud sync error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_cloud_push', {
    description: 'Push local memories to cloud backup (SuperMemory or custom REST).',
    inputSchema: z.object({
      scope: z.string().optional().describe('Scope to push (default: all)'),
    }),
  }, async ({ scope } = {}) => {
    try {
      const result = await cloudManager.push({ scope });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Cloud push error: ${err.message}` }], isError: true };
    }
  });

  server.registerTool('memory_cloud_pull', {
    description: 'Pull memories from cloud backup.',
    inputSchema: z.object({
      scope: z.string().optional().describe('Scope to pull'),
      since: z.number().optional().describe('Pull memories updated after this timestamp'),
    }),
  }, async ({ scope, since } = {}) => {
    try {
      const result = await cloudManager.pull({ scope, since });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2)
        }]
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Cloud pull error: ${err.message}` }], isError: true };
    }
  });
}
