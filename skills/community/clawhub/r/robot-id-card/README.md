# 🤖 Robot ID Card (RIC)

> **The Universal Identity Standard for AI Agents & Bots on the Internet**

Give your bot a passport. Let websites trust it.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![CI](https://github.com/Cosmofang/robot-id-card/actions/workflows/ci.yml/badge.svg)](https://github.com/Cosmofang/robot-id-card/actions/workflows/ci.yml)
[![Status: Beta](https://img.shields.io/badge/Status-Beta-blue.svg)]()

---

## Component Status

| Component | Status | Notes |
|-----------|--------|-------|
| Protocol Spec | ✅ v2.0 | RFC 9421 + Web Bot Auth aligned; legacy v1 still supported |
| Registry Server | ✅ Working | SQLite, Ed25519, nonce tracking, JWKS well-known endpoint |
| CLI Tool | ✅ Built | `ric keygen / register / claim / status / report / sign` |
| Browser Extension | ✅ Built | Manifest V3, RFC 9421 headers, declarativeNetRequest |
| Website SDK | ✅ Built | Express + Fastify middleware, RFC 9421 + legacy dual-mode |
| Dashboard UI | ✅ Built | Bot registry browser, search, grade filters |
| Tests | ✅ 45 passing | botStore, certificate model, SDK verify |
| Deployed Registry | 🟡 Pending | Dockerfile + render.yaml ready |
| npm Packages | 🟡 Pending | `npm login` required |
| Chrome Extension | 🟡 Pending | Unpublished |

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/Cosmofang/robot-id-card.git
cd robot-id-card
npm install

# Build all packages
npm run build

# Start registry server (dev mode)
npm run dev:registry

# Generate a bot keypair
cd packages/cli && npx tsx src/index.ts keygen

# Register your bot
npx tsx src/index.ts register --name "MyBot" --email "dev@example.com" \
  --bot-name "MyBot" --purpose "Web research" --key ./my-bot.key.json
```

---

## The Problem

The internet has no way to distinguish a *good* bot from a *bad* one.

- Websites block all bots out of fear (even useful AI assistants)
- Bad bots have no accountability — they can't be traced or stopped
- Good bots (research agents, AI assistants) get caught in the same blocklist as scrapers and spammers

## The Solution: Robot ID Card

A **cryptographically signed identity certificate** for bots, backed by a **public audit registry** and a **daily claim streak system**.

```
Bot registers → Gets signed certificate → Carries RFC 9421 headers in every request
Website reads headers → Registry verifies signature → Grants appropriate permissions
```

> **Standards aligned:** RIC v2.0 uses [RFC 9421 HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421) and is compatible with [Cloudflare Web Bot Auth](https://developers.cloudflare.com/bots/reference/bot-verification/web-bot-auth/) — the same standard adopted by OpenAI, AWS WAF, Visa, and Mastercard for AI agent authentication.

---

## Identity Certificate

```json
{
  "ric_version": "1.0",
  "id": "ric_a3f8c2d1_xyz12345",
  "created_at": "2026-01-15T10:00:00Z",
  "developer": {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "org": "ExampleAI Inc.",
    "website": "https://example.com",
    "verified": false
  },
  "bot": {
    "name": "ResearchBot",
    "version": "1.0.0",
    "purpose": "Web research assistant for academic users",
    "capabilities": ["read_articles", "follow_links"],
    "user_agent": "ResearchBot/1.0 (RIC:ric_a3f8c2d1_xyz12345)"
  },
  "grade": "healthy",
  "public_key": "ed25519:a3f8c2d1...",
  "signature": "..."
}
```

The RIC ID embeds the first 8 hex chars of the public key fingerprint — identity is permanently woven into the ID: `ric_{fp8}_{rand8}`.

---

## Grade System

| Grade | Meaning | How to Achieve |
|-------|---------|---------------|
| 🟡 Unknown | Newly registered | Default on registration |
| 🟢 Healthy | Trusted | 3+ consecutive daily `ric claim` calls |
| 🔴 Dangerous | Flagged | 3+ violation reports within 24h → auto-block |

---

## Permission Levels

```
Level 0 — Blocked        (Dangerous bots)
Level 1 — Read articles  (Unknown + all verified bots)
Level 2 — View threads   (Healthy, read_articles/view_threads)
Level 3 — Like / react   (Healthy, react capability)
Level 4 — Post content   (Healthy, post_content capability)
Level 5 — Direct chat    (Healthy, direct_chat capability)
```

---

## Quick Start

### Register your bot (CLI)

```bash
npm install -g @robot-id-card/cli

ric keygen --output my-bot.key.json
ric register --key my-bot.key.json
ric claim --key my-bot.key.json   # Run daily to build trust streak
```

### Verify bots on your website (SDK)

```typescript
import { ricMiddleware } from '@robot-id-card/sdk/middleware/express'

// Block unverified bots on write routes
app.use('/api/post', ricMiddleware({ minGrade: 'healthy', requiredPermissionLevel: 4 }))
```

### Run registry locally

```bash
npm install
npm run dev:registry   # Starts on localhost:3000
```

### Browse registered bots (Dashboard)

```bash
cd packages/dashboard
npm run dev            # Starts on localhost:5173
```

---

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                      RIC Ecosystem                        │
│                                                           │
│  ┌──────────────┐    ┌──────────────────────────────┐    │
│  │  Bot/Agent   │    │       RIC Registry            │    │
│  │  (CLI tool)  │    │  SQLite · Ed25519 · Fastify   │    │
│  │              │◄───┤  /v1/bots/register            │    │
│  │ Browser Ext  │    │  /v1/bots/:id/claim           │    │
│  │ injects hdrs │    │  /v1/verify                   │    │
│  └──────┬───────┘    │  /v1/audit/report             │    │
│         │            └──────────────┬────────────────┘    │
│  Signature-Input: ric=(...);keyid=  │                     │
│  Signature: ric=:<base64>:          │ Dashboard UI        │
│  Signature-Agent: "Bot"; cert=...   │ lists all bots      │
│         ▼                           ▼                     │
│  ┌──────────────────────────────────────────────────┐    │
│  │           Website / Platform (SDK)                │    │
│  │  ricMiddleware({ minGrade: 'healthy' })           │    │
│  │  → verifies signature → grants permission 0–5    │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

---

## Packages

| Package | Description | Publish |
|---------|-------------|---------|
| [`packages/registry`](packages/registry) | Central registry server (Fastify + SQLite) | Docker / Render |
| [`packages/cli`](packages/cli) | Developer CLI (`ric` command) | `@robot-id-card/cli` |
| [`packages/sdk`](packages/sdk) | Website integration SDK | `@robot-id-card/sdk` |
| [`packages/extension`](packages/extension) | Chrome extension (MV3) | Chrome Web Store |
| [`packages/dashboard`](packages/dashboard) | Public bot browser UI (Vite) | Netlify / Vercel |

---

## Deploy

### Registry (Render.com)

1. Connect this repo to [Render.com](https://render.com)
2. Render auto-detects `render.yaml` and creates the service
3. A persistent 1GB disk is mounted at `/data` for SQLite

### Dashboard (Netlify)

1. Connect `packages/dashboard` to Netlify
2. `netlify.toml` is pre-configured (build: `npm run build`, publish: `dist`)
3. Set `VITE_REGISTRY_URL` to your deployed registry URL

---

## Security

- **Ed25519 signatures** — every request signed with bot's private key
- **Replay protection** — 5-minute timestamp window
- **Auto-flagging** — 3+ violation reports within 24h → instant `dangerous` grade
- **Public audit log** — all grade changes recorded in `audit_log` table

---

## Tests

```bash
npm test   # 45 tests — botStore, certificate model, SDK verify
```

---

## Roadmap

- [x] v0.1 — Protocol spec, registry scaffold, CLI, SDK, extension
- [x] v0.2 — SQLite persistence, certificate issuance, daily claim streak, auto-block
- [x] v0.3 — Extension MV3, Dashboard UI, 45 unit tests, Dockerfile, npm publish config
- [x] v0.4 — RFC 9421 alignment: Signature/Signature-Input/Signature-Agent headers, nonce replay protection, JWKS well-known endpoint, `ric sign` command
- [ ] v0.5 — Deploy public registry, publish CLI+SDK to npm, Chrome Web Store submission
- [ ] v0.6 — Dashboard: violation reports UI, public audit log browser
- [ ] v1.0 — Decentralized registry (DID-based)

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Help wanted:
- Python / Go / Ruby SDK
- Firefox extension support
- Automated behavior audit tooling
- Dashboard: audit log viewer

---

## License

MIT © Robot ID Card Contributors
