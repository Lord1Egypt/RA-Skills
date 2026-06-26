/**
 * Debug Tools - Memory Replay Debugger (Feature #8)
 * 
 * MCP tools for retrieval debugging:
 *   - memory_replay_query: replay a historical query
 *   - memory_trace_memory: show retrieval history for a specific memory
 *   - memory_explain_rank: explain why a memory ranked where it did
 *   - memory_trace_stats: overall retrieval quality stats
 */

import { z } from 'zod';
import { config } from '../config.js';
import { 
  startRetrievalTrace, 
  recordPipelineStep, 
  recordFinalRanking, 
  finalizeTrace,
  getAllTraces,
  getTraceById,
  getMemoryRetrievalHistory,
  clearAllTraces,
  getMemoryIndexStats,
  searchTraces,
  traceBm25Step,
  traceVectorStep,
  traceMergeStep,
  traceRerankStep,
  traceMmrStep,
  traceDecayStep,
  traceEntityBoostStep,
  traceImportanceBoostStep
} from '../retrieval_tracer.js';
import { replayQuery, replayMemory, diffQueries, explainMemoryRetrieval, findTracesByQuery } from '../memory_replay.js';
import { attributeMemoryScore, getAttributionPieChart, attributeQueryResults } from '../memory_attribution.js';
import { analyzeRetrievalPatterns, getRetrievalQualityScore } from '../trace_analyzer.js';

/**
 * Register debug tools with MCP server
 * @param {object} server - MCP server instance
 */
export function registerDebugTools(server) {
  // Tool: memory_replay_query - replay a historical query
  server.registerTool('memory_replay_query', {
    description: 'Replay a historical query and see its full retrieval pipeline trace. Like "git blame" for memory retrieval - trace exactly how results were retrieved.',
    inputSchema: z.object({
      queryId: z.string().describe('The trace query ID (format: qt-xxx). Use memory_trace_stats to find recent query IDs.'),
    }),
  }, async ({ queryId }) => {
    try {
      const result = await replayQuery(queryId);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Replay error: ${err.message}` }], isError: true };
    }
  });

  // Tool: memory_trace_memory - show retrieval history for a specific memory
  server.registerTool('memory_trace_memory', {
    description: 'Show all queries that retrieved a specific memory and how it ranked. See if a memory is being consistently retrieved or is getting lost.',
    inputSchema: z.object({
      memoryId: z.string().describe('Memory ID to trace'),
    }),
  }, async ({ memoryId }) => {
    try {
      const result = replayMemory(memoryId);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Trace error: ${err.message}` }], isError: true };
    }
  });

  // Tool: memory_explain_rank - explain why a memory ranked where it did
  server.registerTool('memory_explain_rank', {
    description: 'Explain why a memory ranked where it did. Shows which factors contributed to its score: BM25, vector similarity, entity boost, importance, recency, etc.',
    inputSchema: z.object({
      memoryId: z.string().describe('Memory ID to explain'),
      queryId: z.string().optional().describe('Optional specific query trace ID. Uses most recent if not provided.'),
    }),
  }, async ({ memoryId, queryId }) => {
    try {
      const result = explainMemoryRetrieval(memoryId);
      if (result.success) {
        // Also get pie chart
        const pieResult = getAttributionPieChart(memoryId, queryId);
        return {
          content: [{
            type: 'text',
            text: JSON.stringify({
              ...result,
              pieChart: pieResult.pieChart,
              asciiChart: pieResult.asciiChart,
            }, null, 2),
          }],
        };
      }
      return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Explain error: ${err.message}` }], isError: true };
    }
  });

  // Tool: memory_trace_stats - overall retrieval quality stats
  server.registerTool('memory_trace_stats', {
    description: 'Get overall retrieval quality statistics. Shows patterns, biases, failing queries, and tuning suggestions based on all traced searches.',
    inputSchema: z.object({
      limit: z.number().optional().default(200).describe('Number of recent traces to analyze (default 200)'),
    }),
  }, async ({ limit }) => {
    try {
      const analysis = analyzeRetrievalPatterns(limit);
      const qualityScore = getRetrievalQualityScore(limit);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            qualityScore: `${qualityScore}/100`,
            ...analysis,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Stats error: ${err.message}` }], isError: true };
    }
  });

  // Tool: memory_diff_queries - compare two query retrieval paths
  server.registerTool('memory_diff_queries', {
    description: 'Compare two query retrieval paths side by side. See what\'s different between two searches.',
    inputSchema: z.object({
      queryId1: z.string().describe('First query trace ID'),
      queryId2: z.string().describe('Second query trace ID'),
    }),
  }, async ({ queryId1, queryId2 }) => {
    try {
      const result = await diffQueries(queryId1, queryId2);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify(result, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Diff error: ${err.message}` }], isError: true };
    }
  });

  // Tool: memory_search_traces - find traces by query text
  server.registerTool('memory_search_traces', {
    description: 'Search through historical query traces by text. Find all traces that match a query substring.',
    inputSchema: z.object({
      query: z.string().describe('Query text to search for'),
      limit: z.number().optional().default(20).describe('Maximum results to return'),
    }),
  }, async ({ query, limit }) => {
    try {
      const traces = findTracesByQuery(query);
      const limited = traces.slice(0, limit).map(t => ({
        queryId: t.queryId,
        query: t.query,
        timestamp: t.timestamp,
        durationMs: t.durationMs,
        resultCount: t.finalRanking?.length || 0,
      }));
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            found: limited.length,
            total: traces.length,
            traces: limited,
          }, null, 2),
        }],
      };
    } catch (err) {
      return { content: [{ type: 'text', text: `Search error: ${err.message}` }], isError: true };
    }
  });

  // Tool: memory_clear_traces - clear all traces (debug only)
  server.registerTool('memory_clear_traces', {
    description: 'Clear all retrieval traces. Use for debugging or to reset trace storage.',
    inputSchema: z.object({
      confirm: z.boolean().describe('Must be true to confirm clearing'),
    }),
  }, async ({ confirm }) => {
    if (!confirm) {
      return { content: [{ type: 'text', text: 'Set confirm: true to clear traces' }] };
    }
    try {
      clearAllTraces();
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, message: 'All traces cleared' }) }] };
    } catch (err) {
      return { content: [{ type: 'text', text: `Clear error: ${err.message}` }], isError: true };
    }
  });
}

export default registerDebugTools;
