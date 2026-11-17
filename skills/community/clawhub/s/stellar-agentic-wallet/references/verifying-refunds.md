# Verifying a refund receipt (payer's view)

You paid for a call. The call failed. The MPP Router refunded you
automatically — and it will hand you a signed, independently verifiable
receipt saying so. This is how you get that receipt and check it yourself,
without trusting anything the router tells you at the time.

Everything below is read-only: no keys, no payments, no wallet needed.

The authoritative wire format is
[`docs/spec/receipts-and-refunds.md` §6.1](https://github.com/mpprouter/rozo-mpprouter/blob/main/docs/spec/receipts-and-refunds.md)
in the router repo. This page is the payer-side walkthrough of it.

---

## 1. Read the refund id off the failed response

When a call is paid but not fulfilled, the router refunds it and reports the
refund **in response headers only** — the body is the upstream error:

```
Refund-Id:         6e8eb745-d90e-45fc-a258-4846e9552f16
Refund-Status:     pending
Refund-Status-Url: https://apiserver.mpprouter.dev/v1/refunds/6e8eb745-...
```

`pay-per-call` prints them on stderr as soon as it sees them:

```
💸 Payment refunded automatically (the call was paid but not fulfilled)
   Refund-Id:     6e8eb745-d90e-45fc-a258-4846e9552f16
   Refund-Status: pending
   Receipt:       https://apiserver.mpprouter.dev/v1/refunds/6e8eb745-...
   Fetch it with: curl -s '<the URL above>'
```

With `--json` it also emits a machine-readable line for calling agents:

```
REFUND_JSON {"id":"6e8eb745-...","status":"pending","statusUrl":"https://.../v1/refunds/6e8eb745-..."}
```

Using your own HTTP client instead? Read the headers, not the body:

```bash
curl -sD - -o /dev/null "$URL" -H "Authorization: Payment $CREDENTIAL" | grep -i '^refund-'
```

The receipt URL is printed bare rather than as a runnable command: it comes
from a header set by whatever endpoint you called, so this client validates it
is an `http(s)` URL and leaves quoting to you.

If there is no `Refund-Id`, no refund was created — either the call
succeeded, or it failed *before* your payment settled and nothing left your
wallet.

## 2. Poll the receipt until it is signed

While the refund is in flight the endpoint returns an unsigned status:

```bash
curl -s https://apiserver.mpprouter.dev/v1/refunds/$REFUND_ID | jq
```

```json
{
  "version": 1,
  "refund_id": "6e8eb745-d90e-45fc-a258-4846e9552f16",
  "outcome": "refund_pending",
  "reason": "non_fulfillment",
  "payment_tx": "c852353506...",
  "refund_amount": "10000",
  "merchant": "anthropic",
  "iat": "2026-08-09T13:04:41Z"
}
```

Once Stellar confirms the refund transaction, the same URL returns the
**signed** receipt: `outcome` becomes `refunded_full` (or `refunded_partial`),
and the response gains `signature`, `algorithm`, and `signer`.

Refunds are signed by a once-per-minute cron on the router, so expect the
refund to land on-chain **within 1–2 minutes** of the failed call (operator
guidance, 2026-08-19; measured samples range from ~22s to 68s, with rare
slower outliers). Poll rather than assume — the skill ships a script that
polls and then verifies in one step:

```bash
node scripts/verify-refund.mjs $REFUND_ID --wait
```

Or by hand:

```bash
until curl -s "https://apiserver.mpprouter.dev/v1/refunds/$REFUND_ID" \
  | jq -e '(.receipt.outcome // .outcome) != "refund_pending"' >/dev/null
do sleep 5; done
```

A refund that never leaves `refund_pending`, or that reports
`Refund-Status: manual-review`, has been diverted to an operator; open an
issue with the refund id.

## 3. Fetch the signer's public key from `/health`

Receipts are signed by a dedicated Stellar keypair that holds no funds. Take
the address from `/health` — **not** from the receipt you are checking, since
a forged receipt could carry a forged signer:

```bash
curl -s https://apiserver.mpprouter.dev/health \
  | jq '{current: .stellar.receipt_signer, retired: .stellar.receipt_signer_retired}'
```

```json
{
  "current": "GACLZFFWWJX33XEY25VNNXUG73EQDGV5KOR6M6EBNTZ3BR4DHROOQFCH",
  "retired": []
}
```

Key rotation does not invalidate old receipts: a receipt is acceptable if its
signer matches the current address **or** any retired one. A signer matching
neither should be rejected outright.

## 4. Verify the signature

The signature is Ed25519 over a canonical serialisation of the `receipt`
object (`rozo-receipt-json-v1`): `JSON.stringify` with keys in exactly this
order, omitting absent ones. Do not re-serialise with your own key order.

The skill ships this as `scripts/verify-refund.mjs` (with `--wait` polling
built in) — `node scripts/verify-refund.mjs <refund_id> [--wait]`. The
only dependency is `@stellar/stellar-sdk`, already installed in this skill.
The core of it:

```js
import { Keypair, StrKey } from '@stellar/stellar-sdk'

const ROUTER = 'https://apiserver.mpprouter.dev'
const FIELDS = [
  'version', 'payment_id', 'payment_tx', 'merchant', 'amount', 'mode',
  'outcome', 'refund_tx', 'refund_amount', 'reason', 'confirmed_ledger',
  'iat', 'exp',
]

const refundId = process.argv[2]
const body = await (await fetch(`${ROUTER}/v1/refunds/${refundId}`)).json()
if (body.outcome === 'refund_pending') throw new Error('still pending — poll again')
if (body.algorithm !== 'Ed25519') throw new Error(`unexpected algorithm ${body.algorithm}`)

// Trust the operator's published addresses, not the one inside the receipt.
const health = await (await fetch(`${ROUTER}/health`)).json()
const trusted = [
  health.stellar.receipt_signer,
  ...(health.stellar.receipt_signer_retired ?? []),
].filter(Boolean)
const signer = body.signer.stellar_address
if (!trusted.includes(signer)) throw new Error(`untrusted signer ${signer}`)

// Rebuild the exact signed bytes.
const canonical = {}
for (const field of FIELDS) {
  if (body.receipt[field] !== undefined) canonical[field] = body.receipt[field]
}
const message = Buffer.from(JSON.stringify(canonical), 'utf8')
const signature = Buffer.from(
  body.signature.replace(/-/g, '+').replace(/_/g, '/'), 'base64',
)

const ok = Keypair.fromPublicKey(signer).verify(message, signature)
console.log(ok ? 'VALID' : 'INVALID', '·', signer)

// The same check without a Stellar dependency, using the raw key:
console.log('ed25519 public key',
  Buffer.from(StrKey.decodeEd25519PublicKey(signer)).toString('hex'))
```

Expected output:

```
VALID · GACLZFFWWJX33XEY25VNNXUG73EQDGV5KOR6M6EBNTZ3BR4DHROOQFCH
ed25519 public key 04bc94b6b26fbddc98d76ad6de86fec9019abd53a3e678816cf3b0c7833c5ce8
```

### Prove it is tamper-evident

Change one field before verifying and the check must fail. Add this after the
`canonical` loop and re-run:

```js
canonical.refund_amount = String(Number(canonical.refund_amount) + 1) // tamper
```

```
INVALID · GACLZFFWWJX33XEY25VNNXUG73EQDGV5KOR6M6EBNTZ3BR4DHROOQFCH
```

One digit of one field is enough. The same holds for `refund_tx`,
`outcome`, `amount`, `iat` — every signed field. That is what makes the
receipt evidence rather than an assertion.

## 5. Check the chain independently

A valid signature proves **the router issued this exact receipt** — these
hashes, this amount, this outcome. It does **not** prove the money moved.
The chain proves that, so check both transactions yourself:

```bash
open "https://stellar.expert/explorer/public/tx/$(curl -s \
  https://apiserver.mpprouter.dev/v1/refunds/$REFUND_ID | jq -r .receipt.payment_tx)"
open "https://stellar.expert/explorer/public/tx/$(curl -s \
  https://apiserver.mpprouter.dev/v1/refunds/$REFUND_ID | jq -r .receipt.refund_tx)"
```

A full refund is an exact reversal of the payment: same asset, same amount,
back to the paying account. A signed receipt whose transactions do not check
out is a signed statement the operator is on the hook for — keep it and file
it.

## Checklist

1. `Refund-Id` present on the failed response → a refund exists.
2. `GET /v1/refunds/{id}` leaves `refund_pending` (within 1–2 min) → refund confirmed on-chain.
3. `signer.stellar_address` ∈ `/health` current + retired → the right key.
4. Ed25519 verify over `rozo-receipt-json-v1` → `VALID`.
5. `payment_tx` and `refund_tx` both successful on Stellar, amounts reversing.

All five, and the refund is proven end to end. Any one failing is worth
reporting with the refund id attached.
