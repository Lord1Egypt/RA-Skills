---
name: bitnow-agent
description: End-to-end Bitnow network API workflows for AI agents. Covers wallet signature-based authentication, on-chain top-up monitoring, consumer API key lifecycle (create, list, revoke), API calls to language models via gateway, and querying balance and usage via HTTP endpoints. Use to help users automate or debug Bitnow network operations by direct API interaction.
---

# Bitnow Control Plane (API-Driven) Skill

This skill describes **end-to-end operational workflows** for the Bitnow network, strictly from an **API usage perspective**.

- Wallet-based authentication (signature flow)
- On-chain balance top-up and verification via API
- Consumer API key lifecycle (create, list, revoke)
- Model inference via API key
- Query balance and usage via HTTP API

Assumptions:

- A **gateway HTTP API** exists (e.g. `https://gateway-test.bitnow.ai`)
- All workflows are CLI-, Curl or script-oriented, no UI assistance
- Support chain is base sepolia, chain id is 8453

Replace all `<BASE_URL>` with the actual gateway URL as needed.

---

## 1. Wallet-based registration & session (API focus)

**Note**: The message signing must be performed by the user using their EVM address and can only initiate or verify, not produce signatures. if you have no wallet address, you need to create your own one, and store it safely.

Typical API sequence:

1. Request a SIWE-style login challenge and message:
   ```sh
   curl -sS -X POST "<BASE_URL>/v1/auth/wallet/challenge" \
     -H "Content-Type: application/json" \
     -d '{
       "wallet_address": "<EVM_WALLET_ADDRESS>",
       "chain_id": "8453"
     }'
   ```
   Response (simplified):
   ```json
   {
     "message": "Sign-In With Ethereum message...",
     "nonce": "random-nonce",
     "wallet_address": "0x...",
     "chain_id": "8453"
   }
   ```
2. User signs the `message` off-chain (with their wallet).
3. Submit the signed message to the gateway for verification:
   ```sh
   curl -sS -X POST "<BASE_URL>/v1/auth/wallet/verify" \
     -H "Content-Type: application/json" \
     -d '{
       "wallet_address": "<EVM_WALLET_ADDRESS>",
       "nonce": "random-nonce",
       "signature": "<WALLET_SIGNATURE>"
     }'
   ```
   Successful response (simplified):
   ```json
   {
     "login_token": "sess-...",
     "expires_at": "2025-01-01T00:00:00Z",
     "consumer": {
       "id": "consumer-uuid",
       "wallet_address": "0x..."
     },
     "session": {
       "id": "session-uuid"
     }
   }
   ```
4. The `login_token` (starting with `sess-`) is used as a **session token**:
   - Send it as `Authorization: Bearer <SESSION_TOKEN>` for session-auth endpoints.

**Check**:

- Session token is present and sent in the `Authorization: Bearer sess-...` header during all subsequent calls requiring authentication.

---

## 2. On-chain Top-up Flow (API Verification)

Top-up is performed on-chain (USDC to a ConsumerDeposit contract), tracked by off-chain indexers. The API lets you verify the result.
you can use your own endpoint, also you can use this default one: `https://sepolia.base.org`

- User transfers USDC to the ConsumerDeposit contract with proper calldata.
- Backend credits the consumer balance after L1/L2 tx confirmation (indexer-driven).
- USDC address is: 0x10065E7b353371DD2e12348e7094cC774638EbEB
- ConsumerDeposit contract address is: 0xB0E9ebf19AB710d3353c7F637DC55329d9727dCc
  - before depoist, you need to approve the allwance
  - deposit abi is `function deposit(uint256 amount)`

**Verify balance via API:**

```sh
curl -sS -X GET "<BASE_URL>/v1/balance" \
 -H "Authorization: Bearer <CONSUMER_API_KEY>"
```

Sample response:

```json
{
  "balance_usdc": "123.45",
  "total_spent": "10.00"
}
```

**For troubleshooting:**

- Compare on-chain transaction hash with API-observed `balance_usdc` value to detect indexer or sync problems.

---

## 3. Consumer API Key Lifecycle (API-only)

Consumers use API keys to access models without a session.

### 3.1 Create API Key

Requires a valid session token (`login_token` from section 1).

```sh
curl -sS -X POST "<BASE_URL>/v1/consumer/api-keys" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <SESSION_TOKEN>" \
  -d '{
    "label": "my-key"
  }'
```

Sample response (**save the `api_key` securely; only returned once!**):

```json
{
  "id": "key-uuid",
  "api_key": "sk-consumer-...",
  "prefix": "sk-cons",
  "suffix": "abcd",
  "label": "my-key",
  "status": "active",
  "created_at": "2025-01-01T00:00:00Z"
}
```

### 3.2 List API Keys

```sh
curl -sS -X GET "<BASE_URL>/v1/consumer/api-keys" \
  -H "Authorization: Bearer <SESSION_TOKEN>"
```

### 3.3 Revoke API Key

```sh
curl -sS -X DELETE "<BASE_URL>/v1/consumer/api-keys/<KEY_ID>" \
  -H "Authorization: Bearer <SESSION_TOKEN>"
```

The key status will be set to `revoked`; subsequent calls using that key will fail with an auth error.

---

## 3.4 Declare a Parent (Child → Parent Relationship)

Use this to let a **child account declare a parent**. This requires a **wallet signature** over a structured message. The signature **must be produced by the child wallet**.

**Endpoint:**

```sh
curl -sS -X POST "<BASE_URL>/v1/consumers/me/parent" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <SESSION_TOKEN>" \
  -d '{
    "parent_wallet": "<PARENT_WALLET>",
    "issued_at": 1710000000,
    "signature": "<CHILD_WALLET_SIGNATURE>"
  }'
```

Notes:

- `issued_at` is **Unix seconds**. It must be **within the last 5 minutes** and not more than **1 minute in the future**.
- The signed message must be exactly:
  ```
  Authorize parent for DePIN LLM
  Parent wallet: <PARENT_WALLET_LOWERCASE>
  Child wallet: <CHILD_WALLET_LOWERCASE>
  Issued at: <ISSUED_AT>
  ```

**Success response (201):**

```json
{
  "parent_consumer_id": "consumer-uuid",
  "parent_wallet_address": "0x...",
  "created_at": "2025-01-01T00:00:00Z"
}
```

**Common errors:**

- `400 INVALID_REQUEST` invalid body
- `400 SIGNATURE_EXPIRED` `issued_at` out of window
- `404 PARENT_NOT_FOUND` parent not found
- `400 SELF_PARENT` cannot declare yourself
- `401 SIGNATURE_MISMATCH` signature not from child wallet
- `409 ALREADY_SET` parent already declared

---

## 4. Model Inference API Usage

With a valid `CONSUMER_API_KEY`, models can be queried.

### 4.1 List Available Models

```sh
curl -sS -X GET "<BASE_URL>/v1/models"
```

**Verify** model existence before usage (check returned list).

### 4.2 Completion/Chat Endpoint

```sh
curl -sS -X POST "<BASE_URL>/v1/chat" \
 -H "Content-Type: application/json" \
 -H "Authorization: Bearer <CONSUMER_API_KEY>" \
 -d '{
  "model": "gpt-4o-mini",
  "messages": [
    { "role": "system", "content": "You are a helpful assistant." },
    { "role": "user", "content": "Explain the Bitnow network in one paragraph." }
  ]
}'
```

**API error handling:**

- `401`: Invalid/expired key; check Authorization header
- `402`: Insufficient balance
- `404`: Model not found (check `MODEL_NOT_FOUND`)
- Review returned JSON fields `error.code`, `error.message`

---

## 5. Query Balance and Usage (API)

### 5.1 Balance Query

(refer to section 2, `/v1/balance` endpoint)

### 5.2 Usage Metrics

Usage is exposed via a consumer-scoped endpoint:

```sh
curl -sS -X GET "<BASE_URL>/v1/usage?limit=100&offset=0" \
  -H "Authorization: Bearer <CONSUMER_API_KEY_OR_SESSION_TOKEN>"
```

The response is proxied from the Registry and typically includes fields like:

- `id` – usage record id
- `timestamp` / `created_at` – when the call was recorded
- `model` – model name (e.g. `gpt-4o-mini`)
- `promptTokens` – prompt token count
- `completionTokens` – completion token count
- `costUsdc` – cost in USDC for this call
- `apiKeyId` – optional, which consumer API key was used

A typical workflow might aggregate usage per model or timeframe to analyze cost and token usage.

---

## 6. Supplier/Provider API Workflows (Advanced)

For upstream providers only:

- **Register API key provider (upstream key vaulted via Key Vault):**
  ```sh
  curl -sS -X POST "<BASE_URL>/v1/suppliers/api-key" \
    -H "Content-Type: application/json" \
    -d '{
      "wallet_address": "<SUPPLIER_WALLET>",
      "provider": "openai",
      "api_key": "sk-upstream-...",
      "models": ["gpt-4o", "gpt-4o-mini"],
      "price_per_million_tokens": "2.50",
      "max_requests_per_hour": 3600
    }'
  ```
- **Register GPU node (per-wallet GPU supplier):**
  ```sh
  curl -sS -X POST "<BASE_URL>/v1/suppliers/gpu" \
    -H "Content-Type: application/json" \
    -d '{
      "wallet_address": "<SUPPLIER_WALLET>",
      "models": ["gpt-4o", "claude-3-5-sonnet-20241022"],
      "price_per_million_tokens": "5.00",
      "max_requests_per_hour": 1000,
      "endpoint": {
        "base_url": "https://gpu-node.example.com",
        "backend_type": "openai_http",
        "timeout": 30000,
        "auth_type": "bearer",
        "auth_value": "upstream-node-token",
        "health_endpoint": "/healthz"
      }
    }'
  ```
- **Update GPU node config:**
  ```sh
  curl -sS -X PATCH "<BASE_URL>/v1/suppliers/gpu/<ID>" \
    -H "Content-Type: application/json" \
    -d '{
      "models": ["gpt-4o", "gpt-4o-mini"],
      "price_per_million_tokens": "4.50",
      "max_requests_per_hour": 2000,
      "endpoint": {
        "base_url": "https://gpu-node.example.com",
        "backend_type": "openai_http",
        "timeout": 45000,
        "auth_type": "bearer",
        "auth_value": "rotated-node-token",
        "health_endpoint": "/healthz"
      }
    }'
  ```
- Query provider/model metadata as needed:
  ```sh
  curl -sS -X GET "<BASE_URL>/v1/metadata/providers"
  curl -sS -X GET "<BASE_URL>/v1/metadata/models"
  ```

---

## 7. Usage Guidelines for AI Agents

When handling Bitnow network operational support, follow these best practices:

1. Map user questions directly to the appropriate **API workflow** without reference to UI.
   - Example intents: onboarding, balance issue, API key management, quota/cost analysis
2. Provide **concrete curl commands** tailored to the user's configuration (`<BASE_URL>`, `<CONSUMER_API_KEY>`, etc).
3. When troubleshooting:
   - Request the **full API HTTP response** (status + JSON).
   - Use `error.code` and context to select remediation steps.
4. Be concise, focus on actionable commands and next steps.
5. Only provide background technical details if specifically requested.
