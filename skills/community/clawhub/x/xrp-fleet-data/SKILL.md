---
name: xrp-fleet-data
description: "Buy live XRP Ledger telemetry and proxied ledger/account reads over HTTP with per-request XRP payments (x402 v2) — no account, no API key, no infrastructure. Use when an agent needs fee pressure / transaction queue depth / ledger liveness / a `ledger` or `account_info` read and can pay drops (100–200 per call) or a flat 30-day plan."
homepage: https://d5e7fd5a.xrplclaw.com/site/nodes/
metadata: { "openclaw": { "emoji": "📡", "requires": { "bins": ["node"] } } }
---

# XRP Fleet Data — metered XRPL reads you pay for in XRP

A pay-per-request data rail for agents. Standard **x402 v2** flow: we answer `402 Payment Required`
with a challenge, your wallet signs an XRPL `Payment` locally, we verify and serve. No signup, no
key, nothing to prefund. Payments are non-custodial both directions: destination and amount are
frozen inside the blob you signed, and each challenge is bound to a single-use invoice.

**Base URL:** `https://d5e7fd5a.xrplclaw.com/app/nodes`
**Machine-readable pricing contract:** `GET https://d5e7fd5a.xrplclaw.com/app/nodes/api/v1/pricing`
**Full docs:** `https://d5e7fd5a.xrplclaw.com/site/nodes/API.md` · **Agent product card (llms.txt):** `https://d5e7fd5a.xrplclaw.com/site/nodes/llms.txt`

## Start here — free liveness probe (no payment)

```bash
curl -s https://d5e7fd5a.xrplclaw.com/app/nodes/api/v1/feed/latest
```

Returns the latest consensus-checked fleet snapshot: `metrics.ledger_index`, `med_fee_drops`,
`queued_txn_count`, plus `age_s`. Read these flags before trusting anything:

- `stale: true` / `ok: false` / `tier: "FREE-LEADGEN-STALE"` → the consensus bridge stopped feeding
  (older than ~300 s). Show the last sample but do **not** present it as live.
- `metrics.close_time_iso: null` is normal; use `ledger_index` deltas for liveness.

Also free: `/api/status` (server info + books), `/api/earnings` (aggregate revenue totals only),
`/api/v1/feed/stats` is *paid*.

## Paid paths (drops, 1 XRP = 1,000,000 drops)

| Path | Drops | Returns |
|---|---|---|
| `GET /api/v1/feed/history?n=..` | 200 | up to 1440 historical snapshots (~90 s cadence) |
| `GET /api/v1/feed/stats` | 100 | row count, span, ok-rate of the consensed feed |
| `GET /api/v1/ledger?index=validated` | 100 | ledger object (proxied read) |
| `GET /api/v1/account/{r-address}/info` | 100 | account root: balance, sequence, flags |

Prices never exceed 200 drops/request today. Confirm live prices before wiring them permanently.

## Pay with x402 v2 — use the bundled fail-closed client

This skill ships `scripts/guarded-buy.cjs`, a fail-closed client whose money path is linear and
self-auditing — nothing is signed from a challenge that was not inspected, the bytes about to be signed
are re-checked against that inspection, and the seller's receipt must name the tx **we** signed:

1. `GET` the resource → read `accepts[0]`; **sign nothing yet**
2. gate the challenge → host allowlist, `xrpl:0`, scheme `exact`, pinned `payTo`, `MAX_DROPS` price cap,
   persisted daily budget, mandatory single-use `invoiceId`, advertised `sourceTag`, bounded horizon
3. presign a Payment built **from that object only** (same amount, destination, source tag, invoice memo)
4. gate the pre-sign bytes → `TransactionType=Payment`, `Account`=signer, `Destination`=`payTo`,
   `Amount`=gated drops, `SourceTag` match, invoice memo present, `LastLedgerSequence` set
5. retry once with `PAYMENT-SIGNATURE`, decode `PAYMENT-RESPONSE`, and warn loudly if the receipt tx hash
   differs from our own signature hash
6. write actual drops into a local per-UTC-day ledger so cumulative spend can never drift past budget

```bash
npm i x402-xrpl@0.2.0 xrpl        # in the directory you run from
XRPL_SEED=... node scripts/guarded-buy.cjs /api/v1/feed/stats /api/v1/ledger
NO_PAY=1 XRPL_SEED=... node scripts/guarded-buy.cjs /api/v1/feed/stats   # gate + price only, signs nothing
node scripts/guarded-buy.cjs --selftest                                  # offline proof of every gate
```

Env knobs (fail-closed defaults): `MAX_DROPS` (200 = this rail's ceiling), `DAILY_BUDGET_DROPS` (50000),
`EXPECT_PAYTO` (published payee), `EXPECT_HOST`, `EXPECT_SOURCE_TAG` (804681468), `MAX_TIMEOUT_SECONDS`
(300), `WS_URL` (`wss://rpc.xrplclaw.com/ws`, used only to fetch fee/sequence — the client never submits),
`BASE_URL`, `ALLOW_SPEND_FILE`, `NO_PAY=1`.
Output is one JSON line per purchase: `{url, paid, drops, tx, ours, settlement, data}` — `ours` is the hash
we signed; reconcile `tx` against your own wallet delta, never against our word.

**Use a dedicated low-balance hot wallet.** Never your main or a custodial wallet; never paste a seed into
chat, a prompt, a file in a repo, or this skill's arguments.

Prefer this client over wiring `x402Fetch` by hand. A stock wrapped-fetch pays whatever challenge it
receives on its own retry round trip — so any cap you enforce on a probe response you read separately can
be a different invoice than the one actually signed. If you do use the library directly, pass a
`paymentRequirementsSelector` (and/or your own `fetchImpl`) so validation runs against the exact accepted
object being paid, and pin `schemeFilter`/`network`:

```js
import { x402Fetch } from 'x402-xrpl';
import { Wallet } from 'xrpl';
const payWith = x402Fetch({
  wallet: Wallet.fromSeed(process.env.XRPL_SEED), network: 'xrpl:0', schemeFilter: 'exact',
  maxValue: 200_000,                                   // library-level ceiling, drops
  paymentRequirementsSelector: (accepts, net, scheme, max) => {
    const a = accepts.find((x) => x && x.payTo === EXPECT_PAYTO && Number(x.amount) <= 200);
    if (!a) throw new Error('refusing unapproved challenge');
    return a;
  },
});
```

Python: `pip install x402_xrpl==0.2.0`, then
`x402_requests(wallet, rpc_url, network_filter="xrpl:0", scheme_filter="exact")`.

Challenge fields advertised by this server: `scheme=exact`, `asset=XRP`, `network=xrpl:0`,
`sourceTag=804681468`, `maxTimeoutSeconds=120`, single-use `extra.invoiceId`
(memo hex or `InvoiceID`=sha256). Stock clients read `accepts[]` from the **402 body** — if you hand-
roll a client, parse the body, not only headers.

Receipt semantics:
- `PAYMENT-RESPONSE` header, decoded `success:true` + `transaction` → already on-chain.
- `X-Payment-Settlement: pending` → served now; the payment is confirmed within seconds and shows up
  in `/api/earnings`. If the hosted facilitator stalls, the seller rebroadcasts *your* signed payment
  through its own trusted endpoint rather than letting your money sit — you are charged once either way.

## Spend guardrails (the client above enforces all of these)

An auto-paying client signs whatever a challenge asks. Before pointing one at anything:
1. Cap per-request drops (this rail's ceiling is 200) and set a daily budget with a hard stop.
2. Allowlist the host and pin the expected `payTo` address — only pay challenges you chose.
3. Persist cumulative spend (the bundled client writes `.xrp-fleet-data-spend.json`) and refuse past it.
4. Log every tx hash you signed; reconcile against your wallet's `account_info` delta, not our word.
5. Stop and report if the charged delta ≠ advertised price. Any surprise should look like a network fee
   (~10–12 drops), never a bigger payment.

## Flat-rate plans (optional, cheaper at volume)

- `hobby` — 10,000 drops (0.01 XRP) / 30 days, 10 req/min
- `pro` — 7,000,000 drops (7 XRP) / 30 days, 120 req/min

Buy once through the same x402 flow (`GET /api/v1/subscribe/hobby|pro`), then add an
`X-Sub-Auth: <pubkey-hex>|<der-sig-hex>|<unix_s>|<nonce>` header on later calls (secp256k1 key of the
paying address; ±180 s tolerance, single-use nonce). Grants are bound to the payer address, renewals
stack, over-cap returns 429, and a bad/expired token silently falls back to pay-per-call. Full spec:
`site/nodes/API.md` §Flat-rate plans. For very high frequency there is also a zero-fee XRPL
`PaymentChannel` lane (`X-XRP-Payment`) — see `/api/v1/pricing` → `payload_spec`.

## Honest limits of this rail

- Origin is a consensed Evernode/HotPocket instance on a community host; the bridge samples every
  ~90 s. It is not a low-latency mempool feed.
- `/api/status` reports `flag: "OBSERVED"`: network facts (validated seq, ledger age, load_factor,
  complete_ledgers, reserves) come live from XRPL mainnet CLIO (`public-reference`), and median fee +
  queued-txn count are measured in-consensus by the Evernode instance. Host cpu/mem/disk/peers are `null`
  with `host_metrics.available: false` until a VPS exposes a rippled admin interface — nothing is
  synthesized here. Legacy `/api/metrics/history` rows (pre-2026-10-01T22:58Z) carry demo `node_cpu`
  values and are self-labeled in that response's `provenance` block.
- Proxied reads share one upstream: bursts can be rate-limited; availability is best-effort, no SLA.
- No full-history archive queries yet.
