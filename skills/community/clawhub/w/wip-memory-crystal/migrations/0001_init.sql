-- Memory Crystal Cloud: OAuth + User tables
-- Applied to D1 database: memory-crystal-cloud

-- OAuth dynamic client registration
CREATE TABLE IF NOT EXISTS oauth_clients (
  client_id TEXT PRIMARY KEY,
  client_secret_hash TEXT,
  redirect_uris TEXT NOT NULL,
  client_name TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  last_used_at TEXT
);

-- Authorization codes (short-lived, PKCE)
CREATE TABLE IF NOT EXISTS authorization_codes (
  code TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  code_challenge TEXT NOT NULL,
  code_challenge_method TEXT NOT NULL DEFAULT 'S256',
  redirect_uri TEXT NOT NULL,
  scope TEXT,
  expires_at TEXT NOT NULL,
  used INTEGER DEFAULT 0,
  FOREIGN KEY (client_id) REFERENCES oauth_clients(client_id)
);

-- Access tokens (hashed, never stored raw)
CREATE TABLE IF NOT EXISTS access_tokens (
  token_hash TEXT PRIMARY KEY,
  client_id TEXT NOT NULL,
  user_id TEXT NOT NULL,
  scope TEXT,
  tier TEXT NOT NULL DEFAULT 'sovereign',
  expires_at TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now')),
  FOREIGN KEY (client_id) REFERENCES oauth_clients(client_id)
);

-- Users
CREATE TABLE IF NOT EXISTS users (
  user_id TEXT PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  tier TEXT NOT NULL DEFAULT 'sovereign',
  relay_token TEXT,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- Index for token lookup
CREATE INDEX IF NOT EXISTS idx_access_tokens_expires ON access_tokens(expires_at);
CREATE INDEX IF NOT EXISTS idx_authorization_codes_expires ON authorization_codes(expires_at);
