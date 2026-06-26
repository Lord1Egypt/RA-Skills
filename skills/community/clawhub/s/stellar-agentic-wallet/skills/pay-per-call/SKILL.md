---
name: pay-per-call
description: Call a 402-gated HTTP API and pay automatically with Stellar USDC. Handles the 402 → sign → retry loop for both MPP Router services and x402 facilitators. Triggers on "call this paid API", "pay and fetch <url>", "summarize via parallel.ai", or after `discover-mpprouter` picks a service. Reads 402 challenges in either x402 format (X-Payment header) or MPP format (mppx Credential) and signs with the same underlying Stellar key.
---

# pay-per-call

The "execute" step of the wallet agent. Call a paid HTTP endpoint, handle the 402 response, sign, retry, return the result.

## When to trigger

- After `discover-mpprouter` returns a service to call
- "Call <url> and pay with stellar"
- "Fetch this paid endpoint"
- "Summarize https://stripe.com/docs using parallel.ai via mpprouter" (chain: discover → pay-per-call)

## Not for

- Unpaid HTTP calls — just use `fetch`
- Cross-chain payments — use `send-payment` or `bridge`
- Pure SDK-level signing without HTTP — use the `client.ts` template directly

## Prerequisites

Before calling a service, you need TWO things: the HTTP method and
the request body shape. The MPP Router **forwards both as-is** — it
does not transform, validate, or guess.

**HTTP method — do NOT default to GET.** Most MPP Router services are
POST-only. The catalog `method` field is authoritative; pass it via
`--method`. Calling the wrong method returns 405 with `allowed_methods`
in the body (older deployments may return 400 "Unknown public service
route" — same root cause). The script auto-recovers from 405 once,
but the right move is to read the catalog up front.

**Request body shape:**
- **If you already know the schema** (e.g. from the user's prompt or
  prior context) → proceed directly.
- **If you don't** → run `discover` first. The service's `docs` field
  points to upstream API documentation. Read `docs.llms_txt` (preferred)
  or `docs.api_reference` to learn the correct request shape before
  paying. Sending a malformed body wastes the payment.

## Flow

1. First attempt: plain POST/GET to the URL.
2. Expect `402 Payment Required`. Parse the challenge in this priority order:
   1. **MPP dialect** — `WWW-Authenticate: Payment request="<base64>"` header.
      Values may be quoted or unquoted per RFC 7235; we accept both.
   2. **x402 v2 dialect** — `Payment-Required: <base64>` response header
      carrying `{ x402Version, accepts: [PaymentRequirements] }`.
   3. **x402 legacy** — same envelope but in the JSON response body
      (older x402 servers).
3. Both formats produce the same inner XDR (sponsored SAC transfer). We sign once.
4. Wrap the XDR in the envelope matching the challenge:
   - x402 → base64 JSON in `X-Payment` header
   - MPP → `Authorization: Payment <credential>` header
5. Re-POST/GET with the payment header attached.
6. Return the response body + any `Payment-Receipt` header for auditing.

Before signing, the script checks that the selected payer wallet exists on
the target Stellar network, has a Classic USDC trustline, has enough USDC for
the challenge amount, and is not below XLM reserve. This catches wrong-wallet
failures before any payment credential is signed.

### Dialect priority — when a server emits multiple

MPP Router is the canonical example: a single 402 response includes
BOTH the MPP `WWW-Authenticate` header AND the x402 `Payment-Required`
header, with **different `payTo` addresses** for each dialect. The
addresses are HMAC-bound to the challenge, so you can't mix them —
pay the MPP address with an MPP credential, or the x402 address with
an x402 envelope. Pay the wrong address and the server rejects the
request while you still eat the on-chain fee.

This skill always tries MPP first and uses the MPP address if that
header is present. The x402 `Payment-Required` header is only used
when the MPP header is absent. If you need to force the x402 path
for a server that emits both, use a different client — this skill
doesn't expose a dialect override.

## How to run

```bash
# MPP Router service (discovered via discover skill)
npx tsx skills/pay-per-call/run.ts \
  "https://apiserver.mpprouter.dev/v1/services/parallel/search" \
  --body '{"query": "Summarize https://stripe.com/docs"}' \
  --method POST \
  --identity mpp-mainnet-payer

# x402 facilitator
npx tsx skills/pay-per-call/run.ts https://some-x402-api.example/endpoint

# Include JSON output mode
npx tsx skills/pay-per-call/run.ts <url> --body '{...}' --json

# Save payment receipt to file
npx tsx skills/pay-per-call/run.ts <url> --receipt-out receipt.json
```

## Async jobs (202 responses)

Some services (e.g. StableStudio video generation) are async — the paid
request returns `202 Accepted` with a `jobId` instead of an immediate
result. When this happens:

1. The MPP Router stores a job auth record binding the job to your
   Stellar address and returns headers:
   - `X-Job-Poll-Url` — the full URL to poll
   - `X-Job-Id` — the job identifier
2. This skill automatically polls the `X-Job-Poll-Url` every 5 seconds
   using the same Stellar credentials for identity verification.
3. Polling is **free** — no additional USDC is charged.
4. Job results are available for **24 hours** after creation.
5. The poll loop times out after 10 minutes. For longer jobs, re-run
   with the poll URL manually.

If there is no `X-Job-Poll-Url` header, the 202 body is printed as-is.

## Safety

- ✅ **Credentials are single-use** — if the first retry fails, the credential is burned. Don't blindly re-retry; start fresh.
- ✅ **Every mainnet payment prompts by default.** No silent auto-pay out of the box. After you confirm the first payment, the script offers to save an autopay ceiling (e.g. $0.10) so future payments at or below that amount go through without a prompt. The ceiling is stored as a `# autopay-ceiling-usd:` comment inside the secret file itself, bound to the wallet. Delete the line to revoke.
  - `--max-auto <usd>` — one-shot override for this call only; does not touch the saved ceiling.
  - `--no-autopay` — force a prompt for this call even if a ceiling is saved.
  - `--yes` — skip confirmation entirely (dangerous on mainnet; use only in trusted automation).
  - Every auto-paid call still logs `[autopay] $X USDC ...` to stderr so there is a trail.
- ✅ **Challenge validation (opt-in).** Pass `--expect-pay-to <G...>`, `--expect-amount <USDC>`, and/or `--expect-asset <SAC>` — typically piped from `discover --pick-one --json` via its `expect` block — and the script refuses to sign a 402 whose recipient, price, or asset drifts from the catalog. Without these flags, the server's challenge is trusted; a hostile 402 can set any recipient. Treat `--expect-*` as mandatory in production.
  - `--expect-amount-tolerance <fraction>` — allow small drift (e.g. `0.01` = 1%) for services that quote ranges.
- ❌ **Don't reuse a credential** — the HMAC binding to amount/currency/recipient is the router's defense against replay.

## Example: full MPP Router flow

```bash
# Discover — capture the service + its catalog-asserted payment
# expectations so pay-per-call can refuse a hostile 402.
SERVICE=$(npx tsx skills/discover/run.ts --query "web search" --pick-one --json)
URL="https://apiserver.mpprouter.dev$(echo "$SERVICE" | jq -r '.public_path')"
EXPECT_AMT=$(echo "$SERVICE" | jq -r '.expect.amount_usdc // empty')
EXPECT_TO=$(echo "$SERVICE" | jq -r '.expect.pay_to // empty')

# Call
npx tsx skills/pay-per-call/run.ts "$URL" \
  --body '{"query": "Summarize https://stripe.com/docs"}' \
  --method POST \
  ${EXPECT_AMT:+--expect-amount "$EXPECT_AMT"} \
  ${EXPECT_TO:+--expect-pay-to "$EXPECT_TO"}
```

## Env vars used

- `--identity` or `--secret-file`, plus `--network`, `--rpc-url` — for signing
- `--asset-sac <address>` — default asset if challenge doesn't specify one
