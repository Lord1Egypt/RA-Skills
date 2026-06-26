-- Provider Checkout - Database Schema
-- Standard PostgreSQL. Works on: Supabase, AWS RDS, Neon, self-hosted, etc.
-- Run via psql, pgAdmin, Supabase SQL Editor, or your preferred tool.
-- Adjust table/column names as needed for your project.

-- Purchases table: one row per checkout session
CREATE TABLE IF NOT EXISTS purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_email VARCHAR(255) NOT NULL,
  provider_payment_id TEXT,
  provider_preference_id TEXT,
  status VARCHAR(20) NOT NULL DEFAULT 'pending'
    CHECK (status IN ('pending', 'approved', 'rejected')),
  total_amount NUMERIC(10,2),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Purchase items: line items for each purchase
-- Adjust the item_id foreign key to match your product table
CREATE TABLE IF NOT EXISTS purchase_items (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  purchase_id UUID NOT NULL REFERENCES purchases(id) ON DELETE CASCADE,
  item_id UUID NOT NULL,  -- FK to your products/items table
  price NUMERIC(10,2) NOT NULL
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_purchases_email ON purchases(user_email);
CREATE INDEX IF NOT EXISTS idx_purchases_status ON purchases(status);
CREATE INDEX IF NOT EXISTS idx_purchases_mp_payment ON purchases(provider_payment_id);
CREATE INDEX IF NOT EXISTS idx_purchase_items_purchase ON purchase_items(purchase_id);

-- gen_random_uuid() requires pgcrypto on PostgreSQL < 13:
-- CREATE EXTENSION IF NOT EXISTS pgcrypto;

