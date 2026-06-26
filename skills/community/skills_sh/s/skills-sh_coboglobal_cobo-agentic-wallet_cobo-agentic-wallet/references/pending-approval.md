# Pending Approval

How to handle transactions that return `status=PendingApproval` — the required approval flow depends on whether the wallet has been paired to a human owner.

## Check wallet_paired

Always check `wallet_paired` before telling the user how to approve:

```bash
caw status | jq .wallet_paired
```

Or read it from the response of any `caw status` call earlier in the conversation.

## wallet_paired = false — approve in this conversation

The wallet has no paired owner yet. Approval happens directly in this conversation — the user decides, and the agent executes their decision. Ask the user to reply with their decision directly in the chat:

> Note: pending operations expire after a period of inactivity. If the user is unreachable, do not approve. Wait for the user to return before proceeding.

> "This transaction requires your approval before it can proceed.
> Transaction ID: `<request_id>`
> Amount: `<amount>` `<token>` → `<recipient>`
>
> Please reply **approve** or **reject**."

Once the user replies:
- **approve** → call `caw pending approve --operation-id <pending_operation_id>`
  - If this call fails (`.success = false`), surface the error to the user and do not retry — the operation may have already expired or been processed.
- **reject** → call `caw pending reject --operation-id <pending_operation_id> --reason "<reason>"`
- **no reply / user unreachable** → do not approve. Wait and notify when the user returns.

The `pending_operation_id` is returned in the original `caw tx transfer` / `caw tx call` response as `result.pending_operation_id`.

## wallet_paired = true — approve in Cobo Agentic Wallet app

The wallet owner must approve via the Cobo Agentic Wallet app (mobile). Inform the user:

> "This transaction requires approval from the wallet owner in the Cobo Agentic Wallet app.
> Transaction ID: `<request_id>`
> Amount: `<amount>` `<token>` → `<recipient>`
>
> Please open the Cobo Agentic Wallet app and approve the pending operation. I'll continue once it's approved."

Do NOT call `caw pending approve` — that requires the owner's credentials. Poll for completion instead:

```bash
caw pending get --operation-id <pending_operation_id>
# Check .status field
```

Poll every ~10 seconds. Act on `.status`:

| Status | Action |
|---|---|
| `pending` | Still waiting — continue polling |
| `approved` | See **After approval** below |
| `rejected` | Tell the user the owner declined; ask how to proceed |

**After approval:**

Stop polling pending status. Switch to polling transaction status:

```bash
caw tx get --request-id <request-id>
# Poll until terminal state
```

| TX Status | Action |
|---|---|
| `Success` | Report completion to the user |
| `Failed` / `Rejected` / `Cancelled` | Report the failure; ask how to proceed |

**If the owner has not responded after several minutes:** remind the user once:
> "The transaction is still pending approval in the Cobo Agentic Wallet app. Please check your app when you get a chance."

Then continue polling. Do not resubmit the operation.

## Getting pending_operation_id

The `pending_operation_id` is in the submit response:

```bash
caw tx transfer ... | jq .result.pending_operation_id
```

If the transfer was submitted earlier and you no longer have the response, list pending operations:

```bash
caw pending list | jq '.result.items[] | select(.request_id == "<request_id>")'
```

---

Once the approval flow completes (approved or rejected), return to the transaction execution flow in SKILL.md.
