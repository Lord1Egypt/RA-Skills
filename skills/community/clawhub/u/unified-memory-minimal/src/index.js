/**
 * Unified Memory MCP Server v1.1 - Full-featured memory system
 * Complete port from Python unified-memory to Node.js
 */

import { z } from 'zod';
import { McpServer } from '/root/.openclaw/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/mcp.js';
import { StdioServerTransport } from '/root/.openclaw/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/stdio.js';
import http from 'http';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Tool utilities (ported from memory-tencentdb)
import { CheckpointManager } from './utils/checkpoint.js';
import { CleanContextRunner, parseModelRef, resolveModelFromMainConfig, prewarmEmbeddedAgent } from './utils/clean_context_runner.js';
import { sanitizeText, shouldCaptureL0, shouldExtractL1, shouldCapture, looksLikePromptInjection, escapeXmlTags, sanitizeJsonForParse, pickRecentUnique } from './utils/sanitize.js';
import { SerialQueue } from './utils/serial_queue.js';
import { ManagedTimer } from './utils/managed_timer.js';
import { SessionFilter } from './utils/session_filter.js';
import { BackupManager } from './utils/backup.js';
// v4.2.0: Hooks (from memory-tencentdb)
import { performAutoCapture } from './hooks/auto_capture.js';
import { performAutoRecall } from './hooks/auto_recall.js';
// v4.2.0: Conversation
import { recordConversation } from './conversation/l0_recorder.js';
// v4.2.0: Record / L1
import { batchDedup } from './record/l1_dedup.js';
// v4.2.0: Scene
import { generateSceneNavigation, stripSceneNavigation } from './scene/scene_navigation.js';
import { readSceneIndex, syncSceneIndex } from './scene/scene_index.js';
import { parseSceneBlock, formatSceneBlock } from './scene/scene_format.js';
// v4.2.0: Persona
import { PersonaTrigger } from './persona/persona_trigger.js';
import { PersonaGenerator } from './persona/persona_generator.js';
// v4.2.0: Prompts
import { CONFLICT_DETECTION_SYSTEM_PROMPT, formatBatchConflictPrompt } from './prompts/l1_dedup.js';
import { EXTRACT_MEMORIES_SYSTEM_PROMPT, formatExtractionPrompt } from './prompts/l1_extraction.js';
import { buildPersonaPrompt } from './prompts/persona_generation.js';
import { buildSceneExtractionPrompt } from './prompts/scene_extraction.js';
// v4.2.0: Tools
import { executeConversationSearch, formatConversationSearchResponse } from './tools/conversation_search.js';
import { executeMemorySearch, formatSearchResponse } from './tools/memory_search.js';
import { extractWords } from './utils/text_utils.js';

import { config, log as configLog } from './config.js';
import { log as structuredLog, getLogger } from './logger.js';
import { metrics, recordSearchLatency, recordStore, recordError } from './metrics.js';
import { startTrace, endTrace, getTraceExport, clearTrace } from './tracer.js';
import { getAllMemories, getMemory, addMemory, deleteMemory, touchMemory, saveMemories } from './storage.js';
import { memoryCompose } from './tools/memory_compose.js';
import { hybridSearch } from './fusion.js';
import { analyzeInsights } from './tools/insights.js';
import { exportMemories } from './tools/export.js';
import { dedupMemories } from './tools/dedup.js';
import { decayMemories } from './tools/decay.js';
import { askQuestion } from './tools/qa.js';
import { memoryPreferenceSlotsTool } from './preference_slots.js';
import { memoryLessonsTool } from './lesson.js';
import { extractImportantInfo, isSensitive, autoStore } from './tools/autostore.js';
import { ConcurrentSearch } from './tools/concurrent_search.js';
import { cmdPredict } from './tools/predict.js';
import { cmdRecommend } from './tools/recommend.js';
import { MemoryInference, cmdInference } from './tools/inference.js';
import { MemorySummarizer, cmdSummary } from './tools/summary.js';
import { FeedbackLearner, OUTCOME_HELPFUL, OUTCOME_IRRELEVANT, OUTCOME_WRONG, OUTCOME_OUTDATED } from './tools/feedback_learner.js';
import { qmdSearch } from './tools/qmd_search.js';
import { TemplateManager, cmdTemplates } from './tools/templates.js';
import { shouldStore, qualityScore, learnNoisePattern, getNoiseCount } from './noise.js';
import { routeSearch, INTENT_TYPES } from './intent.js';
import { extractMemories, batchExtract } from './extract.js';
import { getProfile } from './profile.js';
import { addLearning, addError, getLearnings, getErrors, getStats } from './reflection.js';
import { initWal, flushWal, listWalFiles, logOp } from './wal.js';
import { assignTiers, partitionByTier, redistributeTiers, compressColdTier, autoMigrateTiers } from './tier.js';
import { memoryTierStatusTool, memoryTierMigrateTool, memoryTierCompressTool } from './tier_tools.js';
import { shouldSkipRetrieval } from './adaptive.js';
import { buildBM25Index, bm25Search } from './bm25.js';
import { getEmbedding } from './vector_lancedb.js';
import { mmrSelect, mmrSelectWithEmbedding } from './mmr.js';
import { LlmReranker, keywordRerank } from './rerank.js';
import { CrossEncoderRerank, rerankResults } from './tools/rerank.js';
import { normalizeScope, filterByScope, SCOPE_LEVELS, SCOPE_HIERARCHY } from './scope.js';
import { walWrite, walReplay, walTruncate, walStatus, walExport, walImport, readWal, closeWal } from './wal.js';
import { evidenceAdd, evidenceGet, evidenceFindByType, evidenceFindBySource, evidenceGetHighestConfidence, evidenceGetHighConfidence, evidenceExport, evidenceImport, evidenceStats } from './evidence.js';
import { organizeMemories, compressTier, archiveOldMemories, getTierStats, fullOrganize } from './organize.js';
import { transcriptAdd, transcriptGet, transcriptUpdate, transcriptDelete, transcriptList, transcriptFindBySource, rebuildMemoriesFromTranscript, getMemoriesForTranscript, getTranscriptSummary, getTranscriptStats, exportTranscripts, importTranscripts, verifyTranscriptIntegrity, compactTranscripts } from './transcript_first.js';
import { getProactiveManager } from './proactive_manager.js';
import { getReminderScheduler } from './reminder.js';
import { enhancedPredictRecall, predictRelatedOnAccess, predictHighValueMemories } from './tools/predict.js';
import { registerMultimodalTools } from './multimodal.js';
import { registerEpisodeTools } from './episode/episode_tools.js';
import { registerRerankTools } from './rerank/rerank_tools.js';
import { registerRefreshTools } from './consolidate/refresh_tools.js';
import { registerProceduralTools } from './procedural/procedural_tools.js';
import { registerRuleTools } from './rule/rule_tools.js';
import { registerObservabilityTools } from './observability/observability_tools.js';
import { registerChunkTools } from './chunking/chunk_tools.js';
import { registerPluginTools } from './plugin/tools.js';
import { registerGitTools } from './integrations/git_tools.js';
import { registerCloudTools } from './integrations/cloud_tools.js';

// God Object split: modular tool registrations (extracted to src/entries/)
import { registerWALTools } from './entries/wal-tools.js';
import { registerEvidenceTools } from './entries/evidence-tools.js';
import { registerOrganizeTools } from './entries/organize-tools.js';
import { registerTranscriptFirstTools } from './entries/transcript-tools.js';
import { registerSceneBlockTools, registerPipelineTools } from './entries/scene-tools.js';
import { registerCleanerTools, registerLocalEmbeddingTools, registerBenchmarkTools, registerEntityTools, registerPluginToolsInline } from './entries/system-tools.js';

// v4.3: Supermemory Features
import { getProfile as getDynamicProfile, getProfiles, invalidateCache as invalidateProfileCache } from './profile/dynamic_profile.js';
import { detectContradiction, detectContradictions, resolveContradictions, dedupWithContradictionResolution } from './forgetting/contradiction_resolver.js';
import { isTemporalMemory, extractExpiryTime, isExpired, extractExpiryTimes, cleanExpiredMemories, startExpiryChecker } from './forgetting/temporal_expiry.js';
import { hybridSearch as hybridSearchEngine, searchMemoriesOnly, searchDocumentsOnly, getSearchStats } from './search/hybrid_search.js';
import { BaseConnector, registerConnector, createConnector, listConnectors, createConnectors } from './connectors/index.js';
import { BaseExtractor, TextExtractor, registerExtractor, createExtractor, getExtractorForFile, autoExtract, listExtractors } from './extractors/index.js';
import { registerDecayStatsTool } from './decay/weibull_tools.js';

// Feature #10: Preference Slots
import { memoryPreferenceGetTool, memoryPreferenceSetTool, memoryPreferenceInferTool, memoryPreferenceExplainTool } from './tools/preference_tools.js';

// Feature #11 + v2.7.0: Semantic Versioning + 完整修订历史
import { memoryVersionListTool, memoryVersionDiffTool, memoryVersionRestoreTool } from './tools/version_tools.js';

// P0-2: Entity Tools
import { memoryEntityExtractTool, memoryEntityLinkTool, memoryEntityNeighborsTool, memoryEntitySearchTool } from './tools/entity_tools.js';

// v2.7.0: Identity Memory Tools
import { memoryIdentityExtractTool, memoryIdentityUpdateTool, memoryIdentityGetTool } from './tools/identity_tools.js';

// P1-4: Git Notes
import { memoryGitnotesBackupTool, memoryGitnotesRestoreTool } from './tools/git_notes.js';
import { memoryGitNotesTool } from './git_notes.js';

// P1-6: Auto Extractor
import { AutoExtractor } from './tools/auto_extractor.js';

// P1-5: Token Budget
import { calculateBudget, TokenAllocator, getAllocator, allocateTokens, getBudgetStatus, compressIfNeeded, recalculateBudgets } from './budget.js';

// P2-7: Cloud Backup (from existing collab/cloud.js)
import { MemoryBackup, CloudConfig } from './collab/cloud.js';

// Cloud Backup API (managed multi-provider backup with versioning, retention, sync)
import { memoryCloudBackupApiTool } from './cloud_backup_api.js';

// Session State RAM Layer
import { memorySessionTool } from './session_state.js';

// Cognitive Memory Scheduler (curiosity-driven exploration)
import { memoryCognitiveTool } from './cognitive_scheduler.js';

// P0-3: Transcript Manager (Transcript-first memory system)
import { memoryTranscriptTool } from './transcript_manager.js';

// P0-4: Revision Manager (version conflict detection)
import { registerRevisionTools } from './revision_manager.js';

// Memory Lanes - Parallel swim lanes for different memory contexts
import { memoryLanesTool } from './lanes_manager.js';

// P1-1: QMD Deep Integration
import { isQMDEngine, getQMDEngineStatus, qmdEngineSearch, vectorSearch as qmdVectorSearch } from './qmd_integration.js';

// P2-1: Semantic Cache
import { memoryCacheTool } from './cache_semantic.js';

// P2-2: Incremental Sync
import { memorySyncTool } from './sync_incremental.js';

// P0-3: Transcript logging (simple file-based)
import { existsSync, mkdirSync, appendFileSync } from 'fs';
import { join } from 'path';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const TRANSCRIPTS_DIR = join(__dirname, '..', 'transcripts');

function ensureTranscriptsDir() {
  if (!existsSync(TRANSCRIPTS_DIR)) mkdirSync(TRANSCRIPTS_DIR, { recursive: true });
}

function logTranscript(operation, data) {
  try {
    ensureTranscriptsDir();
    const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
    const logFile = join(TRANSCRIPTS_DIR, `${today}.jsonl`);
    const entry = JSON.stringify({ op: operation, ...data, ts: new Date().toISOString() }) + '\n';
    appendFileSync(logFile, entry, 'utf8');
  } catch {
    // Best-effort logging
  }
}

const server = new McpServer(
  { name: 'unified-memory-mcp', version: '1.1.0' },
  { capabilities: { tools: {} } }
);

// ============ v4.0 Storage Gateway ============

let _v4Gateway = null;
async function getV4Gateway() {
  if (!_v4Gateway) {
    const { StorageGateway } = await import('./v4/storage-gateway.js');
    _v4Gateway = new StorageGateway();
    await _v4Gateway.init();
  }
  return _v4Gateway;
}

// ============ Core Search Tools ============

server.registerTool('memory_search', {
  description: 'Search memories using BM25 + Vector hybrid search powered by Ollama. Returns relevant memories ranked by relevance. Scope filtering enables true multi-tenant isolation. P2-8: scope=team searches TEAM scope + all USER scope memories.',
  inputSchema: z.object({
    query: z.string().describe('Search query text'),
    topK: z.number().optional().default(5).describe('Number of results to return'),
    mode: z.enum(['hybrid', 'bm25', 'vector']).optional().default('hybrid').describe('Search mode: hybrid=BM25+vector, bm25=keyword only, vector=semantic only'),
    scope: z.string().optional().describe('Scope filter: AGENT, USER, TEAM, GLOBAL, or team (P2-8: team = TEAM + all USER scopes)'),
  }),
}, async ({ query, topK = 5, mode = 'hybrid', scope }) => {
  const span = startTrace('memory_search', { query: query.slice(0, 50), scope: mode });
  const timer = metrics.timer('memory_search', { scope: mode });
    structuredLog.info( `Search: query="${query}" mode=${mode} topK=${topK} scope=${scope}`);
  try {
    // P2-8: scope=team → search TEAM scope + all USER scope memories
    let effectiveScope = scope || null;
    if (scope && scope.toLowerCase() === 'team') {
      // TEAM + all USER scope: pass TEAM for now (hybridSearch handles it)
      effectiveScope = 'TEAM';
    }

    const results = await hybridSearch(query, topK, mode, effectiveScope);

    // P1-5: token budget info
    const budget = calculateBudget({ query, topK });
    const maxTokens = budget.contextBudget;
    const usedTokens = budget.queryTokens + (results.reduce((acc, r) => acc + (r.memory?.text?.length || 0), 0) / 4);
    const remainingTokens = Math.max(0, maxTokens - usedTokens);
    const percentUsed = maxTokens > 0 ? Math.round((usedTokens / maxTokens) * 1000) / 10 : 0;
    const warning = percentUsed > 80 ? 'Token budget >80% utilized' : null;

    for (const r of results) {
      touchMemory(r.memory.id);
    }
    const duration = timer.end();
    recordSearchLatency(duration * 1000, mode);
    endTrace(span);
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          count: results.length,
          query,
          mode,
          scope: scope || null,
          results: results.map((r) => ({
            id: r.memory.id,
            text: r.memory.text,
            category: r.memory.category,
            importance: r.memory.importance,
            score: Math.round(r.fusionScore * 1000) / 1000,
            highlight: r.highlight,
            created_at: new Date(r.memory.created_at).toISOString(),
          })),
          token_budget: {
            used_tokens: Math.round(usedTokens),
            max_tokens: maxTokens,
            remaining_tokens: Math.round(remainingTokens),
            percent_used: percentUsed,
            warning,
          },
        }, null, 2),
      }],
    };
  } catch (err) {
    const duration = timer.end();
    recordSearchLatency(duration * 1000, mode);
    recordError('search');
    endTrace(span, { error: err.message }, 'error');
    structuredLog.error( `Search failed: ${err.message}`);
    return { content: [{ type: 'text', text: `Search error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_store', {
  description: 'Store a new memory with content, category, importance and tags. P0-1: WAL logging. P0-3: transcript logging. P1-6: auto-extracts structured facts when category=general and importance>0.7.',
  inputSchema: z.object({
    text: z.string().describe('Memory content (required)'),
    category: z.string().optional().default('general').describe('Category: preference, fact, decision, entity, reflection, or other'),
    importance: z.number().optional().default(0.5).describe('Importance score 0-1'),
    tags: z.array(z.string()).optional().default([]).describe('Tags for the memory'),
    scope: z.string().optional().describe('Scope: AGENT, USER, TEAM, GLOBAL (default GLOBAL)'),
    source: z.string().optional().default('manual').describe('Source of this store: manual, auto, extraction'),
  }),
}, async ({ text, category = 'general', importance = 0.5, tags = [], scope, source = 'manual' }) => {
  const span = startTrace('memory_store', { category });
    structuredLog.info( `Store: text="${text.slice(0, 50)}..." category=${category} source=${source}`);
  try {
    // P0-1: WAL logging before store
    logOp({ op: 'store', text: text.slice(0, 100), category, importance, scope, source, ts: Date.now() });

    // P0-3: transcript logging
    logTranscript('store', { text: text.slice(0, 200), category, importance, tags, scope, source });

    const mem = addMemory({ text, category, importance, tags, scope });
    recordStore(Buffer.byteLength(text, 'utf8'));

    // P1-6: Auto-extract when category=general and importance>0.7
    let autoExtracted = null;
    if (category === 'general' && importance > 0.7) {
      try {
        const extractor = new AutoExtractor();
        const extracted = await extractor.extractFromConversation(text, true);
        if (extracted && extracted.length > 0) {
          autoExtracted = extracted;
          // Store each extracted fact as a separate memory with extraction source
          for (const ex of extracted) {
            addMemory({
              text: ex.text,
              category: ex.category,
              importance: ex.importance,
              tags: ['auto-extracted', ...(ex.matched_keyword ? [ex.matched_keyword] : [])],
              scope,
              source: 'extraction',
            });
          }
        }
      } catch {
        // Auto-extract is best-effort; don't fail the store
      }
    }

    endTrace(span);
    const result = { success: true, id: mem.id };
    if (autoExtracted) {
      result.auto_extracted = autoExtracted.length;
    }
    return { content: [{ type: 'text', text: JSON.stringify(result) }] };
  } catch (err) {
    recordError('store');
    endTrace(span, { error: err.message }, 'error');
    structuredLog.error( `Store failed: ${err.message}`);
    return { content: [{ type: 'text', text: `Store error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_list', {
  description: 'List all stored memories with their metadata.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const memories = await getAllMemories();
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          count: memories.length,
          memories: memories.map((m) => ({
            id: m.id,
            text: m.text.slice(0, 100),
            category: m.category,
            importance: m.importance,
            created_at: new Date(m.created_at).toISOString(),
          })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `List error: ${err.message}` }], isError: true };
  }
});

// ============ Prompt Composition API (Task #1) ============

server.registerTool('memory_compose', {
  description: 'Compose a memory context block for prompt injection. Selects memories by priority (PIN > HOT > WARM > COLD) to fill a target token budget. Supports category filtering and query-biased selection. Input: last N messages (conversation context) + target token count + optional category filter.',
  inputSchema: z.object({
    messages: z.array(z.object({
      role: z.string().optional(),
      content: z.union([z.string(), z.record(z.string(), z.unknown())]),
    })).optional().default([]).describe('Conversation messages (last N) to use as context'),
    targetTokens: z.number().optional().default(2000).describe('Target token budget for composed memory block'),
    categories: z.array(z.string()).optional().default([]).describe('Filter memories by category (e.g. preference, decision). Empty = all categories.'),
    query: z.string().optional().describe('Search query to bias memory selection (uses hybrid search to boost relevance)'),
    messageWindow: z.number().optional().default(10).describe('How many recent messages to include from the conversation'),
  }),
}, async ({ messages = [], targetTokens = 2000, categories = [], query, messageWindow = 10 }) => {
  try {
    const result = await memoryCompose({
      messages,
      targetTokens,
      categories,
      query,
      messageWindow,
    });
    return {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `memory_compose error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_delete', {
  description: 'Delete a memory by its ID. P0-1: WAL logged. P0-3: transcript logged.',
  inputSchema: z.object({
    id: z.string().describe('Memory ID to delete'),
  }),
}, async ({ id }) => {
  try {
    // P0-1: WAL logging before delete
    logOp({ op: 'delete', id, ts: Date.now() });
    // P0-3: transcript logging
    logTranscript('delete', { id });
    const success = deleteMemory(id);
    return { content: [{ type: 'text', text: JSON.stringify({ success }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Delete error: ${err.message}` }], isError: true };
  }
});

// ============ v4.0 Tools (Phase 1: StorageGateway + Incremental BM25) ============
// v4.0 tools use the new StorageGateway with persistent SQLite schema.
// These are additive to v3 tools and can be used alongside existing ones.

server.registerTool('memory_v4_stats', {
  description: '[v4.0] Get storage gateway statistics. Use this for debugging Phase 1 StorageGateway.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const stats = await gw.stats();
    return {
      content: [{ type: 'text', text: JSON.stringify({ v4: true, ...stats }, null, 2) }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `v4 stats error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_search', {
  description: '[v4.0] Search memories using v4.0 StorageGateway with incremental BM25 (no full rebuild). Additive to memory_search.',
  inputSchema: z.object({
    query: z.string().describe('Search query'),
    topK: z.number().optional().default(5).describe('Number of results'),
    scope: z.string().optional().describe('Scope filter: USER, TEAM, AGENT, GLOBAL'),
  }),
}, async ({ query, topK = 5, scope }) => {
  try {
    const gw = await getV4Gateway();
    const results = await gw.searchMemories(query, { topK, scope });
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          v4: true,
          engine: 'incremental_bm25',
          count: results.length,
          results: results.map(r => ({
            id: r.id,
            text: r.text,
            category: r.category,
            importance: r.importance,
            score: r.score,
            scope: r.scope,
          })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `v4 search error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_store', {
  description: '[v4.0] Store a memory via v4.0 StorageGateway (WAL + incremental index in one transaction).',
  inputSchema: z.object({
    text: z.string().describe('Memory text content'),
    category: z.string().optional().default('general'),
    importance: z.number().optional().default(0.5),
    scope: z.string().optional().default('USER'),
    tags: z.array(z.string()).optional(),
  }),
}, async ({ text, category = 'general', importance = 0.5, scope = 'USER', tags = [] }) => {
  try {
    const gw = await getV4Gateway();
    const mem = await gw.writeMemory({ text, category, importance, scope, tags });
    return {
      content: [{ type: 'text', text: JSON.stringify({ v4: true, id: mem.id, success: true }) }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `v4 store error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_list', {
  description: '[v4.0] List memories via v4.0 StorageGateway with B-tree scope filtering.',
  inputSchema: z.object({
    scope: z.string().optional().describe('Scope filter: USER, TEAM, AGENT, GLOBAL'),
    category: z.string().optional(),
    tier: z.string().optional(),
    limit: z.number().optional().default(50),
  }),
}, async ({ scope, category, tier, limit = 50 }) => {
  try {
    const gw = await getV4Gateway();
    const memories = await gw.getMemories({ scope, category, tier, limit });
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          v4: true,
          count: memories.length,
          memories: memories.map(m => ({ id: m.id, text: m.text, category: m.category, importance: m.importance, scope: m.scope })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `v4 list error: ${err.message}` }], isError: true };
  }
});

/**
 * Reciprocal Rank Fusion — used by memory_v4_hybrid_search
 * @param {Array<{id: string, score: number}>[]} resultLists
 * @param {number} [k=60]
 */
function rrfFuse(resultLists, k = 60) {
  const scores = new Map();
  for (const results of resultLists) {
    for (let i = 0; i < results.length; i++) {
      const memId = results[i].id;
      const rrfScore = 1 / (k + i + 1);
      if (scores.has(memId)) {
        scores.get(memId).fusionScore += rrfScore;
        scores.get(memId).rankCount++;
      } else {
        scores.set(memId, {
          id: memId,
          text: results[i].text,
          category: results[i].category,
          importance: results[i].importance,
          scope: results[i].scope,
          bm25Score: results[i].bm25Score,
          vectorScore: results[i].vectorScore,
          fusionScore: rrfScore,
          rankCount: 1,
        });
      }
    }
  }
  return Array.from(scores.values()).sort((a, b) => b.fusionScore - a.fusionScore);
}

server.registerTool('memory_v4_hybrid_search', {
  description: '[v4.0 Phase 2] Hybrid search using StorageGateway incremental BM25 + Ollama vector with RRF fusion. Phase 2: hybrid search.',
  inputSchema: z.object({
    query: z.string().describe('Search query text'),
    topK: z.number().optional().default(5).describe('Number of final results'),
    scope: z.string().optional().describe('Scope filter: USER, TEAM, AGENT, GLOBAL'),
    bm25Weight: z.number().optional().default(0.5).describe('BM25 weight in fusion (0-1)'),
  }),
}, async ({ query, topK = 5, scope, bm25Weight = 0.5 }) => {
  try {
    const gw = await getV4Gateway();

    // Phase 2: fetch BM25 + vector results in parallel
    const [bm25Results, vectorResults] = await Promise.all([
      gw.searchMemories(query, { topK: topK * 4, scope }),
      vectorSearch(query, topK * 4).catch(() => []),
    ]);

    // Normalize scores to [0, 1] before fusion
    const bm25Max = Math.max(1, ...bm25Results.map(r => r.score || 0));
    const vectorMax = Math.max(1, ...vectorResults.map(r => r.score || r.similarity || r.distance || 0));

    // RRF k=60, ranked separately per engine
    const k = 60;
    const fused = new Map();

    for (let i = 0; i < bm25Results.length; i++) {
      const r = bm25Results[i];
      const normScore = (r.score || 0) / bm25Max;  // normalized to [0,1]
      const rrf = 1 / (k + i + 1);
      const w = rrf * normScore * bm25Weight;
      if (fused.has(r.id)) {
        fused.get(r.id).fusionScore += w;
      } else {
        fused.set(r.id, {
          id: r.id,
          text: r.text,
          category: r.category,
          importance: r.importance,
          scope: r.scope,
          bm25Score: Math.round((r.score || 0) * 1000) / 1000,
          vectorScore: null,
          fusionScore: w,
          bm25Rank: i,
          vectorRank: null,
        });
      }
    }

    for (let i = 0; i < vectorResults.length; i++) {
      const r = vectorResults[i];
      const rawVec = r.score ?? r.similarity ?? r.distance ?? 0;
      const normScore = rawVec / vectorMax;
      const rrf = 1 / (k + i + 1);
      const w = rrf * normScore * (1 - bm25Weight);
      if (fused.has(r.id)) {
        fused.get(r.id).fusionScore += w;
        fused.get(r.id).vectorScore = Math.round(rawVec * 1000) / 1000;
        fused.get(r.id).vectorRank = i;
      } else {
        fused.set(r.id, {
          id: r.id,
          text: r.text ?? r.memory?.text,
          category: r.category ?? r.memory?.category,
          importance: r.importance ?? r.memory?.importance,
          scope: r.scope ?? r.memory?.scope,
          bm25Score: null,
          vectorScore: Math.round(rawVec * 1000) / 1000,
          fusionScore: w,
          bm25Rank: null,
          vectorRank: i,
        });
      }
    }

    const results = Array.from(fused.values())
      .sort((a, b) => b.fusionScore - a.fusionScore)
      .slice(0, topK)
      .map(r => ({
        id: r.id,
        text: r.text,
        category: r.category,
        importance: r.importance,
        scope: r.scope,
        bm25Score: r.bm25Score !== null ? Math.round(r.bm25Score * 1000) / 1000 : null,
        vectorScore: r.vectorScore !== null ? Math.round(r.vectorScore * 1000) / 1000 : null,
        fusionScore: Math.round(r.fusionScore * 1000) / 1000,
        engines: [
          r.bm25Rank !== null ? 'bm25' : null,
          r.vectorRank !== null ? 'vector' : null,
        ].filter(Boolean),
      }));

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          v4: true,
          phase: 2,
          engine: 'hybrid_bm25_vector_rrf',
          query,
          topK,
          bm25Weight,
          bm25Count: bm25Results.length,
          vectorCount: vectorResults.length,
          fusionCount: results.length,
          results,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `v4 hybrid search error: ${err.message}` }], isError: true };
  }
});

// ============ Phase 3: Multi-Tenant Team Spaces ============

server.registerTool('memory_v4_create_team', {
  description: '[v4.0 Phase 3] Create a team space for multi-tenant memory isolation.',
  inputSchema: z.object({
    teamId: z.string().describe('Unique team identifier (e.g., team_123)'),
    name: z.string().optional().describe('Team display name'),
    config: z.object({
      rateLimit: z.number().optional().default(100).describe('Max writes per minute'),
      maxMemories: z.number().optional().describe('Max memories per team'),
    }).optional(),
  }),
}, async ({ teamId, name, config = {} }) => {
  try {
    const gw = await getV4Gateway();
    const team = await gw.createTeam(teamId, name, config);
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 3, team, success: true }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `create team error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_list_teams', {
  description: '[v4.0 Phase 3] List all team spaces.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const teams = await gw.listTeams();
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 3, teams }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `list teams error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_get_team', {
  description: '[v4.0 Phase 3] Get team configuration and stats.',
  inputSchema: z.object({
    teamId: z.string().describe('Team identifier'),
  }),
}, async ({ teamId }) => {
  try {
    const gw = await getV4Gateway();
    const team = await gw.getTeam(teamId);
    if (!team) return { content: [{ type: 'text', text: `Team ${teamId} not found` }], isError: true };

    // Get team memory count
    const mems = await gw.getMemories({ scopeType: 'TEAM', scopeId: teamId, limit: 10000 });
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          v4: true,
          phase: 3,
          team,
          memoryCount: mems.length,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `get team error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_delete_team', {
  description: '[v4.0 Phase 3] Delete a team space (memories preserved, scope removed).',
  inputSchema: z.object({
    teamId: z.string().describe('Team identifier'),
  }),
}, async ({ teamId }) => {
  try {
    const gw = await getV4Gateway();
    const deleted = await gw.deleteTeam(teamId);
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 3, teamId, deleted }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `delete team error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_team_store', {
  description: '[v4.0 Phase 3] Store a memory in a team space (automatically creates team if not exists).',
  inputSchema: z.object({
    teamId: z.string().describe('Team identifier'),
    text: z.string().describe('Memory text'),
    category: z.string().optional().default('general'),
    importance: z.number().optional().default(0.5),
    tags: z.array(z.string()).optional(),
  }),
}, async ({ teamId, text, category = 'general', importance = 0.5, tags = [] }) => {
  try {
    const gw = await getV4Gateway();
    // Ensure team exists
    await gw.createTeam(teamId, `Team ${teamId}`);
    const mem = await gw.writeMemory({ text, category, importance, scope: `TEAM:${teamId}`, scopeId: teamId, tags });
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 3, teamId, memory: { id: mem.id, success: true } }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `team store error: ${err.message}` }], isError: true };
  }
});

// ============ Phase 4: Distributed Rate Limiting ============

server.registerTool('memory_v4_rate_limit_status', {
  description: '[v4.0 Phase 4] Check current rate limit status for a scope.',
  inputSchema: z.object({
    scopeType: z.string().optional().default('USER').describe('Scope type: USER, TEAM, AGENT'),
    scopeId: z.string().optional().describe('Scope ID (team_id or agent_id)'),
    operation: z.string().optional().default('write').describe('Operation: write, read, search'),
  }),
}, async ({ scopeType = 'USER', scopeId, operation = 'write' }) => {
  try {
    const gw = await getV4Gateway();
    const key = scopeId ? `${operation}:${scopeType}:${scopeId}` : `${operation}:default`;
    const limits = { write: 30, read: 100, search: 50 };
    const status = gw.getRateLimitStatus(key, limits[operation] || 30, 60);
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 4, rateLimit: status }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `rate limit status error: ${err.message}` }], isError: true };
  }
});

// ============ Phase 7: HTTP REST API (via child process) ============

server.registerTool('memory_v4_http_start', {
  description: '[v4.0 Phase 7] Start the HTTP REST API server on a port. External clients can call REST endpoints without MCP.',
  inputSchema: z.object({
    port: z.number().optional().default(3099).describe('HTTP port (default 3099)'),
    host: z.string().optional().default('0.0.0.0').describe('Bind host (default 0.0.0.0)'),
  }),
}, async ({ port = 3099, host = '0.0.0.0' }) => {
  try {
    const { spawn } = await import('child_process');
    const { join, dirname } = await import('path');
    const { fileURLToPath } = await import('url');
    const __dirname = dirname(fileURLToPath(import.meta.url));
    const serverPath = join(__dirname, 'v4', 'http_server.js');

    // Check if already running
    const existing = process.env.MEMORY_HTTP_PORT;
    if (existing) {
      return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 7, status: 'already_running', port: parseInt(existing) }) }] };
    }

    const child = spawn('node', [serverPath, String(port)], {
      detached: true,
      stdio: 'ignore',
      env: { ...process.env, MEMORY_HTTP_PORT: String(port), MEMORY_HTTP_HOST: host },
    });
    child.unref();

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          v4: true, phase: 7,
          status: 'started',
          port,
          host,
          baseUrl: 'http://' + host + ':' + port + '/api/v4/',
          endpoints: {
            health: 'GET /api/v4/health',
            memories: 'GET|POST /api/v4/memories',
            memoryById: 'GET|DELETE /api/v4/memories/:id',
            search: 'GET /api/v4/search?q=&topK=',
            teams: 'GET|POST /api/v4/teams',
            stats: 'GET /api/v4/stats',
            wal: 'GET /api/v4/wal?limit=&since=',
          },
        }),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `http start error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_http_stop', {
  description: '[v4.0 Phase 7] Stop the HTTP REST API server.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const port = process.env.MEMORY_HTTP_PORT;
    if (port) {
      const { execSync } = await import('child_process');
      execSync('pkill -f "http_server.js.*' + port + '"', { stdio: 'ignore' });
    }
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 7, status: 'stopped' }) }] };
  } catch {
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 7, status: 'stopped' }) }] };
  }
});

// ============ Phase 5: Evidence TTL + Revision Limits ============

server.registerTool('memory_v4_evidence_stats', {
  description: '[v4.0 Phase 5] Get evidence chain statistics including TTL status.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const stats = await gw.getEvidenceStats();
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 5, evidence: stats }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `evidence stats error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_trim_evidence', {
  description: '[v4.0 Phase 5] Manually trigger evidence TTL trim (90-day cutoff). Uses B-tree index — O(log n + k).',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const result = await gw.trimEvidence();
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 5, trim: result }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `trim evidence error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_revision_stats', {
  description: '[v4.0 Phase 5] Get version history statistics.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const stats = await gw.getRevisionStats();
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 5, revisions: stats }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `revision stats error: ${err.message}` }], isError: true };
  }
});

// ============ Phase 6: WAL Operations ============

server.registerTool('memory_v4_wal_status', {
  description: '[v4.0 Phase 6] Get WAL status (total, pending, committed, oldest).',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const status = await gw.getWalStatus();
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 6, wal: status }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `wal status error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_wal_export', {
  description: '[v4.0 Phase 6] Export WAL entries as JSONL for backup/audit.',
  inputSchema: z.object({
    since: z.number().optional().describe('Unix ms timestamp to export from'),
    limit: z.number().optional().default(1000),
  }),
}, async ({ since, limit = 1000 }) => {
  try {
    const gw = await getV4Gateway();
    const entries = await gw.exportWal({ since, limit });
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 6, count: entries.length, entries }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `wal export error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_v4_wal_truncate', {
  description: '[v4.0 Phase 6] Remove non-committed WAL entries (cleanup after crash recovery).',
  inputSchema: z.object({}),
}, async () => {
  try {
    const gw = await getV4Gateway();
    const result = await gw.truncateWal();
    return { content: [{ type: 'text', text: JSON.stringify({ v4: true, phase: 6, truncate: result }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `wal truncate error: ${err.message}` }], isError: true };
  }
});

/**
 * Helper: get vector search results from Ollama.
 * Returns array of {id, score, text, category, ...} or empty array on failure.
 */
async function vectorSearch(query, topK) {
  try {
    const { default: ollama } = await import('ollama');
    const host = process.env.OLLAMA_HOST || 'http://localhost:11434';
    const model = process.env.OLLAMA_EMBED_MODEL || 'nomic-embed-text';

    const embResp = await fetch(`${host}/api/embeddings`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ model, prompt: query }),
      signal: AbortSignal.timeout(10000),
    });
    if (!embResp.ok) return [];
    const { embedding } = await embResp.json();

    // Search LanceDB if available
    const { VectorMemory } = await import('./vector_lancedb.js').catch(() => ({}));
    if (VectorMemory) {
      const vm = new VectorMemory();
      await vm.initialize().catch(() => {});
      const results = await vm.search(embedding, topK).catch(() => []);
      return results.map(r => ({
        id: r.id,
        score: r.score ?? 0,
        text: r.memory?.text ?? r.text ?? '',
        category: r.memory?.category ?? r.category ?? '',
        importance: r.memory?.importance ?? r.importance ?? 0.5,
        scope: r.memory?.scope ?? r.scope ?? 'USER',
      }));
    }
    return [];
  } catch { return []; }
}

// Phase 3: Team-scoped search (strict isolation — does NOT leak to USER/GLOBAL)
server.registerTool('memory_v4_team_search', {
  description: '[v4.0 Phase 3] Search memories within a specific team space ONLY. Strict isolation — team memories never leak to USER scope.',
  inputSchema: z.object({
    teamId: z.string().describe('Team identifier (e.g., dev_team)'),
    query: z.string().describe('Search query'),
    topK: z.number().optional().default(5),
    mode: z.enum(['bm25', 'hybrid']).optional().default('hybrid'),
    bm25Weight: z.number().optional().default(0.5),
  }),
}, async ({ teamId, query, topK = 5, mode = 'hybrid', bm25Weight = 0.5 }) => {
  try {
    const gw = await getV4Gateway();

    if (mode === 'bm25') {
      const results = await gw.searchMemories(query, { topK, scopeType: 'TEAM', scopeId: teamId });
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            v4: true, phase: 3, engine: 'bm25',
            teamId, mode: 'bm25', count: results.length,
            results: results.map(r => ({
              id: r.id, text: r.text, category: r.category,
              importance: r.importance, score: r.score,
            })),
          }, null, 2),
        }],
      };
    }

    // Hybrid: BM25 + Vector
    const [bm25Results, vectorResults] = await Promise.all([
      gw.searchMemories(query, { topK: topK * 4, scopeType: 'TEAM', scopeId: teamId }),
      vectorSearch(query, topK * 4).catch(() => []),
    ]);

    const bm25Max = Math.max(1, ...bm25Results.map(r => r.score || 0));
    const vectorMax = Math.max(1, ...vectorResults.map(r => r.score || 0));
    const k = 60;
    const fused = new Map();

    for (let i = 0; i < bm25Results.length; i++) {
      const r = bm25Results[i];
      const normScore = (r.score || 0) / bm25Max;
      const w = (1 / (k + i + 1)) * normScore * bm25Weight;
      fused.set(r.id, { ...r, fusionScore: w, bm25Rank: i, vectorRank: null, vectorScore: null });
    }

    for (let i = 0; i < vectorResults.length; i++) {
      const r = vectorResults[i];
      const rawScore = r.score || 0;
      const normScore = rawScore / vectorMax;
      const w = (1 / (k + i + 1)) * normScore * (1 - bm25Weight);
      if (fused.has(r.id)) {
        fused.get(r.id).fusionScore += w;
        fused.get(r.id).vectorScore = Math.round(rawScore * 1000) / 1000;
        fused.get(r.id).vectorRank = i;
      } else {
        fused.set(r.id, {
          id: r.id, text: r.text, category: r.category, importance: r.importance,
          scope: `TEAM:${teamId}`, bm25Score: null,
          vectorScore: Math.round(rawScore * 1000) / 1000,
          fusionScore: w, bm25Rank: null, vectorRank: i,
        });
      }
    }

    const results = Array.from(fused.values())
      .sort((a, b) => b.fusionScore - a.fusionScore)
      .slice(0, topK)
      .map(r => ({
        id: r.id, text: r.text, category: r.category, importance: r.importance,
        fusionScore: Math.round(r.fusionScore * 1000) / 1000,
        bm25Score: r.bm25Score,
        vectorScore: r.vectorScore,
      }));

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          v4: true, phase: 3, engine: 'hybrid',
          teamId, mode: 'hybrid', count: results.length, results,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `team search error: ${err.message}` }], isError: true };
  }
});

/**
 * Helper: get vector search results from Ollama.
 * Returns array of {id, score, text, category, ...} or empty array on failure.
 */


// Phase 3: Team-scoped search (strict isolation — does NOT leak to USER/GLOBAL)

// ============ PIN Tools (v3.4) ============

server.registerTool('memory_pin', {
  description: 'Pin (lock) a memory so it is never compressed, deduplicated, or demoted. Use to protect important user facts, identity, or preferences.',
  inputSchema: z.object({
    id: z.string().describe('Memory ID to pin'),
    reason: z.string().optional().describe('Why this memory is pinned (shown in memory_pins)'),
  }),
}, async ({ id, reason }) => {
  try {
    const { pinMemory, getMemory } = await import('./storage.js');
    const mem = getMemory(id);
    if (!mem) return { content: [{ type: 'text', text: `Memory ${id} not found` }], isError: true };
    if (mem.pinned) return { content: [{ type: 'text', text: `Memory ${id} is already pinned` }] };
    pinMemory(id, reason || '');
    return { content: [{ type: 'text', text: JSON.stringify({ success: true, id, reason: reason || '' }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Pin error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_unpin', {
  description: 'Unpin (unlock) a pinned memory. It will become subject to normal tier compression and deduplication again.',
  inputSchema: z.object({
    id: z.string().describe('Memory ID to unpin'),
  }),
}, async ({ id }) => {
  try {
    const { unpinMemory, getMemory } = await import('./storage.js');
    const mem = getMemory(id);
    if (!mem) return { content: [{ type: 'text', text: `Memory ${id} not found` }], isError: true };
    if (!mem.pinned) return { content: [{ type: 'text', text: `Memory ${id} is not pinned` }] };
    unpinMemory(id);
    return { content: [{ type: 'text', text: JSON.stringify({ success: true, id }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Unpin error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_pins', {
  description: 'List all pinned (locked) memories. Pinned memories are never compressed, deduplicated, or demoted to COLD tier.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const { getPinnedMemories } = await import('./storage.js');
    const pins = getPinnedMemories();
    return { content: [{ type: 'text', text: JSON.stringify({ count: pins.length, pins }, null, 2) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
});

// ============ Advanced Tools (NEW in v1.1) ============


server.registerTool('memory_export', {
  description: 'Export memories to JSON, Markdown, or CSV format. Supports filtering by category and minimum importance.',
  inputSchema: z.object({
    format: z.enum(['json', 'markdown', 'csv']).optional().default('json').describe('Export format'),
    output: z.string().optional().describe('Output file path'),
    category: z.string().optional().describe('Filter by category'),
    minImportance: z.number().optional().describe('Minimum importance threshold'),
  }),
}, async (args) => {
  try {
    return await exportMemories(args);
  } catch (err) {
    structuredLog.error(`Export failed: ${err.message}`);
    return { content: [{ type: 'text', text: `Export error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_dedup', {
  description: 'Detect and merge duplicate memories using hash + Levenshtein similarity.',
  inputSchema: z.object({
    threshold: z.number().optional().default(0.85).describe('Similarity threshold 0-1'),
    dryRun: z.boolean().optional().default(true).describe('If true, only preview changes'),
  }),
}, async ({ threshold = 0.85, dryRun = true }) => {
  try {
    return await dedupMemories({ threshold, dryRun });
  } catch (err) {
    structuredLog.error(`Dedup failed: ${err.message}`);
    return { content: [{ type: 'text', text: `Dedup error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_decay', {
  description: 'Apply time-based importance decay based on memory category half-life rules.',
  inputSchema: z.object({
    apply: z.boolean().optional().default(false).describe('If true, apply decay to memories'),
  }),
}, async ({ apply = false }) => {
  try {
    return await decayMemories({ apply });
  } catch (err) {
    structuredLog.error(`Decay failed: ${err.message}`);
    return { content: [{ type: 'text', text: `Decay error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_qa', {
  description: 'Answer questions based on relevant memories using RAG.',
  inputSchema: z.object({
    question: z.string().describe('Question to answer based on memories'),
  }),
}, async ({ question }) => {
  try {
    return await askQuestion({ question });
  } catch (err) {
    structuredLog.error(`QA failed: ${err.message}`);
    return { content: [{ type: 'text', text: `QA error: ${err.message}` }], isError: true };
  }
});

// ============ Preference Slots (v1.2) ============

// ============ Preference (5→1) ============
// memory_preference: unified preference management (action=get|set|update|merge|delete|reset|stats|explain|infer)
server.registerTool('memory_preference', {
  description: 'Unified preference management. Actions: get/set/update/merge/delete/reset/stats/explain/infer.',
  inputSchema: z.object({
    action: z.enum(['get', 'set', 'update', 'merge', 'delete', 'reset', 'stats', 'explain', 'infer']).describe('Action'),
    key: z.string().optional().describe('Slot key (for get/set/update/delete/explain)'),
    value: z.unknown().optional().describe('Slot value (for set/update)'),
    confidence: z.number().optional().describe('Confidence 0-1 (for set/update)'),
    source: z.enum(['explicit', 'inferred', 'historical']).optional().describe('Source (for set/update)'),
    slots: z.record(z.string(), z.unknown()).optional().describe('Key-value map (for merge)'),
    messageCount: z.number().optional().default(20).describe('Message count (for infer)'),
  }),
}, async ({ action, key, value, confidence = 0.9, source = 'explicit', slots, messageCount = 20 }) => {
  try {
    if (action === 'get') {
      return memoryPreferenceSlotsTool({ action: 'get', key });
    } else if (action === 'set' || action === 'update') {
      return memoryPreferenceSetTool({ key, value, confidence, source });
    } else if (action === 'merge') {
      return memoryPreferenceSlotsTool({ action: 'merge', slots });
    } else if (action === 'delete') {
      return memoryPreferenceSlotsTool({ action: 'delete', key });
    } else if (action === 'reset') {
      return memoryPreferenceSlotsTool({ action: 'reset' });
    } else if (action === 'stats') {
      return memoryPreferenceSlotsTool({ action: 'stats' });
    } else if (action === 'explain') {
      return memoryPreferenceExplainTool({ key });
    } else if (action === 'infer') {
      return memoryPreferenceInferTool({ messageCount });
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Preference error [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers (delegate to unified memory_preference)

// ============ Semantic Versioning (Feature #11) ============

// ============ Version (3→1) ============
// memory_version: action=list|diff|restore
server.registerTool('memory_version', {
  description: 'Version control for memories. Actions: list (history), diff (compare versions), restore (rollback).',
  inputSchema: z.object({
    action: z.enum(['list', 'diff', 'restore']).describe('Action'),
    memoryId: z.string().optional().describe('Memory ID (required for diff/restore)'),
    versionId: z.string().optional().describe('Version ID (for diff/restore)'),
    versionId1: z.string().optional().describe('First version ID (for diff)'),
    versionId2: z.string().optional().describe('Second version ID (for diff)'),
    limit: z.number().optional().default(10).describe('Max versions (for list)'),
    offset: z.number().optional().default(0).describe('Offset (for list)'),
    changeType: z.enum(['create', 'update', 'delete', 'rollback']).optional().describe('Filter (for list)'),
    preview: z.boolean().optional().default(false).describe('Preview without restore (for restore)'),
  }),
}, async ({ action, memoryId, versionId, versionId1, versionId2, limit, offset, changeType, preview }) => {
  try {
    if (action === 'list') {
      return memoryVersionListTool({ memoryId, limit, offset, changeType });
    } else if (action === 'diff') {
      return memoryVersionDiffTool({ memoryId, versionId1, versionId2 });
    } else if (action === 'restore') {
      return memoryVersionRestoreTool({ memoryId, versionId, preview });
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Version error [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers

// ============ Lesson System (v1.2) ============

server.registerTool('memory_lessons', {
  description: 'Lesson management: extract durable high-level principles from recurring memory recall patterns. Supports extract, recall, list, stats, delete.',
  inputSchema: z.object({
    action: z.enum(['extract', 'recall', 'list', 'stats', 'delete', 'touch', 'candidates']).describe('Action to perform'),
    memory_id: z.string().optional().describe('Source memory ID (for extract)'),
    title: z.string().optional().describe('Lesson title (for extract)'),
    body: z.string().optional().describe('Lesson body (for extract)'),
    tags: z.array(z.string()).optional().describe('Tags (for extract)'),
    query: z.string().optional().describe('Search query (for recall)'),
    lesson_id: z.string().optional().describe('Lesson ID (for delete/touch)'),
    limit: z.number().optional().describe('Max results (for list/recall)'),
    tag: z.string().optional().describe('Filter by tag (for list)'),
  }),
}, async (args) => {
  try {
    return memoryLessonsTool(args);
  } catch (err) {
    structuredLog.error(`Lesson system error: ${err.message}`);
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
});

// ============ Profile Aggregator (v3.9, inspired by SuperMemory) ============
// memory_profile: Get user profile with static/dynamic separation
// One call replaces multiple memory searches
server.registerTool('memory_profile', {
  description: 'Get user profile with static/dynamic separation. ' +
    'static = stable long-term facts + preferences. ' +
    'dynamic = recent context + in-progress work. ' +
    'Inspired by SuperMemory profile abstraction.',
  inputSchema: z.object({
    scope: z.string().optional().default('user').describe('Scope: agent, user, team, or global'),
    container_tag: z.string().optional().describe('Project/lane tag to scope profile'),
    entity_filter: z.string().optional().describe('Focus on specific entity'),
    static_days: z.number().optional().default(30).describe('Days without access to mark as static'),
    limit: z.number().optional().default(100).describe('Max memories to analyze'),
  }),
}, async ({ scope, container_tag, entity_filter, static_days, limit }) => {
  try {
    const profile = await getProfile({
      scope: scope || 'user',
      containerTag: container_tag,
      entityFilter: entity_filter,
      staticDays: static_days,
      limit: limit || 100,
    });
    return { content: [{ type: 'text', text: JSON.stringify(profile, null, 2) }] };
  } catch (err) {
    structuredLog.error(`memory_profile error: ${err.message}`);
    return { content: [{ type: 'text', text: `Error: ${err.message}` }], isError: true };
  }
});

// ============ AutoStore (v1.2) ============

server.registerTool('memory_autostore', {
  description: 'Auto-extract important information from conversation text and store as memories. Detects sensitive info and filters appropriately.',
  inputSchema: z.object({
    action: z.enum(['extract', 'stats']).describe('Action to perform'),
    text: z.string().optional().describe('Conversation text to extract from (for extract action)'),
  }),
}, async ({ action, text }) => {
  try {
    if (action === 'extract') {
      if (!text) {
        return { content: [{ type: 'text', text: 'Error: text is required for extract action' }], isError: true };
      }
      const extracted = extractImportantInfo(text);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            extracted: extracted.length,
            items: extracted.map(e => ({ text: e.text, category: e.category, source: e.source }))
          }, null, 2)
        }]
      };
    } else if (action === 'stats') {
      return {
        content: [{ type: 'text', text: JSON.stringify({ message: 'Autostore stats: extraction is rule-based, call extract action to process text' }, null, 2) }]
      };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Autostore error: ${err.message}`);
    return { content: [{ type: 'text', text: `Autostore error: ${err.message}` }], isError: true };
  }
});

// ============ Concurrent Search (v1.2) ============

server.registerTool('memory_concurrent_search', {
  description: 'Parallel BM25 + Vector + QMD hybrid search with multi-query support and timeout control.',
  inputSchema: z.object({
    action: z.enum(['search', 'multi', 'stats']).describe('Action to perform'),
    query: z.string().optional().describe('Search query (for search action)'),
    queries: z.array(z.string()).optional().describe('Multiple queries for parallel search (for search action)'),
    topK: z.number().optional().default(5).describe('Number of results to return'),
    text: z.string().optional().describe('Text to search (for multi action)'),
    tags: z.array(z.string()).optional().describe('Tags to filter by (for multi action)'),
    category: z.string().optional().describe('Category to filter by (for multi action)'),
  }),
}, async ({ action, query, queries, topK = 5, text, tags, category }) => {
  try {
    const searcher = new ConcurrentSearch();
    if (action === 'search') {
      const qList = queries || (query ? [query] : []);
      if (qList.length === 0) {
        return { content: [{ type: 'text', text: 'Error: query or queries is required' }], isError: true };
      }
      const results = await searcher.searchMultiple(qList, topK);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            count: results.length,
            results: results.slice(0, topK).map(r => ({
              id: r.memory?.id,
              text: (r.memory?.text || '').slice(0, 100),
              category: r.memory?.category,
              score: Math.round(r.score * 1000) / 1000,
              match_type: r.match_type
            }))
          }, null, 2)
        }]
      };
    } else if (action === 'multi') {
      if (!text) {
        return { content: [{ type: 'text', text: 'Error: text is required for multi action' }], isError: true };
      }
      const results = await searcher.multiSearch({ text, tags: tags || [], category }, topK);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            count: results.length,
            results: results.map(r => ({
              id: r.memory?.id,
              text: (r.memory?.text || '').slice(0, 100),
              score: Math.round(r.score * 1000) / 1000
            }))
          }, null, 2)
        }]
      };
    } else if (action === 'stats') {
      return { content: [{ type: 'text', text: JSON.stringify(searcher.getStats(), null, 2) }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Concurrent search error: ${err.message}`);
    return { content: [{ type: 'text', text: `Concurrent search error: ${err.message}` }], isError: true };
  }
});

// ============ Predict (v1.2) ============


// ============ Recommend (v1.2) ============

server.registerTool('memory_recommend', {
  description: 'Smart memory recommendations based on vector similarity, co-occurrence, and tag correlation.',
  inputSchema: z.object({
    action: z.enum(['recommend', 'reason', 'hot', 'related']).describe('Action to perform'),
    context: z.string().optional().describe('Query/context for recommendation (for recommend action)'),
    id: z.string().optional().describe('Memory ID (for related action)'),
    k: z.number().optional().default(5).describe('Number of recommendations to return'),
    json: z.boolean().optional().default(false).describe('Return JSON format'),
  }),
}, async ({ action, context, id, k = 5, json = false }) => {
  try {
    if (action === 'recommend') {
      if (!context) {
        return { content: [{ type: 'text', text: 'Error: context is required for recommend action' }], isError: true };
      }
      const result = await cmdRecommend('recommend', { query: context, k: String(k), json });
      return { content: [{ type: 'text', text: result.type === 'json' ? JSON.stringify(result.data, null, 2) : result.text }] };
    } else if (action === 'reason') {
      return { content: [{ type: 'text', text: JSON.stringify({ explanation: 'Recommendations use vector similarity (50%), tag correlation (30%), and co-occurrence (20%) combined with importance weighting (30%)' }) }] };
    } else if (action === 'hot') {
      const result = await cmdRecommend('hot', { k: String(k), json });
      return { content: [{ type: 'text', text: result.type === 'json' ? JSON.stringify(result.data, null, 2) : result.text }] };
    } else if (action === 'related') {
      if (!id) {
        return { content: [{ type: 'text', text: 'Error: id is required for related action' }], isError: true };
      }
      const result = await cmdRecommend('related', { id, k: String(k), json });
      return { content: [{ type: 'text', text: result.type === 'json' ? JSON.stringify(result.data, null, 2) : result.text }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Recommend error: ${err.message}`);
    return { content: [{ type: 'text', text: `Recommend error: ${err.message}` }], isError: true };
  }
});

// ============ Inference (v1.2) ============

server.registerTool('memory_inference', {
  description: 'Joint inference combining vector search with ontology graph path expansion for enhanced memory retrieval.',
  inputSchema: z.object({
    action: z.enum(['infer', 'context', 'stats']).describe('Action to perform'),
    query: z.string().optional().describe('Query for inference (for infer action)'),
    entityId: z.string().optional().describe('Entity ID (for context action)'),
    limit: z.number().optional().default(10).describe('Max results (for infer action)'),
    depth: z.number().optional().default(2).describe('Graph traversal depth (for infer action)'),
    json: z.boolean().optional().default(false).describe('Return JSON format'),
  }),
}, async ({ action, query, entityId, limit = 10, depth = 2, json = false }) => {
  try {
    const inference = new MemoryInference();
    if (action === 'infer') {
      if (!query) {
        return { content: [{ type: 'text', text: 'Error: query is required for infer action' }], isError: true };
      }
      const result = await inference.inferRelated(query, limit, depth);
      return { content: [{ type: 'text', text: json ? JSON.stringify(result, null, 2) : JSON.stringify(result.merged?.slice(0, 5) || [], null, 2) }] };
    } else if (action === 'context') {
      if (!entityId) {
        return { content: [{ type: 'text', text: 'Error: entityId is required for context action' }], isError: true };
      }
      const chain = inference.getContextChain(entityId);
      return { content: [{ type: 'text', text: json ? JSON.stringify(chain, null, 2) : JSON.stringify(chain.slice(0, 10), null, 2) }] };
    } else if (action === 'stats') {
      const stats = inference.getStats();
      return { content: [{ type: 'text', text: JSON.stringify(stats, null, 2) }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Inference error: ${err.message}`);
    return { content: [{ type: 'text', text: `Inference error: ${err.message}` }], isError: true };
  }
});

// ============ Summary (v1.2) ============

server.registerTool('memory_summary', {
  description: 'Generate memory summaries at different granularities using LLM or rule-based extraction.',
  inputSchema: z.object({
    action: z.enum(['summarize', 'stats']).describe('Action to perform'),
    text: z.string().optional().describe('Text to summarize (for summarize action)'),
    memoryId: z.string().optional().describe('Memory ID to summarize (for summarize action)'),
    style: z.enum(['short', 'medium', 'long']).optional().default('medium').describe('Summary style'),
  }),
}, async ({ action, text, memoryId, style = 'medium' }) => {
  try {
    const summarizer = new MemorySummarizer();
    if (action === 'summarize') {
      if (!text && !memoryId) {
        return { content: [{ type: 'text', text: 'Error: text or memoryId is required' }], isError: true };
      }
      let summary;
      if (memoryId) {
        summary = await summarizer.summarizeMemory(memoryId, style);
      } else {
        summary = await summarizer.generateSummary(text, style);
      }
      return { content: [{ type: 'text', text: JSON.stringify({ summary, style }, null, 2) }] };
    } else if (action === 'stats') {
      const cache = summarizer.cache || {};
      return { content: [{ type: 'text', text: JSON.stringify({ cached_summaries: Object.keys(cache.summaries || {}).length }, null, 2) }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Summary error: ${err.message}`);
    return { content: [{ type: 'text', text: `Summary error: ${err.message}` }], isError: true };
  }
});

// ============ Feedback Learner (v1.2) ============


// ============ QMD Search (v1.2) ============

// ============ QMD (4→1) ============
// memory_qmd: unified QMD file search (action=search|get|vsearch|list|status)
server.registerTool('memory_qmd', {
  description: 'QMD local file search. Actions: search/get/vsearch/list/status.',
  inputSchema: z.object({
    action: z.enum(['search', 'get', 'vsearch', 'list', 'status']).describe('Action'),
    query: z.string().optional().describe('Search query (for search/vsearch)'),
    path: z.string().optional().describe('File path (for get)'),
    maxLines: z.number().optional().default(100).describe('Max lines (for get)'),
    offset: z.number().optional().default(0).describe('Offset (for get)'),
    topK: z.number().optional().default(5).describe('Results count (for search/vsearch)'),
    mode: z.enum(['bm25', 'vector', 'hybrid', 'auto']).optional().default('hybrid').describe('Search mode (for search)'),
    pattern: z.string().optional().default('**/*.md').describe('Glob pattern (for list)'),
    limit: z.number().optional().default(20).describe('Max files (for list)'),
  }),
}, async ({ action, query, path, maxLines=100, offset=0, topK=5, mode='hybrid', pattern='**/*.md', limit=20 }) => {
  try {
    const { qmdSearch, qmdGet, qmdVSearch, qmdListFiles, getQMDStatus } = await import('./tools/qmd_search.js');
    if (action === 'search') {
      if (!query) return { content: [{ type: 'text', text: 'Error: query required' }], isError: true };
      const results = await qmdSearch(query, { topK, mode });
      return { content: [{ type: 'text', text: JSON.stringify({ count: results.length, query, mode, results: results.map(r => ({ id: r.id, text: r.text, category: r.category, score: Math.round(r.score*1000)/1000, match_mode: r.mode })) }, null, 2) }] };
    } else if (action === 'get') {
      const result = await qmdGet(path, { maxLines, offset });
      if (result.error) return { content: [{ type: 'text', text: `Error: ${result.error}` }], isError: true };
      return { content: [{ type: 'text', text: JSON.stringify({ path: result.path, content: result.content, lines: result.lines, truncated: result.truncated, source: 'qmd' }, null, 2) }] };
    } else if (action === 'vsearch') {
      if (!query) return { content: [{ type: 'text', text: 'Error: query required' }], isError: true };
      const results = await qmdVSearch(query, { topK });
      if (results.error) return { content: [{ type: 'text', text: `Error: ${results.error}` }], isError: true };
      return { content: [{ type: 'text', text: JSON.stringify({ count: results.length, query, mode: 'vector', results: results.map(r => ({ id: r.id, path: r.path, title: r.title, score: Math.round(r.score*1000)/1000, snippet: r.snippet })) }, null, 2) }] };
    } else if (action === 'list') {
      const result = await qmdListFiles(pattern, limit);
      if (result.error) return { content: [{ type: 'text', text: `Error: ${result.error}` }], isError: true };
      return { content: [{ type: 'text', text: JSON.stringify({ count: Array.isArray(result.files) ? result.files.length : 0, files: result.files || [], source: 'qmd' }, null, 2) }] };
    } else if (action === 'status') {
      return { content: [{ type: 'text', text: JSON.stringify(await getQMDStatus(), null, 2) }] };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `QMD [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers (use memory_qmd instead)

// ============ Templates (v1.2) ============

server.registerTool('memory_templates', {
  description: 'Memory template system for structured memory creation (project, meeting, decision, preference, task, contact, learning).',
  inputSchema: z.object({
    action: z.enum(['list', 'generate', 'get']).describe('Action to perform'),
    command: z.string().optional().describe('Template type (for generate action)'),
    templateType: z.string().optional().describe('Template type to get (for get action)'),
    data: z.record(z.string(), z.unknown()).optional().describe('Template data (for generate action)'),
  }),
}, async ({ action, command, templateType, data }) => {
  try {
    if (action === 'list') {
      const result = cmdTemplates('list', { json: true });
      return { content: [{ type: 'text', text: JSON.stringify(result.data, null, 2) }] };
    } else if (action === 'get') {
      if (!templateType) {
        return { content: [{ type: 'text', text: 'Error: templateType is required for get action' }], isError: true };
      }
      const result = cmdTemplates('get', { type: templateType, json: true });
      return { content: [{ type: 'text', text: JSON.stringify(result.data || result.error, null, 2) }] };
    } else if (action === 'generate') {
      if (!command) {
        return { content: [{ type: 'text', text: 'Error: command (template type) is required for generate action' }], isError: true };
      }
      const result = cmdTemplates('fill', { type: command, data: data ? JSON.stringify(data) : '{}', json: true });
      return { content: [{ type: 'text', text: result.type === 'json' ? JSON.stringify(result.data, null, 2) : result.text }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Templates error: ${err.message}`);
    return { content: [{ type: 'text', text: `Templates error: ${err.message}` }], isError: true };
  }
});

// ============ Stats & Health ============

server.registerTool('memory_stats', {
  description: 'Get memory system statistics: count, categories, tags, access patterns.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const memories = await getAllMemories();
    const categories = {};
    const tagCounts = {};
    for (const m of memories) {
      categories[m.category] = (categories[m.category] || 0) + 1;
      for (const tag of m.tags || []) {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      }
    }

    // Category distribution (mapped to standard categories)
    const categoryMap = { fact: 0, decision: 0, preference: 0, reflection: 0, other: 0 };
    for (const m of memories) {
      const cat = m.category || 'other';
      if (cat === 'fact' || cat === 'entity') categoryMap.fact++;
      else if (cat === 'decision') categoryMap.decision++;
      else if (cat === 'preference') categoryMap.preference++;
      else if (cat === 'reflection') categoryMap.reflection++;
      else categoryMap.other++;
    }

    // Quality distribution (by importance score)
    const qualityMap = { high: 0, medium: 0, low: 0 };
    for (const m of memories) {
      const imp = m.importance || 0.5;
      if (imp > 0.6) qualityMap.high++;
      else if (imp >= 0.3) qualityMap.medium++;
      else qualityMap.low++;
    }

    // Tier distribution and size by tier
    const tierMap = { HOT: 0, WARM: 0, COLD: 0 };
    const sizeByTier = { HOT: 0, WARM: 0, COLD: 0 };
    const DAY_MS = 86400000;
    const now = Date.now();
    for (const m of memories) {
      const raw = m.timestamp || m.created_at || m.createdAt || now;
      const ts = typeof raw === 'string' ? new Date(raw).getTime() : raw;
      const ageDays = (now - ts) / DAY_MS;
      let tier;
      if (ageDays <= 7) tier = 'HOT';
      else if (ageDays <= 30) tier = 'WARM';
      else tier = 'COLD';
      tierMap[tier]++;
      const size = Buffer.byteLength(JSON.stringify(m), 'utf8');
      sizeByTier[tier] += size;
    }

    // Scope distribution
    const scopeMap = { USER: 0, TEAM: 0, AGENT: 0, GLOBAL: 0 };
    for (const m of memories) {
      const scope = (m.scope || 'GLOBAL').toUpperCase();
      if (scope in scopeMap) scopeMap[scope]++;
      else scopeMap.GLOBAL++;
    }

    // Read storage version from package.json
    let storageVersion = '2.0.0';
    try {
      const { readFileSync } = await import('fs');
      const pkgPath = new URL('../package.json', import.meta.url);
      const pkg = JSON.parse(readFileSync(pkgPath, 'utf8'));
      storageVersion = pkg.version || '2.0.0';
    } catch { /* use default */ }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          total: memories.length,
          categories,
          topTags: Object.entries(tagCounts).sort((a, b) => b[1] - a[1]).slice(0, 10).map(([tag, count]) => ({ tag, count })),
          // Enhanced fields (v2.0)
          category_distribution: categoryMap,
          quality_distribution: qualityMap,
          tier_distribution: tierMap,
          size_by_tier: sizeByTier,
          scope_distribution: scopeMap,
          pin_count: memories.filter(m => m.pinned).length,
          memory_count: memories.length,
          storage_version: storageVersion,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Stats error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_health', {
  description: 'Health check for the MCP server and its dependencies.',
  inputSchema: z.object({}),
}, async () => {
  try {
    const memories = await getAllMemories();
    let ollamaOk = false;
    try {
      if (config.ollamaUrl) {
        const res = await fetch(`${config.ollamaUrl}/api/tags`);
        ollamaOk = res.ok;
      }
    } catch { ollamaOk = false; }

    // WAL integrity check
    const walChecks = { status: 'ok', walRecordCount: 0, actualOpsCount: 0, discrepancy: 0, withinTolerance: true };
    try {
      const walFiles = listWalFiles();
      let totalWalRecords = 0;
      for (const wf of walFiles) {
        try {
          const content = await import('fs').then(fs => fs.readFileSync(new URL(`../wal/${wf}`, import.meta.url), 'utf8'));
          totalWalRecords += content.trim().split('\n').filter(Boolean).length;
        } catch { /* skip unreadable files */ }
      }
      walChecks.walRecordCount = totalWalRecords;
      walChecks.actualOpsCount = memories.length;
      walChecks.discrepancy = Math.abs(totalWalRecords - memories.length);
      walChecks.withinTolerance = memories.length === 0
        ? totalWalRecords === 0
        : (walChecks.discrepancy / memories.length) <= 0.05;
    } catch { walChecks.status = 'unknown'; }

    // Vector cache completeness (memories with embeddings)
    let vectorCount = 0;
    for (const m of memories) {
      // Accept both base64 string (from JSON sync) and number array (direct format)
      if (m.embedding && ((Array.isArray(m.embedding) && m.embedding.length > 0) || (typeof m.embedding === 'string' && m.embedding.length > 20))) {
        vectorCount++;
      }
    }
    const vectorCompleteRate = memories.length > 0 ? Math.round((vectorCount / memories.length) * 1000) / 10 : 100;
    const vectorStatus = vectorCompleteRate >= 95 ? 'ok' : (vectorCompleteRate >= 50 ? 'degraded' : 'critical');

    // Tier distribution reasonableness
    const DAY_MS = 86400000;
    const now = Date.now();
    const tierCounts = { HOT: 0, WARM: 0, COLD: 0 };
    for (const m of memories) {
      const raw = m.timestamp || m.created_at || m.createdAt || now;
      const ts = typeof raw === 'string' ? new Date(raw).getTime() : raw;
      const ageDays = (now - ts) / DAY_MS;
      if (ageDays <= 7) tierCounts.HOT++;
      else if (ageDays <= 30) tierCounts.WARM++;
      else tierCounts.COLD++;
    }
    const totalMemories = memories.length || 1;
    const coldRatio = tierCounts.COLD / totalMemories;
    const hotRatio = tierCounts.HOT / totalMemories;
    const tierWarnings = [];
    if (coldRatio > 0.8) tierWarnings.push({ level: 'warning', message: `COLD tier占比${Math.round(coldRatio * 100)}% > 80%,分级可能有问题` });
    if (hotRatio > 0.8) tierWarnings.push({ level: 'warning', message: `HOT tier占比${Math.round(hotRatio * 100)}% > 80%,没有正常衰减` });

    // Long-time-no-access memories (>30 days)
    const staleMemories = [];
    const thirtyDaysAgo = now - 30 * DAY_MS;
    for (const m of memories) {
      const lastAcc = m.last_access || m.lastAccess || m.timestamp || m.created_at || m.createdAt || now;
      const accTs = typeof lastAcc === 'string' ? new Date(lastAcc).getTime() : lastAcc;
      if (accTs < thirtyDaysAgo) {
        staleMemories.push({ id: m.id, last_access: new Date(accTs).toISOString() });
        if (staleMemories.length >= 10) break;
      }
    }

    // Corrupted memory detection
    const corruptedMemories = [];
    const requiredFields = ['id', 'text', 'category'];
    for (const m of memories) {
      let isCorrupted = false;
      try {
        // JSON parse check (already parsed by getAllMemories, so we check structural validity)
        if (!m.id || typeof m.text !== 'string' || !m.category) {
          isCorrupted = true;
        }
        // Check for essential numeric fields being valid
        if (m.importance !== undefined && (typeof m.importance !== 'number' || m.importance < 0 || m.importance > 1)) {
          isCorrupted = true;
        }
      } catch {
        isCorrupted = true;
      }
      if (isCorrupted) {
        corruptedMemories.push({ id: m.id || 'unknown', reason: 'missing required fields or invalid structure' });
      }
    }

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          status: 'ok',
          version: '1.1.0',
          memoryCount: memories.length,
          // Pluggable engine config
          vector_engine: config.vectorEngine,
          embed_provider: config.embedProvider,
          llm_provider: config.llmProvider,
          embed_url: config.ollamaUrl,
          embed_model: config.embedModel,
          llm_url: config.llmUrl,
          llm_model: config.llmModel,
          ollama: ollamaOk ? 'connected' : 'disconnected',
          // Enhanced health checks (v2.0)
          wal_integrity: walChecks,
          vector_cache_complete_rate: `${vectorCompleteRate}%`,
          vector_cache_status: vectorStatus,
          tier_distribution: {
            HOT: tierCounts.HOT,
            WARM: tierCounts.WARM,
            COLD: tierCounts.COLD,
            warnings: tierWarnings,
          },
          stale_memories: staleMemories,
          corrupted_memories: corruptedMemories,
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Health error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_metrics', {
  description: 'View operational metrics: search latency, store counts, error rates.',
  inputSchema: z.object({}),
  handler: async () => {
    const m = metrics.collect();
    const trace = getTraceExport();
    return { content: [{ type: 'text', text: JSON.stringify({ metrics: m, trace }, null, 2) }] };
  }
});

// P1-5: Token Budget Tool (enhanced)
server.registerTool('memory_budget', {
  description: 'Token budget management for memory types. Actions: status (view all budgets), allocate (get allocation for type+priority), compress (compress content if over budget), recalculate (redistribute budgets).',
  inputSchema: z.object({
    action: z.enum(['status', 'allocate', 'compress', 'recalculate']).describe('Action to perform'),
    memoryType: z.string().optional().describe('Memory type: transcript, memory, episode, working, system'),
    priority: z.string().optional().default('medium').describe('Priority: critical, high, medium, low'),
    content: z.string().optional().describe('Content to compress (for compress action)'),
    maxBudget: z.number().optional().describe('Total budget in tokens (for status action, default 8000)'),
  }),
}, async ({ action, memoryType, priority = 'medium', content, maxBudget }) => {
  try {
    if (action === 'status') {
      // Allow setting maxBudget on status call to reconfigure
      const allocator = getAllocator(maxBudget);
      const status = allocator.getStatus();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            action: 'status',
            ...status,
          }, null, 2),
        }],
      };
    } else if (action === 'allocate') {
      if (!memoryType) {
        return { content: [{ type: 'text', text: 'Error: memoryType is required for allocate action' }], isError: true };
      }
      const allocator = getAllocator(maxBudget);
      const tokens = allocator.allocate(memoryType, priority);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            action: 'allocate',
            memoryType,
            priority,
            allocatedTokens: tokens,
            remainingTokens: allocator.getRemaining(memoryType),
          }, null, 2),
        }],
      };
    } else if (action === 'compress') {
      if (!memoryType || content === undefined) {
        return { content: [{ type: 'text', text: 'Error: memoryType and content are required for compress action' }], isError: true };
      }
      const result = compressIfNeeded(memoryType, content);
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            action: 'compress',
            memoryType,
            originalLength: content.length,
            compressed: result.compressed,
            savedTokens: result.savedTokens,
            ratio: Math.round(result.ratio * 100) / 100,
            content: result.content,
          }, null, 2),
        }],
      };
    } else if (action === 'recalculate') {
      const result = recalculateBudgets();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            action: 'recalculate',
            ...result,
          }, null, 2),
        }],
      };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: `memory_budget error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_trace', {
  description: 'Export recent trace spans for debugging.',
  inputSchema: z.object({ clear: z.boolean().default(false) }),
  handler: async ({ clear }) => {
    const t = getTraceExport();
    if (clear) clearTrace();
    return { content: [{ type: 'text', text: JSON.stringify(t, null, 2) }] };
  }
});

// ============ Extended Search & Processing ============

server.registerTool('memory_noise', {
  description: 'Manage noise filtering and quality scoring for memories. Learn noise patterns, check if text should be stored, and get quality scores.',
  inputSchema: z.object({
    action: z.enum(['should_store', 'quality', 'learn', 'stats', 'clear']).describe('Action: should_store=text to check, quality=score memories, learn=add noise pattern, stats=noise count, clear=reset learned'),
    text: z.string().optional().describe('Text content for should_store or learn actions'),
    memories: z.array(z.object({ id: z.string(), content: z.string() })).optional().describe('Memories to score (for quality action)'),
  }),
}, async ({ action, text, memories }) => {
  try {
    if (action === 'should_store') {
      const result = shouldStore(text || '', {});
      return { content: [{ type: 'text', text: JSON.stringify({ should_store: result }) }] };
    }
    if (action === 'quality') {
      const scores = (memories || []).map(m => ({ id: m.id, score: qualityScore(m) }));
      return { content: [{ type: 'text', text: JSON.stringify({ scores }) }] };
    }
    if (action === 'learn') {
      learnNoisePattern(text || '');
      return { content: [{ type: 'text', text: 'Noise pattern learned' }] };
    }
    if (action === 'stats') {
      return { content: [{ type: 'text', text: JSON.stringify({ noise_count: getNoiseCount() }) }] };
    }
    if (action === 'clear') {
      const { clearLearnedNoise } = await import('./noise.js');
      clearLearnedNoise();
      return { content: [{ type: 'text', text: 'Learned noise patterns cleared' }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: `Noise error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_intent', {
  description: 'Route a search query to determine intent type (FACT, PREFERENCE, RECENT, PROJECT, etc.). Returns null to skip retrieval for non-retrieval queries.',
  inputSchema: z.object({
    query: z.string().describe('The search query to classify'),
  }),
}, async ({ query }) => {
  try {
    const intent = routeSearch(query);
    const type = intent?.type || 'UNKNOWN';
    const skip = intent === null;
    return { content: [{ type: 'text', text: JSON.stringify({ intent_type: type, skip_retrieval: skip, intent }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Intent error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_extract', {
  description: 'Extract structured memories from raw text using LLM. Supports batch extraction with progress callbacks.',
  inputSchema: z.object({
    texts: z.array(z.string()).describe('Texts to extract memories from'),
    batch: z.boolean().default(false).describe('Use batch extraction with progress'),
    onProgress: z.boolean().default(false).describe('Report progress per text'),
  }),
}, async ({ texts, batch, onProgress }) => {
  try {
    const { llmCall } = await import('./config.js');
    if (batch) {
      const results = await batchExtract(texts, async (p) => { if (onProgress) process.stderr.write(`[extract] ${p}\n`); }, llmCall);
      return { content: [{ type: 'text', text: JSON.stringify(results) }] };
    } else {
      const results = await Promise.all(texts.map(t => extractMemories(t, llmCall)));
      return { content: [{ type: 'text', text: JSON.stringify(results) }] };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Extract error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_reflection', {
  description: 'Self-improvement system: track learnings, errors, and patterns. Store lessons from operations and retrieve them.',
  inputSchema: z.object({
    action: z.enum(['learn', 'error', 'get', 'stats']).describe('Action: learn=add learning, error=log error, get=retrieve all, stats=summary'),
    text: z.string().optional().describe('Content for learn or error'),
    category: z.string().default('general').describe('Category for learn action'),
    errorType: z.string().default('unknown').describe('Error type for error action'),
  }),
}, async ({ action, text, category, errorType }) => {
  try {
    if (action === 'learn') {
      addLearning(text || '', category || 'general');
      return { content: [{ type: 'text', text: 'Learning added' }] };
    }
    if (action === 'error') {
      addError(text || '', errorType || 'unknown');
      return { content: [{ type: 'text', text: 'Error logged' }] };
    }
    if (action === 'get') {
      return { content: [{ type: 'text', text: JSON.stringify({ learnings: getLearnings(), errors: getErrors() }) }] };
    }
    if (action === 'stats') {
      return { content: [{ type: 'text', text: JSON.stringify(getStats()) }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: `Reflection error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_wal', {
  description: 'Write-Ahead Log operations for crash recovery. Initialize WAL, flush pending ops, or list WAL files.',
  inputSchema: z.object({
    action: z.enum(['init', 'flush', 'list']).describe('Action: init=create new WAL, flush=flush pending ops, list=list WAL files'),
    runId: z.string().optional().describe('Run ID for init'),
  }),
}, async ({ action, runId }) => {
  try {
    if (action === 'init') {
      initWal(runId || `run-${Date.now()}`);
      return { content: [{ type: 'text', text: 'WAL initialized' }] };
    }
    if (action === 'flush') {
      const count = flushWal();
      return { content: [{ type: 'text', text: `Flushed ${count} operations` }] };
    }
    if (action === 'list') {
      return { content: [{ type: 'text', text: JSON.stringify(listWalFiles()) }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: `WAL error: ${err.message}` }], isError: true };
  }
});

// ============ Tier (4→1) ============
// memory_tier: action=status|migrate|compress|assign|partition|redistribute
server.registerTool('memory_tier', {
  description: 'HOT/WARM/COLD tier management. Actions: status, migrate (promote/demote), compress (cold tier), assign, partition, redistribute.',
  inputSchema: z.object({
    action: z.enum(['status', 'migrate', 'compress', 'assign', 'partition', 'redistribute']).describe('Action'),
    apply: z.boolean().optional().default(false).describe('Apply changes (for migrate/compress)'),
    memories: z.array(z.object({ id: z.string(), content: z.string(), accessedAt: z.number(), importance: z.number().optional(), tier: z.string().optional() })).optional().describe('Memories (for assign/partition/compress)'),
  }),
}, async ({ action, apply, memories }) => {
  try {
    if (action === 'status') return await memoryTierStatusTool();
    else if (action === 'migrate') return await memoryTierMigrateTool({ apply });
    else if (action === 'compress') {
      if (apply) return await memoryTierCompressTool({ apply: true });
      const cold = (memories || []).filter(m => m.tier === 'COLD');
      const result = compressColdTier(cold);
      return { content: [{ type: 'text', text: JSON.stringify({ preview: true, ...result }) }] };
    } else if (action === 'assign') return { content: [{ type: 'text', text: JSON.stringify(assignTiers(memories || [])) }] };
    else if (action === 'partition') return { content: [{ type: 'text', text: JSON.stringify(partitionByTier(memories || [])) }] };
    else if (action === 'redistribute') return { content: [{ type: 'text', text: JSON.stringify(redistributeTiers(memories || [])) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Tier error [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers

server.registerTool('memory_adaptive', {
  description: 'Adaptive retrieval control. Check if a query should skip vector search (non-informational queries like greetings).',
  inputSchema: z.object({
    query: z.string().describe('Query to check for adaptive skip'),
  }),
}, async ({ query }) => {
  try {
    const skip = shouldSkipRetrieval(query);
    return { content: [{ type: 'text', text: JSON.stringify({ skip_retrieval: skip }) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Adaptive error: ${err.message}` }], isError: true };
  }
});

// ============ Search Engine (4→1: BM25+Vector+MMR+Rerank) ============
// memory_engine: unified search engine (action=bm25|embed|search|mmr|rerank|qmd)
server.registerTool('memory_engine', {
  description: 'Unified search engine. Actions: bm25, embed, search, mmr, rerank, qmd.',
  inputSchema: z.object({
    action: z.enum(['bm25', 'embed', 'search', 'mmr', 'rerank', 'qmd']).describe('Action'),
    query: z.string().optional().describe('Query string (for bm25/search/rerank)'),
    text: z.string().optional().describe('Text to embed (for embed)'),
    documents: z.array(z.object({ id: z.string(), content: z.string(), score: z.number().optional() })).optional().describe('Documents (for mmr/rerank)'),
    topK: z.number().optional().default(10).describe('Number of results'),
    build: z.boolean().optional().default(false).describe('Rebuild BM25 index (for bm25)'),
    lambda: z.number().optional().default(0.5).describe('MMR lambda balance (for mmr)'),
    useEmbedding: z.boolean().optional().default(false).describe('Use embedding MMR (for mmr)'),
    scope: z.string().optional().describe('Scope filter (for search)'),
    method: z.enum(['keyword', 'llm', 'cross']).optional().default('keyword').describe('Rerank method (for rerank)'),
  }),
}, async ({ action, query, text, documents, topK=10, build=false, lambda=0.5, useEmbedding=false, scope, method='keyword' }) => {
  try {
    if (action === 'bm25') {
      if (build) buildBM25Index();
      const results = bm25Search(query || '', topK);
      return { content: [{ type: 'text', text: JSON.stringify(results) }] };
    } else if (action === 'embed') {
      const embedding = await getEmbedding(text || '');
      return { content: [{ type: 'text', text: JSON.stringify({ embedding, dimensions: embedding.length }) }] };
    } else if (action === 'search') {
      const results = await vectorSearch(query || '', topK, scope || null);
      return { content: [{ type: 'text', text: JSON.stringify(results) }] };
    } else if (action === 'mmr') {
      if (useEmbedding) {
        const { getEmbedding: ge } = await import('./vector.js');
        const results = await mmrSelectWithEmbedding(documents || [], topK, lambda, ge);
        return { content: [{ type: 'text', text: JSON.stringify(results) }] };
      }
      const results = mmrSelect(documents || [], topK, lambda);
      return { content: [{ type: 'text', text: JSON.stringify(results) }] };
    } else if (action === 'rerank') {
      if (method === 'keyword') {
        const results = keywordRerank(query || '', documents || [], topK);
        return { content: [{ type: 'text', text: JSON.stringify(results) }] };
      } else if (method === 'llm') {
        const reranker = new LlmReranker();
        const results = await reranker.rerank(query || '', documents || [], topK);
        return { content: [{ type: 'text', text: JSON.stringify(results) }] };
      } else if (method === 'cross') {
        const reranker = new CrossEncoderRerank();
        const results = await rerankResults(query || '', documents || [], topK, reranker);
        return { content: [{ type: 'text', text: JSON.stringify(results) }] };
      }
    } else if (action === 'qmd') {
      if (!isQMDEngine()) {
        const status = await getQMDEngineStatus();
        if (!status.available) {
          return { content: [{ type: 'text', text: JSON.stringify({ error: 'QMD CLI not available', status }, null, 2) }], isError: true };
        }
      }
      const results = await qmdEngineSearch(query || '', { topK, mode: 'hybrid', scope: scope || undefined });
      return { content: [{ type: 'text', text: JSON.stringify({ engine: 'qmd', query, count: results.length, results }, null, 2) }] };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Engine [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers (use memory_engine instead)

server.registerTool('memory_scope', {
  description: 'Filter and manage memory scope levels (AGENT, USER, TEAM, GLOBAL). Normalize scope strings and filter memories by scope.',
  inputSchema: z.object({
    action: z.enum(['normalize', 'filter', 'levels']).describe('Action: normalize=normalize scope string, filter=filter memories by scope, levels=list all levels'),
    scope: z.string().optional().describe('Scope value (for normalize/filter)'),
    memories: z.array(z.object({ id: z.string(), scope: z.string() })).optional().describe('Memories to filter (for filter action)'),
  }),
}, async ({ action, scope, memories }) => {
  try {
    if (action === 'normalize') {
      return { content: [{ type: 'text', text: JSON.stringify({ normalized: normalizeScope(scope || 'GLOBAL') }) }] };
    }
    if (action === 'filter') {
      const filtered = filterByScope(memories || [], scope || 'GLOBAL');
      return { content: [{ type: 'text', text: JSON.stringify({ filtered }) }] };
    }
    if (action === 'levels') {
      return { content: [{ type: 'text', text: JSON.stringify({ levels: SCOPE_LEVELS, hierarchy: SCOPE_HIERARCHY }) }] };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    return { content: [{ type: 'text', text: `Scope error: ${err.message}` }], isError: true };
  }
});

// ============ Proactive Memory Tools (v1.2) ============

// ============ Proactive (6→3) ============
// memory_proactive: action=status|trigger|start|stop
server.registerTool('memory_proactive', {
  description: 'Proactive memory manager. Actions: status, trigger (manual tick), start (background), stop.',
  inputSchema: z.object({
    action: z.enum(['status', 'trigger', 'start', 'stop']).describe('Action'),
    intervalMinutes: z.number().optional().default(5).describe('Interval minutes (for start)'),
  }),
}, async ({ action, intervalMinutes }) => {
  try {
    const m = getProactiveManager();
    if (action === 'status') return { content: [{ type: 'text', text: JSON.stringify(m.getStatus(), null, 2) }] };
    else if (action === 'trigger') { const r = await m.trigger(); return { content: [{ type: 'text', text: JSON.stringify(r, null, 2) }] }; }
    else if (action === 'start') {
      if (m.timer) return { content: [{ type: 'text', text: 'Already running' }] };
      m.intervalMs = (intervalMinutes || 5) * 60000; m.start();
      return { content: [{ type: 'text', text: `Started with ${intervalMinutes||5}min interval` }] };
    } else if (action === 'stop') { m.stop(); return { content: [{ type: 'text', text: 'Stopped' }] }; }
  } catch (err) {
    return { content: [{ type: 'text', text: `Proactive [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers (removed - use memory_proactive directly)

// ============ Proactive Care & Recall (v1.2 - wired from core stubs) ============

// Import the proactive care check function
import { runCheck as runProactiveCareCheck } from './core/proactive_care.js';
import { predictRecall as corePredictRecall, printRecallReport } from './core/proactive_recall.js';

server.registerTool('memory_proactive_care', {
  description: 'Proactive care: detect Liu总 status changes and send caring messages. Checks meeting density, continuous work, negative keywords, and deadline pressure.',
  inputSchema: z.object({
    action: z.enum(['check', 'config', 'enable', 'disable', 'cache', 'test']).describe('Action to perform'),
    text: z.string().optional().describe('Text to test for negative keywords (for test action)'),
  }),
}, async ({ action, text }) => {
  try {
    if (action === 'check') {
      const results = await runProactiveCareCheck();
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            care_alerts: results.length,
            alerts: results.map(r => ({
              type: r.type,
              message: r.message,
              count: r.count,
              hours: r.hours,
            }))
          }, null, 2)
        }]
      };
    } else if (action === 'config') {
      const { loadConfig } = await import('./core/proactive_care.js');
      const config = await loadConfig();
      return { content: [{ type: 'text', text: JSON.stringify(config, null, 2) }] };
    } else if (action === 'enable') {
      const { loadConfig, saveConfig } = await import('./core/proactive_care.js');
      const config = await loadConfig();
      config.enabled = true;
      await saveConfig(config);
      return { content: [{ type: 'text', text: 'Proactive care enabled' }] };
    } else if (action === 'disable') {
      const { loadConfig, saveConfig } = await import('./core/proactive_care.js');
      const config = await loadConfig();
      config.enabled = false;
      await saveConfig(config);
      return { content: [{ type: 'text', text: 'Proactive care disabled' }] };
    } else if (action === 'cache') {
      const { saveCache } = await import('./core/proactive_care.js');
      await saveCache({ meetings: [], messages: [], tasks: [], timestamp: null });
      return { content: [{ type: 'text', text: 'Cache cleared' }] };
    } else if (action === 'test') {
      if (!text) {
        return { content: [{ type: 'text', text: 'Error: text is required for test action' }], isError: true };
      }
      const { loadConfig } = await import('./core/proactive_care.js');
      const config = await loadConfig();
      const keywords = config.rules?.negative_keywords?.keywords || [];
      const matched = keywords.filter(kw => (text || '').includes(kw));
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            text,
            matched_keywords: matched,
            detected: matched.length > 0,
          }, null, 2)
        }]
      };
    }
    return { content: [{ type: 'text', text: 'Unknown action' }], isError: true };
  } catch (err) {
    structuredLog.error(`Proactive care error: ${err.message}`);
    return { content: [{ type: 'text', text: `Proactive care error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_proactive_recall', {
  description: 'Predict which memories to proactively recall based on current context. Uses keyword matching and importance scoring.',
  inputSchema: z.object({
    action: z.enum(['predict', 'report']).describe('Action: predict=run prediction, report=print human-readable report'),
    context: z.string().optional().describe('Context string to match memories against (for predict action)'),
    topK: z.number().optional().default(10).describe('Number of predictions to return'),
  }),
}, async ({ action, context, topK = 10 }) => {
  try {
    if (action === 'report') {
      // Print human-readable report to console, return confirmation
      printRecallReport(context || undefined);
      return { content: [{ type: 'text', text: 'Report printed to stdout' }] };
    }
    // Default: predict
    const predictions = corePredictRecall(context || 'recent');
    const top = predictions.slice(0, topK);
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          context: context || 'time-based',
          predictions: top.map(p => ({
            id: p.memory?.id,
            text: (p.memory?.text || '').slice(0, 100),
            category: p.memory?.category,
            importance: p.memory?.importance,
            relevance: Math.round(p.relevance * 1000) / 1000,
            reason: p.reason,
          }))
        }, null, 2)
      }]
    };
  } catch (err) {
    structuredLog.error(`Proactive recall error: ${err.message}`);
    return { content: [{ type: 'text', text: `Proactive recall error: ${err.message}` }], isError: true };
  }
});

// ============ Reminder (3→1) ============
// memory_reminder: action=add|list|cancel
server.registerTool('memory_reminder', {
  description: 'Reminder management. Actions: add (one-time/recurring), list (all active), cancel (by ID).',
  inputSchema: z.object({
    action: z.enum(['add', 'list', 'cancel']).describe('Action to perform'),
    text: z.string().optional().describe('Reminder text (for add)'),
    type: z.enum(['once', 'recurring']).default('once').describe('Type (for add)'),
    hours: z.number().optional().default(24).describe('Hours until reminder (for add)'),
    id: z.string().optional().describe('Reminder ID (for cancel)'),
  }),
}, async ({ action, text, type = 'once', hours = 24, id }) => {
  const scheduler = getReminderScheduler();
  try {
    if (action === 'add') {
      let rid;
      if (type === 'recurring') {
        rid = scheduler.addRecurringReminder(text, hours);
      } else {
        rid = scheduler.add({ type: 'once', text, dueAt: Date.now() + hours * 3600 * 1000, repeat: null });
      }
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, id: rid }) }] };
    } else if (action === 'list') {
      const reminders = scheduler.list();
      return { content: [{ type: 'text', text: JSON.stringify({ count: reminders.length, reminders }, null, 2) }] };
    } else if (action === 'cancel') {
      const removed = scheduler.cancel(id);
      return { content: [{ type: 'text', text: JSON.stringify({ success: removed }) }] };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Reminder error [${action}]: ${err.message}` }], isError: true };
  }
});

// Deprecated wrappers (delegate to memory_reminder)



// ============ Knowledge Graph Tools (Entity + Relation Extraction) ============

// v4.4: Benchmark & Evaluation
import { runRecallBenchmark } from './benchmark/eval_recall.js';
// v4.4: Entity Config
import { loadEntityConfig, saveEntityConfig, addEntityType, removeEntityType, getEntityTypesByPriority, reloadEntityConfig } from './graph/entity_config.js';
// v4.4: Plugin System
import { getPlugins, getPlugin, enablePlugin, disablePlugin, registerPlugin as registerExternalPlugin, getPluginStats } from './plugin/plugin_manager.js';

import { extractEntities } from './graph/entity.js';
import { extractRelations } from './graph/relation.js';
import {
  loadGraph,
  addEntity,
  addRelation,
  findEntity,
  findEntityById,
  getNeighbors,
  queryGraph,
  getGraphStats,
  mergeIntoGraph,
  clearGraph,
} from './graph/graph_store.js';

// ============ Graph (6→1: entity|relation|query|stats|add|delete) ============
// memory_graph: unified knowledge graph tool
server.registerTool('memory_graph', {
  description: 'Knowledge graph operations. Actions: entity (extract), relation (extract), query (neighbors/paths), stats, add, delete.',
  inputSchema: z.object({
    action: z.enum(['entity', 'relation', 'query', 'stats', 'add', 'delete']).describe('Action'),
    source: z.enum(['text', 'memory', 'all']).optional().default('all').describe('Source (for entity/relation)'),
    text: z.string().optional().describe('Text to process (for entity/relation)'),
    memoryId: z.string().optional().describe('Memory ID (for entity/relation/query)'),
    useLLM: z.boolean().optional().default(false).describe('Use LLM extraction'),
    entity: z.string().optional().describe('Entity name/ID (for query/delete)'),
    depth: z.number().optional().default(1).describe('Query depth (for query)'),
    relationType: z.string().optional().describe('Relation filter (for query)'),
    entityName: z.string().optional().describe('Entity name (for add/delete)'),
    entityId: z.string().optional().describe('Entity ID (for add/delete)'),
    entityType: z.enum(['person','organization','project','topic','tool','location','date','event','other']).optional().describe('Entity type (for add)'),
    entityDesc: z.string().optional().describe('Entity description (for add)'),
    from: z.string().optional().describe('From entity (for add relation)'),
    to: z.string().optional().describe('To entity (for add relation)'),
    relationType2: z.string().optional().describe('Relation type (for add)'),
    confidence: z.number().optional().default(0.8).describe('Confidence (for add)'),
    relationId: z.string().optional().describe('Relation ID (for delete)'),
  }),
}, async (args) => {
  try {
    const { action, source='all', text, memoryId, useLLM=false, entity, depth=1, relationType, entityName, entityId, entityType, entityDesc, from: relFrom, to: relTo, relationType2, confidence=0.8, relationId } = args;
    if (action === 'entity') {
      let textsToProcess = [];
      if (source === 'text' && text) textsToProcess = [{ id: 'inline', text }];
      else if (source === 'memory' && memoryId) { const mem = getMemory(memoryId); if (!mem) return { content: [{ type: 'text', text: 'Memory not found' }], isError: true }; textsToProcess = [mem]; }
      else { const all = await getAllMemories(); textsToProcess = all.map(m => ({ id: m.id, text: m.text })); }
      const allEntities = [];
      for (const item of textsToProcess) { if (!item.text?.trim()) continue; try { const entities = await extractEntities(item.text, { useLLM }); for (const e of entities) { const ex = allEntities.find(n => n.name === e.name && n.type === e.type); if (ex) ex.memory_ids.push(item.id); else allEntities.push({ ...e, memory_ids: [item.id] }); } } catch {} }
      for (const e of allEntities) addEntity(e);
      return { content: [{ type: 'text', text: JSON.stringify({ count: allEntities.length, entities: allEntities.map(e => ({ id: e.id, name: e.name, type: e.type, method: e.method, memory_ids: e.memory_ids.slice(0,5) })), stats: getGraphStats() }, null, 2) }] };
    } else if (action === 'relation') {
      let sourceText = memoryId ? (getMemory(memoryId)?.text || '') : (text || '');
      if (!sourceText) return { content: [{ type: 'text', text: 'text or memoryId required' }], isError: true };
      const entities = await extractEntities(sourceText, { useLLM });
      const relations = await extractRelations(sourceText, entities, {});
      for (const r of relations) addRelation(r);
      return { content: [{ type: 'text', text: JSON.stringify({ count: relations.length, relations: relations.map(r => ({ id: r.id, from: r.from, to: r.to, relation: r.relation, confidence: r.confidence })), entities_found: entities.map(e => ({ id: e.id, name: e.name, type: e.type })) }, null, 2) }] };
    } else if (action === 'query') {
      if (!entity) return { content: [{ type: 'text', text: 'entity required' }], isError: true };
      const graph = loadGraph();
      const entityObj = graph.entities.find(e => e.id === entity || e.name === entity);
      if (!entityObj) return { content: [{ type: 'text', text: JSON.stringify({ error: 'Entity not found', available: graph.entities.slice(0,10).map(e => ({ id:e.id, name:e.name })) }) }] };
      const neighbors = getNeighbors(entityObj.id, relationType || null);
      const pathResult = queryGraph(entity, relationType, depth);
      return { content: [{ type: 'text', text: JSON.stringify({ entity: { id: entityObj.id, name: entityObj.name, type: entityObj.type }, neighbors: neighbors.map(n => ({ id: n.entity.id, name: n.entity.name, type: n.entity.type, relation: n.relation, weight: n.weight })), paths: (pathResult?.paths||[]).map(p => ({ path: p.path, relations: p.relations, weight: p.totalWeight })), stats: getGraphStats() }, null, 2) }] };
    } else if (action === 'stats') {
      const stats = getGraphStats();
      const graph = loadGraph();
      return { content: [{ type: 'text', text: JSON.stringify({ ...stats, sample_entities: graph.entities.slice(0,10), sample_relations: graph.relations.slice(0,10) }, null, 2) }] };
    } else if (action === 'add') {
      const results = [];
      if (entityName && entityType) { const { loadGraph: lg } = await import('./graph/graph_store.js'); const existing = lg().entities.find(e => e.name === entityName && e.type === entityType); if (existing) results.push({ action: 'skipped', reason: 'exists', entity: entityName }); else { const added = addEntity({ name: entityName, type: entityType, description: entityDesc || null }); results.push({ action: 'added', entity: added }); } }
      if (relFrom && relTo && relationType2) { const { loadGraph: lg } = await import('./graph/graph_store.js'); const graph = lg(); const fromE = graph.entities.find(e => e.name === relFrom || e.id === relFrom); const toE = graph.entities.find(e => e.name === relTo || e.id === relTo); if (!fromE || !toE) results.push({ action: 'error', reason: 'entity_not_found' }); else { addRelation({ from: fromE.id, to: toE.id, relation: relationType2, confidence, source: 'manual' }); results.push({ action: 'added', relation: { from: relFrom, to: relTo, type: relationType2 } }); } }
      return { content: [{ type: 'text', text: JSON.stringify({ results }, null, 2) }] };
    } else if (action === 'delete') {
      const { loadGraph: lg, saveGraph: sg } = await import('./graph/graph_store.js');
      if (relationId) { const graph = lg(); const before = graph.relations.length; graph.relations = graph.relations.filter(r => r.id !== relationId); graph.version++; sg(graph); return { content: [{ type: 'text', text: JSON.stringify({ deleted: 'relation', count: before - graph.relations.length }) }] }; }
      if (entityName || entityId) { const graph = lg(); const ent = graph.entities.find(e => (entityName && e.name === entityName) || (entityId && e.id === entityId)); if (!ent) return { content: [{ type: 'text', text: JSON.stringify({ error: 'entity_not_found' }) }] }; const beforeE = graph.entities.length, beforeR = graph.relations.length; graph.entities = graph.entities.filter(e => e.id !== ent.id); graph.relations = graph.relations.filter(r => r.from !== ent.id && r.to !== ent.id); graph.version++; sg(graph); return { content: [{ type: 'text', text: JSON.stringify({ deleted: 'entity', entity: ent.name, entities_removed: beforeE - graph.entities.length, relations_removed: beforeR - graph.relations.length }) }] }; }
      return { content: [{ type: 'text', text: 'Provide entityName/entityId or relationId' }], isError: true };
    }
  } catch (err) { return { content: [{ type: 'text', text: `Graph [${args.action}]: ${err.message}` }], isError: true }; }
});

// Deprecated wrappers





// ============ v2.7.0: Identity Memory Tools ============

server.registerTool('memory_identity_extract', {
  description: 'Extract identity/preference/habit/requirement statements from text. Rules: "我喜欢..."→preference, "我讨厌..."→preference/dislike, "我是..."→identity, "我习惯..."→habit, "我需要..."→requirement, "我会..."→skill. Returns extracted statements with suggested importance scores.',
  inputSchema: z.object({
    text: z.string().describe('Text to extract identity statements from'),
  }),
}, async ({ text }) => {
  return memoryIdentityExtractTool({ text });
});

server.registerTool('memory_identity_update', {
  description: 'Store extracted identity statements as high-priority memories. Identity memories always use importance >= 0.9.',
  inputSchema: z.object({
    extractions: z.array(z.object({
      content: z.string().describe('Extracted text content'),
      type: z.string().optional().describe('Category: identity, preference, habit, requirement, skill, goal'),
      importance: z.number().optional().describe('Importance (default 0.9 for identity types)'),
      subType: z.string().optional().describe('Sub-type label'),
      label: z.string().optional().describe('Human-readable label'),
    })).describe('Array of extracted identity statements from memory_identity_extract'),
  }),
}, async ({ extractions }) => {
  return memoryIdentityUpdateTool({ extractions });
});

server.registerTool('memory_identity_get', {
  description: 'Get a summary of the user\'s identity profile from stored identity memories. Returns all memories categorized as identity, preference, habit, requirement, skill, or goal, grouped by category with importance scores.',
  inputSchema: z.object({
    type: z.string().optional().describe('Filter by specific identity type (identity/preference/habit/requirement/skill/goal)'),
  }),
}, async ({ type }) => {
  return memoryIdentityGetTool({ type });
});

// ============ P1-4: Git Notes Backup/Restore ============

server.registerTool('memory_gitnotes_backup', {
  description: 'Backup memories to git notes for cold storage. Exports memories to .git/notes/memories ref.',
  inputSchema: z.object({
    scope: z.string().optional().describe('Scope to backup: USER, TEAM, AGENT, GLOBAL, or all (default all)'),
  }),
}, async ({ scope }) => {
  return memoryGitnotesBackupTool({ scope });
});

server.registerTool('memory_gitnotes_restore', {
  description: 'Restore memories from git notes backup.',
  inputSchema: z.object({
    scope: z.string().optional().describe('Scope to restore: USER, TEAM, AGENT, GLOBAL, or all (default all)'),
  }),
}, async ({ scope }) => {
  return memoryGitnotesRestoreTool({ scope });
});

// ============ Enhanced Git Notes (decisions, learnings, context) ============
server.registerTool('memory_git_notes', {
  description: 'Enhanced Git Notes for permanent knowledge storage. Actions: add (add decision note to commit), show (view note), list (all notes), tag (add tag), branch_notes (group by branch), search (full-text search). Branch-aware: tracks which branch notes were created on.',
  inputSchema: z.object({
    action: z.enum(['add', 'show', 'list', 'tag', 'branch_notes', 'search']).describe('Action to perform'),
    commit_hash: z.string().optional().describe('Commit hash (for add|show|tag actions)'),
    decision: z.string().optional().describe('Decision/knowledge text (for add action)'),
    category: z.string().optional().describe('Category: decision, learning, context (default: decision)'),
    tag: z.string().optional().describe('Tag to add (for tag action)'),
    query: z.string().optional().describe('Search query (for search action)'),
    limit: z.number().optional().default(100).describe('Max results (for list action)'),
  }),
}, async (args) => {
  return memoryGitNotesTool(args);
});

// ============ Cloud Backup API (managed multi-provider backup) ============
server.registerTool('memory_cloud_backup_api', {
  description: 'Managed Cloud Backup API for unified memory. Supports S3, GCS, Azure, HTTP (WebDAV), and local storage. Actions: configure (set provider), list (list backups), restore (restore from backup), status (get backup status), prune (delete old backups per retention policy), trigger (manual backup), sync (incremental cloud sync).',
  inputSchema: z.object({
    action: z.enum(['configure', 'list', 'restore', 'status', 'prune', 'trigger', 'sync']).describe('Action to perform'),
    provider: z.enum(['s3', 'gcs', 'azure', 'http', 'none']).optional().describe('Cloud provider type (for configure)'),
    endpoint: z.string().optional().describe('API endpoint URL (for configure, e.g. S3 endpoint or WebDAV URL)'),
    bucket: z.string().optional().describe('Bucket/container name (for configure)'),
    accessKey: z.string().optional().describe('Access key or username (for configure)'),
    secretKey: z.string().optional().describe('Secret key or password (for configure)'),
    region: z.string().optional().describe('Region (for configure, e.g. us-east-1)'),
    enabled: z.boolean().optional().describe('Enable/disable cloud backup (for configure)'),
    backupId: z.string().optional().describe('Backup ID to restore (for restore action)'),
    limit: z.number().optional().default(50).describe('Max backups to return (for list action)'),
    maxBackups: z.number().optional().describe('Max backups to keep (for prune action)'),
    maxAgeDays: z.number().optional().describe('Max age in days for backups (for prune action)'),
  }),
}, async (args) => {
  return memoryCloudBackupApiTool(args);
});

// ============ P1-6: Smart Extraction ============

server.registerTool('memory_auto_extract', {
  description: 'Manually trigger structured fact extraction from text. Extracts preferences, facts, decisions, entities from text using LLM + rules.',
  inputSchema: z.object({
    text: z.string().describe('Text to extract structured facts from'),
    useLLM: z.boolean().optional().default(true).describe('Use LLM for extraction (default true)'),
  }),
}, async ({ text, useLLM = true }) => {
  try {
    const extractor = new AutoExtractor();
    const results = await extractor.extractFromConversation(text, useLLM);
    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          count: results.length,
          extracted: results.map(r => ({
            category: r.category,
            text: r.text,
            importance: r.importance,
            source: r.source,
            matched_keyword: r.matched_keyword,
          })),
        }, null, 2),
      }],
    };
  } catch (err) {
    return { content: [{ type: 'text', text: `Auto extract error: ${err.message}` }], isError: true };
  }
});

// ============ P2-7: Cloud Backup/Restore ============

server.registerTool('memory_cloud_backup', {
  description: 'Backup all memories to cloud storage (local/s3/webdav). Uses MemoryBackup class.',
  inputSchema: z.object({
    scope: z.string().optional().describe('Scope to backup: USER, TEAM, AGENT, GLOBAL, or all'),
  }),
}, async ({ scope }) => {
  try {
    const cfg = new CloudConfig();
    const backup = new MemoryBackup(cfg);
    const result = backup.createBackup();
    return { content: [{ type: 'text', text: JSON.stringify({ success: true, ...result }, null, 2) }] };
  } catch (err) {
    return { content: [{ type: 'text', text: `Cloud backup error: ${err.message}` }], isError: true };
  }
});

server.registerTool('memory_cloud_restore', {
  description: 'Restore memories from cloud backup. Lists available backups or restores a specific one.',
  inputSchema: z.object({
    scope: z.string().optional().describe('Scope to restore'),
    backupId: z.string().optional().describe('Specific backup timestamp to restore'),
    action: z.enum(['list', 'restore']).optional().default('list').describe('Action: list available backups or restore'),
  }),
}, async ({ scope, backupId, action = 'list' }) => {
  try {
    const cfg = new CloudConfig();
    const backup = new MemoryBackup(cfg);
    if (action === 'list') {
      const backups = backup.listBackups();
      return { content: [{ type: 'text', text: JSON.stringify({ count: backups.length, backups }, null, 2) }] };
    } else {
      if (!backupId) {
        return { content: [{ type: 'text', text: 'Error: backupId is required for restore action' }], isError: true };
      }
      const result = backup.restoreBackup(backupId);
      return { content: [{ type: 'text', text: JSON.stringify({ success: true, ...result }, null, 2) }] };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Cloud restore error: ${err.message}` }], isError: true };
  }
});

// ============ P1-1: QMD Deep Integration - QMD actions merged into existing memory_engine above [gap-fill]
// (removed duplicate registration)

// ============ P1-2: Web Dashboard HTTP Exposure [gap-fill]
server.registerTool('memory_dashboard', {
  description: 'Start/stop/query the unified-memory web dashboard HTTP server. Provides real-time stats via /api/stats JSON endpoint.',
  inputSchema: z.object({
    action: z.enum(['start', 'stop', 'status']).describe('Action: start dashboard, stop it, or check status'),
    port: z.number().optional().default(3849).describe('Port to listen on (for start action)'),
  }),
}, async ({ action, port = 3849 }) => {
  try {
    if (action === 'status') {
      return { content: [{ type: 'text', text: JSON.stringify({
        running: !!global._memoryDashboardServer,
        port: global._memoryDashboardServer ? port : null,
        url: global._memoryDashboardServer ? `http://localhost:${port}` : null,
      }, null, 2) }] };
    }
    if (action === 'stop') {
      if (global._memoryDashboardServer) {
        global._memoryDashboardServer.close();
        global._memoryDashboardServer = null;
        return { content: [{ type: 'text', text: JSON.stringify({ stopped: true, port }) }] };
      }
      return { content: [{ type: 'text', text: JSON.stringify({ stopped: false, message: 'Dashboard not running' }) }] };
    }
    if (action === 'start') {
      if (global._memoryDashboardServer) {
        return { content: [{ type: 'text', text: JSON.stringify({ running: true, port, url: `http://localhost:${port}`, message: 'Already running' }) }] };
      }
      const dashboardModule = await import('./webui/dashboard.js');
      const server = dashboardModule.startDashboard(port);
      global._memoryDashboardServer = server;
      return { content: [{ type: 'text', text: JSON.stringify({ started: true, port, url: `http://localhost:${port}`, statsEndpoint: `http://localhost:${port}/api/stats` }) }] };
    }
  } catch (err) {
    return { content: [{ type: 'text', text: `Dashboard error: ${err.message}` }], isError: true };
  }
});

// ============ P2-1: Semantic Cache [gap-fill]
server.registerTool('memory_cache', {
  description: 'Semantic query cache. Caches semantically similar query responses (embedding similarity >0.95). TTL-based expiry.',
  inputSchema: z.object({
    action: z.enum(['get', 'set', 'delete', 'clear', 'stats']).describe('Action'),
    query: z.string().optional().describe('Query string (for get/set/delete)'),
    response: z.unknown().optional().describe('Response to cache (for set action)'),
    ttlSeconds: z.number().optional().default(3600).describe('TTL in seconds (for set/get, default 3600)'),
    similarityThreshold: z.number().optional().describe('Min similarity for semantic hit (default 0.95)'),
  }),
}, async ({ action, query, response, ttlSeconds = 3600, similarityThreshold = 0.95 }) => {
  try {
    const result = await Promise.resolve(memoryCacheTool({ action, query, response, ttlSeconds, similarityThreshold }));
    return result;
  } catch (err) {
    return { content: [{ type: 'text', text: `memory_cache error: ${err.message}` }], isError: true };
  }
});

// ============ P2-2: Incremental Sync [gap-fill]
server.registerTool('memory_sync', {
  description: 'Cross-device incremental sync. Push delta to remote (WebDAV/S3/local) or pull and merge remote changes.',
  inputSchema: z.object({
    action: z.enum(['status', 'push', 'pull']).describe('Action: check status, push delta, or pull+merge'),
    providerType: z.enum(['local', 'webdav']).optional().default('local').describe('Sync provider type'),
    providerConfig: z.record(z.string(), z.unknown()).optional().describe('Provider config: webdav needs {url, username, password}'),
    remotePath: z.string().optional().describe('Specific delta file to pull (optional)'),
    scope: z.string().optional().default('default').describe('Sync scope/namespace'),
    conflictStrategy: z.enum(['timestamp', 'source_priority']).optional().default('timestamp').describe('Conflict resolution strategy'),
  }),
}, async ({ action, providerType = 'local', providerConfig, remotePath, scope = 'default', conflictStrategy = 'timestamp' }) => {
  try {
    const result = memorySyncTool({ action, providerType, providerConfig, remotePath, scope, conflictStrategy });
    // memorySyncTool is sync, not async
    return result;
  } catch (err) {
    return { content: [{ type: 'text', text: `memory_sync error: ${err.message}` }], isError: true };
  }
});

// ============ Session State RAM Layer ============
server.registerTool('memory_session', {
  description: 'Session State RAM Layer: manages SESSION-STATE.md at workspace root. Tracks current task, key context, and pending actions. Survives context compaction. Actions: get (read state), set_task (update current task), add_context (add key:value), add_action (add pending action), complete_action (mark done), clear (reset).',
  inputSchema: z.object({
    action: z.enum(['get', 'set_task', 'add_context', 'add_action', 'complete_action', 'clear']).describe('Action to perform'),
    task: z.string().optional().describe('Task description (for set_task)'),
    key: z.string().optional().describe('Context key (for add_context)'),
    value: z.string().optional().describe('Context value (for add_context)'),
    action_text: z.string().optional().describe('Action text (for add_action/complete_action)'),
  }),
}, async (args) => {
  return memorySessionTool(args);
});

// ============ Cognitive Memory Scheduler ============
// memory_cognitive: Curiosity-driven memory exploration
server.registerTool('memory_cognitive', {
  description: 'Cognitive memory scheduler: curiosity-driven memory exploration. Actions: trigger (check curiosity after memory access), score (score curiosity between two memories), get_recalls (get memories to proactively recall), record_exploration (record a curiosity exploration), status (get cognitive state).',
  inputSchema: z.object({
    action: z.enum(['trigger', 'score', 'get_recalls', 'record_exploration', 'status']).describe('Action to perform'),
    memory_id: z.string().optional().describe('Memory ID (for trigger/score actions)'),
    candidate_id: z.string().optional().describe('Candidate memory ID (for score action)'),
    from_memory: z.string().optional().describe('Source memory ID (for record_exploration)'),
    to_memory: z.string().optional().describe('Target memory ID (for record_exploration)'),
  }),
}, async (args) => {
  return memoryCognitiveTool(args);
});

// ============ Memory Lanes ============
// memory_lanes: Parallel swim lanes for different memory contexts (action=create|switch|current|list|move|archive|memories)
server.registerTool('memory_lanes', {
  description: 'Parallel memory lanes for organizing memories into different contexts. Lanes: primary (main conversation), task (current task focus), background (long-running investigations), archive (completed threads). Actions: create (new lane), switch (set active lane), current (get active lane), list (all lanes), move (move memory between lanes), archive (archive a lane), memories (get memories in a lane).',
  inputSchema: z.object({
    action: z.enum(['create', 'switch', 'current', 'list', 'move', 'archive', 'memories']).describe('Action to perform'),
    name: z.string().optional().describe('Lane name (for create/switch/list actions)'),
    description: z.string().optional().describe('Lane description (for create action)'),
    lane_name: z.string().optional().describe('Lane name (for switch/move/archive/memories actions)'),
    memory_id: z.string().optional().describe('Memory ID (for move action)'),
  }),
}, async (args) => {
  return memoryLanesTool(args);
});

// ============ Transcript Manager ============
// memory_transcript: Transcript-first memory system (action=create|log|end|get|list|search|rebuild|link_memory|extract_entities)
server.registerTool('memory_transcript', {
  description: 'Transcript-first memory system. Stores full conversation transcripts as JSON files. Actions: create (new transcript), log (add message), end (close transcript), get (retrieve), list (paginated), search (full-text), rebuild (context), link_memory (associate), extract_entities.',
  inputSchema: z.object({
    action: z.enum(['create', 'log', 'end', 'get', 'list', 'search', 'rebuild', 'link_memory', 'extract_entities']).describe('Action to perform'),
    transcript_id: z.string().optional().describe('Transcript ID (for log/end/get/rebuild/extract_entities/link_memory)'),
    topic: z.string().optional().describe('Topic/title (for create, optional)'),
    session_id: z.string().optional().describe('Session ID (for create, optional, auto-generated if not provided)'),
    role: z.string().optional().describe('Message role: user|assistant|system (for log action)'),
    content: z.string().optional().describe('Message content (for log action)'),
    metadata: z.record(z.string(), z.unknown()).optional().describe('Additional metadata (for log action, e.g. message_id)'),
    query: z.string().optional().describe('Search query (for search action)'),
    memory_id: z.string().optional().describe('Memory ID to link (for link_memory action)'),
    limit: z.number().optional().default(20).describe('Result limit (for list/search actions)'),
    offset: z.number().optional().default(0).describe('Offset for pagination (for list action)'),
    status: z.string().optional().describe('Status filter: active|completed|archived (for list action)'),
  }),
}, async (args) => {
  return memoryTranscriptTool(args);
});

// ============ HTTP Dashboard Server (Optional) ============

function startDashboardServer(port = 3848) {
  const __dirname = path.dirname(fileURLToPath(import.meta.url));
  const dashboardPath = path.join(__dirname, 'dashboard.html');

  const mimeTypes = {
    '.html': 'text/html; charset=utf-8',
    '.js': 'application/javascript',
    '.css': 'text/css',
    '.json': 'application/json',
    '.png': 'image/png',
    '.ico': 'image/x-icon',
  };

  const server = http.createServer((req, res) => {
    const url = req.url.split('?')[0];

    // Serve dashboard
    if (url === '/' || url === '/dashboard') {
      fs.readFile(dashboardPath, 'utf8', (err, data) => {
        if (err) {
          res.writeHead(404, { 'Content-Type': 'text/plain' });
          res.end('Dashboard not found');
          return;
        }
        res.writeHead(200, { 'Content-Type': mimeTypes['.html'] });
        res.end(data);
      });
      return;
    }

    // ---- API Routes ----
    let apiResult;
    try {
      if (url === '/memories' && req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'application/json' });
        getAllMemories().then(data => res.end(JSON.stringify(data)));
        return;
      }
      if (url === '/stats') {
        getAllMemories().then(all => {
          const byCategory = {};
          const byTier = { HOT: 0, WARM: 0, COLD: 0 };
          const byScope = {};
          all.forEach(m => {
            byCategory[m.category || 'unknown'] = (byCategory[m.category || 'unknown'] || 0) + 1;
            if (m.tier) byTier[m.tier] = (byTier[m.tier] || 0) + 1;
            if (m.scope) byScope[m.scope] = (byScope[m.scope] || 0) + 1;
          });
          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            total: all.length,
            byCategory,
            byTier,
            byScope,
            memoryCount: all.length
          }));
        });
        return;
      }
      const deleteMatch = url.match(/^\/memories\/([^/?]+)/);
      if (deleteMatch && req.method === 'DELETE') {
        const id = decodeURIComponent(deleteMatch[1]);
        deleteMemory(id);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ success: true }));
        return;
      }
      if (url === '/memories' && req.method === 'POST') {
        let body = '';
        req.on('data', chunk => body += chunk);
        req.on('end', () => {
          try {
            const { text, category, importance, tags } = JSON.parse(body);
            const mem = addMemory({ text, category, importance, tags });
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify(mem));
          } catch {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'Invalid JSON' }));
          }
        });
        return;
      }
    } catch (e) {
      res.writeHead(500, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ error: e.message }));
      return;
    }

    // 404
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Not found');
  });

  server.listen(port, () => {
    structuredLog.info(`Dashboard server listening on http://localhost:${port}`);
  });

  return server;
}

// Expose startDashboardServer so it can be called from outside
global._startMemoryDashboard = startDashboardServer;

// ============ Start ============

async function main() {
    structuredLog.info( `Starting unified-memory-mcp v1.1.0`);
    structuredLog.info( `Memory file: ${config.memoryFile}`);
    structuredLog.info( `Ollama: ${config.ollamaUrl}`);

  // Start v2.8.0 Unified Web UI + API Server (port 3850)
  try {
    const { spawn } = await import('child_process');
    const unifiedProcess = spawn('node', ['src/webui/unified_server.js', '--port=3850'], {
      stdio: 'ignore',
      detached: true
    });
    unifiedProcess.unref();
    structuredLog.info('v2.8.0 Unified Server started on port 3850');

  } catch (err) {
    structuredLog.warn(`Failed to start unified server: ${err.message}`);
  }

  // Register multimodal tools (image/audio/file analysis)
  registerMultimodalTools(server);

  // Register Episode v2 tools (conversation session management)
  registerEpisodeTools(server);

  // Register Rerank v2 tools (LLM cross-encoder reranking)
  registerRerankTools(server);

  // Register Refresh v2 tools (48h reconsolidation)
  registerRefreshTools(server);

  // Register Procedural Memory v2 tools
  registerProceduralTools(server);

  // Register Rule Memory v2 tools
  registerRuleTools(server);

  // Register Observability v2 tools (HTTP API)
  registerObservabilityTools(server);

  // Register Chunking v2 tools (context chunking)
  registerChunkTools(server);

  // Register Phase 3 tools: OpenClaw Plugin, Git, Cloud, Weibull
  registerPluginTools(server);
  registerGitTools(server);
  registerCloudTools(server);
  registerDecayStatsTool(server);

  // P0-4: Revision Manager
  registerRevisionTools(server);

  // P1: WAL Protocol
  structuredLog.info('Registering WAL tools...');
  registerWALTools(server);
  structuredLog.info('WAL tools registered');

  // P2: Evidence Chain
  structuredLog.info('Registering Evidence tools...');
  registerEvidenceTools(server);
  structuredLog.info('Evidence tools registered');

  // P3: Auto Organization
  structuredLog.info('Registering Organize tools...');
  registerOrganizeTools(server);
  structuredLog.info('Organize tools registered');

  // P4: Transcript-First Architecture
  structuredLog.info('Registering Transcript-First tools...');
  registerTranscriptFirstTools(server);
  structuredLog.info('Transcript-First tools registered');

  // WAL Tools (extracted to src/entries/wal-tools.js)

  // Evidence Tools (extracted to src/entries/evidence-tools.js)

  // Organize Tools (extracted to src/entries/organize-tools.js)

  // Transcript-First Tools (extracted to src/entries/transcript-tools.js)

  const transport = new StdioServerTransport();
  await server.connect(transport);
    structuredLog.info( 'MCP Server connected via stdio');
}

main().catch((err) => {
  console.error('Fatal:', err);
  process.exit(1);
});

// Scene Block Tools (extracted to src/entries/scene-tools.js)
// Pipeline Tools (extracted to src/entries/scene-tools.js)
// Register v4.0 tools
registerSceneBlockTools(server);
registerPipelineTools(server);

// Cleaner Tools (extracted to src/entries/system-tools.js)
registerCleanerTools(server);

// Local Embedding Tools (extracted to src/entries/system-tools.js)
  registerBenchmarkTools(server);
  registerEntityTools(server);
  registerPluginToolsInline(server);

// 初始化本地 Embedding
if (config.localEmbedding?.enabled && config.localEmbedding?.autoWarmup) {
  const service = getLocalEmbedding(config.localEmbedding);
  service.startWarmup();
}

// 初始化清理器
if (config.cleaner?.enabled) {
  const cleaner = initCleaner({
    baseDir: config.memoryDir,
    ...config.cleaner,
  });
  cleaner.start();
}

// ─── v4.0: Hook Integration ─────────────────────────────────────────────────────

// 导出 hook 函数供 OpenClaw 调用
export async function before_prompt_build(context) {
  // 自动召回: 在对话开始前注入相关记忆
  const { sessionId, userId, query } = context;
  
  try {
    // 搜索相关记忆
    const results = await hybridSearch(query, { topK: 5, scope: 'USER' });
    
    if (results.length > 0) {
      const memoryContext = results.map(r => r.memory.text).join('\n');
      return {
        injectedContext: `相关记忆:\n${memoryContext}`,
      };
    }
  } catch (err) {
    log.error('[Hook] before_prompt_build error:', err);
  }
  
  return {};
}

export async function agent_end(context) {
  // 自动捕获: 对话结束后触发管线
  const { sessionId, userId } = context;
  
  try {
    await onConversationEnd(sessionId, 'USER');
  } catch (err) {
    log.error('[Hook] agent_end error:', err);
  }
}


// ─── v4.1.3: Tool Utilities (ported from memory-tencentdb) ───────────────────
export {
  CheckpointManager,
  CleanContextRunner,
  parseModelRef,
  resolveModelFromMainConfig,
  prewarmEmbeddedAgent,
  sanitizeText,
  shouldCaptureL0,
  shouldExtractL1,
  shouldCapture,
  looksLikePromptInjection,
  escapeXmlTags,
  sanitizeJsonForParse,
  pickRecentUnique,
  SerialQueue,
  ManagedTimer,
  SessionFilter,
  BackupManager,
  extractWords,
  // v4.2.0: Hooks (from memory-tencentdb)
  performAutoCapture,
  performAutoRecall,
  // v4.2.0: Conversation
  recordConversation,
  // v4.2.0: Record / L1
  batchDedup,
  // v4.2.0: Scene
  generateSceneNavigation,
  stripSceneNavigation,
  readSceneIndex,
  syncSceneIndex,
  parseSceneBlock,
  formatSceneBlock,
  // v4.2.0: Persona
  PersonaTrigger,
  // v4.2.0: Prompts
  CONFLICT_DETECTION_SYSTEM_PROMPT,
  formatBatchConflictPrompt,
  EXTRACT_MEMORIES_SYSTEM_PROMPT,
  formatExtractionPrompt,
  buildPersonaPrompt,
  buildSceneExtractionPrompt,
  // v4.2.0: Tools
  executeConversationSearch,
  formatConversationSearchResponse,
  executeMemorySearch,
  formatSearchResponse,
  // v4.3: Supermemory Features
  getDynamicProfile,
  getProfiles,
  invalidateProfileCache,
  detectContradiction,
  detectContradictions,
  resolveContradictions,
  dedupWithContradictionResolution,
  isTemporalMemory,
  extractExpiryTime,
  isExpired,
  extractExpiryTimes,
  cleanExpiredMemories,
  startExpiryChecker,
  hybridSearchEngine,
  searchMemoriesOnly,
  searchDocumentsOnly,
  getSearchStats,
  BaseConnector,
  registerConnector,
  createConnector,
  listConnectors,
  createConnectors,
  BaseExtractor,
  TextExtractor,
  registerExtractor,
  createExtractor,
  getExtractorForFile,
  autoExtract,
  listExtractors,
  // v4.4: Benchmark (Supermemory comparison)
  runRecallBenchmark,
  // v4.4: Entity Config
  loadEntityConfig,
  saveEntityConfig,
  addEntityType,
  removeEntityType,
  getEntityTypesByPriority,
  reloadEntityConfig,
  // v4.4: Plugin System
  getPlugins,
  getPlugin,
  enablePlugin,
  disablePlugin,
  registerExternalPlugin,
  getPluginStats,
};
