import Database from 'better-sqlite3';
import path from 'path';
import os from 'os';

const DB_DIR = path.join(os.homedir(), '.reading-buddy');
const DB_PATH = path.join(DB_DIR, 'reading-buddy.db');

let db: Database.Database | null = null;

export function getDatabase(): Database.Database {
  if (!db) {
    const fs = require('fs');
    if (!fs.existsSync(DB_DIR)) {
      fs.mkdirSync(DB_DIR, { recursive: true });
    }
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');
  }
  return db;
}

export function closeDatabase(): void {
  if (db) {
    db.close();
    db = null;
  }
}
