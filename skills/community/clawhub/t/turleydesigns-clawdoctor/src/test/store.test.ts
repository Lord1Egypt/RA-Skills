import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'fs';
import path from 'path';
import os from 'os';
import Database from 'better-sqlite3';

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'clawdoctor-store-test-'));
const dbPath = path.join(tmpDir, 'events.db');

// Minimal in-process store test that doesn't rely on the module's global path
describe('EventStore (in-process)', () => {
  let db: Database.Database;

  before(() => {
    db = new Database(dbPath);
    db.pragma('journal_mode = WAL');
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
    `);
  });

  after(() => {
    db.close();
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('inserts an event', () => {
    const stmt = db.prepare(`
      INSERT INTO events (timestamp, watcher, severity, event_type, message)
      VALUES (?, ?, ?, ?, ?)
    `);
    const result = stmt.run(new Date().toISOString(), 'GatewayWatcher', 'critical', 'gateway_down', 'Gateway not found');
    assert.ok(result.lastInsertRowid > 0);
  });

  it('retrieves inserted events', () => {
    const rows = db.prepare('SELECT * FROM events ORDER BY id DESC').all();
    assert.ok(rows.length >= 1);
    const row = rows[0] as { watcher: string; severity: string; event_type: string };
    assert.equal(row.watcher, 'GatewayWatcher');
    assert.equal(row.severity, 'critical');
    assert.equal(row.event_type, 'gateway_down');
  });

  it('stores and retrieves JSON details', () => {
    const details = JSON.stringify({ pids: [1234, 5678], host: 'devbox' });
    db.prepare(`
      INSERT INTO events (timestamp, watcher, severity, event_type, message, details)
      VALUES (?, ?, ?, ?, ?, ?)
    `).run(new Date().toISOString(), 'CronWatcher', 'error', 'cron_error', 'Cron failed', details);

    const row = db.prepare(`SELECT * FROM events WHERE watcher = 'CronWatcher' LIMIT 1`).get() as { details: string };
    assert.ok(row);
    const parsed = JSON.parse(row.details) as { pids: number[]; host: string };
    assert.deepEqual(parsed.pids, [1234, 5678]);
    assert.equal(parsed.host, 'devbox');
  });

  it('prunes old events', () => {
    // Insert an old-looking event by overriding created_at
    db.prepare(`
      INSERT INTO events (timestamp, watcher, severity, event_type, message, created_at)
      VALUES (?, ?, ?, ?, ?, datetime('now', '-30 days'))
    `).run(new Date().toISOString(), 'TestWatcher', 'info', 'old_event', 'Old event');

    const before = (db.prepare('SELECT COUNT(*) as count FROM events').get() as { count: number }).count;

    const result = db.prepare(`
      DELETE FROM events WHERE created_at < datetime('now', '-' || ? || ' days')
    `).run(7);

    const after = (db.prepare('SELECT COUNT(*) as count FROM events').get() as { count: number }).count;

    assert.ok(result.changes >= 1);
    assert.ok(after < before);
  });

  it('filters events by watcher', () => {
    const rows = db.prepare(`SELECT * FROM events WHERE watcher = 'GatewayWatcher'`).all();
    assert.ok(rows.length >= 1);
    for (const row of rows as Array<{ watcher: string }>) {
      assert.equal(row.watcher, 'GatewayWatcher');
    }
  });
});
