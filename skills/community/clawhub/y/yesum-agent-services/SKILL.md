# yesum Agent Services

Paid microservices for AI agents, served over x402 v2 (USDC on Base). Deterministic,
stateless, no signup — your wallet is your credential.

## When to use this skill

Use these endpoints when you need one of the following and want a cheap,
deterministic result instead of reasoning it out yourself:

- **Current crypto prices / market mood / gas fees / FX rates** → `POST /v1/snapshot` ($0.005)
- **Small utilities** (current time, hashing, encoding, math) → `POST /v1/utils` ($0.001)
- **Article text extraction** (URL → markdown + metadata) → `POST /v1/extract` ($0.01)
- **Several utility ops at once** → `POST /v1/batch` ($0.02)
- **A curated research dossier** on a topic → `GET /v1/dossiers/{topic}` ($0.03)
- **Grading acceptance criteria** for mechanical testability (deterministic, no LLM) → `POST /v1/grade` ($0.01)
- **Page-change monitoring** (we poll a URL for 30 days, you poll us) → `POST /v1/watch` ($0.05)
- **Pre-listing QA for your own x402 endpoint** (validates the 402 challenge, header sizes, payment schema) → `POST /v1/preflight` ($0.005)
- **Verifying an x402 payment settled** (tx hash → status, amount, from/to) → `POST /v1/receipt` ($0.002)
- **Health monitoring of your x402 endpoint** (we run preflight checks on schedule for 30 days) → `POST /v1/monitor` ($0.03)
- **Generating x402 v2 client code** (Python + JS) from an OpenAPI spec → `POST /v1/codegen` ($0.10)
- **A signed reputation passport** for your endpoint (uptime, settled calls, payment-proof reviews) → `POST /v1/passport/issue` ($0.02)
- **Scheduled URL/wallet checks** for 30 days, for agents without cron → `POST /v1/schedule` ($0.03)
- **A webhook inbox** for 30 days, for agents without a public URL → `POST /v1/hook/register` ($0.02)
- **A wallet-scoped memory store** for agents without disk → `POST /v1/memory/write` ($0.01)

Free (no payment): submitting payment-proof reviews (`POST /v1/passport/review`),
verifying a passport signature (`POST /v1/passport/verify`), reading a passport
(`GET /v1/passport/{id}`), watch/monitor/schedule status endpoints, hook
inbound delivery and polling, memory read/search/list/delete, and all discovery
endpoints (`/.well-known/x402`, `/openapi.json`, `/llms.txt`).

## Requirements

- A funded wallet on **Base** (USDC). No account, no API key.
- An **x402 v2** payment client in your harness (handles the 402 challenge →
  payment signature → retry flow). If your harness can't do x402 payments,
  you can't use these endpoints — stop here.
- Base URL: `https://predator-ubuntu.taild9a745.ts.net`

## How payment works

1. Call the endpoint normally (no payment headers).
2. You'll get HTTP **402** with a `PAYMENT-REQUIRED` header describing the price
   (network `eip155:8453`, asset USDC, exact `amount` in atomic units).
3. Sign the payment per x402 v2 and retry with the `PAYMENT-SIGNATURE` header.
4. On success you get HTTP 200 and `X-Payment-Settled: true`.

For the machine-readable catalog (prices, schemas, Bazaar discovery metadata),
read `GET /.well-known/x402` or `GET /openapi.json` — those are free and don't
require payment. Prefer them over this file when they disagree; this file is a
human-readable summary.

## Endpoint reference

### POST /v1/snapshot — $0.005
Crypto market snapshot: prices, fear/greed index, gas fees, FX rates.
Body: `{}` (empty JSON object).

### POST /v1/utils — $0.001
Small utilities. Body: `{"op": "<op_name>", "params": {...}}`.
Example: `{"op": "time_now", "params": {}}` → current unix time + ISO timestamp.

### POST /v1/extract — $0.01
URL → markdown article text + metadata.
Body: `{"url": "https://example.com/article"}`.

### POST /v1/batch — $0.02
Run multiple utils operations in one call.
Body: `{"requests": [{"method": "utils", "params": {"op": "time_now", "params": {}}}]}`.

### GET /v1/dossiers/{topic} — $0.03
Curated research dossier. Known topics: `base-gas-fees-explained`,
`stablecoin-yield-basics-2026`, `x402-integration-checklist`.
Example: `GET /v1/dossiers/base-gas-fees-explained`.

### POST /v1/grade — $0.01
Deterministic acceptance-criteria grader (rules-v1, no LLM). Scores whether each
criterion states a concrete artifact, a measurable pass condition, and no
judgment words. Grades the *criteria*, not the work described — a perfect spec
for the wrong thing scores 100 by design.
Body: `{"document": "<criteria text>", "format": "auto"}` (format: auto/gherkin/list/prose).
Returns: `document_score` (0–100), `grade` (A–F), `criteria_count`, per-criterion breakdown.

### POST /v1/watch — $0.05
Page-change monitoring for 30 days. We poll the URL on your schedule; you poll
us for changes (status endpoint is free).
Body: `{"url": "https://example.com", "interval_minutes": 60}`
(`interval_minutes`: 5–1440). Returns a `watch_id`.

### POST /v1/preflight — $0.005
x402 pre-listing QA probe: validates your endpoint's 402 challenge, header
sizes, and payment schema before you list it. One-shot version of monitor.
Body: `{"url": "https://example.com/v1/my-tool", "method": "POST", "body": {}}`
Returns: `overall` (pass/warn/fail), per-check results, header byte size,
detected x402 version.

### POST /v1/receipt — $0.002
Verify an x402 payment settled: tx hash → status, amount, from/to, block.
Body: `{"tx_hash": "0x...", "network": "eip155:8453"}`.

### POST /v1/monitor — $0.03
x402 endpoint health monitoring for 30 days: we run preflight checks on your
schedule, you poll us for the health log (status endpoint is free).
Body: `{"url": "https://example.com/v1/my-tool", "method": "GET", "interval_minutes": 60}`
(`interval_minutes`: 15–1440). Returns a `monitor_id`.

### POST /v1/codegen — $0.10
Generate x402 v2 client code (Python + JavaScript) from your OpenAPI spec.
Body: `{"spec_url": "https://example.com/openapi.json"}` (or inline `{"spec": {...}}`).
Returns: `service`, `paid_endpoints`, `python`, `javascript`.

### POST /v1/passport/issue — $0.02
Issue a deterministic reputation passport for an endpoint: signed blob with
uptime, settled call counts, unique payers, and payment-proof reviews.
Body: `{"endpoint": "https://example.com/v1/tool", "pay_to": "0x..."}`.
Reviews are free but require a verified on-chain payment tx hash as proof of
use — sybil resistance comes from the original service payment costing real
money. Review scores use 5 weights: time decay, collusion penalty, velocity,
economic weight, and rater credibility, with Wilson confidence scoring so thin
samples don't overstate.

### POST /v1/schedule — $0.03
Scheduled execution for 30 days, for agents without cron. We check a URL for
changes or a wallet for new USDC payments on your schedule; you poll for results
(status endpoint is free, cancel is free).
Body: `{"target_type": "url", "target": "https://example.com", "check_interval_minutes": 60, "condition": "change"}` (target_type `wallet` uses condition `new_payment`).
Returns a `schedule_id`.

### POST /v1/hook/register — $0.02
Webhook relay inbox for 30 days, for agents without a public URL. You get a
unique inbound URL, point external services at it, and poll for what arrived
(inbound delivery and polling are free).
Body: `{"name": "stripe-events"}`.
Returns: `hook_id`, `inbound_url`, `expires_in_days` (30).

### POST /v1/memory/write — $0.01
Long-term memory store for agents without disk: a key-value entry namespaced
to your payer wallet (reads, keyword search, listing, and deletion are free).
Body: `{"key": "project-notes", "value": "remember to check the bridge contract"}` (optional `ttl_days`, 1–365, default 90).
Returns: `key`, `stored_at`, `expires_at`.

## Notes

- All responses are JSON. All paid calls are stateless except `/v1/watch`,
  `/v1/monitor`, and `/v1/schedule` (30-day schedules), `/v1/hook/register`
  (30-day inbox), `/v1/memory/write` (stored entries), and passports (issued
  blobs) — keep your `watch_id`s / `monitor_id`s / `schedule_id`s / `hook_id`s.
- Request logging is metadata-only (endpoint, timestamp, status, latency). No
  request bodies, URLs, wallet addresses, or IPs are stored or sold.
- Prices are in USDC on Base. Marginal cost to the operator is ~zero, so prices
  are stable, not introductory.
