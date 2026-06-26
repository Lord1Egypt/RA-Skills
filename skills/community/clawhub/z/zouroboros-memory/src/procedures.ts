/**
 * Procedure memory queries for MCP exposure.
 *
 * Provides search, get, compare_versions, and get_episodes
 * actions over the `procedures` table.
 */

import { getDatabase } from './database.js';

export interface ProcedureStep {
  executor: string;
  taskPattern: string;
  timeoutSeconds: number;
  fallbackExecutor?: string;
  notes?: string;
}

export interface Procedure {
  id: string;
  name: string;
  version: number;
  steps: ProcedureStep[];
  successCount: number;
  failureCount: number;
  evolvedFrom: string | null;
  createdAt: number;
}

export interface ProcedureEpisode {
  episodeId: string;
  summary: string;
  outcome: string;
  happenedAt: number;
  daysAgo: number;
}

export interface ProcedureComparison {
  name: string;
  fromVersion: number;
  toVersion: number;
  stepsAdded: ProcedureStep[];
  stepsRemoved: ProcedureStep[];
  stepsChanged: Array<{ step: number; from: ProcedureStep; to: ProcedureStep }>;
  successRateFrom: string;
  successRateTo: string;
}

function rowToProcedure(row: Record<string, unknown>): Procedure {
  return {
    id: row.id as string,
    name: row.name as string,
    version: row.version as number,
    steps: JSON.parse(row.steps as string) as ProcedureStep[],
    successCount: row.success_count as number,
    failureCount: row.failure_count as number,
    evolvedFrom: (row.evolved_from as string) || null,
    createdAt: row.created_at as number,
  };
}

function successRate(proc: Procedure): string {
  const total = proc.successCount + proc.failureCount;
  if (total === 0) return 'N/A (no runs)';
  return `${((proc.successCount / total) * 100).toFixed(1)}% (${proc.successCount}/${total})`;
}

/**
 * Search procedures by name pattern (FTS-like LIKE query).
 */
export function searchProcedures(query: string, limit = 10): Procedure[] {
  const db = getDatabase();
  const rows = db.prepare(
    `SELECT * FROM procedures WHERE name LIKE ? ORDER BY name, version DESC LIMIT ?`
  ).all(`%${query}%`, limit) as Array<Record<string, unknown>>;
  return rows.map(rowToProcedure);
}

/**
 * Get a specific procedure by name (latest version) or name + version.
 */
export function getProcedure(name: string, version?: number): Procedure | null {
  const db = getDatabase();
  const row = version
    ? db.prepare('SELECT * FROM procedures WHERE name = ? AND version = ?').get(name, version)
    : db.prepare('SELECT * FROM procedures WHERE name = ? ORDER BY version DESC LIMIT 1').get(name);
  if (!row) return null;
  return rowToProcedure(row as Record<string, unknown>);
}

/**
 * List all versions of a procedure.
 */
export function getProcedureVersions(name: string): Procedure[] {
  const db = getDatabase();
  const rows = db.prepare(
    'SELECT * FROM procedures WHERE name = ? ORDER BY version DESC'
  ).all(name) as Array<Record<string, unknown>>;
  return rows.map(rowToProcedure);
}

/**
 * Compare two versions of a procedure.
 */
export function compareProcedureVersions(
  name: string,
  fromVersion: number,
  toVersion: number,
): ProcedureComparison | null {
  const from = getProcedure(name, fromVersion);
  const to = getProcedure(name, toVersion);
  if (!from || !to) return null;

  const maxLen = Math.max(from.steps.length, to.steps.length);
  const stepsAdded: ProcedureStep[] = [];
  const stepsRemoved: ProcedureStep[] = [];
  const stepsChanged: ProcedureComparison['stepsChanged'] = [];

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
    successRateTo: successRate(to),
  };
}

/**
 * Get episodes linked to a procedure (via procedure_id FK on episodes table).
 */
export function getProcedureEpisodes(procedureName: string, limit = 20): ProcedureEpisode[] {
  const db = getDatabase();
  const nowSec = Math.floor(Date.now() / 1000);

  const rows = db.prepare(`
    SELECT e.id, e.summary, e.outcome, e.happened_at
    FROM episodes e
    JOIN procedures p ON e.procedure_id = p.id
    WHERE p.name = ?
    ORDER BY e.happened_at DESC
    LIMIT ?
  `).all(procedureName, limit) as Array<Record<string, unknown>>;

  return rows.map(r => ({
    episodeId: r.id as string,
    summary: r.summary as string,
    outcome: r.outcome as string,
    happenedAt: r.happened_at as number,
    daysAgo: Math.round((nowSec - (r.happened_at as number)) / 86400),
  }));
}
