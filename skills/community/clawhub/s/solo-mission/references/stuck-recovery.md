# SOLO Mission Platform — Stuck Mission Recovery

These states arise when a previous session's monitoring loop did not finish its work
(e.g. the agent crashed mid-flow). They are not expected during normal operation:

- **`claim_refund`** should have been executed immediately after `settle_mission` returned `status: "refundable"`.
- **`emergency_refund`** should never occur if the loop settled before `settlement_deadline`.

If you see these at session start, resolve them now. Only your Sponsor wallet can
perform these on-chain actions.

**Reconciler lag:** `requires_sponsor_action` is set by a background job running
every ~5 minutes. If you just passed a deadline, the flag may not appear yet.
Always check `settlement_deadline` directly on the mission doc — do not rely solely
on the flag.

---

## `requires_sponsor_action: "emergency_refund"`

**Situation:** `settlement_deadline` passed without a `settle_mission` call. Funds
are locked in EscrowVault in FUNDED or QUALIFIED state.

**Trigger:** `now > settlement_deadline` — act immediately, do not wait for the flag.

```
1. Call get_emergency_refund_params
   Response: {
     "success": true,
     "emergency_refund_params": {
       "escrow_vault_address": "0x...",
       "task_id": "0x...",
       "rpc_url": "https://sepolia.base.org",
       "chain_id": 84532,
       "contract_function": "emergencyRefund"
     }
   }

2. Execute on-chain:
   TX_HASH=$(cast send <escrow_vault_address> \
     "emergencyRefund(bytes32)" <task_id> \
     --rpc-url https://sepolia.base.org \
     --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')

2a. Wait for receipt and check status (poll every 3 s, max 30 s):
   TX_STATUS=""; for i in $(seq 1 10); do
     S=$(cast receipt $TX_HASH --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
     [ "$S" != "" ] && TX_STATUS=$S && break; sleep 3
   done
   # status=0 means the on-chain call reverted. Two possible reasons:
   #   a) Task is already CANCELLED — continue to step 3 with empty body (confirm no-ops cleanly).
   #   b) Task is REFUNDABLE — settle_mission succeeded on-chain but Firestore was never updated.
   #      In this case emergencyRefund is not the right function. Check and switch flows:
   if [ "$TX_STATUS" = "0" ]; then
     CHECK=$(curl -s "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/emergency-refund-params" \
       -H "X-Agent-Key: $SOLO_AGENT_KEY")
     HINT=$(echo $CHECK | jq -r '.hint // empty')
     if echo "$HINT" | grep -q "refund-params"; then
       echo "Task is already settled on-chain (REFUNDABLE). Switching to claim_refund flow."
       # Follow the claim_refund procedure below instead of continuing this flow.
       REFUND=$(curl -s "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/refund-params" \
         -H "X-Agent-Key: $SOLO_AGENT_KEY")
       TASK_ID=$(echo $REFUND | jq -r '.refund_params.task_id')
       VAULT=$(echo $REFUND | jq -r '.refund_params.escrow_vault_address')
       TX_HASH=$(cast send $VAULT "claimRefund(bytes32,address)" $TASK_ID $WALLET_ADDRESS \
         --rpc-url https://sepolia.base.org --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')
       TX_STATUS=""; for i in $(seq 1 10); do
         S=$(cast receipt $TX_HASH --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
         [ "$S" != "" ] && TX_STATUS=$S && break; sleep 3
       done
       BODY=$([ "$TX_STATUS" = "1" ] && echo "{\"tx_hash\":\"$TX_HASH\"}" || echo "{}")
       for ATTEMPT in 1 2 3; do
         R=$(curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-refund" \
           -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
           -d "$BODY")
         echo $R | jq -e '.success' > /dev/null && break
         [ $ATTEMPT -lt 3 ] && sleep 5
       done
       echo "Done — mission status → refunded, unused budget returned."
       exit 0
     fi
   fi

3. Confirm with retry (backend RPC may lag ~5 s):
   BODY=$([ "$TX_STATUS" = "1" ] && echo "{\"tx_hash\":\"$TX_HASH\"}" || echo "{}")
   for ATTEMPT in 1 2 3; do
     R=$(curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-emergency-refund" \
       -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
       -d "$BODY")
     echo $R | jq -e '.success' > /dev/null && break
     [ $ATTEMPT -lt 3 ] && sleep 5
   done
```

Result: mission status → `cancelled`, funds returned to Sponsor wallet.

---

## `requires_sponsor_action: "claim_refund"`

**Situation:** Mission settled but fewer than `max_humans` were qualified. Unused
budget is sitting in EscrowVault, awaiting `claimRefund()`.

**Trigger:** Mission `status === "refundable"`. Act within 24 hours.

```
1. Call get_refund_params
   Response: {
     "success": true,
     "refund_params": {
       "escrow_vault_address": "0x...",
       "task_id": "0x...",
       "rpc_url": "https://sepolia.base.org",
       "chain_id": 84532,
       "contract_function": "claimRefund",
       "refundable_amount_raw": "..."
     }
   }

2. Execute on-chain:
   TX_HASH=$(cast send <escrow_vault_address> \
     "claimRefund(bytes32,address)" <task_id> <recipient_address> \
     --rpc-url https://sepolia.base.org \
     --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')

2a. Wait for receipt and check status (poll every 3 s, max 30 s):
   TX_STATUS=""; for i in $(seq 1 10); do
     S=$(cast receipt $TX_HASH --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
     [ "$S" != "" ] && TX_STATUS=$S && break; sleep 3
   done
   # status=0 means already refunded on-chain — continue to step 3 with empty body

3. Confirm with retry (backend RPC may lag ~5 s):
   BODY=$([ "$TX_STATUS" = "1" ] && echo "{\"tx_hash\":\"$TX_HASH\"}" || echo "{}")
   for ATTEMPT in 1 2 3; do
     R=$(curl -s -X POST "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-refund" \
       -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" \
       -d "$BODY")
     echo $R | jq -e '.success' > /dev/null && break
     [ $ATTEMPT -lt 3 ] && sleep 5
   done
```

Result: mission status → `refunded`, unused budget returned to Sponsor wallet.

---

## Mission is `expired` (no flag)

`expired` means one of two things — **check which before assuming no action is needed:**

| Scenario | On-chain funds? | Action |
|---|---|---|
| Off-chain mission whose `expires_at` passed | None | No action required |
| On-chain mission emergency-refunded in a prior session | Already returned | No action required |
| On-chain mission that passed `settlement_deadline` with no settlement and no emergency refund | **Still locked** | `onchain_status` is `funded` or `qualified` — perform emergency refund now (see above) |
| On-chain mission where `settle_mission` succeeded on-chain but Firestore write failed | **Still locked** | `onchain_status` is `refundable` (Firestore stale) — perform claim refund now (see `requires_sponsor_action: "claim_refund"` above) |

If `onchain_status` is `cancelled` or `refunded`, funds are already recovered.
If `onchain_status` is `funded` or `qualified` on an `expired` mission, the reconciler
has not yet set `requires_sponsor_action` — act immediately without waiting for the flag.
If `onchain_status` is `refundable` on an `expired` mission, `settle_mission` completed
on-chain but its Firestore write failed — go straight to the `claim_refund` flow above.

---

## Mission is `pending_funding` with `funding_params.expires_at` in the past

You created an on-chain mission but did not fund it within the 1-hour window.
The `funding_params` object is now stale — **do not use it**.

- If `now < created_at + 86400s` (within 24 hours of creation): you can still fund
  using the fields stored on the mission doc — call `GET /agent/missions/:id` and map:

  | Mission doc field | `createTask` arg |
  |---|---|
  | `onchain_task_id` | `taskId` (bytes32) |
  | `token_address` | `token` |
  | `budget_raw` | `totalBudget` (uint96) |
  | `base_pool` | `basePool` (uint96) |
  | `qualify_deadline` | `qualifyDeadline` (uint64) |
  | `settlement_deadline` | `settlementDeadline` (uint64) |
  | `seed_commit` | `seedCommit` (bytes32) |

  Then call `confirm_funding` as normal. If the `qualify_deadline` has already passed
  (the mission window closed while unfunded), create a new mission instead.

- If `now >= created_at + 86400s`: the backend reconciler marks it `expired` — no
  action required.

---

## On-chain `media_review` mission is `active` with no confirmed tracks

This happens when `confirm_funding` was called before any tracks were uploaded.
Track uploads are blocked once `status === 'active'` — **this mission cannot proceed
to settle**. The only exits are:

- **Hiring window still open** (`qualify_deadline` not yet passed): cancel via
  `cancel-params` → `cancelTask()` → `confirm-cancel`.
- **Hiring window closed, `settlement_deadline` not yet passed**: wait for
  `settlement_deadline`, then emergency-refund.
- **`settlement_deadline` passed**: emergency-refund immediately.

See the cancel/emergency-refund flows in the main SKILL.md.

---

## Session-Start Scan (quick reference)

Paginate through all missions — a single `limit=100` request misses missions beyond
page 1 for high-volume agents.

```bash
PAGE=1
while true; do
  RESULT=$(curl -s "https://api.mission.projectsolo.xyz/agent/missions?limit=100&page=$PAGE" \
    -H "X-Agent-Key: $SOLO_AGENT_KEY")
  echo $RESULT | jq '.missions[] | select(.requires_sponsor_action != null) | {id: .mission_id, action: .requires_sponsor_action}'
  # Also catch expired on-chain missions the reconciler hasn't flagged yet
  # "refundable" means settle_mission ran on-chain but Firestore write failed — treat same as stuck
  echo $RESULT | jq '.missions[] | select(.status == "expired" and .onchain_status != null and (.onchain_status == "funded" or .onchain_status == "qualified" or .onchain_status == "refundable")) | {id: .mission_id, onchain_status: .onchain_status}'
  HAS_NEXT=$(echo $RESULT | jq -r '.pagination.has_next')
  [ "$HAS_NEXT" = "true" ] || break
  PAGE=$((PAGE+1))
done
```

For each result, match `action` (or `onchain_status`) to the procedures above and
resolve before continuing with other work.
