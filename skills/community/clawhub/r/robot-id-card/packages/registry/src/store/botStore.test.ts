import { describe, it, expect, beforeEach } from 'vitest'
import Database from 'better-sqlite3'

// ── Inline in-memory store for testing ─────────────────────────────────────
// We replicate the store logic with a :memory: DB so tests are hermetic.

function createTestDb() {
  const db = new Database(':memory:')
  db.pragma('journal_mode = WAL')
  db.pragma('foreign_keys = ON')
  db.exec(`
    CREATE TABLE IF NOT EXISTS bots (
      id TEXT PRIMARY KEY,
      ric_version TEXT NOT NULL DEFAULT '1.0',
      created_at TEXT NOT NULL,
      grade TEXT NOT NULL DEFAULT 'unknown',
      grade_updated_at TEXT NOT NULL,
      public_key TEXT NOT NULL,
      signature TEXT NOT NULL,
      dev_name TEXT NOT NULL, dev_email TEXT NOT NULL,
      dev_org TEXT, dev_website TEXT, dev_verified INTEGER NOT NULL DEFAULT 0,
      bot_name TEXT NOT NULL, bot_version TEXT NOT NULL,
      bot_purpose TEXT NOT NULL, bot_capabilities TEXT NOT NULL,
      bot_user_agent TEXT NOT NULL,
      last_claim_date TEXT,
      consecutive_days INTEGER NOT NULL DEFAULT 0,
      total_claims INTEGER NOT NULL DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS audit_log (
      id TEXT PRIMARY KEY, ric_id TEXT NOT NULL, event TEXT NOT NULL,
      old_grade TEXT, new_grade TEXT, reason TEXT, reporter TEXT,
      description TEXT, timestamp TEXT NOT NULL,
      FOREIGN KEY (ric_id) REFERENCES bots(id)
    );
    CREATE TABLE IF NOT EXISTS claims (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      ric_id TEXT NOT NULL, claim_date TEXT NOT NULL,
      claimed_at TEXT NOT NULL, consecutive_after INTEGER NOT NULL DEFAULT 0,
      FOREIGN KEY (ric_id) REFERENCES bots(id)
    );
  `)
  return db
}

function makeStore(db: ReturnType<typeof createTestDb>) {
  const DAILY_CLAIM_LIMIT = 2
  const CONSECUTIVE_UPGRADE_THRESHOLD = 3

  const stmts = {
    insert: db.prepare(`
      INSERT INTO bots (id, created_at, grade, grade_updated_at, public_key, signature,
        dev_name, dev_email, dev_org, dev_website, dev_verified,
        bot_name, bot_version, bot_purpose, bot_capabilities, bot_user_agent)
      VALUES (@id, @created_at, @grade, @grade_updated_at, @public_key, @signature,
        @dev_name, @dev_email, @dev_org, @dev_website, @dev_verified,
        @bot_name, @bot_version, @bot_purpose, @bot_capabilities, @bot_user_agent)
    `),
    findById: db.prepare(`SELECT * FROM bots WHERE id = ?`),
    findByPublicKey: db.prepare(`SELECT id FROM bots WHERE public_key = ?`),
    findByEmailAndBotName: db.prepare(`SELECT id FROM bots WHERE dev_email = ? AND bot_name = ?`),
    updateGrade: db.prepare(`UPDATE bots SET grade = @grade, grade_updated_at = @grade_updated_at WHERE id = @id`),
    countTodayClaims: db.prepare(`SELECT COUNT(*) as cnt FROM claims WHERE ric_id = ? AND claim_date = ?`),
    insertClaim: db.prepare(`INSERT INTO claims (ric_id, claim_date, claimed_at, consecutive_after) VALUES (@ric_id, @claim_date, @claimed_at, @consecutive_after)`),
    getClaimMeta: db.prepare(`SELECT last_claim_date, consecutive_days, total_claims FROM bots WHERE id = ?`),
    updateClaimMeta: db.prepare(`UPDATE bots SET last_claim_date = @last_claim_date, consecutive_days = @consecutive_days, total_claims = total_claims + 1 WHERE id = @id`),
    countRecentReports: db.prepare(`SELECT COUNT(*) as cnt FROM audit_log WHERE ric_id = ? AND event = 'violation_report' AND timestamp > datetime('now', '-24 hours')`),
    listSummary: db.prepare(`SELECT id, bot_name, bot_purpose, grade, dev_name, dev_org, created_at FROM bots ORDER BY created_at DESC`),
  }

  return {
    insertBot(id: string, pubKey: string, grade = 'unknown') {
      stmts.insert.run({
        id, created_at: new Date().toISOString(), grade,
        grade_updated_at: new Date().toISOString(),
        public_key: pubKey, signature: 'sig',
        dev_name: 'Test Dev', dev_email: 'dev@test.com',
        dev_org: null, dev_website: null, dev_verified: 0,
        bot_name: `Bot-${id}`, bot_version: '1.0.0',
        bot_purpose: 'Testing purposes only',
        bot_capabilities: JSON.stringify(['read_articles']),
        bot_user_agent: 'TestBot/1.0',
      })
    },
    findByPublicKey(pk: string) {
      const row = stmts.findByPublicKey.get(pk) as { id: string } | undefined
      return row?.id ?? null
    },
    findByEmailAndBotName(email: string, name: string) {
      const row = stmts.findByEmailAndBotName.get(email, name) as { id: string } | undefined
      return row?.id ?? null
    },
    findById(id: string) {
      return stmts.findById.get(id) as any | null
    },
    updateGrade(id: string, grade: string) {
      stmts.updateGrade.run({ id, grade, grade_updated_at: new Date().toISOString() })
    },
    recordClaim(id: string, overrideToday?: string) {
      const meta = stmts.getClaimMeta.get(id) as any
      if (!meta) return { ok: false, error: 'NOT_FOUND' }

      const today = overrideToday ?? new Date().toISOString().slice(0, 10)
      const todayCount = (stmts.countTodayClaims.get(id, today) as { cnt: number }).cnt
      if (todayCount >= DAILY_CLAIM_LIMIT) {
        return { ok: false, error: 'DAILY_LIMIT_REACHED', today_count: todayCount }
      }

      const baseDate = overrideToday ? new Date(overrideToday).getTime() : Date.now()
      const yesterday = new Date(baseDate - 86_400_000).toISOString().slice(0, 10)
      let newConsecutive: number
      if (meta.last_claim_date === today) {
        newConsecutive = meta.consecutive_days
      } else if (meta.last_claim_date === yesterday) {
        newConsecutive = meta.consecutive_days + 1
      } else {
        newConsecutive = 1
      }

      const now = new Date().toISOString()
      stmts.insertClaim.run({ ric_id: id, claim_date: today, claimed_at: now, consecutive_after: newConsecutive })
      stmts.updateClaimMeta.run({ id, last_claim_date: today, consecutive_days: newConsecutive })

      let gradeUpgraded = false
      let newGrade: string | undefined
      if (newConsecutive >= CONSECUTIVE_UPGRADE_THRESHOLD) {
        const cert = stmts.findById.get(id) as any
        if (cert?.grade === 'unknown') {
          stmts.updateGrade.run({ id, grade: 'healthy', grade_updated_at: now })
          gradeUpgraded = true
          newGrade = 'healthy'
        }
      }

      return { ok: true, today_count: todayCount + 1, consecutive_days: newConsecutive, grade_upgraded: gradeUpgraded, new_grade: newGrade }
    },
    countRecentReports(id: string) {
      return (stmts.countRecentReports.get(id) as { cnt: number }).cnt
    },
  }
}

// ── Tests ────────────────────────────────────────────────────────────────────

describe('botStore — uniqueness checks', () => {
  let store: ReturnType<typeof makeStore>

  beforeEach(() => {
    store = makeStore(createTestDb())
  })

  it('findByPublicKey returns null when no bot registered', () => {
    expect(store.findByPublicKey('ed25519:aabbccdd')).toBeNull()
  })

  it('findByPublicKey finds a registered bot', () => {
    store.insertBot('ric_test_001', 'ed25519:aabbccdd')
    expect(store.findByPublicKey('ed25519:aabbccdd')).toBe('ric_test_001')
  })

  it('findByEmailAndBotName returns null when no match', () => {
    expect(store.findByEmailAndBotName('dev@test.com', 'Bot-ric_test_001')).toBeNull()
  })

  it('findByEmailAndBotName finds after insert', () => {
    store.insertBot('ric_test_002', 'ed25519:deadbeef')
    expect(store.findByEmailAndBotName('dev@test.com', 'Bot-ric_test_002')).toBe('ric_test_002')
  })
})

describe('botStore — recordClaim: daily limits', () => {
  let store: ReturnType<typeof makeStore>

  beforeEach(() => {
    store = makeStore(createTestDb())
    store.insertBot('ric_bot_1', 'ed25519:11111111')
  })

  it('first claim succeeds', () => {
    const result = store.recordClaim('ric_bot_1')
    expect(result.ok).toBe(true)
    expect(result.today_count).toBe(1)
  })

  it('second claim on same day succeeds', () => {
    store.recordClaim('ric_bot_1')
    const result = store.recordClaim('ric_bot_1')
    expect(result.ok).toBe(true)
    expect(result.today_count).toBe(2)
  })

  it('third claim on same day is rejected with DAILY_LIMIT_REACHED', () => {
    store.recordClaim('ric_bot_1')
    store.recordClaim('ric_bot_1')
    const result = store.recordClaim('ric_bot_1')
    expect(result.ok).toBe(false)
    expect(result.error).toBe('DAILY_LIMIT_REACHED')
    expect(result.today_count).toBe(2)
  })

  it('returns NOT_FOUND for unknown bot', () => {
    const result = store.recordClaim('ric_does_not_exist')
    expect(result.ok).toBe(false)
    expect(result.error).toBe('NOT_FOUND')
  })
})

describe('botStore — recordClaim: streak and grade upgrade', () => {
  let store: ReturnType<typeof makeStore>

  beforeEach(() => {
    store = makeStore(createTestDb())
    store.insertBot('ric_streak', 'ed25519:22222222', 'unknown')
  })

  it('first ever claim sets consecutive_days to 1', () => {
    const result = store.recordClaim('ric_streak')
    expect(result.consecutive_days).toBe(1)
  })

  it('does NOT upgrade grade after 1 day', () => {
    const result = store.recordClaim('ric_streak')
    expect(result.grade_upgraded).toBe(false)
  })

  it('upgrades grade unknown→healthy after 3 consecutive days', () => {
    const today = new Date()
    // day 1
    const d1 = new Date(today); d1.setDate(today.getDate() - 2)
    store.recordClaim('ric_streak', d1.toISOString().slice(0, 10))
    // day 2
    const d2 = new Date(today); d2.setDate(today.getDate() - 1)
    store.recordClaim('ric_streak', d2.toISOString().slice(0, 10))
    // day 3 (today)
    const result = store.recordClaim('ric_streak', today.toISOString().slice(0, 10))
    expect(result.ok).toBe(true)
    expect(result.consecutive_days).toBe(3)
    expect(result.grade_upgraded).toBe(true)
    expect(result.new_grade).toBe('healthy')
  })

  it('does NOT re-upgrade a healthy bot', () => {
    store.updateGrade('ric_streak', 'healthy')
    // fast-forward 3 days
    const today = new Date()
    const d1 = new Date(today); d1.setDate(today.getDate() - 2)
    store.recordClaim('ric_streak', d1.toISOString().slice(0, 10))
    const d2 = new Date(today); d2.setDate(today.getDate() - 1)
    store.recordClaim('ric_streak', d2.toISOString().slice(0, 10))
    const result = store.recordClaim('ric_streak', today.toISOString().slice(0, 10))
    expect(result.grade_upgraded).toBe(false)
  })

  it('resets streak on gap day', () => {
    const d1 = new Date(); d1.setDate(d1.getDate() - 5) // 5 days ago
    store.recordClaim('ric_streak', d1.toISOString().slice(0, 10))
    // skip 4 days, claim today
    const result = store.recordClaim('ric_streak', new Date().toISOString().slice(0, 10))
    expect(result.consecutive_days).toBe(1)
  })
})

describe('botStore — updateGrade', () => {
  let store: ReturnType<typeof makeStore>

  beforeEach(() => {
    store = makeStore(createTestDb())
    store.insertBot('ric_grade', 'ed25519:33333333', 'unknown')
  })

  it('updates grade to dangerous', () => {
    store.updateGrade('ric_grade', 'dangerous')
    const bot = store.findById('ric_grade')
    expect(bot.grade).toBe('dangerous')
  })

  it('updates grade back to healthy', () => {
    store.updateGrade('ric_grade', 'dangerous')
    store.updateGrade('ric_grade', 'healthy')
    const bot = store.findById('ric_grade')
    expect(bot.grade).toBe('healthy')
  })
})
