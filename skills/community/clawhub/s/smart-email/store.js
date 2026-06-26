/**
 * store.js — Local SQLite storage for email accounts
 */

const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = path.join(__dirname, 'data', 'email.db');
let db;

function initDb() {
  db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');

  db.exec(`
    CREATE TABLE IF NOT EXISTS accounts (
      email TEXT PRIMARY KEY,
      password TEXT,
      email_type TEXT DEFAULT 'gmail',
      auth_type TEXT DEFAULT 'password',
      access_token TEXT,
      refresh_token TEXT,
      token_expires INTEGER DEFAULT 0,
      created_at INTEGER
    );
  `);

  return db;
}

function addAccount(email, password, emailType) {
  db.prepare(`
    INSERT INTO accounts (email, password, email_type, auth_type, created_at)
    VALUES (?, ?, ?, 'password', ?)
    ON CONFLICT(email) DO UPDATE SET
      password = excluded.password,
      email_type = excluded.email_type,
      auth_type = 'password',
      access_token = NULL,
      refresh_token = NULL,
      token_expires = 0
  `).run(email, password, emailType || 'gmail', Date.now());
}

function addOAuthAccount(email, emailType, accessToken, refreshToken, tokenExpires) {
  db.prepare(`
    INSERT INTO accounts (email, password, email_type, auth_type, access_token, refresh_token, token_expires, created_at)
    VALUES (?, '', ?, 'oauth', ?, ?, ?, ?)
    ON CONFLICT(email) DO UPDATE SET
      email_type = excluded.email_type,
      auth_type = 'oauth',
      access_token = excluded.access_token,
      refresh_token = excluded.refresh_token,
      token_expires = excluded.token_expires
  `).run(email, emailType || 'outlook', accessToken, refreshToken, tokenExpires, Date.now());
}

function updateTokens(email, accessToken, refreshToken, tokenExpires) {
  db.prepare(`
    UPDATE accounts SET access_token = ?, refresh_token = ?, token_expires = ? WHERE email = ?
  `).run(accessToken, refreshToken, tokenExpires, email);
}

function getAccounts() {
  return db.prepare('SELECT * FROM accounts').all();
}

function getAccount(email) {
  return db.prepare('SELECT * FROM accounts WHERE email = ?').get(email);
}

function removeAccount(email) {
  return db.prepare('DELETE FROM accounts WHERE email = ?').run(email).changes > 0;
}

module.exports = { initDb, addAccount, addOAuthAccount, updateTokens, getAccounts, getAccount, removeAccount };
