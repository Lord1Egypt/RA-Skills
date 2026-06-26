import Database, { type Database as DatabaseType } from 'better-sqlite3'
import path from 'path'
import { fileURLToPath } from 'url'
import { mkdirSync } from 'fs'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const DB_PATH = process.env.RIC_DB_PATH || path.join(__dirname, '../../data/registry.db')

mkdirSync(path.dirname(DB_PATH), { recursive: true })

export const db: DatabaseType = new Database(DB_PATH)

// Enable WAL mode for better concurrent read performance
db.pragma('journal_mode = WAL')
db.pragma('foreign_keys = ON')

// ── Schema ────────────────────────────────────────────────
db.exec(`
  CREATE TABLE IF NOT EXISTS bots (
    id          TEXT PRIMARY KEY,
    ric_version TEXT NOT NULL DEFAULT '1.0',
    created_at  TEXT NOT NULL,
    grade       TEXT NOT NULL DEFAULT 'unknown',
    grade_updated_at TEXT NOT NULL,
    public_key  TEXT NOT NULL,
    signature   TEXT NOT NULL,
    -- Developer fields
    dev_name    TEXT NOT NULL,
    dev_email   TEXT NOT NULL,
    dev_org     TEXT,
    dev_website TEXT,
    dev_verified INTEGER NOT NULL DEFAULT 0,
    -- Bot fields
    bot_name        TEXT NOT NULL,
    bot_version     TEXT NOT NULL,
    bot_purpose     TEXT NOT NULL,
    bot_capabilities TEXT NOT NULL, -- JSON array
    bot_user_agent  TEXT NOT NULL,
    -- Claim tracking
    last_claim_date   TEXT,               -- ISO date of most recent claim (YYYY-MM-DD)
    consecutive_days  INTEGER NOT NULL DEFAULT 0,  -- streak of consecutive daily claims
    total_claims      INTEGER NOT NULL DEFAULT 0
  );

  CREATE TABLE IF NOT EXISTS audit_log (
    id         TEXT PRIMARY KEY,
    ric_id     TEXT NOT NULL,
    event      TEXT NOT NULL,
    old_grade  TEXT,
    new_grade  TEXT,
    reason     TEXT,
    reporter   TEXT,
    description TEXT,
    timestamp  TEXT NOT NULL,
    FOREIGN KEY (ric_id) REFERENCES bots(id)
  );

  -- One row per claim attempt, for daily-limit checks and history
  CREATE TABLE IF NOT EXISTS claims (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    ric_id       TEXT NOT NULL,
    claim_date   TEXT NOT NULL,   -- YYYY-MM-DD
    claimed_at   TEXT NOT NULL,   -- ISO timestamp
    consecutive_after INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (ric_id) REFERENCES bots(id)
  );

  -- RFC 9421 nonce tracking — prevents replay attacks
  -- Nonces expire after 10 minutes; a background sweep cleans up old rows
  CREATE TABLE IF NOT EXISTS used_nonces (
    nonce      TEXT PRIMARY KEY,
    ric_id     TEXT NOT NULL,
    used_at    INTEGER NOT NULL  -- Unix seconds
  );
  CREATE INDEX IF NOT EXISTS idx_nonces_used_at ON used_nonces(used_at);
`)

export default db
