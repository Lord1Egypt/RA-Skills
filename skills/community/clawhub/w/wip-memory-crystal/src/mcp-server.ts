#!/usr/bin/env node
// memory-crystal/mcp-server.ts — MCP tools for Claude Code.
// Wraps core.ts. Registered via .mcp.json.

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { Crystal, RemoteCrystal, resolveConfig, createCrystal } from './core.js';
import { resolveStatePath, stateWritePath } from './ldm.js';
import { setSamplingServer } from './llm.js';
import { existsSync, readFileSync, appendFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const PRIVATE_MODE_PATH = resolveStatePath('memory-capture-state.json');

function isPrivateMode(): boolean {
  try {
    if (existsSync(PRIVATE_MODE_PATH)) {
      const state = JSON.parse(readFileSync(PRIVATE_MODE_PATH, 'utf-8'));
      return state.enabled === false;
    }
  } catch {}
  return false;
}

const METRICS_PATH = stateWritePath('search-metrics.jsonl');

function logSearchMetric(tool: string, query: string, resultCount: number) {
  try {
    const entry = JSON.stringify({
      ts: new Date().toISOString(),
      tool,
      query,
      results: resultCount,
    });
    appendFileSync(METRICS_PATH, entry + '\n');
  } catch {}
}

const config = resolveConfig();
const crystal = createCrystal(config);
const isRemote = crystal instanceof RemoteCrystal;
if (isRemote) {
  process.stderr.write('[memory-crystal] Remote mode: ' + config.remoteUrl + '\n');
}

const server = new Server(
  { name: 'memory-crystal', version: '0.1.0' },
  { capabilities: { tools: {} } }
);

// ── Tool Definitions ──

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'crystal_search',
      description: 'Search memory crystal — semantic search across all agent conversations, files, and stored memories. Returns ranked results with similarity scores.',
      inputSchema: {
        type: 'object' as const,
        properties: {
          query: { type: 'string', description: 'What to search for' },
          limit: { type: 'number', description: 'Max results (default: 5)' },
          agent_id: { type: 'string', description: 'Filter by agent (e.g. "main", "claude-code")' },
          time_filter: { type: 'string', description: 'Only return results newer than this. Relative ("24h", "7d", "30d") or ISO date.' },
          until: { type: 'string', description: 'Only return results older than this. ISO date (e.g. "2026-03-25"). Use with time_filter for date ranges.' },
          quality: { type: 'string', enum: ['fast', 'deep'], description: 'Search quality mode. "fast" (default) uses hybrid search. "deep" adds LLM query expansion + re-ranking.' },
          intent: { type: 'string', description: 'Disambiguate the query without adding search terms. E.g. query "security" + intent "1Password automation" steers toward 1Password results.' },
          candidate_limit: { type: 'number', description: 'Number of candidates for LLM re-ranking (default: 40). More = better recall, slower.' },
          explain: { type: 'boolean', description: 'Return per-result scoring breakdown (FTS, vector, RRF, rerank, recency scores).' },
        },
        required: ['query'],
      },
    },
    {
      name: 'crystal_remember',
      description: 'Store a fact, preference, or observation in memory crystal. Persists across sessions and compaction.',
      inputSchema: {
        type: 'object' as const,
        properties: {
          text: { type: 'string', description: 'The fact or observation to remember' },
          category: {
            type: 'string',
            enum: ['fact', 'preference', 'event', 'opinion', 'skill', 'user', 'feedback', 'project', 'reference'],
            description: 'Category of memory (default: fact)',
          },
        },
        required: ['text'],
      },
    },
    {
      name: 'crystal_forget',
      description: 'Deprecate a memory by ID. Does not delete — marks as deprecated.',
      inputSchema: {
        type: 'object' as const,
        properties: {
          id: { type: 'number', description: 'Memory ID to deprecate' },
        },
        required: ['id'],
      },
    },
    {
      name: 'crystal_status',
      description: 'Show memory crystal status — chunk count, memory count, agents, embedding provider.',
      inputSchema: {
        type: 'object' as const,
        properties: {},
      },
    },
    {
      name: 'crystal_sources_add',
      description: 'Add a directory for source file indexing. Files are chunked, embedded, and searchable via crystal_search. Optional feature... does not affect existing memory capture.',
      inputSchema: {
        type: 'object' as const,
        properties: {
          path: { type: 'string', description: 'Absolute path to the directory to index' },
          name: { type: 'string', description: 'Short name for this collection (e.g. "wipcomputer")' },
        },
        required: ['path', 'name'],
      },
    },
    {
      name: 'crystal_sources_sync',
      description: 'Sync a source collection: scan for new/changed/deleted files and re-index. Run after adding a collection or when files change.',
      inputSchema: {
        type: 'object' as const,
        properties: {
          name: { type: 'string', description: 'Collection name to sync' },
          dry_run: { type: 'boolean', description: 'If true, report what would change without actually indexing' },
        },
        required: ['name'],
      },
    },
    {
      name: 'crystal_sources_status',
      description: 'Show status of all source file collections: file counts, chunk counts, last sync time.',
      inputSchema: {
        type: 'object' as const,
        properties: {},
      },
    },
  ],
}));

// ── Tool Handlers ──

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    await crystal.init();

    // Wire persistent LLM cache to the crystal database
    if (!isRemote && (crystal as any).sqliteDb) {
      const { setLLMCacheDb } = await import('./llm.js');
      setLLMCacheDb((crystal as any).sqliteDb);
    }

    switch (name) {
      case 'crystal_search': {
        const query = args?.query as string;
        const limit = (args?.limit as number) || 5;
        const filter: any = {};
        if (args?.agent_id) filter.agent_id = args.agent_id;
        if (args?.time_filter) filter.since = args.time_filter;
        if (args?.until) filter.until = args.until;
        const intent = args?.intent as string | undefined;
        const candidateLimit = args?.candidate_limit as number | undefined;
        const explain = args?.explain as boolean | undefined;
        const results = isRemote
          ? await crystal.search(query, limit, filter)
          : await (crystal as Crystal).deepSearch(query, limit, filter, { intent, candidateLimit, explain });
        logSearchMetric('crystal_search', query, results.length);

        if (results.length === 0) {
          return { content: [{ type: 'text', text: 'No results found.' }] };
        }

        const freshnessIcon: Record<string, string> = { fresh: "🟢", recent: "🟡", aging: "🟠", stale: "🔴" };
        const formatted = results.map((r, i) => {
          const score = (r.score * 100).toFixed(1);
          const date = r.created_at?.slice(0, 10) || 'unknown';
          const fresh = r.freshness ? `${freshnessIcon[r.freshness]} ${r.freshness}, ` : '';
          return `[${i + 1}] (${fresh}${score}% match, ${r.agent_id}, ${date}, ${r.role})\n${r.text}`;
        }).join('\n\n---\n\n');

        const header = '(Recency-weighted. 🟢 fresh <3d, 🟡 recent <7d, 🟠 aging <14d, 🔴 stale 14d+)\n\n';
        return { content: [{ type: 'text', text: header + formatted }] };
      }

      case 'crystal_remember': {
        if (isPrivateMode()) {
          return { content: [{ type: 'text', text: 'Private mode is on. No memories are being stored. Toggle off to resume.' }] };
        }
        const text = args?.text as string;
        const category = (args?.category || 'fact') as any;
        const id = await crystal.remember(text, category);
        return { content: [{ type: 'text', text: `Remembered (id: ${id}, category: ${category}): ${text}` }] };
      }

      case 'crystal_forget': {
        const id = args?.id as number;
        const ok = crystal.forget(id);
        return {
          content: [{ type: 'text', text: ok ? `Forgot memory ${id}` : `Memory ${id} not found or already deprecated` }],
        };
      }

      case 'crystal_status': {
        const status = await crystal.status();
        const text = [
          `Memory Crystal Status${isRemote ? ' (REMOTE)' : ''}`,
          `  Data dir:   ${status.dataDir}`,
          `  Provider:   ${status.embeddingProvider}`,
          `  Chunks:     ${status.chunks.toLocaleString()}`,
          `  Memories:   ${status.memories}`,
          `  Sources:    ${status.sources}`,
          `  Agents:     ${status.agents.length > 0 ? status.agents.join(', ') : 'none yet'}`,
          `  Sessions:   ${status.capturedSessions} captured`,
          `  Latest:     ${status.latestCapture || 'never'}`,
        ].join('\n');
        return { content: [{ type: 'text', text }] };
      }

      case 'crystal_sources_add': {
        if (isRemote) {
          return { content: [{ type: 'text', text: 'Source indexing not available in remote mode. Index files on the Mac Mini.' }] };
        }
        const path = args?.path as string;
        const collectionName = args?.name as string;
        const col = await (crystal as Crystal).sourcesAdd(path, collectionName);
        return {
          content: [{ type: 'text', text: `Added collection "${col.name}" at ${col.root_path}\nRun crystal_sources_sync with name "${collectionName}" to index files.` }],
        };
      }

      case 'crystal_sources_sync': {
        if (isRemote) {
          return { content: [{ type: 'text', text: 'Source indexing not available in remote mode. Sync files on the Mac Mini.' }] };
        }
        const collectionName = args?.name as string;
        const dryRun = args?.dry_run as boolean;
        const result = await (crystal as Crystal).sourcesSync(collectionName, { dryRun });
        const lines = [
          dryRun ? `Dry run for "${result.collection}":` : `Synced "${result.collection}":`,
          `  Added:   ${result.added} files`,
          `  Updated: ${result.updated} files`,
          `  Removed: ${result.removed} files`,
          `  Chunks:  ${result.chunks_added} embedded`,
          `  Time:    ${(result.duration_ms / 1000).toFixed(1)}s`,
        ];
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      case 'crystal_sources_status': {
        if (isRemote) {
          return { content: [{ type: 'text', text: 'Source indexing not available in remote mode.' }] };
        }
        const sourcesStatus = (crystal as Crystal).sourcesStatus();
        if (sourcesStatus.collections.length === 0) {
          return { content: [{ type: 'text', text: 'No source collections. Use crystal_sources_add to add a directory.' }] };
        }
        const lines = ['Source Collections:'];
        for (const col of sourcesStatus.collections) {
          const syncAgo = col.last_sync_at
            ? `${Math.round((Date.now() - new Date(col.last_sync_at).getTime()) / 60000)}m ago`
            : 'never';
          lines.push(`  ${col.name}: ${col.file_count.toLocaleString()} files, ${col.chunk_count.toLocaleString()} chunks, last sync ${syncAgo}`);
        }
        lines.push(`  Total: ${sourcesStatus.total_files.toLocaleString()} files, ${sourcesStatus.total_chunks.toLocaleString()} chunks`);
        return { content: [{ type: 'text', text: lines.join('\n') }] };
      }

      default:
        return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true };
    }
  } catch (err: any) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
});

// ── Start ──

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);

  // Check if the connected client supports MCP sampling.
  // If so, wire it up as the preferred LLM provider (uses Max subscription, no API key).
  // NOTE: This is a no-op until Claude Code implements sampling (Issue #1785).
  try {
    const clientCapabilities = (server as any).getClientCapabilities?.();
    if (clientCapabilities?.sampling) {
      setSamplingServer(server);
      process.stderr.write('[memory-crystal] MCP sampling available: using client LLM for deep search\n');
    }
  } catch {
    // Client doesn't support sampling yet. Fall through to MLX/API providers.
  }
}

main().catch(err => {
  console.error(`MCP server failed: ${err.message}`);
  process.exit(1);
});
