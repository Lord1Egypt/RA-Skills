# Sage Router Frontend MVP

Static React/Vite landing page for sagerouter.dev. It lives in web/ so the Python router service and OpenClaw skill packaging stay untouched.

## Preview

    cd web
    npm install
    npm run dev

Open the local Vite URL, usually http://localhost:5173.

## Production build

    cd web
    npm install
    npm run build

The static site is emitted to web/dist/.

## Local production preview

    cd web
    npm run preview

## Deploy notes

This site is deployed with Cloudflare Pages so static assets and Pages Functions ship together. `web/dist/` contains the static build; `web/functions/` contains production functions such as the waitlist endpoint.
The repo deploy helper compiles `web/functions` into the deploy artifact before
calling `wrangler pages deploy`, which keeps `/api/waitlist` routed to the
function in direct Wrangler uploads.

Suggested Cloudflare Pages settings:

- Root directory: web
- Build command: npm run build
- Build output directory: dist

The waitlist form posts to `/api/waitlist`, a Cloudflare Pages Function that inserts into Supabase table `sage_router_waitlist` and falls back to `funnel_leads` for older AOps schemas. `GET /api/waitlist` is a non-mutating health check used by `scripts/check_sagerouter_launch_readiness.sh`. The managed-access intake posts `interest=managed-access` plus allowlisted qualification buckets for private-beta demand measurement while public managed provider access stays disabled, including target provider family and commercial preference buckets for Ollama, OpenAI, Anthropic, and BYOK-compatible demand, plus support need, target launch window, and coarse inbound intent from known CTA URLs for Max implementation follow-up. It also sends anonymous page-view, form-start, submit, and received events to `/api/funnel-event` with only those qualification buckets, so operators can see one-subscription and implementation demand before full contact submission without sending email or company fields through the marketing-event path. Browser-originating waitlist and funnel-event writes must come from Sage Router-owned production hosts, local development hosts, Cloudflare Pages preview hosts ending in `.sage-router-web.pages.dev`, or exact origins listed in `SAGEROUTER_WAITLIST_ALLOWED_ORIGINS`/`SAGEROUTER_FUNNEL_ALLOWED_ORIGINS`; the endpoints require an explicit trusted `Origin` and reject third-party or missing-origin writes before using the Supabase service-role insert. `Referer` is stored only as sanitized attribution metadata and is not accepted as an origin fallback. Set both `SAGEROUTER_TURNSTILE_SECRET_KEY` and `SAGEROUTER_TURNSTILE_SITE_KEY` in Cloudflare Pages to require Cloudflare Turnstile on waitlist submissions; the health check fails if the secret is enabled without a public site key.

The homepage, calculator, pricing, Fusion, launch plan, quickstart, model-gateway
comparison, and model catalog pages send anonymous pre-signup page-view, CTA,
quickstart snippet-copy, setup-next, filter, and bucketed search intent to
`/api/funnel-event`, backed by Supabase table `sage_router_funnel_events`.
The public model catalog at `/models` uses safe `/model-catalog` metadata for
gateway-style searchable discovery and falls back to embedded public route
families; it does not call live `/v1/models` without a generated customer API
key. It also exposes `Copy 60-second catalog setup` and an always-visible
`Create API key next` handoff with `model_catalog_setup_next_clicked`
telemetry. Catalog search telemetry stores only coarse model-family and query-bucket
labels, not raw search text.
`GET /api/funnel-event` is a non-mutating health check. The function only
accepts allowlisted event names, plans, sanitized URLs, and metadata buckets so
the operator launch funnel can count demand without storing prompts, workflow
text, emails, API keys, or provider credentials. Browser-originating writes must
come from Sage Router-owned production hosts, local development hosts,
Cloudflare Pages preview hosts ending in `.sage-router-web.pages.dev`, or exact
origins listed in `SAGEROUTER_FUNNEL_ALLOWED_ORIGINS`; the endpoint rejects
third-party origins before using the Supabase service-role insert.

The account and standalone login pages use the same endpoint for activation and
checkout intent: signup/login attempt, OAuth click, wallet connect attempt,
browser-visible auth-provider state check, selected plan, API-key creation,
email verification resend recovery, public-edge key verification, first browser test request success, Stripe
checkout click/return, Stripe portal click/return, and crypto/manual payment
intent click. Keep the payload limited to event name, plan, sanitized
source/target URL, and allowlisted metadata; Supabase Auth,
generated-key records, billing webhooks, route usage, and Supabase customer
records remain authoritative for activation and paid conversion. Login-page
events and verification-resend events must not include typed emails, account
email addresses, passwords, wallet addresses, OAuth codes, OAuth secrets, or
access tokens.
The dedicated `/billing` recovery page also sends account, pricing, support,
troubleshooting, quickstart, and status CTA events through this endpoint so the
operator funnel can distinguish payment recovery friction from normal
pre-signup checkout interest without collecting secrets or support text.



## Hosted onboarding CTA

The primary homepage CTA is `Create hosted API key`, which links to
`https://app.sagerouter.dev/account.html?plan=pro&start=create_key` directly,
without the marketing-host redirect hop. The above-the-fold key-first panel now
leads with `Open account key creator` and records `landing_key_first_direct_clicked`
before GitHub, email magic-link, or setup-copy fallbacks. The hero also exposes a
no-secret `Copy 60-second setup bundle` action that records `quickstart_snippet_copied`
with `landing-hero-setup-bundle` metadata, so setup-copy intent is measurable
before signup. A persistent bottom activation bar keeps `Create API key` and
`60-second setup` visible after scroll while reusing `landing_account_clicked`
and `landing_quickstart_clicked` telemetry. The hero keeps pricing, quickstart, public status,
model-gateway comparison, model catalog, calculator, security, analytics, login,
managed-access private beta review, support, and local GitHub install paths
visible so a prospect can move from discovery to generated `sk_sage_*` key setup
without joining a waitlist first. The homepage route-path grid gives Cursor,
coding-agent, Ollama, OpenAI API, Anthropic API, and self-hosted prospects a
direct route from the homepage to the most relevant setup page while recording
`landing_article_clicked` intent metadata. The waitlist remains secondary for release
notes, integration updates, private deployment help, and future managed-provider
beta interest.
The public status page doubles as a no-secret operator launch-actions surface:
it copies activation-email preflight, managed-provider resale dry-run/staging,
first-request setup, and Cloudflare BIC verification commands from safe public
metadata without exposing provider credentials, private costs, customer data, or
tokens.
The same hero CTAs and successful waitlist submissions emit privacy-safe homepage funnel events with the `landing` source surface, so the private launch funnel can measure visitor-to-signup movement without storing form emails, company names, prompts, API keys, provider credentials, or raw query strings.

## Hot-swappable copy

The page now includes the product line: “Your agents’ engine is now hot-swappable.” It frames Sage Router as a model layer that lets agents swap/fail over between authorized providers and local/cloud models without rewiring the harness.

## SEO / GEO / LLM discovery

The MVP treats discoverability as first-class. Current static assets include:

- Canonical placeholder: https://sagerouter.ai/
- OpenGraph and Twitter metadata.
- Keyword coverage for AI model router, LLM router, provider routing, model selection automation, AI agent model routing, OpenAI-compatible router, Anthropic-compatible router, Ollama routing, BYOK AI gateway, local-first AI router, and model gateway alternatives.
- Structured page sections for automation, BYOK routing, model-gateway comparison, and Ollama/Ollama Cloud roadmap language.
- Dedicated hosted pricing page at `/pricing` with plan limits, compliance-safe positioning, and $10k MRR launch math.
- Pricing uses the same measurable activation CTA as quickstart: `Copy 60-second setup bundle`, `Create API key next` visible before and after copy, `pricing-full-setup-bundle`, `quickstart_snippet_copied` telemetry, `pricing_setup_next_clicked` telemetry, Pro `start=create_key` handoffs, Lite/Max `start=checkout` plan handoffs, and a key-first proof block that tells buyers to create the generated `sk_sage_*` key before checkout unlocks hosted routing.
- Dedicated Fusion page at `/fusion` with `sage-router/fusion`, the `sage-router:fusion` server tool, `tool_choice: "required"`, Pro/Max gating, and `fusion_plan_required` upgrade guidance.
- Dedicated billing help page at `/billing` with Stripe checkout, Stripe billing portal, manual/crypto settlement, activation states, generated key behavior, payment recovery, and no-secret support boundaries.
- Dedicated managed-access private beta and Max implementation intake at `/managed-access` with no-secret qualification buckets for one-subscription demand capture, target provider family, commercial preference, support need, target launch window, and coarse inbound CTA intent. The page points to the public pricing readiness checkpoint and keeps activation conditioned on provider authorization, terms acknowledgment, an authorized provider allowlist, configured provider cost model, and plan-margin checks.
- Hosted account page primary activation creates the first `sk_sage_*` key directly for signed-in, verified users without one, preserving the one-time key display and saved checkout intent. Saved `start=checkout` intent also auto-creates that first key once after verified sign-in when no key exists, reducing signup-to-generated-key friction. A persistent post-key activation panel keeps `/v1/models` verification, first `sage-router/frontier` request, and Codex setup copy visible after key generation, with no raw key included in funnel telemetry.
- Login key recovery at `/login.html?start=create_key` keeps same-email recovery first, shows the generated-key-before-checkout steps, preserves the account activation URL, and records `login_key_recovery_account_setup_clicked` so the launch funnel can separate passive no-key recovery views from click-throughs toward API-key setup.
- Dedicated API quickstart page at `/quickstart` with `Copy 60-second setup bundle`, an always-visible `Create API key next` handoff with `quickstart_setup_next_clicked` telemetry, hosted `sk_sage_*` key setup, `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, `sage-router/frontier`, curl, JavaScript, Python, Codex, and error troubleshooting.
- Dedicated API troubleshooting page at `/api-troubleshooting` with no-secret guidance for hosted 401/402/429/503 responses, safe curl probes, `WWW-Authenticate`, `Retry-After`, `X-RateLimit-*`, `X-Quota-*`, and account/pricing/status onboarding links.
- Dedicated hosted API reference page at `/docs/api-reference` with OpenAI-compatible endpoint docs for `GET /v1/models`, `POST /v1/chat/completions`, `POST /v1/responses`, public `/model-catalog`, generated keys, quotas, rate limits, and failover signals.
- Dedicated Gateway migration guide at `/docs/gateway-migration` mapping `https://gateway.example/api/v1` to `https://api.sagerouter.dev/v1`, generated `sk_sage_*` keys, `sage-router/frontier`, model catalog discovery, and provider terms boundaries.
- Model-gateway comparison at `/compare/model-gateways` also promotes a copy-first `Copy 60-second gateway setup` bundle for migration-intent visitors.
- Reddit-style AI gateway evaluation kit at `/reddit-ai-gateway-evaluation` with copyable comparison/setup snippets, local-first custody proof, OpenRouter BYOK boundary, multiple API-key load balancing, 429 failover, multimodal routing, hosted generated-key activation, sitemap, LLM discovery, and readiness checks.
- Reliability proof kit at `/reliability-proof` with copyable 429 failover, credential load-balancing, multimodal routing, and Reddit proof-reply snippets, measured proof CTAs, sitemap, LLM discovery, and readiness checks.
- Community launch kit at `/community-launch-kit` with copyable Show HN, Indie Hackers, Dev.to, X, and LinkedIn launch copy, measured community/social campaign links, no-secret posting boundaries, sitemap, LLM discovery, and readiness checks.
- Founder sales kit at `/founder-sales-kit` with copyable Pro activation, Max implementation, gateway migration, and calculator follow-up outreach, measured `utm_source=founder-sales` links, no-secret boundaries, sitemap, LLM discovery, and readiness checks.
- Ollama AI model router page at `/ollama-ai-model-router` with local Ollama and Ollama Cloud positioning, one OpenAI-compatible endpoint, multiple API-key load balancing, 429 failover, multimodal routing, hosted generated-key activation, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- OpenAI API router page at `/openai-api-router` with hosted generated keys, `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, OpenAI-compatible chat and Responses API positioning, multiple OpenAI API-key load balancing, 429 failover, multimodal routing, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Azure OpenAI router page at `/azure-openai-router` with customer-owned `AZURE_OPENAI_API_KEY` and `AZURE_OPENAI_ENDPOINT` custody, Azure deployment routing, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Anthropic API router page at `/anthropic-api-router` with hosted generated keys, `ANTHROPIC_BASE_URL=https://api.sagerouter.dev`, Claude Code and Anthropic-compatible `/v1/messages` positioning, Dario-ready subscription paths, 429 failover, multimodal routing, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- AWS Bedrock router page at `/aws-bedrock-router` with customer-owned AWS account/IAM custody, `AWS_PROFILE`, `AWS_REGION`, Bedrock model routing for authorized foundation models, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal safeguards, provider-authorization boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- GitHub Copilot router page at `/github-copilot-router` with GitHub Copilot and Copilot-compatible endpoint positioning, customer-owned `GITHUB_COPILOT_TOKEN` custody, OpenAI-compatible setup, model discovery, credential load balancing, 429 failover, multimodal safeguards, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- Codex CLI router page at `/codex-cli-router` with hosted generated keys, `base_url = "https://api.sagerouter.dev/v1/"`, `wire_api = "responses"`, local port `8790`, Tailnet routing, 429 failover, multimodal routing, Codex OAuth boundary language, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Aider AI model router page at `/aider-ai-model-router` with hosted generated keys, `OPENAI_API_BASE=https://api.sagerouter.dev/v1`, `aider --model openai/auto`, local port `8790`, local Ollama fallback, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Continue AI model router page at `/continue-ai-model-router` with hosted generated keys, OpenAI-compatible `apiBase=https://api.sagerouter.dev/v1`, `model=auto`, local port `8790`, local Ollama fallback, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- OpenHands AI model router page at `/openhands-ai-model-router` with hosted generated keys, `OPENAI_BASE_URL=https://api.sagerouter.dev/v1`, `model = "auto"`, local port `8790`, local Ollama fallback, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- OpenClaw AI model router page at `/openclaw-ai-model-router` with Sage Router skill setup, `OPENAI_BASE_URL=http://localhost:8790/v1`, `ANTHROPIC_BASE_URL=http://localhost:8790`, Codex OAuth passthrough, Tailnet routing, 429 failover, multimodal routing, provider-authorization boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Claude Code router page at `/claude-code-router` with Anthropic-compatible coding-agent positioning, hosted generated keys, `ANTHROPIC_BASE_URL=https://api.sagerouter.dev`, authorized Anthropic or Dario subscription paths, local/Tailnet fallback, 429 failover, multimodal routing, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- Gemini API router page at `/gemini-api-router` with Google AI and Vertex AI positioning, function-tool routing, Gemini CLI setup intent, 429 failover, multimodal routing, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- xAI Grok router page at `/xai-grok-router` with xAI API-key positioning, customer-owned `XAI_API_KEY` custody, OpenAI-compatible setup, `/v1/models` discovery, credential load balancing, 429 failover, multimodal safeguards, xAI SSO proxy boundaries, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Mistral AI router page at `/mistral-ai-router` with Mistral and Codestral positioning, customer-owned `MISTRAL_API_KEY` custody, OpenAI-compatible setup, code-profile routing, credential load balancing, 429 failover, multimodal safeguards, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- Groq AI router page at `/groq-ai-router` with low-latency Llama and Mixtral positioning, customer-owned `GROQ_API_KEY` custody, OpenAI-compatible setup, latency-aware routing, credential load balancing, 429 failover, multimodal safeguards, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- NVIDIA NIM router page at `/nvidia-nim-router` with NVIDIA NIM and NVIDIA Cloud positioning, customer-owned `NVIDIA_API_KEY` custody, OpenAI-compatible setup, credential load balancing, 429 failover, multimodal routing, copyable setup snippets, provider-authorization boundaries, sitemap, LLM discovery, and readiness checks.
- Coding agent model router page at `/coding-agent-model-router` with Codex, Cursor, Aider, Continue, Claude Code, OpenHands, and OpenClaw positioning, hosted generated keys, Codex Responses API profiles, local Ollama fallback, 429 failover, multimodal routing, copyable setup snippets, sitemap, LLM discovery, and readiness checks.
- Cursor AI model router page at `/cursor-ai-model-router` with custom OpenAI-compatible endpoint setup, Anthropic-compatible paths, hosted generated keys, local Ollama fallback, multiple API-key load balancing, 429 failover, multimodal routing, copyable Cursor setup snippets, sitemap, LLM discovery, and readiness checks.
- Dedicated Codex setup page at `/docs/codex` with hosted `https://api.sagerouter.dev/v1/`, local `http://127.0.0.1:8790/v1/`, Tailnet `http://<tailnet-host>:8790/v1/`, `wire_api = "responses"`, and `sage-router/frontier` profiles.
- Dedicated agent-native routing page at `/agent-native` with `sage-router/frontier`, Responses API and Codex compatibility, health-aware fallback, BYOK custody, local/Tailnet/hosted deployment choices, and the public `/features/agent-native` metadata endpoint.
- Dedicated integrations index at `/integrations` with hosted `https://api.sagerouter.dev/v1`, local `http://127.0.0.1:8790/v1`, Tailnet `http://<tailnet-host>:8790/v1`, `sage-router/frontier`, OpenAI-compatible clients, Codex, Cursor, Aider, Continue, Claude Code, OpenHands, Anthropic-compatible clients, Ollama, Ollama Cloud, NVIDIA NIM, OpenClaw, Hermes, and Pi agents.
- No-login model routing calculator at `/model-routing-calculator` for acquisition and workflow qualification; it recommends Lite/Pro/Max, reads public `/pricing` billing readiness metadata for current limits and checkout availability, sends recommended tiers into generated-key-first account setup on `/account.html?plan=...&start=create_key`, and emits `calculator_key_activation_clicked` for the primary handoff.
- FAQ content intended for snippets and LLM ingestion.
- JSON-LD SoftwareApplication and FAQPage schema in index.html.
- Machine-readable files served from the static root:
  - /llms.txt
  - /llms-full.txt
  - /robots.txt
  - /sitemap.xml

Next recommended additions after MVP:

- Dedicated `/compare/model-gateways` page for model-gateway acquisition traffic.
- Keep `/docs/gateway-migration` aligned with the model-gateway comparison page, hosted quickstart, API reference, sitemap, LLM discovery, and readiness checks.
- Keep `/reddit-ai-gateway-evaluation` aligned with gateway comparison, OpenRouter comparison, hosted quickstart, sitemap, LLM discovery, and readiness checks.
- Keep `/reliability-proof` aligned with failover, credential load-balancing, multimodal routing, Reddit proof replies, sitemap, LLM discovery, and readiness checks.
- Keep `/community-launch-kit` aligned with the launch plan, final community posts, sitemap, LLM discovery, and readiness checks.
- Keep `/founder-sales-kit` aligned with founder-led Pro and Max outreach, measured UTM links, no-secret boundaries, sitemap, LLM discovery, and readiness checks.
- Keep `/ollama-ai-model-router` aligned with local Ollama, Ollama Cloud, hosted quickstart, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/openai-api-router` aligned with hosted quickstart, OpenAI-compatible API reference, Responses API compatibility, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/azure-openai-router` aligned with Azure OpenAI deployment routing, OpenAI-compatible setup, authorized Azure tenant custody, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/anthropic-api-router` aligned with Anthropic-compatible setup, Claude Code, Dario-ready paths, provider authorization boundaries, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/aws-bedrock-router` aligned with Amazon Bedrock model routing, authorized AWS account custody, OpenAI-compatible setup, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/github-copilot-router` aligned with Copilot-compatible endpoint routing, coding-agent setup, authorized token custody, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/codex-cli-router` aligned with Codex CLI setup, Responses API profiles, local port `8790`, Tailnet routing, Codex OAuth boundaries, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/aider-ai-model-router` aligned with Aider setup, OpenAI-compatible routing, local Ollama fallback, local port `8790`, Tailnet routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/continue-ai-model-router` aligned with Continue setup, OpenAI-compatible routing, local Ollama fallback, local port `8790`, Tailnet routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/openhands-ai-model-router` aligned with OpenHands setup, OpenAI-compatible routing, local Ollama fallback, local port `8790`, Tailnet routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/openclaw-ai-model-router` aligned with OpenClaw skill setup, OpenAI-compatible and Anthropic-compatible routing, Codex OAuth passthrough, local port `8790`, Tailnet routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/claude-code-router` aligned with Claude Code setup, Anthropic-compatible routing, authorized Anthropic or Dario paths, local/Tailnet fallback, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/gemini-api-router` aligned with Google AI and Vertex AI routes, Gemini function-tool support, hosted quickstart, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/xai-grok-router` aligned with xAI Grok API-key routing, OpenAI-compatible setup, SSO proxy boundaries, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/mistral-ai-router` aligned with Mistral and Codestral API-key routing, OpenAI-compatible setup, code-profile routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/groq-ai-router` aligned with Groq API-key routing, low-latency Llama/Mixtral positioning, OpenAI-compatible setup, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/nvidia-nim-router` aligned with NVIDIA NIM, NVIDIA Cloud, GPU-backed hosted inference, OpenAI-compatible setup, BYOK custody, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/coding-agent-model-router` aligned with Codex setup, integrations, agent-native routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep `/cursor-ai-model-router` aligned with Cursor integration docs, coding-agent setup, OpenAI-compatible routing, Anthropic-compatible routing, model catalog, sitemap, LLM discovery, and readiness checks.
- Keep the hosted pricing page aligned with `/pricing` API metadata and the account checkout plans.
- Keep `/fusion` aligned with premium route aliases, server-tool compatibility, Pro/Max gating, sitemap, LLM discovery, and readiness checks.
- Keep `/billing` aligned with Stripe checkout, Stripe billing portal, manual/crypto settlement, generated-key activation behavior, sitemap, LLM discovery, and readiness checks.
- Keep `/managed-access` aligned with provider-resale terms, margin policy, waitlist metadata, sitemap, LLM discovery, and readiness checks.
- Keep `/quickstart` aligned with the hosted account page and public edge error guidance.
- Keep `/api-troubleshooting` aligned with public edge 401/402/429/503 payloads, rate-limit headers, quota headers, sitemap, LLM discovery, and readiness checks.
- Keep `/docs/api-reference` aligned with the hosted OpenAI-compatible API surface, quota/rate-limit headers, authenticated model API boundary, sitemap, LLM discovery, and readiness checks.
- Keep `/agent-native` aligned with `/features/agent-native`, Codex setup, public model profiles, sitemap, LLM discovery, and readiness checks.
- Keep `/integrations` aligned with the public quickstart, Codex setup, integration docs, local port `8790`, Tailnet routing, sitemap, LLM discovery, and readiness checks.
- Keep the model routing calculator in navigation, sitemap, LLM discovery, and readiness checks.
- Keep the public `/security` trust page in navigation, sitemap, LLM discovery, and readiness checks whenever hosted edge authentication copy changes.
- Keep the public `/support` page in navigation, sitemap, LLM discovery, and readiness checks whenever hosted account, billing, quota, reliability, or security escalation copy changes.
- Dedicated docs pages for OpenAI-compatible, Anthropic-compatible, Ollama, Gemini, Cursor, Aider, Continue, Claude Code, and OpenHands setup.
- Expand JSON-LD once final production docs URLs, logo/social image, and hosted beta URLs are stable.
- Real case-study/benchmark pages targeting `automate model selection`, `agent model router`, and `BYOK LLM gateway` searches.

## Business model positioning

The MVP page now encodes the intended business model:

- Free local router, works without an account.
- Paid Sage Cloud / hosted control plane for team config sync, provider health monitoring, hosted dashboards, uptime checks, routing policy sync, and optional reliability.
- Optional managed cloud fallback/failover, framed as BYOK/BYOS reliability infrastructure, not model resale.
- Enterprise deployment/support: private deployments, compliance/security review, custom routing strategies, audit logs, usage visibility, team API keys, and private deployments.
- Developer-first docs as acquisition, with prominent tutorial CTAs for the public Codex setup page, Claude Code, OpenClaw, Ollama/Ollama Cloud, and OpenAI-compatible endpoint use.
- Provider profiles/routing presets for coding, fast chat, local fallback, and hybrid local/cloud routes.
- Crypto-native billing remains planned, with Algorand-native billing and BTC bridge support.

This scope keeps the frontend lightweight: Vite/React static assets, Cloudflare Pages Functions for narrow hosted flows, Supabase Auth for account/session state, and the Sage Router API edge for billing, API keys, usage, and model traffic.

## Crypto billing direction

The landing page now includes only a lightweight payment direction section. Payment rails are not wired in this pass.

Planned direction:

- Crypto-native billing for hosted beta.
- Algorand-native billing, with BTC bridge support.
- Use AOps.studio infrastructure where appropriate.
- Borrow EARLCoin wallet/payment UX patterns where useful.
- Avoid Stripe-first assumptions until payment scope is explicitly chosen.

Reuse opportunities found:

- /home/umbrel/.openclaw/workspace/.vite-build/earlcoin_frontend appears to include WalletConnect/Web3Modal-style wallet flow code in built assets.
- /home/umbrel/.openclaw/workspace/earlcoin_frontend_build.zip contains a built EARLCoin frontend bundle, useful as a visual/flow reference but not source-level reusable as-is.
- No live payment wiring was added, to avoid accidental external money movement or premature custody/payment commitments.

## Compliance and security copy guardrails

- Customers bring their own authorized provider access.
- Do not claim Sage Router resells model access, pools accounts, bypasses ToS, or grants unauthorized provider access.
- Default key custody is local. Hosted Sage infrastructure should be described as control plane/docs/health/optional reliability infrastructure unless an explicit encrypted hosted proxy mode is implemented.
