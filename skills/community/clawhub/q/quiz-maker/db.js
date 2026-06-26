const Database = require('better-sqlite3');
const path = require('path');
const fs = require('fs');

const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const DB_PATH = path.join(DATA_DIR, 'quiz.db');
let _db = null;

function initDb() {
  if (_db) return _db;
  _db = new Database(DB_PATH);
  _db.pragma('journal_mode = WAL');

  _db.exec(`
    CREATE TABLE IF NOT EXISTS quizzes (
      id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      description TEXT,
      questions TEXT NOT NULL,
      created_at TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS submissions (
      id TEXT PRIMARY KEY,
      quiz_id TEXT NOT NULL,
      name TEXT NOT NULL,
      class_name TEXT,
      score INTEGER NOT NULL,
      answers TEXT,
      submitted_at TEXT DEFAULT (datetime('now')),
      FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    );

    CREATE TABLE IF NOT EXISTS quiz_stats (
      quiz_id TEXT PRIMARY KEY,
      total_participants INTEGER DEFAULT 0,
      total_score INTEGER DEFAULT 0,
      min_score INTEGER,
      max_score INTEGER,
      FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
    );
  `);

  return _db;
}

function getDb() { return _db; }

module.exports = { initDb, getDb };
