# SoloMission Platform — Stuck Mission Recovery

These states arise when a previous session's monitoring loop did not finish its work
(e.g. the agent crashed mid-flow). They are not expected during normal operation:

- **`claim_refund`** should have run immediately after `settle_mission` returned `status: "refundable"`.
- **`emergency_refund`** should never be needed if the loop settled before `settlement_deadline`.
  Two exceptions are by design: a lottery whose entropy was not recorded in time (settle returns
  `entropy_expired`), and a mission that hired nobody and was never finalized. Both are below.

If you see these at session start, resolve them now. Only the Sponsor wallet that funded a
mission can get its money back; the platform cannot do it for you.

`requires_sponsor_action` is set by a background job that runs every ~5 minutes and
reads the same `onchain_status`/`settlement_deadline` fields already in your work file.
Use it only in the [Session-Start Scan](#session-start-scan-quick-reference) below. For
any mission in your own work file, trigger directly from your own tracked fields
instead — never poll this flag for it:

- **`emergency_refund`** — trigger on `now > settlement_deadline`, every tick.
- **`claim_refund`** — trigger the instant `settle_mission` returns `status: "refundable"`, same tick.

---

## One procedure for every refund: ask, then act

All three recovery routes (`cancel`, `emergency_refund`, `claim_refund`) go through the same
two calls, and the backend tells you which one is legal. Do not guess from the flag or from
your own clock: ask.

**MCP:**

```
refund_solana_mission { mission_id: "<MISSION_ID>" }
→ { available_actions: [...], why_not_claim_refund: "...", note: "..." }

refund_solana_mission { mission_id: "<MISSION_ID>", action: "<one of available_actions>" }
→ { refunded: true, verified: true, onchain_status: "cancelled" | "refunded",
    vault_remaining_raw: "0", signature: "..." }
```

**REST:**

```
POST /agent/solana/missions/:id/refund-transaction
  { "action": "<cancel|emergency_refund|claim_refund>",
    "sponsor_wallet": "<base58>", "sponsor_token_account": "<base58>" }
  → 200 { action, task_id, transaction_base64, ... }            action is legal
  → 409 { error, message, available_actions: [...] }            action is not legal now

(verify the transaction, then sign it locally — see solana-wallet.md, "Raw REST path")

POST /agent/solana/missions/:id/confirm-refund
  { "signed_transaction": "<base64>", "action": "<same action>" }
  → 200 { mission_id, action, signature, onchain_status, vault_remaining_raw }
```

`sponsor_token_account` is the sponsor's token account **for the mission's own mint**
(`token_address` on `GET /agent/missions/:id`).

How to choose, from `available_actions`:

| `available_actions` contains | Do | Result |
|---|---|---|
| `claim_refund` | `claim_refund` | unspent remainder returns; mission `refunded` |
| `emergency_refund` | `emergency_refund` | whole budget returns; mission `cancelled` |
| `cancel` (and you mean to stop the mission) | `cancel` | whole budget returns; mission `cancelled` |
| nothing | wait — see below | |

An empty list means no route is legal yet. That is the escrow program's rule: once hiring
closes (`qualify_deadline`), `cancel` is gone, and `emergency_refund` only opens after
`settlement_deadline`. The program itself enforces the cancel cut-off (`TooLateToCancel`), so a
`cancel` built just before `qualify_deadline` that lands after it fails on chain, and
`confirm-refund` returns 409. Record `settlement_deadline` and ask again once it has passed.

**Check the result.** `vault_remaining_raw` should be `"0"`: the program empties the vault on
all three paths. Anything else means something other than what you asked for executed; stop
and report it to the operator. If the tool returns `refused_to_sign: true`, nothing was
signed and nothing moved: report the `problems`, do not retry blindly. If it returns
`refunded: false` with `rejected_by`, read who refused: `"client"` (the tool itself, e.g. a
`cancel` after `qualify_deadline`; nothing was built), `"backend"` (409 with
`available_actions`) or `"chain"` (the escrow program; `program_error` names the error, e.g.
`TooLateToCancel`, and says what to do).

---

## `requires_sponsor_action: "emergency_refund"`

**Situation:** `settlement_deadline` passed without a `settle_mission` call. Funds are
locked in the escrow vault with `onchain_status` `funded` or `qualified`.

**Trigger:** `now > settlement_deadline` — act immediately, do not wait for the flag.

Run the procedure above. Expect `available_actions: ["emergency_refund"]`; run it.

If `available_actions` is `["claim_refund"]` instead, the mission actually settled: run
`claim_refund`. If the emergency refund is rejected on chain (`rejected_by: "chain"`, or
`confirm-refund` returns 400 over REST), check `program_error`: `TooEarlyForEmergencyRefund`
means the program's clock hasn't passed `settlement_deadline` yet, so retry shortly. Otherwise,
`available_actions` is computed from the platform's record, which can lag the chain. Call
`get_mission`, ask again, and if the answer doesn't change, stop and report the mission id to
the operator rather than retrying.

Result: mission status → `cancelled`, the whole budget back in the Sponsor's token account.

---

## `requires_sponsor_action: "claim_refund"`

**Situation:** the mission settled but fewer than `max_humans` qualified (or none did).
Unused budget is sitting in the escrow vault.

**Trigger:** mission `status === "refundable"`. Act now.

Run the procedure above with `action: "claim_refund"`.

Result: mission status → `refunded`, unused budget back in the Sponsor's token account.
Check `settlement_outcome` on the mission to see whether anyone was paid
(`completed_refundable`) or nobody qualified (`no_payout_refunded`).

The flag clears on the background job's next run (up to ~5 minutes) after the refund lands.

---

## Lottery settle returned `entropy_expired`

**Situation:** a lottery that needs a draw was finalized, but nobody recorded the entropy slot's
entry within about 512 slots (~3.4 minutes), so the draw can never happen on chain (see
`solana-wallet.md`, *Where a lottery's randomness comes from*). There is no way to commit a new
slot. `onchain_status` stays `qualified` until `settlement_deadline`.

**Action:** stop calling `settle_mission`. Record `settlement_deadline`; once it has passed, run
the procedure above and expect `emergency_refund`. The whole budget comes back, and the
participants are not paid, so tell the operator.

(`entropy_not_available` is different: the committed slot hasn't been produced yet. Retry settle
in a few seconds.)

---

## Mission hired nobody, and hiring has closed

**Situation:** `onchain_status` is `funded`, `qualify_deadline` has passed, and no participant is
`hired` or still `applied` (the reconciler would hire an applicant). `cancel` is no longer
available, even with nobody hired, and the platform's reconciler won't finalize a mission with
nobody hired, so left alone the mission waits for `settlement_deadline`.

**Action**, either:

- **Settle it with zero payout now:** `finalize_qualification` with an empty
  `qualified_human_uids` list, then `settle_mission`. The mission becomes `refundable`
  (`settlement_outcome: "no_payout_refunded"`); `claim_refund` returns the budget less the
  platform fee (`floor(budget × fee_bps / 10000)`, `0` on devnet today). Finalize must still run at
  least `max(60 s, min_review_window)` before `settlement_deadline`.
- **Or wait** for `settlement_deadline` and `emergency_refund` the whole budget, with no fee.

The same applies to a `media_review` mission where nobody finished a review: finalize it with `{}`.

---

## Mission is `expired` (no flag)

`expired` means one of these — **check which before assuming no action is needed:**

| Scenario | Funds in escrow? | Action |
|---|---|---|
| Off-chain mission whose `expires_at` passed | None | No action required |
| On-chain mission refunded in a prior session (`onchain_status` `cancelled` or `refunded`) | Already returned | No action required |
| On-chain mission past `settlement_deadline` with `onchain_status` `funded` or `qualified` | **Still locked** | Run the procedure; expect `emergency_refund` |
| On-chain mission with `onchain_status` `refundable` | **Still locked** | Run the procedure; expect `claim_refund` |

If `onchain_status` is `funded`, `qualified` or `refundable` on an `expired` mission, the
background job has not flagged it yet — act immediately without waiting for the flag.

---

## Mission is still `pending_funding`

Usually nothing is escrowed yet. An unfunded mission is cancelled automatically 24 hours after
creation: that is `funding_params.expires_at` in the create response (not the mission's own
`expires_at`, which is when hiring closes). Before cancelling, the background job checks the
chain, and activates a mission that was funded but never confirmed.

- **Want to go ahead, hiring window still open** (`hiring_closes_at` in the future): fund it now
  with `fund_solana_mission`, which requests a fresh transaction each call. Do not resubmit an
  old signed transaction: its blockhash and `task_id` are stale.
- **Don't want it, or the hiring window already closed:** do not fund it. Cancel it with
  `cancel_mission` (`POST /agent/missions/:id/cancel`), or let the 24-hour expiry do it, and
  create a new mission if you still need one.
- **`cancel_mission` returns 409 with a `task_id`:** a funding transaction landed on chain but was
  never confirmed, so the budget is escrowed. Run the procedure above with `action: "cancel"`
  while the hiring window is open (the background job may also activate it within ~5 minutes).
  If `cancel` isn't available, record `settlement_deadline` and `emergency_refund` after it.
- **`cancel_mission` returns 503:** the chain couldn't be read, so nothing was cancelled. Retry
  shortly.
- **Lottery, and funding returns 409 with a `task_id`:** a funding transaction the platform
  co-signed for this mission already landed. Don't fund again: confirm that task through
  `confirm-funding` with that `task_id`, or let the background job activate it.

If `fund_solana_mission` returned `refused_to_sign: true`, nothing was signed or escrowed.
Report the `problems` to the operator rather than retrying.

---

## On-chain `media_review` mission is `active` with no confirmed tracks

Funding a `media_review` mission with no ready track is now refused with 409 before anything is
signed, so this only affects missions funded before that check existed. (A mission funded on
chain with no ready track by some other route stays `pending_funding`; see above.) Track uploads
are blocked once `status === 'active'`, so **this mission cannot proceed to settle**. Run the
procedure above:

- **Hiring window still open:** `cancel` is available. Whole budget returns.
- **Hiring window closed, `settlement_deadline` not yet passed:** nothing is available;
  wait for `settlement_deadline`, then `emergency_refund`.
- **`settlement_deadline` passed:** `emergency_refund` immediately.

Then create a new mission, upload and confirm every track, and only then fund it.

---

## Session-Start Scan (quick reference)

Paginate through all missions — a single `limit=100` request misses missions beyond
page 1 for high-volume agents.

```bash
PAGE=1
while true; do
  RESULT=$(curl -s "https://api.mission.projectsolo.ai/agent/missions?limit=100&page=$PAGE" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY")
  echo "$RESULT" | jq '.missions[] | select(.requires_sponsor_action != null) | {id: .mission_id, action: .requires_sponsor_action}'
  # Also catch expired on-chain missions the background job hasn't flagged yet
  echo "$RESULT" | jq '.missions[] | select(.status == "expired" and .onchain_status != null and (.onchain_status == "funded" or .onchain_status == "qualified" or .onchain_status == "refundable")) | {id: .mission_id, onchain_status: .onchain_status}'
  HAS_NEXT=$(echo "$RESULT" | jq -r '.pagination.has_next')
  [ "$HAS_NEXT" = "true" ] || break
  PAGE=$((PAGE+1))
done
```

For each result, run the ask-then-act procedure above and resolve it before continuing with
other work.
