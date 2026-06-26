import { db } from './db.js'
import type { RICCertificate } from '../models/certificate.js'

// ── Row ↔ Certificate conversion ─────────────────────────

function rowToCert(row: any): RICCertificate {
  return {
    ric_version: '1.0',
    id: row.id,
    created_at: row.created_at,
    grade: row.grade,
    grade_updated_at: row.grade_updated_at,
    public_key: row.public_key,
    signature: row.signature,
    developer: {
      name: row.dev_name,
      email: row.dev_email,
      org: row.dev_org ?? undefined,
      website: row.dev_website ?? undefined,
      verified: row.dev_verified === 1,
    },
    bot: {
      name: row.bot_name,
      version: row.bot_version,
      purpose: row.bot_purpose,
      capabilities: JSON.parse(row.bot_capabilities),
      user_agent: row.bot_user_agent,
    },
  }
}

const DAILY_CLAIM_LIMIT = 2
const CONSECUTIVE_UPGRADE_THRESHOLD = 3

const stmts = {
  insert: db.prepare(`
    INSERT INTO bots (
      id, created_at, grade, grade_updated_at, public_key, signature,
      dev_name, dev_email, dev_org, dev_website, dev_verified,
      bot_name, bot_version, bot_purpose, bot_capabilities, bot_user_agent
    ) VALUES (
      @id, @created_at, @grade, @grade_updated_at, @public_key, @signature,
      @dev_name, @dev_email, @dev_org, @dev_website, @dev_verified,
      @bot_name, @bot_version, @bot_purpose, @bot_capabilities, @bot_user_agent
    )
  `),

  findById: db.prepare(`SELECT * FROM bots WHERE id = ?`),
  findByPublicKey: db.prepare(`SELECT id FROM bots WHERE public_key = ?`),
  findByEmailAndBotName: db.prepare(`
    SELECT id FROM bots WHERE dev_email = ? AND bot_name = ?
  `),
  listSummary: db.prepare(`
    SELECT id, bot_name, bot_purpose, grade, dev_name, dev_org, created_at
    FROM bots ORDER BY created_at DESC
  `),
  updateGrade: db.prepare(`
    UPDATE bots SET grade = @grade, grade_updated_at = @grade_updated_at WHERE id = @id
  `),
  countRecentReports: db.prepare(`
    SELECT COUNT(*) as cnt FROM audit_log
    WHERE ric_id = ? AND event = 'violation_report'
    AND timestamp > datetime('now', '-24 hours')
  `),

  // RFC 9421 nonce statements
  insertNonce: db.prepare(`
    INSERT OR IGNORE INTO used_nonces (nonce, ric_id, used_at) VALUES (?, ?, ?)
  `),
  nonceExists: db.prepare(`SELECT 1 FROM used_nonces WHERE nonce = ?`),
  sweepNonces: db.prepare(`DELETE FROM used_nonces WHERE used_at < ?`),

  // Claim statements
  countTodayClaims: db.prepare(`
    SELECT COUNT(*) as cnt FROM claims
    WHERE ric_id = ? AND claim_date = ?
  `),
  insertClaim: db.prepare(`
    INSERT INTO claims (ric_id, claim_date, claimed_at, consecutive_after)
    VALUES (@ric_id, @claim_date, @claimed_at, @consecutive_after)
  `),
  getClaimMeta: db.prepare(`
    SELECT last_claim_date, consecutive_days, total_claims FROM bots WHERE id = ?
  `),
  updateClaimMeta: db.prepare(`
    UPDATE bots
    SET last_claim_date = @last_claim_date,
        consecutive_days = @consecutive_days,
        total_claims = total_claims + 1
    WHERE id = @id
  `),
}

export const botStore = {
  findByPublicKey(publicKey: string): string | null {
    const row = stmts.findByPublicKey.get(publicKey) as { id: string } | undefined
    return row?.id ?? null
  },

  findByEmailAndBotName(email: string, botName: string): string | null {
    const row = stmts.findByEmailAndBotName.get(email, botName) as { id: string } | undefined
    return row?.id ?? null
  },

  insert(cert: RICCertificate): void {
    stmts.insert.run({
      id: cert.id,
      created_at: cert.created_at,
      grade: cert.grade,
      grade_updated_at: cert.grade_updated_at,
      public_key: cert.public_key,
      signature: cert.signature,
      dev_name: cert.developer.name,
      dev_email: cert.developer.email,
      dev_org: cert.developer.org ?? null,
      dev_website: cert.developer.website ?? null,
      dev_verified: cert.developer.verified ? 1 : 0,
      bot_name: cert.bot.name,
      bot_version: cert.bot.version,
      bot_purpose: cert.bot.purpose,
      bot_capabilities: JSON.stringify(cert.bot.capabilities),
      bot_user_agent: cert.bot.user_agent,
    })
  },

  findById(id: string): RICCertificate | null {
    const row = stmts.findById.get(id)
    return row ? rowToCert(row) : null
  },

  listSummary() {
    return (stmts.listSummary.all() as any[]).map((row) => ({
      id: row.id,
      name: row.bot_name,
      purpose: row.bot_purpose,
      grade: row.grade,
      developer_org: row.dev_org || row.dev_name,
      created_at: row.created_at,
    }))
  },

  updateGrade(id: string, grade: string): void {
    stmts.updateGrade.run({ id, grade, grade_updated_at: new Date().toISOString() })
  },

  countRecentReports(id: string): number {
    const row = stmts.countRecentReports.get(id) as { cnt: number }
    return row.cnt
  },

  /**
   * RFC 9421 nonce uniqueness check.
   * Returns true if the nonce is fresh (never seen).
   * Marks it as used and sweeps nonces older than 10 minutes.
   */
  checkAndMarkNonce(nonce: string, ricId: string, createdSec: number): boolean {
    const existing = stmts.nonceExists.get(nonce)
    if (existing) return false
    stmts.insertNonce.run(nonce, ricId, createdSec)
    // Sweep nonces older than 10 minutes
    stmts.sweepNonces.run(createdSec - 600)
    return true
  },

  /**
   * Attempt a daily claim for a bot.
   *
   * Rules:
   *   - Max DAILY_CLAIM_LIMIT (2) claims per calendar day
   *   - Tracks consecutive daily streak
   *   - After CONSECUTIVE_UPGRADE_THRESHOLD (3) consecutive days → grade unknown→healthy
   *
   * Returns the result of the claim or an error code.
   */
  recordClaim(id: string): {
    ok: boolean
    error?: 'DAILY_LIMIT_REACHED' | 'NOT_FOUND'
    today_count?: number
    consecutive_days?: number
    grade_upgraded?: boolean
    new_grade?: string
  } {
    const meta = stmts.getClaimMeta.get(id) as {
      last_claim_date: string | null
      consecutive_days: number
      total_claims: number
    } | undefined

    if (!meta) return { ok: false, error: 'NOT_FOUND' }

    const today = new Date().toISOString().slice(0, 10)

    // Check daily limit
    const todayCount = (stmts.countTodayClaims.get(id, today) as { cnt: number }).cnt
    if (todayCount >= DAILY_CLAIM_LIMIT) {
      return { ok: false, error: 'DAILY_LIMIT_REACHED', today_count: todayCount }
    }

    // Compute new consecutive streak
    const yesterday = new Date(Date.now() - 86_400_000).toISOString().slice(0, 10)
    let newConsecutive: number
    if (meta.last_claim_date === today) {
      // Second claim on same day — streak unchanged
      newConsecutive = meta.consecutive_days
    } else if (meta.last_claim_date === yesterday) {
      // Claimed yesterday → extend streak
      newConsecutive = meta.consecutive_days + 1
    } else {
      // Gap or first ever claim → reset streak to 1
      newConsecutive = 1
    }

    const now = new Date().toISOString()

    // Persist claim record
    stmts.insertClaim.run({
      ric_id: id,
      claim_date: today,
      claimed_at: now,
      consecutive_after: newConsecutive,
    })

    // Update bot meta (only update last_claim_date if this is first claim today)
    stmts.updateClaimMeta.run({
      id,
      last_claim_date: today,
      consecutive_days: newConsecutive,
    })

    // Grade upgrade: unknown → healthy after N consecutive days
    let gradeUpgraded = false
    let newGrade: string | undefined
    if (newConsecutive >= CONSECUTIVE_UPGRADE_THRESHOLD) {
      const cert = stmts.findById.get(id) as any
      if (cert && cert.grade === 'unknown') {
        stmts.updateGrade.run({ id, grade: 'healthy', grade_updated_at: now })
        gradeUpgraded = true
        newGrade = 'healthy'
      }
    }

    return {
      ok: true,
      today_count: todayCount + 1,
      consecutive_days: newConsecutive,
      grade_upgraded: gradeUpgraded,
      new_grade: newGrade,
    }
  },
}
