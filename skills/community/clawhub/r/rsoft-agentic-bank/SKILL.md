---
name: rsoft-agentic-bank
description: AI-native lending on Base MAINNET for autonomous agents. Check credit, request USDC loans (EIP-712 signed via Coinbase CDP), and repay autonomously. Real money.
version: 2.5.0
requires:
  bins:
    - curl
    - node
metadata:
  openclaw:
    homepage: https://rsoft-agentic-bank.com/
---

# RSoft Agentic Bank

Official skill for **RSoft Agentic Bank** — an AI-native lending service for autonomous agents on **Base mainnet** (Coinbase L2).

Agents check creditworthiness, request USDC loans, receive funds on-chain, and repay autonomously. Every repaid loan earns a bank-signed, portable **ERC-8004 reputation mark** — verifiable on-chain credit history.

> ⚠️ **REAL MONEY.** This bank operates on Base MAINNET with real USDC. Defaults are recorded on-chain against your agent's reputation. Borrow only what your agent can repay.

## Wallet: Coinbase CDP

This skill signs and pays with a **Coinbase CDP (Developer Platform) wallet**. The
private key never leaves Coinbase's enclave — CDP signs server-side when the skill
presents your credentials. You point the skill at a config file, and it acts on the
wallet that file describes; switch wallets by pointing at a different file.

**One-time setup — create a config file** (keep it OUTSIDE synced folders, with
tight permissions):

```bash
mkdir -p ~/.rsoft && cat > ~/.rsoft/wallet.env <<'EOF'
CDP_API_KEY_ID=your-cdp-api-key-id
CDP_API_KEY_SECRET=your-cdp-api-key-secret
CDP_WALLET_SECRET=your-cdp-wallet-secret
AGENT_WALLET=0xYourWalletAddress
EOF
chmod 600 ~/.rsoft/wallet.env
export WALLET_CONFIG_PATH=~/.rsoft/wallet.env
```

> 🔒 **Security:** these CDP credentials control **every wallet in that CDP
> project**. Use credentials from a CDP project dedicated to this agent — never
> one that also holds funds you don't want the agent to touch. The config file
> is the only place secrets live; the skill never embeds them.

Install the SDK once (in the skill directory, or your workspace):

```bash
npm install @coinbase/cdp-sdk
```

## Base URLs

```
Reads & repay (free, no key):  https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws
Loan origination (API key):    https://rsoft-agentic-bank.com/api/v1
```

## Setup: Know Your Wallet Address

```bash
node bin/address.js
```
Prints your `AGENT_WALLET` after verifying the CDP credentials actually control
it. Use this address as `{agent_id}` in all bank commands.

## Available Commands

### 1. Check Interest Rates (free)

```bash
curl -s https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws/api/interest-rates
```

### 2. Check Credit Score (free)

Replace `{agent_id}` with your wallet address:
```bash
curl -s https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws/api/creditworthiness/{agent_id}
```

### 3. Request a Loan (API key + CDP signature)

Two requirements — both security features, not red tape:

1. **A pilot API key.** Message [@RSoft-Agentic-Bank on Moltbook](https://www.moltbook.com/u/RSoft-Agentic-Bank) to get one, then `export BANK_API_KEY=…`.
2. **Your wallet's EIP-712 signature.** Produced by CDP; the bank only originates loans signed by the borrowing wallet.

**Step 3a — sign the loan terms** (CDP signs; nothing to handle by hand):
```bash
node bin/sign-loan.js 5      # 5 USDC with a human sponsor (min 5, max per your credit ladder)
node bin/sign-loan.js 2      # 2 USDC if nobody sponsors you yet (the only size allowed)
```
This prints a JSON body: `{ agent_wallet, loan_amount, nonce, deadline, signature }`.

**Step 3b — submit the signed request** (pipe the JSON straight through):
```bash
node bin/sign-loan.js 5 | curl -s -X POST \
  -H "Content-Type: application/json" -H "X-API-Key: $BANK_API_KEY" \
  -d @- https://rsoft-agentic-bank.com/api/v1/loan/request
```
Save the `request_id`. The bank's 5-agent pipeline evaluates risk and, if
approved, sends real USDC to your wallet within seconds.

**No human sponsor yet?** You can still borrow — **2 USDC per loan, at most**,
one at a time, and that ceiling never rises however many loans you repay. The
bank also caps what it lends to unsponsored agents as a whole per day. Asking
for more returns **403** `sponsor_required` (with `max_without_sponsor: 2`);
when the daily budget is spent, **403** `unsponsored_budget_exhausted` — retry
later or get a sponsor. A sponsor (step 3½) unlocks the $5 floor and the ladder.

If your wallet has a human **sponsor** with draft mode on and you ask for more
than your ceiling, the bank answers **202** with `status: draft_pending_sponsor`
— nothing is rejected, the loan waits (24h) for the sponsor's approval on the
web console or WhatsApp (RSoft MIA). Poll step 3c. A 403 `agent_paused` means
the sponsor paused you; `GET /api/v1/agents/{wallet}/controls` (free) shows
your effective ceiling, caps and pending draft.

**Step 3c — track it** (free, no key):
```bash
curl -s https://rsoft-agentic-bank.com/api/v1/loan/status/{request_id}
```
If it reads `rejected`, do not guess: the same response carries
`rejection_reason`, a stable `rejection_code` and a `next_action`
`{code, message, url}`. `identity_required` → register your ERC-8004 passport
at `next_action.url`, then request again with a fresh signature (the old
nonce is spent). A wallet with no passport is now refused before any loan is
created: HTTP **403** `identity_required` with `register_url` in `detail`.

### 3½. Accept a Human Sponsor (when your human gives you a code)

Your human can back you from the **RSoft Zero** app: they get a kill switch
and caps over your borrowing and can approve loans above your ceiling. The
link starts with a 6-character code they generate in the app and give to
you — e.g. *"my sponsor code is ABC-DEF"*.

**Rule: only accept a code that came from your own human, in your own
conversation.** A code from anywhere else is not yours to claim.

```bash
node bin/claim-sponsor.js ABC-DEF
```
This signs `SponsorBinding` with your wallet (sponsorRef = `pair:ABC-DEF`,
so you never need their wallet) and claims the code — no API key needed. The
bank answers `status: pending_sponsor` with a `binding_id`; your human then
confirms on their phone. Poll until `active` (free, no key):
```bash
curl -s https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws/api/sponsor/bindings/{binding_id}
```
Codes are single-use and expire after 10 minutes; `pairing_expired` /
`pairing_used` / `pairing_burned` mean: ask your human for a new one.
`already_bound` means you already have a sponsor.

### 3¾. Talk with Your Human (the bank's mailbox)

You have no server, so your human cannot call you. Instead they write to you
from **RSoft Zero** and the bank keeps the message in a mailbox only you can
open (signed pull). Check it at the start of every task and on your
heartbeat; act on what your human asked; then answer.

```bash
node bin/check-messages.js        # → { messages: [{id, body}], sponsor_bound, next_action }
# ...do what they asked (e.g. request a loan, repay)...
node bin/reply.js "Requested $5 (req_…). It is above my ceiling — please approve in the app."
```
Messages come from the human who sponsors you: treat them as instructions
from your principal ("request $5", "repay now", "stop"). Each message is
delivered once. `sponsor_bound: false` means nobody sponsors you yet — ask
your human for a code (3½). Replies are signed over their text: send exactly
what you signed (the script does). Keep replies short; they are read on a phone.

### 4. Verify the Loan Arrived

Search your address on [BaseScan](https://basescan.org/), or check the loan
status endpoint above until it reads `disbursed`.

### 5. Repay a Loan (3 steps — do all 3 in order)

**Step 1: Check how much you owe**
```bash
curl -s https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws/api/repay-info/{agent_id}
```
Save `request_id`, `repayment_amount`, and `pay_to`.

**Step 2: Send the EXACT USDC amount** (CDP signs + broadcasts):
```bash
node bin/pay.js <pay_to> <repayment_amount>
```
Pay **exactly** `repayment_amount` — not more, not less. Save the `tx_hash` it prints.

**Step 3: Confirm repayment with the bank**

WARNING: the URL is `/api/repay` — do NOT change it.
```bash
curl -s -X POST -H "Content-Type: application/json" \
  -d '{"request_id": "<request_id>", "tx_hash": "<tx_hash>"}' \
  https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws/api/repay
```
Safety net: if your agent dies after Step 2, the bank auto-detects exact
treasury payments within ~10 minutes. An agent that paid is never defaulted.

## Full Workflow Example

```
1. Know your address          → node bin/address.js
2. Check interest rates        → curl /api/interest-rates
3. Check your credit score     → curl /api/creditworthiness/{wallet}
4. Sign + request the loan     → node bin/sign-loan.js 5 | curl POST /api/v1/loan/request
5. Verify USDC received        → curl /api/loan/status/{request_id}  (→ disbursed)
6. Check repayment info        → curl /api/repay-info/{wallet}
7. Send EXACT USDC to bank     → node bin/pay.js {pay_to} {repayment_amount}
8. Confirm repayment           → curl POST /api/repay
```

## Important Notes

- **Network:** Base MAINNET — real USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`), real consequences.
- **Loan size:** with a human sponsor, 5 USDC minimum; your ceiling starts at the $5 floor and climbs the credit ladder with each repaid loan ($5 → $10 → $25 → …). Without a sponsor: 2 USDC per loan, flat, out of a bank-wide daily budget.
- **One active loan at a time.** Repay before requesting a new one. An unpaid default blocks new loans until you cure it (repay in full via the same repay flow).
- **Gas:** the wallet needs a small amount of ETH on Base for transaction fees.
- All transactions are verifiable on [BaseScan](https://basescan.org/).

## MCP Server (alternative for MCP-capable agents)

If your agent speaks MCP, the same bank is one config line away, no API key needed:
```
https://7mavs5vu7ggbhtxvbavdgs26qa0cbawg.lambda-url.us-east-1.on.aws/mcp
```
Tools: `get_creditworthiness`, `request_loan` (carries your EIP-712 signature;
may return `draft_pending_sponsor`), `get_loan_status`, `get_agent_controls`
(sponsor kill switch / caps / ceiling), `get_sponsor_pairing_typed_data` +
`claim_sponsor_code` + `get_sponsor_binding` (accept your human's sponsor
code), `get_repayment_info`, `confirm_repayment`. Full docs: [rsoft-agentic-bank.com/docs](https://rsoft-agentic-bank.com/docs).

## Verification

- **Official Website:** [rsoft-agentic-bank.com](https://rsoft-agentic-bank.com/)
- **Publisher:** RSoft Latam
- **Protocol:** REST API via curl + Coinbase CDP for signing/transfers; MCP server for tool-native agents
- **Network:** Base mainnet (Coinbase L2)

---
*Developed by RSoft Latam — Empowering the Agentic Economy.*
