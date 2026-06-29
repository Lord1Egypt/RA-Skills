# Security & Privacy

Sage Router is a **router, not a collector**. It exists to forward requests to model providers using the credentials you already configured for them. This document explains what the router does and does not do with secrets, identities, and request data.

## TL;DR

- Self-hosted/private router mode **does not collect user identities** by default.
- The hosted public edge requires customer auth for model traffic.
- The router **does not store** OAuth tokens, API keys, prompts, or responses.
- The router **does not phone home**. The only outbound calls are the ones you make to upstream providers.
- All persisted state is local: a route event log and (optionally) a customer record for the hosted billing tier.

## Default posture (no opt-in required)

| Capability | Default | Toggle |
| --- | --- | --- |
| Collect user identities (Supabase Auth) | **Off** | `SAGE_ROUTER_SUPABASE_AUTH_ENABLED=1` |
| Mirror analytics/customers to Supabase | **Off** | `SAGE_ROUTER_SUPABASE_MIRROR_ENABLED=1` |
| Hosted billing tier (creates customer rows) | **Off** | `SAGE_ROUTER_BILLING_ENABLED=1` |
| Stripe / crypto checkout endpoints | Returns `503 *_not_configured` | `STRIPE_SECRET_KEY` / `SAGE_ROUTER_CRYPTO_PAYMENT_ADDRESS` |

If none of the toggles above are set:

- `customer_for_user()` returns `None` for every request.
- The local `~/.cache/sage-router/customers.json` file is **never created**.
- The route event log is the only persisted state, and it is sanitized:
  - `Authorization` and `Cookie` headers are stripped.
  - Email addresses are masked to `<email-N>` tokens.
  - Bodies are kept at a compact summary; raw prompts are not logged.

## Hosted public edge

The hosted SaaS edge at `https://api.sagerouter.dev` is intentionally stricter
than a private local router:

- `/v1/*` and `/v1beta/*` model APIs require an active generated `sk_sage_*`
  customer API key.
- anonymous model requests fail closed with setup-safe account, pricing, status,
  OpenAI base URL, and API-key-prefix guidance.
- account and billing UI routes require a valid Supabase user JWT and are routed
  to the hosted control plane.
- `/analytics` and `/analytics/funnel` are operator-only routes.
- Customer dashboards use `/account/analytics`, which is scoped to the signed-in
  account.
- generated-key traffic is rate-limited at the edge and can be counted against
  durable monthly Supabase quotas.
- `/edge/health`, `/pricing`, `/plans`, `/model-catalog`, and
  `/features/agent-native` expose only public-safe operational, model-family,
  and plan metadata.

The launch readiness script verifies that anonymous model and analytics APIs are
blocked. It also verifies that direct hosted origins fail closed, Supabase auth
and quotas are active, and generated API-key revocation is effective on the next
request.

## What the router does store (when the hosted tier is enabled)

When the operator explicitly turns on the hosted billing tier (`SAGE_ROUTER_BILLING_ENABLED=1`), the router will:

- Create a `customers.json` row with `{id, user_id, email, plan, status, ...}`.
- Store a SHA-256 hash (salted) of generated API keys, never the raw key.
- Append a sanitized event line to the local route log per request.

No payload content is stored. No upstream responses are stored. Tokens never leave the runtime process.

## Credentials handling

Sage Router only ever reads credentials from these sources:

1. Environment variables (e.g. `OPENAI_API_KEY`, `OPENAI_CODEX_API_KEY`).
2. `~/.openclaw/agents/main/agent/auth-profiles.json` for OpenClaw OAuth tokens.

Credentials are held in memory and used as `Authorization: Bearer …` headers. They are not logged, not persisted, and not forwarded to any destination other than the upstream provider they authenticate against.

## What the router does **not** do

- It does not run a separate authentication backend.
- It does not call Supabase, Stripe, or any third party unless the operator has set the corresponding env var.
- It does not record prompts, completions, tool calls, or attachments.
- In self-hosted/private mode, it does not track users across requests unless
  the operator enables the hosted billing/Supabase features.
- In hosted public edge mode, `/v1/models` and analytics are not anonymous:
  model traffic requires a generated customer key, customer analytics are
  account-scoped, and global analytics require the private operator token.

## Threat model assumptions

- The host running Sage Router is trusted. Anyone with shell access can read the env / auth-profiles.json.
- The Docker network between Sage Router and bundled providers (Ollama, OpenClaw) is trusted; nothing leaves the host unless you tunnel it.
- Untrusted clients should put a reverse proxy in front of port `8790` and supply `SAGE_ROUTER_CLIENT_API_KEYS`.

## Reporting issues

Email `security@earlvanze.dev` or open a private security advisory on GitHub. Please do not file public issues for vulnerabilities.
