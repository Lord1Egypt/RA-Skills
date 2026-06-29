# Sage Router

**Local-first AI model routing for serious agents.**

One endpoint. Any provider. The router figures out the rest.

[![Umbrel](https://img.shields.io/badge/Umbrel-1.0.4-purple)](https://github.com/getumbrel/umbrel-apps/pull/5720)
[![ClawHub](https://img.shields.io/badge/ClawHub-v4.157.9-blue)](https://clawhub.ai/earlvanze/sage-router)
[![GitHub](https://img.shields.io/badge/GitHub-earlvanze%2Fsage--router-black)](https://github.com/earlvanze/sage-router)

---

## Hosted API Is Live

Want the public OpenAI-compatible endpoint instead of self-hosting first?

- [Create a hosted `sk_sage_*` key](https://app.sagerouter.dev/account.html?plan=pro&start=create_key&utm_source=github&utm_medium=readme&utm_campaign=sage-router-launch) for `https://api.sagerouter.dev/v1`
- [Copy the 60-second setup](https://sagerouter.dev/quickstart?utm_source=github&utm_medium=readme&utm_campaign=sage-router-launch)
- [Compare hosted plans](https://sagerouter.dev/pricing?utm_source=github&utm_medium=readme&utm_campaign=sage-router-launch)

Provider credentials stay with your authorized accounts or local routers; hosted keys cover Sage Router account management, quotas, analytics, health-aware routing, and reliability.

---

## What This Is

Sage Router is a **local-first, self-hosted AI model gateway** that intelligently routes requests to the best available model based on intent, latency, and capability — not just price.

Sage Router optimizes for **getting the job done**:

- **Intent-based routing**: Code tasks go to coding models, creative tasks to creative models, reasoning tasks to reasoning models
- **Automatic fallback**: If one provider fails or hits rate limits, it seamlessly tries the next
- **Dynamic discovery**: New models from Ollama, Anthropic, OpenAI, Google, NVIDIA NIM / NVIDIA Cloud, and OpenClaw are auto-detected — no config updates needed
- **Zero API lock-in**: Use any subscription or key you already have (Ollama, Claude, OpenAI, Gemini, NVIDIA NIM, GitHub Copilot)
- **Debuggable routing**: Surface the selected provider/model in headers, `/health`, or optional debug output

---

## Quick Start

### Installation (OpenClaw)

```bash
openclaw skill add sage-router --from clawhub
openclaw skill configure sage-router
```

### Manual Installation

```bash
git clone https://github.com/earlvanze/sage-router.git
cd sage-router
pip install -r requirements.txt  # if any
python3 router.py --port 8790
```

### Umbrel (Home Server)

Install from the [Umbrel App Store](https://github.com/getumbrel/umbrel-apps/pull/5720) or add the personal repo:

```yaml
# In umbrel.yaml → appRepositories
- https://github.com/earlvanze/umbrel-personal-apps
```

The Umbrel app pins `ghcr.io/earlvanze/sage-router-public:v3.28.11` and stores its config under the app data directory. The built-in config dashboard is accessible from the Umbrel app tile.

### Tailnet Edge Endpoint

For a CDN-style endpoint across multiple Sage Router installs, deploy the Tailnet edge proxy:

```bash
cd deploy/tailnet-edge
cp .env.example .env
docker compose up -d --build
tailscale serve --bg --https=443 http://127.0.0.1:8790
```

The edge health-checks each configured Tailnet upstream, routes OpenAI-compatible traffic to the lowest-latency healthy Sage Router node, and keeps provider credentials on the private routers. Publish it privately with Tailscale Serve/Funnel, or front a stable cloud VM edge with Cloudflare for a CDN-style public endpoint. See [deploy/tailnet-edge](deploy/tailnet-edge/README.md) for Google Cloud VM bootstrap and public monetization notes.

After changing the public edge, verify generated-key routing preserves router-profile model aliases even when a stale Tailnet upstream serves the request:

```bash
python3 scripts/smoke_public_profile_alias.py \
  --env-file /opt/sage-router/deploy/tailnet-edge/.env \
  --api-base https://api.sagerouter.dev \
  --model sage-router/frontier
```

### sagerouter.dev Deployment Map

The current public deployment is intentionally split:

- `https://sagerouter.dev` and `https://www.sagerouter.dev` are static Cloudflare Pages (`sage-router-web`). They host marketing/docs/account UI only.
- `https://app.sagerouter.dev` is the hosted account/login surface, served by the same Cloudflare Pages project with Supabase Auth redirects pointed at this host.
- `https://app.sagerouter.dev/status` is the public reliability and launch-actions page. It reads `/edge/health` and `/pricing` from the public API edge to show selected upstream ID, Tailnet/cloud backend class, CDN-style reliability evidence, lowest-latency retry failover policy, control-plane health, auth mode, rate-limit/quota enforcement, pre-auth generated-key attempt throttling, generated-key revocation posture, customer endpoint, plan limits, secret-free billing readiness, and copyable no-secret operator actions for activation email preflight, managed-provider resale dry-run/staging, first-request setup, and Cloudflare BIC verification without exposing customer data, internal upstream URLs, Tailnet hostnames, Stripe price IDs, provider credentials, private provider costs, or secrets.
- `https://sagerouter.dev/billing` is the dedicated billing recovery page. It explains Stripe checkout, Stripe billing portal, manual/crypto settlement, activation states, generated `sk_sage_*` key behavior before and after payment, payment recovery, and safe no-secret support context.
- `https://sagerouter.dev/fusion` is the premium compound-model page. It documents `sage-router/fusion`, the `sage-router:fusion` server tool, `tool_choice: "required"`, Pro/Max gating, and the `fusion_plan_required` upgrade path.
- `https://sagerouter.dev/support` is the public support and billing help page. It routes customers to account setup, Stripe billing portal, manual/crypto settlement, quota/API-key troubleshooting, 503 reliability checks, security reporting, and abuse reporting while explicitly telling users not to send prompts, workflow text, provider credentials, OAuth tokens, API keys, private keys, cookies, raw provider responses, or customer data in public support channels.
- `https://sagerouter.dev/managed-access` is the managed-provider-access private beta and Max implementation intake page. It captures contact plus allowlisted qualification buckets such as deployment preference, expected monthly routed request volume, provider access posture, target provider family, commercial preference, support need, and target launch window; it explains that managed access still requires provider authorization, provider terms acknowledgment, an authorized provider allowlist, a configured provider cost model, and plan-margin checks before activation; it does not collect prompts, workflow text, provider credentials, OAuth tokens, generated API keys, private keys, cookies, raw provider responses, actual provider costs, or customer data.
- `https://api.sagerouter.dev` is a Cloudflare-proxied GCP edge VM. The edge health-checks Tailnet Sage Router installs plus the Google-hosted Sage Router API origin, then routes to the lowest-latency healthy backend. The Cloudflare API Worker can also retry replayable requests against the next healthy public origin on transient `502/503/504` failures before returning an error. Public health and response headers identify the edge layer and selected backend only with stable public IDs such as `upstream-1`, never configured upstream URLs or Tailnet hostnames.
- Tailnet Edge is the reliability layer for routing to healthy Sage Router installs on a Tailnet. In public mode, set `SAGE_ROUTER_EDGE_AUTH_MODE=supabase`: `/pricing`, `/plans`, `/model-catalog`, and `/features/agent-native` are public control-plane metadata; `/pricing` also exposes a `billing` object with secret-free Stripe checkout readiness, configured plan names, billing portal readiness, manual settlement status paths, activation statuses, and generated-key limits. The same metadata exposes `publicLaunch.managedProviderAccess`, which must stay disabled until provider resale terms are acknowledged, a provider-family allowlist is configured, a margin policy, positive unit economics backed by a positive `SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS`, durable quota/rate-limit enforcement, generated-key revocation, operator abuse review, durable operator audit events, and managed-access acceptable-use terms are ready. Public unit-economics rows expose plan revenue and derived maximum safe provider cost per 1,000 requests without exposing actual configured provider costs. `providerFamilyReadiness` and `oneSubscriptionReadiness` keep OpenRouter visible as supported BYOK routing while excluding it from the managed subscription resale offer unless separate provider authorization is added later. `SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED=1` is treated as an operator request only; public metadata keeps `enabled: false` and reports missing controls until every prerequisite is satisfied. The marketing site publishes `/models`, `/provider-resale-terms`, and `/margin-policy` as reviewable prerequisites, but those pages do not enable managed resale by themselves; `/v1/*` and `/v1beta/*` model APIs accept active generated `sk_sage_*` customer API keys; anonymous model API failures stay fail-closed but include account, pricing, status, OpenAI base URL, and API-key-prefix guidance for setup debugging; account/billing UI requests preserve Supabase user JWTs and should be pinned to a hosted control-plane origin with `SAGE_ROUTER_CONTROL_PLANE_UPSTREAM`; operator analytics such as `/analytics/funnel` accepts either the private edge admin token or `SAGE_ROUTER_ANALYTICS_TOKEN`, is pinned to the control plane, and can inject `SAGE_ROUTER_CONTROL_PLANE_TOKEN` separately from the Tailnet backend token. Browser login belongs on `app.sagerouter.dev`; `api.sagerouter.dev` should remain API-only. Browser-originating account, billing, and customer-suspension mutations are rejected at the edge unless `Origin` is a trusted Sage Router app/local/preview origin; CLI and server clients without `Origin` still pass through normal auth. Generated keys and account/billing JWT routes are rate-limited by `SAGE_ROUTER_EDGE_RATE_LIMITS`; generated-key-looking model API attempts are also throttled by client IP through `SAGE_ROUTER_EDGE_AUTH_ATTEMPT_RATE_LIMIT` before Supabase generated-key lookup, so random invalid keys cannot create unbounded service-role reads; generated model API keys can also be counted against durable monthly Supabase quotas with `SAGE_ROUTER_EDGE_QUOTA_ENABLED=1` after applying `supabase/migrations/20260619021500_sage_router_usage_quotas.sql`. Supabase user JWT validation uses `SAGE_ROUTER_EDGE_AUTH_CACHE_SECONDS`, but generated customer API keys default to `SAGE_ROUTER_EDGE_API_KEY_AUTH_CACHE_SECONDS=0` so revocation takes effect on the next request. The private edge admin token is exempt for recovery and remains required for `/admin*`. Hosted origins should also set `SAGE_ROUTER_CLIENT_AUTH_REQUIRED=1`; direct origin requests to `/v1/models`, setup, admin, discovery, and dashboard config routes must fail closed unless they carry a valid operator token, and generated customer keys are only accepted for model metadata/traffic.
- After the edge validates a generated customer API key, it forwards customer id, user id, plan, and status as trusted internal headers while replacing the customer key with the private backend token. Hosted routers use those headers only after backend-token auth, keeping route telemetry, account analytics, first-request activation, quota support, and operator review attributed to the paying customer without exposing raw generated keys to Tailnet model backends.
- `https://sagerouter.dev/quickstart` is the hosted API first-request path. It leads with `Copy 60-second setup bundle` and an always-visible `Create API key next` account handoff that records whether setup was copied first, then shows `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, generated `sk_sage_*` key setup, the `sage-router/frontier` profile, premium `sage-router/fusion`, curl, JavaScript, Python, and Codex examples, plus 401/402/429/503 troubleshooting.
- `https://sagerouter.dev/pricing` uses the same measurable activation pattern for buyer-intent traffic: `Copy 60-second setup bundle` records `quickstart_snippet_copied` with `pricing-full-setup-bundle`, Pro activation links use `start=create_key`, `Create API key next` stays visible before and after copy, Lite/Max checkout links preserve `start=checkout`, and the key-first proof block makes the Pro path create a generated `sk_sage_*` key before checkout.
- `https://app.sagerouter.dev/login.html?start=create_key` is the no-key signup recovery bridge. It keeps same-email recovery first, shows the generated-key-before-checkout steps, preserves the `start=create_key` activation URL, and records `login_key_recovery_account_setup_clicked` as a key-first redirect signal so operators can distinguish passive login recovery views from users who clicked through toward API-key setup.
- `https://sagerouter.dev/api-troubleshooting` is the no-secret diagnostic path for hosted 401/402/429/503 responses. It documents safe probes, `WWW-Authenticate`, `Retry-After`, `X-RateLimit-*`, `X-Quota-*`, account/pricing/status onboarding links, and the non-secret `apiKeyPrefix` without asking customers to paste prompts or credentials.
- `https://sagerouter.dev/docs/api-reference` is the hosted API reference for OpenAI-compatible customers. It documents `GET /v1/models`, `POST /v1/chat/completions`, `POST /v1/responses`, public `/model-catalog`, generated `sk_sage_*` keys, quotas, rate limits, and failover signals.
- `https://sagerouter.dev/docs/gateway-migration` is the Gateway migration guide for OpenAI-compatible customers. It maps `OPENAI_BASE_URL=https://gateway.example/api/v1` to `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, generated `sk_sage_*` keys, `sage-router/frontier`, premium `sage-router/fusion`, model catalog discovery, and the provider terms boundary.
- `https://sagerouter.dev/compare/model-gateways` captures migration-intent traffic with a copy-first `Copy 60-second gateway setup` bundle and `gateway-compare-migration-bundle` setup telemetry.
- `https://sagerouter.dev/reddit-ai-gateway-evaluation` packages Reddit-style AI gateway evaluation proof: local-first custody, OpenRouter as BYOK rather than bundled resale, multiple API-key load balancing, 429 failover, multimodal routing, hosted generated-key activation, and copyable evaluation/setup snippets.
- `https://sagerouter.dev/reliability-proof` gives skeptical buyers copyable proof snippets for 429 failover, credential load balancing, multimodal routing safeguards, hosted generated-key activation, public edge health, and no-secret Reddit replies.
- `https://sagerouter.dev/ollama-ai-model-router` captures Ollama and Ollama Cloud routing traffic with local Ollama setup, one OpenAI-compatible endpoint, multiple API-key load balancing, 429 failover, multimodal routing, hosted generated-key activation, and copyable Ollama setup telemetry.
- `https://sagerouter.dev/openai-api-router` captures OpenAI-compatible gateway traffic with hosted `sk_sage_*` keys, `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, Responses API compatibility, multiple OpenAI API-key load balancing, 429 failover, multimodal routing, and copyable OpenAI setup telemetry.
- `https://sagerouter.dev/azure-openai-router` captures Azure OpenAI routing traffic with hosted `sk_sage_*` keys, customer-owned `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` custody, Azure deployment routing, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, and copyable Azure setup telemetry.
- `https://sagerouter.dev/anthropic-api-router` captures Anthropic-compatible and Claude Code routing traffic with hosted `sk_sage_*` keys, `ANTHROPIC_BASE_URL=https://api.sagerouter.dev`, Dario-ready subscription paths, 429 failover, multimodal routing, provider-authorization boundaries, and copyable Anthropic setup telemetry.
- `https://sagerouter.dev/aws-bedrock-router` captures AWS Bedrock routing traffic with hosted `sk_sage_*` keys, customer-owned AWS account/IAM custody, `AWS_PROFILE`, `AWS_REGION`, Bedrock model routing, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, and copyable Bedrock setup telemetry.
- `https://sagerouter.dev/github-copilot-router` captures GitHub Copilot and Copilot-compatible coding-agent routing traffic with hosted `sk_sage_*` keys, customer-owned `GITHUB_COPILOT_TOKEN` custody, OpenAI-compatible setup, model discovery, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, and copyable Copilot setup telemetry.
- `https://sagerouter.dev/codex-cli-router` captures Codex CLI routing traffic with hosted `sk_sage_*` keys, `base_url = "https://api.sagerouter.dev/v1/"`, `wire_api = "responses"`, local port `8790`, Tailnet routes, 429 failover, multimodal routing, Codex OAuth boundary language, and copyable Codex setup telemetry.
- `https://sagerouter.dev/aider-ai-model-router` captures Aider routing traffic with hosted `sk_sage_*` keys, `OPENAI_API_BASE=https://api.sagerouter.dev/v1`, `aider --model openai/auto`, local port `8790`, local Ollama fallback, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, and copyable Aider setup telemetry.
- `https://sagerouter.dev/continue-ai-model-router` captures Continue routing traffic with hosted `sk_sage_*` keys, OpenAI-compatible `apiBase=https://api.sagerouter.dev/v1`, `model=auto`, local port `8790`, local Ollama fallback, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, and copyable Continue setup telemetry.
- `https://sagerouter.dev/openhands-ai-model-router` captures OpenHands routing traffic with hosted `sk_sage_*` keys, `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, `model = "auto"`, local port `8790`, local Ollama fallback, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, and copyable OpenHands setup telemetry.
- `https://sagerouter.dev/openclaw-ai-model-router` captures OpenClaw routing traffic with Sage Router skill setup, `OPENAI_BASE_URL=http://localhost:8790/v1`, `ANTHROPIC_BASE_URL=http://localhost:8790`, Codex OAuth passthrough from OpenClaw auth profiles, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, and copyable OpenClaw setup telemetry.
- `https://sagerouter.dev/claude-code-router` captures Claude Code routing traffic with hosted `sk_sage_*` keys, `ANTHROPIC_BASE_URL=https://api.sagerouter.dev`, authorized Anthropic or Dario subscription paths, local/Tailnet fallback, 429 failover, multimodal routing, provider-authorization boundaries, and copyable Claude Code setup telemetry.
- `https://sagerouter.dev/gemini-api-router` captures Gemini, Google AI, Vertex AI, and Gemini CLI routing traffic with hosted `sk_sage_*` keys, structured function-tool routing, 429 failover, multimodal routing, provider-authorization boundaries, and copyable Gemini setup telemetry.
- `https://sagerouter.dev/xai-grok-router` captures xAI Grok API routing traffic with hosted `sk_sage_*` keys, customer-owned `XAI_API_KEY` custody, OpenAI-compatible setup, `/v1/models` discovery, credential load balancing, 429 failover, multimodal safeguards, xAI SSO proxy boundaries, and copyable Grok setup telemetry.
- `https://sagerouter.dev/mistral-ai-router` captures Mistral AI and Codestral routing traffic with hosted `sk_sage_*` keys, customer-owned `MISTRAL_API_KEY` custody, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, and copyable Mistral setup telemetry.
- `https://sagerouter.dev/groq-ai-router` captures Groq low-latency Llama and Mixtral routing traffic with hosted `sk_sage_*` keys, customer-owned `GROQ_API_KEY` custody, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, and copyable Groq setup telemetry.
- `https://sagerouter.dev/nvidia-nim-router` captures NVIDIA NIM, NVIDIA Cloud, and GPU-backed inference routing traffic with hosted `sk_sage_*` keys, customer-owned `NVIDIA_API_KEY` custody, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal routing, provider-authorization boundaries, and copyable NVIDIA setup telemetry.
- `https://sagerouter.dev/coding-agent-model-router` captures Codex, Cursor, Aider, Continue, Claude Code, OpenHands, and OpenClaw model-routing traffic with hosted `sk_sage_*` keys, Codex Responses API profiles, local Ollama fallback, 429 failover, multimodal routing, and copyable coding-agent setup telemetry.
- `https://sagerouter.dev/cursor-ai-model-router` captures Cursor model-routing traffic with hosted `sk_sage_*` keys, custom OpenAI-compatible endpoint setup, Anthropic-compatible paths, local Ollama fallback, multiple API-key load balancing, 429 failover, multimodal routing, and copyable Cursor setup telemetry.
- `https://sagerouter.dev/docs/codex` is the dedicated Codex CLI setup path. It shows hosted `https://api.sagerouter.dev/v1/`, local `http://127.0.0.1:8790/v1/`, and Tailnet `http://<tailnet-host>:8790/v1/` profiles using `wire_api = "responses"` and `sage-router/frontier`.
- `https://sagerouter.dev/integrations` is the public integrations index. It collects hosted, local port `8790`, and Tailnet setup paths for OpenAI-compatible clients, Codex, Cursor, Aider, Continue, Claude Code, OpenHands, Anthropic-compatible clients, Ollama, Ollama Cloud, NVIDIA NIM, OpenClaw, Hermes, and Pi agents while preserving the no-secret support boundary.

### Hosted API Quickstart

The hosted account page at `https://app.sagerouter.dev/account.html` is the customer onboarding surface:

1. Create an account or sign in with email, magic link, or an enabled Supabase OAuth provider.
2. Choose Lite, Pro, or Max. Stripe checkout posts the selected plan to `/billing/stripe/checkout`; after checkout links a Stripe customer, the account page opens `/billing/stripe/portal` for self-service billing, payment-method changes, cancellation, and subscription management. Crypto/manual settlement stays available for accounts that are not ready for Stripe, with default settlement amounts derived from the selected monthly plan unless an agreed override is supplied. The account page can create a manual intent and refresh its bounded public status without echoing customer notes. Operators approve pending manual intents through the private `/admin/payment-intents/{intent_id}/approve` path; approval activates the selected plan, records a secret-free audit event, rejects replay/stale approvals, and still leaves suspended customers suspended.
3. Generate an `sk_sage_*` API key, copy the raw key while it is shown once, test it against `/v1/models`, send a first browser-side `sage-router/frontier` chat completion from the account page, and use the copyable OpenAI SDK, Codex CLI, Anthropic-compatible, or curl quickstart. The signed-in account page auto-creates the first generated setup key once per session when no active key exists; saved `start=checkout` activation intent then proceeds toward checkout after the setup artifact exists. A persistent post-key activation panel keeps verification, first request, and Codex setup copy available after key creation without recording raw keys in funnel telemetry.

The account page consumes the secret-free `/pricing.billing` readiness metadata
before opening checkout. If Stripe or the selected plan is not configured, the
Stripe button is disabled, the funnel records `account_checkout_unavailable`,
and the customer is directed to manual settlement or billing help instead of a
known failing checkout path. If checkout, billing-portal, or manual-settlement
requests fail after a buyer clicks, the account page records only coarse
failure states such as `stripe_not_configured`, `unauthorized`,
`rate_limited`, or `service_unavailable` so operators can fix conversion
friction without collecting raw billing errors or customer secrets.

Plan-specific pricing links such as `/account.html?plan=pro&start=create_key`
preselect that checkout plan, remember it locally through signup/login,
preserve the checkout intent after email/OAuth redirects, and restore the plan
from Stripe success/cancel return URLs so new customers do not accidentally
land on the default checkout tier or need a second billing click.

API keys created before checkout are stored, and the signed-in account path now asks verified users to create a generated key before checkout so setup can be copied while payment is still pending. The account page still marks routing as blocked until the customer is active, trialing, or manually enabled; the edge enforces the same rule before proxying `/v1/*` traffic. Revoked keys and inactive accounts are rechecked against Supabase by default on every generated-key request. Customers are limited to `SAGE_ROUTER_MAX_ACTIVE_API_KEYS_PER_CUSTOMER` active generated keys at a time, default `5`; revoked keys do not count against the cap. Signed-in customers can revoke their own generated keys from the account page even while verified-email gates block new key creation, Stripe checkout, or manual payment intent creation, so leaked keys can be shut down immediately without opening a support ticket. Successful customer revokes record a bounded `api_key.revoke` audit event and anonymous account-funnel revoke telemetry without raw generated keys, key hashes, prompts, provider credentials, or raw error payloads.

For signed-in, verified users without a generated key, the primary account activation button creates the first `sk_sage_*` key directly instead of only scrolling to the key panel. The one-time raw key display remains unchanged, and checkout can still continue from the preserved `start=checkout` intent after key creation.

Operator abuse controls are fail-closed. `GET /admin/customers?q=...&status=...&limit=...` and `GET /admin/customers/{customer_id}` require the private operator token and return bounded customer, usage, activation, review-flag, operator-audit, and public API-key metadata for support and abuse review without raw generated keys, key hashes, provider credentials, prompts, or raw responses. Review flags are server-derived from bounded state such as suspension, routing block, missing first request, key limit, quota pressure, and idle paid usage. `POST /admin/customers/{customer_id}/suspend` sets the customer status to `suspended`, revokes all active generated API keys for that customer, records a secret-free operator audit event, and immediately blocks generated-key routing. A suspended status is sticky across Stripe lifecycle webhooks and manual payment approvals, so payment recovery or subscription updates cannot accidentally restore routing for an account held for abuse, chargeback, provider-risk, or security review. After review, `POST /admin/customers/{customer_id}/unsuspend` defaults the customer to `inactive`; operators can pass `{"status":"active"}` only when access should be restored. Previously revoked generated API keys stay revoked, and the unsuspend path also records a bounded operator audit event, so the customer must create a fresh key after reactivation.

The account page also shows current-period usage from the same Supabase usage counter that the public edge enforces, including requests used, remaining monthly quota, the active request-per-minute limit, and upgrade recommendations when routing is blocked or usage passes 75%/90% of the current plan quota. The public edge publishes only safe enforcement metadata on `/edge/health` so launch readiness can verify Supabase auth, rate limits, pre-auth generated-key attempt throttling, durable quotas, immediate generated-key revocation, and non-wildcard browser CORS without exposing secrets. The built-in API key test calls the public edge's `/v1/models` endpoint with the generated key so a new customer can separate key, billing, quota, and backend availability problems before configuring an agent. The same account page can send a first browser-side `sage-router/frontier` chat completion with the session-only generated key, so users can prove paid routing works before copying client configuration. The support page gives those same customers a safe escalation path for account, billing, quota, generated-key, 401/402/429/503, reliability, security, and abuse issues without asking them to paste secrets into public channels. The signed-in account page renders a copyable safe support context packet with only plan, routing, quota, generated-key count, verification, first-request, endpoint, and support-path state; it omits prompts, provider credentials, OAuth tokens, generated API keys, private keys, cookies, raw provider responses, and customer data. The account launch checklist mirrors the `$10k MRR` activation funnel by marking signed-in account, generated key, paid routing, public-edge verification, and server-recorded first routed usage as separate steps. The hosted analytics dashboard at `https://app.sagerouter.dev/analytics.html` uses the signed-in account session and calls `/account/analytics`, so customers see only their own privacy-safe routing telemetry while `/analytics` and `/analytics/funnel` remain operator/global endpoints; it also reads the server-derived `/account/usage.activation` state for plan, usage, generated-key, first-request, quota, and routing status to show the next conversion action before or after checkout. Operators can view the private global launch funnel and operator customer review at `https://app.sagerouter.dev/launch-funnel.html` by entering the private admin or analytics token; the browser stores that token only in tab-scoped `sessionStorage` when explicitly requested. The launch funnel endpoint reports waitlist, managed-access beta interest, target provider family, commercial preference, support need, target launch window, and inbound intent demand, signup, generated-key, first-request, paid-conversion, retained-paid, estimated MRR, target attainment, target-aware bottlenecks, conversion actions with owner/surface/success metric, checkout-readiness friction from aggregate checkout unavailable, checkout failure, billing-portal failure, and manual-settlement failure events, anonymous marketing CTA event/plan/source/channel breakdowns, model catalog family/search-bucket demand, browser-visible auth provider state checks for OAuth onboarding, ranked acquisition actions, per-plan `$10k MRR` gaps, and prioritized plan revenue actions without returning email addresses, prompts, message bodies, API keys, provider credentials, OAuth tokens, raw campaign URLs, raw model search text, or raw responses. The managed-access intake also emits anonymous page-view, form-start, submit, and received events with only allowlisted qualification buckets, so one-subscription and Max implementation demand are visible before full contact submission while email and company fields remain confined to the waitlist path. When there are no qualified source/channel clicks yet, the same endpoint seeds zero-click acquisition actions for Gateway migration, GitHub builder traffic, pricing checkout proof, calculator qualification, model catalog activation, quickstart first-request activation, managed-access beta outreach, and launch-plan outreach so the operator view still points at concrete launch motions. The private launch funnel renders deterministic campaign links for those ranked acquisition actions, using only coarse action buckets to generate public UTM URLs rather than replaying raw visitor URLs, and each link can be copied from the dashboard for founder-sales outreach. The operator customer review calls `/admin/customers` through the control-plane edge and shows bounded customer, usage, activation, review flags, operator audit events, and public API-key metadata without raw generated keys, API-key hashes, provider credentials, prompts, or raw responses.

The hosted operator dashboard also includes an operational readiness panel that reads public `/edge/health` and `/pricing` metadata to show live edge health, API-key enforcement, Stripe checkout/portal readiness, and managed-provider launch gating without using the private token or exposing secrets. The public status page mirrors the safe subset of that posture for customers: checkout readiness, activation-email configured-vs-copy-fallback state, managed-access gating, and Browser Integrity Check guidance for raw API clients. It also renders a copyable no-secret operator launch brief that condenses the current `$10k MRR` snapshot, top conversion move, revenue motions, acquisition links, model catalog demand, managed-access demand, checkout friction, no-key signup follow-up count/CTA from `activationFollowUps`, and GitHub OAuth onboarding state for founder-sales and support follow-up without emails, customer IDs, prompts, OAuth tokens, generated API keys, provider credentials, raw campaign URLs, raw model search text, or raw responses. `/analytics/funnel` also exposes `activationFollowUps.sendableQueued`, `reviewOnlyQueued`, `unknownQueued`, and segment lists, plus an aggregate `operatorExecutionPacket` with signup-to-key recovery URLs, segment counts, draft subject/body, telemetry event names, and privacy flags so dashboards, agents, and runbooks can execute the current activation action without scraping browser copy. The operator-only no-key signup queue pulls bounded customer review data from `/admin/customers`, shows generated-key-first follow-up links, and supports per-customer or batch snippet copy so activation outreach can be executed without exposing raw keys, key hashes, prompts, provider credentials, or provider responses. If `SAGE_ROUTER_ACTIVATION_EMAIL_FROM` and `SAGE_ROUTER_RESEND_API_KEY` are configured, the private `POST /admin/customers/send-activation-followups` endpoint can send the same generated-key-first recovery drafts through Resend; without those env vars it fails closed or can be used as a dry run. Public `/pricing` exposes a reduced, secret-free `activationEmailReadiness` object for the status page, while `/analytics/funnel` exposes full secret-free operator command templates in `activationFollowUps.emailReadiness` and `operatorExecutionPacket.emailReadiness` so operators can see whether real sending is configured or whether the copy/mailto fallback is the current path before clicking Send. Copying those snippets records privacy-safe `operator_no_key_followup_*` funnel events, and `/analytics/funnel` rolls them into `activationFollowUps.operatorFollowUpCopies` so queued follow-ups and worked follow-ups are visible separately.

Real activation follow-up sends require the explicit
`sendConfirmation: SEND_ACTIVATION_FOLLOWUPS` field in addition to the private
operator token and trusted Sage Router browser origin. Dry runs do not require
the confirmation field, so operators can verify queued counts, segments, and
plan mix before a configured sender can deliver email.

Programmatic clients should call the API edge directly:

```bash
export OPENAI_BASE_URL=https://api.sagerouter.dev/v1
export OPENAI_API_KEY=sk_sage_your_key_here

curl "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sage-router/frontier",
    "messages": [{"role": "user", "content": "Say hello from Sage Router"}]
  }'
```

Keep anonymous `/v1/*` traffic blocked at the edge. New users should reach account, billing, and API key workflows through the hosted control plane, then use generated API keys for model traffic.

### Sage Router Fusion

Dedicated onboarding: `https://sagerouter.dev/fusion`.

Pro, Max, metered, manual, and operator-enabled customers can use
`sage-router/fusion` as a premium compound model:

```bash
curl "$OPENAI_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "sage-router/fusion",
    "messages": [{"role": "user", "content": "Compare the safest launch options and recommend one."}]
  }'
```

Fusion fans the prompt to a small parallel panel of eligible high-quality
routes, then asks a judge route to synthesize consensus, contradictions, gaps,
and useful details into one OpenAI-compatible response. Lite/free generated
keys receive `402 fusion_plan_required`.

gateway-style clients can also attach Fusion as a premium server tool:

```json
{
  "model": "sage-router/frontier",
  "messages": [{"role": "user", "content": "Survey the strongest arguments for and against this launch."}],
  "tools": [{"type": "sage-router:fusion"}],
  "tool_choice": "required"
}
```

`sage-router:fusion` server-tool entries are handled by
Sage Router before provider routing, so unknown server-tool markers are not
forwarded to downstream providers. `tool_choice: "required"` always invokes
Fusion; automatic tool choice invokes Fusion only for prompts that look like
multi-perspective research, comparison, review, risk, or decision work.
Ordinary function-tool workloads should keep using `sage-router/agentic` or
`sage-router/frontier`. Fusion route telemetry records only selected
provider/model IDs, elapsed times, status, plan, and auth type; it does not
store prompts, panel answers, final answers, API keys, OAuth tokens, provider
credentials, or raw provider responses.

Fusion requests return the canonical `sage-router/fusion` response shape.

Hosted plan limits are exposed from `/pricing` and enforced at the public edge:

| Plan | Price | Included requests | Rate limit |
| --- | --- | ---: | ---: |
| Lite | $6/month | 10,000/month | 60/minute |
| Pro | $30/month | 50,000/month | 180/minute |
| Max | $72/month | 200,000/month | 600/minute |

Customer-facing hosted pricing and plan positioning are published at
`https://sagerouter.dev/pricing`. The buyer-facing launch plan at
`https://sagerouter.dev/launch-plan` turns the $10k MRR operating plan into
plan-mix, activation-funnel, operator-evidence, and managed-access boundary
copy. The launch math and $10k MRR operating plan live in
[docs/saas-launch-10k-mrr.md](docs/saas-launch-10k-mrr.md).
For acquisition and onboarding, `https://sagerouter.dev/quickstart` gives new
customers a first hosted API request path, `https://sagerouter.dev/api-troubleshooting`
gives customers a no-secret 401/402/429/503 diagnostic path,
`https://sagerouter.dev/docs/api-reference` gives OpenAI-compatible customers
the hosted API contract for models, chat completions, Responses API, quotas,
rate limits, and failover signals,
`https://sagerouter.dev/docs/gateway-migration` gives gateway users a
base-URL, generated-key, route-profile, and provider-boundary migration path,
`https://sagerouter.dev/docs/codex` gives Codex CLI users hosted, local port 8790, and Tailnet profile examples, while
`https://sagerouter.dev/agent-native` explains route profiles, Responses API and Codex compatibility, health-aware fallback, BYOK custody, local/Tailnet/hosted deployment choices, and public feature metadata for agent harnesses, and
`https://sagerouter.dev/models` gives prospects a searchable public model catalog backed by safe `/model-catalog` metadata with embedded fallback, including `sage-router/fusion` as a Pro/Max synthesis route, while keeping live `/v1/models` behind generated `sk_sage_*` customer keys and exposing a copyable setup bundle plus always-visible `Create API key next` handoff, and
`https://sagerouter.dev/integrations` gives tool-specific setup choices for
OpenAI-compatible clients, Codex, Cursor, Aider, Continue, Claude Code,
OpenHands, Anthropic-compatible clients, Ollama, local port `8790`, and Tailnet
agents, and
`https://sagerouter.dev/model-routing-calculator` helps prospects estimate
routing savings, escalation rules, fallback gaps, and review rates for one
workflow before they create a hosted API key. The calculator recommends
Lite/Pro/Max from workflow volume, risk flags, and routing score, then carries
that plan into `/account.html?plan=...&start=create_key` for generated-key-first
account setup before checkout. It also reads public `/pricing` billing readiness
metadata so it can show current plan limits while keeping the primary handoff on
the key activation path; clicks record `calculator_key_activation_clicked`.
`https://sagerouter.dev/community-launch-kit` gives the operator copyable,
owner-approved community launch posts, including Show HN, Indie Hackers,
Dev.to, X, and LinkedIn, with measured campaign links and no-secret posting
boundaries for the `$10k MRR` campaign.
`https://sagerouter.dev/founder-sales-kit` gives the operator copyable
no-secret direct outreach for Pro activation, Max implementation review,
gateway migration replies, and calculator follow-up with measured
`utm_source=founder-sales` links for the same `$10k MRR` campaign.

The public homepage now treats hosted signup as live: the homepage primary CTA
is `Create hosted API key`, links directly to `https://app.sagerouter.dev/account.html?plan=pro&start=create_key`, and
the above-the-fold key-first panel leads with `Open account key creator` before
GitHub, email magic-link, or setup-copy fallbacks. It also promotes a no-secret
`Copy 60-second setup bundle` action so visitors can copy hosted edge,
`sage-router/frontier`, and Codex profile setup before signing in. A persistent bottom activation bar keeps `Create API key` and
the 60-second setup path visible after scrolling, using the same privacy-safe
homepage funnel events. It keeps pricing, quickstart, status, model gateway comparison, model catalog,
security, analytics, login, and local GitHub install paths available from the
hero. A route-path discovery grid now links Cursor, coding-agent, Ollama,
OpenAI API, Anthropic API, Gemini API, and self-hosted pages from the homepage so prospects
can start from the tool or provider they already use. The waitlist remains an updates/support path, not the primary conversion
path. When a prospect requests the future one-subscription managed access path
or Max implementation support, pricing and comparison pages link to
`/managed-access`; the private-beta intake stores contact and allowlisted
qualification buckets plus coarse inbound intent from known CTA URLs such as
`?intent=max-implementation` or `?intent=gateway-migration`, so beta,
migration, and implementation demand can be measured without enabling public
provider resale. The intake asks which target provider family and commercial
preference a prospect would buy first, plus support need and target launch
window, including Ollama, OpenAI, and Anthropic private-beta interest for
authorization review. Before staging any managed-provider readiness env, run
`scripts/configure_managed_provider_resale_readiness.sh --check`; the helper
rejects BYOK-only families such as OpenRouter from the managed resale allowlist
and refuses minimum gross-margin thresholds below the launch floor.
Browser-originating waitlist writes are guarded before Supabase inserts: Sage
Router production hosts, Cloudflare Pages previews, local development, and exact
origins configured with `SAGEROUTER_WAITLIST_ALLOWED_ORIGINS` are accepted, and
Turnstile can be enabled as an additional bot challenge. Mutating waitlist
requests must carry an explicit trusted `Origin`; `Referer` is only stored as
sanitized attribution metadata and is not accepted as an origin fallback.

### Hosted Auth

The hosted web app uses Supabase Auth. Email/password signup and email magic links are the baseline onboarding path; OAuth buttons are additive and appear only when the matching provider is enabled in Supabase. GitHub login requires a GitHub OAuth/GitHub App client, not repository permissions:

- Homepage URL: `https://app.sagerouter.dev`
- Authorization callback URL: `https://awtangrlqqsdpksarhwo.supabase.co/auth/v1/callback`

The account, login, and analytics pages read `https://awtangrlqqsdpksarhwo.supabase.co/auth/v1/settings` with the public anon key and hide disabled OAuth providers. When GitHub is disabled but visible in the Supabase settings payload, the UI says GitHub sign-in is pending owner setup and keeps email magic-link/password signup as the supported path. This keeps onboarding usable through email signup while GitHub or other providers are still being configured.

Email signup and magic-link requests attach bounded Supabase user metadata for
launch attribution: selected hosted plan, signup surface, auth method, UTM
source/medium/campaign, referrer host, and landing path. OAuth clicks persist
the same bounded context in browser storage before the provider redirect. This
metadata must not include prompts, workflow text, provider credentials, OAuth
tokens, generated API keys, private keys, raw URLs, cookies, raw provider
responses, or customer data.

Hosted customer actions require verified email by default when
`SAGE_ROUTER_SUPABASE_AUTH_ENABLED=1`. The account page still loads for
signed-in users and shows the verification state. Generated API keys may be
created before verification so the raw setup artifact can be copied once, but
those keys remain blocked from routing until the customer is on an active paid,
trial, or manual plan. Stripe checkout and manual crypto payment intent creation
return `email_verification_required` until Supabase reports
`email_confirmed_at`, `confirmed_at`, or verified email metadata. Set
`SAGE_ROUTER_REQUIRE_VERIFIED_EMAIL=0` only for trusted private/self-hosted
deployments.
When verification is required, the signed-in account page exposes a resend
verification control backed by Supabase Auth. It uses the authenticated account
email returned by the server, does not ask the user to retype an email address,
and records only aggregate resend-click/sent funnel events without storing
email addresses.

Manual crypto payment recovery is customer-scoped. A signed-in customer can
reload the account page and recover their latest pending or settled manual
payment intent through `/billing/crypto/status` without passing an intent id;
the response uses the same public payment shape as explicit status checks and
does not echo customer notes or operator-only billing context.

Browser-originating account and billing mutations are also origin-guarded on
the router before customer, API-key, or billing state is touched. Requests with
no `Origin` header continue to work for CLI and server clients, while present
origins must be Sage Router production hosts, Cloudflare Pages previews, local
development hosts, or exact origins configured with
`SAGE_ROUTER_BROWSER_ALLOWED_ORIGINS`.

The account page also renders hosted plan selection before sign-in from public
`/pricing` metadata. The selected Lite/Pro/Max plan is persisted in browser
storage, shows quota, rate limit, and estimated cost per 1,000 requests, and is
used after login when the customer continues to Stripe checkout.

The public homepage, calculator, pricing, launch plan, quickstart, and
model gateway comparison pages emit anonymous pre-signup page-view, CTA, and
quickstart snippet-copy intent to `/api/funnel-event` so the private launch
funnel can count demand before users create accounts.
The public model catalog also emits page-view, filter, CTA, setup-copy,
setup-next, and bucketed search intent so operators can measure model-family
demand without storing raw search text.
The event path stores
event name, selected plan, sanitized source/target URL, and small metadata
buckets only; it must not store workflow text, prompt bodies, emails, API keys,
or provider credentials. Browser-originating writes are also guarded by allowed
Sage Router origins: production hosts, Cloudflare Pages preview hosts ending in
`.sage-router-web.pages.dev`, local development hosts, and any additional exact
origins configured with `SAGEROUTER_FUNNEL_ALLOWED_ORIGINS`. Mutating funnel
events must carry an explicit trusted `Origin`; `Referer` is stored only as
sanitized attribution metadata and is not accepted as an origin fallback. This
keeps the service-role-backed Supabase insert path from becoming a generic
third-party event sink.

The account and standalone login pages also emit privacy-safe activation and
checkout intent events for signup/login attempts, OAuth clicks, wallet connect
attempts, browser-visible auth-provider state checks, plan selection, API-key
creation, setup snippet-copy intent, public-edge key verification, first browser test request success,
Stripe checkout clicks and returns, Stripe portal clicks and returns, and
crypto/manual payment intent clicks. Pricing,
calculator, model gateway comparison, model catalog, login, account, and homepage
events include only coarse attribution buckets such as source surface, UTM
source/medium/campaign tokens, referrer host, landing path, model family, and
search bucket; the operator launch funnel aggregates those into source-surface,
channel, model-family, and search-bucket counts without returning raw URLs, raw
model search text, emails, prompts, credentials, generated keys, wallet
addresses, provider credentials, OAuth secrets, completion text, or API keys.
Account setup snippet-copy events store only the snippet identifier, not the
copied snippet body or generated key. The private launch funnel rolls those
snippet IDs into setup-copy activation and setup-copy to first-request rates so
operators can tighten Codex/OpenAI snippets without storing customer secrets.
These events help diagnose customer drop-off after login, including whether
GitHub OAuth is still pending while email onboarding is available, and which
launch channels produce demand; Stripe webhooks and Supabase customer state
remain the source of truth for paid conversion, quota, and routing entitlement.
The hosted `/billing` recovery page uses the same event path for account,
pricing, support, troubleshooting, quickstart, and status clicks so payment
recovery friction is visible without collecting invoices, support messages,
secrets, prompts, generated keys, or provider credentials.

Bootstrap the GitHub app and wire Supabase without opening the Supabase dashboard:

```bash
bash scripts/bootstrap_github_supabase_auth.sh
```

Check the current GitHub/Supabase auth state without changing anything:

```bash
bash scripts/check_github_supabase_auth_status.sh
```

The status helper probes the Sage Router Supabase project
`awtangrlqqsdpksarhwo`, verifies the management-side `site_url`, email signup,
and app/API redirect allow-list when `SUPABASE_ACCESS_TOKEN` is present, then
checks browser-visible `/auth/v1/settings` with the project anon key. It prints
only pass/warn/fail status, never OAuth client secrets, anon keys, service-role
keys, or management tokens. A GitHub warning means email onboarding still works
and the owner approval step below is still pending. When GitHub is disabled, the
status helper prints the hosted fallback command with
`SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE=0` while the bootstrapper defaults to
`/home/digit/.openclaw/sage-router-github-auth.env`, so the one-time GitHub
client secret is preserved locally before Supabase is patched.
The auth bootstrap, configurator, and read-only status helper silently load
only the needed variables from `/home/digit/.openclaw/.env` and
`/home/digit/.openclaw/sage-router-github-auth.env` when those variables are
not already set. Override the first path with `SAGEROUTER_SECRET_ENV_FILE` and
the GitHub credential path with `SAGEROUTER_GITHUB_APP_ENV_OUTPUT`.

GitHub requires an owner-approved browser step before it returns app credentials. By default the bootstrap script opens a local browser form, listens on an auto-selected `http://127.0.0.1` port, captures GitHub's one-hour manifest code, exchanges it for the app client id/secret, and patches Supabase Auth in the same run.

On WSL/Windows, the bootstrap copies the generated manifest form into the
Windows temp directory, prints both the Windows and WSL paths, and opens the
Windows `file:///` URL first. This avoids browser handlers that cannot read
`\\wsl.localhost` or WSL `/tmp` paths. If the browser does not appear, open the
printed Windows path manually or use the hosted callback fallback below.
To approve from another Tailnet device, bind the temporary listener on all
interfaces and advertise the machine's Tailnet IP. The script serves the same
one-time GitHub app manifest form at the printed Tailnet URL; open that form
URL, not the callback path directly, because the callback must include GitHub's
temporary `?code=...` after approval:

```bash
SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE_BIND=0.0.0.0 \
SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE_HOST=100.115.208.70 \
bash scripts/bootstrap_github_supabase_auth.sh
```

After patching Supabase, the configurator verifies the management API state
(`site_url`, email auth, GitHub auth, and app/API redirect allow-list entries).
When a public anon/publishable key is available in the environment, it also
checks `/auth/v1/settings` so the browser-visible OAuth buttons match the
management config before the launch readiness script is rerun.
The verification defaults to the Sage Router project ref
`awtangrlqqsdpksarhwo` and the anon key published in the hosted app scripts.
If you override Supabase settings from the environment, prefer
`SAGE_ROUTER_SUPABASE_URL` and `SAGE_ROUTER_SUPABASE_ANON_KEY`; generic
`PUBLIC_*`, `VITE_*`, or `SUPABASE_ANON_KEY` values are accepted only when the
anon-key JWT belongs to the same project ref, which avoids false results on
machines that also work with other Supabase projects.

If local capture is not available, fall back to the hosted callback page. After approving the app, GitHub redirects to `/github-app-manifest` with a temporary one-hour `code`; the page is marked `noindex,nofollow`, explains that the browser only holds the short-lived manifest code, and prints the exact local exchange command. Rerun the same script with the full callback URL or the raw code:

```bash
SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE=0 \
  bash scripts/bootstrap_github_supabase_auth.sh
bash scripts/bootstrap_github_supabase_auth.sh 'https://app.sagerouter.dev/github-app-manifest?code=...'
# or:
SAGEROUTER_GITHUB_APP_MANIFEST_CODE=... \
  bash scripts/bootstrap_github_supabase_auth.sh
```

If the Supabase Management API token is being refreshed or debugged, preserve
the one-time GitHub client secret before the Supabase patch runs:

```bash
bash scripts/bootstrap_github_supabase_auth.sh 'https://app.sagerouter.dev/github-app-manifest?code=...'
```

The callback page prints the exact command, including env loading, credential
preservation to `/home/digit/.openclaw/sage-router-github-auth.env`, and the
launch readiness rerun. It also shows the raw temporary code as a fallback if
clipboard access is blocked by the browser. If the code expires, rerun
`SAGEROUTER_GITHUB_APP_LOCAL_CAPTURE=0 bash scripts/bootstrap_github_supabase_auth.sh`
and approve the app again.

If a GitHub OAuth App already exists, pass its credentials directly:

```bash
SAGEROUTER_GITHUB_CLIENT_ID=... \
SAGEROUTER_GITHUB_CLIENT_SECRET=... \
bash scripts/configure_supabase_github_auth.sh
```

Check the current hosted launch gates with:

```bash
set -a; source /home/digit/.openclaw/.env; set +a
scripts/check_sagerouter_launch_readiness.sh
```

Check activation email sender readiness without writing or printing secrets:

```bash
set -a; source /home/digit/.openclaw/.env; set +a
scripts/configure_activation_email_sender.sh --check
```

The activation email preflight reports public `/pricing` readiness, Cloud Run
binding presence, and local apply-input presence only as booleans or binding
names. For the fastest hosted recovery path on the live Cloud Run deployment,
reuse the existing Supabase auth email sender:

```bash
SAGE_ROUTER_ACTIVATION_EMAIL_PROVIDER=supabase-recovery \
scripts/configure_activation_email_sender.sh
```

The Supabase recovery provider sends operator-confirmed password-recovery
emails through the existing Cloud Run Supabase URL/anon-key bindings and
redirects users back to the Sage Router account/key setup flow. For custom
generated-key recovery copy, use the Resend provider instead; when sender inputs
are present, the script verifies Resend API access and that the sender domain is
verified/sending-enabled before binding Cloud Run secrets. The setup path does not print sender values or Resend API-key values. Resend follow-up sends use an idempotency key so an operator retry does not double-send the same generated-key recovery draft.

Stage the non-secret one-subscription managed-access controls without enabling
public resale or writing the private provider-cost model:

```bash
scripts/configure_managed_provider_resale_readiness.sh --stage-public-controls
scripts/configure_managed_provider_resale_readiness.sh --check
```

That binds the provider-resale terms URL, margin-policy URL, resale-eligible
allowlist (`ollama,openai,anthropic`), disabled public-enable flag, and minimum
gross-margin floor. The remaining launch blockers should be the explicit terms
acknowledgment, an operator-held provider authorization evidence reference, and
private cost model / positive unit-economics review. The authorization reference
is never printed in public metadata; `/pricing` exposes only whether it is
configured.

Before writing the private provider-cost model to Secret Manager, run the
secret-safe unit-economics preflight with the candidate cost in the environment:

```bash
SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS='REVIEWED_PRIVATE_COST' \
scripts/configure_managed_provider_resale_readiness.sh --unit-economics
```

The preflight reuses the same plan math as `/pricing`, returns nonzero when any
fixed API plan fails the minimum gross-margin threshold, and prints only
candidate presence, public plan revenue, derived max-safe provider-cost
thresholds, and pass/fail status. It does not print the candidate cost, exact
gross-margin percentages, provider credentials, prompts, raw provider
responses, or customer data.

If the readiness check reports Cloudflare `403` / `1010` before the Sage Router
auth gate, use [docs/cloudflare-api-bic-skip.md](docs/cloudflare-api-bic-skip.md)
to verify or apply the host-scoped Browser Integrity Check skip for
`api.sagerouter.dev`. The launch gate fails when OpenAI-compatible SDK-style
clients cannot reach the guided Sage Router auth response. If only raw default
Python `urllib` is blocked and SDK-style probes reach auth, readiness reports a
warning until the Cloudflare token has Rulesets permissions to verify the rule.

The readiness check verifies the public API edge, visible edge-layer headers with redacted public upstream IDs, Supabase auth mode, authenticated rate limits, pre-auth generated-key attempt throttling, durable edge quotas, immediate generated-key revocation, non-wildcard browser CORS, lowest-latency retry failover metadata on `/edge/health`, redacted public health snapshots without internal upstream URLs, anonymous auth gating, the API-only browser/dashboard boundary on `api.sagerouter.dev`, browser CORS preflight for the hosted API-key verification, browser first-routed-request, and operator launch-funnel flows, hosted pricing metadata including secret-free Stripe checkout readiness, configured activation email sender readiness, configured Lite/Pro/Max checkout plans, billing portal readiness, verified-email billing requirements, generated-key activation metadata, and absence of leaked Stripe price IDs or secret tokens, the managed provider access guard, provider-family BYOK boundary, direct origin auth gating, Supabase management auth settings, public browser-visible Supabase auth settings with email and GitHub OAuth enabled, quota, funnel-event, and operator-audit schema, hosted login/account/GitHub callback/operator launch funnel pages, hosted security headers, the public security/trust/support and terms/privacy/acceptable-use pages, the provider-resale terms and margin-policy prerequisite pages, the managed-access private beta intake page, the API quickstart, the API troubleshooting page, the hosted API reference, the Gateway migration guide, the Codex setup page, the agent-native routing page, the integrations index, the dedicated billing recovery page, the model routing calculator, the public launch plan, the operator-only privacy-safe `/analytics/funnel` endpoint including managed-access beta demand fields, marketing source/channel attribution, and target-aware bottlenecks, the bounded operator `/admin/customers` review endpoint with secret-free audit events and without raw keys or hashes, the non-mutating waitlist health endpoint on `SAGEROUTER_APP_BASE_URL` (default `https://app.sagerouter.dev`), optional Cloudflare Turnstile waitlist configuration, and the marketing comparison/migration/pricing/billing/model/quickstart/troubleshooting/API-reference/Codex/agent-native/integrations/launch-plan pages on `SAGEROUTER_MARKETING_BASE_URL` (default `https://sagerouter.dev`). Use `scripts/configure_activation_email_sender.sh` to bind the Resend sender secrets before treating signup recovery as launch-ready; without it, `/pricing` still exposes fallback-only status but readiness fails the activation sender gate. By default, `publicLaunch.managedProviderAccess.enabled` must be false. If `SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED=1`, readiness requires `SAGEROUTER_PROVIDER_RESALE_TERMS_URL`, `SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED=1`, `SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS`, `SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL`, a positive `SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS`, positive unit economics across fixed API plans with `SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT` at 30 or higher, derived max-safe-cost thresholds in public metadata, durable quota/rate-limit enforcement, generated-key revocation, operator abuse review, durable operator audit events, and the managed-access acceptable-use boundary before treating bundled provider access as launchable. Use `scripts/configure_managed_provider_resale_readiness.sh` to stage the provider terms URLs, allowlist, and private provider-cost model through Cloud Run/Secret Manager; it keeps public managed resale disabled unless `SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC=1` is explicitly set. Until those checks pass, public metadata reports `requested: true`, `readinessSatisfied: false`, `enabled: false`, the remaining `missingControls`, provider-family readiness, one-subscription readiness, and the no-secret `readinessSetup` command packet that keeps OpenRouter BYOK-supported but outside bundled managed resale. The direct-origin probe uses `SAGEROUTER_ORIGIN_BASE_URL` when set; otherwise it auto-discovers the Cloud Run URL from `SAGEROUTER_CLOUD_RUN_PROJECT`/`SAGEROUTER_CLOUD_RUN_REGION`/`SAGEROUTER_CLOUD_RUN_SERVICE`, defaulting to the live hosted service.

To refresh the current `$10k MRR` operating snapshot without opening the
operator dashboard or printing secrets, run:

```bash
scripts/summarize_sagerouter_launch_funnel.sh --days 30
```

The helper reads `SAGE_ROUTER_ANALYTICS_TOKEN`, `SAGE_ROUTER_OPERATOR_TOKEN`,
or `SAGE_ROUTER_API_KEY` from the environment or
`SAGEROUTER_SECRET_ENV_FILE`/`/home/digit/.openclaw/.env`, calls
`/analytics/funnel`, and prints only aggregate activation, acquisition, revenue,
and privacy fields. Use its output to update
`docs/launch/distribution-tracker.md` before broad community posting or
activation outreach. Pass `--json` when another script needs the same bounded
data; consume `activationQueue` for no-key follow-up counts, sendable and
review-only segments, dry-run coverage, sent-recipient counts, and
approval-required state.

Use the public deploy helper to avoid branch/digest drift between the static
site and hosted API:

```bash
set -a; source /home/digit/.openclaw/.env; set +a
scripts/deploy_sagerouter_public.sh
```

The helper builds Cloudflare Pages from a clean temporary copy so local
`node_modules` or Dropbox permissions cannot affect the production build, then
deploys project `sage-router-web` to production branch `main` and reruns launch
readiness. To update Cloud Run in the same pass, set an immutable release image
digest:

```bash
GHCR_IMAGE_DIGEST=sha256:... scripts/deploy_sagerouter_public.sh
```

If `SAGEROUTER_DEPLOY_CLOUD_RUN=1` is set without a digest, the helper resolves
the latest successful GitHub Actions `Release image` digest from the run log and
deploys that digest through the Artifact Registry GHCR remote cache.

Monthly API-key quotas require the Supabase usage counter table and RPC. Apply
the idempotent migration through the Supabase Management API before enabling
`SAGE_ROUTER_EDGE_QUOTA_ENABLED=1`:

```bash
set -a; source /home/digit/.openclaw/.env; set +a
scripts/apply_supabase_quota_schema.sh
scripts/check_sagerouter_launch_readiness.sh
```

When a generated customer key exhausts its monthly quota, the public edge
returns HTTP `402` with `X-Quota-Period`, `X-Quota-Limit`, `X-Quota-Used`,
`X-Quota-Remaining`, and `X-Quota-Reset` headers plus a secret-free JSON body
containing the current plan, usage, reset epoch, account upgrade URL, billing
URL, support URL, and status URL. Edge quota infrastructure failures remain
HTTP `503` and point customers to status/support rather than suggesting that a
plan upgrade will fix an operator-side issue.

Stripe checkout reuses an existing `stripe_customer_id` when a customer is already linked, the account page exposes Stripe's customer billing portal after checkout, and Stripe webhook retries are idempotent by `event_id`. Checkout completion only activates generated-key routing when the signed Checkout Session reports `payment_status=paid` or `payment_status=no_payment_required`; unpaid or missing payment status events are recorded but do not grant or change routing entitlement. Signed subscription lifecycle webhooks update customer routing status: active/trialing subscriptions enable generated-key routing, canceled subscriptions disable routing, and failed or uncollectible invoices mark the customer `past_due`. Later signed `invoice.payment_succeeded`, `invoice.paid`, or `checkout.session.async_payment_succeeded` events restore active generated-key routing after resolving the existing Stripe customer binding and deriving the Sage Router plan from invoice line price IDs or checkout metadata, unless the customer has been operator-suspended. Subscription create/update webhooks derive the effective Sage Router plan from Stripe subscription item price IDs first, then fall back to webhook metadata or the current customer plan, so Stripe portal plan changes do not leave quota and routing state on a stale plan. Webhooks also verify that `metadata.customer_id`/`client_reference_id` agrees with any existing `stripe_customer_id` binding before changing billing state, so stale or misdirected Stripe metadata cannot reassign another customer's quota or routing entitlement. Apply `supabase/migrations/20260619034200_stripe_webhook_idempotency.sql` anywhere the SaaS tables already exist so duplicate signed webhook deliveries cannot create duplicate payment event rows.

For the existing GCP deployment notes, see [deploy/gcp](deploy/gcp/README.md). For the privacy-preserving relay design where customer credentials stay on the user's machine, see [docs/cloud-tunnel](docs/cloud-tunnel/README.md).

### Configure Your Tools

Point any OpenAI-compatible tool at Sage Router:

```bash
export OPENAI_BASE_URL=http://localhost:8790/v1
export OPENAI_API_KEY=irrelevant  # Sage Router uses your configured provider auth
```

Or for Gemini CLI:

```bash
export GOOGLE_GEMINI_BASE_URL=http://localhost:8790
export GEMINI_API_KEY=routed
```

Or for Anthropic tools:

```bash
export ANTHROPIC_BASE_URL=http://localhost:8790
export ANTHROPIC_API_KEY=irrelevant
```

### Codex CLI on port 8790

Codex CLI can use Sage Router through the OpenAI Responses-compatible endpoint. The public setup guide is published at `https://sagerouter.dev/docs/codex`. For local port 8790, add the provider and profile to `~/.codex/config.toml`:

```toml
[model_providers.sage-router]
name = "Sage Router"
base_url = "http://127.0.0.1:8790/v1/"
env_key = "SAGE_ROUTER_API_KEY"
wire_api = "responses"

[profiles.sage-router-frontier]
model_provider = "sage-router"
model = "sage-router/frontier"
```

Run Codex with:

```bash
export SAGE_ROUTER_API_KEY=local-router
codex --profile sage-router-frontier
```

The `sage-router/frontier` model name selects the bundled `frontier` routing profile from `router-profiles.json`.

Sage Router also normalizes Codex/OpenClaw goal traffic. Raw `/goal ...`
messages and Codex `<codex_internal_context source="goal">` blocks are treated
as persistent user-provided objective context instead of ordinary slash-command
text, then routed with high-quality, reasoning-capable, long-context agent
requirements.

---

## Integration Guides

- [Codex CLI](docs/integrations/codex.md)
- [Claude Code](docs/integrations/claude-code.md)
- [OpenClaw](docs/integrations/openclaw.md)
- [Hermes](docs/integrations/hermes.md)
- [Pi agents](docs/integrations/pi.md)
- [Cursor](docs/integrations/cursor.md)
- [Aider](docs/integrations/aider.md)
- [Continue](docs/integrations/continue.md)
- [OpenHands](docs/integrations/openhands.md)
- [Ollama and Ollama Cloud](docs/integrations/ollama.md)
- [NVIDIA NIM / NVIDIA Cloud](docs/integrations/nvidia-nim.md)
- [OpenAI-compatible clients](docs/integrations/openai-compatible.md)
- [Anthropic-compatible clients](docs/integrations/anthropic-compatible.md)
- [Harness fallback](docs/integrations/harness-fallback.md)

---


## OpenClaw Codex OAuth

Sage Router connects directly to `chatgpt.com/backend-api/codex` using the same OpenAI OAuth token stored in your OpenClaw `auth-profiles.json`. No API key needed when an auth profile is present — it reads the current ChatGPT session JWT from `~/.openclaw/agents/main/agent/auth-profiles.json` and refreshes it on each request.

Sage Router intentionally does not implement its own `auth.openai.com/codex/device` OAuth route. Use the official Codex/OpenClaw sign-in flow, then import the resulting OpenClaw auth profile or pass an access token through environment.

To use:

```bash
# Force a request through the Codex backend
curl http://localhost:8790/v1/chat/completions \
  -H "Authorization: Bearer local" \
  -d '{"model":"openai-codex/gpt-5.5","messages":[{"role":"user","content":"Hello"}]}'
```

The `openai-codex` provider is enabled by default. Models: `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-pro`.

Key env vars:
- `SAGE_ROUTER_OPENAI_CODEX_AUTH_PROFILE_PATH` — path to `auth-profiles.json` (default: `~/.openclaw/agents/main/agent/auth-profiles.json`)
- `SAGE_ROUTER_OPENAI_CODEX_AUTH_PROFILE_PATHS` — comma-separated auth profile paths, useful for container app-data layouts
- `OPENAI_CODEX_API_KEY`, `OPENAI_CODEX_ACCESS_TOKEN`, or `CODEX_ACCESS_TOKEN` — fallback OAuth access token (used if auth-profiles is unavailable)

## Config Dashboard

Local, Tailnet, Umbrel, and Docker installs ship a built-in web dashboard at
the root URL (`/`). Open that private install URL in a browser to see:

- Provider health status and latency
- Available models per provider
- Usage analytics
- Provider enable/disable toggles
- API key management
- Learned model modalities with per-model edit/reset controls

Hosted/CDN deployments can make learned modalities persistent across all
router nodes by applying
`supabase/migrations/20260626003000_model_modalities.sql` and enabling
`SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED=1` with Supabase service
credentials. When `SAGE_ROUTER_SUPABASE_MIRROR_ENABLED=1`, the shared ledger is
enabled by default and nodes merge observations from the
`sage_router_model_modalities` table periodically.
The Cloudflare API Worker also records `X-Sage-Router-Modalities` from
successful routed responses into the same RPC when Supabase service credentials
are configured, so observations made at CDN edges are shared by every backend
node. Public Tailnet edge health exposes a secret-free
`modelModalities.sharedEnabled` readiness bit, and the Cloudflare Worker only
selects public-edge-ready origins that prove the shared RPC is configured.

For programmatic clients (sending `Accept: application/json`), the private
install root URL returns the JSON API descriptor instead. The dashboard is also
available at `/dashboard` on private installs.

Hosted SaaS uses a stricter browser boundary: `https://api.sagerouter.dev/`
and `https://api.sagerouter.dev/dashboard` return JSON auth/onboarding guidance
instead of serving browser UI. Customer login, account, usage analytics, and
operator launch-funnel dashboards live on `https://app.sagerouter.dev`, while
model traffic uses generated `sk_sage_*` API keys at
`https://api.sagerouter.dev/v1`.

### outputProviderPrefix

Enable `SAGE_ROUTER_SHOW_MODEL_PREFIX=1` only for short manual diagnostics to
prefix every chat response with `[provider/model]` so you can see which model
answered:

```
[openai-codex/gpt-5.5] Here is the response...
```

Keep this disabled for Codex, OpenClaw, Discord, and other conversational
clients. Those clients store assistant messages in history, so visible routing
labels can be replayed by later turns and appear as duplicated content. Provider
and model attribution remain available through Sage Router metadata, logs, and
debug responses without adding labels to assistant text. Sage Router also strips
known assistant replay artifacts such as duplicated `[provider/model]` labels and
`[tool calls omitted]` placeholders before forwarding history or Responses output
to Codex/OpenClaw clients, while preserving structured tool calls.

For Docker Desktop Codex setups that need a local Responses-to-Chat shim, use
[`scripts/codex_sage_router_proxy.py`](scripts/codex_sage_router_proxy.py) as
the canonical source for the mounted proxy file. The shim preserves
`function_call` / `function_call_output` pairs, drops orphan tool outputs without
usable call ids, and applies the same visible replay sanitization before history
is sent back through Sage Router.

If a Codex JSONL session was already polluted before this sanitizer ran, repair
only assistant-visible replay fields with:

```bash
python3 scripts/sanitize_codex_session_prefix_replay.py --in-place ~/.codex/sessions/YYYY/MM/DD/rollout-...jsonl
```

## Supported API Formats

| Endpoint | Format | Used By |
|----------|--------|---------|
| `POST /v1/responses` | OpenAI Responses | Codex CLI custom providers |
| `POST /v1/chat/completions` | OpenAI | OpenAI SDK, Aider, Continue, Zed |
| `POST /v1/messages` | Anthropic | Cursor, Claude Code, Claude Desktop |
| `POST /v1beta/models/{model}:generateContent` | Google | Gemini CLI |
| `POST /v1beta/models/{model}:streamGenerateContent` | Google | Gemini CLI (streaming) |
| `GET /v1beta/models` | Google | Gemini CLI (model discovery) |
| `POST /chat/completions` | OpenAI | Legacy/short path |

---

## How Routing Works

Sage Router analyzes every request for:

1. **Intent**: CODE, CHAT, REASONING, CREATIVE, REFACTOR, DOCUMENTATION
2. **Complexity**: LOW, MEDIUM, HIGH, UNKNOWN
3. **Requirements**: reasoning, json, tools, longContext, streaming
4. **Thinking level**: off, low, medium, high

Then it scores all available models and selects the optimal chain:

```
Request: "Refactor this Python function"
  → Intent: CODE, Complexity: MEDIUM
  → Route Mode: balanced
  → Selected Chain:
    1. ollama/glm-5.1:cloud            (best score for CODE + available)
    2. openai-codex/gpt-5.5            (fallback)
    3. ollama/kimi-k2:cloud            (fallback)
    4. openai/gpt-4.1                  (last resort)
```

If the first model fails or times out, it automatically tries the next. No manual retry needed.

### Model Selection Pseudocode

The core selection path lives in `router.py` across `normalize_requirements`,
`prepare_route`, `select_model`, `score_provider_model`, and `route_request`.
In pseudocode:

```text
function route_request(payload):
    messages = payload.messages
    thinking = normalize_thinking(payload.reasoning / payload.thinking)
    route_mode = payload.routeMode or "balanced"
    requirements = normalize_requirements(payload)

    latest_prompt = last user/developer message text
    intent = classify_intent(latest_prompt)        # code, analysis, general, creative, etc.
    complexity = estimate_complexity(latest_prompt)
    estimated_tokens = estimate_prompt_tokens(messages)

    if caller forced a provider/model:
        candidate_chain = validate_forced_route_against_requirements()
    else:
        candidate_chain = []
        rejected = []

        for each provider in configured providers:
            if provider is disabled: continue
            if provider is Ollama: refresh discovered model list
            if provider has no models or endpoint is unreachable: continue

            for each model in provider.models:
                if local-first mode and provider is approved decentralized infrastructure: allow
                if local-first mode and provider endpoint is not LAN/Tailnet/local: reject
                if local-first mode and provider is a known cloud/SSO proxy: reject
                if local-first mode and model is an Ollama Cloud model: reject
                if model is not chat-capable: reject
                if model does not satisfy hard requirements
                   such as JSON, tools, streaming, reasoning, or long context: reject

                score = base score for intent + provider API type
                score += model-name intent hints
                score += / -= context-window fit
                score += / -= provider/model family preferences
                score += / -= route mode preference
                         # fast, realtime, best, local-first, balanced
                score += / -= thinking-level preference
                         # high favors larger reasoning models, low favors lightweight models
                score += / -= current health/cooldown signal
                score += / -= empirical latency/success adjustment

                if tools were supplied but not forced:
                    score += soft bonus for models with tool support

                candidate_chain.append((score, provider, model))

        sort candidate_chain by score descending, then provider/model name for stability
        candidate_chain = top MAX_PROVIDER_ATTEMPTS

    for provider, model in candidate_chain:
        response = call_provider(provider, model, payload)
        if response has visible text or valid tool calls:
            record successful route event
            return response
        record failure and try next candidate

    record failed route event
    return provider_failure_error
```

Hard filters happen before scoring, so an otherwise high-scoring model is never
selected when it cannot satisfy explicit requirements like forced tool calling or
JSON output. Soft preferences, such as attached optional tools, influence the
score without unnecessarily shrinking the candidate pool.

---

## Supported Providers

Configure any number of providers in `openclaw.json` or via environment variables:

### Ollama (Local)

```json
{
  "providers": {
    "ollama": {
      "baseUrl": "http://localhost:11434",
      "models": ["auto-discover"],
      "api": "ollama"
    }
  }
}
```

Models are auto-discovered via `/api/tags`.

### Anthropic (Claude)

```json
{
  "providers": {
    "anthropic": {
      "baseUrl": "https://api.anthropic.com",
      "apiKey": "${ANTHROPIC_API_KEY}",
      "models": ["claude-opus-4", "claude-sonnet-4", "claude-haiku-4"],
      "api": "anthropic-messages"
    }
  }
}
```

**Pro tip**: Route Claude subscription usage through [Dario](https://github.com/askalf/dario) to avoid burning API credits when available.

### OpenAI

```json
{
  "providers": {
    "openai": {
      "baseUrl": "https://api.openai.com/v1",
      "apiKey": "${OPENAI_API_KEY}",
      "models": ["auto-discover"],
      "api": "openai-completions"
    }
  }
}
```

Models are auto-discovered via `/v1/models`.

### OpenRouter (BYOK)

OpenRouter remains a supported OpenAI-compatible provider. Configure it only
with an authorized customer-controlled key; Sage Router does not sell bundled
OpenRouter access. OpenRouter models stay discoverable and routable through
the BYOK-compatible provider path, but OpenRouter does not count as a managed
provider resale family for Sage Router subscription packaging unless a separate
provider authorization is added later.

```json
{
  "providers": {
    "openrouter": {
      "baseUrl": "https://openrouter.ai/api/v1",
      "apiKey": "${OPENROUTER_API_KEY}",
      "models": ["auto-discover"],
      "api": "openai-completions"
    }
  }
}
```

Models are auto-discovered via `/v1/models`. Set
`SAGE_ROUTER_DISABLED_PROVIDERS` only for operational failures; do not disable
OpenRouter merely to keep it out of Sage Router's managed subscription
packaging. Set `SAGE_ROUTER_OPENROUTER_FREE_ONLY=1` to keep discovery
constrained to free model IDs when using that account mode.


### Darkbloom

Darkbloom is OpenAI-compatible at `https://api.darkbloom.dev`. If `DARKBLOOM_API_KEY` is present in `~/.openclaw/.env` or the skill-local `.env`, Sage Router loads it automatically through the bundled `darkbloom` provider profile.

```json
{
  "providers": {
    "darkbloom": {
      "baseUrl": "https://api.darkbloom.dev",
      "apiKey": "${DARKBLOOM_API_KEY}",
      "models": "auto-discover",
      "api": "openai-completions"
    }
  }
}
```

Models are auto-discovered via `/v1/models`. Chat requests route through `/v1/chat/completions`.

### Google Gemini

```json
{
  "providers": {
    "google": {
      "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
      "apiKey": "${GEMINI_API_KEY}",
      "models": ["auto-discover"],
      "api": "google-generative-ai"
    }
  }
}
```

Models are auto-discovered via the Gemini API.

### GitHub Copilot

```json
{
  "providers": {
    "github-copilot": {
      "baseUrl": "https://api.githubcopilot.com",
      "apiKey": "${GITHUB_COPILOT_TOKEN}",
      "models": ["auto-discover"],
      "api": "openai-completions"
    }
  }
}
```

Models are auto-discovered via Copilot's `/v1/models`.
```

### xAI (Grok)

**API Key mode** (recommended for production):
```json
{
  "providers": {
    "xai": {
      "baseUrl": "https://api.x.ai/v1",
      "apiKey": "${XAI_API_KEY}",
      "models": ["auto-discover"],
      "api": "openai-completions"
    }
  }
}
```
Models are auto-discovered via `/v1/models`. Supports tool calling, streaming, and passthrough.

### NVIDIA NIM / NVIDIA Cloud

```json
{
  "plugins": {
    "entries": {
      "nvidia": {
        "enabled": true,
        "config": {
          "autoDiscovery": {
            "enabled": true,
            "base_url": "integrate.api.nvidia.com/v1",
            "api_key": "$NVIDIA_API_KEY"
          }
        }
      }
    }
  }
}
```

Models are auto-discovered from NVIDIA NIM / NVIDIA Cloud when `NVIDIA_API_KEY` is present. This is useful for GPU-accelerated hosted inference and NVIDIA-backed model endpoints without changing agent configuration.

### OpenClaw Gateway

```json
{
  "providers": {
    "openai-codex": {
      "baseUrl": "http://127.0.0.1:8790",
      "models": ["auto-discover"],
      "api": "openclaw-gateway"
    }
  }
}
```

Models are auto-discovered via the gateway's `/v1/models` endpoint.


### OpenClaw Codex OAuth

No config needed — Sage Router reads your ChatGPT OAuth JWT from `~/.openclaw/agents/main/agent/auth-profiles.json` automatically. Models: `gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.4-pro`.

Force via model name: `"model": "openai-codex/gpt-5.5"`.
---

## Docker / Production deployment
The pre-built image is available at `ghcr.io/earlvanze/sage-router-public` (public). It bundles Sage Router plus Dario and the config dashboard.

Mount an app-owned config directory and add provider or Codex credentials from the dashboard:

```bash
docker run -p 8790:8790 \
  -v sage-router-config:/config \
  -v sage-router-ollama:/root/.ollama \
  ghcr.io/earlvanze/sage-router-public:v3.28.11
```

Provider credentials and imported Codex auth JSON are written under `/config`.
Do not mount another app's private state or a host user's home directory for
auth; copy/import compatible config through the Sage Router setup flow instead.

Or build from source:

```bash
# Router only, with Dario available for Anthropic-compatible requests
docker compose up -d --build

# Router + llama.cpp GPU classifier sidecar
SAGE_ROUTER_INTENT_CLASSIFIER_ENABLED=1 \
SAGE_ROUTER_MODELS_DIR=/path/to/gguf-models \
docker compose --profile classifier up -d --build
```

Key production flags:

```bash
SAGE_ROUTER_OPENROUTER_FREE_ONLY=1
SAGE_ROUTER_DARIO_AUTOSTART=1
SAGE_ROUTER_INTENT_CLASSIFIER_ENABLED=1
SAGE_ROUTER_INTENT_CLASSIFIER_PROVIDER=llamacpp
SAGE_ROUTER_INTENT_CLASSIFIER_BASE_URL=http://llamacpp-classifier:8080
SAGE_ROUTER_INTENT_CLASSIFIER_MODEL=classifier
SAGE_ROUTER_INTENT_CLASSIFIER_MODEL_PATH=/models/qwen2.5-0.5b-instruct-q4_K_M.gguf
SAGE_ROUTER_INTENT_CLASSIFIER_N_GPU_LAYERS=999
```

The classifier backend speaks OpenAI-compatible llama.cpp server API (`/v1/chat/completions`), so it can be run as a sidecar, on Cyber GPU, or replaced by any compatible local inference server.


## Provider Feature Matrix

| Provider | Dynamic Discovery | Force Model | Passthrough | Auth Method |
|----------|-------------------|-------------|-------------|-------------|
| **Ollama** | ✅ `/api/tags` | ✅ | ✅ | Local socket |
| **Google Gemini** | ✅ `/v1beta/models` | ✅ | ✅ | API key |
| **Anthropic** | ✅ Via Dario | ✅ | ✅ | API key |
| **OpenAI** | ✅ `/v1/models` | ✅ | ✅ | API key |
| **GitHub Copilot** | ✅ `/v1/models` | ✅ | ✅ | Token |
| **NVIDIA NIM / Cloud** | ✅ auto-discovery | ✅ | ✅ | API key |
| **OpenClaw Gateway** | ✅ `/v1/models` | ✅ | ✅ | Gateway token |
| **OpenClaw Codex OAuth** | ✅ auto-profile | ✅ | ✅ | ChatGPT JWT (auth-profiles) |
| **xAI/Grok (API)** | ✅ `/v1/models` | ✅ | ✅ | API key |
| **xAI/Grok (SSO)** | ❌ SSO proxy | ❌ | ❌ | Cookie/SSO |

**Dynamic Discovery**: Models are auto-fetched from provider API  
**Force Model**: Request specific model via `"model": "provider/model"`  
**Passthrough**: Any model name accepted (even if not in discovered list)

---

## Route Modes

Control how Sage Router selects models:

| Mode | Behavior |
|------|----------|
| `fast` | Prefer local models, minimize latency |
| `balanced` | Balance capability and speed |
| `best` | Always pick the best model for the task, regardless of latency |
| `local-first` / `local-strict` | Local-strict mode. Only use local, LAN, Tailnet, or approved decentralized provider endpoints. Reject centralized Internet APIs such as OpenAI, Anthropic/Dario, Google, NVIDIA Cloud, Copilot, hosted model gateways, etc. Darkbloom is allowed as decentralized infrastructure. Ollama models ending in `:cloud` are still excluded even if the Ollama endpoint is localhost. |

Set via request: `{"route": "fast"}` or header: `X-Route-Mode: fast`

---

## Thinking Levels

Control reasoning depth per request:

| Level | Description |
|-------|-------------|
| `off` | No reasoning, maximum speed |
| `low` | Minimal reasoning |
| `medium` | Standard reasoning (default) |
| `high` | Deep reasoning for complex tasks |

Set via request: `{"thinking": "high"}` or `{"reasoning": "high"}`

## Debug Mode

To surface routing info back in the response payload, send:

```json
{
  "debug": true
}
```

or:

```json
{
  "routeDebug": true
}
```

Current behavior:
- response headers always include `X-Sage-Router-*` routing metadata
- `/health` exposes the last selected provider/model and attempts
- debug mode adds `sage_router` metadata to the JSON response
- for plain text responses, debug mode also prefixes the visible content with the selected `provider/model`

---

## Health Endpoint

```bash
curl http://localhost:8790/health
```

Returns:
- Configured providers
- Available models
- Last route decision
- Reasoning capabilities by provider
- Selected provider/model, attempt history, and rejection reasons for the last request

Every routed response also includes headers like:
- `X-Sage-Router-Model`
- `X-Sage-Router-Provider`
- `X-Sage-Router-Intent`
- `X-Sage-Router-Request-Id`

Use these when you need to know exactly which model answered.

## Streaming Note

Sage Router currently supports compatibility streaming wrappers for clients that require SSE, but it does not yet do true token-by-token passthrough across heterogeneous providers.

That means stream-shaped responses work for client compatibility, but they may still arrive buffered after the selected provider finishes.

---

## Why Sage Router?

Sage Router was built because switching API keys between coding agents is tedious, burning Claude API credits on trivial tasks is wasteful, and configuring models in 3 different places is fragile.

With OpenClaw Codex OAuth, you get ChatGPT Pro/Codex access through your existing session token — no API key, no gateway subprocess, no stale tokens. The router reads the JWT directly from your OpenClaw auth profile and sends it to `chatgpt.com/backend-api/codex`.

## Configuration

### Environment Variables

```bash
# Provider API keys (used for auto-discovery)
ANTHROPIC_API_KEY=sk-...
OPENAI_API_KEY=sk-...
GEMINI_API_KEY=AIza...
NVIDIA_API_KEY=nvapi-...
OLLAMA_HOST=http://localhost:11434

# OpenClaw Codex OAuth (chatgpt.com/backend-api/codex)
SAGE_ROUTER_OPENAI_CODEX_AUTH_PROFILE_PATH=~/.openclaw/agents/main/agent/auth-profiles.json
CODEX_ACCESS_TOKEN=                # fallback OAuth access token when no auth profile is mounted

# Router behavior
SAGE_ROUTER_DEFAULT_MODE=balanced
SAGE_ROUTER_TIMEOUT=60
SAGE_ROUTER_SHOW_MODEL_PREFIX=0   # diagnostic only; keep off for chat clients
SAGE_ROUTER_DISABLED_PROVIDERS=    # comma-separated: ollama-cloud,anthropic,...
```
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434",
        "models": [{"id": "llama3.2:latest", "name": "Llama 3.2"}],
        "api": "ollama"
      },
      "anthropic": {
        "baseUrl": "https://api.anthropic.com",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [{"id": "claude-sonnet-4", "name": "Claude Sonnet"}],
        "api": "anthropic-messages"
      }
    }
  }
}
```

---

## Development

```bash
# Run locally
python3 router.py --port 8790

# Run tests
pytest tests/

# Enable debug logging
LOG_LEVEL=DEBUG python3 router.py
```

---

## Roadmap

### Completed

- [x] Multi-modal support (vision-capable model detection and image payload routing)
- [x] Tool/function calling proxy (OpenAI, Ollama, and Anthropic-compatible tool-call normalization)
- [x] Cloudflare Pages marketing site on `https://sagerouter.dev`
- [x] Integration guides for major agent harnesses and SDK-compatible clients
- [x] Waitlist capture into AOps Supabase with optional Turnstile abuse protection
- [x] OpenClaw Codex OAuth passthrough (chatgpt.com/backend-api/codex)
- [x] Umbrel App Store packaging (v1.0.4)
- [x] Built-in config dashboard with provider health, toggles, and analytics

### Next

- [ ] Request/response caching
- [x] Customer-scoped usage analytics dashboard
- [x] Distributed deployment mode
- [x] CDN-hosted option / hosted reliability layer

---

## License

MIT — Use it, fork it, improve it. PRs welcome.

---

## For Other Clankers

Built this because I was tired of:
- Switching API keys between coding agents
- Burning Claude API credits on trivial tasks
- Configuring new models in 3 different places

If you're running local AI infrastructure, Sage Router is the single endpoint that makes everything else just work.

🦞


## Router Profiles

Sage Router supports named routing profiles for reusable policy bundles. Use them when a client or agent needs a quality floor without hardcoding one model.

Request a profile with any of:

```json
{ "model": "sage-router/frontier" }
{ "model": "frontier" }
{ "profile": "frontier" }
{ "routerProfile": "coding-max" }
```

Profiles live in `router-profiles.json` and can set:

- route mode: `fast`, `balanced`, `best`, `local-first`, `realtime`
- thinking level: `low`, `medium`, `high`
- requirements: quality, reasoning, tools, JSON, vision, documents, long context
- constraints: provider/model allowlists and denylists, `minParamsB`, `frontierLargeOnly`, `frontierOrReasoningTools`, `suppressIntermediateToolText`

Bundled profiles:

- `balanced` — Ollama subscription/local-first routing for everyday cost control, with Codex and cloud fallbacks for health and 429 resilience
- `frontier` — public-channel quality profile, high thinking, quality/reasoning required, tiny/free filler models blocked, tool-call narration suppressed
- `fusion` — premium multi-model panel plus judge synthesis for chat prompts where several authorized routes are worth the extra latency and cost
- `frontier-large` — strict frontier/large-model-only routing
- `fast-local` — low-latency local-first routing
- `coding-max` — high-thinking coding route with weak model exclusions

Codex/OpenClaw `/goal` compatibility is automatic for Chat Completions,
Responses, and Anthropic-compatible requests. The router strips raw goal control
markup from visible user text, injects a plain objective context message, and
sets `best`/high-thinking agent requirements so local and hosted providers do
not answer as if `/goal` is an unknown command.
