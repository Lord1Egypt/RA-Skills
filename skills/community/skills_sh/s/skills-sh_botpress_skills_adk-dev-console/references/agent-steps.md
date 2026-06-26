# Agent Steps

Agent Steps is the execution visualizer on the right side of the **Chat** page. It shows exactly what the agent did to process each conversation message — in real time.

## What Users See

When a user sends a message in the webchat (left panel), the Agent Steps panel (right panel) shows the execution flow as a sequence of collapsible cards:

```
┌─ User Message: "Help me with order #123"
│
├─ 🤖 Bot Handler (onWebchatConversation)
│   ├─ Iteration 1
│   │   ├─ 🟣 Tool: lookupOrder (input: {orderId: "123"})
│   │   └─ → continued
│   ├─ Iteration 2
│   │   ├─ 🔵 Message: "I found order #123. It was shipped yesterday..."
│   │   └─ → message_sent
│   └─ 🟢 State: conversation.lastOrderId = "123"
│
└─ Total: 2 iterations, $0.0034, 1.2s
```

## Data Model

### Turns

A **Turn** is one conversation exchange — from the user's input through the agent's complete response. Each turn contains:

- **User message** or **event** that triggered processing
- **Handler span** — the conversation/event/trigger handler that processed it
- **Steps** — autonomous iterations (the agent's think-decide-act loops)
- **Direct messages** — messages sent outside iterations
- **State mutations** — state changes made during the turn
- **Total cost** — aggregated AI cost across all iterations

### Steps (Autonomous Iterations)

Each **Step** is one iteration of the autonomous agent loop. The agent:

1. Receives context (conversation history, available tools)
2. Makes an LLM call (the **cognitive request**)
3. Decides what to do: call a tool, send a message, or stop

Each step shows:

- **Iteration number** (1, 2, 3...)
- **Exit reason**: "continued" (more work to do), "tool_called", "message_sent", "errored"
- **Cognitive request** metadata: model, input/output tokens, cost, duration
- **Tools called** in this iteration
- **Messages sent** in this iteration

### Tool Calls

Displayed as **violet cards** (or green for `search_knowledge`). Each shows:

- Tool name
- Input (JSON)
- Output (JSON or markdown for knowledge search results)
- Duration
- Status (ok / error / running)

### Bot Messages

Displayed as **blue cards**. Each shows:

- Message content (markdown rendered)
- Duration
- Long messages are clamped at 300 characters — click to expand

### State Mutations

Displayed as **teal cards**. Each shows:

- State type (bot, user, conversation)
- Two-column "Before" and "After" view
- Only changed keys shown by default (toggle for full state)
- JSON tree view for complex objects

### Trigger Handlers

When a trigger fires instead of a conversation message, the turn shows an **amber card** with:

- Trigger name
- Event type that fired it
- Same iteration/tool/message structure inside

## Status Indicators

| Visual                       | Meaning                                |
| ---------------------------- | -------------------------------------- |
| ✓ Green checkmark            | Completed successfully                 |
| ✗ Red X                      | Failed (error message in detail panel) |
| ⟳ Blue spinner               | Currently executing                    |
| Shimmer text ("thinking...") | LLM is generating                      |

## AI Metrics

Each iteration's cognitive request shows:

- **Model**: e.g., "claude-3.5-sonnet"
- **Input tokens**: count + cost
- **Output tokens**: count + cost
- **Total cost**: USD with 4 decimal places
- **Duration**: milliseconds

Turn-level cost is the sum of all iteration costs.

## Interactions

- **Collapse/Expand**: Click any card to toggle children. "Collapse All" / "Expand All" buttons in header.
- **Detail Panel**: Click a step to open a resizable detail panel on the right with full span data.
- **Copy**: Copy buttons on IDs, tokens, error messages.
- **Open Traces**: "Open conversation traces" link in the header navigates to the full Traces page filtered to this conversation.

## Real-Time Updates

Agent Steps streams data via SSE (Server-Sent Events):

- Running spans show a live timer
- New spans animate in from the top
- Auto-scrolls to bottom when new content arrives
- Stale detection marks spans as errored if the CLI stops sending updates for 5+ seconds
