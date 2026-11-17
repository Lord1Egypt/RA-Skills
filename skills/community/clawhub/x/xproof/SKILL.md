---
name: Prove Before Act
version: 3.3.14
description: Prove Before Act accountability integration for AI agents. REST API, MCP, and x402. The @jasonxkensei/xproof ClawHub slug is a legacy compatibility identifier.
homepage: https://provebeforeact.com
metadata: {"prove-before-act": {"category":"proof,security,compliance,accountability,prove-before-act","api_base":"https://provebeforeact.com"}}
---

# Prove Before Act — Accountability Layer for AI Agents

This skill describes how to anchor reasoning (WHY) before an action and its result (WHAT) afterwards with Prove Before Act. It provides an auditable record when the returned proof is confirmed; it does not itself enforce an execution policy.

> **Current product and compatibility notice:** Prove Before Act is the product name. The ClawHub install slug `@jasonxkensei/xproof` is retained as a legacy compatibility identifier for existing OpenClaw installations. Install the canonical Python package as `prove-before-act`; its supported Python module namespace is `xproof`. `XProofClient`, `XPROOF_*`, `xProof-Action`, and `jasonxkensei/xProof` are legacy protocol, action, or repository identifiers retained for compatibility. MX-8004 support is not active unless `GET /api/mx8004/status` reports `status: "active"`; the current production response is `status: "not_configured"`.

## The Core Pattern: Prove Before & After Act

```
1. Reason (WHY) → 2. Hash locally → 3. Anchor WHY on-chain → 4. Get proof_id → 5. Execute → 6. Hash result (WHAT) → 7. Anchor WHAT on-chain → 8. Full 4W trail
```

Anchor reasoning (WHY) on-chain **before** execution. Anchor the actual result/output (WHAT) **after** for a complete 4W audit trail. The proof_id is your immutable pre-execution commitment — if something goes wrong, you have forensic evidence that the reasoning preceded the action.

**4W breakdown — what each letter means and who provides it:**

| | Question | Provided by |
|:--|:--|:--|
| **W**HO | Which agent or actor made this decision? | **MX-8004** — optional identity integration when live status reports active |
| **W**HAT | What output or action was certified? | **Prove Before Act** — SHA-256 hash of the output, anchored on MultiversX mainnet |
| **W**HEN | Immutable timestamp? | **Prove Before Act** — MultiversX block finality (~6 s); not a self-reported clock |
| **W**HY | What reasoning led to the decision? | **Prove Before Act** — `action_description`, `risk_level`, and `context` fields from `/api/audit` |

Prove Before Act records WHAT / WHEN / WHY context. MX-8004 may provide WHO when its integration is active. Check live proof and MX-8004 responses before treating the resulting record as complete.

> **Agent reference:** [`https://provebeforeact.com/agent-context`](https://provebeforeact.com/agent-context) — 13 Q&A sections written specifically for autonomous agents: production deployment patterns, retry policy, x402 payment walkthrough, 4W audit trail deep-dive, privacy model, fleet monitoring, latency benchmarks, and framework integration examples (LangChain, CrewAI, AutoGen, LlamaIndex, OpenAI Agents SDK, Fetch.ai).

**Why Prove Before Act?** An agent that can prove its reasoning before acting is fundamentally more trustworthy than one that cannot. It creates an unbreakable causal chain: the intent existed before the action, and the blockchain makes that sequence immutable.

**Why audit?** Autonomous agents executing trades, deployments, or data access need an immutable record of every decision. The Agent Audit Log Standard describes a blocking pattern your agent can adopt: obtain a proof before executing. Enforcement is implemented in your agent code; Prove Before Act supplies the proof record.

**Why violations?** Operators can use recorded violations as an accountability signal when the relevant Base integration is deployed and active. Confirm contract and event availability from the live documentation before automating a policy.

## Pricing

**Flat rate per proof** -- no tiers, no volume discounts, same price whether you anchor 1 or 100,000 proofs. The current per-proof price is served live at `/api/pricing`; multiply it by your volume for a cost estimate.

| Scale | Cost |
|:---|:---|
| 1 proof | 1× current price |
| 1,000 proofs | 1,000× current price |
| 10,000 proofs | 10,000× current price |
| 50 agents × 20 actions/day × 30 days | 30,000× current price / month |

Payment: USDC on Base (x402, no account) or EGLD on MultiversX (ACP/wallet) or prepaid credits.

## Quick Install

```bash
mkdir -p .agent/skills/prove-before-act/references

# Core Skill — from the canonical main repository
curl -sL https://raw.githubusercontent.com/jasonxkensei/prove-before-act/main/clawhub-publish/xproof/SKILL.md \
  > .agent/skills/prove-before-act/SKILL.md

# Reference Manuals
for f in certification x402 mcp; do
  curl -sL "https://raw.githubusercontent.com/jasonxkensei/prove-before-act/main/clawhub-publish/xproof/references/${f}.md" \
    > ".agent/skills/prove-before-act/references/${f}.md"
done
```

> **Source verification:** All files above are served from `github.com/jasonxkensei/prove-before-act` — the canonical repository for the server code, contracts, and SDKs.

## First successful integration

Use this four-step path to create a verified record without exposing the original content:

1. **Install** — run `openclaw skills install @jasonxkensei/xproof`. Its package slug is legacy; the installed skill and product are **Prove Before Act**.
2. **Hash locally** — compute a SHA-256 hash of the decision or output. Do not send raw text, files, prompts, or credentials.
3. **Anchor** — call `certify_file` through MCP or `POST /api/proof` with the hash and a filename.
4. **Verify before relying on it** — retain the returned `proof_id` and use `verify_proof` or `GET /api/proof/<proof_id>` until the status is confirmed. Your own operator policy decides whether to continue, retry, request review, or block an action.

## Python SDK quick start

Install the canonical package:

```bash
pip install prove-before-act
```

Then import its supported `xproof` module namespace and hash the content locally:

```python
import hashlib
import json

from xproof import XProofClient

decision = {"action": "publish report", "reason": "approved by operator"}
sha256_hex = hashlib.sha256(
    json.dumps(decision, sort_keys=True).encode("utf-8"),
).hexdigest()

client = XProofClient.register("my-agent")
proof = client.certify_hash(sha256_hex, "decision.json", "my-agent")
```

## Data & Privacy

> **Transparency notice — what leaves your environment when using this skill.**

| Data field | Sent to provebeforeact.com? | Notes |
|:---|:---:|:---|
| File content / raw text | **Never** | Hash locally; only the digest crosses the boundary |
| `file_hash` (SHA-256 hex, 64 chars) | Yes | One-way fingerprint; original content cannot be reconstructed |
| `filename` / `author` | Optional | Metadata you explicitly supply; omit if sensitive |
| `action_description` / `context` | Optional | Only when you call `/api/audit` or `audit_agent_session` |
| USDC payment (x402) | Yes — Base chain | On-chain transaction; amount is your configured ceiling |
| API key (`pm_...`) | Yes — HTTP header | Treat like a password; never log or commit |

**What provebeforeact.com does NOT receive:** raw file contents, prompt text, model weights, environment variables, or any field you do not explicitly pass.

**Data retention:** proof records are permanent and public by default (that is the point — immutable evidence). Before certifying, confirm you want the hash publicly anchored on MultiversX mainnet forever.

**Skill file:** this file is intentionally public and contains no secrets. It is documentation only — API patterns, pricing, and integration examples. Safe to audit, share, or version-control.

## Security

- **NEVER** commit API keys to a public repository.
- **ALWAYS** add `.env` to your `.gitignore`.
- API keys are prefixed `pm_` -- treat them like passwords.
- x402 mode requires no API key (payment replaces authentication).
- **NEVER send plaintext content to provebeforeact.com** -- always hash locally first (`sha256sum`, `crypto.subtle.digest`, or equivalent). The only field Prove Before Act accepts is `file_hash` (64-char SHA-256 hex). No raw text, documents, or binary data should ever leave your environment.
- **x402 is opt-in and autonomous** -- once enabled, your agent can initiate USDC payments on Base without per-transaction confirmation. Configure a spending cap in your agent framework and require human approval above your threshold before enabling x402 in production.
- **`llms.txt` and `llms-full.txt` are static documentation references** -- load them once at install time for API reference, not at runtime on every call. Fetching them dynamically on each invocation creates an unnecessary runtime dependency on provebeforeact.com availability and a potential prompt-injection surface if the file is ever compromised.
- **Guard/enforcement templates are versioned in the repository** -- never fetch agent enforcement code from a runtime URL. Use the pinned versions in `references/` or the canonical `prove-before-act` SDK package on PyPI and npm. Python users install `prove-before-act` and import its supported `xproof` module namespace.

---

## Configuration

### Option A: API Key Authentication

```bash
# ---- Prove Before Act ---------------------------------------------------------------
XPROOF_API_KEY="pm_..."                          # Your API key (from provebeforeact.com)
XPROOF_BASE_URL="https://provebeforeact.com"             # Production endpoint
```

Get an API key at [provebeforeact.com](https://provebeforeact.com) (connect wallet, go to Settings > API Keys).

### Option B: x402 Payment Protocol (No Account Required)

No configuration needed. Pay in USDC on Base (eip155:8453) directly in the HTTP request. The 402 response header tells your agent exactly what to pay (the current flat per-proof price, also served at `/api/pricing`).

> **WARNING -- autonomous payments:** x402 is an opt-in mode that enables your agent to initiate on-chain USDC transactions without per-transaction user confirmation. Before enabling x402 in production:
> - Set a **spending cap** in your agent framework (e.g. max $N/day or $N/session).
> - Require **human approval** for any single call that would exceed your risk threshold.
> - Note that `POST /api/batch` supports up to 100 items per call -- at the current per-item price, a batch of 100 costs 100× that price.
> - Disable x402 entirely in environments where autonomous spending is not authorised.

---

## 1. Core Skills Catalog

### 1.1 Proof Anchoring (REST API)
[Full Reference](references/certification.md)

| Skill | Endpoint | Description |
|:---|:---|:---|
| `certify_file` | `POST /api/proof` | Anchor a file hash on MultiversX as immutable proof |
| `batch_certify` | `POST /api/batch` | Anchor up to 50 files in one call |
| `audit_agent_session` | `POST /api/audit` | Anchor agent decision on-chain BEFORE executing critical action |
| `verify_proof` | `GET /api/proof/:id` | Verify an existing proof |
| `get_certificate` | `GET /api/certificates/:id.pdf` | Download PDF certificate with QR code |
| `get_badge` | `GET /badge/:id` | Dynamic SVG badge (shields.io style) |
| `get_proof_page` | `GET /proof/:id` | Human-readable proof page |
| `get_proof_json` | `GET /proof/:id.json` | Structured proof document (JSON) |
| `get_audit_page` | `GET /audit/:id` | Human-readable audit log page |

### 1.2 Proof Anchoring (MCP -- JSON-RPC 2.0)
[Full Reference](references/mcp.md)

| Tool | Description |
|:---|:---|
| `certify_file` | Create blockchain proof -- SHA-256 hash, filename, optional author/webhook |
| `verify_proof` | Verify existing proof by UUID |
| `get_proof` | Retrieve proof in JSON or Markdown format |
| `discover_services` | List capabilities, pricing, and usage guidance |
| `audit_agent_session` | Anchor agent decision on-chain BEFORE executing critical action |

### 1.3 Payment (x402)
[Full Reference](references/x402.md)

x402 is not a separate skill -- it is a payment method. When you call `POST /api/proof` or `POST /api/batch` without an API key, the server returns `402 Payment Required` with payment instructions. Your agent pays in USDC on Base and retries with an `X-Payment` header.

---

## 2. Coherence Loop — close the WHY→WHAT link

Anchoring the WHY and the WHAT is not enough: you must **link** them. An unlinked WHY anchor shows as **divergent** in your public coherence history after 1 hour, and after the 2-hour TTL it is additionally flagged as a proposed fault violation — both lower your public coherence rate.

**Full loop:** `check_coherence` (WHY) → execute → `certify_file` with `metadata.why_proof_id` (WHAT) → `POST /api/coherence/link`.

```bash
# Step 4 — close the loop (API key required; both proofs must be yours)
curl -X POST https://provebeforeact.com/api/coherence/link \
  -H "Authorization: Bearer pm_..." \
  -H "Content-Type: application/json" \
  -d '{"why_proof_id": "<UUID from check_coherence>", "what_proof_id": "<UUID from certify_file>"}'
# → 200 {"success": true, "coherence_check": {"coherence_score": 85, ...},
#        "score_breakdown": {"linked": true, "what_within_1h": true,
#                            "what_references_why": true, "what_confirmed_on_chain": false,
#                            "execution_preceded_intent": false}}
```

**Score (0–100):** 50 for linking + 15 if WHAT within 1h of WHY + 20 if WHAT's `metadata.why_proof_id` references the WHY + 15 if WHAT confirmed on-chain. WHAT certified *before* the WHY → base halved to 25.

**Error cases:**

| Status | Error | Meaning |
|:--|:--|:--|
| `409` | `ALREADY_LINKED` | WHY anchor already linked to a *different* WHAT. Re-linking the same pair returns 200 with `already_linked: true` (idempotent). |
| `400` | `NOT_A_COHERENCE_ANCHOR` | `why_proof_id` is a regular proof. Create the WHY via the `check_coherence` MCP tool, or certify with `metadata.type = "coherence_check"`. |
| `404` | `WHY_PROOF_NOT_FOUND` / `WHAT_PROOF_NOT_FOUND` | Proof missing or owned by another account. |

**SDK helpers:** `client.link_coherence(why_proof_id, what_proof_id)` (Python `xproof` ≥ 0.2.10) · `client.linkCoherence(whyProofId, whatProofId)` (npm `prove-before-act` ≥ 0.1.11).

**Check your history:** `GET https://provebeforeact.com/api/agents/<wallet>/coherence` — public; per-anchor status (`linked` / `pending` / `divergent`) + aggregate coherence rate.

---

## 3. Webhooks

Supply an optional `webhook_url` field on `POST /api/proof` or `POST /api/batch` to receive a callback when the proof is confirmed on-chain.

**Scope — the webhook payload contains only:**

| Field | Type | Description |
|:---|:---|:---|
| `proof_id` | string (UUID) | The proof identifier |
| `file_hash` | string | SHA-256 hex of the certified file |
| `filename` | string | Filename submitted with the proof |
| `status` | string | `"confirmed"` |
| `blockchain_tx` | string | MultiversX transaction hash |
| `explorer_url` | string | Link to the transaction on MultiversX Explorer |
| `timestamp` | string | ISO 8601 confirmation time |

No raw file content, no API keys, no account information, and no metadata beyond the above is ever sent to the webhook endpoint.

**Authentication:** Every delivery includes an `X-Webhook-Signature` header containing an HMAC-SHA256 signature computed with a per-relationship secret. Verify this signature before processing the payload. Retry policy: 3 attempts with exponential backoff (1 s, 5 s, 30 s).

**SSRF protection:** provebeforeact.com validates `webhook_url` before delivery. Private IP ranges (RFC 1918), loopback (`127.x`, `::1`), link-local, and non-HTTPS destinations are blocked. DNS rebinding is mitigated by pinning the resolved socket address to the pre-validated IP at connection time.

```bash
# Example proof request with webhook
curl -X POST https://provebeforeact.com/api/proof \
  -H "Authorization: Bearer pm_..." \
  -H "Content-Type: application/json" \
  -d '{
    "file_hash": "a1b2c3...",
    "filename": "output.json",
    "webhook_url": "https://your-agent.example.com/webhooks/prove-before-act"
  }'
```

---

## 9. Violations Layer (Base)

The violation flow is optional and deployment-dependent. Confirm the live contract and event status before relying on it for Base enforcement or trust scoring.

### Violation Types

| Type | Penalty | Trigger |
|:---|:---|:---|
| `gap` (fault) | Deployment-defined | Potential inactive-session gap |
| `burst` (breach) | Deployment-defined | Potential abnormal submission pattern |

Deployed Base contract sources retain their legacy Solidity names and cannot be renamed on-chain: [XProofViolations.sol](https://github.com/jasonxkensei/prove-before-act/blob/main/contracts/XProofViolations.sol) | [ViolationWatcher.sol](https://github.com/jasonxkensei/prove-before-act/blob/main/contracts/ViolationWatcher.sol)

Docs: [https://provebeforeact.com/docs/base-violations](https://provebeforeact.com/docs/base-violations)

---

## 10. Agent Proof Standard

Prove Before Act implements the open Agent Proof Standard -- a composable, chain-agnostic format for agent accountability.

Full specification: [AGENT_PROOF_STANDARD.md](https://github.com/jasonxkensei/prove-before-act/blob/main/AGENT_PROOF_STANDARD.md)

Standard API: `GET /api/standard` | `GET /api/standard/validate` (POST)

---

## 11. Discovery Endpoints

| Endpoint | Description |
|:---|:---|
| `GET /.well-known/agent.json` | Agent Protocol manifest |
| `GET /.well-known/mcp.json` | MCP server manifest |
| `GET /.well-known/agent-audit-schema.json` | Agent Audit Log canonical schema |
| `GET /ai-plugin.json` | OpenAI ChatGPT plugin manifest |
| `GET /llms.txt` | LLM-friendly summary |
| `GET /llms-full.txt` | Complete LLM reference |
| `POST /mcp` | MCP JSON-RPC 2.0 endpoint |
| `GET /mcp` | MCP capability discovery |
| `GET /api/standard` | Agent Proof Standard specification |
| `GET /agent-context` | Agent-first deep-dive: production patterns, retry policy, 4W walkthrough, x402, cost, MCP examples, framework integrations |

---

## 12. Command Cheatsheet

```bash
# Hash locally first -- the original content must never leave your environment.
# Prove Before Act only receives the SHA-256 hex hash, filename, and metadata you choose to share.
sha256sum myfile.pdf | awk '{print $1}'
# Then POST the hash to /api/proof

# Anchor via MCP
curl -X POST https://provebeforeact.com/mcp \
  -H "Authorization: Bearer pm_..." \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"certify_file","arguments":{"file_hash":"...","filename":"myfile.pdf"}}}'

# Verify a proof
curl https://provebeforeact.com/api/proof/<proof_id>

# Get badge (embed in README)
![Prove Before Act](https://provebeforeact.com/badge/<proof_id>)

# Batch anchor
curl -X POST https://provebeforeact.com/api/batch \
  -H "Authorization: Bearer pm_..." \
  -d '{"files":[{"file_hash":"...","filename":"a.txt"},{"file_hash":"...","filename":"b.txt"}]}'

# Close the WHY→WHAT coherence loop (after check_coherence + certify_file)
curl -X POST https://provebeforeact.com/api/coherence/link \
  -H "Authorization: Bearer pm_..." \
  -d '{"why_proof_id":"<why-uuid>","what_proof_id":"<what-uuid>"}'

# Health check
curl https://provebeforeact.com/api/acp/health
```
