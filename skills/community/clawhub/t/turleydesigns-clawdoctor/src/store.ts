import Database from 'better-sqlite3';
import { DB_PATH, ensureAgentwatchDir } from './config.js';

export type Severity = 'info' | 'warning' | 'error' | 'critical';

export interface Event {
  id?: number;
  timestamp: string;
  watcher: string;
  severity: Severity;
  event_type: string;
  message: string;
  details?: string;
  action_taken?: string;
  action_result?: string;
  created_at?: string;
}

export interface EventRow extends Required<Event> {
  id: number;
}

let _db: Database.Database | null = null;

function getDb(): Database.Database {
  if (!_db) {
    ensureAgentwatchDir();
    _db = new Database(DB_PATH);
    _db.pragma('journal_mode = WAL');
    initSchema(_db);
  }
  return _db;
}

function initSchema(db: Database.Database): void {
  db.exec(`
    CREATE TABLE IF NOT EXISTS events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      timestamp TEXT NOT NULL,
      watcher TEXT NOT NULL,
      severity TEXT NOT NULL,
      event_type TEXT NOT NULL,
      message TEXT NOT NULL,
      details TEXT,
      action_taken TEXT,
      action_result TEXT,
      created_at TEXT DEFAULT (datetime('now'))
    );
    CREATE INDEX IF NOT EXISTS idx_events_watcher ON events(watcher);
    CREATE INDEX IF NOT EXISTS idx_events_timestamp ON events(timestamp);
    CREATE INDEX IF NOT EXISTS idx_events_severity ON events(severity);

    CREATE TABLE IF NOT EXISTS alert_dedup (
      dedup_key TEXT PRIMARY KEY,
      last_sent_ms INTEGER NOT NULL
    );
  `);
}

/** Read a dedup timestamp from persistent storage. Returns 0 if not found. */
export function getDedupTimestamp(key: string): number {
  const db = getDb();
  const row = db.prepare('SELECT last_sent_ms FROM alert_dedup WHERE dedup_key = ?').get(key) as { last_sent_ms: number } | undefined;
  return row?.last_sent_ms ?? 0;
}

/** Write/update a dedup timestamp in persistent storage. */
export function setDedupTimestamp(key: string, tsMs: number): void {
  const db = getDb();
  db.prepare('INSERT OR REPLACE INTO alert_dedup (dedup_key, last_sent_ms) VALUES (?, ?)').run(key, tsMs);
}

/** Prune dedup entries older than maxAgeMs to keep the table small. */
export function pruneDedup(maxAgeMs: number): void {
  const db = getDb();
  const cutoff = Date.now() - maxAgeMs;
  db.prepare('DELETE FROM alert_dedup WHERE last_sent_ms < ?').run(cutoff);
}

export function insertEvent(event: Omit<Event, 'id' | 'created_at'>): number {
  const db = getDb();
  const stmt = db.prepare(`
    INSERT INTO events (timestamp, watcher, severity, event_type, message, details, action_taken, action_result)
    VALUES (@timestamp, @watcher, @severity, @event_type, @message, @details, @action_taken, @action_result)
  `);
  const result = stmt.run({
    timestamp: event.timestamp,
    watcher: event.watcher,
    severity: event.severity,
    event_type: event.event_type,
    message: event.message,
    details: event.details ?? null,
    action_taken: event.action_taken ?? null,
    action_result: event.action_result ?? null,
  });
  return result.lastInsertRowid as number;
}

export function getRecentEvents(limit = 50, watcher?: string, severity?: Severity): EventRow[] {
  const db = getDb();
  let query = 'SELECT * FROM events';
  const conditions: string[] = [];
  const params: Record<string, string | number> = { limit };

  if (watcher) {
    conditions.push('watcher = @watcher');
    params.watcher = watcher;
  }
  if (severity) {
    conditions.push('severity = @severity');
    params.severity = severity;
  }

  if (conditions.length > 0) {
    query += ' WHERE ' + conditions.join(' AND ');
  }
  query += ' ORDER BY id DESC LIMIT @limit';

  return db.prepare(query).all(params) as EventRow[];
}

export function pruneOldEvents(retentionDays: number): number {
  const db = getDb();
  const result = db.prepare(`
    DELETE FROM events WHERE created_at < datetime('now', '-' || ? || ' days')
  `).run(retentionDays);
  return result.changes;
}

export function closeDb(): void {
  if (_db) {
    _db.close();
    _db = null;
  }
}

export function getEventCount(): number {
  const db = getDb();
  const row = db.prepare('SELECT COUNT(*) as count FROM events').get() as { count: number };
  return row.count;
}
