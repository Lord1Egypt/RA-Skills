-- ride-receipts-gateway-llm schema (SQLite)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS rides (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  provider TEXT NOT NULL,

  gmail_message_id TEXT NOT NULL,
  email_date_text TEXT,
  subject TEXT,

  start_time_text TEXT,
  end_time_text TEXT,

  total_text TEXT,
  currency TEXT,
  amount REAL,

  pickup TEXT,
  dropoff TEXT,
  pickup_city TEXT,
  pickup_country TEXT,
  dropoff_city TEXT,
  dropoff_country TEXT,

  payment_method TEXT,
  driver TEXT,
  distance_text TEXT,
  duration_text TEXT,

  notes TEXT,

  extracted_ride_json TEXT,

  inserted_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ','now')),

  UNIQUE(provider, gmail_message_id) ON CONFLICT REPLACE
);

CREATE INDEX IF NOT EXISTS idx_rides_provider_date ON rides(provider, email_date_text);
CREATE INDEX IF NOT EXISTS idx_rides_amount ON rides(currency, amount);
