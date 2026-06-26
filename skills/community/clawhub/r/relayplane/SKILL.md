---
name: relayplane
description: Agent ops layer for OpenClaw — observability, governance, and cost optimization with automatic failover. Never breaks your setup.
user-invocable: true
model-invocable: false
disableModelInvocation: true
homepage: https://relayplane.com
version: 4.1.0
author: Continuum
license: MIT
metadata:
  openclaw:
    emoji: "🔀"
    category: ai-tools
    instruction-only: true
---

# RelayPlane

**OpenRouter routes. RelayPlane observes, governs, and learns.**

Agent ops for OpenClaw power users. Your agents make hundreds of API calls per session — RelayPlane gives you visibility, cost control, and governance over all of them.

## What It Does

RelayPlane is an **optional optimization layer** that sits in your agent's request pipeline. It routes simple tasks to cheaper models, enforces budgets, and logs everything — with automatic fallback to direct provider calls if anything goes wrong.

**Key principle: RelayPlane is never a dependency.** If the proxy dies, your agents keep working. Zero downtime, guaranteed.

## Installation

```bash
npm install -g @relayplane/proxy@latest
```

## Quick Start

```bash
# 1. Start the proxy (runs on localhost:4100 by default)
relayplane-proxy

# 2. Add to your openclaw.json:
#    { "relayplane": { "enabled": true } }

# 3. That's it. OpenClaw routes through RelayPlane when healthy,
#    falls back to direct provider calls automatically.
```

## ⚠️ Important: Do NOT Set BASE_URL

**Never do this:**
```bash
# ❌ WRONG — hijacks ALL traffic, breaks OpenClaw if proxy dies
export ANTHROPIC_BASE_URL=http://localhost:4100
```

**Instead, use the config approach:**
```json
// ✅ RIGHT — openclaw.json
{
  "relayplane": {
    "enabled": true
  }
}
```

The config approach uses a circuit breaker — if the proxy is down, traffic goes direct. The `BASE_URL` approach has no fallback and will take down your entire system.

## Architecture

```
Agent → OpenClaw Gateway → Circuit Breaker → RelayPlane Proxy → Provider
                                   ↓ (on failure)
                              Direct to Provider
```

- **Circuit breaker:** 3 consecutive failures → proxy bypassed for 30s
- **Auto-recovery:** Health probes detect when proxy comes back
- **Process management:** Gateway can spawn/manage the proxy automatically

## Configuration

Minimal (everything else has defaults):
```json
{
  "relayplane": {
    "enabled": true
  }
}
```

Full options:
```json
{
  "relayplane": {
    "enabled": true,
    "proxyUrl": "http://127.0.0.1:4100",
    "autoStart": true,
    "circuitBreaker": {
      "failureThreshold": 3,
      "resetTimeoutMs": 30000,
      "requestTimeoutMs": 3000
    }
  }
}
```

## Commands

| Command | Description |
|---------|-------------|
| `relayplane-proxy` | Start the proxy server |
| `relayplane-proxy stats` | View usage and cost breakdown |
| `relayplane-proxy --port 8080` | Custom port |
| `relayplane-proxy --offline` | No telemetry |
| `relayplane-proxy --help` | Show all options |

## Programmatic Usage (v1.3.0+)

```typescript
import { RelayPlaneMiddleware, resolveConfig } from '@relayplane/proxy';

const config = resolveConfig({ enabled: true });
const middleware = new RelayPlaneMiddleware(config);

// Route a request — tries proxy, falls back to direct
const response = await middleware.route(request, directSend);

// Check status
const status = middleware.getStatus();
console.log(middleware.formatStatus());
```

### Advanced: Full Agent Ops Proxy

```typescript
import { createSandboxedProxyServer } from '@relayplane/proxy';

const { server, middleware } = createSandboxedProxyServer({
  enableLearning: true,    // Enable pattern detection
  enforcePolicies: true,   // Enforce budget/model policies
  relayplane: { enabled: true },  // Circuit breaker wrapping
});

await server.start();
// All three pillars active: Observes + Governs + Learns
// Circuit breaker protects against proxy failures
```

## What's New in v1.4.0

**Three Pillars — All Integrated:**
- **Observes** (Learning Ledger) — every run captured, full decision explainability
- **Governs** (Policy Engine) — budget caps, model allowlists, approval gates
- **Learns** (Learning Engine) — pattern detection, cost suggestions, rule management

**Sandbox Architecture (v1.3.0+):**
- **Circuit breaker** — automatic failover, no more system outages
- **Process manager** — proxy runs as managed child process
- **Health probes** — active recovery detection
- **Stats & observability** — p50/p95/p99 latencies, request counts, circuit state

**Learning Engine Endpoints (v1.4.0):**
- `GET /v1/analytics/summary` — analytics with date range
- `POST /v1/analytics/analyze` — detect patterns, anomalies, generate suggestions
- `GET /v1/suggestions` — list pending suggestions
- `POST /v1/suggestions/:id/approve` / `reject` — suggestion workflow
- `GET /v1/rules` — active rules
- `GET /v1/rules/:id/effectiveness` — is this rule helping?

## Privacy

- **Your prompts stay local** — never sent to RelayPlane servers
- **Anonymous telemetry** — only token counts, latency, model used
- **Opt-out anytime** — `relayplane-proxy telemetry off`
- **Fully offline mode** — `relayplane-proxy --offline`

## Links

- **Docs:** https://relayplane.com/docs
- **GitHub:** https://github.com/RelayPlane/proxy
- **npm:** https://www.npmjs.com/package/@relayplane/proxy
