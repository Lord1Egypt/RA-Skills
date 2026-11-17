# Two 402 dialects, one Stellar payment — an end-to-end showcase

This skill speaks both HTTP-402 dialects in use on Stellar today:

| Dialect | Challenge carried in | Payment carried in |
| --- | --- | --- |
| **MPP** | `WWW-Authenticate: Payment <auth-params>` | `Authorization: Payment <credential>` |
| **x402 v2** | `Payment-Required: <base64 envelope>` | `X-Payment: <base64 envelope>` |
| x402 legacy | same envelope, in the JSON response body | `X-Payment: <base64 envelope>` |

The point of this document is that **the dialects differ only in
packaging**. Underneath, both ask for the identical thing: a sponsored
Soroban SAC `transfer` on Stellar. The client signs that transfer once
and only then decides which envelope to put it in.

Every part of this document is **real captured data**, including the
paid retry. Both dialects were settled on mainnet on 2026-07-31 — the
x402 half only after fixing three client defects and one server-side
config bug that had kept that path broken since it was written.

---

## Part 1 — The unpaid call

Captured 2026-07-31 against a live, verified MPP Router route. An unpaid
request to a payable route returns the challenge and charges nothing, so
this is reproducible for free:

```bash
curl -s -D headers.txt -o body.json \
  -X POST https://apiserver.mpprouter.dev/v1/services/firecrawl/scrape \
  -H 'content-type: application/json' \
  -d '{"url":"https://example.com"}'
```

Response:

```http
HTTP/2 402
content-type: application/problem+json
www-authenticate: Payment id="taXgfY5_EKUBYh17XrVS_5KzFpdCqfsox6POv9xYEVs", realm="apiserver.mpprouter.dev", method="stellar", intent="charge", request="eyJhbW91bnQiOiIyMDAwMC…", expires="2026-07-31T00:21:12.780Z", opaque="eyJyb3V0ZSI6ImZpcmVjcmF3bF9zY3JhcGUifQ"
payment-required: eyJ4NDAyVmVyc2lvbiI6MiwiZXJyb3IiOiJQYXltZW50IHJlcXVpcmVkIiwicmVzb3VyY2U…
```

```json
{
  "type": "https://paymentauth.org/problems/payment-required",
  "title": "Payment Required",
  "status": 402,
  "detail": "Payment is required.",
  "challengeId": "taXgfY5_EKUBYh17XrVS_5KzFpdCqfsox6POv9xYEVs"
}
```

**Both dialects arrive in a single response.** That is what makes MPP
Router the useful specimen: one request, two complete challenges, and a
client has to make a choice.

---

## Part 2 — Decoding each challenge, field by field

### 2a. MPP dialect — `WWW-Authenticate`

An RFC 7235 challenge with auth scheme `Payment`. Two of its parameters
(`request`, `opaque`) are base64url-encoded JSON.

| Parameter | Value | Meaning |
| --- | --- | --- |
| `id` | `taXgfY5_EKUBYh17XrVS_5KzFpdCqfsox6POv9xYEVs` | Challenge id, **HMAC-bound by the server to every other field**. Must round-trip byte-for-byte into the credential. |
| `realm` | `apiserver.mpprouter.dev` | Protection space. |
| `method` | `stellar` | Payment method family. |
| `intent` | `charge` | The `stellar.charge` flow (see `mpp-charge-spec.md`). |
| `expires` | `2026-07-31T00:21:12.780Z` | Challenge lifetime — a few minutes. |
| `opaque` | base64url | Server state, echoed back unmodified. |
| `request` | base64url | The charge itself, decoded below. |

`opaque` decodes to:

```json
{ "route": "firecrawl_scrape" }
```

`request` decodes to:

```json
{
  "amount": "20000",
  "currency": "CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75",
  "methodDetails": {
    "credentialTypes": ["transaction"],
    "feePayer": true,
    "network": "stellar:pubnet"
  },
  "recipient": "GDK3AVW3YE6UL3J4WLNKBMP65KSY32YPUKIOC6PXW65XJ3LEG3YIDXXB"
}
```

- `amount` — **base units**, i128 decimal string. USDC has 7 decimals, so
  `20000` = `0.0020000` USDC. It is not a human decimal; treating it as
  one under-reports the charge by 10⁷.
- `currency` — the Soroban SAC contract id (a `C…` address), not the
  string `"USDC"`. The client passes it straight through as the token
  contract to invoke.
- `recipient` — the destination `G…` account.
- `methodDetails.feePayer: true` — sponsored mode. The client signs auth
  entries only; the server pays the Stellar network fee and submits.
- `methodDetails.credentialTypes: ["transaction"]` — the server wants a
  signed XDR to broadcast itself (pull), not a hash of something the
  client already broadcast (push).

Parsed by `parse402()` in `scripts/src/pay-engine.ts`, which delegates
the header walk to `mppx.Challenge.deserialize` rather than hand-rolling
RFC 7235 parsing — that hand-rolled version was the source of the v1.1.0
–v1.1.3 regressions.

### 2b. x402 dialect — `Payment-Required`

The header value is a plain base64 (not base64url) JSON envelope:

```json
{
  "x402Version": 2,
  "error": "Payment required",
  "resource": {
    "url": "https://apiserver.mpprouter.dev/v1/services/firecrawl/scrape"
  },
  "accepts": [
    {
      "scheme": "exact",
      "network": "stellar:pubnet",
      "amount": "20000",
      "asset": "CCW67TSZV3SSS2HXMBQ5JFGCKJNXKZM7UQUWUZPUTHXSTZLEO7SJMI75",
      "payTo": "GDK3AVW3YE6UL3J4WLNKBMP65KSY32YPUKIOC6PXW65XJ3LEG3YIDXXB",
      "maxTimeoutSeconds": 300,
      "extra": { "areFeesSponsored": true }
    }
  ]
}
```

| x402 field | MPP equivalent | Note |
| --- | --- | --- |
| `accepts[0].amount` | `request.amount` | Identical: `20000` base units. |
| `accepts[0].asset` | `request.currency` | Identical SAC contract id. |
| `accepts[0].payTo` | `request.recipient` | Identical `G…` address. |
| `accepts[0].network` | `request.methodDetails.network` | Both CAIP-2 `stellar:pubnet`. |
| `extra.areFeesSponsored` | `methodDetails.feePayer` | Both assert sponsored mode. |
| `maxTimeoutSeconds` | `methodDetails.maxTimeoutSeconds` | Derives the auth-entry expiration ledger. |
| `x402Version: 2` | — | No MPP analogue; must be echoed in `X-Payment`. |
| — | `id` (HMAC-bound) | No x402 analogue; x402 carries no per-challenge binding. |

`accepts` is an array: a server may offer several ways to pay. This
client reads `accepts[0]` only.

### 2c. Do the two dialects use different `payTo` addresses?

**Not in production today.** Earlier documentation in this repo said the
two dialects are routed to different addresses. That was checked against
production on 2026-07-31 and is not what MPP Router emits:

- On all three payable routes probed live (`firecrawl/scrape`,
  `exa/search`, `parallel/search`), the MPP `recipient` and the x402
  `payTo` were **byte-identical**.
- The published catalog agrees: all 481 payable services advertise the
  same single `pay_to`, and `methods.stellar_x402.pay_to` equals
  `payment_hints.pay_to` for every one of them.

What *is* true, and what actually matters, is that the MPP challenge
`id` is HMAC-bound to the challenge contents. You still cannot assemble a
credential from mixed fields — but the reason is the binding, not a
per-dialect address split. `SKILL.md` has been corrected accordingly.

Practical consequence: **do not hardcode either assumption.** Always pay
the address in the challenge you actually parsed, and — when you know
what to expect from the catalog — pass `--expect-pay-to` /
`--expect-amount` so a rewritten challenge is refused before signing
(`validateChallenge()` in `pay-engine.ts`).

### 2d. Which one does this client pick?

MPP, whenever the `WWW-Authenticate: Payment` header is present. Order in
`parse402()`: MPP header → `Payment-Required` header → legacy JSON body.
There is deliberately no dialect override flag.

A `WWW-Authenticate` that is *not* the `Payment` scheme (a `Bearer`
challenge from an auth proxy, say) must not abort parsing; the client
falls through to the x402 branches. That case is covered by
`scripts/smoke-test-x402-dialect.ts`.

---

## Part 3 — One inner transaction, two wrappers

Both challenges above resolve to the same `ParsedChallenge`, and the
client signs **once**, in `signSacTransfer()`
(`scripts/src/stellar-signer.ts`):

1. Build a Soroban `invokeHostFunction` op calling
   `transfer(from = signer, to = payTo, amount = i128)` on the SAC
   contract from `asset` / `currency`.
2. Source account = the all-zeros placeholder — the server rebuilds and
   fee-bumps the envelope.
3. Sign **auth entries only**, via `authorizeEntry(entry, keypair,
   validUntilLedger, networkPassphrase)`, where `validUntilLedger` is
   derived from `maxTimeoutSeconds`. The transaction envelope is left
   unsigned.
4. Export with `envelope.toXDR("base64")`.

That single XDR string then gets wrapped differently per dialect, in
`buildRetryHeaders()`:

**MPP** → `encodeMppHeader()` builds an `mppx.Credential`:

```jsonc
{
  "challenge": { /* the ENTIRE challenge, echoed byte-for-byte incl. `id` */ },
  "payload":   { "type": "transaction", "transaction": "<base64 XDR>" },
  "source":    "did:pkh:stellar:pubnet:G…"   // signer's own account
}
```

serialized by `mppx.Credential.serialize` and sent as:

```http
Authorization: Payment <base64url credential>
```

Two footguns live here, both previously shipped as bugs:

- `network` from the challenge **already carries the `stellar:` prefix**,
  so the DID is `did:pkh:${network}:${pubkey}`. Prepending another
  `stellar:` produces `did:pkh:stellar:stellar:pubnet:…` (the v1.1.2 bug).
- The challenge must be echoed exactly as received. Re-canonicalizing or
  re-encoding `request` / `opaque` breaks the server's HMAC over `id`.

**x402** → `wrapX402()` + `encodeX402Header()`:

```json
{
  "x402Version": 2,
  "scheme": "exact",
  "network": "stellar:pubnet",
  "payload": { "transaction": "<base64 XDR>" }
}
```

base64-encoded and sent as:

```http
X-Payment: eyJ4NDAyVmVyc2lvbiI6Miwic2NoZW1lIjoiZXhhY3QiLCJ…
```

`x402Version` is echoed from the challenge (`2` here), **not** hardcoded
to `1`. Regression-guarded in `smoke-test-x402-dialect.ts`.

One more x402-only rule: `extra.areFeesSponsored: false` is not
supported, because the whole flow depends on the server paying the fee.
`assertSponsored()` rejects it with a named error.

---

## Part 4 — The paid retry and the receipt

> ✅ **Real mainnet capture, 2026-07-31.** Two payments were made from a
> dedicated hot wallet to produce this section:
> `firecrawl/scrape` at $0.002 and `ipinfo_ip-lite` at $0.001. Both
> settled; both transaction hashes below are real and resolvable on
> stellar.expert.

The retry is the original request with the payment header attached:

```http
POST /v1/services/firecrawl/scrape HTTP/2
content-type: application/json
Authorization: Payment <base64url credential>     # MPP dialect
# — or, for the x402 dialect —
X-Payment: <base64 envelope>
```

A settled payment returns `200` with the merchant's response body and a
`Payment-Receipt` response header — a dot-separated, base64url token.
Two shapes are in circulation: a single payload segment, and a classic
three-segment JWT. `decodeReceipt()` (`scripts/src/receipt.ts`) decodes
every segment that parses as a JSON object and merges them, so signature
segments are simply skipped and one decoder serves both shapes.

MPP Router's actual receipt is a **single base64url segment** (no dots,
no signature segment). Decoded, verbatim, from the `ipinfo_ip-lite` call:

```json
{
  "method": "stellar",
  "reference": "ade2e9d16a45528a74d1b6f306ca3aa7e88d64aaf059042f7f9cda026e64e5d4",
  "status": "success",
  "timestamp": "2026-07-31T00:45:35.305Z"
}
```

**Note what is not there: no `amount`, no `payTo`.** The receipt carries
only the settlement reference and a status. Everything the user reads
about *what* was paid therefore comes from the 402 challenge, via the
client's fallback — that fallback is load-bearing, not decoration.
`timestamp` arrives as an ISO-8601 string, not unix seconds.

The client renders it as:

```
📝 Payment: 0.0010000 USDC → GDK3AVW3YE6UL3J4WLNKBMP65KSY32YPUKIOC6PXW65XJ3LEG3YIDXXB (2026-07-31T00:45:35.305Z)
🔗 Explorer: https://stellar.expert/explorer/public/tx/ade2e9d16a45528a74d1b6f306ca3aa7e88d64aaf059042f7f9cda026e64e5d4
```

and, under `--json`, emits one machine-readable line on stderr so a
calling agent never has to parse prose (stdout stays exactly the
merchant response body):

```
PAYMENT_RECEIPT_JSON {"amount":"0.0010000","payTo":"GDK3AVW3...DXXB","txHash":"ade2e9d1...e5d4","timestamp":"2026-07-31T00:45:35.305Z","explorer":"https://stellar.expert/explorer/public/tx/ade2e9d1...e5d4","receipt":"eyJtZXRob2QiOiJzdGVsbGFyIiwi..."}
```

Three decoding rules are worth stating, because each one is a deliberate
refusal to guess:

1. **Amounts are only trusted when unambiguous.** Receipts report either
   human USDC (`"0.0020000"`) or base units (`"20000"`), with no unit
   metadata. A bare integer is genuinely ambiguous, and guessing wrong
   misreports the payment by seven orders of magnitude — so only a value
   containing a decimal point is accepted as human USDC. Otherwise the
   field is left undefined and the caller falls back to the 402
   challenge, whose units are known.
2. **Explorer links require a well-formed hash.** The candidate must
   match `/^[0-9a-fA-F]{64}$/` before a URL is built. `reference` is the
   last-resort field and is not guaranteed to be a transaction hash at
   all — MPP Router also uses it for non-hash references. A wrong link is
   worse than no link.
3. **An undecodable receipt is not a failed payment.** Decoding is
   best-effort and yields an empty summary rather than an error, so a
   cosmetic parsing problem never reports a successful payment as a
   failure.

Covered by `scripts/smoke-test-receipt.ts`.

### What the funded run settled

Every item that was open before 2026-07-31 is now answered by capture,
not inference:

- **The real receipt shape.** One base64url segment, fields
  `method` / `reference` / `status` / `timestamp`. `reference` *is* the
  64-hex Stellar transaction hash, so the hash-format guard (rule 2)
  accepts it. The broad alias set in `decodeReceipt()` is now known to be
  speculative except for `reference` and `timestamp` — it is kept as
  tolerance for other x402 servers, not because MPP Router needs it.
- **Amount units — the question is moot.** The receipt carries no amount
  at all, so rule 1 never fires against MPP Router and the challenge
  fallback always supplies the figure. This is exactly why the decoder
  refuses to guess: had it invented a number, it would have had nothing
  to invent it from.
- **The MPP credential is accepted end-to-end.** The HMAC-bound `id`
  round-trip survives a real request — `firecrawl/scrape` returned `200`
  with scraped markdown after the retry.
- **Both dialects settle to the same destination.** Confirmed on-chain,
  not just at the challenge layer: `GDK3AVW3...DXXB` in both.

**The x402 settlement path — verified 2026-07-31, after fixing three
defects that had kept it broken since it was written.** It had never
succeeded against a v2 server. Nothing detected that, because every
failure mode returns a second `402`, which is indistinguishable from a
payment the server simply declined:

1. **Wrong header.** The credential went in `X-Payment`, the pre-v2
   convention. v2 servers read `Payment-Signature`.
2. **Wrong envelope.** The v1 shape (`scheme` + `network` at the top
   level) was sent regardless of version. v2 requires the accepted
   `PaymentRequirements` echoed back verbatim in `accepted`, and
   verifies by strict equality against it.
3. **Signature window too wide.** The client assumed a 5-second ledger
   while mainnet was closing at ~5.56s, so it signed auth entries valid
   for 60 ledgers against a verifier ceiling of 57
   (`invalid_exact_stellar_signature_expiration_too_far`). It now
   assumes a slower ledger than reality, so its window is always
   shorter than any verifier's — erring short only ever fails a
   payment, never misplaces funds.

A fourth was server-side: MPP Router's facilitator used the library's
default 50,000-stroop fee ceiling while a real mainnet SAC transfer
simulates at ~141,535, so its accepted fee range was empty and no
client could have settled regardless (fixed in mpprouter/rozo-mpprouter#21).

With all four resolved, `--dialect x402` settles end to end and returns
the merchant's response. Both dialects are now proven in production.

Reproducing the paid half — the exact invocation used, with expectations
pinned so a rewritten challenge is refused before signing:

```bash
./node_modules/.bin/tsx skills/pay-per-call/run.ts \
  https://apiserver.mpprouter.dev/v1/services/firecrawl/scrape \
  --method POST --body '{"url":"https://example.com"}' \
  --expect-pay-to GDK3AVW3YE6UL3J4WLNKBMP65KSY32YPUKIOC6PXW65XJ3LEG3YIDXXB \
  --expect-amount 0.0020000 \
  --identity <funded-identity>
```

Verified transactions from the 2026-07-31 run:

| What | Amount | Transaction |
|---|---|---|
| USDC trustline (wallet setup) | 0.5 XLM reserve | [`3ba374d9…`](https://stellar.expert/explorer/public/tx/3ba374d9f6c8a98eb59c533851f770783c318eac093095a1a6e143b719631fd3) |
| XLM → USDC swap (wallet setup) | 15 XLM → 2.5752 USDC | [`d7fde259…`](https://stellar.expert/explorer/public/tx/d7fde259db696bba23fd76e335fe3ea155e5fc2b12c8271ab08fe243d43bcf72) |
| `ipinfo/ipinfo_ip-lite` payment (MPP dialect) | $0.001 | [`ade2e9d1…`](https://stellar.expert/explorer/public/tx/ade2e9d16a45528a74d1b6f306ca3aa7e88d64aaf059042f7f9cda026e64e5d4) |
| `ipinfo/ipinfo_ip-lite` payment (**x402 dialect**) | $0.001 | [`747f5009…`](https://stellar.expert/explorer/public/tx/747f50093549643973c2243ed0afdff531ec1e1c1f98169c3c98831ace10dacc) |
| `ipinfo/ipinfo_ip-lite` payment (**x402 dialect**) | $0.001 | [`ebde6534…`](https://stellar.expert/explorer/public/tx/ebde65343d3a99a1324e0c7a94c9218a506999fd0ef79068daa3000abe37038d) |

The `firecrawl/scrape` payment ($0.002) also settled and returned scraped
markdown, but that run was made before `--json` was used, so its receipt
was not retained — the decoded receipt shown above is the `ipinfo` one.

---

## Reproducing Parts 1–3

Free, no payment, no wallet:

```bash
# 1. Find a payable route
curl -s https://apiserver.mpprouter.dev/v1/services/catalog | jq '.summary'

# 2. Capture a dual-dialect 402 (stop here — never retry with payment)
curl -s -D - -o /dev/null -X POST \
  https://apiserver.mpprouter.dev/v1/services/firecrawl/scrape \
  -H 'content-type: application/json' -d '{"url":"https://example.com"}'

# 3. Decode both challenges
npm test   # scripts/smoke-test-x402-dialect.ts asserts against these exact bytes
```

## See also

- `references/x402-exact-spec.md` — the x402 Stellar `exact` scheme.
- `references/mpp-charge-spec.md` — the MPP `stellar.charge` method.
- `skills/pay-per-call/SKILL.md` — the operational flow.
- `scripts/src/pay-engine.ts` — `parse402`, `buildRetryHeaders`,
  `validateChallenge`.
