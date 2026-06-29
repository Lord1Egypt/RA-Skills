# Hosted provider secrets for Cloud Run Sage Router

Cloud Run Sage Router can now keep upstream provider credentials server-side. Premium client apps can send only a Sage Router subscription key via `Authorization: Bearer <client-key>`.

This does **not** deprecate pass-through user subscriptions. Bring-your-own-key/user-subscription routing remains supported and should stay available alongside hosted-provider routing. Hosted credentials are an additional managed-provider option, not a replacement.

Create these Secret Manager secrets before deploy, using dedicated hosted-router credentials, not personal/local OpenClaw keys:

- `SAGE_ROUTER_CLIENT_API_KEYS` — comma-separated client/subscription keys
- `SAGE_ROUTER_API_KEY_HASH_PEPPER` or `SAGE_ROUTER_SIGNING_SECRET` — optional pepper used when hashing newly generated Sage Router API keys
- `SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY` — server-side Supabase REST key for customer, API key, payment intent, and analytics tables
- `SAGE_ROUTER_SUPABASE_ANON_KEY` — public Supabase Auth validation key
- `STRIPE_SECRET_KEY` or `SAGE_ROUTER_STRIPE_SECRET_KEY`
- `STRIPE_WEBHOOK_SECRET` or `SAGE_ROUTER_STRIPE_WEBHOOK_SECRET`
- `SAGE_ROUTER_STRIPE_PRICE_IDS` — comma-separated plan map, for example `lite=price_...,pro=price_...,max=price_...`
- `SAGE_ROUTER_STRIPE_PRICE_ID` or `STRIPE_PRICE_ID` — legacy single-price fallback
- `SAGE_ROUTER_ACTIVATION_EMAIL_FROM` — sender identity for signup-to-key recovery follow-ups
- `SAGE_ROUTER_RESEND_API_KEY` — Resend API key for activation follow-ups
- `SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO` — optional reply-to for activation follow-ups
- `SAGE_ROUTER_PUBLIC_BASE_URL` — public account/control-plane origin, for example `https://app.sagerouter.dev`
- `SAGE_ROUTER_API_BASE_URL` — public API origin, for example `https://api.sagerouter.dev`
- `SAGE_ROUTER_CRYPTO_PAYMENT_ADDRESS` — optional manual crypto receiving address
- `SAGE_ROUTER_OPENAI_API_KEY`
- `SAGE_ROUTER_OPENROUTER_API_KEY`
- `SAGE_ROUTER_ANTHROPIC_API_KEY`
- `SAGE_ROUTER_GOOGLE_API_KEY`
- `SAGE_ROUTER_XAI_API_KEY`
- `SAGE_ROUTER_ZAI_API_KEY`
- `NVIDIA_API_KEY` (also exposed as `SAGE_ROUTER_NVIDIA_API_KEY`)
- `SAGE_ROUTER_CLOUDFLARE_API_TOKEN`
- `OLLAMA_API_KEY` (also exposed as `SAGE_ROUTER_OLLAMA_API_KEY`)
- `SAGE_ROUTER_OPENAI_CODEX_ACCESS_TOKEN` — OpenAI Codex OAuth bearer token

Optional model allowlists, comma-separated env vars:

- `SAGE_ROUTER_OPENAI_MODELS`
- `SAGE_ROUTER_OPENROUTER_MODELS`
- `SAGE_ROUTER_ANTHROPIC_MODELS`
- `SAGE_ROUTER_GOOGLE_MODELS`
- `SAGE_ROUTER_XAI_MODELS`
- `SAGE_ROUTER_ZAI_MODELS`
- `SAGE_ROUTER_NVIDIA_MODELS`
- `SAGE_ROUTER_CLOUDFLARE_MODELS`
- `SAGE_ROUTER_OLLAMA_MODELS`
- `SAGE_ROUTER_OPENAI_CODEX_MODELS`

OpenAI Codex OAuth compatibility:

- Preferred hosted path: wire `SAGE_ROUTER_OPENAI_CODEX_ACCESS_TOKEN` from Secret Manager.
- Local/mounted compatibility: router will also read OpenClaw/Hermes-style auth profiles from `SAGE_ROUTER_OPENAI_CODEX_AUTH_PROFILE_PATH(S)` if mounted.
- OAuth access tokens are usually short-lived, so production should rotate/update this secret or mount a refresh-capable auth profile intentionally.

Cloudflare account id is configured as deploy env `SAGE_ROUTER_CLOUDFLARE_ACCOUNT_ID`.

Apply `supabase/sage_router_saas.sql` before enabling self-serve account creation in production. Tailnet Edge monthly quotas require `supabase/migrations/20260619021500_sage_router_usage_quotas.sql` if the full schema has not already been applied. CDN-wide learned model modalities require `supabase/migrations/20260626003000_model_modalities.sql`.

Self-serve SaaS tables are configured by name through:

- `SAGE_ROUTER_SUPABASE_CUSTOMERS_TABLE` default `sage_router_customers`
- `SAGE_ROUTER_SUPABASE_API_KEYS_TABLE` default `sage_router_api_keys`
- `SAGE_ROUTER_SUPABASE_PAYMENT_INTENTS_TABLE` default `sage_router_payment_intents`
- Tailnet Edge monthly quotas use `sage_router_usage_counters` plus the `sage_router_increment_usage` RPC from `supabase/migrations/20260619021500_sage_router_usage_quotas.sql`
- Learned model modalities use `sage_router_model_modalities` plus the `sage_router_record_model_modalities` RPC from `supabase/migrations/20260626003000_model_modalities.sql`; set `SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED=1` to enable it when Supabase mirroring is not already enabled.
- Cloudflare API Worker deployments also write successful response modality headers to the same RPC when `SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED=1` and Supabase service credentials are present; public edge health must report `modelModalities.sharedEnabled=true` and `modelModalities.rpcConfigured=true` before the Worker treats an origin as CDN-ready.

Minimum columns expected by the incremental backend:

- `sage_router_customers`: `id`, `user_id`, `email`, `plan`, `status`, `stripe_customer_id`, `stripe_subscription_id`, `created_at_epoch`, `updated_at_epoch`
- `sage_router_api_keys`: `id`, `customer_id`, `user_id`, `name`, `prefix`, `api_key_hash`, `status`, `plan`, `created_at_epoch`, `last_used_at_epoch`, `revoked_at_epoch`
- `sage_router_payment_intents`: `id`, `kind`, `customer_id`, `user_id`, `status`, `asset`, `network`, `amount`, `address`, `metadata`, `event_type`, `event_id`, `created_at_epoch`, `updated_at_epoch`
- `sage_router_usage_counters`: `id`, `customer_id`, `user_id`, `plan`, `period`, `requests`, `created_at_epoch`, `updated_at_epoch`
- `sage_router_model_modalities`: `key`, `provider`, `model`, `modalities`, `count`, `first_seen_epoch_ms`, `last_seen_epoch_ms`, `updated_at_epoch_ms`

Generated API keys are returned raw once on creation. Store only `api_key_hash` server-side. Legacy/manual `SAGE_ROUTER_CLIENT_API_KEYS` remains supported for migrations and operator-issued keys.
