-- Migration 005: Crypto payments support

-- Crypto payment records table
CREATE TABLE IF NOT EXISTS public.crypto_payments (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  payment_token   UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  type            TEXT NOT NULL CHECK (type IN ('credits', 'plan')),
  credits         INTEGER,           -- set when type='credits'
  plan            TEXT,              -- set when type='plan'
  months          INTEGER,           -- set when type='plan' and plan is monthly
  amount_usd      DECIMAL(10,2) NOT NULL,
  amount_coin     DECIMAL(20,8) NOT NULL,
  coin            TEXT NOT NULL,
  address         TEXT NOT NULL,
  status          TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'confirmed', 'failed')),
  tx_hash         TEXT,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  confirmed_at    TIMESTAMPTZ,
  expires_at      TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS crypto_payments_payment_token_idx ON public.crypto_payments(payment_token);
CREATE INDEX IF NOT EXISTS crypto_payments_user_status_idx ON public.crypto_payments(user_id, status);

ALTER TABLE public.crypto_payments ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own crypto payments" ON public.crypto_payments
  FOR SELECT USING (auth.uid() = user_id);

-- Track when a crypto-prepaid plan expires
ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS crypto_plan_expires_at TIMESTAMPTZ;
