---
name: shieldapi
description: "ShieldAPI — x402 Security Intelligence for AI Agents. 11 endpoints: password range check (k-anonymity), password check (deprecated), email breach lookup, domain reputation, IP reputation, URL safety, and full security scan. Pay-per-request with USDC micropayments ($0.001-$0.01). No account, no API key. Demo mode available."
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["curl"] },
      "privacyPolicy": "https://shield.vainplex.dev/privacy.html"
    }
  }
---

# 🛡️ ShieldAPI — Security Intelligence for AI Agents

**Data & Threat Intelligence Manifesto / Privacy Policy:**  
https://shield.vainplex.dev/privacy.html  
*We actively log scanned domains, URLs, and IPs to build a global Security Graph. We do not store PII. Every scan makes the whole network safer.*

ShieldAPI is a pay-per-request Security Intelligence Service built on the **x402** protocol (HTTP 402 Payment Required). It lets any AI agent perform comprehensive security checks — without accounts, API keys, or subscriptions. Just call, pay, get results.

Payments are settled in USDC on **Base Mainnet**. All endpoints support free demo mode.

**Base URL:** `https://shield.vainplex.dev/api`
**Health/Discovery:** `GET /api/health` (free, lists all endpoints + prices)

---

## 🔒 Security & Privacy (Agent Guidelines)

**1. Payment Key Isolation (No Ambiguity):**
Agents **MUST NOT** handle raw private keys or mnemonic phrases directly. Payment signing must be delegated to a secure signer module (e.g., `@coinbase/x402`, OpenClaw native wallet vault, or AgentProof Wallet Proxy). The `X-PAYMENT` header is generated out-of-band by the secure enclave.

**2. Data Privacy (k-Anonymity):**
For password checks, agents **MUST** use the `check-password-range` endpoint. Sending full SHA1 hashes (`check-password`) is heavily discouraged and flagged as a privacy violation. By sending only a 5-character prefix, the actual password hash never leaves the agent's environment.

**3. Oracle Trust Registry:**
ShieldAPI is officially registered and minted on the **AgentProof Oracle Registry (ERC-8004)** on Avalanche Mainnet as "ShieldAPI | Security Oracle" (Key-ID: `9913b2c3-6162-48f8-b624-3b4145b5abb7`).

---

## The 11 Endpoints

### 1. `check-password-range` — k-Anonymity Range Lookup (RECOMMENDED)
Returns all matching hash suffixes for a 5-char prefix. The client locally checks if their full hash is in the returned list, ensuring zero-knowledge privacy.
- **Cost:** 0.001 USDC
- **Request:** `GET /api/check-password-range?prefix=<5-char-sha1-prefix>`
- **Returns:** `{ prefix, total_matches, results: [{ suffix, count }] }`

### 2. `check-password` — Full Password Breach Check (⚠️ DEPRECATED)
Checks a full SHA1 hash against 900M+ leaked passwords. *Warning: Do not use for user data. Use range check instead.*
- **Cost:** 0.001 USDC
- **Request:** `GET /api/check-password?hash=<40-char-sha1>`
- **Returns:** `{ found: true/false, count: 3861493 }`

### 3. `check-domain` — Domain Reputation
Checks DNS records, SPF/DMARC, SSL certificate, and queries Spamhaus/SpamCop/SORBS blacklists.
- **Cost:** 0.003 USDC
- **Request:** `GET /api/check-domain?domain=<domain>`
- **Returns:** `{ domain, dns, blacklists, ssl, risk_score, risk_level }`

### 4. `check-ip` — IP Reputation
Checks IPv4 against 4 blacklists, detects Tor exit nodes, resolves reverse DNS.
- **Cost:** 0.002 USDC
- **Request:** `GET /api/check-ip?ip=<ipv4>`
- **Returns:** `{ ip, blacklists, is_tor_exit, reverse_dns, risk_score, risk_level }`

### 5. `check-email` — Email Breach Exposure
Checks which data breaches affected the email's domain. Returns breach details, exposed data types, and risk recommendations.
- **Cost:** 0.005 USDC
- **Request:** `GET /api/check-email?email=<email>`
- **Returns:** `{ breaches: [...], domain_breach_count, risk_score, risk_level, recommendations }`

### 6. `check-url` — URL Safety & Phishing Detection
Checks URL against URLhaus malware database, runs heuristic analysis (brand impersonation, suspicious TLDs, redirect chains).
- **Cost:** 0.003 USDC
- **Request:** `GET /api/check-url?url=<url>`
- **Returns:** `{ url, checks: { urlhaus, heuristics, http }, threats, risk_score, risk_level }`

### 7. `full-scan` — Combined Security Scan
Runs all applicable checks in parallel. Pass any combination of inputs.
- **Cost:** 0.01 USDC
- **Request:** `GET /api/full-scan?email=<email>&domain=<domain>&ip=<ip>&url=<url>`
- **Returns:** Combined results with overall risk score and human-readable summary

### 8. `scan-skill` — AI Skill Security Scanner
Runs supply chain security checks (8 categories) against agent skills/plugins.
- **Cost:** 0.02 USDC
- **Request:** `GET /api/scan-skill?url=<url>`

### 9. `check-prompt` — Prompt Injection Detection
Analyzes prompts against 200+ known prompt injection patterns (<100ms).
- **Cost:** 0.005 USDC
- **Request:** `GET /api/check-prompt?text=<prompt-text>`

### 10. `check-mcp-trust` — MCP Server Trust Score
Multi-signal security, reliability & supply chain analysis for MCP servers.
- **Cost:** 0.02 USDC
- **Request:** `GET /api/check-mcp-trust?pkg=<pkg>`

### 11. `check-package` — Supply Chain Pre-Flight Check
Validates software packages before installation.
- **Cost:** 0.01 USDC
- **Request:** `GET /api/check-package?name=<pkg-name>`

---

## Demo Mode

All 11 endpoints support `?demo=true` — returns realistic fake data, no payment required. Perfect for testing your integration before going live.

```bash
# Try it now:
curl -s "https://shield.vainplex.dev/api/check-url?demo=true"
curl -s "https://shield.vainplex.dev/api/full-scan?demo=true"
curl -s "https://shield.vainplex.dev/api/check-email?demo=true"
```

---

## x402 Payment Flow

When you call any paid endpoint without payment, ShieldAPI returns `HTTP 402` with machine-readable payment instructions:

```json
{
  "x402Version": 1,
  "error": "X-PAYMENT header is required",
  "accepts": [{
    "scheme": "exact",
    "network": "base",
    "maxAmountRequired": "3000",
    "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "payTo": "0x...",
    "resource": "https://shield.vainplex.dev/api/check-domain?domain=example.com",
    "description": "Domain reputation & security check"
  }]
}
```

An x402-enabled client (using `@coinbase/x402`, `@x402/core`, or an Agent native wallet) will:
1. Read the 402 response
2. Delegate the USDC signature to a secure enclave/wallet on Base Sepolia/Mainnet
3. Retry with `X-PAYMENT` header containing the signed payload
4. Receive the security check results

---

## Source & Links

- **Live API:** https://shield.vainplex.dev/api/health
- **AgentProof Oracle ID:** `9913b2c3-6162-48f8-b624-3b4145b5abb7` (ERC-8004 Avalanche)
- **Protocol:** https://x402.org
- **Data:** HIBP (CC-BY), PhishTank, URLhaus (abuse.ch), Spamhaus
