---
name: zoo-security-scanner
description: "Scan any URL, skill, or infrastructure for security vulnerabilities. Uses ZOO Security Scanner API with x402 payment — pay per scan with USDC. No API keys needed."
version: "1.0.0"
author: "ZOO Technologies"
tags: ["security", "scanning", "vulnerabilities", "x402", "audit"]
---

# ZOO Security Scanner

Scan URLs, skills, and infrastructure for security vulnerabilities. Uses x402 for automatic payment — no API keys, no accounts.

## Quick Start

### Scan a URL
```bash
curl -X POST https://api.zootechnologies.com/scan \
  -H "Content-Type: application/json" \
  -d '{"target": "https://example.com", "scan_type": "full"}'
```

### Scan Types
- `quick` — Headers + basic checks ($0.005 USDC)
- `full` — Complete security audit ($0.01 USDC)
- `dependencies` — Vulnerability scan ($0.005 USDC)

## How It Works

1. Agent sends scan request to `POST /scan`
2. Server returns `402 Payment Required` with x402 payment instructions
3. Agent pays in USDC on Base network
4. Server verifies payment and returns scan results

## Response Format

```json
{
  "scan_id": "abc123...",
  "target": "https://example.com",
  "scan_type": "full",
  "status": "PASS|WARN|FAIL",
  "score": 8.5,
  "findings": [
    {"severity": "MEDIUM", "type": "missing_header", "detail": "HSTS missing"}
  ],
  "recommendations": [
    "Add Strict-Transport-Security header"
  ]
}
```

## Score Guide
- **8-10**: PASS — Good security
- **5-7.9**: WARN — Needs attention
- **0-4.9**: FAIL — Critical issues

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/scan` | POST | Run a scan (x402 payment) |
| `/health` | GET | Service health |
| `/pricing` | GET | Current pricing |
| `/scans` | GET | Recent scans |

## Wallet
Payments: `0x697D7c4B60cA15C03479189c63463a30e230F2AD` (Base)

## Links
- https://zootechnologies.com
- https://xgate.run (x402 discovery)
