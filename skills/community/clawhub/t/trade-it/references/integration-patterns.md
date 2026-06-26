# Integration Patterns for AI Agents and Chatbots

## Core product choice

Trade It provides two integration modes for AI products:

### Mode A: API-native conversational trading
Use when your agent should:
- inspect accounts
- read holdings/trades
- create draft trades
- ask for confirmation
- execute after confirmation

Key endpoints:
- `GET /api/user/me`
- `POST /api/tool/execute`
- `GET /api/trade`
- `GET /api/account/:id/holdings`

### Mode B: Hosted browser handoff
Use when your agent should:
- prompt the user to link a brokerage
- open a pre-authenticated Trade It UI
- let the user review a hosted trade experience

Key endpoint:
- `POST /api/session/url`

Many products combine both modes: API-native steps for automation and hosted UI for connection/review.

## Pattern 1: Connect on demand

Use when the user asks to trade but has no usable connection.

Flow:
1. Parse intent.
2. Check user/account/connectivity context.
3. Generate a connect session URL.
4. Send the user into the hosted connect flow.
5. Resume conversation after they return.

Best for:
- OpenClaw
- Discord bots
- web chat products
- agentic assistants that need browser help mid-conversation

## Pattern 2: Draft-first execution

This should be the default for agentic trading, while still checking for cases where create is immediately placed.

Flow:
1. Fetch candidate accounts with `get_accounts` if needed.
2. Normalize symbol, side, amount, order type, and account.
3. Create a draft trade with `create_trade` or `create_options_trade`.
4. Summarize the draft in plain English.
5. Execute only after the user explicitly confirms.

Why it is the right default:
- safer
- auditable
- easier to explain in chat
- matches Trade It's draft/execute model cleanly

## Pattern 3: Review in hosted trade UI

Use when you want Trade It to own the review/placement UX.

Flow:
1. Generate `target: "trade"` session URL.
2. Open hosted UI.
3. Let the user review and submit there.

This is especially good when:
- you want less custom frontend work
- you want consistency across brokerages
- your chat product is mostly orchestration, not full UI

## Recommended module boundaries

### tradeit-client
Own raw HTTP calls.

### tradeit-service
Own business helpers like:
- `getAccounts`
- `createDraftTrade`
- `createDraftOptionsTrade`
- `executeTrade`
- `createConnectSessionUrl`
- `createTradeSessionUrl`

### chat-orchestrator
Own user interaction:
- ask clarifying questions
- summarize account choices
- require execution confirmation
- decide between hosted UI and direct API path

## Validation checklist before `create_trade`

- symbol present
- side present
- amount present
- account selected or defaulted intentionally
- order type present
- limit price present for `limit` and `stop_limit`
- stop price present for `stop` and `stop_limit` if supported by the chosen payload

## Validation checklist before `execute_trade`

- draft trade exists
- user has just confirmed
- account and symbol still match the summary shown to the user
- no stale state from an earlier conversation turn

## Suggested UX copy

### Need connection
"You need to link a brokerage first. Open this Trade It link, finish the connection, then come back and I'll continue from there."

### Draft created
"I drafted the order. Review this summary and tell me if you want me to place it."

### Hosted review
"I've prepared a Trade It review link. Open it to inspect and submit the order."

### Missing inputs
"I need symbol, side, amount, account, and order type. If it's limit or stop-based, I also need the price levels."
