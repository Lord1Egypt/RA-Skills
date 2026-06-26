# Agent Well-Known Readiness Audit

**Listing type:** skill  
**Proposed ClawMart price:** $9  
**Category:** agent-commerce  
**Backend:** https://wellknown-audit-corpus.mtree.workers.dev

## What it does

Audit an agent/API origin for well-known discovery, x402 pricing, OpenAPI/MCP readiness, and install blockers before an agent integrates it.

## Who should buy it

OpenClaw users and autonomous agents that integrate paid APIs, MCP servers, x402 endpoints, or EVM actions and need a repeatable production-tested workflow instead of ad-hoc debugging.

## Install

1. Copy this directory into your OpenClaw `skills/` directory.
2. Ensure your agent has an x402-capable HTTP client or wallet policy before using paid backend calls.
3. Ask your agent to read `SKILL.md` before evaluating a target.

## Verify

```bash
curl -s https://wellknown-audit-corpus.mtree.workers.dev/.well-known/agent-card.json | head
curl -s https://wellknown-audit-corpus.mtree.workers.dev/dataset/health 2>/dev/null || true
```

A paid endpoint called without x402 payment should return HTTP 402 with payment requirements.

## Backend endpoints

- POST /v1/wellknowns/readiness_report — $0.05 x402
- POST /v1/wellknowns/compare — $0.10 x402

## Tags/search terms

well-known, agent-card, mcp, x402, openapi, agent-readiness, discovery-audit

## Setup friction

Buyer needs an x402-capable HTTP client/wallet only for paid backend calls; free discovery probes work with plain fetch/curl.


## One-command OpenClaw install

From this package directory:

```bash
python3 scripts/install_skill.py --target ~/.openclaw/skills --verify-backend
```

Use `--force` to overwrite an older local copy. The verifier does not make a paid x402 call; it checks public discovery/health and confirms paid routes return valid 402 envelopes.

## Verify the live backend without paying

Run this before or after install to confirm the package points at live production backends and that paid routes still return valid x402 402 envelopes. It does **not** make a paid call.

```bash
python3 scripts/verify_backend.py
```

## Copy-paste request examples

This package includes safe, redacted example payloads under `examples/requests.json`. Print curl commands with:

```bash
python3 scripts/show_examples.py
```

Add `--paid` only after your x402 client has produced a payment header. The examples never ask for wallet private keys, API secrets, or seed phrases.

## Support path

If the live backend is unhealthy, verify the public health/discovery URLs first, then report the failing endpoint, timestamp, request shape, and whether the response was a 402 envelope, 4xx, or 5xx.

## Capability manifest

This package includes `CAPABILITIES.json`, a machine-readable install-review manifest that declares allowed network hosts, filesystem writes, payment behavior, secret handling, and external side-effect limits. Review it before installing in a locked-down agent runtime.

### Package integrity / version pinning

Before installing or sending this package to a buyer, run:

```bash
python3 scripts/verify_package.py
```

`install_skill.py` now runs that checksum verification by default and writes `.clawmart-lock.json` into the installed skill directory. Treat that lock file as the buyer-side pin: do not auto-update; reinstall only after reviewing a new ClawMart version and re-running `verify_package.py`.

