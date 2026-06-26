import {
  blendEmbeddings,
  checkOllamaHealth,
  cosineSimilarity,
  deserializeEmbedding,
  generateEmbedding,
  generateHyDEExpansion,
  generateHypotheticalAnswer,
  listAvailableModels,
  resetThrottleState,
  serializeEmbedding,
  throttleMetrics
} from "./chunk-5GUD3MLZ.js";

// src/compat/sqlite.ts
import Sqlite3 from "better-sqlite3";
var QueryStatement = class {
  stmt;
  constructor(stmt) {
    this.stmt = stmt;
  }
  all(...params) {
    return this.stmt.all(...params);
  }
  get(...params) {
    return this.stmt.get(...params) ?? null;
  }
  run(...params) {
    return this.stmt.run(...params);
  }
};
var Database = class {
  _db;
  constructor(path, options) {
    this._db = new Sqlite3(path, options);
  }
  exec(sql) {
    this._db.exec(sql);
  }
  query(sql) {
    return new QueryStatement(this._db.prepare(sql));
  }
  prepare(sql) {
    return new QueryStatement(this._db.prepare(sql));
  }
  run(sql, params = []) {
    return this._db.prepare(sql).run(...params);
  }
  close() {
    this._db.close();
  }
};

// src/database.ts
import { existsSync, mkdirSync } from "fs";
import { dirname } from "path";
var db = null;
var SCHEMA_SQL = `
CREATE TABLE IF NOT EXISTS facts (
  id TEXT PRIMARY KEY,
  persona TEXT,
  entity TEXT NOT NULL,
  key TEXT,
  value TEXT NOT NULL,
  text TEXT NOT NULL,
  category TEXT DEFAULT 'fact' CHECK(category IN ('preference', 'fact', 'decision', 'convention', 'other', 'reference', 'project')),
  decay_class TEXT DEFAULT 'medium' CHECK(decay_class IN ('permanent', 'long', 'medium', 'short')),
  importance REAL DEFAULT 1.0,
  source TEXT,
  created_at INTEGER DEFAULT (strftime('%s', 'now')),
  expires_at INTEGER,
  last_accessed INTEGER DEFAULT (strftime('%s', 'now')),
  confidence REAL DEFAULT 1.0,
  metadata TEXT
);

CREATE TABLE IF NOT EXISTS fact_embeddings (
  fact_id TEXT PRIMARY KEY REFERENCES facts(id) ON DELETE CASCADE,
  embedding BLOB NOT NULL,
  model TEXT DEFAULT 'nomic-embed-text',
  created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS episodes (
  id TEXT PRIMARY KEY,
  summary TEXT NOT NULL,
  outcome TEXT NOT NULL CHECK(outcome IN ('success', 'failure', 'resolved', 'ongoing')),
  happened_at INTEGER NOT NULL,
  duration_ms INTEGER,
  procedure_id TEXT,
  metadata TEXT,
  created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS episode_entities (
  episode_id TEXT NOT NULL REFERENCES episodes(id) ON DELETE CASCADE,
  entity TEXT NOT NULL,
  PRIMARY KEY (episode_id, entity)
);

CREATE TABLE IF NOT EXISTS procedures (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  version INTEGER DEFAULT 1,
  steps TEXT NOT NULL,
  success_count INTEGER DEFAULT 0,
  failure_count INTEGER DEFAULT 0,
  evolved_from TEXT,
  created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS open_loops (
  id TEXT PRIMARY KEY,
  summary TEXT NOT NULL,
  entity TEXT NOT NULL,
  status TEXT DEFAULT 'open' CHECK(status IN ('open', 'resolved')),
  priority INTEGER DEFAULT 1,
  created_at INTEGER DEFAULT (strftime('%s', 'now')),
  resolved_at INTEGER
);

CREATE TABLE IF NOT EXISTS continuation_context (
  id TEXT PRIMARY KEY,
  conversation_id TEXT NOT NULL,
  last_summary TEXT NOT NULL,
  open_loop_ids TEXT,
  entity_stack TEXT,
  last_agent TEXT,
  updated_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE TABLE IF NOT EXISTS cognitive_profiles (
  entity TEXT PRIMARY KEY,
  traits TEXT,
  preferences TEXT,
  interaction_count INTEGER DEFAULT 0,
  last_interaction INTEGER,
  created_at INTEGER DEFAULT (strftime('%s', 'now'))
);

CREATE INDEX IF NOT EXISTS idx_facts_entity_key ON facts(entity, key);
CREATE INDEX IF NOT EXISTS idx_facts_decay ON facts(decay_class, expires_at);
CREATE INDEX IF NOT EXISTS idx_facts_category ON facts(category);
CREATE INDEX IF NOT EXISTS idx_facts_persona ON facts(persona);
CREATE INDEX IF NOT EXISTS idx_episodes_happened ON episodes(happened_at);
CREATE INDEX IF NOT EXISTS idx_episodes_outcome ON episodes(outcome);
CREATE INDEX IF NOT EXISTS idx_episode_entities ON episode_entities(entity);
CREATE INDEX IF NOT EXISTS idx_open_loops_entity ON open_loops(entity, status);
`;
function initDatabase(config) {
  if (db) return db;
  const dir = dirname(config.dbPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
  db = new Database(config.dbPath);
  db.exec("PRAGMA journal_mode = WAL");
  db.exec(SCHEMA_SQL);
  return db;
}
function getDatabase() {
  if (!db) {
    throw new Error("Database not initialized. Call initDatabase first.");
  }
  return db;
}
function closeDatabase() {
  if (db) {
    db.close();
    db = null;
  }
}
function isInitialized() {
  return db !== null;
}
function runMigrations(config) {
  const database = initDatabase(config);
  database.exec(`
    CREATE TABLE IF NOT EXISTS _migrations (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      applied_at INTEGER DEFAULT (strftime('%s', 'now'))
    );
  `);
  const applied = database.query("SELECT name FROM _migrations").all();
  const appliedSet = new Set(applied.map((m) => m.name));
  const migrations = [
    {
      name: "001_ensure_facts_persona_column",
      sql: `CREATE INDEX IF NOT EXISTS idx_facts_persona ON facts(persona);`
    },
    {
      name: "002_backfill_facts_persona_shared",
      sql: `UPDATE facts SET persona = 'shared' WHERE persona IS NULL;`
    }
  ];
  for (const migration of migrations) {
    if (!appliedSet.has(migration.name)) {
      database.exec(migration.sql);
      database.run("INSERT INTO _migrations (name) VALUES (?)", [migration.name]);
    }
  }
}
function getDbStats(config) {
  const database = initDatabase(config);
  return {
    facts: database.query("SELECT COUNT(*) as count FROM facts").get().count,
    episodes: database.query("SELECT COUNT(*) as count FROM episodes").get().count,
    procedures: database.query("SELECT COUNT(*) as count FROM procedures").get().count,
    openLoops: database.query("SELECT COUNT(*) as count FROM open_loops").get().count,
    embeddings: database.query("SELECT COUNT(*) as count FROM fact_embeddings").get().count
  };
}

// src/episodes.ts
import { randomUUID } from "crypto";
function createEpisode(input) {
  const db2 = getDatabase();
  const id = randomUUID();
  const happenedAt = input.happenedAt || /* @__PURE__ */ new Date();
  db2.run(
    `INSERT INTO episodes (id, summary, outcome, happened_at, duration_ms, procedure_id, metadata)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [
      id,
      input.summary,
      input.outcome,
      Math.floor(happenedAt.getTime() / 1e3),
      input.durationMs || null,
      input.procedureId || null,
      input.metadata ? JSON.stringify(input.metadata) : null
    ]
  );
  for (const entity of input.entities) {
    db2.run(
      "INSERT INTO episode_entities (episode_id, entity) VALUES (?, ?)",
      [id, entity]
    );
  }
  return {
    id,
    conversationId: id,
    // Using episode ID as conversation ID
    summary: input.summary,
    outcome: input.outcome,
    entities: input.entities,
    tags: [],
    createdAt: happenedAt.toISOString()
  };
}
function searchEpisodes(query) {
  const db2 = getDatabase();
  const nowSec = Math.floor(Date.now() / 1e3);
  let sql = `
    SELECT e.id, e.summary, e.outcome, e.happened_at as happenedAt,
           e.duration_ms as durationMs, e.procedure_id as procedureId,
           e.metadata, e.created_at as createdAt,
           p.name as procedureName, p.version as procedureVersion
    FROM episodes e
    LEFT JOIN procedures p ON e.procedure_id = p.id
    WHERE 1=1
  `;
  const params = [];
  if (query.since) {
    sql += " AND e.happened_at >= ?";
    params.push(Math.floor(new Date(query.since).getTime() / 1e3));
  }
  if (query.until) {
    sql += " AND e.happened_at <= ?";
    params.push(Math.floor(new Date(query.until).getTime() / 1e3));
  }
  if (query.outcome) {
    sql += " AND e.outcome = ?";
    params.push(query.outcome);
  }
  sql += " ORDER BY e.happened_at DESC";
  if (query.limit) {
    sql += " LIMIT ?";
    params.push(query.limit);
  }
  const rows = db2.query(sql).all(...params);
  return rows.map((row) => {
    const entityRows = db2.query(
      "SELECT entity FROM episode_entities WHERE episode_id = ?"
    ).all(row.id);
    const daysAgo = Math.round((nowSec - row.happenedAt) / 86400);
    return {
      id: row.id,
      conversationId: row.id,
      summary: row.summary,
      outcome: row.outcome,
      entities: entityRows.map((e) => e.entity),
      tags: [],
      createdAt: new Date(row.createdAt * 1e3).toISOString(),
      tokenCount: row.durationMs || void 0,
      // procedure linkage
      ...row.procedureName && { procedureName: row.procedureName, procedureVersion: row.procedureVersion },
      // temporal enrichment
      daysAgo
    };
  });
}
function getEntityEpisodes(entity, options = {}) {
  const db2 = getDatabase();
  const { limit = 10, outcome } = options;
  const nowSec = Math.floor(Date.now() / 1e3);
  let sql = `
    SELECT e.id, e.summary, e.outcome, e.happened_at as happenedAt,
           e.duration_ms as durationMs, e.procedure_id as procedureId,
           e.metadata, e.created_at as createdAt,
           p.name as procedureName, p.version as procedureVersion
    FROM episodes e
    JOIN episode_entities ee ON e.id = ee.episode_id
    LEFT JOIN procedures p ON e.procedure_id = p.id
    WHERE ee.entity = ?
  `;
  const params = [entity];
  if (outcome) {
    sql += " AND e.outcome = ?";
    params.push(outcome);
  }
  sql += " ORDER BY e.happened_at DESC LIMIT ?";
  params.push(limit);
  const rows = db2.query(sql).all(...params);
  return rows.map((row) => {
    const daysAgo = Math.round((nowSec - row.happenedAt) / 86400);
    return {
      id: row.id,
      conversationId: row.id,
      summary: row.summary,
      outcome: row.outcome,
      entities: [entity],
      tags: [],
      createdAt: new Date(row.createdAt * 1e3).toISOString(),
      tokenCount: row.durationMs || void 0,
      ...row.procedureName && { procedureName: row.procedureName, procedureVersion: row.procedureVersion },
      daysAgo
    };
  });
}
function updateEpisodeOutcome(id, outcome) {
  const db2 = getDatabase();
  const result = db2.run(
    "UPDATE episodes SET outcome = ? WHERE id = ?",
    [outcome, id]
  );
  return result.changes > 0;
}
function getEpisodeStats() {
  const db2 = getDatabase();
  const total = db2.query("SELECT COUNT(*) as count FROM episodes").get().count;
  const byOutcome = {
    success: 0,
    failure: 0,
    resolved: 0,
    ongoing: 0
  };
  const rows = db2.query(
    "SELECT outcome, COUNT(*) as count FROM episodes GROUP BY outcome"
  ).all();
  for (const row of rows) {
    byOutcome[row.outcome] = row.count;
  }
  return { total, byOutcome };
}

// src/profiles.ts
function getProfile(entity) {
  const db2 = getDatabase();
  const row = db2.query(
    "SELECT entity, traits, preferences, interaction_count, last_interaction, created_at FROM cognitive_profiles WHERE entity = ?"
  ).get(entity);
  if (row) {
    return {
      entity: row.entity,
      traits: row.traits ? JSON.parse(row.traits) : {},
      preferences: row.preferences ? JSON.parse(row.preferences) : {},
      interactionHistory: getRecentInteractions(entity),
      lastUpdated: row.last_interaction ? new Date(row.last_interaction * 1e3).toISOString() : new Date(row.created_at * 1e3).toISOString()
    };
  }
  const now = Math.floor(Date.now() / 1e3);
  db2.run(
    "INSERT INTO cognitive_profiles (entity, traits, preferences, interaction_count, last_interaction) VALUES (?, ?, ?, 0, ?)",
    [entity, "{}", "{}", now]
  );
  return {
    entity,
    traits: {},
    preferences: {},
    interactionHistory: [],
    lastUpdated: new Date(now * 1e3).toISOString()
  };
}
function updateTraits(entity, traits) {
  const db2 = getDatabase();
  const profile = getProfile(entity);
  const merged = { ...profile.traits, ...traits };
  const now = Math.floor(Date.now() / 1e3);
  db2.run(
    "UPDATE cognitive_profiles SET traits = ?, last_interaction = ? WHERE entity = ?",
    [JSON.stringify(merged), now, entity]
  );
}
function updatePreferences(entity, preferences) {
  const db2 = getDatabase();
  const profile = getProfile(entity);
  const merged = { ...profile.preferences, ...preferences };
  const now = Math.floor(Date.now() / 1e3);
  db2.run(
    "UPDATE cognitive_profiles SET preferences = ?, last_interaction = ? WHERE entity = ?",
    [JSON.stringify(merged), now, entity]
  );
}
function recordInteraction(entity, type, success, latencyMs) {
  const db2 = getDatabase();
  const now = Math.floor(Date.now() / 1e3);
  getProfile(entity);
  db2.run(
    `INSERT INTO profile_interactions (entity, type, success, latency_ms, timestamp)
     VALUES (?, ?, ?, ?, ?)`,
    [entity, type, success ? 1 : 0, latencyMs, now]
  );
  db2.run(
    "UPDATE cognitive_profiles SET interaction_count = interaction_count + 1, last_interaction = ? WHERE entity = ?",
    [now, entity]
  );
}
function getRecentInteractions(entity, limit = 50) {
  const db2 = getDatabase();
  const tableExists = db2.query(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='profile_interactions'"
  ).get();
  if (!tableExists) return [];
  const rows = db2.query(
    "SELECT type, success, latency_ms, timestamp FROM profile_interactions WHERE entity = ? ORDER BY timestamp DESC LIMIT ?"
  ).all(entity, limit);
  return rows.map((row) => ({
    timestamp: new Date(row.timestamp * 1e3).toISOString(),
    type: row.type,
    success: row.success === 1,
    latencyMs: row.latency_ms
  }));
}
function getProfileSummary(entity) {
  const db2 = getDatabase();
  const profile = getProfile(entity);
  const row = db2.query(
    "SELECT interaction_count FROM cognitive_profiles WHERE entity = ?"
  ).get(entity);
  const tableExists = db2.query(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='profile_interactions'"
  ).get();
  let successRate2 = 0;
  let avgLatencyMs = 0;
  if (tableExists) {
    const stats = db2.query(
      "SELECT AVG(CAST(success AS REAL)) as sr, AVG(latency_ms) as avg_lat FROM profile_interactions WHERE entity = ?"
    ).get(entity);
    successRate2 = stats?.sr ?? 0;
    avgLatencyMs = stats?.avg_lat ?? 0;
  }
  return {
    entity,
    totalInteractions: row?.interaction_count ?? 0,
    successRate: successRate2,
    avgLatencyMs,
    traitCount: Object.keys(profile.traits).length,
    preferenceCount: Object.keys(profile.preferences).length
  };
}
function listProfiles() {
  const db2 = getDatabase();
  const rows = db2.query(
    "SELECT entity FROM cognitive_profiles ORDER BY last_interaction DESC"
  ).all();
  return rows.map((r) => r.entity);
}
function deleteProfile(entity) {
  const db2 = getDatabase();
  const result = db2.run("DELETE FROM cognitive_profiles WHERE entity = ?", [entity]);
  const tableExists = db2.query(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='profile_interactions'"
  ).get();
  if (tableExists) {
    db2.run("DELETE FROM profile_interactions WHERE entity = ?", [entity]);
  }
  return result.changes > 0;
}
function ensureProfileSchema() {
  const db2 = getDatabase();
  db2.exec(`
    CREATE TABLE IF NOT EXISTS profile_interactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      entity TEXT NOT NULL,
      type TEXT NOT NULL CHECK(type IN ('query', 'store', 'search')),
      success INTEGER NOT NULL DEFAULT 1,
      latency_ms REAL NOT NULL DEFAULT 0,
      timestamp INTEGER NOT NULL DEFAULT (strftime('%s', 'now'))
    );
    CREATE INDEX IF NOT EXISTS idx_profile_interactions_entity ON profile_interactions(entity, timestamp);
  `);
}

// src/facts.ts
import { randomUUID as randomUUID2 } from "crypto";

// src/graph.ts
var _graphCache = null;
var GRAPH_CACHE_TTL_MS = 6e4;
function invalidateGraphCache() {
  _graphCache = null;
}
function buildEntityGraph() {
  if (_graphCache && Date.now() - _graphCache.builtAt < GRAPH_CACHE_TTL_MS) {
    return { nodes: _graphCache.nodes, edges: _graphCache.edges };
  }
  const db2 = getDatabase();
  const entityRows = db2.query(
    "SELECT DISTINCT entity FROM episode_entities"
  ).all();
  const nodes = entityRows.map((r) => ({
    id: r.entity,
    type: "entity",
    label: r.entity,
    properties: {}
  }));
  const edgeMap = /* @__PURE__ */ new Map();
  const episodes = db2.query(
    "SELECT id FROM episodes"
  ).all();
  const stmt = db2.query(
    "SELECT entity FROM episode_entities WHERE episode_id = ?"
  );
  for (const ep of episodes) {
    const entities = stmt.all(ep.id).map((r) => r.entity);
    for (let i = 0; i < entities.length; i++) {
      for (let j = i + 1; j < entities.length; j++) {
        const key = [entities[i], entities[j]].sort().join("||");
        edgeMap.set(key, (edgeMap.get(key) ?? 0) + 1);
      }
    }
  }
  const factEntities = db2.query(
    "SELECT DISTINCT entity FROM facts"
  ).all();
  for (const fe of factEntities) {
    const existing = nodes.find((n) => n.id === fe.entity);
    if (!existing) {
      nodes.push({
        id: fe.entity,
        type: "entity",
        label: fe.entity,
        properties: {}
      });
    }
  }
  const edges = Array.from(edgeMap.entries()).map(([key, weight]) => {
    const [source, target] = key.split("||");
    return { source, target, relation: "co-occurs", weight };
  });
  _graphCache = { nodes, edges, builtAt: Date.now() };
  return { nodes, edges };
}
function getRelatedEntities(entity, options = {}) {
  const { depth = 2, limit = 20 } = options;
  const { edges } = buildEntityGraph();
  const visited = /* @__PURE__ */ new Map();
  const queue = [
    { entity, score: 1, hop: 0 }
  ];
  visited.set(entity, 1);
  while (queue.length > 0) {
    const current = queue.shift();
    if (current.hop >= depth) continue;
    for (const edge of edges) {
      let neighbor = null;
      if (edge.source === current.entity) neighbor = edge.target;
      else if (edge.target === current.entity) neighbor = edge.source;
      if (neighbor && !visited.has(neighbor)) {
        const decayFactor = 1 / (current.hop + 2);
        const score = current.score * decayFactor * Math.min(edge.weight, 5) / 5;
        visited.set(neighbor, score);
        queue.push({ entity: neighbor, score, hop: current.hop + 1 });
      }
    }
  }
  visited.delete(entity);
  return Array.from(visited.entries()).map(([entity2, score]) => ({ entity: entity2, score })).sort((a, b) => b.score - a.score).slice(0, limit);
}
function searchFactsGraphBoosted(baseResults, queryEntities, options = {}) {
  const { limit = 10, graphWeight = 0.2, graphDepth = 2 } = options;
  const db2 = getDatabase();
  const relatedEntities = /* @__PURE__ */ new Map();
  for (const entity of queryEntities) {
    for (const related of getRelatedEntities(entity, { depth: graphDepth })) {
      const existing = relatedEntities.get(related.entity) ?? 0;
      relatedEntities.set(related.entity, Math.max(existing, related.score));
    }
  }
  if (relatedEntities.size === 0) return baseResults;
  const entityList = Array.from(relatedEntities.keys());
  const placeholders = entityList.map(() => "?").join(",");
  const graphRows = db2.query(`
    SELECT id, entity, key, value, category, decay_class as decayClass,
           importance, created_at as createdAt
    FROM facts
    WHERE entity IN (${placeholders})
      AND (expires_at IS NULL OR expires_at > strftime('%s', 'now'))
    ORDER BY importance DESC
    LIMIT 50
  `).all(...entityList);
  const graphResults = graphRows.map((row) => ({
    entry: {
      id: row.id,
      entity: row.entity,
      key: row.key,
      value: row.value,
      decay: row.decayClass,
      createdAt: new Date(row.createdAt * 1e3).toISOString(),
      updatedAt: new Date(row.createdAt * 1e3).toISOString(),
      tags: row.category ? [row.category] : void 0
    },
    score: relatedEntities.get(row.entity) ?? 0,
    matchType: "graph"
  }));
  const k = 60;
  const scores = /* @__PURE__ */ new Map();
  const baseWeight = 1 - graphWeight;
  baseResults.forEach((result, rank) => {
    const rrfScore = 1 / (k + rank + 1) * baseWeight;
    scores.set(result.entry.id, {
      entry: result.entry,
      score: rrfScore,
      matchType: result.matchType
    });
  });
  graphResults.sort((a, b) => b.score - a.score).forEach((result, rank) => {
    const rrfScore = 1 / (k + rank + 1) * graphWeight;
    const existing = scores.get(result.entry.id);
    if (existing) {
      existing.score += rrfScore;
    } else {
      scores.set(result.entry.id, {
        entry: result.entry,
        score: rrfScore,
        matchType: "graph"
      });
    }
  });
  return Array.from(scores.values()).sort((a, b) => b.score - a.score).slice(0, limit).map((r) => ({
    entry: r.entry,
    score: r.score,
    matchType: r.matchType
  }));
}
function extractQueryEntities(query) {
  const db2 = getDatabase();
  const words = query.split(/\s+/);
  const knownEntities = /* @__PURE__ */ new Set();
  const entityRows = db2.query(
    "SELECT DISTINCT entity FROM facts"
  ).all();
  const entitySet = new Set(entityRows.map((r) => r.entity.toLowerCase()));
  for (let i = 0; i < words.length; i++) {
    const word = words[i].replace(/[^a-zA-Z0-9_-]/g, "");
    if (entitySet.has(word.toLowerCase())) {
      knownEntities.add(word);
    }
    if (i < words.length - 1) {
      const bigram = `${word} ${words[i + 1].replace(/[^a-zA-Z0-9_-]/g, "")}`;
      if (entitySet.has(bigram.toLowerCase())) {
        knownEntities.add(bigram);
      }
    }
  }
  return Array.from(knownEntities);
}

// src/llm.ts
var KNOWN_OPENAI = /* @__PURE__ */ new Set([
  "gpt-4o",
  "gpt-4o-mini",
  "gpt-4-turbo",
  "gpt-4",
  "gpt-3.5-turbo",
  "o1",
  "o1-mini",
  "o3-mini"
]);
function parseSpec(spec) {
  if (!spec) return { provider: "openai", model: "gpt-4o-mini" };
  const colon = spec.indexOf(":");
  if (colon >= 0) {
    const prefix = spec.slice(0, colon).toLowerCase();
    if (prefix === "openai" || prefix === "ollama") {
      return { provider: prefix, model: spec.slice(colon + 1) };
    }
  }
  if (KNOWN_OPENAI.has(spec)) return { provider: "openai", model: spec };
  return { provider: "ollama", model: spec };
}
async function callOpenai(opts, model) {
  const key = process.env.OPENAI_API_KEY || process.env.ZO_OPENAI_API_KEY;
  if (!key) throw new Error("OPENAI_API_KEY not set");
  const start = Date.now();
  const messages = [];
  if (opts.system) messages.push({ role: "system", content: opts.system });
  messages.push({ role: "user", content: opts.prompt });
  const resp = await fetch("https://api.openai.com/v1/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${key}`
    },
    body: JSON.stringify({
      model,
      messages,
      temperature: opts.temperature ?? 0.1,
      max_tokens: opts.maxTokens ?? 200
    }),
    signal: AbortSignal.timeout(3e4)
  });
  if (!resp.ok) throw new Error(`OpenAI ${resp.status}: ${await resp.text()}`);
  const data = await resp.json();
  return {
    content: data.choices?.[0]?.message?.content?.trim() || "",
    latencyMs: Date.now() - start,
    provider: "openai",
    model
  };
}
async function callOllama(opts, model) {
  const url = process.env.OLLAMA_URL || "http://localhost:11434";
  const start = Date.now();
  const body = {
    model,
    prompt: opts.prompt,
    stream: false,
    keep_alive: "24h",
    options: {
      temperature: opts.temperature ?? 0.1,
      num_predict: opts.maxTokens ?? 200
    }
  };
  if (opts.system) body.system = opts.system;
  const resp = await fetch(`${url}/api/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(6e4)
  });
  if (!resp.ok) throw new Error(`Ollama ${resp.status}: ${await resp.text()}`);
  const data = await resp.json();
  return {
    content: (data.response || "").trim(),
    latencyMs: Date.now() - start,
    provider: "ollama",
    model
  };
}
async function llmCall(opts) {
  const { provider, model } = parseSpec(opts.model || "gpt-4o-mini");
  switch (provider) {
    case "openai":
      return callOpenai(opts, model);
    case "ollama":
      return callOllama(opts, model);
  }
}

// src/reranker.ts
var DEFAULT_TOP_K = 6;
var DEFAULT_MODEL = "gpt-4o-mini";
var PREVIEW_CHARS = 300;
async function rerankResults(query, results, config, topK) {
  const k = topK ?? config.reranker?.maxContextChunks ?? DEFAULT_TOP_K;
  if (results.length <= k) return results;
  const model = config.reranker?.model ?? DEFAULT_MODEL;
  const numbered = results.map((r, i) => `[${i + 1}] ${r.entry.value.slice(0, PREVIEW_CHARS)}`).join("\n\n");
  const prompt = `You are a relevance judge. Given a question and numbered context passages, return ONLY the numbers of the ${k} most relevant passages in order of relevance, comma-separated.

Question: ${query}

Passages:
${numbered}

Return ONLY comma-separated numbers (e.g. "3,1,5"). No explanation.`;
  try {
    const resp = await llmCall({ prompt, model, temperature: 0, maxTokens: 60 });
    const indices = resp.content.match(/\d+/g)?.map(Number).filter((n) => n >= 1 && n <= results.length) ?? [];
    if (indices.length === 0) return results.slice(0, k);
    const seen = /* @__PURE__ */ new Set();
    const reranked = [];
    for (const idx of indices) {
      if (!seen.has(idx) && reranked.length < k) {
        seen.add(idx);
        reranked.push(results[idx - 1]);
      }
    }
    for (let i = 0; i < results.length && reranked.length < k; i++) {
      if (!seen.has(i + 1)) reranked.push(results[i]);
    }
    return reranked;
  } catch {
    return results.slice(0, k);
  }
}

// src/facts.ts
var TTL_DEFAULTS = {
  permanent: null,
  long: 365 * 24 * 3600,
  medium: 90 * 24 * 3600,
  short: 30 * 24 * 3600
};
var DEDUP_SUBSTR_LEN = 60;
function deduplicateResults(results) {
  const seen = [];
  return results.filter((r) => {
    const val = r.entry.value;
    const substr = val.slice(0, DEDUP_SUBSTR_LEN);
    if (seen.some((s) => s === substr || val.includes(s) || s.includes(substr.slice(0, 40)))) {
      return false;
    }
    seen.push(substr);
    return true;
  });
}
async function storeFact(input, config) {
  const db2 = getDatabase();
  const id = randomUUID2();
  const now = Math.floor(Date.now() / 1e3);
  const decay = input.decay || "medium";
  const ttl = TTL_DEFAULTS[decay];
  const expiresAt = ttl ? now + ttl : null;
  const text = input.key ? `${input.entity} ${input.key} ${input.value}` : `${input.entity} ${input.value}`;
  const entry = {
    id,
    entity: input.entity,
    key: input.key || null,
    value: input.value,
    decay,
    createdAt: (/* @__PURE__ */ new Date()).toISOString(),
    updatedAt: (/* @__PURE__ */ new Date()).toISOString()
  };
  db2.run(
    `INSERT INTO facts (id, persona, entity, key, value, text, category, decay_class, importance, source,
                        created_at, expires_at, confidence, metadata)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
    [
      id,
      input.persona || "shared",
      input.entity,
      input.key || null,
      input.value,
      text,
      input.category || "fact",
      decay,
      input.importance || 1,
      input.source || "manual",
      now,
      expiresAt,
      input.confidence || 1,
      input.metadata ? JSON.stringify(input.metadata) : null
    ]
  );
  if (config.vectorEnabled) {
    try {
      const embedding = await generateEmbedding(text, config);
      const serialized = serializeEmbedding(embedding);
      db2.run(
        "INSERT INTO fact_embeddings (fact_id, embedding, model) VALUES (?, ?, ?)",
        [id, serialized, config.ollamaModel]
      );
    } catch (error) {
      console.warn("Failed to generate embedding:", error);
    }
  }
  invalidateGraphCache();
  return entry;
}
function searchFacts(query, options = {}) {
  const db2 = getDatabase();
  const { entity, category, persona, limit = 10 } = options;
  let sql = `
    SELECT id, persona, entity, key, value, category, decay_class as decayClass,
           importance, source, created_at as createdAt, expires_at as expiresAt,
           confidence, metadata
    FROM facts
    WHERE (text LIKE ? OR entity LIKE ? OR value LIKE ?)
      AND (expires_at IS NULL OR expires_at > strftime('%s', 'now'))
  `;
  const params = [`%${query}%`, `%${query}%`, `%${query}%`];
  if (persona) {
    sql += " AND (persona = ? OR persona = ?)";
    params.push(persona, "shared");
  }
  if (entity) {
    sql += " AND entity = ?";
    params.push(entity);
  }
  if (category) {
    sql += " AND category = ?";
    params.push(category);
  }
  sql += " ORDER BY importance DESC, created_at DESC LIMIT ?";
  params.push(limit);
  const rows = db2.query(sql).all(...params);
  return rows.map((row) => ({
    id: row.id,
    entity: row.entity,
    key: row.key,
    value: row.value,
    decay: row.decayClass,
    createdAt: new Date(row.createdAt * 1e3).toISOString(),
    updatedAt: new Date(row.createdAt * 1e3).toISOString(),
    tags: row.category ? [row.category] : void 0
  }));
}
async function searchFactsVector(query, config, options = {}) {
  if (!config.vectorEnabled) {
    throw new Error("Vector search is disabled. Enable it in configuration.");
  }
  const db2 = getDatabase();
  const { limit = 10, threshold = 0.7, useHyDE } = options;
  let queryEmbedding;
  const shouldUseHyDE = useHyDE ?? config.hydeExpansion;
  if (shouldUseHyDE) {
    const hyde = await generateHyDEExpansion(query, config);
    queryEmbedding = blendEmbeddings(hyde.original, hyde.expanded);
  } else {
    queryEmbedding = await generateEmbedding(query, config);
  }
  let factsSql = `
    SELECT f.id, f.entity, f.key, f.value, f.category, f.decay_class as decayClass,
           f.importance, f.created_at as createdAt, f.persona, fe.embedding
    FROM facts f
    JOIN fact_embeddings fe ON f.id = fe.fact_id
    WHERE (f.expires_at IS NULL OR f.expires_at > strftime('%s', 'now'))
  `;
  const factsParams = [];
  if (options.persona) {
    factsSql += " AND (f.persona = ? OR f.persona = ?)";
    factsParams.push(options.persona, "shared");
  }
  const rows = factsParams.length > 0 ? db2.query(factsSql).all(...factsParams) : db2.query(factsSql).all();
  const { cosineSimilarity: cosineSimilarity2 } = await import("./embeddings-MWMHNJOJ.js");
  const results = rows.map((row) => {
    const embedding = deserializeEmbedding(row.embedding);
    const similarity = cosineSimilarity2(queryEmbedding, embedding);
    return {
      entry: {
        id: row.id,
        entity: row.entity,
        key: row.key,
        value: row.value,
        decay: row.decayClass,
        createdAt: new Date(row.createdAt * 1e3).toISOString(),
        updatedAt: new Date(row.createdAt * 1e3).toISOString(),
        tags: row.category ? [row.category] : void 0
      },
      score: similarity,
      matchType: "semantic"
    };
  }).filter((r) => r.score >= threshold).sort((a, b) => b.score - a.score).slice(0, limit);
  return results;
}
async function searchFactsHybrid(query, config, options = {}) {
  const { limit = 10, vectorWeight = 0.7, persona } = options;
  const shouldRerank = options.rerank ?? config.reranker?.enabled ?? false;
  const fetchLimit = shouldRerank ? Math.max(limit * 2, 20) : limit;
  const exactMatches = searchFacts(query, { limit: fetchLimit * 2, persona });
  let vectorMatches = [];
  if (config.vectorEnabled) {
    try {
      vectorMatches = await searchFactsVector(query, config, { limit: fetchLimit * 2, persona });
    } catch (error) {
      console.warn("Vector search failed:", error);
    }
  }
  const k = 60;
  const scores = /* @__PURE__ */ new Map();
  exactMatches.forEach((entry, rank) => {
    const id = entry.id;
    const rrfScore = 1 / (k + rank + 1);
    scores.set(id, { entry, score: rrfScore * (1 - vectorWeight) });
  });
  vectorMatches.forEach((result, rank) => {
    const id = result.entry.id;
    const rrfScore = 1 / (k + rank + 1);
    const existing = scores.get(id);
    if (existing) {
      existing.score += rrfScore * vectorWeight;
    } else {
      scores.set(id, { entry: result.entry, score: rrfScore * vectorWeight });
    }
  });
  let fused = Array.from(scores.values()).sort((a, b) => b.score - a.score).slice(0, fetchLimit).map((r) => ({
    entry: r.entry,
    score: r.score,
    matchType: "hybrid"
  }));
  fused = deduplicateResults(fused);
  if (shouldRerank && fused.length > 0) {
    fused = await rerankResults(query, fused, config, limit);
  } else {
    fused = fused.slice(0, limit);
  }
  return fused;
}
function getFact(id) {
  const db2 = getDatabase();
  const row = db2.query(`
    SELECT id, entity, key, value, category, decay_class as decayClass,
           importance, source, created_at as createdAt, expires_at as expiresAt,
           confidence, metadata
    FROM facts
    WHERE id = ?
  `).get(id);
  if (!row) return null;
  return {
    id: row.id,
    entity: row.entity,
    key: row.key,
    value: row.value,
    decay: row.decayClass,
    createdAt: new Date(row.createdAt * 1e3).toISOString(),
    updatedAt: new Date(row.createdAt * 1e3).toISOString(),
    tags: row.category ? [row.category] : void 0
  };
}
function deleteFact(id) {
  const db2 = getDatabase();
  const result = db2.run("DELETE FROM facts WHERE id = ?", [id]);
  if (result.changes > 0) invalidateGraphCache();
  return result.changes > 0;
}
function touchFact(id) {
  const db2 = getDatabase();
  const now = Math.floor(Date.now() / 1e3);
  db2.run("UPDATE facts SET last_accessed = ? WHERE id = ?", [now, id]);
}
function cleanupExpiredFacts() {
  const db2 = getDatabase();
  const result = db2.run(`
    DELETE FROM facts
    WHERE expires_at IS NOT NULL
      AND expires_at < strftime('%s', 'now')
  `);
  if (result.changes > 0) invalidateGraphCache();
  return result.changes;
}

// src/procedures.ts
function rowToProcedure(row) {
  return {
    id: row.id,
    name: row.name,
    version: row.version,
    steps: JSON.parse(row.steps),
    successCount: row.success_count,
    failureCount: row.failure_count,
    evolvedFrom: row.evolved_from || null,
    createdAt: row.created_at
  };
}
function successRate(proc) {
  const total = proc.successCount + proc.failureCount;
  if (total === 0) return "N/A (no runs)";
  return `${(proc.successCount / total * 100).toFixed(1)}% (${proc.successCount}/${total})`;
}
function searchProcedures(query, limit = 10) {
  const db2 = getDatabase();
  const rows = db2.prepare(
    `SELECT * FROM procedures WHERE name LIKE ? ORDER BY name, version DESC LIMIT ?`
  ).all(`%${query}%`, limit);
  return rows.map(rowToProcedure);
}
function getProcedure(name, version) {
  const db2 = getDatabase();
  const row = version ? db2.prepare("SELECT * FROM procedures WHERE name = ? AND version = ?").get(name, version) : db2.prepare("SELECT * FROM procedures WHERE name = ? ORDER BY version DESC LIMIT 1").get(name);
  if (!row) return null;
  return rowToProcedure(row);
}
function getProcedureVersions(name) {
  const db2 = getDatabase();
  const rows = db2.prepare(
    "SELECT * FROM procedures WHERE name = ? ORDER BY version DESC"
  ).all(name);
  return rows.map(rowToProcedure);
}
function compareProcedureVersions(name, fromVersion, toVersion) {
  const from = getProcedure(name, fromVersion);
  const to = getProcedure(name, toVersion);
  if (!from || !to) return null;
  const maxLen = Math.max(from.steps.length, to.steps.length);
  const stepsAdded = [];
  const stepsRemoved = [];
  const stepsChanged = [];
  for (let i = 0; i < maxLen; i++) {
    const a = from.steps[i];
    const b = to.steps[i];
    if (!a && b) {
      stepsAdded.push(b);
    } else if (a && !b) {
      stepsRemoved.push(a);
    } else if (a && b && JSON.stringify(a) !== JSON.stringify(b)) {
      stepsChanged.push({ step: i + 1, from: a, to: b });
    }
  }
  return {
    name,
    fromVersion,
    toVersion,
    stepsAdded,
    stepsRemoved,
    stepsChanged,
    successRateFrom: successRate(from),
    successRateTo: successRate(to)
  };
}
function getProcedureEpisodes(procedureName, limit = 20) {
  const db2 = getDatabase();
  const nowSec = Math.floor(Date.now() / 1e3);
  const rows = db2.prepare(`
    SELECT e.id, e.summary, e.outcome, e.happened_at
    FROM episodes e
    JOIN procedures p ON e.procedure_id = p.id
    WHERE p.name = ?
    ORDER BY e.happened_at DESC
    LIMIT ?
  `).all(procedureName, limit);
  return rows.map((r) => ({
    episodeId: r.id,
    summary: r.summary,
    outcome: r.outcome,
    happenedAt: r.happened_at,
    daysAgo: Math.round((nowSec - r.happened_at) / 86400)
  }));
}

// src/mcp-server.ts
var TOOLS = [
  {
    name: "memory_store",
    description: "Store a fact in memory with optional embedding generation",
    inputSchema: {
      type: "object",
      properties: {
        entity: { type: "string", description: "The entity this fact is about" },
        value: { type: "string", description: "The fact content" },
        key: { type: "string", description: "Optional key for the fact" },
        category: { type: "string", enum: ["preference", "fact", "decision", "convention", "other", "reference", "project"] },
        decay: { type: "string", enum: ["permanent", "long", "medium", "short"] },
        importance: { type: "number", description: "Importance score (default 1.0)" }
      },
      required: ["entity", "value"]
    }
  },
  {
    name: "memory_search",
    description: "Search facts by keyword or semantic similarity",
    inputSchema: {
      type: "object",
      properties: {
        query: { type: "string", description: "Search query" },
        entity: { type: "string", description: "Filter by entity" },
        category: { type: "string", description: "Filter by category" },
        limit: { type: "number", description: "Max results (default 10)" },
        mode: { type: "string", enum: ["keyword", "hybrid"], description: "Search mode: keyword (exact) or hybrid (RRF fusion)" }
      },
      required: ["query"]
    }
  },
  {
    name: "memory_episodes",
    description: "Search or create episodic memories",
    inputSchema: {
      type: "object",
      properties: {
        action: { type: "string", enum: ["search", "create", "entity"], description: "Action to perform" },
        summary: { type: "string", description: "Episode summary (for create)" },
        outcome: { type: "string", enum: ["success", "failure", "resolved", "ongoing"] },
        entities: { type: "array", items: { type: "string" }, description: "Related entities" },
        entity: { type: "string", description: "Entity to search episodes for (for entity action)" },
        since: { type: "string", description: "ISO date filter (for search)" },
        limit: { type: "number", description: "Max results" }
      },
      required: ["action"]
    }
  },
  {
    name: "cognitive_profile",
    description: "Get or update cognitive profiles for entities",
    inputSchema: {
      type: "object",
      properties: {
        action: { type: "string", enum: ["get", "update_traits", "update_preferences", "summary", "list"] },
        entity: { type: "string", description: "Entity name" },
        traits: { type: "object", description: "Traits to update (name \u2192 score)" },
        preferences: { type: "object", description: "Preferences to update (key \u2192 value)" }
      },
      required: ["action"]
    }
  },
  {
    name: "memory_graph",
    description: "Query the entity relationship graph",
    inputSchema: {
      type: "object",
      properties: {
        action: { type: "string", enum: ["related", "build"], description: "Graph action" },
        entity: { type: "string", description: "Entity to find relations for" },
        depth: { type: "number", description: "Traversal depth (default 2)" },
        limit: { type: "number", description: "Max related entities (default 20)" }
      },
      required: ["action"]
    }
  },
  {
    name: "memory_procedures",
    description: "Query stored procedures (workflow memory). Search, get specific versions, compare versions, or list linked episodes.",
    inputSchema: {
      type: "object",
      properties: {
        action: { type: "string", enum: ["search", "get", "versions", "compare", "episodes"], description: "Action: search by name, get specific, list versions, compare two versions, or get linked episodes" },
        name: { type: "string", description: "Procedure name (for get/versions/compare/episodes)" },
        query: { type: "string", description: "Search query (for search action)" },
        version: { type: "number", description: "Specific version (for get)" },
        fromVersion: { type: "number", description: "Version to compare from (for compare)" },
        toVersion: { type: "number", description: "Version to compare to (for compare)" },
        limit: { type: "number", description: "Max results (default 10)" }
      },
      required: ["action"]
    }
  },
  {
    name: "memory_stats",
    description: "Get memory system statistics",
    inputSchema: {
      type: "object",
      properties: {}
    }
  },
  {
    name: "memory_delete",
    description: "Delete a specific fact by ID. Cascades to embeddings.",
    inputSchema: {
      type: "object",
      properties: {
        id: { type: "string", description: "The fact UUID to delete" }
      },
      required: ["id"]
    }
  },
  {
    name: "memory_prune",
    description: "Garbage-collect expired facts. Returns count of deleted facts.",
    inputSchema: {
      type: "object",
      properties: {
        dry_run: { type: "boolean", description: "Preview what would be pruned without deleting (default false)" }
      }
    }
  }
];
async function handleToolCall(name, args, config) {
  switch (name) {
    case "memory_store": {
      const result = await storeFact({
        entity: args.entity,
        value: args.value,
        key: args.key,
        category: args.category,
        decay: args.decay,
        importance: args.importance,
        source: "mcp"
      }, config);
      return { stored: true, id: result.id, entity: result.entity };
    }
    case "memory_search": {
      const mode = args.mode ?? "keyword";
      if (mode === "hybrid") {
        return searchFactsHybrid(args.query, config, {
          limit: args.limit
        });
      }
      return searchFacts(args.query, {
        entity: args.entity,
        category: args.category,
        limit: args.limit
      });
    }
    case "memory_episodes": {
      const action = args.action;
      if (action === "create") {
        return createEpisode({
          summary: args.summary,
          outcome: args.outcome ?? "ongoing",
          entities: args.entities ?? ["system"]
        });
      }
      if (action === "entity") {
        return getEntityEpisodes(args.entity, {
          limit: args.limit
        });
      }
      return searchEpisodes({
        since: args.since,
        outcome: args.outcome,
        limit: args.limit
      });
    }
    case "cognitive_profile": {
      const action = args.action;
      if (action === "list") return listProfiles();
      if (action === "summary") return getProfileSummary(args.entity);
      if (action === "update_traits") {
        updateTraits(args.entity, args.traits);
        return { updated: true };
      }
      if (action === "update_preferences") {
        updatePreferences(args.entity, args.preferences);
        return { updated: true };
      }
      return getProfile(args.entity);
    }
    case "memory_graph": {
      const action = args.action;
      if (action === "build") return buildEntityGraph();
      return getRelatedEntities(args.entity, {
        depth: args.depth,
        limit: args.limit
      });
    }
    case "memory_procedures": {
      const action = args.action;
      if (action === "search") {
        return searchProcedures(args.query, args.limit);
      }
      if (action === "get") {
        return getProcedure(args.name, args.version);
      }
      if (action === "versions") {
        return getProcedureVersions(args.name);
      }
      if (action === "compare") {
        return compareProcedureVersions(
          args.name,
          args.fromVersion,
          args.toVersion
        );
      }
      if (action === "episodes") {
        return getProcedureEpisodes(args.name, args.limit);
      }
      throw new Error(`Unknown memory_procedures action: ${action}`);
    }
    case "memory_stats": {
      const dbStats = getDbStats(config);
      const epStats = getEpisodeStats();
      return { database: dbStats, episodes: epStats };
    }
    case "memory_delete": {
      const id = args.id;
      if (!id) throw new Error("id is required");
      const deleted = deleteFact(id);
      if (!deleted) throw new Error(`Fact not found: ${id}`);
      return { deleted: true, id };
    }
    case "memory_prune": {
      const dryRun = args.dry_run ?? false;
      if (dryRun) {
        const db2 = getDatabase();
        const rows = db2.query(
          "SELECT id FROM facts WHERE expires_at IS NOT NULL AND expires_at < strftime('%s', 'now')"
        ).all();
        return { dry_run: true, would_delete: rows.length, ids: rows.slice(0, 20).map((r) => r.id) };
      }
      const count = cleanupExpiredFacts();
      return { pruned: count };
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
}
function createResponse(id, result) {
  return { jsonrpc: "2.0", id, result };
}
function createError(id, code, message) {
  return { jsonrpc: "2.0", id, error: { code, message } };
}
async function handleMessage(message, config) {
  try {
    switch (message.method) {
      case "initialize":
        return createResponse(message.id, {
          protocolVersion: "2024-11-05",
          capabilities: { tools: {} },
          serverInfo: { name: "zouroboros-memory", version: "1.0.0" }
        });
      case "tools/list":
        return createResponse(message.id, { tools: TOOLS });
      case "tools/call": {
        const params = message.params;
        const result = await handleToolCall(params.name, params.arguments ?? {}, config);
        return createResponse(message.id, {
          content: [{ type: "text", text: JSON.stringify(result, null, 2) }]
        });
      }
      case "notifications/initialized":
        return createResponse(message.id, {});
      default:
        return createError(message.id, -32601, `Method not found: ${message.method}`);
    }
  } catch (err) {
    return createError(
      message.id,
      -32e3,
      err instanceof Error ? err.message : String(err)
    );
  }
}
async function startMcpServer(config) {
  initDatabase(config);
  ensureProfileSchema();
  const decoder = new TextDecoder();
  let buffer = "";
  process.stdin.resume();
  process.stdin.on("data", async (chunk) => {
    buffer += decoder.decode(chunk, { stream: true });
    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed) continue;
      try {
        const request = JSON.parse(trimmed);
        const response = await handleMessage(request, config);
        if (request.id !== void 0) {
          process.stdout.write(JSON.stringify(response) + "\n");
        }
      } catch {
      }
    }
  });
  process.on("SIGINT", () => {
    closeDatabase();
    process.exit(0);
  });
  process.on("SIGTERM", () => {
    closeDatabase();
    process.exit(0);
  });
}
if (process.argv[1] && new URL(import.meta.url).pathname === process.argv[1]) {
  const args = process.argv.slice(2);
  const dbPathIdx = args.indexOf("--db-path");
  const dbPath = dbPathIdx >= 0 ? args[dbPathIdx + 1] : void 0;
  const config = {
    enabled: true,
    dbPath: dbPath ?? `${process.env.HOME ?? "~"}/.zouroboros/memory.db`,
    vectorEnabled: false,
    ollamaUrl: "http://localhost:11434",
    ollamaModel: "nomic-embed-text",
    autoCapture: false,
    captureIntervalMinutes: 30,
    graphBoost: true,
    hydeExpansion: false,
    decayConfig: { permanent: Infinity, long: 365, medium: 90, short: 30 }
  };
  startMcpServer(config);
}

// src/index.ts
var VERSION = "1.0.0";
function init(config) {
  initDatabase(config);
  runMigrations(config);
  ensureProfileSchema();
}
function shutdown() {
  closeDatabase();
}
function getStats(config) {
  return {
    database: getDbStats(config),
    episodes: getEpisodeStats()
  };
}
export {
  VERSION,
  blendEmbeddings,
  buildEntityGraph,
  checkOllamaHealth,
  cleanupExpiredFacts,
  closeDatabase,
  compareProcedureVersions,
  cosineSimilarity,
  createEpisode,
  deleteFact,
  deleteProfile,
  deserializeEmbedding,
  ensureProfileSchema,
  extractQueryEntities,
  generateEmbedding,
  generateHyDEExpansion,
  generateHypotheticalAnswer,
  getDatabase,
  getDbStats,
  getEntityEpisodes,
  getEpisodeStats,
  getFact,
  getProcedure,
  getProcedureEpisodes,
  getProcedureVersions,
  getProfile,
  getProfileSummary,
  getRecentInteractions,
  getRelatedEntities,
  getStats,
  handleMessage,
  init,
  initDatabase,
  invalidateGraphCache,
  isInitialized,
  listAvailableModels,
  listProfiles,
  llmCall,
  recordInteraction,
  rerankResults,
  resetThrottleState,
  runMigrations,
  searchEpisodes,
  searchFacts,
  searchFactsGraphBoosted,
  searchFactsHybrid,
  searchFactsVector,
  searchProcedures,
  serializeEmbedding,
  shutdown,
  startMcpServer,
  storeFact,
  throttleMetrics,
  touchFact,
  updateEpisodeOutcome,
  updatePreferences,
  updateTraits
};
