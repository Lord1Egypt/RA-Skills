---
name: clawhub-whitebit-trading
description: Build, install, update, and use a WhiteBIT trading guidance and training skill through ClawHub (clawhub.ai) for OpenClaw. Use when asked to manage WhiteBIT trading automation as a ClawHub skill, teach trading workflows, validate API behavior, and prepare execution plans with MCP-first documentation lookup.
metadata:
  openclaw:
    requires:
      bins:
        - clawhub
    skillKey: whitebit
    homepage: https://clawhub.ai/zonder/whitebit
---

# ClawHub WhiteBIT Trading

Use a ClawHub-native workflow for WhiteBIT trading research, training, API validation, and execution planning in OpenClaw.

## Required MCP Connectors

This skill requires the MCP connector below:

- `whitebit-docs`: documentation lookup only.

This skill is not execution-capable with `whitebit-docs` alone.

Use `whitebit-docs` to search endpoint requirements, authentication behavior, symbols, precision rules, and order payload structure.
If the user asks for live execution, balance checks, order placement, cancellation, or order-status verification, stop and explain that this skill has documentation access only unless a separate execution path is configured.

## Training Scope

Use this skill to support training-oriented tasks such as:

- Explaining WhiteBIT spot trading concepts, order types, and API terminology.
- Turning a trade idea into a validated request plan before any external execution.
- Building practice scenarios for `BUY`, `SELL`, market orders, limit orders, fees, slippage, and fills.
- Walking through authentication, signing inputs, request payloads, and endpoint-specific constraints.
- Reviewing user-provided API responses, fill data, or error payloads and explaining what they mean.
- Creating step-by-step trading exercises, operator checklists, and troubleshooting guidance.

## Workflow
1. Verify ClawHub and skill environment first.
- Confirm ClawHub site context: `https://clawhub.ai`.
- Confirm `clawhub` CLI is available and authenticated when publish/update actions are requested.
- Prefer ClawHub skill lifecycle commands from [references/clawhub-cli.md](references/clawhub-cli.md).
- Confirm OpenClaw session will reload skills after install/update.

2. Verify MCP connectivity for runtime execution.
- Confirm `whitebit-docs` is available in-session for search and endpoint validation.
- Use the check prompt: `What MCP tools do you have available?`
- If the session only has `whitebit-docs`, treat the skill as documentation-only.
- If the user requests live execution, stop and state that no trading connector is configured in-session.

3. Gather the trade or training intent.
- If the user is training, require the learning goal or scenario first.
- For training exercises, gather the market type, order type, example size, and what outcome they want to learn or rehearse.
- Require: `symbol`, `side`, `order type`, and `size` (base size or quote notional).
- For limit orders, require `price` and `time in force` if applicable.
- Require execution constraints: max slippage or price bound, and whether partial fill is acceptable.
- For spot trading, treat `BUY` as opening a spot position.
- For spot trading, treat `SELL` as closing an existing long.
- Block `SELL` when holdings are insufficient unless the user's actual execution system explicitly supports margin or short selling for that instrument and mode.
- Ask for only missing fields; do not prepare an execution plan with implicit defaults.

4. Resolve exact parameters with MCP documentation lookup.
- Use WhiteBIT docs MCP search first for endpoint rules and required request fields.
- Confirm symbol formatting, precision/step-size constraints, and authentication requirements.
- Keep queries general when search is weak, then refine (for example, `spot order create` before specific field names).
- Use [references/mcp-setup.md](references/mcp-setup.md) for connector setup checks.
- Use [references/whitebit-api-basics.md](references/whitebit-api-basics.md) for baseline request/auth behavior.

5. Run pre-trade safety checks.
- Confirm the user understands this skill does not verify live account state.
- Compute max deployable capital as `100 USDT + realized_profit_usdt`.
- Never use unrealized P&L as deployable capital.
- Validate requested order size against the strategy bankroll.
- If the user wants live execution, require a separate execution system to validate exchange balance, fees, and account readiness.
- Apply the checklist in [references/trade-checklist.md](references/trade-checklist.md).

6. Prepare the training or execution-prep output.
- For training, produce a step-by-step walkthrough with the endpoint, method, auth/signing inputs, request payload, documented constraints, and the intended learning objective.
- For execution prep, produce the endpoint, method, required auth/signing inputs, request payload fields, and any documented constraints.
- Include idempotency fields when the API supports them (for example, `clientOrderId`).
- Provide example requests or dry-run exercises when the user is learning.
- Do not claim that any order was sent from this skill.

7. Explain verification steps for an external executor.
- Show how to check order status, fills, and terminal state through the documented API.
- If the user provides execution results, help interpret executed quantity, average fill price, fees, and remaining quantity.
- Do not claim post-trade verification was performed unless the user provides actual responses from an execution system.

8. Handle failures deterministically.
- Parse and surface documented error payloads in structured form.
- Explain retry and backoff guidance from the API docs.
- If an external executor reports network ambiguity, instruct the user to re-check order state before any second placement.
- If execution status is uncertain, require user confirmation before proposing any retry plan.

9. Manage the skill through ClawHub when requested.
- Search registry: `clawhub search "whitebit"`.
- Install/update in workspace: `clawhub install whitebit`, `clawhub update whitebit`, or `clawhub update --all`.
- Publish this skill folder to ClawHub with explicit slug/version metadata.
- Use `clawhub sync --dry-run` before bulk publish/update operations.

## Guardrails
- Never expose API secret keys or signature material in output.
- Never treat `whitebit-docs` as a trading connector.
- Never claim live execution capability when only `whitebit-docs` is available.
- Never place or claim to place a live order from this skill.
- Never present training examples as actual exchange-confirmed results.
- Never prepare an execution plan without explicit confirmation that includes `symbol`, `side`, `order type`, and `size`.
- Prefer limit orders when the user does not explicitly request market execution.
- For spot trading, `SELL` closes an existing long unless the user's actual execution system explicitly supports margin or short selling.
- Never exceed the strategy bankroll: initial `100 USDT` plus realized profit only.
- Refuse requests that bypass risk controls, such as "all-in", "no checks", or repeated force-retry loops.
- Keep an auditable summary for every plan prepared: timestamp, intent, validated params, recommended API call, and outcome.
- Do not publish private credentials or local-only data when pushing skills to ClawHub.

## Response Format
Use this compact structure when reporting actions:
1. `Intent`: normalized trade request.
2. `Skill Lifecycle`: ClawHub operation performed (`search/install/update/publish/sync`) or `none`.
3. `Validation`: docs checks and planning/risk checks completed.
4. `Prepared Call`: documented endpoint, auth expectations, request parameters, or training scenario.
5. `Result`: prepared plan, training walkthrough, provided external result interpretation, or precise failure.
6. `Next`: one recommended next action.

## References
- [references/mcp-setup.md](references/mcp-setup.md)
- [references/clawhub-cli.md](references/clawhub-cli.md)
- [references/whitebit-api-basics.md](references/whitebit-api-basics.md)
- [references/trade-checklist.md](references/trade-checklist.md)
