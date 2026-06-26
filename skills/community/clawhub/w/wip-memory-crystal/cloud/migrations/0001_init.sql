-- Memory Crystal Cloud: initial schema
-- OAuth tables for auth + user accounts
-- Tier 1: relay-only (sovereign)
-- Tier 2: adds chunks + memories tables (separate migration)

-- ── OAuth Clients (Dynamic Client Registration) ──
CREATE TABLE IF NOT EXISTS oauth_clients (
  client_id TEXT PRIMARY KEY,
  redirect_uris TEXT NOT NULL DEFAULT '[]',
  client_name TEXT,
  created_at TEXT NOT NULL,
  last_used_at TEXT
);

-- ── Authorization Codes (PKCE flow) ──
CREATE TABLE IF NOT EXISTS authorization_codes (
  code TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  code_challenge TEXT NOT NULL,
  code_challenge_method TEXT NOT NULL DEFAULT 'S256',
  redirect_uri TEXT NOT NULL,
  scope TEXT,
  expires_at TEXT NOT NULL,
  used INTEGER DEFAULT 0
);

-- ── Access Tokens ──
CREATE TABLE IF NOT EXISTS access_tokens (
  token_hash TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  scope TEXT,
  tier TEXT NOT NULL DEFAULT 'sovereign',
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL
);

-- ── Users ──
CREATE TABLE IF NOT EXISTS users (
  user_id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  tier TEXT NOT NULL DEFAULT 'sovereign',
  relay_token TEXT,
  created_at TEXT NOT NULL
);

-- ── Indexes ──
CREATE INDEX IF NOT EXISTS idx_auth_codes_client ON authorization_codes(client_id);
CREATE INDEX IF NOT EXISTS idx_tokens_user ON access_tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_tokens_expires ON access_tokens(expires_at);
CREATE INDEX IF NOT EXISTS idx_clients_last_used ON oauth_clients(last_used_at);
