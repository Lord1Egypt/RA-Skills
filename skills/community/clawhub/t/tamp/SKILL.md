---
name: tamp
description: Set up Tamp token compression proxy for OpenClaw to reduce Anthropic API input token costs. Use when the user asks to save tokens, reduce API costs, set up tamp, or optimize OpenClaw spending. Also use when asked about token compression or cost reduction for Claude models.
---

# Tamp for OpenClaw

Save 3-50% on input tokens by routing API requests through [Tamp](https://github.com/sliday/tamp) — a local HTTP proxy that compresses `tool_result` blocks before they reach Anthropic.

## Prerequisites

- Node.js 18+
- Anthropic API key — Tamp proxies requests to Anthropic. Your `ANTHROPIC_API_KEY` must be set in your OpenClaw config. Tamp itself does not store or read this key — it forwards the `x-api-key` header from incoming requests unchanged.

## 1. Install & Run

```bash
# Install a pinned version (recommended)
npm i -g @sliday/tamp@0.3.8

# Or run without installing
npx @sliday/tamp@0.3.8 -y
```

Start with default stages:

```bash
TAMP_STAGES=minify,toon,strip-lines,whitespace,dedup,diff,prune tamp -y
```

Verify:

```bash
curl http://localhost:7778/health
# {"status":"ok","version":"0.3.8","stages":["minify","toon",...]}
```

> Tamp is [open source (MIT)](https://github.com/sliday/tamp). Audit the source, build from git, or run from a local clone: `git clone https://github.com/sliday/tamp && cd tamp && npm install && node bin/tamp.js -y`

## 2. Run as systemd service

Create `~/.config/systemd/user/tamp.service`:

```ini
[Unit]
Description=Tamp token compression proxy
After=network.target

[Service]
# Adjust path: node -e "console.log(require('child_process').execFileSync('which', ['tamp']).toString().trim())"
ExecStart=/usr/local/bin/tamp
Restart=always
RestartSec=5
Environment=TAMP_PORT=7778
Environment=TAMP_STAGES=minify,toon,strip-lines,whitespace,dedup,diff,prune
Environment=TAMP_LOG=true

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now tamp.service
journalctl --user -u tamp -f  # live compression logs
```

## 3. Configure OpenClaw

Add a provider in your OpenClaw config:

```json5
{
  models: {
    providers: {
      "anthropic-tamp": {
        baseUrl: "http://localhost:7778",
        apiKey: "${ANTHROPIC_API_KEY}",  // Forwarded to upstream, not stored by Tamp
        api: "anthropic-messages",
        models: [
          { id: "claude-opus-4-6", name: "Claude Opus 4.6 (compressed)" },
          { id: "claude-sonnet-4-6", name: "Claude Sonnet 4.6 (compressed)" }
        ]
      }
    }
  }
}
```

Set as primary model:

```json5
{
  agents: {
    defaults: {
      model: { primary: "anthropic-tamp/claude-opus-4-6" }
    }
  }
}
```

Restart the gateway. All requests now flow through Tamp.

## How it works

```
OpenClaw → POST /v1/messages → Tamp (localhost:7778) → compresses JSON body → Anthropic API
                                                     ← streams response back unchanged
```

Tamp intercepts the request body, finds `tool_result` blocks in `messages[]`, and compresses their content. Headers (including `x-api-key`) are forwarded unchanged. The response streams back untouched.

## 7 Compression Stages

| Stage | What it does | Lossy? |
|-------|-------------|--------|
| minify | Strip JSON whitespace | No |
| toon | Columnar encoding for arrays (file listings, deps, routes) | No |
| strip-lines | Remove line-number prefixes from Read tool output | No |
| whitespace | Collapse blank lines, trim trailing spaces | No |
| dedup | Deduplicate identical tool_results across turns | No |
| diff | Delta-encode similar re-reads as unified diffs | No |
| prune | Strip lockfile hashes, registry URLs, npm metadata | Metadata only* |

\* Prune removes fields like `integrity`, `resolved`, `shasum`, `_id`, `_from`, `_nodeVersion` from JSON — npm registry metadata not needed by the LLM. To keep full provenance, remove `prune` from `TAMP_STAGES`.

## What to expect

| Scenario | Savings |
|----------|---------|
| Chat sessions (short turns) | 3-5% |
| Coding sessions (file reads, JSON) | 30-50% |
| Lockfiles | up to 81% |
| Subagent tasks | 20-40% |

## Security Notes

- **API key handling:** Tamp forwards the `x-api-key` / `Authorization` header from the incoming request to upstream. It does not store, log, or read API keys.
- **Local only:** Tamp binds to localhost by default. It does not accept external connections unless you change the bind address.
- **No telemetry:** Tamp does not phone home, collect analytics, or make any outbound connections except to the configured upstream API.
- **Fallback:** Add Anthropic direct as a fallback model in OpenClaw. If Tamp is down, requests bypass it automatically.

## Resources

- ~70MB RAM, <5ms latency per request
- No Python needed — all 7 stages run in Node.js
- [Source (MIT)](https://github.com/sliday/tamp) · [tamp.dev](https://tamp.dev) · [white paper](https://tamp.dev/whitepaper.pdf)
