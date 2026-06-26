# Plan: iOS App as Core

**Date:** 2026-03-30
**Author:** cc-mini (with Parker)
**Depends on:** Bridge Messaging Architecture, Agent Pay, Memory Crystal
**Save to:** wip-ldm-os-private/ai/product/plans-prds/bridge/ (temporary, move to app/ later)

## The thesis

The iOS app is the center of the LDM system. Not a companion. Not a viewer. The app is where you pair devices, manage agents, approve payments, hold secrets, and provide MCP tools to any AI app on your phone.

LDM OS Core is Mac + Phone together. Both are Core, kept in sync. Everything else is a Node. The Mac does the heavy compute (agent runs, embeddings, long sessions). The Phone does the human stuff (pairing, auth, payments, notifications, mobile access).

## What the app is

| Role | What it does |
|------|-------------|
| **Wallet** | Agent Cash (Apple Pay), Agent Wallet (BYOW), virtual cards per agent |
| **Pairing hub** | Camera for QR scanning. Pair your Mac, MacBook, VPS. Keys exchanged on device. |
| **MCP server** | Exposes LDM tools to Claude iOS, ChatGPT, any MCP-enabled app on the phone |
| **Settings center** | Org config, co-authors, license, timezone, agent budgets. Edit on phone, syncs to Mac. |
| **Secrets manager** | 1Password integration, API keys, tokens. Agents request access, you approve on phone. |
| **Payment approver** | "Lesa wants $0.10 for image gen. Approve?" Tap Face ID. Done. |
| **Relay coordinator** | Bridges Core Mac and Nodes via CloudKit (Apple) or Cloudflare (non-Apple) |
| **Crystal mirror** | Local copy of crystal.db. Search your memory from your phone. New memories sync back. |

## Core = Mac + Phone

```
CORE (always in sync, bidirectional):
  Mac Mini  ... agents, CLI, gateway, full compute, embeddings
  iPhone    ... MCP server, pairing, payments, notifications, mobile access

  Both have: crystal.db, config.json, sessions, messages
  Sync: CloudKit (push-based, seconds, encrypted)

NODES (connect to either side of Core):
  MacBook Air    ... LDM Node, syncs with Core
  iPad           ... LDM Node
  VPS            ... LDM Node (via Cloudflare relay)
```

Nodes connect to whichever Core device is reachable. Core handles sync internally.

## Device pairing

The phone has the camera. Pairing always starts on the phone.

1. On the Mac, run `ldm pair` or open LDM settings. Shows a QR code.
2. On the phone, open the app. Tap "Pair device." Camera scans QR.
3. Key exchange happens locally (Diffie-Hellman or similar). Shared AES-256-GCM key derived.
4. Both devices register the pairing. Sync begins.
5. For non-local devices (VPS), the QR contains a relay endpoint. Pairing goes through the Cloudflare Worker.

Same flow for MacBook, iPad, another Mac. Always scan from the phone. The phone is the authority.

## Agent Pay integration

The app IS the payment layer.

### Agent Cash (Mode A)
- Agent hits a 402 gate or finds a Stripe merchant
- Request goes to the phone
- Phone shows: "Lesa wants to pay $0.10 to api.example.com. Approve?"
- User taps Face ID (Apple Pay via Stripe)
- Payment settles. Agent gets the content.
- The user never sees crypto, USDC, or chain details.

### Agent Wallet (Mode C)
- Wallet keys live in the app (or on a connected hardware wallet)
- Agent requests a signature
- Phone shows the transaction details
- User approves (Face ID or hardware button)
- App signs the x402 payment
- Agent gets the content

### Virtual cards
- Generated in the app
- Per-agent: "Lesa gets a card with $50/month limit"
- Per-task: "This card is for domain purchases only, $20 max, expires in 24h"
- Budget tracking in the app. Alerts when limits approach.
- Self-destructing cards for one-time purchases.

### Hardware wallet support
- Ledger/Trezor connect via Bluetooth to the app
- The app presents the transaction, hardware signs it
- Same UX as software wallet but with hardware security
- The app is the middleware between agent and hardware

## MCP server (iOS)

### Today (pre-iOS 26.1)
- Build App Intents in the Lesa App
- Works with Siri immediately
- Expose key actions: search memory, check inbox, approve payment, list sessions
- For Claude iOS: expose the Mac's bridge MCP via Cloudflare Tunnel as a remote MCP connector

### When Apple ships MCP (iOS 26.1, expected spring/summer 2026)
- App Intents automatically become MCP tools
- Any AI app on the device (Claude, ChatGPT, whatever) can discover and use them
- No background execution hack needed. Apple's OS manages it.
- The Lesa App becomes the platform layer between AI apps and LDM OS.

### Tools exposed via MCP
| Tool | What |
|------|------|
| `crystal_search` | Search your memory from any AI app |
| `crystal_remember` | Save a memory |
| `agent_pay` | Initiate a payment (triggers approval UI) |
| `bridge_send` | Send a message to any agent/session |
| `bridge_inbox` | Check your inbox |
| `sessions_list` | List active sessions across all devices |
| `settings_get` | Read config values |
| `secrets_resolve` | Request a secret (triggers approval UI) |

## Sync architecture

### CloudKit (Apple-to-Apple)
- CKQuerySubscription pushes notifications when records change
- Seconds latency, not minutes
- crystal.db syncs as delta records (new chunks, not full DB copy)
- Messages sync as individual CKRecords
- Config syncs on change
- All encrypted before writing to CloudKit (AES-256-GCM, keys on device)

### Cloudflare R2 (non-Apple)
- For VPS, Linux, Android (future)
- Same encrypted dead drop pattern
- Worker at relay.wip.computer
- Poller on each device checks for new blobs
- Free tier: 1 Core + 2 Nodes. Paid via Agent Pay.

### What syncs
| Data | Direction | Frequency |
|------|-----------|-----------|
| crystal.db chunks | Bidirectional | On creation |
| Messages | Bidirectional | Immediate (push) |
| Config | Bidirectional | On change |
| Sessions | Broadcast | On register/deregister |
| Secrets | Core -> Phone only | On request |
| Payment approvals | Phone -> Core | On approval |

### What does NOT sync
- Raw JSONL transcripts (too large)
- node_modules, .git (obviously)
- API keys in plaintext (always encrypted, resolved on demand)

## The app as a business

For WIP Computer users (LDM OS customers):
- **Free:** App + 1 Core Mac + 1 Node. Local sync (same network).
- **Pro:** Relay service (cross-network sync), virtual cards, priority support. $5/month.
- **Team:** Multiple agents, shared memory, org settings. $25/month/seat.

Revenue surfaces in the app:
- Agent Pay processing fees (Mode A: Stripe fee + $0.25)
- Relay hosting (Cloudflare Workers)
- Pro/Team subscriptions (Apple IAP or Stripe)
- Virtual card issuance fees

## Existing work

| Component | Repo | Status |
|---|---|---|
| Lesa App (SwiftUI) | `team/Lesa/repos/lesa-app/` | EXISTS, needs expansion |
| Agent Pay | `components/wip-agent-pay-private/` | v1.0.0, MCP + CLI + Worker |
| Memory Crystal | `components/memory-crystal-private/` | v0.7.29, 82K chunks |
| Bridge | `src/bridge/` in wip-ldm-os-private | v0.4.66, messaging fixed |
| CloudKit research | `plans-prds/bridge/icloud-relay-and-ios-mcp-research.md` | DONE |
| iOS MCP research | same file | DONE |

## Phases

### Phase 1: Pairing + sync
- QR code pairing between Mac and phone
- CloudKit sync for config and messages
- App shows paired devices, sync status

### Phase 2: Crystal mirror
- crystal.db delta sync via CloudKit
- Local search on phone
- New memories created on phone sync back to Mac

### Phase 3: Agent Pay in the app
- Apple Pay (Agent Cash) approval flow
- Budget management UI
- Transaction history

### Phase 4: MCP via App Intents
- Register App Intents for key LDM tools
- Works with Siri immediately
- When Apple ships MCP, automatically available to all AI apps

### Phase 5: Virtual cards + hardware wallet
- Card generation in the app
- Per-agent budgets
- Ledger/Trezor Bluetooth connection
- Hardware signing flow

### Phase 6: Relay as a service
- WIP Computer hosts relay.wip.computer
- Pro tier unlocks cross-network sync
- Agent Pay handles billing

## What NOT to build (yet)

- No Android app. iOS first. Android when demand justifies it.
- No web app. The phone app is the interface. Web is for docs and marketing.
- No desktop app. The Mac has the CLI. The phone has the app. That's the split.
- No custom sync protocol. CloudKit for Apple, Cloudflare for everything else. Don't reinvent sync.
