---
name: sage-router
description: Local-first AI model routing for serious agents. One endpoint. Any provider. The router figures out the rest.
version: 4.157.9
env:
  - SAGE_ROUTER_HOME (required: path to sage-router repo)
  - SAGE_ROUTER_DISABLED_PROVIDERS (optional: comma-separated provider names to suppress)
  - SAGE_ROUTER_DISABLED_MODELS (optional: comma-separated model IDs or provider/model keys to suppress)
  - SAGE_ROUTER_OLLAMA_TIMEOUT_SECONDS (optional, default 120)
  - SAGE_ROUTER_OLLAMA_AUTO_PULL_PATTERNS (optional, default :cloud)
  - OPENCLAW_GATEWAY_TOKEN (optional: token for OpenClaw gateway agent bridge)
---

# Sage Router

HTTP server on `:8790` that routes chat requests to the optimal provider based on intent classification.

## Endpoints

- `POST /v1/chat/completions` — OpenAI-compatible; routes automatically
- `POST /v1/responses` — OpenAI Responses API compatible; supports Codex custom provider traffic
- `POST /v1/messages` — Anthropic Messages API compatible; translates to/from OpenAI format internally
- `GET /health` — Provider status, model lists, routing debug

Any Anthropic-compatible tool (Cursor, Aider, Claude Code, Zed, Continue, OpenHands) can point at `http://localhost:8790` as the API base URL. Both streaming and non-streaming are supported.

## Active Providers

Providers are discovered from app-owned or harness config at startup. For
Umbrel and Docker installs, write provider config under the mounted app config
directory, usually `/config/openclaw/openclaw.json`. For local OpenClaw installs,
`~/.openclaw/openclaw.json` remains supported.

Rules:
- skips the router's own `sage-router` provider entry to avoid recursion
- resolves `${ENV_VAR}` values for `baseUrl` and `apiKey`
- includes `openai-codex` only when a token or imported app-owned auth JSON exists, unless an explicit gateway fallback is enabled
- recognizes Google Gemini providers from `generativelanguage.googleapis.com`
- auto-discovers Google models when the provider exists but `models` is empty in `openclaw.json`
- normalizes `anthropic` or Anthropic-hosted `anthropic-messages` providers onto the local Dario proxy at `localhost:3456`
- starts the Dario user service when Anthropic compatibility is needed and the service is not already running; in Docker, the image bundles `@askalf/dario` and autostarts `dario proxy` when credentials are mounted at `/root/.dario`
- supports temporary provider suppression via `SAGE_ROUTER_DISABLED_PROVIDERS=name1,name2`

## Multiple credentials per provider

A single provider may carry an ordered pool of credentials — multiple API keys
and/or multiple OAuth subscription paths (e.g. several ChatGPT/Codex accounts).
The router tries them in order and fails over to the next on auth/quota/transient
errors (`401`/`403`/`429`/`5xx`, rate-limit, quota, billing, overload). Failover
runs in both the non-streaming completion path and the streaming open path: a
rate-limited (429) key transparently yields to the next credential before any
bytes are committed to the client. Mid-stream failures (after the SSE response
has started) cannot be retried and fall back to the next provider in the route
chain as before.

Provider config entries accept, alongside the legacy single `apiKey`:

- `apiKeys`: list of `{label, key}` API key credentials
- `oauthPaths`: list of `{label, accessToken, refreshToken?, expires?, profile?}` OAuth subscription paths
- `credentialStrategy`: how the pool is selected each request — `failover`
  (ordered, primary first; default), `round-robin` (rotate the starting key to
  spread load/quota), `lru` (least-recently-used first), or `random`

The legacy single `apiKey` is preserved as the `default` credential for backward
compatibility. `${ENV_VAR}` references are resolved at request time. A global
default strategy can be set via `SAGE_ROUTER_CREDENTIAL_STRATEGY`; the per-key
cooldown window is `SAGE_ROUTER_CREDENTIAL_COOLDOWN_SECONDS` (default 60).

For `openai-codex`, existing multi-account OAuth profiles in
`~/.openclaw/agents/main/agent/auth-profiles.json` are folded into the pool
automatically, so ChatGPT subscription paths are usable with failover.

Dashboard (operator) configuration:

- `GET /setup/credentials` — masked summary of every provider's credentials
- `POST /setup/credentials/add` — add an API key or OAuth subscription path to a
  provider (creates the provider if it does not exist; never overwrites existing
  credentials)
- `POST /setup/credentials/remove` — remove a credential by `provider` + `label`/`slot`
- `POST /setup/credentials/strategy` — set a provider's `credentialStrategy`

The web dashboard exposes a **Credentials** card to add, list, and remove
credentials per provider, with primary targets Ollama (`ollama`/`ollama-cloud`),
OpenAI (`openai-completions`/`openai-codex-responses`), and Anthropic
(`anthropic-messages`, routed through Dario).

`GET /health` shows:
- `configured`: all discovered providers
- `providers`: reachable providers with model lists
- `disabled`: providers suppressed by env

## Multimodal input routing

Requests carrying multimodal inputs are detected via a deep payload scan (chat
content blocks, Responses API `input` items, tool calls/results, and `data:`
URIs) and set the corresponding requirement:

- images (`image_url` / `input_image` / `data:image/`) -> `vision`
- audio (`input_audio` / `audio` / `data:audio/`) -> `audio`
- video (`input_video` / `video` / `data:video/`) -> `video`
- documents/files -> `document` (and `longContext`)

Routing is strictly capability-based. `model_capabilities` reports `vision`,
`audio`, and `video` from each model's declared `input` modalities / flags, and
`model_meets_requirements` rejects models that lack the required modality:

- text-only GLM models (`glm-5`, `glm-5.2:cloud`) are rejected for image requests
  (`vision unsupported`); image-capable GLM variants (e.g. `glm-4v`) are allowed
- audio/video inputs route only to models declaring that input modality

`auto` and `agentic` profiles constrain `allowProviders`/`allowModels`/
`frontierLargeOnly`. When a multimodal request has no capable model under those
constraints, the router relaxes the profile allow-lists (keeping safety
deny-lists) and re-selects globally in both the forced-provider and auto-route
paths, so multimodal requests route to a capable model instead of failing.

`GET /health` exposes `imageCapable`, `audioCapable`, and `videoCapable`: the
exact models currently treated as capable of each modality (per provider, GLM
flagged). The dashboard Health card renders all three summaries.

## Modality learning

On every successful completion the router records the modalities that a model
actually served (`image`, `audio`, `video`, `document`, `text`) into an
append-only ledger persisted at `APP_MODEL_MODALITIES` (env
`SAGE_ROUTER_MODEL_MODALITIES`, default
`~/.openclaw/openclaw/model-modalities.json`). Disk writes are throttled (at
most once per 5 s unless forced).

Hosted/CDN deployments can share the ledger across all router nodes through
Supabase by applying
`supabase/migrations/20260626003000_model_modalities.sql` and enabling
`SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED=1` with
`SAGE_ROUTER_SUPABASE_URL` plus `SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY`.
When `SAGE_ROUTER_SUPABASE_MIRROR_ENABLED=1`, shared modality learning is on by
default. Nodes merge the shared table into local memory periodically
(`SAGE_ROUTER_MODEL_MODALITIES_SHARED_REFRESH_SECONDS`, default 60) and mirror
new observations through the atomic `sage_router_record_model_modalities` RPC,
so one CDN/Tailnet backend can benefit from modalities learned by another.
The Cloudflare API Worker records the same response headers into that RPC with
`ctx.waitUntil`, which keeps edge requests fast while making CDN observations
durable in the shared ledger. Public Tailnet edge health exposes
`modelModalities.sharedEnabled`, and the Cloudflare origin gate requires it
before treating an origin as public-edge-ready.

Learned modalities feed back into `model_capabilities` as an augmentation: a
model is treated as supporting a modality if it declares it *or* it has served
that modality before, so routing improves as the router observes more traffic.
When a request needs a learned modality, `score_provider_model` adds a
`learned_modality:*` contribution so models with proven successful history are
preferred among otherwise-capable candidates.

Observability:

- `LAST_ROUTE_DEBUG['modalities']` and the `X-Sage-Router-Modalities` response
  header expose the modalities of the active request
- `GET /setup/model-modalities` (operator) returns `modelModalities` plus the
  ledger `path`; the dashboard renders a "Learned Modalities" card
- `POST /setup/model-modalities/update` and `/reset` let operators edit or clear
  learned modalities; the dashboard exposes per-model save/reset and reset-all

## Routing Logic

The router does **not** perform mid-stream switching. Once a request is sent to a provider, the full response is returned or the attempt fails. If it fails, the next candidate in the chain is tried sequentially. There is no partial-output fallback or streaming handoff between providers.

Flow:
- detect intent from the latest user message
- estimate complexity from prompt length
- score every reachable (provider, model) pair globally — not per-provider — from the discovered provider config
- in `local-first`, operate as local-strict: reject centralized Internet API providers and only allow local/LAN/Tailnet endpoints plus approved decentralized providers such as Darkbloom, with Ollama `:cloud` models excluded
- for `GENERAL`, blend static heuristics with persisted empirical latency stats by provider and model
- rank candidates by API type, model-name hints, complexity, and measured latency
- attempt the top `SAGE_ROUTER_MAX_PROVIDER_ATTEMPTS` candidates in order
- `sage-router` provider (the router itself, model `auto`) is scored as a low-priority recursive fallback, never preferred
- paid plans can request premium Fusion with `model: "sage-router/fusion"` or the server tool `{"type":"sage-router:fusion"}`; server-tool markers are handled before downstream provider routing and gated with the same plan checks

Intent scoring is generic, for example:
- code and analysis strongly favor Anthropic/OpenAI-style reasoning models
- general/realtime requests prefer fast direct providers first
- general traffic learns from real successful request latency over time, with light exploration for cold providers/models
- complex prompts boost larger reasoning models and penalize mini/haiku-class models

Intent is detected by keyword matching on the latest user message. Complexity is estimated by word count.

## API

- `GET /health` — JSON with reachable providers, configured providers, and disabled providers
- `POST /v1/chat/completions` — OpenAI-compatible; routes automatically
- `POST /v1/responses` — OpenAI Responses API compatible; translates to/from Chat Completions internally

## Notes

- `openai-codex` is kept as an optional bridge, not a required first hop.
- Anthropic compatibility is provided through Dario, so `anthropic` can stay in `openclaw.json` while routing locally through `dario`.
- The repo `systemd` unit is template-style and expects local machine values in `~/.config/sage-router/sage-router.env`.
- Empirical latency memory is persisted at `~/.cache/sage-router/latency-stats.json` by default.
- When the OpenClaw gateway model-set path is unhealthy, the helper falls back to running without provider/model overrides instead of failing hard.
- If any provider starts misbehaving, suppress it with `SAGE_ROUTER_DISABLED_PROVIDERS` instead of editing the router.
- For reliable Umbrel/OpenClaw/Remnic use, point clients at `http://sage-router:8790/v1` on `umbrel_main_network`, set unauthenticated Ollama auto-pull patterns to empty, and keep quota-bound providers disabled until credentials are healthy.
- GitHub workflows now include CI syntax checks and CodeQL analysis for Python + JavaScript.
- See `BRANCH_PROTECTION.md` for the exact required-check setup on GitHub.

## Install

Install the user service from the repo copy:

```bash
mkdir -p ~/.config/systemd/user ~/.config/sage-router
cp systemd/sage-router.service ~/.config/systemd/user/sage-router.service
cp systemd/sage-router.env.example ~/.config/sage-router/sage-router.env
# edit ~/.config/sage-router/sage-router.env for your machine
systemctl --user daemon-reload
systemctl --user enable --now sage-router.service
```

Notes:
- the repo unit is now env-driven and does not hardcode your home path, Node version, or workspace location
- set `SAGE_ROUTER_HOME` to the actual repo path on your machine
- optionally set `SAGE_ROUTER_PATH_PREFIX` if your Python, Node, or Dario bins are not already on PATH

If an Anthropic provider is detected and Dario is not installed yet, install Dario first:
- GitHub: https://github.com/askalf/dario

## Service

```bash
systemctl --user status sage-router
systemctl --user restart sage-router
journalctl --user -u sage-router -f   # live logs
```


## Docker production notes

- Docker image includes Node, Python, Sage Router, and `@askalf/dario`.
- Mount an app-owned config directory at `/config` and use the dashboard setup flow for provider config or Codex auth JSON imports.
- Enable llama.cpp classifier sidecar with `docker compose --profile classifier up -d` and `SAGE_ROUTER_INTENT_CLASSIFIER_ENABLED=1`.
- Production classifier flags: `SAGE_ROUTER_INTENT_CLASSIFIER_PROVIDER=llamacpp`, `SAGE_ROUTER_INTENT_CLASSIFIER_BASE_URL=http://llamacpp-classifier:8080`, `SAGE_ROUTER_INTENT_CLASSIFIER_MODEL=classifier`.

## Router profiles

Sage Router supports named routing profiles in `router-profiles.json` next to `router.py`.

Request a profile with any of:
- `model: "sage-router/<profile>"`
- `model: "<profile>"`
- top-level `profile`, `routerProfile`, or `sageRouterProfile`

Profile fields currently supported:
- `route`: `fast`, `balanced`, `best`, `local-first`, `realtime`
- `thinking`: `low`, `medium`, `high`
- capability/quality flags: `requiresQuality`, `requiresReasoning`, `requiresTools`, `frontierLargeOnly`, `frontierOrReasoningTools`, `suppressIntermediateToolText`, `qualitySensitive`, `reasoning`, `tools`, `preferTools`, `json`, `vision`, `document`, `longContext`
- constraints: `allowProviders`, `denyProviders`, `allowModels`, `denyModels`, `minParamsB`

Current profiles:
- `frontier`: default high-quality frontier routing profile. Forces best/high, reasoning, quality-sensitive, suppresses tool-call narration, and blocks tiny/free filler models.
- `frontier-large`: strict frontier-large-only routing.
- `fast-local`: low-latency local-first routing.
- `coding-max`: high-thinking code route with weak model exclusions.

Codex/OpenClaw `/goal` compatibility is automatic. Raw `/goal ...` messages and
Codex `<codex_internal_context source="goal">` blocks are normalized into
plain persistent objective context, then routed with best/high, reasoning,
long-context, agentic requirements so providers do not treat `/goal` as an
ordinary unknown slash command.
