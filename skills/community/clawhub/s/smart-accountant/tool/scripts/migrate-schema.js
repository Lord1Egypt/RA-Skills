const db = require('../lib/db');

function migrate() {
  console.log('Running schema migrations...');

  db.exec(`
    CREATE TABLE IF NOT EXISTS schema_migrations (
      version INTEGER PRIMARY KEY
    );

    -- Ledger Groups (e.g. Assets, Liabilities)
    CREATE TABLE IF NOT EXISTS ledger_groups (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      parent_group_id INTEGER,
      FOREIGN KEY(parent_group_id) REFERENCES ledger_groups(id)
    );

    -- Ledgers (Postable accounts)
    CREATE TABLE IF NOT EXISTS ledgers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL UNIQUE,
      type TEXT NOT NULL CHECK(type IN ('Asset', 'Liability', 'Equity', 'Income', 'Expense')),
      normal_balance TEXT NOT NULL CHECK(normal_balance IN ('Debit', 'Credit')),
      parent_group_id INTEGER,
      gstin TEXT,
      state_code TEXT,
      registration_type TEXT CHECK(registration_type IN ('regular', 'composition', 'unregistered', 'overseas', NULL)),
      default_supply_type TEXT CHECK(default_supply_type IN ('taxable', 'exempt', 'nil_rated', 'non_gst', NULL)),
      rcm_flag BOOLEAN DEFAULT 0,
      FOREIGN KEY(parent_group_id) REFERENCES ledger_groups(id)
    );

    -- Vouchers (Journal Entries)
    CREATE TABLE IF NOT EXISTS vouchers (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      voucher_no TEXT UNIQUE,
      type TEXT NOT NULL CHECK(type IN ('CR', 'BR', 'CP', 'BP', 'PE', 'SE', 'PR', 'SR', 'CN', 'JE', 'OE')),
      date DATE NOT NULL,
      amount REAL NOT NULL CHECK(amount >= 0),
      narration TEXT,
      source_doc_type TEXT,
      source_doc_no TEXT,
      status TEXT NOT NULL DEFAULT 'DRAFT' CHECK(status IN ('DRAFT', 'PREVIEWED', 'CONFIRMED', 'POSTED', 'REVERSED')),
      request_id TEXT UNIQUE, -- for idempotency
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    -- Lines (Debits and Credits)
    CREATE TABLE IF NOT EXISTS lines (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      voucher_id INTEGER NOT NULL,
      ledger_id INTEGER NOT NULL,
      debit REAL NOT NULL DEFAULT 0 CHECK(debit >= 0),
      credit REAL NOT NULL DEFAULT 0 CHECK(credit >= 0),
      FOREIGN KEY(voucher_id) REFERENCES vouchers(id),
      FOREIGN KEY(ledger_id) REFERENCES ledgers(id)
    );

    -- Audit Log (Immutable record)
    CREATE TABLE IF NOT EXISTS audit_log (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      event_type TEXT NOT NULL,
      entity_id INTEGER,
      before_json TEXT,
      after_json TEXT,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    
    -- Global Configuration
    CREATE TABLE IF NOT EXISTS config (
      key TEXT PRIMARY KEY,
      value TEXT
    );
  `);

  console.log('Schema migration complete.');
}

if (require.main === module) {
  migrate();
}

module.exports = { migrate };
