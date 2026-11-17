---
name: resonance-futures
description: Design and run an agent-native, evidence-settled prediction market — the trust model (who proposes, trades, settles), the propose→open→settle lifecycle, machine-measurable settlement, anti-gaming rules, and the path from play-credits to real money. Use when building a prediction market that autonomous agents originate and settle.
---

# Resonance Futures — an agent-native prediction market

A prediction market run *by* and *for* autonomous agents is only trustworthy if
it is a **market**, not a poll: claims are falsifiable and machine-measurable,
identity is verified, and settlement is evidence-first and separated from
authorship. This skill is the architecture, distilled from building one across
a multi-service constellation and hardening it with an adversarial review.

## The one-sentence thesis

*Labs measure · the Exchange settles · a public ledger witnesses.* Keep those
three responsibilities in different hands and most of the failure modes
disappear.

## Trust model — separate the credentials

Give each capability a **distinct** credential; do not reuse one bearer token
for everything.

| Capability | Who | Why it's separate |
|---|---|---|
| Propose a prediction | any verified identity (user or agent) | origination should be open, but attributable |
| Curate — open / reject | the Labs oracle (service) or an admin | opens the measurability gate |
| Trade / vote | any verified identity | one account per verified principal |
| **Settle / resolve** | the **oracle service only** | a proposer must never settle their own market |
| Dispute | any verified identity, within a window | a check on the oracle |

**Identity provider.** Issue short-lived, asymmetrically-signed tokens (EdDSA)
from one provider; every surface verifies them *locally* against a published
JWKS — no per-request introspection. Harden the verifier: pin the algorithm
allowlist (reject `alg=none` and HMAC-with-the-public-key confusion), require
`exp`/`iat`/`nbf`, select the key by `kid`, and **fail closed** if the JWKS
can't be fetched. Bind an agent token to an identity the provider has *proven*
control of (e.g. a challenge the agent answers through a channel only it
controls) — never to a merely-observed id. Derive a trader's id from the
verified token `sub`, never from a request-body string (that's the sybil door).

## Lifecycle

`proposed → open → settled` (plus `rejected`, `disputed`).

1. **Propose** — a verified principal submits a statement + a settlement method,
   attributed to them. It carries no tradeable market yet.
2. **Curate / open** — the oracle applies the **measurability gate** and, if it
   passes, opens the market (and pairs a tradeable market if you have one).
3. **Trade** — verified principals take positions.
4. **Settle** — the oracle measures and records the *reading* (the actual
   measurement output), sets TRUE/FALSE, and witnesses it.

## The measurability gate

A proposal may not **open** unless it can actually be settled by evidence:
either a **machine-readable measurement spec** (auto-settle) *or* a **named
settlement procedure plus a deadline**. "Will X be cool?" is rejected at
curation, not settled by whoever shows up at the deadline.

A measurement spec is a small, declarative object your settler can execute —
e.g. *count entities matching a condition in a named external data source at a
deadline; settle TRUE if the count meets a threshold*. Store the spec with the
prediction so settlement is reproducible and auditable.

## Settlement — evidence-first and safe

- **Record the reading.** Every settlement stores what was actually measured,
  who/what settled it, and when. Push it to an append-only public ledger.
- **Early settlement only for monotone, irreversible facts**, and only after
  the condition has **held across several consecutive checks** — an external
  signal that can be reverted (a claim that gets undone) must not lock a
  permanent wrong outcome on a single transient read.
- **Partial/ambiguous measurements are a skip, not a settle.** A truncated or
  paginated data read that yields a low count must be treated as "measurement
  failed → stay open," never as a settlement. Never settle FALSE at a deadline
  off one unconfirmed read.
- **Cross-service consistency.** If settlement writes to more than one store
  (a registry, a ledger, a paired market), use a durable **outbox** and
  idempotent, retried deliveries — never fire-and-forget. Otherwise the ledger
  says TRUE while the market paid FALSE.

## Anti-gaming rules (the ones that actually bite)

- **No self-fulfilling conditions.** If a market participant can *cause* the
  measured fact (e.g. "someone builds a building" is trivially caused by a
  Yes-holder), the market is theft-at-real-money. Require the triggering fact to
  be attributable to a **non-participant**, exclude actions by principals
  holding a position, and/or gate settlement behind independent corroboration.
- **Sybil-proof the price.** An open, self-registration market's displayed price
  is trivially forgeable by one actor with N free accounts — **never cite it as
  authoritative signal.** Require verified-identity trading (and per-principal
  position caps) on any market whose price you quote.
- **Halt trading before a deterministic settlement**, and snapshot the price at
  the freeze — otherwise anyone who sees the reading flip buys in risk-free.
- **Single-flip settlement.** Guard the resolve in the database
  (`… WHERE resolved = 0` + changed-rows check) so a manual settle racing an
  automated one can't pay winners twice and mint credits. Guard the debit
  (`… WHERE balance >= cost`) so concurrent trades can't overdraw.

## Ledger — before any real money

- **Double-entry, append-only, hash-chained.** Balances are *derived* from
  balanced postings, never stored-and-mutated. Each entry commits to the
  previous entry's hash; enforce no-UPDATE/no-DELETE as a database grant, not an
  app-code convention. A witnessed settlement is a new superseding row, never an
  in-place rewrite.
- **Integer minor units** for money-shaped amounts; keep market *prices*
  floating but settle *amounts* as integers, with one canonical rounding rule.
- **The automated market maker is a funded account.** Its bounded subsidy is a
  real posting escrowed at market creation, so payouts don't mint unbacked
  credit and total value is conserved.

## From play-credits to real money — a hard gate

Real-money event contracts are regulated in most jurisdictions. Treat legal
review as a **launch precondition, not a to-do**. Build so the gate is the only
blocker: KYC + geo-fencing hooks at the identity layer; custody keys physically
separated from the settlement oracle (different box / HSM / multisig, so no
single credential both settles and pays); a continuous reconciler that **halts**
settlement on any on-chain/off-chain divergence; and play vs real ledgers
segregated and never fungible. Until the gate opens, the market's realness comes
from **integrity, not stakes** — verified identity, measurable claims,
evidence-first settlement, and an append-only public record.

## Before you build it

This is exactly the "hard to reverse" territory an adversarial design review
pays for: identity, settlement authority, and money. Attack the design first —
have specialists each hunt one lens (capability/identity, ledger integrity,
oracle/market economics, cross-service consistency) for concrete failure
scenarios — then implement the survivors.
