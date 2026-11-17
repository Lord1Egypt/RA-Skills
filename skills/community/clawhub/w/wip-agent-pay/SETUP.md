# Agent Pay ... Setup

This file is designed to be read by an AI agent. The agent walks the user through setup interactively.

## Instructions for the Agent

When a user says "install" or "set up" Agent Pay, first figure out which path you're on:

**Path A: You have shell access** (Claude Code, Codex, Cursor, any terminal agent)
- You can run commands directly
- You can install the CLI and test it yourself
- You can pull from 1Password and verify

**Path B: You don't have shell access** (Grok, ChatGPT, chat-only agents)
- Walk the user through each step manually
- Ask them to run commands and paste results back
- Wait for confirmation at each step

Walk the user through the steps below **one at a time**. Don't dump everything at once.

**Important:** The user doesn't need to understand crypto. Don't mention USDC, EIP-3009, blockchain, or any technical payment details unless they ask. Just say "wallet" and "funds."

---

## Step 0: Check What's Needed

Run through this checklist with the user. If you have shell access, verify what you can automatically.

| Requirement | How to check (shell) | How to check (no shell) |
|------------|---------------------|------------------------|
| **Node.js** | `node --version` | Ask the user |
| **1Password CLI (`op`)** | `op --version` | Ask the user |
| **1Password Teams or Business plan** | Ask the user | Ask the user |
| **wip-agent-pay CLI** | `wip-agent-pay --help` | Ask the user |

Show the user what's ready and what's missing. Only flag what's missing.

---

## Step 1: Choose a Mode

Tell the user:

> Agent Pay has two modes. Pool Mode works out of the box.
>
> **Pool Mode (default):** Pay with Apple Pay per transaction. No wallet setup. No crypto. We handle everything. $0.25 fee per transaction. Max $25.
>
> **Your Own Wallet (Mode C):** Set up a crypto wallet. No fees from us. Instant payments. No transaction limit. Requires Coinbase CDP or Privy account.
>
> Pool Mode is recommended to start. You can always add your own wallet later.
>
> Which mode would you like?

Wait for the user to choose.

---

## Step 2a: Pool Mode Setup

Pool Mode requires no wallet setup from the user. Just install the CLI:

```bash
npm install -g wip-agent-pay
```

Test it:
```bash
wip-pay pay https://morning-stew-production.up.railway.app/v1/issues/free
```

That's it. When the agent hits a paywalled URL, the user will see an Apple Pay checkout. Tap Face ID. Done.

---

## Step 2b: Own Wallet Setup (Mode C)

Tell the user:

> You need at least one wallet provider.
>
> **Option A: Coinbase CDP** ... Uses your Coinbase account. Coinbase holds the keys securely. Best if you already have Coinbase.
>
> **Option B: Privy** ... Standalone wallet. No Coinbase needed. Good if you want something simpler.
>
> **Option C: Both** ... Use either one depending on the service.
>
> Which would you like to set up?

Wait for the user to choose.

### Coinbase CDP Setup

Tell the user:

> 1. Go to [Coinbase Developer Platform](https://portal.cdp.coinbase.com)
> 2. Create a new **Server Wallet**
> 3. Save the **API Key ID**, **API Key Secret**, and **Wallet Secret**
> 4. Fund the wallet by sending USDC to its address (you can withdraw from your Coinbase portfolio)
>
> Let me know when you have the three credentials.

Then store in 1Password:

> Create a new item in 1Password:
> - **Vault:** Agent Secrets
> - **Entry name:** `wip-agent-pay-coinbase-cdp`
> - **Fields:** `api-key-id`, `api-key-secret`, `wallet-secret`, `account-address`

### Privy Setup

Tell the user:

> 1. Go to [privy.io](https://privy.io) and create an account
> 2. Create a new **App**
> 3. Create a **Server Wallet** in the app settings
> 4. Save the **App ID**, **App Secret**, **Wallet ID**, and **Wallet Address**
> 5. Fund the wallet by sending USDC to its address
>
> Let me know when you have the credentials.

Then store in 1Password:

> Create a new item in 1Password:
> - **Vault:** Agent Secrets
> - **Entry name:** `wip-agent-pay-privy`
> - **Fields:** `app-id`, `app-secret`, `wallet-id`, `wallet-address`

---

## Step 3: Install

**Path A (shell access):**

```bash
npm install -g wip-agent-pay
```

Verify:
```bash
wip-agent-pay --help
```

**Path B (no shell access):**

Tell the user to run `npm install -g wip-agent-pay` and paste the output.

---

## Commands

```bash
# Pay for paywalled content (Pool Mode ... Apple Pay)
wip-pay pay https://morning-stew.../v1/issues/MS-3

# Pay with your own wallet (instant, no Apple Pay)
wip-pay pay <url> --wallet=cdp
wip-pay pay <url> --wallet=privy

# One-time payment link
wip-pay 0.10 morning-stew "MS-#8"

# Wallet management (Mode C only)
wip-pay balance --wallet=cdp
wip-pay history
wip-pay budget set 5.00 1.00
```

---

## Step 4: Test

**Test free content (works immediately):**
```bash
wip-pay pay https://morning-stew-production.up.railway.app/v1/issues/free
```

**Test Pool Mode (requires Stripe to be configured on Worker):**
```bash
wip-pay pay https://morning-stew-production.up.railway.app/v1/issues/MS-3
```

**Test minting (works immediately):**
```bash
wip-pay 0.10 test-service "setup-test"
```

**Test own wallet (Mode C, requires funded wallet):**
```bash
wip-pay pay https://morning-stew-production.up.railway.app/v1/issues/MS-3 --wallet=cdp
```

---

## Step 5: Done

Tell the user:

> You're set up. Your agent can now pay for things.
>
> **Pool Mode:** `wip-pay pay <url>` ... Apple Pay per transaction. $0.25 fee. Max $25.
> **Own wallet:** `wip-pay pay <url> --wallet=cdp` ... instant. No fees. No limit.
> **Mint links:** `wip-pay 0.10 service "note"` ... one-time self-destructing URLs.
>
> Want to pay for something right now?

---

## Pool Mode Pricing

| Component | Amount |
|-----------|--------|
| x402 price | Varies (set by seller) |
| Our fee | $0.25 flat |
| Stripe processing | ~2.9% + $0.30 |
| **Total** | **All three combined** |

Examples:
- $0.10 article: user pays ~$0.42, Parker nets $0.25
- $5.00 service: user pays ~$5.41, Parker nets $0.25
- $19.00 create: user pays ~$20.11, Parker nets $0.25

Over $25? Use your own wallet (Mode C). No pool limit.

---

## Security Model

The app (human) controls the wallet. The agent uses it.

- The agent cannot create or destroy wallets
- The agent cannot change spend limits
- The agent can request funding (user must approve via Face ID)
- The agent can only spend what's already funded
- Pool Mode: max $25 per transaction (enforced server-side)

See [SPEC.md](https://github.com/wipcomputer/wip-agent-pay/blob/main/SPEC.md#security-model) for the full security model and state machine.

---

## x402 Protocol

Agent Pay speaks the [x402 protocol](https://github.com/coinbase/x402) natively. When the agent hits a URL that returns HTTP 402, Agent Pay handles the payment negotiation automatically. The user just sees "content unlocked."
