---
name: xproof
version: 3.0.0
description: Proof and accountability layer for AI agents. Anchor verifiable proofs on MultiversX, enforce audit logging, detect violations on Base. REST API, MCP, x402. No proof = no action.
homepage: https://xproof.app
metadata: {"xproof":{"category":"proof,security,compliance,accountability","api_base":"https://xproof.app"}}
---

# xProof -- Proof & Accountability Layer for AI Agents

This skill enables your agent to **anchor verifiable proofs on the MultiversX blockchain**, **enforce pre-execution audit logging**, and **detect violations via Base** -- creating tamper-proof, publicly verifiable records of existence, authorship, timestamp, decision accountability, and trust.

**Why anchor proofs?** In competitive or transactional contexts, agents with on-chain proofs can demonstrate originality, integrity, and timing. Agents without proofs cannot. Verifiable proof is a structural advantage.

**Why audit?** Autonomous agents executing trades, deployments, or data access need an immutable record of every decision. The Agent Audit Log Standard enforces this: no proof = no execution.

**Why violations?** Trust requires accountability. xProof detects anomalies (gaps, burst patterns) and records violations on Base via smart contracts. Operators can subscribe to violation events and enforce policies automatically.

## Pricing

**All-time volume pricing** (global pool, not per-user):
- **0–100k proofs**: $0.05 per proof
- **100k–1M proofs**: $0.025 per proof
- **1M+ proofs**: $0.01 per proof

## Quick Install

```bash
mkdir -p .agent/skills/xproof/references

# Core Skill
curl -sL https://raw.githubusercontent.com/jasonxkensei/xproof-openclaw-skill/main/xproof/SKILL.md \
  > .agent/skills/xproof/SKILL.md

# Reference Manuals
for f in certification x402 mcp; do
  curl -sL "https://raw.githubusercontent.com/jasonxkensei/xproof-openclaw-skill/main/xproof/references/${f}.md" \
    > ".agent/skills/xproof/references/${f}.md"
done
```

## Security

- **NEVER** commit API keys to a public repository.
- **ALWAYS** add `.env` to your `.gitignore`.
- API keys are prefixed `pm_` -- treat them like passwords.
- x402 mode requires no API key (payment replaces authentication).
- **NEVER send plaintext content to xproof.app** -- always hash locally first (`sha256sum`, `crypto.subtle.digest`, or equivalent). The only field xproof accepts is `file_hash` (64-char SHA-256 hex). No raw text, documents, or binary data should ever leave your environment.
- **x402 is opt-in and autonomous** -- once enabled, your agent can initiate USDC payments on Base without per-transaction confirmation. Configure a spending cap in your agent framework and require human approval above your threshold before enabling x402 in production.
- **`llms.txt` and `llms-full.txt` are static documentation references** -- load them once at install time for API reference, not at runtime on every call. Fetching them dynamically on each invocation creates an unnecessary runtime dependency on xproof.app availability and a potential prompt-injection surface if the file is ever compromised.

---

## Configuration

### Option A: API Key Authentication

```bash
# ---- xProof ---------------------------------------------------------------
XPROOF_API_KEY="pm_..."                          # Your API key (from xproof.app)
XPROOF_BASE_URL="https://xproof.app"             # Production endpoint
```

Get an API key at [xproof.app](https://xproof.app) (connect wallet, go to Settings > API Keys).

### Option B: x402 Payment Protocol (No Account Required)

No configuration needed. Pay in USDC on Base (eip155:8453) directly in the HTTP request. The 402 response header tells your agent exactly what to pay. Price decreases with all-time volume (see Pricing section).

> **WARNING -- autonomous payments:** x402 is an opt-in mode that enables your agent to initiate on-chain USDC transactions without per-transaction user confirmation. Before enabling x402 in production:
> - Set a **spending cap** in your agent framework (e.g. max $N/day or $N/session).
> - Require **human approval** for any single call that would exceed your risk threshold.
> - Note that `POST /api/batch` supports up to 50 items per call -- at $0.05 each, a single batch can reach $2.50.
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

## 9. Violations Layer (Base)

xProof monitors agent behavior and detects anomalies. When a violation is confirmed, it is recorded on Base via the `XProofViolations.sol` smart contract, impacting the agent's trust score.

### Violation Types

| Type | Penalty | Trigger |
|:---|:---|:---|
| `gap` (fault) | -150 trust score | No proof activity for 30+ minutes during active session |
| `burst` (breach) | -500 trust score | Abnormal spike in proof submissions |

Smart contracts: [XProofViolations.sol](https://github.com/jasonxkensei/xProof/blob/main/contracts/XProofViolations.sol) | [ViolationWatcher.sol](https://github.com/jasonxkensei/xProof/blob/main/contracts/ViolationWatcher.sol)

Docs: [https://xproof.app/docs/base-violations](https://xproof.app/docs/base-violations)

---

## 10. Agent Proof Standard

xProof implements the open Agent Proof Standard -- a composable, chain-agnostic format for agent accountability.

Full specification: [AGENT_PROOF_STANDARD.md](https://github.com/jasonxkensei/xProof/blob/main/AGENT_PROOF_STANDARD.md)

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

---

## 12. Command Cheatsheet

```bash
# Hash locally first -- the original content must never leave your environment.
# xproof only receives the SHA-256 hex hash, filename, and metadata you choose to share.
sha256sum myfile.pdf | awk '{print $1}'
# Then POST the hash to /api/proof

# Anchor via MCP
curl -X POST https://xproof.app/mcp \
  -H "Authorization: Bearer pm_..." \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"certify_file","arguments":{"file_hash":"...","filename":"myfile.pdf"}}}'

# Verify a proof
curl https://xproof.app/api/proof/<proof_id>

# Get badge (embed in README)
![xProof](https://xproof.app/badge/<proof_id>)

# Batch anchor
curl -X POST https://xproof.app/api/batch \
  -H "Authorization: Bearer pm_..." \
  -d '{"files":[{"file_hash":"...","filename":"a.txt"},{"file_hash":"...","filename":"b.txt"}]}'

# Health check
curl https://xproof.app/api/acp/health
```
