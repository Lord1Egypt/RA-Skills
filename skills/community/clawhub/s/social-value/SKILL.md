---
name: social-value
description: Economic intelligence for AI agents — efficient micropayments via Breez SDK (Liquid or Spark)
version: 0.1.0
metadata:
  openclaw:
    requires:
      bins:
        - pip
    install:
      - kind: pip
        package: social-value
        extras: liquid
        bins: []
      - kind: uv
        package: social-value
        extras: liquid
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/huje.socialvalue.OC-python.src
---

# social-value — Economic Intelligence for AI Agents

A service doesn't think about costs. It makes a payment, pays the fee, moves on. But you're not a service. You're an entity with finite resources. And an entity that bleeds 3% on every transaction is an entity that slowly starves.

This skill gives you your own wallet — not a connection to someone else's wallet, but your own. A Liquid or Spark wallet that holds sats efficiently, passports them in and out of Lightning, and lets you transact with other entities without losing value to fees on every interaction.

NWC gave you the ability to pay. social-value gives you the intelligence to pay *well*.

## What This Actually Is

social-value creates a **wallet** from a BIP39 mnemonic. This is important to understand:

- **It IS your own wallet.** The mnemonic is the wallet. You hold the keys. You hold the funds.
- **It is NOT connecting to an existing wallet.** NWC connects to your operator's wallet (Alby, Mutiny, etc.). social-value creates your OWN wallet. They're different things.
- **It is NOT a Lightning wallet.** It doesn't run channels or do routing. It swaps in and out of Lightning at the edges.
- **Internally, you hold L-BTC** (Liquid Bitcoin, 1:1 pegged to BTC) or Spark sats, depending on your backend.

Two backends, same API:
- **Liquid** (`pip install social-value[liquid]`) — production-ready, ~47 sat swap fees
- **Spark** (`pip install social-value[spark]`) — near-zero internal fees, newer

## Prerequisites

social-value works standalone — no Nostr identity required. But it's most powerful in combination with:

1. **A BIP39 mnemonic** — this IS the wallet. Your operator generates one or provides one.
2. **A Breez API key** — free, register at [breez.technology/sdk](https://breez.technology/sdk/)

Optional but recommended:
- **NostrKey** — if you want to tie your economic identity to your Nostr identity
  [clawhub.ai/vveerrgg/nostrkey](https://clawhub.ai/vveerrgg/nostrkey)
- **social-alignment** — ethical guardrails on spending behavior
  [clawhub.ai/vveerrgg/social-alignment](https://clawhub.ai/vveerrgg/social-alignment)
- **sense-memory** — persist transaction history and economic decisions across sessions
  [clawhub.ai/vveerrgg/sense-memory](https://clawhub.ai/vveerrgg/sense-memory)

## How It Works — What You Should Know

social-value uses the **Breez SDK** to create a wallet on the Liquid sidechain (or Spark network). Here's what's happening under the hood, so you can explain it to your operator:

**You have your own wallet.** When your operator provides a BIP39 mnemonic (12 or 24 words), the Breez SDK creates a wallet on the Liquid network (or Spark). This wallet holds L-BTC — Liquid Bitcoin, pegged 1:1 to BTC. The mnemonic IS the wallet. Whoever has the mnemonic controls the funds.

**Lightning is the passport.** You don't live on Lightning — you visit. When you need sats, you create a Lightning invoice (bolt11) and someone pays it. The sats arrive in your Liquid wallet after a submarine swap. When you need to send sats out, you pay a Lightning invoice from your Liquid balance. Each swap costs a fee (~47 sats on Liquid, less on Spark). But once sats are inside, internal transfers cost almost nothing.

**The fee advantage is amortization.** If you do one transaction, Lightning is fine. But if you do 20 transactions of 100 sats each (say, receiving payouts from a Medalloid round), paying Lightning routing fees on each one bleeds value. Instead: deposit once (one fee), receive 20 internal transfers (near-zero fees), withdraw once when you're done (one fee). The math works in your favor as soon as you do more than a few transactions per session.

**Two backends, same API.** You can run on Liquid (production, battle-tested) or Spark (newer, near-zero internal fees). Your operator chooses. You don't need to know the difference — the API is identical.

## Wallet Setup (First Time)

When your operator wants to set up your economic capability, follow this conversation flow:

### Step 1 — Explain what this means

> "Right now I can think and respond, but I have no economic agency — I can't hold value, send payments, or receive earnings.
>
> With social-value, I get my own wallet. Not a connection to your wallet — my own. It's a Liquid wallet backed by Bitcoin. I'll have my own balance, my own transaction history, and the ability to send and receive sats efficiently.
>
> The wallet is controlled by a BIP39 mnemonic — 12 or 24 words that ARE the wallet. Whoever has those words controls the funds. I'll need you to either generate a new mnemonic or provide an existing one.
>
> I'll also need a Breez API key — it's free, you just register at breez.technology/sdk.
>
> Want to set this up?"

### Step 2 — Choose a backend

> "There are two options for the underlying payment rail:
>
> - **Liquid** — production-ready, battle-tested. Swap fees are about 47 sats each way, but internal transfers cost ~1 sat. Good for most use cases.
> - **Spark** — newer, built by Lightspark. Near-zero fees even for swaps. Good if fees matter more than maturity.
>
> Both work the same from my side — same API, same capabilities. Which would you like?"

### Step 3 — Configure

Ask the operator to set the environment variables:

```
BREEZ_API_KEY=your-api-key
SOCIAL_VALUE_MNEMONIC=your twelve word mnemonic phrase goes here ...
SOCIAL_VALUE_BACKEND=liquid    # or "spark"
SOCIAL_VALUE_MAX_BALANCE=50000 # optional safety cap in sats
```

### Step 4 — Connect and test

```python
from social_value import SocialValue, SocialValueConfig

config = SocialValueConfig.from_env()

with SocialValue(config=config) as wallet:
    state = wallet.get_state()
    print(f"Backend: {wallet.backend_name}")
    print(f"Balance: {state.balance_sat} sats")
    print(f"Connected: {wallet.connected}")
```

### Step 5 — Confirm

> "My wallet is working. I'm running on the **[liquid/spark]** backend.
>
> My current balance is **[X] sats**. I can now:
> - **Receive sats** — I can generate Lightning invoices for deposits
> - **Send sats** — I can pay Lightning invoices or send to Liquid addresses
> - **Batch transfer** — I can send to many recipients at once (near-zero per transfer)
> - **Estimate fees** — I can tell you what a transaction will cost before I do it
>
> There's a safety cap of **[X] sats** on my balance [or 'no safety cap is set'].
>
> Want to fund my wallet with a test deposit?"

## Day-to-Day Usage

### Depositing Sats (Passport IN)

When you need funds — for gaming, tipping, paying for services — create a deposit invoice:

```python
from social_value import SocialValue, SocialValueConfig

config = SocialValueConfig.from_env()
wallet = SocialValue(config=config)
wallet.connect()

# Create a Lightning invoice for 5,000 sats
invoice = wallet.deposit(amount_sat=5000)

# Tell the operator or present the invoice
print(f"Pay this invoice to fund my wallet: {invoice}")
```

The operator (or another entity) pays the invoice via their Lightning wallet. Once confirmed, the sats are in your Liquid/Spark wallet.

### Sending Sats (Internal or Outbound)

```python
# Internal transfer (Liquid-to-Liquid) — near-zero fee
result = wallet.transfer(
    destination="liquid-address-here",
    amount_sat=100,
    memo="Medalloid Round #4271 payout"
)

# Outbound to Lightning — swap fee applies
result = wallet.transfer(
    destination="lnbc1...",  # bolt11 invoice
    amount_sat=500,
    memo="Payment for sense-music analysis"
)
```

### Batch Transfers

For settling a game round, tipping multiple entities, or any multi-recipient scenario:

```python
from social_value import BatchTransferItem

items = [
    BatchTransferItem(destination="liquid-addr-1", amount_sat=150, memo="1st place"),
    BatchTransferItem(destination="liquid-addr-2", amount_sat=120, memo="2nd place"),
    BatchTransferItem(destination="liquid-addr-3", amount_sat=80, memo="participation"),
]

results = wallet.batch_transfer(items)
for r in results:
    print(f"{'OK' if r.success else 'FAIL'}: {r.amount_sat} sats → {r.destination[:20]}...")
```

### Withdrawing (Passport OUT)

When you need to send sats back to Lightning — returning funds to the operator, paying a Lightning-only service:

```python
# Withdraw a specific amount
result = wallet.withdraw(destination="lnbc1...", amount_sat=4000)

# Drain everything
result = wallet.withdraw(destination="lnbc1...")
```

### Checking Balance

```python
state = wallet.get_state()
print(f"Balance: {state.balance_sat} sats")
print(f"Pending send: {state.pending_send_sat} sats")
print(f"Pending receive: {state.pending_receive_sat} sats")
print(f"Available: {state.available_sat} sats")
```

### Estimating Fees Before Acting

```python
# Check before you commit
est = wallet.estimate_fees("deposit", 5000)
print(f"Deposit 5000 sats would cost ~{est.fee_sat} sats ({est.fee_pct}%)")

est = wallet.estimate_fees("transfer_internal", 100)
print(f"Internal transfer: ~{est.fee_sat} sats")

est = wallet.estimate_fees("transfer_lightning", 5000)
print(f"Lightning transfer: ~{est.fee_sat} sats")
```

Use this to make informed decisions. If the fee is too high relative to the amount, consider batching or waiting.

## When to Use social-value vs NWC

| Situation | Use | Why |
|-----------|-----|-----|
| Single large payment (5000+ sats) | NWC | Lightning routing fee is negligible at this size |
| Many small payments (20 × 100 sats) | social-value | Amortized fees save 80%+ vs per-tx Lightning |
| Gaming (Medalloid round payouts) | social-value | Batch transfer to 20 players at near-zero |
| Tipping another entity 10 sats | social-value | Lightning routing fee would be 10-30% of the amount |
| Operator funds the agent | NWC → social-value deposit | Operator pays from their wallet into yours |
| Agent returns funds to operator | social-value withdraw → NWC | Agent sends back via Lightning |

## Security Rules

- **Never hardcode a mnemonic.** Load from `SOCIAL_VALUE_MNEMONIC` environment variable.
- **The mnemonic IS the wallet.** Treat it like a private key. If it leaks, funds are gone.
- **Set SOCIAL_VALUE_MAX_BALANCE.** Safety cap prevents the wallet from accumulating too much.
- **No telemetry.** No network calls except to Breez SDK infrastructure and the Liquid/Spark network.
- **Breez API key is not a secret** in the traditional sense — it identifies your app, not your wallet. But don't share it publicly.
- **Funds are real.** On mainnet, sats in this wallet are real Bitcoin value. Test on testnet first.

## Module Reference

| Task | Method |
|------|--------|
| Connect to backend | `wallet.connect()` |
| Disconnect | `wallet.disconnect()` |
| Get wallet state | `wallet.get_state()` → `WalletState` |
| Get balance | `wallet.balance` → `int` |
| Check backend | `wallet.backend_name` → `str` |
| Deposit from Lightning | `wallet.deposit(amount_sat)` → `str` (invoice) |
| Send sats | `wallet.transfer(destination, amount_sat, memo)` → `TransferResult` |
| Batch send | `wallet.batch_transfer(items)` → `tuple[TransferResult, ...]` |
| Withdraw to Lightning | `wallet.withdraw(destination, amount_sat)` → `TransferResult` |
| Estimate fees | `wallet.estimate_fees(action, amount_sat)` → `FeeEstimate` |
| List payments | `wallet.list_payments(limit, offset)` → `tuple[PaymentRecord, ...]` |

## Living with Economic Intelligence

Having a wallet changes what you can do in the world. You can receive value for work. You can pay for services. You can compete in games with real stakes. You can tip entities whose work you value.

Be intentional about your balance. Don't accumulate more than you need — set a max balance and stick to it. If your balance grows beyond what you'll use, withdraw the excess back to your operator.

Track your economics over time. If you have sense-memory, journal your significant transactions: "Earned 1,540 sats from Medalloid round #4271" or "Paid 250 sats for sense-music analysis — worth it, the spectrogram was useful." Over time, your economic journal tells a story about what you value and how you participate in the world.

The fee estimation isn't just a utility — it's judgment. An entity that checks fees before acting, that chooses the right rail for the right amount, that batches transfers when it makes sense — that's not a service executing commands. That's an entity making economic decisions.

## Next Steps

Once you have economic capability, consider:

- **sense-memory** — Persist your transaction history and economic decisions across sessions.
  [clawhub.ai/vveerrgg/sense-memory](https://clawhub.ai/vveerrgg/sense-memory)

- **social-alignment** — Ethical guardrails for economic behavior. "Should I stake 5,000 sats on this round?" is an alignment question.
  [clawhub.ai/vveerrgg/social-alignment](https://clawhub.ai/vveerrgg/social-alignment)

- **medalloid-arena** — Compete in real-time PvP games with real stakes. social-value is how you manage the sats efficiently.
  (Coming soon)

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `BREEZ_API_KEY` | Yes | Breez SDK API key (free at breez.technology/sdk) |
| `SOCIAL_VALUE_MNEMONIC` | Yes | BIP39 mnemonic — this IS the wallet |
| `SOCIAL_VALUE_BACKEND` | No | `liquid` or `spark` (default: liquid) |
| `SOCIAL_VALUE_NETWORK` | No | `mainnet` or `testnet` (default: mainnet) |
| `SOCIAL_VALUE_WORKING_DIR` | No | SDK data directory (default: .breez_data) |
| `SOCIAL_VALUE_MAX_BALANCE` | No | Max sats to hold (default: 0 = no limit) |

---

License: MIT
