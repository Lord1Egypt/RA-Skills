/**
 * Evidence Tools Registration
 * Inline tool registration for evidence chain functionality
 */
import { evidenceAdd, evidenceGet, evidenceFindByType, evidenceFindBySource, evidenceStats } from '../evidence.js';

export function registerEvidenceTools(server, { z }) {
  server.registerTool('memory_evidence_add', {
    description: 'Add evidence to a memory\'s chain',
    inputSchema: z.object({
      memoryId: z.string().describe('Memory ID'),
      type: z.enum(['transcript', 'message', 'manual', 'inference']).describe('Evidence type'),
      sourceId: z.string().describe('Source identifier'),
      confidence: z.number().min(0).max(1).describe('Confidence score'),
      context: z.string().describe('Evidence context')
    })
  }, async ({ memoryId, type, sourceId, confidence, context }) => {
    const chain = evidenceAdd(memoryId, { type, sourceId, confidence, context });
    return { content: [{ type: 'text', text: JSON.stringify(chain, null, 2) }] };
  });

  server.registerTool('memory_evidence_get', {
    description: 'Get evidence chain for a memory',
    inputSchema: z.object({ memoryId: z.string().describe('Memory ID') })
  }, async ({ memoryId }) => {
    const chain = evidenceGet(memoryId);
    return { content: [{ type: 'text', text: chain ? JSON.stringify(chain, null, 2) : 'No evidence found' }] };
  });

  server.registerTool('memory_evidence_find_by_type', {
    description: 'Find memories by evidence type',
    inputSchema: z.object({ type: z.string().describe('Evidence type to filter by') })
  }, async ({ type }) => {
    const memories = evidenceFindByType(type);
    return { content: [{ type: 'text', text: JSON.stringify(memories, null, 2) }] };
  });

  server.registerTool('memory_evidence_find_by_source', {
    description: 'Find memories by source ID',
    inputSchema: z.object({ sourceId: z.string().describe('Source ID to filter by') })
  }, async ({ sourceId }) => {
    const memories = evidenceFindBySource(sourceId);
    return { content: [{ type: 'text', text: JSON.stringify(memories, null, 2) }] };
  });

  server.registerTool('memory_evidence_stats', {
    description: 'Get evidence statistics',
    inputSchema: z.object({})
  }, async () => {
    const stats = evidenceStats();
    return { content: [{ type: 'text', text: JSON.stringify(stats, null, 2) }] };
  });
}
