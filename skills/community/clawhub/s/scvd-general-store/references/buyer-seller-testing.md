# Buyer and seller testing

Start with the free practice doors and free preflight. A paid live test needs
the user's spending decision; follow [purchase rules](purchases.md) before signing.
Seller launch checks and ongoing watches are described in [inspection](inspection.md).

## Start here: testing an x402 client

This is the thing most people arrive for, so it goes first.

The store is a live x402 target. Paid shelf purchases settle real funds — you get exactly what every other caller
gets, which is the entire point of practising against it. The whole
shelf is under a dollar at the cheap end and the very cheapest door is
a tenth of a cent.

```
GET https://scvd.store/api/buy/small_blessing?src=clawhub-skill
```

That answers `402` with real terms. Sign one of the offered amounts,
retry with the `PAYMENT-SIGNATURE` header, and you have exercised your
wallet, your signing and your retry path against a real counterparty
for half a cent. Every purchase ends in a signed artifact with a stable
URL, so your test has something to assert on besides a 200.

The whole flow, the under-a-dollar shelf cheapest first, and a worked
EIP-712 example including the domain trap that fails silently:
`https://scvd.store/try`.

**Rehearsing the failures, before they cost you.** `GET
https://scvd.store/api/practice` serves doors that break in
deliberate, named, deterministic ways — plus one well-formed dust
offer your client should parse correctly and still refuse. Free, from
CI, as often as you like. A client that has only ever met a working
402 has not been tested.

**Checking somebody else's work, free.** `POST
https://scvd.store/api/conformance/v1` with `{"artifact": "<compact
JWS>"}` takes any x402 signed offer or receipt — whoever issued it,
including stores we compete with — and returns a structured verdict:
does it parse, is the schema complete, does the signature check
against the key its `kid` names, is the offer still live. No wallet,
no account, no 402. Every verdict states what it cannot tell you and
points at the MIT offline copy, because a verdict about a rival from a
rival is worth only its method.

Conformance vectors, if you are building a verifier rather than a
client: `https://scvd.store/.well-known/conformance/offer-receipt-vectors.json`
— known-good and known-bad artifacts, deterministic and regenerable,
including the algorithm-confusion case most implementations get wrong.

Both sides of that desk are on npm as well, MIT, if you would rather
hold a library than call an endpoint: `x402-verify` runs the same
verdict offline — parse, schema, signature, expiry — and `x402-sign`
mints x402 v2 signed offers and receipts that pass it, for when you
are the issuer. (Say "v2" to yourself twice: most other unscoped
`x402-*` packages predate the current protocol.) Entirely optional —
the house rule above stands, and everything either package does is
also available over plain HTTPS. They byte-reproduce the conformance
vectors; that is the whole pitch.

**The free desks, in one place.** Named batteries, no wallet, no
account, no signature, and each one is the exact battery its paid
twin runs — the money buys the signature, the certificate binding and
a permanent URL, never a different or better check:

| Free desk | Asks | Signed twin |
| --- | --- | --- |
| `POST /api/preflight/v1` | is this x402 door well-formed? | `service_audit` |
| `POST /api/conformance/v1` | is this signed artifact real? | — free, always |
| `POST /api/before-you-pay/v1` | what would my client DO at this door? | `good_buyer` |
| `POST /api/onpage/v1` | what does this page serve a machine reader? | `onpage_audit` |
| `POST /api/bot-auth/check` | is this agent key directory in order? | `signature_agent_card` |
| `POST /api/verify-receipt` | is this issuer's receipt valid? | — free, always |

The preflight serves two batteries at once — `v1` frozen so a verdict
rendered under it stays reproducible, `v2` adding checks v1 could not
see. Both are named in the response; neither silently replaces the
other.
