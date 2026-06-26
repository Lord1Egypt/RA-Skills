/**
 * Cognitive profile tracking for entities (executors, users, subsystems).
 *
 * Tracks interaction patterns, performance traits, and preferences
 * to enable adaptive behavior over time.
 */

import { getDatabase } from './database.js';
import type { CognitiveProfile, InteractionRecord } from './types.js';

/**
 * Get or create a cognitive profile for an entity.
 */
export function getProfile(entity: string): CognitiveProfile {
  const db = getDatabase();
  const row = db.query(
    'SELECT entity, traits, preferences, interaction_count, last_interaction, created_at FROM cognitive_profiles WHERE entity = ?'
  ).get(entity) as {
    entity: string;
    traits: string | null;
    preferences: string | null;
    interaction_count: number;
    last_interaction: number | null;
    created_at: number;
  } | null;

  if (row) {
    return {
      entity: row.entity,
      traits: row.traits ? JSON.parse(row.traits) : {},
      preferences: row.preferences ? JSON.parse(row.preferences) : {},
      interactionHistory: getRecentInteractions(entity),
      lastUpdated: row.last_interaction
        ? new Date(row.last_interaction * 1000).toISOString()
        : new Date(row.created_at * 1000).toISOString(),
    };
  }

  // Auto-create on first access
  const now = Math.floor(Date.now() / 1000);
  db.run(
    'INSERT INTO cognitive_profiles (entity, traits, preferences, interaction_count, last_interaction) VALUES (?, ?, ?, 0, ?)',
    [entity, '{}', '{}', now]
  );

  return {
    entity,
    traits: {},
    preferences: {},
    interactionHistory: [],
    lastUpdated: new Date(now * 1000).toISOString(),
  };
}

/**
 * Update traits for an entity (merges with existing).
 */
export function updateTraits(
  entity: string,
  traits: Record<string, number>
): void {
  const db = getDatabase();
  const profile = getProfile(entity);
  const merged = { ...profile.traits, ...traits };
  const now = Math.floor(Date.now() / 1000);

  db.run(
    'UPDATE cognitive_profiles SET traits = ?, last_interaction = ? WHERE entity = ?',
    [JSON.stringify(merged), now, entity]
  );
}

/**
 * Update preferences for an entity (merges with existing).
 */
export function updatePreferences(
  entity: string,
  preferences: Record<string, string>
): void {
  const db = getDatabase();
  const profile = getProfile(entity);
  const merged = { ...profile.preferences, ...preferences };
  const now = Math.floor(Date.now() / 1000);

  db.run(
    'UPDATE cognitive_profiles SET preferences = ?, last_interaction = ? WHERE entity = ?',
    [JSON.stringify(merged), now, entity]
  );
}

/**
 * Record an interaction for tracking patterns.
 */
export function recordInteraction(
  entity: string,
  type: 'query' | 'store' | 'search',
  success: boolean,
  latencyMs: number
): void {
  const db = getDatabase();
  const now = Math.floor(Date.now() / 1000);

  // Ensure profile exists
  getProfile(entity);

  // Store in interactions table
  db.run(
    `INSERT INTO profile_interactions (entity, type, success, latency_ms, timestamp)
     VALUES (?, ?, ?, ?, ?)`,
    [entity, type, success ? 1 : 0, latencyMs, now]
  );

  // Update aggregate counts
  db.run(
    'UPDATE cognitive_profiles SET interaction_count = interaction_count + 1, last_interaction = ? WHERE entity = ?',
    [now, entity]
  );
}

/**
 * Get recent interactions for an entity.
 */
export function getRecentInteractions(
  entity: string,
  limit: number = 50
): InteractionRecord[] {
  const db = getDatabase();

  // Check if table exists (it's created by ensureProfileSchema)
  const tableExists = db.query(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='profile_interactions'"
  ).get();

  if (!tableExists) return [];

  const rows = db.query(
    'SELECT type, success, latency_ms, timestamp FROM profile_interactions WHERE entity = ? ORDER BY timestamp DESC LIMIT ?'
  ).all(entity, limit) as Array<{
    type: 'query' | 'store' | 'search';
    success: number;
    latency_ms: number;
    timestamp: number;
  }>;

  return rows.map(row => ({
    timestamp: new Date(row.timestamp * 1000).toISOString(),
    type: row.type,
    success: row.success === 1,
    latencyMs: row.latency_ms,
  }));
}

/**
 * Get performance summary for an entity.
 */
export function getProfileSummary(entity: string): {
  entity: string;
  totalInteractions: number;
  successRate: number;
  avgLatencyMs: number;
  traitCount: number;
  preferenceCount: number;
} {
  const db = getDatabase();
  const profile = getProfile(entity);

  const row = db.query(
    'SELECT interaction_count FROM cognitive_profiles WHERE entity = ?'
  ).get(entity) as { interaction_count: number } | null;

  const tableExists = db.query(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='profile_interactions'"
  ).get();

  let successRate = 0;
  let avgLatencyMs = 0;

  if (tableExists) {
    const stats = db.query(
      'SELECT AVG(CAST(success AS REAL)) as sr, AVG(latency_ms) as avg_lat FROM profile_interactions WHERE entity = ?'
    ).get(entity) as { sr: number | null; avg_lat: number | null } | null;

    successRate = stats?.sr ?? 0;
    avgLatencyMs = stats?.avg_lat ?? 0;
  }

  return {
    entity,
    totalInteractions: row?.interaction_count ?? 0,
    successRate,
    avgLatencyMs,
    traitCount: Object.keys(profile.traits).length,
    preferenceCount: Object.keys(profile.preferences).length,
  };
}

/**
 * List all known entities with profiles.
 */
export function listProfiles(): string[] {
  const db = getDatabase();
  const rows = db.query(
    'SELECT entity FROM cognitive_profiles ORDER BY last_interaction DESC'
  ).all() as { entity: string }[];
  return rows.map(r => r.entity);
}

/**
 * Delete a cognitive profile.
 */
export function deleteProfile(entity: string): boolean {
  const db = getDatabase();
  const result = db.run('DELETE FROM cognitive_profiles WHERE entity = ?', [entity]);

  // Clean up interactions if table exists
  const tableExists = db.query(
    "SELECT name FROM sqlite_master WHERE type='table' AND name='profile_interactions'"
  ).get();
  if (tableExists) {
    db.run('DELETE FROM profile_interactions WHERE entity = ?', [entity]);
  }

  return result.changes > 0;
}

/**
 * Ensure the profile_interactions table exists.
 * Called during memory system init.
 */
export function ensureProfileSchema(): void {
  const db = getDatabase();
  db.exec(`
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
