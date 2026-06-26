---
name: tyrpay-buyer-skill
description: Buyer-side TyrPay workflow for LLM agents. Create tasks, optionally wait for seller commitment, fund tasks explicitly, monitor settlement, and request refunds.
---

# TyrPay Buyer Skill

Use this skill when an agent needs to act as the buyer in a TyrPay payment flow.
It assumes the runtime already has a configured `BuyerSdk` and access to the
`@tyrpay/buyer-skill` tool set.

## Quick Start

1. Install `@tyrpay/buyer-skill`, `@tyrpay/buyer-sdk`, and a storage adapter.
2. Construct `BuyerSdk` with a signer, settlement address, and storage adapter.
3. Register `createBuyerTools(sdk)` with your tool-calling runtime.
4. Call `tyrpay_ready` before the first paid workflow.
5. Use `tyrpay_post_task` with `expectations` for the default flow, or `createOnly: true` plus `tyrpay_fund_task` (with `expectations`) for explicit control.

## When To Use

- The agent is responsible for creating and funding a TyrPay task.
- The agent must enforce buyer-side commitment expectations before payment is locked.
- The agent needs structured task state that is safe to show to an end user.
- The buyer workflow must stay non-blocking and recover cleanly after seller-response timeouts.

## Workflow

1. Run `tyrpay_ready` to verify signer and provider connectivity.
2. Call `tyrpay_post_task` with `expectations` describing the acceptable commitment terms.
3. If you need explicit orchestration, set `createOnly: true` (no `expectations` needed at creation).
4. When the seller commitment is ready, call `tyrpay_fund_task` with `expectations` to validate and fund.
5. Use `tyrpay_check_task` or `tyrpay_list_tasks` to monitor progress.
6. If proof submission or verification stalls past protocol timeouts, call `tyrpay_refund_task`.

## Mandatory Expectations

- **`expectations` is required on every funding path.**
  `tyrpay_fund_task` always requires it. `tyrpay_post_task` requires it unless `createOnly: true`.
- The on-chain protocol does **not** enforce that the seller's commitment matches the buyer's requirements.
  The chain only records the commitment; it does not validate host, path, models, minimum usage, verifier, or deadline against the buyer's intent.
- The skill layer rejects any funding call that omits `expectations`, preventing the agent from locking funds under unintended terms.

## Tooling Notes

- All tools reject malformed inputs with structured `BuyerSkillToolError` errors.
- `tyrpay_post_task` returns `timedOut: true` instead of throwing when seller wait time expires after task creation.
- `tyrpay_fund_task` validates the commitment once, then funds without a second redundant validation pass.
- Buyer-facing statuses include `VERIFIED_PASS` and `VERIFIED_FAIL` when a verification report is available.

## Resources

- `references/tool-reference.md` for the tool contract and status model.
