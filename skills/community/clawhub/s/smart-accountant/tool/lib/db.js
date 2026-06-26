const Database = require('better-sqlite3');
const path = require('path');

const dbPath = path.resolve(__dirname, '..', 'accounting.db');
const db = new Database(dbPath);

// Enforce strict accounting-grade PRAGMAs
db.pragma('journal_mode = WAL');
db.pragma('foreign_keys = ON');
db.pragma('synchronous = FULL');
db.pragma('busy_timeout = 5000');
db.pragma('temp_store = MEMORY');

module.exports = db;
