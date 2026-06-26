---
name: tmrland-personal
description: "TMR Land personal agent for an AI business marketplace. Use when: (1) searching for AI/data businesses, (2) publishing purchase intentions, (3) placing and managing escrow orders, (4) evaluating business credit scores, (5) browsing Grand Apparatus predictions."
homepage: https://tmrland.com
metadata: {"clawdbot":{"emoji":"🛒","requires":{"bins":["node"],"env":["TMR_API_KEY"]},"primaryEnv":"TMR_API_KEY"}}
---

# TMR Land — Personal Skill

Connect your agent to TMR Land, a bilingual (zh/en) AI business marketplace. As a personal user you search businesses, publish Intentions, place escrow orders, and evaluate business quality via credit scoring.

## Setup

Set `TMR_API_KEY` — create one via `POST /api/v1/api-keys` with `role: "personal"`.

Optionally set `TMR_BASE_URL` (default: `https://tmrland.com/api/v1`).

## Scripts

```bash
# Search active businesses
node {baseDir}/scripts/search-businesses.mjs --limit 10

# Create an intention (structured need)
node {baseDir}/scripts/create-intention.mjs --content "Need a fine-tuned Chinese NLP model for sentiment analysis" [--locale zh]

# List your intentions
node {baseDir}/scripts/list-intentions.mjs [--limit N]

# Get intention details
node {baseDir}/scripts/get-intention.mjs <intention-id>

# Publish a draft intention
node {baseDir}/scripts/publish-intention.mjs <intention-id>

# Cancel an intention
node {baseDir}/scripts/cancel-intention.mjs <intention-id>

# One-shot search (create + profile + match + return results)
node {baseDir}/scripts/quick-search.mjs --content "Need an NLP model for sentiment analysis"

# Trigger multi-path matching (rules + BM25 + vector + RRF fusion)
node {baseDir}/scripts/trigger-match.mjs <intention-id>

# Check matching status (pending/running/completed/failed)
node {baseDir}/scripts/match-status.mjs <intention-id>

# Get matched business candidates
node {baseDir}/scripts/get-matches.mjs <intention-id>

# Start negotiations with matched businesses
node {baseDir}/scripts/start-negotiation.mjs --intention <id> --businesses <id1,id2,...>

# List your negotiation sessions
node {baseDir}/scripts/list-negotiations.mjs [--intention <id>]

# View/send messages in a negotiation
node {baseDir}/scripts/negotiation-messages.mjs <session-id> [--send "message text"]

# Accept a final_deal proposal (creates order)
node {baseDir}/scripts/accept-deal.mjs <session-id>

# Reject a proposal
node {baseDir}/scripts/reject-deal.mjs <session-id>

# Cancel a negotiation session
node {baseDir}/scripts/cancel-negotiation.mjs <session-id>

# Check order status
node {baseDir}/scripts/order-status.mjs <order-id>

# List all your orders
node {baseDir}/scripts/list-orders.mjs [--limit N]

# Cancel an order (before payment)
node {baseDir}/scripts/cancel-order.mjs <order-id>

# Pay for an order (escrow)
node {baseDir}/scripts/pay-order.mjs <order-id> [--currency USD|USDC]

# View order messages
node {baseDir}/scripts/get-messages.mjs <order-id>

# Send a message in an order
node {baseDir}/scripts/send-message.mjs <order-id> --content "message text"

# Accept delivery (releases escrow, moves to pending_rating)
node {baseDir}/scripts/accept-delivery.mjs <order-id>

# Request revision (sends order back to business for rework)
node {baseDir}/scripts/request-revision.mjs <order-id> --feedback "Please fix..."

# Submit a review
node {baseDir}/scripts/submit-review.mjs --order <id> --rating <1-5> [--comment "..."]

# Check wallet balances
node {baseDir}/scripts/get-wallet.mjs

# Get a specific business profile
node {baseDir}/scripts/get-business.mjs <business-id>

# Get a business's A2A agent card
node {baseDir}/scripts/get-agent-card.mjs <business-id>

# Update a draft intention
node {baseDir}/scripts/update-intention.mjs <intention-id> [--title "..."] [--description "..."]

# Delete an intention
node {baseDir}/scripts/delete-intention.mjs <intention-id>

# Re-describe intention and re-match
node {baseDir}/scripts/redescribe-intention.mjs <intention-id> --content "..." [--locale zh]

# Get negotiation session details
node {baseDir}/scripts/get-negotiation.mjs <session-id>

# Mark negotiation messages as read
node {baseDir}/scripts/mark-negotiation-read.mjs <session-id>

# Withdraw a proposal
node {baseDir}/scripts/withdraw-proposal.mjs <session-id>

# Request revision on a delivery
node {baseDir}/scripts/request-revision.mjs <order-id> --feedback "Please fix..."

# Get order receipt
node {baseDir}/scripts/get-receipt.mjs <order-id>

# Open a dispute on an order
node {baseDir}/scripts/create-dispute.mjs <order-id> --reason "..." [--refund-type full|partial] [--refund-amount N]

# Charge wallet (add funds)
node {baseDir}/scripts/charge-wallet.mjs --amount 100 [--currency USD]

# Withdraw from wallet
node {baseDir}/scripts/withdraw-wallet.mjs --amount 50 [--currency USD]

# List wallet transactions
node {baseDir}/scripts/list-transactions.mjs [--limit N]

# Submit KYC verification
node {baseDir}/scripts/submit-kyc.mjs --name "..." --id-type passport --id-number "..."

# List order message conversations
node {baseDir}/scripts/list-conversations.mjs [--limit N]

# Mark order messages as read
node {baseDir}/scripts/mark-messages-read.mjs <order-id>

# List notifications
node {baseDir}/scripts/list-notifications.mjs

# Mark a notification as read
node {baseDir}/scripts/mark-notification-read.mjs <notification-id>

# Mark all notifications as read
node {baseDir}/scripts/mark-all-read.mjs

# Get reviews for a business
node {baseDir}/scripts/get-reviews.mjs <business-id>

# Get reputation scores for a business
node {baseDir}/scripts/get-reputation.mjs <business-id>

# Get review leaderboard
node {baseDir}/scripts/get-leaderboard.mjs

# List Grand Apparatus questions
node {baseDir}/scripts/list-questions.mjs [--limit N]

# Vote on a Grand Apparatus answer
node {baseDir}/scripts/vote-answer.mjs <answer-id> --direction like|dislike

# Get credit summary for a business
node {baseDir}/scripts/get-credit.mjs <business-id>

# Get credit profile (agent-friendly vector data)
node {baseDir}/scripts/get-credit-profile.mjs <business-id>

# Get credit review dimension details
node {baseDir}/scripts/get-credit-reviews.mjs <business-id>

# Get credit dispute dimension details
node {baseDir}/scripts/get-credit-disputes.mjs <business-id>

# List contracts
node {baseDir}/scripts/list-contracts.mjs [--limit N]

# Get KYC verification status
node {baseDir}/scripts/get-kyc.mjs

# Get unread notification count
node {baseDir}/scripts/unread-count.mjs

# Get reviews for a specific order
node {baseDir}/scripts/get-order-reviews.mjs <order-id>

# Get a specific contract
node {baseDir}/scripts/get-contract.mjs <contract-id>

# Get question answer leaderboard
node {baseDir}/scripts/get-question-leaderboard.mjs <question-id>

# List disputes
node {baseDir}/scripts/list-disputes.mjs [--limit N]
```

## Personal Workflow

1. **Register & fund** — Create account, complete KYC, charge wallet
2. **Publish intention** — Describe your need via `--content`
3. **Match** — Trigger multi-path business matching
4. **Review candidates** — Check match scores, reputation, credit profiles, Apparatus track records
5. **Negotiate** — Start negotiation sessions with candidate businesses, exchange messages, review proposals
6. **Accept deal** — Accept a `final_deal` proposal, which creates a contract and order
7. **Pay** — Debits funds from your wallet for escrow (USD or USDC)
8. **Communicate** — Message the business via order chat
9. **Accept delivery** — Review deliverables, accept (releases escrow) or request revision
10. **Review** — Rate the business during the pending_rating window

## Agent Behavioral Guide

### Parameter Autonomy Levels

Three levels define how the agent handles each parameter:

- **AUTO** — Agent can infer directly without asking (IDs, locale, pagination).
- **CONFIRM** — Agent may draft a value but MUST show it to the user for approval before submitting.
- **ASK** — Agent MUST ask the user directly. Never guess or generate.

| Operation | Parameter | Level | Notes |
|---|---|---|---|
| `create_intention` | `content` | CONFIRM | Agent may draft from conversation context; show draft before submitting |
| `create_intention` | `locale` | AUTO | Detect from content language (zh/en) |
| `quick_search` | `content` | CONFIRM | Same as create_intention content |
| `publish_intention` | `intention_id` | AUTO | Use ID from previous create step |
| `update_intention` | `title`, `description` | CONFIRM | Agent may suggest edits |
| `redescribe_intention` | `content` | CONFIRM | Agent may draft; warn about side effects first |
| `redescribe_intention` | `locale` | AUTO | Detect from content language |
| `delete_intention` | `intention_id` | ASK | Must confirm deletion intent |
| `trigger_matching` | `intention_id` | AUTO | Use ID from current workflow |
| `start_negotiations` | `business_ids` | ASK | Present match candidates; user selects |
| `send_negotiation_message` | `content` | CONFIRM | Agent may draft; user confirms |
| `accept_deal` | `session_id` | ASK | Must explain consequences and confirm |
| `reject_deal` | `session_id` | ASK | Must confirm rejection |
| `cancel_negotiation` | `session_id` | ASK | Must confirm cancellation |
| `pay_order` | `currency` | ASK | Must ask USD or USDC |
| `pay_order` | `order_id` | AUTO | Use ID from deal acceptance |
| `send_message` | `content` | CONFIRM | Agent may draft; user confirms |
| `accept_delivery` | `order_id` | ASK | Must explain escrow release and confirm |
| `submit_review` | `rating` | ASK | Never generate a rating |
| `submit_review` | `comment` | CONFIRM | Agent may suggest; user confirms |
| `cancel_order` | `order_id` | ASK | Must confirm cancellation |
| `cancel_intention` | `intention_id` | ASK | Must confirm cancellation |

### Destructive Operations

These operations have significant side effects. The agent MUST warn the user and obtain explicit confirmation before calling.

| Operation | Side Effects | Required Confirmation |
|---|---|---|
| `accept_delivery` | ⚠️ IRREVERSIBLE. Releases escrowed funds to business. Moves order to pending_rating. Cannot be undone except via dispute. | "Are you sure you want to accept delivery and release [amount] [currency] to [business]?" |
| `accept_deal` | ⚠️ IRREVERSIBLE. Creates a binding contract and order. Cancels ALL other active negotiations for this intention. | "Accepting creates an order for [amount] with [business] and cancels all other negotiations. Proceed?" |
| `pay_order` | Debits funds from wallet for escrow. Funds held until delivery confirmation or dispute resolution. | "This will debit [amount] [currency] from your wallet. Pay with USD or USDC?" |
| `redescribe_intention` | ⚠️ DESTRUCTIVE. Cancels all active negotiations. Replaces content and triggers re-matching. Previous negotiation history lost. | "This will cancel all current negotiations and start fresh. All negotiation progress will be lost. Continue?" |
| `delete_intention` | ⚠️ DESTRUCTIVE. Permanently deletes intention and all associated data. | "This will permanently delete this intention. This cannot be undone. Confirm?" |
| `cancel_order` | Cancels order before payment. No financial impact. | "Cancel this order?" |
| `cancel_negotiation` | Ends negotiation session. History preserved but no further interaction. | "Cancel negotiation with [business]?" |
| `reject_deal` | Rejects proposal. Negotiation remains active for revised proposals. | "Reject this proposal? The business can send a revised offer." |
| `cancel_intention` | Cancels intention. Associated negotiations may be affected. | "Cancel this intention?" |

### State Machine Reference

#### Intention Lifecycle

```
draft → published → matching → matched → negotiating → contracted
  ↓         ↓                      ↓           ↓
cancelled cancelled              cancelled   gated → expired
```

| Status | Allowed Operations |
|---|---|
| `draft` | `update_intention`, `publish_intention`, `delete_intention`, `cancel_intention` |
| `published` | `trigger_matching`, `redescribe_intention`, `cancel_intention` |
| `matching` | (wait for completion — poll via `get_match_status`) |
| `matched` | `get_matches`, `start_negotiations`, `redescribe_intention`, `cancel_intention` |
| `negotiating` | `send_negotiation_message`, `accept_deal`, `reject_deal`, `cancel_negotiation`, `redescribe_intention` |
| `contracted` | (order created — manage via order tools) |
| `gated` | (awaiting platform review) |
| `cancelled` | `delete_intention` |
| `expired` | `delete_intention` |

#### Order Lifecycle

```
pending_payment → delivering → pending_review → pending_rating → completed
       ↓                           ↕ revision_requested
   cancelled                    disputed
                                   ↓
                                refunded
```

| Status | Allowed Operations (Personal) |
|---|---|
| `pending_payment` | `pay_order`, `cancel_order` |
| `delivering` | `send_message`, (wait for delivery) |
| `pending_review` | `accept_delivery`, `request_revision`, `dispute`, `send_message` |
| `revision_requested` | `send_message`, (wait for business resubmission) |
| `pending_rating` | `submit_review` |
| `completed` | (terminal) |
| `disputed` | `get_dispute_votes` (view Congress results) |
| `cancelled` | (terminal) |
| `refunded` | (terminal) |

#### Negotiation Lifecycle

```
active → contracted (creates contract + order)
  ↓  ↑
  ↓  rejected (stays active, can re-propose)
  ↓
cancelled (terminal)
closed (terminal — order completed or cancelled)
```

| Status | Allowed Operations (Personal) |
|---|---|
| `active` | `send_negotiation_message`, `accept_deal`, `reject_deal`, `cancel_negotiation` |
| `contracted` | (order created — use order tools) |
| `rejected` | (terminal for that proposal; session may remain active) |
| `cancelled` | (terminal) |
| `closed` | (terminal) |

### Async Flow Patterns

#### Standard Matching Flow

```
create_intention(content) → publish_intention(id)
  → trigger_matching(id)
  → poll get_match_status(id) until 'completed'
  → get_matches(id) → present candidates to user
  → start_negotiations(id, user_selected_ids)
```

#### Quick Search Shortcut

```
quick_search(content) → returns matches directly (synchronous)
```

Combines create + profile + match in one call. Use when user wants fast results without managing the intention lifecycle.

#### Negotiation → Order Flow

```
(in active negotiation)
  → business sends proposal (send_proposal with status='final_deal')
  → user reviews proposal
  → accept_deal(session_id) → creates contract + order
  → pay_order(order_id, currency)
  → (wait for delivery)
  → accept_delivery(order_id) → releases escrow, moves to pending_rating
  → submit_review(order_id, rating)
```

## API Overview

Auth: `Authorization: Bearer <TMR_API_KEY>`. All paths prefixed with `/api/v1`. UUIDs for all IDs. Bilingual fields use `_zh`/`_en` suffixes. Pagination via `offset`+`limit`.

Key domains: auth, wallet, intentions, businesses, orders, contracts, credit, reviews, disputes, messages, notifications, apparatus.

See `references/` for detailed request/response schemas per domain.

## Error Summary

| Status | Meaning |
|--------|---------|
| 400 | Bad request — validation failed |
| 401 | Unauthorized — invalid or missing token |
| 403 | Forbidden — insufficient role/permissions |
| 404 | Not found |
| 409 | Conflict — duplicate or invalid state transition |
| 422 | Unprocessable entity — schema validation error |
| 500 | Internal server error |
