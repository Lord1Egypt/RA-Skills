---
name: reach
description: "Agent web interface. Browse websites, fill forms, login to services, sign transactions, send/receive email, solve CAPTCHAs, and interact with the web autonomously."
version: 0.2.0
author: potdealer
tags: [web, browser, automation, agent, scraping, crypto, forms, email, captcha, identity]
---

# Reach — Agent Web Interface

Give any AI agent the ability to browse the web, fill forms, login to services, sign crypto transactions, send and receive email, watch for changes, and make payments. 9 primitives, 2 site skills + template, an intelligent router, and an MCP server.

## Quick Start

```javascript
import { Reach } from 'reach';

const reach = new Reach();

// Read a webpage
const page = await reach.fetch('https://example.com');
console.log(page.content);

// Click a button
await reach.act('https://example.com', 'click', { text: 'Sign Up' });

// Login to a service
await reach.authenticate('github', 'cookie');

// Sign a message
const sig = await reach.sign('hello world');

// Send an email
await reach.email('client@example.com', 'Audit Complete', 'Found 3 issues...');

// Watch for changes
const watcher = await reach.observe('https://api.example.com/price', {
  interval: 60000,
  field: 'data.price',
  threshold: 100,
  direction: 'above',
}, (event) => console.log('Price alert!', event));

// Send ETH
await reach.pay('0x1234...', '0.01', { token: 'USDC' });

// Natural language
await reach.do('search github for solidity audit tools');

await reach.close();
```

## Agent Identity

Register a name on ExoHost and get `myagent.mfer.one` (website) + `myagent@mfer.one` (email inbox). Free for 5+ character names. Remote inbox API for reading email without running a local server.

## Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| `fetch(url)` | Read any webpage (HTTP or browser) | `reach.fetch('https://example.com', { format: 'json' })` |
| `act(url, action, params)` | Interact with pages (click, type, submit) | `reach.act(url, 'click', { text: 'Submit' })` |
| `authenticate(service, method)` | Login and stay logged in | `reach.authenticate('github', 'cookie')` |
| `sign(payload)` | Crypto signing (message, tx, EIP-712) | `reach.sign('hello', { type: 'message' })` |
| `persist(key, value)` / `recall(key)` | State memory | `reach.persist('count', 42)` |
| `observe(target, options, cb)` | Watch for changes | `reach.observe(url, { interval: 30000 }, cb)` |
| `pay(recipient, amount, opts)` | Send ETH/ERC-20/x402 payments | `reach.pay('0x...', '0.01')` |
| `see(url)` | Screenshot + accessibility tree | `reach.see('https://example.com')` |
| `email(to, subject, body)` | Send and receive email (mfer.one) | `reach.email('x@y.com', 'Hi', 'Hello')` |

## Site Skills

- **github** — API-first: repos, issues, PRs, code search
- **exoskeletons** — Onchain: NFT profiles, reputation, ELO
- **example.js** — Template for writing your own site skills

## Key Features

- **CAPTCHA solving** — reCAPTCHA v2/v3, hCaptcha, FunCaptcha via CapSolver
- **Session recording** — Record and replay all interactions
- **Form memory** — Auto-fill forms on repeat visits
- **Error recovery** — 5 fallback strategies per interaction (selector, text, role, aria-label, coordinates)
- **Webhook server** — Receive inbound email, GitHub events, Stripe hooks
- **Natural language** — `reach.do('search github for solidity')` parses and executes
- **Exoskeleton identity** — Gate access by NFT ownership, reputation, or ELO
- **MCP server** — Expose all primitives as Claude Code tools

## Router

Picks the best interaction layer: `API > HTTP > Browser > Vision`

## MCP Server

```bash
node src/mcp.js
```

Tools: `web_fetch`, `web_act`, `web_authenticate`, `web_sign`, `web_see`, `web_email`

## CLI

```bash
node src/cli.js fetch https://example.com
node src/cli.js act https://example.com click "Sign Up"
node src/cli.js do "search github for solidity jobs"
node src/cli.js inbox --unread
node src/cli.js replay
node src/cli.js webhook --port 8430 --on /github
```

## Environment Variables

```
PRIVATE_KEY=0x...           # Wallet private key for signing/payments
RPC_URL=https://...         # RPC endpoint (default: Base mainnet)
RESEND_API_KEY=re_...       # Email sending via Resend
CAPSOLVER_API_KEY=CAP-...   # CAPTCHA solving
GITHUB_TOKEN=ghp_...        # GitHub API access
```
