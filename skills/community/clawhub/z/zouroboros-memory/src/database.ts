/**
 * Database management for Zouroboros Memory
 */

import { Database } from './compat/sqlite.js';
import { existsSync, mkdirSync } from 'fs';
import { dirname } from 'path';
import type { MemoryConfig } from './types.js';

export { Database };

let db: Database | null = null;

const SCHEMA_SQL = `
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

export function initDatabase(config: MemoryConfig): Database {
  if (db) return db;

  const dir = dirname(config.dbPath);
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }

  db = new Database(config.dbPath);
  db.exec('PRAGMA journal_mode = WAL');
  db.exec(SCHEMA_SQL);

  return db;
}

export function getDatabase(): Database {
  if (!db) {
    throw new Error('Database not initialized. Call initDatabase first.');
  }
  return db;
}

export function closeDatabase(): void {
  if (db) {
    db.close();
    db = null;
  }
}

export function isInitialized(): boolean {
  return db !== null;
}

export function runMigrations(config: MemoryConfig): void {
  const database = initDatabase(config);

  database.exec(`
    CREATE TABLE IF NOT EXISTS _migrations (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      applied_at INTEGER DEFAULT (strftime('%s', 'now'))
    );
  `);

  const applied = database.query('SELECT name FROM _migrations').all() as { name: string }[];
  const appliedSet = new Set(applied.map((m) => m.name));

  const migrations: { name: string; sql: string }[] = [
    {
      name: '001_ensure_facts_persona_column',
      sql: `CREATE INDEX IF NOT EXISTS idx_facts_persona ON facts(persona);`,
    },
    {
      name: '002_backfill_facts_persona_shared',
      sql: `UPDATE facts SET persona = 'shared' WHERE persona IS NULL;`,
    },
  ];

  for (const migration of migrations) {
    if (!appliedSet.has(migration.name)) {
      database.exec(migration.sql);
      database.run('INSERT INTO _migrations (name) VALUES (?)', [migration.name]);
    }
  }
}

export function getDbStats(config: MemoryConfig): {
  facts: number;
  episodes: number;
  procedures: number;
  openLoops: number;
  embeddings: number;
} {
  const database = initDatabase(config);

  return {
    facts: (database.query('SELECT COUNT(*) as count FROM facts').get() as { count: number }).count,
    episodes: (database.query('SELECT COUNT(*) as count FROM episodes').get() as { count: number }).count,
    procedures: (database.query('SELECT COUNT(*) as count FROM procedures').get() as { count: number }).count,
    openLoops: (database.query('SELECT COUNT(*) as count FROM open_loops').get() as { count: number }).count,
    embeddings: (database.query('SELECT COUNT(*) as count FROM fact_embeddings').get() as { count: number }).count,
  };
}
