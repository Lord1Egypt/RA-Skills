---
name: safetok-bridge
description: "Connect safeTok Nostr DMs to your OpenClaw agent. Use OpenClaw with Claude OAuth — no Anthropic API key needed. Communicate via safeTok NIP-44 encrypted DMs from your phone."
metadata:
  openclaw:
    emoji: "🔐"
---

# safeTok ↔ OpenClaw Bridge

> **Want to use OpenClaw with Claude OAuth (no API key) and talk to your agent from your phone?**
> This bridge enables two things:
>
> 1. Use OpenClaw with Claude OAuth — no Anthropic API key needed.
> 2. Communicate with your OpenClaw agent via Nostr — specifically safeTok NIP-44 DMs.

![safeTok DMs appearing in OpenClaw Control UI](https://raw.githubusercontent.com/ductapecode/openclaw/feat/safetok-bridge-example/examples/safetok-bridge/docs/preview.png)

A bidirectional DM bridge connecting [safeTok](https://safetok.me) to OpenClaw via the Gateway WebSocket API. Incoming safeTok DMs are routed to a dedicated OpenClaw session; the assistant's reply is encrypted and published back to the Nostr relays — end-to-end encrypted, decentralized, no middleman.

## Setup

See [README.md](README.md) for full setup instructions.

### Quick start

```bash
export OPENCLAW_TOKEN="your-gateway-token"
export SAFETOK_PRIVATE_KEY="your-hex-priv-key"
npm install @noble/curves
node bridge.mjs
```

## Files

| File         | Purpose                                              |
| ------------ | ---------------------------------------------------- |
| `bridge.mjs` | Main bridge process                                  |
| `nip44.mjs`  | safeTok NIP-44 crypto primitives (encrypt/decrypt)   |

## Requirements

- Node.js ≥ 22
- Running OpenClaw gateway
- [safeTok](https://safetok.me) installed on your phone
