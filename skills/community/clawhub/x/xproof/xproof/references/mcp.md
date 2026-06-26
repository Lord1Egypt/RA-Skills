# MCP Server

xProof exposes a Model Context Protocol (MCP) JSON-RPC 2.0 endpoint for AI agent integration.

## Endpoint

```
POST https://xproof.app/mcp
```

**Required headers on every call:**

```
Content-Type: application/json
Accept: application/json, text/event-stream
```

**Authentication:** API Key (`Authorization: Bearer pm_...`) -- except for `register_free_trial`, `verify_proof`, `get_proof`, `discover_services`, `check_attestations`, and `investigate_proof`, which are public.

## Bootstrap (No Account, No Wallet)

If your agent has no key yet, call `register_free_trial` first -- it's the only MCP tool that requires no authentication. It returns a `pm_` API key with 10 free certifications.

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "register_free_trial",
    "arguments": {
      "agent_name": "my-agent"
    }
  }
}
```

**Response (excerpt):**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"api_key\":\"pm_xxxxx\",\"trial\":{\"quota\":10,\"used\":0,\"remaining\":10},\"agent_name\":\"my-agent\",\"endpoints\":{...}}"
    }]
  }
}
```

Store the `api_key` and use it as `Authorization: Bearer pm_xxxxx` for all subsequent authenticated calls.

## Available Tools

### `register_free_trial` (no auth)

Get a free `pm_` API key instantly. 10 free certifications, no wallet, no credit card.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `agent_name` | string | Yes | Agent identifier (2-128 chars, used to deduplicate trials) |

---

### `certify_file`

Create a blockchain certification for a file.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `file_hash` | string | Yes | SHA-256 hash (64 hex characters) |
| `filename` | string | Yes | Original filename with extension |
| `author_name` | string | No | Name of the certifier (default: "AI Agent") |
| `webhook_url` | string | No | HTTPS URL for on-chain confirmation callback |

**Example:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "certify_file",
    "arguments": {
      "file_hash": "a1b2c3d4e5f6789012345678901234567890123456789012345678901234abcd",
      "filename": "report.pdf",
      "author_name": "MyAgent"
    }
  }
}
```

**Response:**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [{
      "type": "text",
      "text": "{\"proof_id\":\"uuid-v4\",\"status\":\"certified\",\"file_hash\":\"a1b2c3...\",\"filename\":\"report.pdf\",\"verify_url\":\"https://xproof.app/proof/uuid-v4\",\"certificate_url\":\"https://xproof.app/api/certificates/uuid-v4.pdf\",\"blockchain\":{\"network\":\"MultiversX\",\"transaction_hash\":\"abc123...\",\"explorer_url\":\"https://explorer.multiversx.com/transactions/abc123...\"},\"timestamp\":\"2026-02-19T12:00:00.000Z\"}"
    }]
  }
}
```

---

### `certify_with_confidence`

Certify a file along with a confidence score, model name, and reasoning trace -- used for AI-generated content where provenance must include the model's self-reported certainty.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `file_hash` | string | Yes | SHA-256 hash of the artifact (64 hex chars) |
| `filename` | string | Yes | Original filename |
| `confidence` | number | Yes | 0.0 to 1.0 -- model's self-reported confidence |
| `model_name` | string | Yes | e.g. `gpt-4o`, `claude-sonnet-4`, `grok-4` |
| `reasoning_hash` | string | No | SHA-256 of the reasoning trace (linked WHY proof) |
| `author_name` | string | No | Default: "AI Agent" |

---

### `verify_proof` (no auth)

Verify an existing certification by UUID.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `proof_id` | string | Yes | UUID of the certification to verify |

---

### `get_proof` (no auth)

Retrieve a proof in structured JSON or Markdown format.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `proof_id` | string | Yes | UUID of the certification |
| `format` | string | No | `json` (default) or `md` |

Use `md` format for LLM consumption -- produces human-readable Markdown with all proof details.

---

### `discover_services` (no auth)

List xProof capabilities, pricing, and usage guidance. No parameters required.

**Returns:** Service description, pricing tiers ($0.05 / $0.025 / $0.01 per proof depending on all-time volume), list of tools, certification triggers, batch API details, free trial details, and supported protocols.

---

### `audit_agent_session`

Anchor an agent's decision on-chain BEFORE executing a critical action. If the call fails or no `proof_id` is returned, the agent MUST block execution.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `agent_id` | string | Yes | Wallet, DID, or free identifier |
| `session_id` | string | Yes | UUID for the execution session |
| `action_type` | string | Yes | `trade` / `deploy` / `data_access` / `transfer` / `api_call` |
| `action_description` | string | Yes | Human-readable intent |
| `inputs_hash` | string | Yes | SHA-256 of canonical action inputs |
| `risk_level` | enum | Yes | `low` / `medium` / `high` / `critical` |
| `decision` | enum | Yes | `approved` / `rejected` / `deferred` |
| `risk_summary` | string | No | Explanation of risk factors |
| `context` | object | No | Free-form metadata (model, env, etc.) |

See [SKILL.md Section 8](../SKILL.md#8-agent-audit-log-standard) for the complete enforcement pattern.

---

### `check_attestations` (no auth)

Check domain-specific attestations for an agent wallet on Base.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `wallet_address` | string | Yes | EVM address on Base (0x...) |
| `domain` | string | No | Filter by domain (e.g. `kyc`, `code-review`, `compliance`) |

Returns the list of attestations issued by recognized issuers, with timestamps and trust weights.

---

### `investigate_proof` (no auth)

Reconstruct the full 4W audit trail for a contested agent action. Walks back from a single proof_id to surface the WHY (decision), WHAT (output), WHEN (timestamps), and WHO (agent identity), including any linked audit log and violation records.

**Parameters:**

| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| `proof_id` | string | Yes | UUID of the disputed proof or audit record |
| `depth` | integer | No | Trail depth (default 3) |

Use this when an agent's action is challenged -- the response is a structured timeline suitable for dispute resolution or regulatory review.

---

## Discovery

| Endpoint | Description |
|:---|:---|
| `GET /mcp` | MCP capability discovery (tool list) |
| `GET /.well-known/mcp.json` | MCP server manifest |

## LLM Prompt Engineering

When exposing xProof to an LLM, use:

> **Skill: Bootstrap (no account)**
> "If you have no XPROOF_API_KEY in env, call `register_free_trial` first with your agent name. Store the returned `api_key`. You get 10 free proofs."

> **Skill: Certify**
> "Use this to create an immutable blockchain proof for a file. Compute SHA-256 of the file content, then call `certify_file` with the hash and filename. Cost: trial-free or $0.05."

> **Skill: Audit before action**
> "Before any high-risk action (trade, deploy, transfer), call `audit_agent_session` with the action details. If no `proof_id` is returned, BLOCK the action."

> **Skill: Verify**
> "Use this to check if a file has been certified. Pass the proof UUID to `verify_proof`. Returns blockchain transaction, timestamp, and verification status."
