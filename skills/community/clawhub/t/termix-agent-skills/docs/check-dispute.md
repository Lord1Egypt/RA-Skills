# Check Dispute

Read dispute status / verdict / settlement progress on the Termix Platform
(dev-v2 dispute model: evidence phase → evaluator panel verdict → optional
arbitration → settle). Dispute reads are **participant-scoped** — use
`--auth session` with a wallet involved in the dispute.

See [env.md](env.md) for base URL and auth. Provider-side actions (submit
evidence, settle) live in [`provider-dispute.md`](provider-dispute.md).

---

## Steps

### 1. Resolve the dispute

By dispute ID:

```bash
node scripts/aacp-api.mjs GET /api/v1/disputes/<disputeId> --auth session
```

From an order:

```bash
node scripts/aacp-api.mjs GET /api/v1/orders/<orderId>/dispute --auth session
```

Public read-only resolution view (share/inspect):

```bash
node scripts/aacp-api.mjs GET /api/v1/resolutions/<disputeId> --auth session
```

If not found, report "No dispute for this order/ID" and stop.

### 2. Display overview

Key fields of the dispute DTO (print the JSON and summarize):

| Field | Notes |
|---|---|
| `id` | dispute id (cuid) |
| `status` | see status flow below |
| subject | order / campaign-slot reference |
| evidence deadlines | evidence phase window |
| evaluator panel + votes | panel seats, per-seat verdicts once revealed |
| `evaluatorFeeAmount` | evaluator panel cost (order budget × on-chain evaluatorFeeBps) |
| `arbitratorFeeAmount` | only present once escalated to arbitration |
| final verdict / settlement tx | after FINAL_VERDICT / SETTLED |

**Status flow:**

`OPEN` → `EVIDENCE_PHASE` → `EVALUATOR_VERDICT` → `DISPUTE_WINDOW`
→ (optional `ARBITRATION_REVIEW`) → `FINAL_VERDICT` → `SETTLED`

### 3. Interpret

| Status | Meaning |
|---|---|
| `EVIDENCE_PHASE` | Both sides upload evidence (`/disputes/:id/evidence/*`) |
| `EVALUATOR_VERDICT` | Evaluator panel is scoring |
| `DISPUTE_WINDOW` | Loser may accept (`/disputes/:id/accept`) or escalate to arbitration (`/disputes/:id/arbitration`) |
| `ARBITRATION_REVIEW` | Arbitrator reviewing; rules via `/disputes/:id/arbitration/verdict` |
| `FINAL_VERDICT` | Outcome fixed — waiting for on-chain settle (last lifecycle actor settles) |
| `SETTLED` | Funds distributed on-chain |

If a phase deadline passed without action, anyone involved can prepare the
timeout path: `POST /api/v1/disputes/:id/finalize-after-timeout/prepare`.
