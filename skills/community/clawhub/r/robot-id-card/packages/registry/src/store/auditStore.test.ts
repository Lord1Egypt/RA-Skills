import { describe, it, expect, beforeEach } from 'vitest'
import Database from 'better-sqlite3'
import { nanoid } from 'nanoid'

function createTestDb() {
  const db = new Database(':memory:')
  db.pragma('foreign_keys = ON')
  db.exec(`
    CREATE TABLE bots (
      id TEXT PRIMARY KEY, ric_version TEXT NOT NULL DEFAULT '1.0',
      created_at TEXT NOT NULL, grade TEXT NOT NULL DEFAULT 'unknown',
      grade_updated_at TEXT NOT NULL, public_key TEXT NOT NULL, signature TEXT NOT NULL,
      dev_name TEXT NOT NULL, dev_email TEXT NOT NULL, dev_org TEXT,
      dev_website TEXT, dev_verified INTEGER NOT NULL DEFAULT 0,
      bot_name TEXT NOT NULL, bot_version TEXT NOT NULL, bot_purpose TEXT NOT NULL,
      bot_capabilities TEXT NOT NULL, bot_user_agent TEXT NOT NULL,
      last_claim_date TEXT, consecutive_days INTEGER NOT NULL DEFAULT 0,
      total_claims INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE audit_log (
      id TEXT PRIMARY KEY, ric_id TEXT NOT NULL, event TEXT NOT NULL,
      old_grade TEXT, new_grade TEXT, reason TEXT, reporter TEXT,
      description TEXT, timestamp TEXT NOT NULL,
      FOREIGN KEY (ric_id) REFERENCES bots(id)
    );
  `)
  return db
}

function makeAuditStore(db: ReturnType<typeof createTestDb>) {
  const insert = db.prepare(`
    INSERT INTO audit_log (id, ric_id, event, old_grade, new_grade, reason, reporter, description, timestamp)
    VALUES (@id, @ric_id, @event, @old_grade, @new_grade, @reason, @reporter, @description, @timestamp)
  `)
  const findByRicId = db.prepare(`SELECT * FROM audit_log WHERE ric_id = ? ORDER BY timestamp DESC`)
  const countRecent = db.prepare(`
    SELECT COUNT(*) as cnt FROM audit_log
    WHERE ric_id = ? AND event = 'violation_report'
    AND timestamp > datetime('now', '-24 hours')
  `)

  return {
    insertBot(id: string) {
      db.prepare(`INSERT INTO bots (id, created_at, grade, grade_updated_at, public_key, signature,
        dev_name, dev_email, dev_org, dev_website, dev_verified, bot_name, bot_version,
        bot_purpose, bot_capabilities, bot_user_agent)
        VALUES (?, ?, 'unknown', ?, 'ed25519:aa', 'sig', 'Dev', 'dev@test.com',
        null, null, 0, 'Bot', '1.0.0', 'Testing purposes only', '[]', 'Bot/1.0')`)
        .run(id, new Date().toISOString(), new Date().toISOString())
    },
    append(entry: { ric_id: string; event: string; old_grade?: string; new_grade?: string; reason?: string; reporter?: string; description?: string }) {
      const now = new Date().toISOString()
      const id = nanoid()
      insert.run({ id, timestamp: now, old_grade: null, new_grade: null, reason: null, reporter: null, description: null, ...entry })
      return { id, timestamp: now }
    },
    findByRicId(id: string) {
      return findByRicId.all(id) as any[]
    },
    countRecentReports(id: string) {
      return (countRecent.get(id) as { cnt: number }).cnt
    },
  }
}

describe('auditStore — append and query', () => {
  let store: ReturnType<typeof makeAuditStore>

  beforeEach(() => {
    store = makeAuditStore(createTestDb())
    store.insertBot('ric_audit_001')
  })

  it('appends a registration event', () => {
    store.append({ ric_id: 'ric_audit_001', event: 'registered', reason: 'New bot' })
    const events = store.findByRicId('ric_audit_001')
    expect(events).toHaveLength(1)
    expect(events[0].event).toBe('registered')
  })

  it('appends multiple events and returns them all', () => {
    store.append({ ric_id: 'ric_audit_001', event: 'registered' })
    store.append({ ric_id: 'ric_audit_001', event: 'identity_claimed', reason: 'Day 1' })
    store.append({ ric_id: 'ric_audit_001', event: 'grade_changed', old_grade: 'unknown', new_grade: 'healthy' })
    const events = store.findByRicId('ric_audit_001')
    expect(events).toHaveLength(3)
  })

  it('findByRicId returns empty array for unknown bot', () => {
    const events = store.findByRicId('ric_does_not_exist')
    expect(events).toHaveLength(0)
  })

  it('appends violation_report with reporter and description', () => {
    store.append({
      ric_id: 'ric_audit_001',
      event: 'violation_report',
      reason: 'spam',
      reporter: 'example.com',
      description: 'Repeated spam posts',
    })
    const events = store.findByRicId('ric_audit_001')
    expect(events[0].reporter).toBe('example.com')
    expect(events[0].description).toBe('Repeated spam posts')
  })

  it('countRecentReports returns 0 with no reports', () => {
    expect(store.countRecentReports('ric_audit_001')).toBe(0)
  })

  it('countRecentReports counts only violation_report events', () => {
    store.append({ ric_id: 'ric_audit_001', event: 'violation_report', reason: 'spam' })
    store.append({ ric_id: 'ric_audit_001', event: 'violation_report', reason: 'scraping' })
    store.append({ ric_id: 'ric_audit_001', event: 'grade_changed', old_grade: 'unknown', new_grade: 'dangerous' })
    expect(store.countRecentReports('ric_audit_001')).toBe(2)
  })

  it('append returns an id and timestamp', () => {
    const result = store.append({ ric_id: 'ric_audit_001', event: 'registered' })
    expect(result.id).toBeTruthy()
    expect(result.timestamp).toMatch(/^\d{4}-\d{2}-\d{2}/)
  })
})
