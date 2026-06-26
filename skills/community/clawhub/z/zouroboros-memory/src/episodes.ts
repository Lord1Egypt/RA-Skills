/**
 * Episodic memory for event-based storage
 */

import { randomUUID } from 'crypto';
import { getDatabase } from './database.js';
import type { EpisodicMemory, TemporalQuery } from './types.js';

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
export function createEpisode(input: CreateEpisodeInput): EpisodicMemory {
  const db = getDatabase();
  const id = randomUUID();
  const happenedAt = input.happenedAt || new Date();

  db.run(
    `INSERT INTO episodes (id, summary, outcome, happened_at, duration_ms, procedure_id, metadata)
     VALUES (?, ?, ?, ?, ?, ?, ?)`,
    [
      id,
      input.summary,
      input.outcome,
      Math.floor(happenedAt.getTime() / 1000),
      input.durationMs || null,
      input.procedureId || null,
      input.metadata ? JSON.stringify(input.metadata) : null,
    ]
  );

  // Link entities
  for (const entity of input.entities) {
    db.run(
      'INSERT INTO episode_entities (episode_id, entity) VALUES (?, ?)',
      [id, entity]
    );
  }

  return {
    id,
    conversationId: id, // Using episode ID as conversation ID
    summary: input.summary,
    outcome: input.outcome,
    entities: input.entities,
    tags: [],
    createdAt: happenedAt.toISOString(),
  };
}

/**
 * Search episodes with temporal filters
 */
export function searchEpisodes(query: TemporalQuery): EpisodicMemory[] {
  const db = getDatabase();
  const nowSec = Math.floor(Date.now() / 1000);

  let sql = `
    SELECT e.id, e.summary, e.outcome, e.happened_at as happenedAt,
           e.duration_ms as durationMs, e.procedure_id as procedureId,
           e.metadata, e.created_at as createdAt,
           p.name as procedureName, p.version as procedureVersion
    FROM episodes e
    LEFT JOIN procedures p ON e.procedure_id = p.id
    WHERE 1=1
  `;
  const params: (string | number)[] = [];

  if (query.since) {
    sql += ' AND e.happened_at >= ?';
    params.push(Math.floor(new Date(query.since).getTime() / 1000));
  }

  if (query.until) {
    sql += ' AND e.happened_at <= ?';
    params.push(Math.floor(new Date(query.until).getTime() / 1000));
  }

  if (query.outcome) {
    sql += ' AND e.outcome = ?';
    params.push(query.outcome);
  }

  sql += ' ORDER BY e.happened_at DESC';

  if (query.limit) {
    sql += ' LIMIT ?';
    params.push(query.limit);
  }

  const rows = db.query(sql).all(...params) as Array<{
    id: string;
    summary: string;
    outcome: Outcome;
    happenedAt: number;
    durationMs: number | null;
    procedureId: string | null;
    metadata: string | null;
    createdAt: number;
    procedureName: string | null;
    procedureVersion: number | null;
  }>;

  // Get entities for each episode
  return rows.map(row => {
    const entityRows = db.query(
      'SELECT entity FROM episode_entities WHERE episode_id = ?'
    ).all(row.id) as { entity: string }[];

    const daysAgo = Math.round((nowSec - row.happenedAt) / 86400);

    return {
      id: row.id,
      conversationId: row.id,
      summary: row.summary,
      outcome: row.outcome,
      entities: entityRows.map(e => e.entity),
      tags: [],
      createdAt: new Date(row.createdAt * 1000).toISOString(),
      tokenCount: row.durationMs || undefined,
      // procedure linkage
      ...(row.procedureName && { procedureName: row.procedureName, procedureVersion: row.procedureVersion }),
      // temporal enrichment
      daysAgo,
    } as EpisodicMemory;
  });
}

/**
 * Get episodes for a specific entity
 */
export function getEntityEpisodes(
  entity: string,
  options: { limit?: number; outcome?: Outcome } = {}
): EpisodicMemory[] {
  const db = getDatabase();
  const { limit = 10, outcome } = options;

  const nowSec = Math.floor(Date.now() / 1000);

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
  const params: (string | number)[] = [entity];

  if (outcome) {
    sql += ' AND e.outcome = ?';
    params.push(outcome);
  }

  sql += ' ORDER BY e.happened_at DESC LIMIT ?';
  params.push(limit);

  const rows = db.query(sql).all(...params) as Array<{
    id: string;
    summary: string;
    outcome: Outcome;
    happenedAt: number;
    durationMs: number | null;
    procedureId: string | null;
    metadata: string | null;
    createdAt: number;
    procedureName: string | null;
    procedureVersion: number | null;
  }>;

  return rows.map(row => {
    const daysAgo = Math.round((nowSec - row.happenedAt) / 86400);
    return {
      id: row.id,
      conversationId: row.id,
      summary: row.summary,
      outcome: row.outcome,
      entities: [entity],
      tags: [],
      createdAt: new Date(row.createdAt * 1000).toISOString(),
      tokenCount: row.durationMs || undefined,
      ...(row.procedureName && { procedureName: row.procedureName, procedureVersion: row.procedureVersion }),
      daysAgo,
    } as EpisodicMemory;
  });
}

/**
 * Update episode outcome
 */
export function updateEpisodeOutcome(
  id: string,
  outcome: Outcome
): boolean {
  const db = getDatabase();
  const result = db.run(
    'UPDATE episodes SET outcome = ? WHERE id = ?',
    [outcome, id]
  );
  return result.changes > 0;
}

/**
 * Get episode statistics
 */
export function getEpisodeStats(): {
  total: number;
  byOutcome: Record<Outcome, number>;
} {
  const db = getDatabase();

  const total = (db.query('SELECT COUNT(*) as count FROM episodes').get() as { count: number }).count;

  const byOutcome: Record<Outcome, number> = {
    success: 0,
    failure: 0,
    resolved: 0,
    ongoing: 0,
  };

  const rows = db.query(
    'SELECT outcome, COUNT(*) as count FROM episodes GROUP BY outcome'
  ).all() as { outcome: Outcome; count: number }[];

  for (const row of rows) {
    byOutcome[row.outcome] = row.count;
  }

  return { total, byOutcome };
}
