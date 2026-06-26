/**
 * WAL Tools Registration
 * Inline tool registration for Write-Ahead Log functionality
 */
import { walWrite, walReplay, walTruncate, walStatus, walExport, walImport } from '../wal.js';
import { addMemory, deleteMemory } from '../storage.js';

export function registerWALTools(server, { z }) {
  server.registerTool('memory_wal_write', {
    description: 'Write entry to Write-Ahead Log for durability',
    inputSchema: z.object({
      operation: z.enum(['insert', 'update', 'delete']).describe('Operation type'),
      collection: z.string().describe('Collection name'),
      data: z.any().describe('Data to write')
    })
  }, async ({ operation, collection, data }) => {
    const entry = walWrite({ operation, collection, data });
    return { content: [{ type: 'text', text: JSON.stringify(entry, null, 2) }] };
  });

  server.registerTool('memory_wal_replay', {
    description: 'Replay WAL entries for crash recovery',
    inputSchema: z.object({})
  }, async () => {
    let replayed = 0;
    walReplay((entry) => {
      if (entry.operation === 'insert') addMemory(entry.data);
      else if (entry.operation === 'delete') deleteMemory(entry.data.id);
      replayed++;
    });
    walTruncate();
    return { content: [{ type: 'text', text: `Replayed ${replayed} entries` }] };
  });

  server.registerTool('memory_wal_status', {
    description: 'Get WAL status and statistics',
    inputSchema: z.object({})
  }, async () => {
    const status = walStatus();
    return { content: [{ type: 'text', text: JSON.stringify(status, null, 2) }] };
  });

  server.registerTool('memory_wal_truncate', {
    description: 'Truncate WAL after successful commit',
    inputSchema: z.object({})
  }, async () => {
    walTruncate();
    return { content: [{ type: 'text', text: 'WAL truncated successfully' }] };
  });

  server.registerTool('memory_wal_export', {
    description: 'Export WAL for backup',
    inputSchema: z.object({})
  }, async () => {
    const content = walExport();
    return { content: [{ type: 'text', text: content || 'No WAL content' }] };
  });

  server.registerTool('memory_wal_import', {
    description: 'Import WAL from backup',
    inputSchema: z.object({ walContent: z.string().describe('WAL content to import') })
  }, async ({ walContent }) => {
    walImport(walContent);
    return { content: [{ type: 'text', text: 'WAL imported successfully' }] };
  });
}
