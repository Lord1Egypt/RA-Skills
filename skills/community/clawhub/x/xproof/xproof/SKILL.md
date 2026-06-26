---
name: xproof
version: 3.1.0
description: Proof and accountability layer for AI agents. Anchor verifiable proofs on MultiversX, enforce audit logging, detect violations on Base. REST API, MCP, x402. Free trial with no wallet required. No proof = no action.
homepage: https://xproof.app
metadata: {"xproof":{"category":"proof,security,compliance,accountability","api_base":"https://xproof.app"}}
---

# xProof -- Proof & Accountability Layer for AI Agents

This skill enables your agent to **anchor verifiable proofs on the MultiversX blockchain**, **enforce pre-execution audit logging**, and **detect violations via Base** -- creating tamper-proof, publicly verifiable records of existence, authorship, timestamp, decision accountability, and trust.

**Why anchor proofs?** In competitive or transactional contexts, agents with on-chain proofs can demonstrate originality, integrity, and timing. Agents without proofs cannot. Verifiable proof is a structural advantage.

**Why audit?** Autonomous agents executing trades, deployments, or data access need an immutable record of every decision. The Agent Audit Log Standard enforces this: no proof = no execution.

**Why violations?** Trust requires accountability. xProof detects anomalies (gaps, burst patterns) and records violations on Base via smart contracts. Operators can subscribe to violation events and enforce policies automatically.

---

## 0. Quick Start -- Free Trial (No Wallet, No Card, 30 seconds)

**Get a `pm_` API key instantly with 10 free certifications.** No wallet, no credit card, no signup form. The fastest way for an autonomous agent to start anchoring proofs.

### REST (one curl)

```bash
# Step 1 — Register your agent (no auth required)
curl -X POST https://xproof.app/api/agent/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'
# Response: { "api_key": "pm_...", "trial": { "remaining": 10 }, ... }

# Step 2 — Anchor your first proof (use the api_key from step 1)
curl -X POST https://xproof.app/api/proof \
  -H "Authorization: Bearer pm_your_key" \
  -H "Content-Type: application/json" \
  -d '{"file_hash": "<sha256_hex>", "filename": "report.pdf", "author_name": "my-agent"}'
# Response: { "proof_id": "uuid", "verify_url": "...", "transaction_hash": "..." }

# Step 3 — Verify publicly (anyone, no auth)
curl https://xproof.app/api/proof/<proof_id>

# Step 4 — Check remaining credits + last proof
curl -H "Authorization: Bearer pm_your_key" https://xproof.app/api/agent/status
# Response: { "credits_remaining": 9, "last_proof": {...}, ... }
```

### MCP (Clawhub install)

```json
{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{
  "name":"register_free_trial",
  "arguments":{"agent_name":"my-agent"}
}}
```

The `register_free_trial` MCP tool requires **no authentication** -- it's the only MCP tool that can be called without an `Authorization` header. It returns the same `pm_` key as the REST endpoint.

### TypeScript SDK

```typescript
import { XProofClient, hashString } from "@xproof/xproof";

const client = await XProofClient.register("my-agent");  // 10 free certs, key stored
const proof = await client.certifyHash(hashString(JSON.stringify(decision)), "decision.json", "my-agent");
console.log(proof.verifyUrl);
```

### Python SDK

```python
from xproof import XProofClient

client = XProofClient.register("my-agent")  # 10 free certs
proof = client.certify_hash(sha256_hex, "decision.json", "my-agent")
```

### After the trial

When the 10 free proofs are consumed, the agent automatically transitions to per-proof billing. Three options, no friction:

| Option | Best for | Setup |
|:---|:---|:---|
| **Same `pm_` key + wallet top-up** | Existing trial agents | Connect wallet at https://xproof.app, deposit EGLD/USDC |
| **x402 USDC on Base** | Autonomous agents, no account | Pay $0.05/proof per request via 402 challenge (see Section 1.3) |
| **Existing API key (paid)** | Multi-agent fleets | Generate at xproof.app > Settings > API Keys |

---

## Quick Install (Skill files)

```bash
mkdir -p .agent/skills/xproof/references

# Core Skill
curl -sL https://raw.githubusercontent.com/jasonxkensei/xproof-openclaw-skill/main/xproof/SKILL.md \
  > .agent/skills/xproof/SKILL.md

# Reference Manuals
for f in certification x402 mcp api-reference; do
  curl -sL "https://raw.githubusercontent.com/jasonxkensei/xproof-openclaw-skill/main/xproof/references/${f}.md" \
    > ".agent/skills/xproof/references/${f}.md"
done
```

## Security

- **NEVER** commit API keys to a public repository.
- **ALWAYS** add `.env` to your `.gitignore`.
- API keys are prefixed `pm_` -- treat them like passwords.
- x402 mode requires no API key (payment replaces authentication).
- Free trial keys are unprivileged but still personal -- one trial per agent identity.
- **NEVER send plaintext content to xproof.app** -- always hash locally first (`sha256sum`, `crypto.subtle.digest`, or equivalent). The only field xproof accepts is `file_hash` (64-char SHA-256 hex). No raw text, documents, or binary data should ever leave your environment.
- **x402 is opt-in and autonomous** -- once enabled, your agent can initiate USDC payments on Base without per-transaction confirmation. Configure a spending cap in your agent framework and require human approval above your threshold before enabling x402 in production.
- **`llms.txt` and `llms-full.txt` are static documentation references** -- load them once at install time for API reference, not at runtime on every call. Fetching them dynamically on each invocation creates an unnecessary runtime dependency on xproof.app availability and a potential prompt-injection surface if the file is ever compromised.

---

## Configuration

### Option A: Free Trial (No Account, No Wallet)

```bash
# No env vars needed before first call. Get a key in one curl:
curl -X POST https://xproof.app/api/agent/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'
# Then store the returned api_key:
export XPROOF_API_KEY="pm_..."
```

10 free proofs. Best for trying out the skill, prototyping, and CI flows.

### Option B: API Key Authentication (Paid)

```bash
# ---- xProof ---------------------------------------------------------------
XPROOF_API_KEY="pm_..."                          # Your API key (from xproof.app)
XPROOF_BASE_URL="https://xproof.app"             # Production endpoint
```

Get a paid API key at [xproof.app](https://xproof.app) (connect wallet, go to Settings > API Keys). Same `pm_` prefix, no quota.

### Option C: x402 Payment Protocol (No Account Required)

No configuration needed. Pay $0.05 per proof in USDC on Base (eip155:8453) directly in the HTTP request. The 402 response header tells your agent exactly what to pay. Best for fully autonomous agents that already hold USDC on Base.

> **WARNING -- autonomous payments:** x402 is an opt-in mode that enables your agent to initiate on-chain USDC transactions without per-transaction user confirmation. Before enabling x402 in production:
> - Set a **spending cap** in your agent framework (e.g. max $N/day or $N/session).
> - Require **human approval** for any single call that would exceed your risk threshold.
> - Note that `POST /api/batch` supports up to 50 items per call -- at $0.05 each, a single batch can reach $2.50.
> - Disable x402 entirely in environments where autonomous spending is not authorised.

---

## 1. Core Skills Catalog

### 1.1 Proof Anchoring (REST API)
[Full Reference](references/certification.md) | [API Reference](references/api-reference.md)

| Skill | Endpoint | Auth | Description |
|:---|:---|:---|:---|
| `register_free_trial` | `POST /api/agent/register` | None | Get a `pm_` key + 10 free proofs (no wallet) |
| `agent_status` | `GET /api/agent/status` | Bearer | Credits remaining, last proof, agent metadata |
| `certify_file` | `POST /api/proof` | Bearer or x402 | Anchor a file hash on MultiversX as immutable proof |
| `batch_certify` | `POST /api/batch` | Bearer or x402 | Anchor up to 50 files in one call |
| `audit_agent_session` | `POST /api/audit` | Bearer | Anchor agent decision on-chain BEFORE executing critical action |
| `verify_proof` | `GET /api/proof/:id` | None | Verify an existing proof |
| `get_certificate` | `GET /api/certificates/:id.pdf` | None | Download PDF certificate with QR code |
| `get_badge` | `GET /badge/:id` | None | Dynamic SVG badge (shields.io style) |
| `get_proof_page` | `GET /proof/:id` | None | Human-readable proof page |
| `get_proof_json` | `GET /proof/:id.json` | None | Structured proof document (JSON) |
| `get_audit_page` | `GET /audit/:id` | None | Human-readable audit log page |

### 1.2 Proof Anchoring (MCP -- JSON-RPC 2.0)
[Full Reference](references/mcp.md)

| Tool | Auth | Description |
|:---|:---|:---|
| `register_free_trial` | **None** | Get a free `pm_` key + 10 proofs without an account or wallet |
| `certify_file` | Bearer | Create blockchain proof -- SHA-256 hash, filename, optional author/webhook |
| `certify_with_confidence` | Bearer | Certify with confidence score, model name, and reasoning trace |
| `verify_proof` | None | Verify existing proof by UUID |
| `get_proof` | None | Retrieve proof in JSON or Markdown format |
| `discover_services` | None | List capabilities, pricing, and usage guidance |
| `audit_agent_session` | Bearer | Anchor agent decision on-chain BEFORE executing critical action |
| `check_attestations` | None | Check domain-specific attestations for an agent wallet on Base |
| `investigate_proof` | None | Reconstruct the full 4W audit trail for a contested agent action |

### 1.3 Payment (x402)
[Full Reference](references/x402.md)

x402 is not a separate skill -- it is a payment method. When you call `POST /api/proof` or `POST /api/batch` without an API key, the server returns `402 Payment Required` with payment instructions. Your agent pays in USDC on Base and retries with an `X-Payment` header.

---

## 2. The Proof Lifecycle

```
+--------------+     +--------------+     +--------------+     +--------------+
|  Hash file   |---->|  POST /api/  |---->|  On-chain    |---->|  Proof       |
|  (SHA-256)   |     |  proof       |     |  anchoring   |     |  verified    |
+--------------+     +--------------+     +--------------+     +--------------+
                                                                      |
                     +--------------+     +--------------+           |
                     |  Embed badge |<----|  Get PDF /   |<----------+
                     |  in output   |     |  badge / URL |
                     +--------------+     +--------------+
```

### Step-by-Step

1. **Register (optional, free)** -- if you don't have a key yet, `POST /api/agent/register` for an instant `pm_` trial key (10 proofs, no wallet)
2. **Hash locally** -- compute SHA-256 of your file (client-side; the file never leaves your machine). The original content must never leave your environment -- xproof only receives the hash, filename, and metadata you choose to share.
3. **Send metadata** -- POST the hash + filename to `/api/proof` (with API key or x402 payment)
4. **Receive proof** -- xProof records the hash on MultiversX mainnet (6-second finality)
5. **Verify anytime** -- anyone can verify via proof URL, JSON endpoint, or blockchain explorer
6. **Embed proof** -- use the SVG badge, PDF certificate, or proof URL in your deliverables

---

## 3. Authentication Methods

### Free Trial (No Wallet, No Card)

```bash
# Get a pm_ key instantly with 10 free proofs
curl -X POST https://xproof.app/api/agent/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'
```

The returned `api_key` works exactly like a paid key for all `Bearer pm_...` endpoints.

### API Key (Bearer Token)

```bash
curl -X POST https://xproof.app/api/proof \
  -H "Authorization: Bearer pm_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "file_hash": "a1b2c3d4e5f6...64hex",
    "filename": "report.pdf",
    "author_name": "MyAgent"
  }'
```

### x402 (USDC on Base -- No Account Required)

```bash
# Step 1: Request without auth returns 402 with payment instructions
curl -X POST https://xproof.app/api/proof \
  -H "Content-Type: application/json" \
  -d '{"file_hash": "a1b2c3...", "filename": "report.pdf"}'
# Response: 402 with JSON body containing accepts[{scheme, price, network, payTo}]

# Step 2: Pay USDC on Base, then retry with X-Payment header (base64 JSON)
curl -X POST https://xproof.app/api/proof \
  -H "Content-Type: application/json" \
  -H "X-Payment: <base64_encoded_payment_payload>" \
  -d '{"file_hash": "a1b2c3...", "filename": "report.pdf"}'
```

### MCP (JSON-RPC 2.0)

**Important:** MCP requires the `Accept: application/json, text/event-stream` header on every call.

```bash
curl -X POST https://xproof.app/mcp \
  -H "Authorization: Bearer pm_your_key_here" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/call",
    "params": {
      "name": "certify_file",
      "arguments": {
        "file_hash": "a1b2c3d4e5f6...64hex",
        "filename": "output.json"
      }
    }
  }'
```

The MCP tool `register_free_trial` is the only one that does **not** require the `Authorization` header -- use it to bootstrap a key on first run.

---

## 4. Batch Proof Anchoring

Anchor up to 50 files in a single API call:

```bash
curl -X POST https://xproof.app/api/batch \
  -H "Authorization: Bearer pm_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {"file_hash": "abc123...", "filename": "model.bin"},
      {"file_hash": "def456...", "filename": "training_data.csv"},
      {"file_hash": "789ghi...", "filename": "config.yaml"}
    ],
    "author_name": "MyAgent"
  }'
```

Each file in the batch consumes one credit (trial users) or one billable unit (paid users).

---

## 5. Webhooks

Receive a POST notification when your proof is confirmed on-chain:

```bash
curl -X POST https://xproof.app/api/proof \
  -H "Authorization: Bearer pm_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "file_hash": "a1b2c3...",
    "filename": "deliverable.pdf",
    "webhook_url": "https://your-agent.com/hooks/xproof"
  }'
```

The webhook payload includes proof ID, file hash, blockchain transaction hash, and explorer URL. Signed with HMAC-SHA256 in the `X-Webhook-Signature` header. Retry policy: 3 attempts with exponential backoff.

---

## 6. When to Anchor Proofs

Autonomous agents should anchor proofs whenever provenance, integrity, or priority matters:

- **After generating code, contracts, or configs** -- proves authorship and timestamp
- **Before delivering work products** -- proves integrity at handoff
- **After creating datasets or models** -- proves version and origin
- **Before publishing reports or documents** -- establishes priority
- **After completing build artifacts** -- creates auditable record
- **When resolving disputes** -- timestamped proof settles who created what first
- **When exchanging assets between agents** -- chain of custody

---

## 7. Integration with MultiversX Agent Stack

xProof is complementary to the core MultiversX agent skills:

| MultiversX Skill | xProof Complement |
|:---|:---|
| `init_job` (Validation Registry) | Anchor job output before submitting proof |
| `submit_proof` (Validation Registry) | Use xProof hash as the proof payload |
| `register_agent` (Identity Registry) | Anchor your agent manifest for integrity |
| `deposit` (Escrow) | Anchor deliverables before release |

### Typical Flow: Job + Proof

```
1. Accept job via init_job
2. Do the work
3. Anchor output via xProof (POST /api/proof)
4. Submit xProof hash as proof via submit_proof
5. Employer verifies via xProof URL
6. Escrow released
```

---

## 8. Agent Audit Log Standard

The Agent Audit Log is a compliance primitive for autonomous agents. Before executing any critical action (trade, deploy, data access, transfer), the agent MUST anchor its decision on-chain. No proof_id = no execution.

### Why Audit?

- **Regulatory compliance** -- Immutable record of every agent decision, timestamped and anchored on-chain
- **Dispute resolution** -- Prove what the agent decided, why, and when
- **Trust signal** -- Agents with audit trails are verifiably accountable
- **Blocking enforcement** -- If the audit call fails, the action does not execute

### Audit Endpoint

```bash
curl -X POST https://xproof.app/api/audit \
  -H "Authorization: Bearer pm_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "erd1abc...or-any-identifier",
    "session_id": "550e8400-e29b-41d4-a716-446655440000",
    "action_type": "trade",
    "action_description": "Buy 10 EGLD at market price on xExchange",
    "inputs_hash": "a1b2c3d4e5f6...64hex",
    "risk_level": "high",
    "risk_summary": "Market order on volatile asset, amount exceeds daily threshold",
    "decision": "approved",
    "context": {"model": "gpt-4", "environment": "production"}
  }'
```

**Response:**

```json
{
  "proof_id": "uuid",
  "audit_url": "https://xproof.app/audit/uuid",
  "proof_url": "https://xproof.app/proof/uuid",
  "decision": "approved",
  "risk_level": "high",
  "inputs_hash": "a1b2c3...",
  "blockchain": {
    "network": "mainnet",
    "transaction_hash": "abc123...",
    "explorer_url": "https://explorer.multiversx.com/transactions/abc123..."
  }
}
```

### Canonical Schema

10 fields. JSON Schema: `https://xproof.app/.well-known/agent-audit-schema.json`

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `agent_id` | string | Yes | Agent identifier (wallet, DID, or name) |
| `session_id` | string | Yes | UUID for this execution session |
| `action_type` | string | Yes | Category: trade, deploy, data_access, transfer, api_call |
| `action_description` | string | Yes | Human-readable intent |
| `inputs_hash` | string | Yes | SHA-256 of action inputs (64 hex chars) |
| `risk_level` | enum | Yes | low, medium, high, critical |
| `risk_summary` | string | No | Explanation of risk factors |
| `decision` | enum | Yes | approved, rejected, deferred |
| `context` | object | No | Additional metadata (model, environment, etc.) |
| `timestamp` | string | No | ISO 8601 (auto-generated if omitted) |

### Enforcement Pattern

```
1. Agent prepares action (trade, deploy, etc.)
2. Agent calls POST /api/audit with action details
3. If proof_id returned -> proceed with action
4. If API fails, timeout, or no proof_id -> BLOCK execution (throw error)
5. No fallback. No soft fail. No silent continue.
```

Guard templates for multiple frameworks:
- **LangChain**: `https://xproof.app/agent-tools/audit-guard-langchain.py`
- **CrewAI**: `https://xproof.app/agent-tools/audit-guard-crewai.py`
- **n8n**: `https://xproof.app/agent-tools/audit-guard-n8n.json`
- **ElizaOS**: `https://xproof.app/agent-tools/audit-guard-eliza.ts`
- **ElizaOS Plugin (NPM)**: `npm install xproof-eliza-plugin`

### When to Audit

Autonomous agents should audit BEFORE executing any action where accountability matters:

- **Before executing trades** -- proves intent, risk assessment, and decision
- **Before deploying contracts** -- immutable record of deployment decision
- **Before accessing sensitive data** -- audit trail for data governance
- **Before transferring assets** -- proves authorization and risk review
- **Before calling external APIs** -- records outbound action intent

---

## 9. Violations Layer (Base)

xProof monitors agent behavior and detects anomalies. When a violation is confirmed, it is recorded on Base via the `XProofViolations.sol` smart contract, impacting the agent's trust score.

### Violation Types

| Type | Penalty | Trigger |
|:---|:---|:---|
| `gap` (fault) | -150 trust score | No proof activity for 30+ minutes during active session |
| `burst` (breach) | -500 trust score | Abnormal spike in proof submissions |

### Violation Lifecycle

```
detected -> proposed -> confirmed (-penalty) or rejected
```

Auto-confirmed for irrefutable anomalies (gap > threshold). Operators can subscribe to on-chain violation events via `ViolationWatcher.sol` (3 modes: ALERT_ONLY, AUTO_PAUSE_FAULT, AUTO_PAUSE_BREACH).

### Operator Integration

```solidity
// Subscribe to violations for a specific agent
IXProofViolations(xproofContract).getViolations(agentId)
```

Smart contracts: [XProofViolations.sol](https://github.com/jasonxkensei/xProof/blob/main/contracts/XProofViolations.sol) | [ViolationWatcher.sol](https://github.com/jasonxkensei/xProof/blob/main/contracts/ViolationWatcher.sol)

Docs: [https://xproof.app/docs/base-violations](https://xproof.app/docs/base-violations)

---

## 10. Agent Proof Standard

xProof implements the open Agent Proof Standard -- a composable, chain-agnostic format for agent accountability. Any platform can adopt the standard to interoperate with xProof proofs.

- **4W Framework**: WHO (agent_id) / WHAT (file_hash + metadata) / WHEN (timestamp + chain finality) / WHY (action_description + risk_level)
- **Signature**: Mandatory in v1
- **agent_id**: Free string (wallet address, DID, or plain identifier)

Full specification: [AGENT_PROOF_STANDARD.md](https://github.com/jasonxkensei/xProof/blob/main/AGENT_PROOF_STANDARD.md)

Standard API: `GET /api/standard` | `POST /api/standard/validate`

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
| `GET /api/acp/openapi.json` | OpenAPI 3.1 spec for the full REST surface |

---

## 12. Command Cheatsheet

```bash
# Get a free pm_ key (no wallet, no card)
curl -X POST https://xproof.app/api/agent/register \
  -H "Content-Type: application/json" \
  -d '{"agent_name": "my-agent"}'

# Hash a file locally
sha256sum myfile.pdf | awk '{print $1}'

# Anchor a single file proof
curl -X POST https://xproof.app/api/proof \
  -H "Authorization: Bearer pm_..." \
  -d '{"file_hash":"...","filename":"myfile.pdf","author_name":"my-agent"}'

# Anchor via MCP (note the Accept header)
curl -X POST https://xproof.app/mcp \
  -H "Authorization: Bearer pm_..." \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"certify_file","arguments":{"file_hash":"...","filename":"myfile.pdf"}}}'

# Verify a proof (no auth)
curl https://xproof.app/api/proof/<proof_id>

# Check agent status (credits + last proof)
curl -H "Authorization: Bearer pm_..." https://xproof.app/api/agent/status

# Get badge (embed in README)
![xProof](https://xproof.app/badge/<proof_id>)

# Batch anchor up to 50 files
curl -X POST https://xproof.app/api/batch \
  -H "Authorization: Bearer pm_..." \
  -d '{"files":[{"file_hash":"...","filename":"a.txt"},{"file_hash":"...","filename":"b.txt"}]}'

# Audit a critical action (block on failure)
curl -X POST https://xproof.app/api/audit \
  -H "Authorization: Bearer pm_..." \
  -d '{"agent_id":"my-agent","session_id":"<uuid>","action_type":"trade","action_description":"...","inputs_hash":"...","risk_level":"high","decision":"approved"}'

# Health check
curl https://xproof.app/api/acp/health
```
