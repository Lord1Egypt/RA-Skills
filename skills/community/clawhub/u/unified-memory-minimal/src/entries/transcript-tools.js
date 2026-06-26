/**
 * Transcript Tools Registration
 * Inline tool registration for transcript-first memory system
 */
import {
  transcriptAdd, transcriptGet, transcriptUpdate, transcriptDelete, transcriptList,
  transcriptFindBySource, rebuildMemoriesFromTranscript, getTranscriptSummary,
  getTranscriptStats, verifyTranscriptIntegrity, compactTranscripts
} from '../transcript_first.js';

export function registerTranscriptFirstTools(server, { z }) {
  server.registerTool('memory_transcript_add', {
    description: 'Add a transcript (session/chat/message)',
    inputSchema: z.object({
      type: z.enum(['session', 'chat', 'message']).describe('Transcript type'),
      sourceId: z.string().describe('Source identifier'),
      messages: z.array(z.object({
        role: z.enum(['user', 'assistant', 'system']),
        content: z.string(),
        timestamp: z.number(),
        metadata: z.any()
      })).describe('Messages'),
      summary: z.string().optional().describe('Transcript summary')
    })
  }, async ({ type, sourceId, messages, summary }) => {
    const transcript = transcriptAdd({ type, source_id: sourceId, messages, summary });
    return { content: [{ type: 'text', text: JSON.stringify(transcript, null, 2) }] };
  });

  server.registerTool('memory_transcript_get', {
    description: 'Get transcript by ID',
    inputSchema: z.object({ id: z.string().describe('Transcript ID') })
  }, async ({ id }) => {
    const transcript = transcriptGet(id);
    return { content: [{ type: 'text', text: transcript ? JSON.stringify(transcript, null, 2) : 'Transcript not found' }] };
  });

  server.registerTool('memory_transcript_update', {
    description: 'Update transcript',
    inputSchema: z.object({
      id: z.string().describe('Transcript ID'),
      updates: z.object({
        messages: z.array(z.any()).optional(),
        summary: z.string().optional(),
        memory_count: z.number().optional()
      }).describe('Fields to update')
    })
  }, async ({ id, updates }) => {
    const transcript = transcriptUpdate(id, updates);
    return { content: [{ type: 'text', text: transcript ? JSON.stringify(transcript, null, 2) : 'Transcript not found' }] };
  });

  server.registerTool('memory_transcript_delete', {
    description: 'Delete transcript',
    inputSchema: z.object({ id: z.string().describe('Transcript ID') })
  }, async ({ id }) => {
    const success = transcriptDelete(id);
    return { content: [{ type: 'text', text: success ? 'Transcript deleted' : 'Transcript not found' }] };
  });

  server.registerTool('memory_transcript_list', {
    description: 'List all transcripts',
    inputSchema: z.object({})
  }, async () => {
    const transcripts = transcriptList();
    return { content: [{ type: 'text', text: JSON.stringify(transcripts, null, 2) }] };
  });

  server.registerTool('memory_transcript_find_by_source', {
    description: 'Find transcripts by source ID',
    inputSchema: z.object({ sourceId: z.string().describe('Source ID') })
  }, async ({ sourceId }) => {
    const transcripts = transcriptFindBySource(sourceId);
    return { content: [{ type: 'text', text: JSON.stringify(transcripts, null, 2) }] };
  });

  server.registerTool('memory_transcript_rebuild', {
    description: 'Rebuild memories from transcript',
    inputSchema: z.object({ transcriptId: z.string().describe('Transcript ID') })
  }, async ({ transcriptId }) => {
    const result = rebuildMemoriesFromTranscript(transcriptId);
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });

  server.registerTool('memory_transcript_summary', {
    description: 'Get transcript summary',
    inputSchema: z.object({ transcriptId: z.string().describe('Transcript ID') })
  }, async ({ transcriptId }) => {
    const summary = getTranscriptSummary(transcriptId);
    return { content: [{ type: 'text', text: summary || 'No summary available' }] };
  });

  server.registerTool('memory_transcript_stats', {
    description: 'Get transcript statistics',
    inputSchema: z.object({})
  }, async () => {
    const stats = getTranscriptStats();
    return { content: [{ type: 'text', text: JSON.stringify(stats, null, 2) }] };
  });

  server.registerTool('memory_transcript_verify', {
    description: 'Verify transcript integrity',
    inputSchema: z.object({})
  }, async () => {
    const result = verifyTranscriptIntegrity();
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });

  server.registerTool('memory_transcript_compact', {
    description: 'Compact transcripts (remove deleted)',
    inputSchema: z.object({})
  }, async () => {
    const result = compactTranscripts();
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  });
}
