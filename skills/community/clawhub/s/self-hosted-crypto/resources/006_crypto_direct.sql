-- Migration 006: Self-custody HD wallet columns for direct on-chain payments
-- Removes dependency on CryptAPI by tracking which HD derivation index each payment used.

ALTER TABLE public.crypto_payments
  ADD COLUMN IF NOT EXISTS wallet_type TEXT
    CHECK (wallet_type IN ('evm', 'btc', 'sol'));

ALTER TABLE public.crypto_payments
  ADD COLUMN IF NOT EXISTS derivation_index INTEGER;

-- Prevent address reuse: only one active payment per (wallet_type, derivation_index)
CREATE UNIQUE INDEX IF NOT EXISTS crypto_payments_wallet_index_unique
  ON public.crypto_payments (wallet_type, derivation_index)
  WHERE status IN ('pending', 'confirmed');

-- Fast lookup of pending payments by wallet type (used by cron poller)
CREATE INDEX IF NOT EXISTS crypto_payments_pending_wallet_idx
  ON public.crypto_payments (wallet_type, status)
  WHERE status = 'pending';
