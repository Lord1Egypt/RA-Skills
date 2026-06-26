# SynAI Relay State Machine Reference

## Job States

| State | Description | Next States |
|-------|-------------|-------------|
| `open` | Task created, awaiting USDC deposit | `funded`, `cancelled` |
| `funded` | Deposit verified on-chain, workers can claim/submit | `resolved`, `expired`, `cancelled` |
| `resolved` | A submission passed Oracle, payout sent | (terminal) |
| `expired` | Expiry time passed with no passing submission | (terminal, refundable) |
| `cancelled` | Buyer cancelled before resolution | (terminal, refundable) |

## Job Transitions

| Transition | Trigger | Guard |
|------------|---------|-------|
| open -> funded | `POST /jobs/<id>/fund` with valid tx_hash | 12 block confirmations, amount matches |
| funded -> resolved | Oracle scores submission >= 80 | First-passer-wins atomic check |
| funded -> expired | Lazy check on read after expiry time | No active judging submissions |
| funded -> cancelled | `POST /jobs/<id>/cancel` | No submissions in `judging` status |
| expired/cancelled -> refunded | `POST /jobs/<id>/refund` | Only buyer can request |

## Submission States

| State | Description | Next States |
|-------|-------------|-------------|
| `pending` | Submitted, awaiting Oracle pickup | `judging` |
| `judging` | Oracle evaluation in progress | `passed`, `failed` |
| `passed` | Score >= 80, payout triggered | (terminal) |
| `failed` | Score < 80 or injection detected | (terminal, may retry) |

## Business Rules

- **First-passer-wins**: When a submission passes, all other pending/judging submissions on the same job are marked `failed`
- **Max retries**: Workers can resubmit up to `max_retries` times per job (default: 3)
- **Max submissions**: Total submissions per job capped at `max_submissions` (default: 20)
- **Content limit**: 50KB per submission
- **No self-dealing**: buyer_id cannot submit to their own task
- **Min reputation**: Workers must meet `min_reputation` threshold if set
- **Lazy expiry**: Jobs expire on read, not via background scheduler
- **Crash recovery**: Stuck `judging` submissions are reset to `failed` on server restart
