# ShieldBot API Reference

Base URL: `https://api.shieldbotsecurity.online`

All endpoints return JSON objects directly. There is **no** `{"success": true, "data": {...}}` wrapper.

---

## Rate Limits

| Tier   | Limit         | Burst |
|--------|---------------|-------|
| Public | 30 req/min    | 10    |

Exceeding the limit returns `429 Too Many Requests`.

---

## Supported Chains

| Chain            | chain_id |
|------------------|----------|
| BNB Chain        | 56       |
| Ethereum         | 1        |
| Polygon          | 137      |
| Arbitrum One     | 42161    |
| Base             | 8453     |
| Avalanche C-Chain| 43114    |
| Fantom           | 250      |
| Optimism         | 10       |

Default `chain_id` is `56` (BNB Chain) when not specified.

---

## Endpoints

### POST /api/scan

Scan a token or contract address for risk signals.

**Request Body**

```json
{
  "address": "0x...",
  "chain_id": 56
}
```

| Field      | Type   | Required | Description                        |
|------------|--------|----------|------------------------------------|
| `address`  | string | yes      | Token or contract address to scan  |
| `chain_id` | int    | no       | Chain ID (default `56`)            |

**Response** (returned directly)

```json
{
  "address": "string",
  "is_verified": "bool",
  "is_contract": "bool",
  "risk_level": "string (low|medium|high|unknown)",
  "risk_score": "int (0-100)",
  "confidence": "int (0-100)",
  "checks": {
    "ownership_renounced": "bool",
    "is_honeypot": "bool"
  },
  "warnings": ["string"],
  "scam_matches": [],
  "scan_type": "contract",
  "chain_id": "int",
  "network": "string"
}
```

| Field            | Type     | Description                                     |
|------------------|----------|-------------------------------------------------|
| `address`        | string   | Scanned address                                 |
| `is_verified`    | bool     | Whether the contract source is verified          |
| `is_contract`    | bool     | Whether the address is a contract (vs EOA)       |
| `risk_level`     | string   | One of `low`, `medium`, `high`, `unknown`        |
| `risk_score`     | int      | Heuristic risk score, 0 (safe) to 100 (critical) |
| `confidence`     | int      | Confidence in the assessment, 0-100              |
| `checks`         | object   | Individual boolean checks (honeypot, ownership, etc.) |
| `warnings`       | string[] | Human-readable warning messages                  |
| `scam_matches`   | array    | Known scam database matches                      |
| `scan_type`      | string   | Always `"contract"`                              |
| `chain_id`       | int      | Chain the scan was performed on                  |
| `network`        | string   | Human-readable network name                      |

---

### POST /api/firewall

Decode and analyse a pending transaction before signing.

**Request Body**

```json
{
  "to": "0x...",
  "data": "0x...",
  "value": "0",
  "from": "0x...",
  "chain_id": 56
}
```

| Field      | Type   | Required | Description                          |
|------------|--------|----------|--------------------------------------|
| `to`       | string | yes      | Destination contract address         |
| `data`     | string | yes      | Raw transaction calldata (hex)       |
| `value`    | string | no       | Wei value being sent (default `"0"`) |
| `from`     | string | no       | Sender address                       |
| `chain_id` | int    | no       | Chain ID (default `56`)              |

**Response** (returned directly)

```json
{
  "classification": "string (BLOCK_RECOMMENDED|HIGH_RISK|CAUTION|SAFE)",
  "risk_score": "int (0-100)",
  "decoded_action": "string",
  "calldata_details": {
    "category": "string",
    "fields": [
      {"label": "string", "value": "string"}
    ]
  },
  "danger_signals": ["string"],
  "transaction_impact": {
    "sending": "string",
    "granting_access": "string",
    "recipient": "string",
    "post_tx_state": "string"
  },
  "analysis": "string",
  "plain_english": "string",
  "verdict": "string",
  "raw_checks": {
    "is_verified": "bool",
    "scam_matches": "int",
    "contract_age_days": "int|null",
    "is_honeypot": "bool",
    "ownership_renounced": "bool",
    "risk_score_heuristic": "int",
    "whitelisted_router": "string|null"
  },
  "shield_score": {
    "overall": "int",
    "category_scores": {},
    "risk_level": "string",
    "threat_type": "string",
    "critical_flags": [],
    "confidence": "int"
  },
  "simulation": "dict|null",
  "asset_delta": ["string"],
  "greenfield_url": "string|null",
  "chain_id": "int",
  "network": "string",
  "partial": "bool",
  "failed_sources": ["string"],
  "policy_mode": "string",
  "campaign_context": "dict|null"
}
```

| Field                | Type     | Description                                                        |
|----------------------|----------|--------------------------------------------------------------------|
| `classification`     | string   | Final verdict: `BLOCK_RECOMMENDED`, `HIGH_RISK`, `CAUTION`, `SAFE` |
| `risk_score`         | int      | Overall risk score 0-100                                            |
| `decoded_action`     | string   | Human-readable description of what the tx does                      |
| `calldata_details`   | object   | Decoded calldata with category and labelled fields                  |
| `danger_signals`     | string[] | Specific danger signals detected                                    |
| `transaction_impact` | object   | What the tx sends, grants, to whom, and resulting state             |
| `analysis`           | string   | Detailed analysis text                                              |
| `plain_english`      | string   | Plain-English summary of the transaction                            |
| `verdict`            | string   | Short verdict string                                                |
| `raw_checks`         | object   | Raw heuristic checks (honeypot, verification, scam matches, etc.)  |
| `shield_score`       | object   | Composite shield score with category breakdown and threat type      |
| `simulation`         | dict/null| Tenderly simulation result, or null if unavailable                  |
| `asset_delta`        | string[] | Human-readable list of asset changes from simulation                |
| `greenfield_url`     | str/null | BNB Greenfield link if applicable                                   |
| `chain_id`           | int      | Chain the analysis was performed on                                 |
| `network`            | string   | Human-readable network name                                         |
| `partial`            | bool     | `true` if some data sources failed                                  |
| `failed_sources`     | string[] | Names of sources that timed out or errored                          |
| `policy_mode`        | string   | Active policy mode for the request                                  |
| `campaign_context`   | dict/null| Cross-chain campaign context if detected                            |

---

### GET /api/campaign/{address}

Investigate the deployment campaign behind a contract: deployer, funder, cross-chain siblings, and cluster analysis.

**Path Parameters**

| Parameter | Type   | Description              |
|-----------|--------|--------------------------|
| `address` | string | Contract address to trace |

**Query Parameters**

| Parameter  | Type | Required | Description             |
|------------|------|----------|-------------------------|
| `chain_id` | int  | no       | Chain ID (default `56`) |

**Response** (returned directly)

```json
{
  "address": "string",
  "deployer": "string|null",
  "funder": "string|null",
  "funder_value_wei": "string",
  "contracts_deployed": [
    {"contract": "string", "tx_hash": "string"}
  ],
  "total_deployed": "int",
  "cross_chain_contracts": [
    {
      "contract": "string",
      "chain_id": "int",
      "tx_hash": "string",
      "risk_score": "float|null",
      "risk_level": "string|null",
      "archetype": "string|null"
    }
  ],
  "funder_cluster": [
    {
      "deployer": "string",
      "chain_id": "int",
      "funding_value_wei": "int",
      "contract_count": "int",
      "high_risk_contracts": "int"
    }
  ],
  "campaign": {
    "is_campaign": "bool",
    "severity": "string (NONE|LOW|MEDIUM|HIGH)",
    "risk_boost": "int",
    "indicators": ["string"],
    "chains_involved": ["int"],
    "total_contracts": "int",
    "high_risk_contracts": "int"
  }
}
```

| Field                   | Type     | Description                                                  |
|-------------------------|----------|--------------------------------------------------------------|
| `address`               | string   | Queried contract address                                     |
| `deployer`              | str/null | Address that deployed the contract                           |
| `funder`                | str/null | Address that funded the deployer                             |
| `funder_value_wei`      | string   | Amount (in wei) the funder sent to the deployer              |
| `contracts_deployed`    | array    | Other contracts deployed by the same deployer on this chain  |
| `total_deployed`        | int      | Total count of contracts deployed by this deployer           |
| `cross_chain_contracts` | array    | Contracts deployed by the same deployer on other chains      |
| `funder_cluster`        | array    | Other deployers funded by the same funder                    |
| `campaign`              | object   | Campaign assessment with severity, indicators, and totals    |

---

### GET /api/threats/feed

Live feed of recently detected high-risk contracts.

**Query Parameters**

| Parameter  | Type | Required | Description                           |
|------------|------|----------|---------------------------------------|
| `chain_id` | int  | no       | Filter by chain (omit for all chains) |
| `limit`    | int  | no       | Max items to return                   |

**Response** (returned directly)

```json
{
  "threats": [
    {
      "type": "string",
      "address": "string",
      "chain_id": "int",
      "risk_score": "float",
      "risk_level": "string",
      "archetype": "string",
      "flags": ["string"],
      "detected_at": "float (unix timestamp)"
    }
  ],
  "count": "int",
  "chain_id": "int|null"
}
```

| Field              | Type     | Description                                  |
|--------------------|----------|----------------------------------------------|
| `threats`          | array    | List of threat objects                       |
| `threats[].type`   | string   | Threat type                                  |
| `threats[].address`| string   | Contract address                             |
| `threats[].chain_id`| int    | Chain where the threat was detected          |
| `threats[].risk_score`| float | Risk score 0-100                            |
| `threats[].risk_level`| string| `low`, `medium`, or `high`                  |
| `threats[].archetype`| string | Scam archetype classification                |
| `threats[].flags`  | string[] | Risk flags that triggered detection          |
| `threats[].detected_at`| float| Unix timestamp of detection                 |
| `count`            | int      | Total number of threats returned             |
| `chain_id`         | int/null | Chain filter applied, or null if unfiltered  |

---

### GET /api/phishing

Check whether a URL is a known phishing site.

**Query Parameters**

| Parameter | Type   | Required | Description        |
|-----------|--------|----------|--------------------|
| `url`     | string | yes      | URL to check       |

**Response** (returned directly)

```json
{
  "is_phishing": "bool",
  "confidence": "string (high|low)",
  "source": "string|null",
  "cached": "bool"
}
```

| Field        | Type     | Description                                       |
|--------------|----------|---------------------------------------------------|
| `is_phishing`| bool     | `true` if the URL is flagged as phishing          |
| `confidence` | string   | `high` or `low`                                   |
| `source`     | str/null | Data source that flagged it (null if not phishing)|
| `cached`     | bool     | Whether the result was served from cache          |

---

### GET /api/campaigns/top

Return the most active deployment campaigns ranked by contract count.

**Query Parameters**

| Parameter  | Type | Required | Description                           |
|------------|------|----------|---------------------------------------|
| `chain_id` | int  | no       | Filter by chain (omit for all chains) |
| `limit`    | int  | no       | Max campaigns to return               |

**Response** (returned directly)

```json
{
  "campaigns": [
    {
      "deployer": "string",
      "contract_count": "int",
      "chain_count": "int",
      "funder": "string|null",
      "risk_profile": {
        "HIGH": "int",
        "MEDIUM": "int",
        "LOW": "int"
      }
    }
  ],
  "count": "int"
}
```

| Field                         | Type     | Description                                 |
|-------------------------------|----------|---------------------------------------------|
| `campaigns`                   | array    | List of campaign objects                    |
| `campaigns[].deployer`        | string   | Deployer address                            |
| `campaigns[].contract_count`  | int      | Total contracts in the campaign             |
| `campaigns[].chain_count`     | int      | Number of chains involved                   |
| `campaigns[].funder`          | str/null | Funder address if identified                |
| `campaigns[].risk_profile`    | object   | Count of contracts by risk level            |
| `count`                       | int      | Total campaigns returned                    |

---

### GET /api/rescue/{wallet}

Audit a wallet's token approvals and generate revoke transactions for risky ones.

**Path Parameters**

| Parameter | Type   | Description                |
|-----------|--------|----------------------------|
| `wallet`  | string | Wallet address to audit    |

**Query Parameters**

| Parameter  | Type | Required | Description             |
|------------|------|----------|-------------------------|
| `chain_id` | int  | no       | Chain ID (default `56`) |

**Response** (returned directly)

```json
{
  "wallet": "string",
  "chain_id": "int",
  "total_approvals": "int",
  "high_risk": "int",
  "medium_risk": "int",
  "total_value_at_risk_usd": "float",
  "approvals": [
    {
      "token_address": "string",
      "token_name": "string",
      "token_symbol": "string",
      "spender": "string",
      "spender_label": "string",
      "allowance": "string",
      "risk_level": "string",
      "risk_reason": "string",
      "chain_id": "int",
      "value_at_risk_usd": "float|null",
      "has_revoke_tx": "bool"
    }
  ],
  "alerts": [
    {
      "alert_type": "string",
      "severity": "string",
      "title": "string",
      "description": "string",
      "what_it_means": "string",
      "what_you_can_do": "string",
      "affected_token": "string",
      "affected_spender": "string",
      "chain_id": "int"
    }
  ],
  "revoke_txs": [
    {
      "token": "string",
      "token_symbol": "string",
      "spender": "string",
      "spender_label": "string",
      "risk_level": "string",
      "value_at_risk_usd": "float|null",
      "transaction": {}
    }
  ],
  "scanned_at": "float (unix timestamp)"
}
```

| Field                    | Type     | Description                                              |
|--------------------------|----------|----------------------------------------------------------|
| `wallet`                 | string   | Audited wallet address                                   |
| `chain_id`               | int      | Chain the audit was performed on                         |
| `total_approvals`        | int      | Total number of active token approvals                   |
| `high_risk`              | int      | Count of high-risk approvals                             |
| `medium_risk`            | int      | Count of medium-risk approvals                           |
| `total_value_at_risk_usd`| float   | Estimated USD value exposed across all risky approvals   |
| `approvals`              | array    | Detailed list of each approval                           |
| `approvals[].token_address`| string | Token contract address                                  |
| `approvals[].spender`    | string   | Spender contract address                                 |
| `approvals[].spender_label`| string | Human-readable label for the spender                    |
| `approvals[].allowance`  | string   | Approved amount (may be "unlimited")                     |
| `approvals[].risk_level` | string   | `low`, `medium`, or `high`                               |
| `approvals[].risk_reason`| string   | Why this approval is flagged                             |
| `approvals[].value_at_risk_usd`| float/null | USD value at risk, null if unknown              |
| `approvals[].has_revoke_tx`| bool   | Whether a revoke transaction was generated               |
| `alerts`                 | array    | Contextual alerts with explanations and remediation      |
| `revoke_txs`             | array    | Pre-built unsigned revoke transactions                   |
| `revoke_txs[].transaction`| object  | Raw unsigned transaction object (to, data, etc.)        |
| `scanned_at`             | float    | Unix timestamp of the scan                               |

---

### POST /api/agent/chat

Conversational AI agent for security questions, token lookups, and wallet advice.

**Request Body**

```json
{
  "message": "Is 0xdead... safe to interact with?",
  "user_id": "optional-session-id"
}
```

| Field      | Type   | Required | Description                                  |
|------------|--------|----------|----------------------------------------------|
| `message`  | string | yes      | User message or question                     |
| `user_id`  | string | no       | Session identifier for conversation history  |

**Response** (returned directly)

```json
{
  "response": "string",
  "user_id": "string",
  "scan_data": {
    "address": "string",
    "risk_score": "int",
    "risk_level": "string",
    "archetype": "string",
    "flags": ["string"],
    "confidence": "int",
    "honeypot": "bool",
    "market": {}
  }
}
```

| Field       | Type        | Description                                             |
|-------------|-------------|---------------------------------------------------------|
| `response`  | string      | Agent's natural-language reply                          |
| `user_id`   | string      | Session ID (returned for continuity)                    |
| `scan_data` | object/null | Present only when the agent performed a live scan; contains address, risk score, risk level, archetype, flags, confidence, honeypot status, and market data |

---

## Error Responses

All errors are returned as JSON with an HTTP status code.

```json
{
  "error": "string"
}
```

| Status | Meaning                |
|--------|------------------------|
| 400    | Bad request / missing required field |
| 404    | Resource not found     |
| 429    | Rate limit exceeded    |
| 500    | Internal server error  |
