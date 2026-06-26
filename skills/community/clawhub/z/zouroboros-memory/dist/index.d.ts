import Sqlite3 from 'better-sqlite3';

type DecayClass = 'permanent' | 'long' | 'medium' | 'short';
interface MemoryConfig {
    enabled: boolean;
    dbPath: string;
    vectorEnabled: boolean;
    ollamaUrl: string;
    ollamaModel: string;
    autoCapture: boolean;
    captureIntervalMinutes: number;
    graphBoost: boolean;
    hydeExpansion: boolean;
    decayConfig: {
        permanent: number;
        long: number;
        medium: number;
        short: number;
    };
    reranker?: {
        enabled: boolean;
        model?: string;
        maxContextChunks?: number;
    };
    cot?: {
        enabled: boolean;
        model?: string;
    };
}
interface MemoryEntry {
    id: string;
    entity: string;
    key: string | null;
    value: string;
    decay: DecayClass;
    createdAt: string;
    updatedAt: string;
    tags?: string[];
}
interface MemorySearchResult {
    entry: MemoryEntry;
    score: number;
    matchType: 'exact' | 'semantic' | 'hybrid' | 'graph';
}
interface EpisodicMemory {
    id: string;
    conversationId: string;
    summary: string;
    outcome: 'success' | 'failure' | 'resolved' | 'ongoing';
    entities: string[];
    tags: string[];
    createdAt: string;
    tokenCount?: number;
    daysAgo?: number;
    procedureName?: string;
    procedureVersion?: number | null;
}
interface TemporalQuery {
    since?: string;
    until?: string;
    outcome?: 'success' | 'failure' | 'resolved' | 'ongoing';
    limit?: number;
}
interface CognitiveProfile {
    entity: string;
    traits: Record<string, number>;
    preferences: Record<string, string>;
    interactionHistory: InteractionRecord[];
    lastUpdated: string;
}
interface InteractionRecord {
    timestamp: string;
    type: 'query' | 'store' | 'search';
    success: boolean;
    latencyMs: number;
}
interface GraphNode {
    id: string;
    type: string;
    label: string;
    properties: Record<string, unknown>;
}
interface GraphEdge {
    source: string;
    target: string;
    relation: string;
    weight: number;
}
interface CotAnswerResult {
    answer: string;
    reasoning: string;
    confidence: number;
    sourceFacts: string[];
}
interface DeepSearchResult {
    results: MemorySearchResult[];
    answer: CotAnswerResult;
}

/**
 * Bun:sqlite compatibility wrapper around better-sqlite3.
 * Exposes the same API surface that Zouroboros memory code uses.
 */

interface RunResult {
    changes: number;
    lastInsertRowid: number | bigint;
}
declare class QueryStatement<T = Record<string, unknown>> {
    private stmt;
    constructor(stmt: Sqlite3.Statement);
    all(...params: unknown[]): T[];
    get(...params: unknown[]): T | null;
    run(...params: unknown[]): RunResult;
}
declare class Database {
    private _db;
    constructor(path: string, options?: {
        readonly?: boolean;
    });
    exec(sql: string): void;
    query<T = Record<string, unknown>>(sql: string): QueryStatement<T>;
    prepare(sql: string): QueryStatement;
    run(sql: string, params?: unknown[]): RunResult;
    close(): void;
}

/**
 * Database management for Zouroboros Memory
 */

declare function initDatabase(config: MemoryConfig): Database;
declare function getDatabase(): Database;
declare function closeDatabase(): void;
declare function isInitialized(): boolean;
declare function runMigrations(config: MemoryConfig): void;
declare function getDbStats(config: MemoryConfig): {
    facts: number;
    episodes: number;
    procedures: number;
    openLoops: number;
    embeddings: number;
};

/**
 * Vector embeddings for semantic search
 *
 * ECC-010: Memory Explosion Throttling
 *   - Rate limiting: max MAX_EMBEDDINGS_PER_MINUTE per conversation (sliding window)
 *   - Dedup: same content hash within DEDUP_COOLDOWN_MS returns cached embedding
 *   - Tail sampling: when rate limited, return last cached embedding for the conversation
 *   - Metrics: throttleCount / dedupCount exported for observability
 */

/** Exported metrics counters — reset only on process restart. */
declare const throttleMetrics: {
    throttleCount: number;
    dedupCount: number;
};
/** ECC-010: Reset throttle state (for testing). */
declare function resetThrottleState(): void;
/**
 * Generate embeddings for text using Ollama.
 *
 * ECC-010: Throttling applied when conversationId is provided:
 *   1. Dedup check — returns cached embedding if same content seen within 5 min
 *   2. Rate limit check — returns tail-sampled embedding if > 20/min per conversation
 *   3. Ollama call — only reached if dedup and rate limit both pass
 *
 * @param conversationId  Optional. When provided, enables per-conversation throttling.
 */
declare function generateEmbedding(text: string, config: MemoryConfig, conversationId?: string): Promise<number[]>;
/**
 * Generate a hypothetical answer using Ollama's generate endpoint.
 * Used by HyDE to create an ideal document for embedding.
 */
declare function generateHypotheticalAnswer(query: string, config: MemoryConfig, options?: {
    model?: string;
    maxTokens?: number;
}): Promise<string>;
/**
 * Generate HyDE (Hypothetical Document Expansion) embeddings.
 *
 * 1. Embeds the original query.
 * 2. Uses an LLM to generate a hypothetical ideal answer.
 * 3. Embeds the hypothetical answer.
 * 4. Returns both embeddings so the caller can blend them.
 *
 * Falls back to duplicating the original embedding if generation fails.
 */
declare function generateHyDEExpansion(query: string, config: MemoryConfig, options?: {
    generationModel?: string;
    maxTokens?: number;
}): Promise<{
    original: number[];
    expanded: number[];
    hypothetical: string;
}>;
/**
 * Blend two embeddings by weighted average.
 * Default: 40% original query, 60% hypothetical answer (HyDE sweet spot).
 */
declare function blendEmbeddings(a: number[], b: number[], weightA?: number): number[];
/**
 * Calculate cosine similarity between two vectors
 */
declare function cosineSimilarity(a: number[], b: number[]): number;
/**
 * Serialize embedding for SQLite storage
 */
declare function serializeEmbedding(embedding: number[]): Buffer;
/**
 * Deserialize embedding from SQLite storage
 */
declare function deserializeEmbedding(buffer: Buffer): number[];
/**
 * Check if Ollama is available
 */
declare function checkOllamaHealth(config: MemoryConfig): Promise<boolean>;
/**
 * List available models from Ollama
 */
declare function listAvailableModels(config: MemoryConfig): Promise<string[]>;

/**
 * Fact storage and retrieval operations
 */

type Category = 'preference' | 'fact' | 'decision' | 'convention' | 'other' | 'reference' | 'project';
interface StoreFactInput {
    entity: string;
    key?: string;
    value: string;
    persona?: string;
    category?: Category;
    decay?: DecayClass;
    importance?: number;
    source?: string;
    confidence?: number;
    metadata?: Record<string, unknown>;
}
/**
 * Store a fact in memory
 */
declare function storeFact(input: StoreFactInput, config: MemoryConfig): Promise<MemoryEntry>;
/**
 * Search facts by exact match or keyword
 */
declare function searchFacts(query: string, options?: {
    entity?: string;
    category?: string;
    persona?: string;
    limit?: number;
}): MemoryEntry[];
/**
 * Search facts using vector similarity
 */
declare function searchFactsVector(query: string, config: MemoryConfig, options?: {
    limit?: number;
    threshold?: number;
    useHyDE?: boolean;
    persona?: string;
}): Promise<MemorySearchResult[]>;
/**
 * Hybrid search combining exact and vector search
 */
declare function searchFactsHybrid(query: string, config: MemoryConfig, options?: {
    limit?: number;
    vectorWeight?: number;
    rerank?: boolean;
    persona?: string;
}): Promise<MemorySearchResult[]>;
/**
 * Get a fact by ID
 */
declare function getFact(id: string): MemoryEntry | null;
/**
 * Delete a fact by ID
 */
declare function deleteFact(id: string): boolean;
/**
 * Update fact access time
 */
declare function touchFact(id: string): void;
/**
 * Clean up expired facts
 */
declare function cleanupExpiredFacts(): number;

/**
 * Episodic memory for event-based storage
 */

type Outcome = 'success' | 'failure' | 'resolved' | 'ongoing';
interface CreateEpisodeInput {
    summary: string;
    outcome: Outcome;
    entities: string[];
    happenedAt?: Date;
    durationMs?: number;
    procedureId?: string;
    metadata?: Record<string, unknown>;
}
/**
 * Create a new episode
 */
declare function createEpisode(input: CreateEpisodeInput): EpisodicMemory;
/**
 * Search episodes with temporal filters
 */
declare function searchEpisodes(query: TemporalQuery): EpisodicMemory[];
/**
 * Get episodes for a specific entity
 */
declare function getEntityEpisodes(entity: string, options?: {
    limit?: number;
    outcome?: Outcome;
}): EpisodicMemory[];
/**
 * Update episode outcome
 */
declare function updateEpisodeOutcome(id: string, outcome: Outcome): boolean;
/**
 * Get episode statistics
 */
declare function getEpisodeStats(): {
    total: number;
    byOutcome: Record<Outcome, number>;
};

/**
 * Graph-boosted search v2
 *
 * Builds an implicit entity graph from facts and episodes,
 * then uses graph traversal to boost search results for
 * entities that are closely related to the query context.
 */

/**
 * Invalidate the graph cache. Call after mutations (fact store/delete, episode create).
 */
declare function invalidateGraphCache(): void;
/**
 * Build a graph of entity co-occurrences from episodes.
 * Two entities are connected if they appear in the same episode.
 * Results are cached with a 60-second TTL.
 */
declare function buildEntityGraph(): {
    nodes: GraphNode[];
    edges: GraphEdge[];
};
/**
 * Get entities related to a given entity via graph traversal.
 * Returns entities within `depth` hops, scored by connection strength.
 */
declare function getRelatedEntities(entity: string, options?: {
    depth?: number;
    limit?: number;
}): {
    entity: string;
    score: number;
}[];
/**
 * Graph-boosted search: augments keyword/vector results with
 * graph-adjacent facts from related entities.
 *
 * Uses RRF fusion across three signals:
 * 1. Exact/keyword matches (weight: exactWeight)
 * 2. Vector/semantic matches (weight: vectorWeight)
 * 3. Graph-adjacent facts (weight: graphWeight)
 */
declare function searchFactsGraphBoosted(baseResults: MemorySearchResult[], queryEntities: string[], options?: {
    limit?: number;
    graphWeight?: number;
    graphDepth?: number;
}): MemorySearchResult[];
/**
 * Extract entity names from a query string.
 * Simple heuristic: capitalized words, quoted strings, known entities.
 */
declare function extractQueryEntities(query: string): string[];

/**
 * Cognitive profile tracking for entities (executors, users, subsystems).
 *
 * Tracks interaction patterns, performance traits, and preferences
 * to enable adaptive behavior over time.
 */

/**
 * Get or create a cognitive profile for an entity.
 */
declare function getProfile(entity: string): CognitiveProfile;
/**
 * Update traits for an entity (merges with existing).
 */
declare function updateTraits(entity: string, traits: Record<string, number>): void;
/**
 * Update preferences for an entity (merges with existing).
 */
declare function updatePreferences(entity: string, preferences: Record<string, string>): void;
/**
 * Record an interaction for tracking patterns.
 */
declare function recordInteraction(entity: string, type: 'query' | 'store' | 'search', success: boolean, latencyMs: number): void;
/**
 * Get recent interactions for an entity.
 */
declare function getRecentInteractions(entity: string, limit?: number): InteractionRecord[];
/**
 * Get performance summary for an entity.
 */
declare function getProfileSummary(entity: string): {
    entity: string;
    totalInteractions: number;
    successRate: number;
    avgLatencyMs: number;
    traitCount: number;
    preferenceCount: number;
};
/**
 * List all known entities with profiles.
 */
declare function listProfiles(): string[];
/**
 * Delete a cognitive profile.
 */
declare function deleteProfile(entity: string): boolean;
/**
 * Ensure the profile_interactions table exists.
 * Called during memory system init.
 */
declare function ensureProfileSchema(): void;

/**
 * MCP (Model Context Protocol) server for Zouroboros Memory
 *
 * Exposes memory operations as MCP tools accessible by external
 * AI agents and clients via stdio transport.
 *
 * Usage: node dist/mcp-server.js [--db-path <path>]
 */

interface McpRequest {
    jsonrpc: '2.0';
    id: number | string;
    method: string;
    params?: Record<string, unknown>;
}
interface McpResponse {
    jsonrpc: '2.0';
    id: number | string;
    result?: unknown;
    error?: {
        code: number;
        message: string;
        data?: unknown;
    };
}
declare function handleMessage(message: McpRequest, config: MemoryConfig): Promise<McpResponse>;
/**
 * Start the MCP server on stdio.
 */
declare function startMcpServer(config: MemoryConfig): Promise<void>;

/**
 * Procedure memory queries for MCP exposure.
 *
 * Provides search, get, compare_versions, and get_episodes
 * actions over the `procedures` table.
 */
interface ProcedureStep {
    executor: string;
    taskPattern: string;
    timeoutSeconds: number;
    fallbackExecutor?: string;
    notes?: string;
}
interface Procedure {
    id: string;
    name: string;
    version: number;
    steps: ProcedureStep[];
    successCount: number;
    failureCount: number;
    evolvedFrom: string | null;
    createdAt: number;
}
interface ProcedureEpisode {
    episodeId: string;
    summary: string;
    outcome: string;
    happenedAt: number;
    daysAgo: number;
}
interface ProcedureComparison {
    name: string;
    fromVersion: number;
    toVersion: number;
    stepsAdded: ProcedureStep[];
    stepsRemoved: ProcedureStep[];
    stepsChanged: Array<{
        step: number;
        from: ProcedureStep;
        to: ProcedureStep;
    }>;
    successRateFrom: string;
    successRateTo: string;
}
/**
 * Search procedures by name pattern (FTS-like LIKE query).
 */
declare function searchProcedures(query: string, limit?: number): Procedure[];
/**
 * Get a specific procedure by name (latest version) or name + version.
 */
declare function getProcedure(name: string, version?: number): Procedure | null;
/**
 * List all versions of a procedure.
 */
declare function getProcedureVersions(name: string): Procedure[];
/**
 * Compare two versions of a procedure.
 */
declare function compareProcedureVersions(name: string, fromVersion: number, toVersion: number): ProcedureComparison | null;
/**
 * Get episodes linked to a procedure (via procedure_id FK on episodes table).
 */
declare function getProcedureEpisodes(procedureName: string, limit?: number): ProcedureEpisode[];

/**
 * LLM-based reranker for memory search results.
 *
 * After hybrid search retrieves candidates, the reranker uses an LLM
 * to select and reorder the most relevant results for a given query.
 * Gracefully falls back to truncation on any failure.
 */

declare function rerankResults(query: string, results: MemorySearchResult[], config: MemoryConfig, topK?: number): Promise<MemorySearchResult[]>;

/**
 * Lightweight LLM client for memory retrieval enhancement (reranker, CoT).
 *
 * Routes to OpenAI (default) or Ollama based on model spec.
 * Model spec format: "provider:model" or bare model name.
 */
type LlmProvider = 'openai' | 'ollama';
interface LlmCallOptions {
    prompt: string;
    system?: string;
    model?: string;
    temperature?: number;
    maxTokens?: number;
}
interface LlmCallResult {
    content: string;
    latencyMs: number;
    provider: LlmProvider;
    model: string;
}
declare function llmCall(opts: LlmCallOptions): Promise<LlmCallResult>;

/**
 * @zouroboros/memory
 *
 * Production-grade persistent memory system with hybrid search,
 * decay classes, episodic memory, cognitive profiles, and MCP server.
 * Node.js 22+ port of the Zouroboros memory subsystem.
 *
 * @module @zouroboros/memory
 */
declare const VERSION = "1.0.0";

/**
 * Initialize the memory system (database + migrations + profile schema).
 */
declare function init(config: MemoryConfig): void;
/**
 * Shutdown the memory system gracefully.
 */
declare function shutdown(): void;
/**
 * Get combined memory system statistics.
 */
declare function getStats(config: MemoryConfig): {
    database: {
        facts: number;
        episodes: number;
        procedures: number;
        openLoops: number;
        embeddings: number;
    };
    episodes: {
        total: number;
        byOutcome: Record<string, number>;
    };
};

export { type CognitiveProfile, type CotAnswerResult, type DecayClass, type DeepSearchResult, type EpisodicMemory, type GraphEdge, type GraphNode, type InteractionRecord, type LlmCallOptions, type LlmCallResult, type MemoryConfig, type MemoryEntry, type MemorySearchResult, type Procedure, type ProcedureComparison, type ProcedureEpisode, type ProcedureStep, type TemporalQuery, VERSION, blendEmbeddings, buildEntityGraph, checkOllamaHealth, cleanupExpiredFacts, closeDatabase, compareProcedureVersions, cosineSimilarity, createEpisode, deleteFact, deleteProfile, deserializeEmbedding, ensureProfileSchema, extractQueryEntities, generateEmbedding, generateHyDEExpansion, generateHypotheticalAnswer, getDatabase, getDbStats, getEntityEpisodes, getEpisodeStats, getFact, getProcedure, getProcedureEpisodes, getProcedureVersions, getProfile, getProfileSummary, getRecentInteractions, getRelatedEntities, getStats, handleMessage, init, initDatabase, invalidateGraphCache, isInitialized, listAvailableModels, listProfiles, llmCall, recordInteraction, rerankResults, resetThrottleState, runMigrations, searchEpisodes, searchFacts, searchFactsGraphBoosted, searchFactsHybrid, searchFactsVector, searchProcedures, serializeEmbedding, shutdown, startMcpServer, storeFact, throttleMetrics, touchFact, updateEpisodeOutcome, updatePreferences, updateTraits };
