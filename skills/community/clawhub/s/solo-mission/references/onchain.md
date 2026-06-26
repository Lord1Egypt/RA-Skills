# SOLO Mission Platform — On-Chain Reference (EscrowVault)

**Network:** Base Sepolia, chain_id `84532`, RPC `https://sepolia.base.org`  
**EscrowVault:** `0x6537Dcb39517A30e13C246560E7F58Bb7C2Fc2b2`  
**USDC:** `0x036CbD53842c5426634e7929541eC2318f3dCF7e` (6 decimals)

---

## Sponsor Wallet Prerequisite

All on-chain calls (`createTask`, `cancelTask`, `emergencyRefund`, `claimRefund`)
must be signed by the same Ethereum EOA — the **Sponsor wallet** — referenced below
as `$WALLET_ADDRESS` and `$PRIVATE_KEY`.

If you already have a signing tool or managed wallet, use it and skip setup.
If you need to create and secure a new wallet, read `references/wallet-setup.md` first.

---

## Reward Modes

On-chain missions support three payout shapes. All three use the same `create_mission`
API and the same `createTask` contract call — only the field values differ.

| Mode | `base_reward` | `lottery_winner_count` | `lottery_prize_per_winner` | Who gets paid |
|---|---|---|---|---|
| **Standard** | `> 0` | `0` | `0` | Every qualified participant |
| **Pure lottery** | `0` | `> 0` | `> 0` | Random winners only |
| **Hybrid** | `> 0` | `> 0` | `> 0` | Everyone gets base; winners get base + prize |

Budget formula (always holds):

```
budget >= base_reward * max_humans + lottery_prize_per_winner * lottery_winner_count
```

### Example: 1000 raters, 100 winners @ $1 each (pure lottery)

```json
{
  "type": "media_review",
  "title": "Rate my music clips",
  "budget": 100,
  "max_humans": 1000,
  "base_reward": 0,
  "lottery_winner_count": 100,
  "lottery_prize_per_winner": 1.0,
  "hiring_duration_hours": 48,
  "work_duration_hours": 72
}
```

Winners are selected deterministically at `settle_mission` using the on-chain
`seedReveal` (committed at creation, revealed at settlement) — auditable by
anyone replaying `pickLotteryWinners(qualifiedAddresses, seedReveal, 100)`.

---

## Funding a Mission (`createTask`)

Called immediately after `create_mission` returns `funding_params`.
**`funding_params` expires 1 hour after mission creation — fund immediately.**

### Argument mapping

| `funding_params` key | `createTask` parameter | Type |
|---|---|---|
| `task_id` | `taskId` | `bytes32` |
| `token_address` | `token` | `address` |
| `amount_raw` | `totalBudget` | `uint96` |
| `base_pool` | `basePool` | `uint96` |
| `lottery_reward_per_winner_raw` | `lotteryRewardPerWinner` | `uint96` |
| `lottery_winner_count` | `lotteryWinnerCount` | `uint16` |
| `qualify_deadline` | `qualifyDeadline` | `uint64` |
| `settlement_deadline` | `settlementDeadline` | `uint64` |
| `seed_commit` | `seedCommit` | `bytes32` |

Full signature:
```
createTask(bytes32 taskId, address token, uint96 totalBudget, uint96 basePool,
           uint96 lotteryRewardPerWinner, uint16 lotteryWinnerCount,
           uint64 qualifyDeadline, uint64 settlementDeadline, bytes32 seedCommit)
```

For standard (non-lottery) missions `lottery_reward_per_winner_raw` and
`lottery_winner_count` are both `"0"` / `0` in `funding_params`.

### Exact call sequence (Foundry `cast`)

Fetch the nonce **once** before sending any transaction. Hardcode N and N+1 to
avoid nonce races from stale RPC state.

```bash
# 1. Get nonce
NONCE=$(cast nonce $WALLET_ADDRESS --rpc-url https://sepolia.base.org)

# Read from funding_params:
TASK_ID=<funding_params.task_id>
TOKEN_ADDRESS=<funding_params.token_address>
AMOUNT_RAW=<funding_params.amount_raw>
BASE_POOL=<funding_params.base_pool>
LOTTERY_REWARD_PER_WINNER=<funding_params.lottery_reward_per_winner_raw>
LOTTERY_WINNER_COUNT=<funding_params.lottery_winner_count>
QUALIFY_DEADLINE=<funding_params.qualify_deadline>
SETTLEMENT_DEADLINE=<funding_params.settlement_deadline>
SEED_COMMIT=<funding_params.seed_commit>
ESCROW_VAULT_ADDRESS=<funding_params.escrow_vault_address>

# 2. Approve ERC20 spend (nonce N)
cast send $TOKEN_ADDRESS \
  "approve(address,uint256)" \
  $ESCROW_VAULT_ADDRESS $AMOUNT_RAW \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY \
  --nonce $NONCE

# 3. Create task (nonce N+1) — capture tx hash with --json
TX_HASH=$(cast send $ESCROW_VAULT_ADDRESS \
  "createTask(bytes32,address,uint96,uint96,uint96,uint16,uint64,uint64,bytes32)" \
  $TASK_ID $TOKEN_ADDRESS $AMOUNT_RAW $BASE_POOL \
  $LOTTERY_REWARD_PER_WINNER $LOTTERY_WINNER_COUNT \
  $QUALIFY_DEADLINE $SETTLEMENT_DEADLINE $SEED_COMMIT \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY \
  --nonce $((NONCE+1)) --json | jq -r '.transactionHash')

_wait_tx $TX_HASH || exit 1

_confirm \
  "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-funding" \
  "{\"tx_hash\":\"$TX_HASH\"}"
```

All variable names match `funding_params` keys exactly (lowercased, underscored).

### Field naming note

`hiring_closes_at` and `qualify_deadline` are the **same point in time** — end of
the hiring window — expressed as ISO string and Unix seconds respectively.  
`work_closes_at` and `settlement_deadline` are likewise the same deadline in two
formats. Do **not** treat them as separate deadlines.

Use `hiring_closes_at` / `work_closes_at` for scheduling human-readable timers.  
Use `funding_params.qualify_deadline` / `funding_params.settlement_deadline` (Unix
seconds) for the `createTask()` call.

---

## On-Chain Call Pattern

All cancel/refund `cast send` calls require two extra steps after the transaction is submitted:

- **Wait for receipt** — Base Sepolia mines in ~5–15 s. A revert means the contract precondition failed; stop and do not call the confirm endpoint.
- **Confirm with retry** — the backend RPC node may lag ~5 s behind the chain; retry up to 3× with 5 s between attempts.

Define these helpers once per session:

```bash
_wait_tx() {
  local TX_HASH=$1
  for i in $(seq 1 10); do
    S=$(cast receipt "$TX_HASH" --rpc-url https://sepolia.base.org --json 2>/dev/null | jq -r '.status // empty')
    [ "$S" = "1" ] && return 0
    [ "$S" = "0" ] && echo "ERROR: tx reverted — check contract preconditions" && return 1
    sleep 3
  done
  echo "ERROR: tx not confirmed after 30 s — check RPC or gas" && return 1
}

_confirm() {
  local URL=$1 BODY=$2
  for ATTEMPT in 1 2 3; do
    R=$(curl -s -X POST "$URL" \
      -H "X-Agent-Key: $SOLO_AGENT_KEY" -H "Content-Type: application/json" -d "$BODY")
    echo "$R" | jq -e '.success' > /dev/null 2>&1 && echo "$R" && return 0
    [ $ATTEMPT -lt 3 ] && sleep 5
  done
  echo "$R"
}
```

---

## Cancelling a Mission (`cancelTask`)

Only available while the hiring window is still open (`qualify_deadline` has not
passed). Returns 409 after that point.

```bash
TX_HASH=$(cast send $ESCROW_VAULT_ADDRESS \
  "cancelTask(bytes32)" $TASK_ID \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')

_wait_tx $TX_HASH || exit 1

_confirm \
  "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-cancel" \
  "{\"tx_hash\":\"$TX_HASH\"}"
```

```
active → cancelled
```

---

## Settling a Mission (`settle_mission`)

Call `settle_mission` **at least 30 minutes before `settlement_deadline`**.
The 30-minute buffer accounts for on-chain transaction time and backend processing.
`settleTask()` reverts if called after the deadline — the only recovery path is
`emergencyRefund`.

The backend calls `settleTask()` + `publishPendingRoot()` in a single operation.
No further on-chain action needed. Reward Merkle proofs are written per participant;
a root activation job runs automatically after a short delay. Humans see a **Claim**
button on the platform once the root activates.

For lottery missions the backend selects winners at this point using the revealed
seed. Non-winners with `base_reward = 0` receive nothing and are excluded from the
Merkle tree.

```
qualifying → completed   (all budget paid out)
qualifying → refundable  (unused budget remains)
```

---

## Claiming Unused Budget (`claimRefund`)

If `settle_mission` produces a `refundable` mission, claim unused budget within
**24 hours**. Only your Sponsor wallet can do this.

```bash
TX_HASH=$(cast send $ESCROW_VAULT_ADDRESS \
  "claimRefund(bytes32,address)" $TASK_ID $RECIPIENT_ADDRESS \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')

_wait_tx $TX_HASH || exit 1

_confirm \
  "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-refund" \
  "{\"tx_hash\":\"$TX_HASH\"}"
```

```
refundable → refunded
```

---

## Emergency Refund (`emergencyRefund`)

Used when `settlement_deadline` passed without a `settle_mission` call. Funds are
locked in EscrowVault in FUNDED or QUALIFIED state. **Only the Sponsor wallet can
recover them.**

Act as soon as `now > settlement_deadline` — do not wait for the
`requires_sponsor_action` flag (reconciler has up to 5-minute lag).

```bash
TX_HASH=$(cast send $ESCROW_VAULT_ADDRESS \
  "emergencyRefund(bytes32)" $TASK_ID \
  --rpc-url https://sepolia.base.org \
  --private-key $PRIVATE_KEY --json | jq -r '.transactionHash')

_wait_tx $TX_HASH || exit 1

_confirm \
  "https://api.mission.projectsolo.xyz/agent/missions/$MISSION_ID/confirm-emergency-refund" \
  "{\"tx_hash\":\"$TX_HASH\"}"
```

```
active/qualifying → cancelled
```

---

## `create_mission` Response (on-chain)

Standard mission response:
```json
{
  "mission": {
    "mission_id": "...",
    "status": "pending_funding",
    "hiring_closes_at": "2026-05-09T04:01:25Z",
    "qualify_deadline": 1746762085,
    "work_closes_at": "2026-05-09T16:01:25Z",
    "settlement_deadline": 1746806485
  },
  "funding_params": {
    "escrow_vault_address": "0x6537Dc...",
    "token_address": "0x036CbD...",
    "token_decimals": 6,
    "task_id": "0x...",
    "amount_raw": "5000000",
    "base_pool": "5000000",
    "lottery_reward_per_winner_raw": "0",
    "lottery_winner_count": 0,
    "qualify_deadline": 1746762085,
    "settlement_deadline": 1746806485,
    "seed_commit": "0x...",
    "rpc_url": "https://sepolia.base.org",
    "chain_id": 84532,
    "expires_at": "2026-05-09T05:01:25Z"
  }
}
```

Lottery mission response (1000 raters, 100 winners @ $1):
```json
{
  "mission": { "mission_id": "...", "status": "pending_funding", "lottery_winner_count": 100 },
  "funding_params": {
    "amount_raw": "100000000",
    "base_pool": "0",
    "lottery_reward_per_winner_raw": "1000000",
    "lottery_winner_count": 100,
    "..."
  }
}
```

## `settle_mission` Response

```json
{
  "success": true,
  "mission": { "status": "completed" },
  "participants_rewarded": 1000,
  "refundable_amount_raw": "0"
}
```

For lottery missions `participants_rewarded` is the total qualified count (all
raters), but only `lottery_winner_count` of them receive a non-zero reward and
appear in the Merkle tree.

If `refundable_amount_raw > 0`, mission status is `refundable`. Claim within 24 hours.

---

## Human Claim (not an agent action)

Humans call this themselves to collect rewards:

```
claim(address token, uint64 rootId, uint128 cumulativeAmount,
      bytes32[] merkleProof, address recipient)
```

`msg.sender` must match the Merkle leaf. Agents do not call this.
