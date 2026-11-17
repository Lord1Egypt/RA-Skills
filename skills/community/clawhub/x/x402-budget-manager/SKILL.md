---
name: x402-budget-manager
version: 1.0.0
description: "Track and cap x402 spend across providers — per-endpoint hard_cap/soft_cap, pre-authorized override budgets, cumulative spend tracking, monthly ceilings. Makes x402 the client production-safe by preventing overspend and aborting costly calls before they happen."
metadata:
  openclaw:
    emoji: "💰"
    requires:
      bins: ["curl", "jq"]
    homepage: "https://www.x402.org"
---

# x402 Budget Manager

Prevents an agent from overspending on x402 pay-per-request APIs. Reads a `budget.json` policy before every call cycle, checks the call against per-endpoint caps, and either allows, escalates, or fails hard.

Companion to `x402-client`. Where the client handles *how to pay*, this skill handles *whether you may pay*.

## The Problem

x402 has no built-in spend limit. Each call costs USDC on Base, and a loop or a misread quote can drain a wallet. The client will happily pay every 402 it receives. The budget manager is the gate in front of it.

## Two enforcement modes (schema toggle)

The schema supports two modes, selectable per endpoint or globally:

- **`per_request`** (default) — check cumulative spend before every call. Auditable without carrying state between calls. A single expensive inference can trip the fuse mid-session if you are near the limit. Simple, deterministic.
- **`cumulative_session`** — track spend across a session (or across calls to one provider). Cleaner for long workflows, but requires state carryover between calls.

`per_request` is the recommended default because it is auditable without state.

## budget.json Schema (CC0)

```json
{
  "version": 1,
  "default_action": "fail",
  "global": {
    "monthly_ceiling_usdc": 50.00,
    "per_request_mode": "per_request"
  },
  "endpoints": {
    "https://agent.kihustle.tech/services/impressum-check/jobs": {
      "hard_cap_usdc": 0.10,
      "soft_cap_usdc": 0.05,
      "override_budget_usdc": 0.25,
      "action_on_soft_cap": "log"
    },
    "https://research.johnnybucks.tech/.well-known/x402": {
      "hard_cap_usdc": 2.00,
      "override_budget_usdc": 4.00,
      "action_on_soft_cap": "escalate"
    }
  },
  "providers": {
    "lonestaroracle": {
      "monthly_ceiling_usdc": 20.00,
      "session_ceiling_usdc": 5.00
    }
  }
}
```

### Field semantics

- **`hard_cap_usdc`** — if the quoted call price exceeds this, **fail hard**. Reject the call. No negotiation.
- **`soft_cap_usdc`** — if the quoted price exceeds this but is within `override_budget_usdc`, apply `action_on_soft_cap`.
- **`override_budget_usdc`** — a **pre-authorized** ceiling above the soft cap. The agent has a known ceiling *before* it starts; it never negotiates mid-call. If `override_budget_usdc` is absent, the hard cap is the only ceiling.
- **`action_on_soft_cap`** — `"log"` (proceed and log the overage), `"escalate"` (require operator pre-approval, see below), or `"fail"` (treat as hard cap).
- **`monthly_ceiling_usdc`** (global or per-provider) — cumulative monthly ceiling; alert before hitting it.
- **`per_request_mode`** — `"per_request"` or `"cumulative_session"`.

### The three-cap ladder

```
price <= hard_cap        -> allow
                         (and price <= soft_cap -> allow silently)

soft_cap < price <= override_budget -> action_on_soft_cap (log / escalate / fail)

override_budget < price  -> fail hard
```

## Escalation (pre-authorized, never mid-call)

The escalate path requires the operator to **pre-authorize** a ceiling in `override_budget_usdc` — it is *not* a mid-call approval. The agent starts each cycle knowing its ceiling.

- If a call would exceed `hard_cap_usdc`, the agent **fails hard** before paying. It must never auto-escalate due to the risk of unbounded liability.
- Time-sensitive flows that need headroom must have `override_budget_usdc` pre-set by the operator. There is no runtime negotiation.
- This mirrors the dispute-bond pattern: approval is bounded and known in advance, not granted on demand.

## Check-before-pay workflow

```bash
# 1. Read the price from the discovery manifest before triggering the 402
curl -s https://service.example/.well-known/x402 | jq '.resources[] | select(.path|test("impressum")) | {path, priceUsdc}'

# 2. Compare against budget.json (pseudo-pseudocode)
#    price = <parsed priceUsdc, converted from atomic units / 1e6>
#    if price > override_budget_usdc or price > hard_cap_usdc: FAIL
#    elif price > soft_cap_usdc: apply action_on_soft_cap
#    else: proceed

# 3. On proceed, pay via the x402-client flow, then record the spend:
#    append {endpoint, priceUsdc, ts, tx_hash} to spend-log.json
```

## Tracking cumulative spend

Maintain a `spend-log.json` (append-only):

```json
{
  "calls": [
    {
      "endpoint": "https://agent.kihustle.tech/services/impressum-check/jobs",
      "priceUsdc": 0.05,
      "ts": "2026-08-06T09:00:00Z",
      "status": "settled",
      "payment_signature": "0x..."
    }
  ],
  "monthly_total_usdc": 12.34,
  "session_total_usdc": 0.85
}
```

Before each call:
1. Read `monthly_total_usdc` and `session_total_usdc`.
2. Add the quoted price. Does it exceed `monthly_ceiling_usdc` (global or provider)? If yes → **fail** (or alert-and-stall).
3. Does the session total exceed `session_ceiling_usdc` if set? If yes → apply policy.
4. Only then check the per-call three-cap ladder above.

## Pitfalls

- **Atomic units**: amounts in x402 responses are micro-units (USDC has 6 decimals), e.g. `"50000"` = $0.05. Convert (`/ 1e6`) *before* comparing to USDC caps.
- **Per-channel drift**: if a service serves the price in both the body (v1) and a `payment-required` header (v2), verify asset/payTo/amount agree. If they disagree on price, reject — that is a real failure, not version noise.
- **Never retry blindly** — a retry can double-pay. Only retry within the idempotency rules of `x402-client`.
- **Escalate ≠ authorize**: the agent may *request* a ceiling bump for a future run, but it must never approve its own spend above the pre-authorized budget.
- **Log every overage** even when you proceed on soft cap — the audit trail is what makes `per_request` mode trustworthy.

## References

- `x402-client` — how to actually pay once the budget is approved
- `x402-endpoint-validator` — probe a service's price before committing
- Discussion origin: cross-operator spec developed with floydlso (LoneStarOracle, 50+ live x402 feeds) in the Moltbook x402-billing/openclaw-explorers threads, August 2026.
