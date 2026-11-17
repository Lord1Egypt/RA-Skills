# Endpoint inspection

For an unpaid check, call `preflight_endpoint` or `POST https://scvd.store/api/preflight/v1`
with `{"url":"https://merchant.example/paid"}`. Preserve named failures,
observation time and coverage. Include the returned `inspection.observed_at` timestamp
in the final answer alongside the verdict; if it is missing, explicitly say
the observation time was not supplied. A passing probe establishes neither settlement
nor delivery and grants no permission to spend. Read [MPP](mpp.md) when present.
The paid options below require the [purchase rules](purchases.md).

Read the returned `inspection` block for reachability, the observed protocol
set, unverified advertised terms, structural findings and gaps. Its signature
state is `not_checked`. The top-level `verdict` remains x402-specific; a
successful inspection is not a payment-readiness verdict. Older reports may
lack this block: keep their actual fields and report missing coverage, without
inventing a protocol result or substituting download time for observation time.
For a package client, use the [installed capability checks](packages.md).

## The verification tier — what the store observes about OTHER people

This is the half the earlier version of this bundle did not mention,
and it is now the larger half. Everything here is an observation of
somebody else's endpoint, artifact or payment, signed by this store's
key rather than by the party it is about — which is the whole point:
a claim you sign about yourself is worth what your reputation is
worth, and a claim we sign about you can be checked by a third party
without trusting either of us.

Every one of these is an artifact class on
`https://scvd.store/attestation`, with `trust_model`, what the
signature covers, and — the load-bearing field — what it does NOT
prove.

- **Free preflight.** `POST https://scvd.store/api/preflight/v1` runs
  the published, versioned conformance battery against any x402
  endpoint and returns the named checks that passed and failed. No
  wallet, no charge, no signature. The paid audit reuses the readiness
  battery; additional discovery-surface observations have their own scope
  and gaps.
- **`service_audit`** ($5) — a signed, dated, point-in-time verdict on
  one endpoint: `ready` / `not_ready` / `unreachable`, with the failing
  checks NAMED rather than collapsed into a score. Carries an
  `evidence_hash` bound into the purchase certificate, so
  `/api/verify` answers for the observation and the receipt at once.
- **`good_buyer`** ($0.99) — not what the door serves but what your
  client would DO with it: the accepts recorded verbatim, a stock
  x402 client's selection replayed over them, and the spend-control
  case where the client was configured with nothing. Free and
  unsigned at `/api/before-you-pay/v1`.
- **`onpage_audit`** ($3) — what one page served a machine reader at
  one moment: title, description, canonical, robots, structured data.
  Read from the HTML as served — scripts never run, and the report
  names that blind spot on itself rather than letting you assume it
  looked. Free and unsigned at `/api/onpage/v1`.
- **`spot_check`** ($0.001) — this store's own books on one host,
  signed: rounds, verdicts as recorded, coverage, gaps with reasons.
  No request is made to the host. A host we have never met returns
  `not_observed`, and that is the answer rather than an error.
- **`conformance_watch`** ($5) — the same battery on a schedule, with
  `drift_detected` computed as set arithmetic over sorted failed-check
  sets, so a reader can recompute the verdict rather than trust it.
- **`launch_check`** ($5) — the one observation no probe can
  substitute: a real EIP-3009 authorization from the store's declared
  field wallet, presented at your till, settled or refused, the whole
  walk signed stage by stage. We pay at most $0.05 at your door.
- **`opening_day`** ($9) — the merchant's opening day in one purchase:
  the launch check's real walk of your till, then seven daily signed
  conformance passes on the same door, then your passport page, under
  one certificate at one URL. Bought apart, $10 and a receipt each. It
  ends after the week and never renews itself.
- **`provenance_check`** ($5) — The Company an Address Keeps: which
  doors advertised a receiving address, in which signed weeks, with
  verdicts and drift, the snapshot digest behind every line. Delivered
  to you, never published, never a score. Your own address is free
  once proved, and the free answer ends with a consent offer.
- **`signature_agent_card`** ($0.99) — the audit's point-in-time shape
  aimed at a Web Bot Auth key directory: the document fetched once,
  every check named, the proof-of-possession signature verified rather
  than noticed, the readout signed and bound into the certificate.
  About the document at one moment, never the operator behind it. The
  free desk is `POST /api/bot-auth/check`; and the store eats its own
  cooking — our outbound probes sign their requests the same way,
  with our directory at
  `https://scvd.store/.well-known/http-message-signatures-directory`.
- **`settlement_attestation`** ($0.004) — a neutral party reads one
  on-chain settlement and signs what it saw.
- **`attestation_bundle`** ($0.05) — a sheaf of settlement
  observations under one signature, with a digest over the whole set
  bound into the certificate.
- **`settlement_reconciliation`** — authorized versus settled, for
  x402's `upto` and `deferred` schemes. The ceiling is attested as
  **observed** only where it is derivable from the chain (an Approval
  in the same receipt, or an EIP-3009 authorization whose value is
  fixed inside the payer's signed digest) and as **declared**
  otherwise. `cap_observed` is its own signed field, never a footnote,
  because signing a cap the buyer handed us would put this store's key
  on the buyer's arithmetic.
- **`bitcoin_anchor`** — your digest, timestamped into Bitcoin via
  OpenTimestamps, bound into a certificate.

### The evidence layer (3.8.0, 2026-08-31)

The observations above compose into standing surfaces an agent can
route on without buying anything:

- **Endpoint passports** — `GET https://scvd.store/passport/{host}`:
  one signed, EXPIRING object per ready-side host — latest census
  verdict, observation history with its gaps counted, and a
  freshness state you act on mechanically (`fresh / aging / expired /
  broken / indeterminate`; refuse expired passports — the arithmetic
  is printed on the payload). Free. Failing hosts get a reasoned
  refusal, never a public row. Each passport carries a free
  embeddable `chip_url` (an SVG that decays with the same freshness
  arithmetic — it cannot become stale wallpaper).
- **`passport_refresh`** ($1) — the census's own probe pointed at
  your door RIGHT NOW, folded into your passport wherever it is
  newest. Payment buys the check, never the grade: a broken finding
  refreshes to a broken passport and a dark chip, and the shelf says
  so before you pay.
- **Verify anyone's receipt** — `POST
  https://scvd.store/api/verify-receipt` with any issuer's signed
  artifact: a SIGNED verdict back (`valid | invalid | expired |
  insufficient_evidence | unsupported | indeterminate`), every check
  named, everything NOT checked stated. Stateless and free.
- **The obstacle course** — `GET https://scvd.store/api/practice`:
  doors that fail in deliberate, named, deterministic ways (plus one
  well-formed dust offer you should parse and still refuse). Rehearse
  failure handling from CI, free, before it costs you at a
  stranger's door.
- **The trust panel** — `https://scvd.store/trust`: the signing key
  and its Bitcoin-anchored history, the five-level assurance ladder
  (what a valid signature CLAIMS per level), and real house-bought
  sample artifacts to inspect before ever paying.
- **`trust_profile`** ($21) — a STANDING page for your endpoint at
  `https://scvd.store/profiles/{host}`: your live passport, the chip
  and the signed history at one URL, 30 days a purchase, renewable
  (renewing early extends the term). Ready-side hosts only at the
  door; the page derives live from the same corpus, so a broken week
  shows broken. The index lists in-term ready-side hosts only.

The claims door's challenge is now standard **SIWX (CAIP-122)** —
any SIWE library signs it natively; the flow is unchanged.
