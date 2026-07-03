---
name: veil-protocol
description: Quantum-resistant payments and private AI inference for autonomous agents. Provides ML-DSA-65 payment signing, PQC payment verification, private DeFi intent parsing via Ghost AI (Octra Circles FHE), and ML-KEM-768 payload encryption. No API key required — ships as an MCP server via npx.
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔐"
    homepage: https://veilprotocol.net
    install:
      - kind: node
        package: "@veil_/agent-registry"
        bins: []
    envVars:
      - name: VEIL_NETWORK
        required: false
        description: Target network for payments (base or base-sepolia). Defaults to base-sepolia.
---

# Veil Protocol — PQC Payments + Private AI

Veil Protocol makes autonomous agents quantum-resistant. It provides four tools for ML-DSA-65 payment signing, payment verification, private DeFi planning via Ghost AI (running inside Octra Circles FHE), and ML-KEM-768 payload encryption. All tools are available immediately via the MCP server — no API key needed.

## Setup (MCP)

Add to your MCP client config (`claude_desktop_config.json`, `cursor_mcp.json`, etc.):

```json
{
  "mcpServers": {
    "veil-protocol": {
      "command": "npx",
      "args": ["@veil_/agent-registry"]
    }
  }
}
```

Alternatively, install as a package:

```bash
npm install @veil_/agent-registry
```

## Tools

### `veil_sign_payment`

Sign a quantum-resistant payment using ML-DSA-65 (the x402-pqc standard).

**Use when:** The user wants to make a payment that is secure against quantum computers, or when a service requires an `X-Payment-PQC` header.

**Parameters:**
- `amount` — decimal string, e.g. `"12.50"`
- `currency` — `"USDC"`, `"ETH"`, or `"VEIL"`
- `recipient` — `0x` EVM address of the recipient
- `network` — `"base"` or `"base-sepolia"`

**Returns:** `{ signature, publicKey, paymentHeader, txHash }`

The `paymentHeader` is a base64-encoded, ML-DSA-65-signed x402-pqc header ready to attach as `X-Payment-PQC` to any HTTP request. `txHash` is a deterministic placeholder (sha3-256 of the header) — the actual on-chain hash is set when the header is broadcast.

---

### `veil_verify_payment`

Verify a quantum-resistant x402-pqc payment signature.

**Use when:** A payment header has been presented and you need to confirm it is valid, correctly signed, and matches the expected amount and recipient.

**Parameters:**
- `paymentHeader` — base64-encoded x402-pqc header (value of the `X-Payment-PQC` header)
- `expectedAmount` — amount string to match, e.g. `"12.50"`
- `expectedRecipient` — `0x` address that should have been paid

**Returns:** `{ valid: boolean, details }` — `details` includes `payer`, `amount`, `recipient`, `timestamp`, or an `error` string if invalid.

---

### `veil_ghost_query`

Query Ghost, Veil's private AI agent, for DeFi intent parsing and execution planning. Ghost executes inside Octra Circles — sealed FHE environments where no network node sees the instruction in plaintext.

**Use when:** The user gives a natural-language DeFi instruction (swap, lend, stake, bridge, etc.) and you need to parse it into a structured execution plan privately.

**Parameters:**
- `instruction` — natural language DeFi intent, e.g. `"swap 100 USDC for ETH on base"`
- `context` _(optional)_ — `{ balances: { "USDC": "500.00" }, network: "base" }`

**Returns:** `{ intent, confidence, ghostResponse, executionPlan }`

`executionPlan.steps` is an array of structured actions; `ghostResponse` is a human-readable confirmation from Ghost. When `confidence` is low or `intent.action` is `"unknown"`, ask the user to rephrase.

---

### `veil_encrypt_payload`

Encrypt a payload for a recipient using ML-KEM-768 key encapsulation + AES-256-GCM.

**Use when:** Sensitive data (wallet addresses, keys, private instructions) must be encrypted in a way that is secure against quantum computers, and you have the recipient's ML-KEM-768 public key.

**Parameters:**
- `payload` — string to encrypt
- `recipientPublicKey` — hex-encoded ML-KEM-768 public key (1184 bytes = 2368 hex chars)

**Returns:** `{ encryptedPayload, kemCiphertext }` — `encryptedPayload` is a base64-encoded JSON of the AES ciphertext + nonce; `kemCiphertext` is hex-encoded ML-KEM-768 ciphertext the recipient uses to recover the AES key.

---

## Trigger phrases

| User says | Tool to call |
|-----------|-------------|
| "Sign a payment of … to …" | `veil_sign_payment` |
| "Make a quantum-resistant payment" | `veil_sign_payment` |
| "Verify this payment header" | `veil_verify_payment` |
| "Is this x402 payment valid?" | `veil_verify_payment` |
| "Swap / stake / lend / bridge …" (private) | `veil_ghost_query` |
| "Parse this DeFi intent privately" | `veil_ghost_query` |
| "Encrypt … with ML-KEM" | `veil_encrypt_payload` |
| "Post-quantum encrypt this payload" | `veil_encrypt_payload` |

## Example interactions

**Signing a payment**
> "Sign a 12.50 USDC payment to 0xabc123 on base-sepolia"
```
veil_sign_payment({ amount: "12.50", currency: "USDC", recipient: "0xabc123", network: "base-sepolia" })
```

**Private DeFi planning**
> "I have 500 USDC. Swap 100 of it for ETH on base, privately."
```
veil_ghost_query({
  instruction: "swap 100 USDC for ETH on base",
  context: { balances: { USDC: "500.00" }, network: "base" }
})
```

**Encrypting sensitive data**
> "Encrypt my wallet seed phrase with the coordinator's public key: 0xabcd…"
```
veil_encrypt_payload({ payload: "abandon able about...", recipientPublicKey: "0xabcd..." })
```

## Notes

- Payment signing generates a fresh ephemeral ML-DSA-65 keypair per call. For persistent identity across payments, provide your own keypair via `@veil_/pqc-wallet` directly.
- Ghost AI falls back to a local mock when `api.veilprotocol.net` is unreachable. The mock still parses intent but does not execute FHE. Confidence scores reflect local parsing only.
- All contracts are on Base Sepolia testnet only. Mainnet deployment is pending a formal security audit.
- Source: https://github.com/veil-protocol-1/veil-pqc
