-- Idempotency guard for Stripe webhook retries.
create unique index if not exists sage_router_payment_intents_stripe_event_idx
  on public.sage_router_payment_intents (event_id)
  where kind = 'stripe_webhook' and event_id is not null;
