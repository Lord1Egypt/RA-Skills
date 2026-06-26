# Conversation Analysis

How to summarize and explain full conversations using the `adk conversations` command. A conversation spans multiple turns (traces), so this is a higher-level view than single-trace analysis.

For single-trace summaries, see `trace-summarization.md`. This document covers multi-turn conversation-level analysis.

---

## CLI Commands

### List recent conversations

```bash
adk conversations --format json
adk conversations list limit=5 --format json
```

**Output** (JSON): Array of objects, each with:

| Field            | Type    | Description                                                             |
| ---------------- | ------- | ----------------------------------------------------------------------- |
| `conversationId` | string  | Unique conversation identifier                                          |
| `firstSeen`      | string  | ISO timestamp of the first recorded turn                                |
| `lastSeen`       | string  | ISO timestamp of the most recent turn                                   |
| `traceCount`     | number  | Total number of turns in the conversation                               |
| `integration`    | string  | Which integration the conversation came from (e.g., `slack`, `webchat`) |
| `channel`        | string  | Which channel within the integration (e.g., `dm`, `thread`)             |
| `hasErrors`      | boolean | Whether any turn in the conversation had errors                         |

### Show a conversation's timeline

```bash
# Standard view
adk conversations show <conversation-id> --format json

# With LLM reasoning included
adk conversations show <conversation-id> --include-llm --format json
```

**Output** (JSON): Object with:

| Field            | Type   | Description                  |
| ---------------- | ------ | ---------------------------- |
| `conversationId` | string | The conversation ID          |
| `turnCount`      | number | Total number of turns        |
| `turns`          | array  | Ordered list of turn objects |

Each turn object contains:

| Field        | Type   | Description                                                  |
| ------------ | ------ | ------------------------------------------------------------ |
| `traceId`    | string | Trace ID for this turn (use for drill-down)                  |
| `startedAt`  | string | ISO timestamp when the turn started                          |
| `duration`   | string | How long the turn took (e.g., `"2.3s"`)                      |
| `status`     | string | `"ok"` or `"error"`                                          |
| `trigger`    | string | What started this turn (e.g., user message, event, workflow) |
| `toolCalls`  | array  | Tools invoked during this turn                               |
| `errors`     | array  | Error strings, if any                                        |
| `llmContent` | array  | LLM reasoning data (only with `--include-llm`)               |

Each `toolCalls` entry has: `name`, `status`, `duration`, `error?`

Each `llmContent` entry has: `name`, `data`

---

## Two Modes of Analysis

### 1. Summarize a Conversation

**Purpose:** Give a concise overview of what happened -- a paragraph or two covering the full conversation arc.

**When to use:** The developer asks "What happened in this conversation?", "Summarize conversation X", or wants a quick picture before diving deeper.

**Data source:**

```bash
adk conversations show <conversation-id> --format json
```

No need for `--include-llm` -- the standard view has enough for a summary.

**What to cover:**

1. **Who and where** -- integration, channel, how many turns, time span
2. **The flow** -- what the user asked for, what the agent did, how the conversation progressed
3. **Tools used** -- which tools were called and how often
4. **Outcome** -- did the conversation succeed? Were there errors? How did it end?
5. **Red flags** -- only if present: errors, long durations, many turns for a simple task

**How to write it:**

Write a natural-language paragraph, not a list or template. Synthesize the turn data into a narrative.

#### Example

Given this conversation data:

```json
{
  "conversationId": "conv_abc123",
  "turnCount": 4,
  "turns": [
    {
      "traceId": "tr_001",
      "startedAt": "2026-04-21T14:00:00.000Z",
      "duration": "1.8s",
      "status": "ok",
      "trigger": "User message via slack/dm",
      "toolCalls": [],
      "errors": []
    },
    {
      "traceId": "tr_002",
      "startedAt": "2026-04-21T14:00:05.000Z",
      "duration": "3.2s",
      "status": "ok",
      "trigger": "User message via slack/dm",
      "toolCalls": [{ "name": "lookupOrder", "status": "ok", "duration": "0.9s" }],
      "errors": []
    },
    {
      "traceId": "tr_003",
      "startedAt": "2026-04-21T14:00:15.000Z",
      "duration": "4.1s",
      "status": "error",
      "trigger": "User message via slack/dm",
      "toolCalls": [
        { "name": "cancelOrder", "status": "error", "duration": "1.2s", "error": "Cannot cancel shipped order" }
      ],
      "errors": ["Cannot cancel shipped order"]
    },
    {
      "traceId": "tr_004",
      "startedAt": "2026-04-21T14:00:25.000Z",
      "duration": "2.0s",
      "status": "ok",
      "trigger": "User message via slack/dm",
      "toolCalls": [],
      "errors": []
    }
  ]
}
```

**Good summary:**

> A 4-turn Slack DM conversation over about 30 seconds. The user started with a greeting, then asked about an order -- the agent looked it up with `lookupOrder`. The user then asked to cancel the order, but `cancelOrder` failed because the order was already shipped. The agent recovered in the final turn without needing more tools, likely explaining the situation to the user. One error occurred (`cancelOrder` failure) but it was handled gracefully.

**Bad summary:**

> Turn 1: traceId tr_001, status ok, no tools. Turn 2: traceId tr_002, called lookupOrder, status ok. Turn 3: traceId tr_003, called cancelOrder, status error, error "Cannot cancel shipped order". Turn 4: traceId tr_004, status ok, no tools.

---

### 2. Explain a Conversation

**Purpose:** Provide a detailed, step-by-step breakdown where the developer understands every decision the agent made.

**When to use:** The developer asks "Walk me through this conversation", "Explain what happened", "Why did the bot respond that way?", or is investigating a specific behavior.

**Data source:**

```bash
adk conversations show <conversation-id> --include-llm --format json
```

**Always use `--include-llm`** for explanations. Without it, you lose the LLM's reasoning, which is essential for explaining _why_ the agent did what it did.

**What to cover for each turn:**

1. **The trigger** -- what started this turn (user message, event, workflow continuation)
2. **LLM reasoning** -- what the agent decided to do and why (from `llmContent`)
3. **Tool calls** -- what was called, with what inputs, what happened
4. **Errors** -- what went wrong and how the agent responded
5. **The response** -- what the agent said back (infer from context if not explicit)
6. **Transitions** -- how one turn's outcome led to the next

**How to write it:**

Walk through turns chronologically. For each turn, narrate what happened as a coherent paragraph. Use tool names in backticks, quote key values, and explain the agent's reasoning when `llmContent` provides it.

#### Example

Given the same conversation with `--include-llm`:

```json
{
  "conversationId": "conv_abc123",
  "turnCount": 4,
  "turns": [
    {
      "traceId": "tr_001",
      "startedAt": "2026-04-21T14:00:00.000Z",
      "duration": "1.8s",
      "status": "ok",
      "trigger": "User message via slack/dm",
      "toolCalls": [],
      "errors": [],
      "llmContent": [
        {
          "name": "cognitive.iteration",
          "data": "The user said 'Hi, I need help with an order'. This is a greeting with intent to discuss an order. I'll respond and ask for the order number."
        }
      ]
    },
    {
      "traceId": "tr_002",
      "startedAt": "2026-04-21T14:00:05.000Z",
      "duration": "3.2s",
      "status": "ok",
      "trigger": "User message via slack/dm",
      "toolCalls": [{ "name": "lookupOrder", "status": "ok", "duration": "0.9s" }],
      "errors": [],
      "llmContent": [
        {
          "name": "cognitive.iteration",
          "data": "The user provided order number #4521. I should look this up to get the details before responding."
        }
      ]
    },
    {
      "traceId": "tr_003",
      "startedAt": "2026-04-21T14:00:15.000Z",
      "duration": "4.1s",
      "status": "error",
      "trigger": "User message via slack/dm",
      "toolCalls": [
        { "name": "cancelOrder", "status": "error", "duration": "1.2s", "error": "Cannot cancel shipped order" }
      ],
      "errors": ["Cannot cancel shipped order"],
      "llmContent": [
        { "name": "cognitive.iteration", "data": "The user wants to cancel order #4521. I'll use cancelOrder." },
        {
          "name": "cognitive.iteration",
          "data": "cancelOrder failed -- the order is already shipped. I need to tell the user and suggest a return instead."
        }
      ]
    },
    {
      "traceId": "tr_004",
      "startedAt": "2026-04-21T14:00:25.000Z",
      "duration": "2.0s",
      "status": "ok",
      "trigger": "User message via slack/dm",
      "toolCalls": [],
      "errors": [],
      "llmContent": [
        {
          "name": "cognitive.iteration",
          "data": "The user asked how to start a return. I know the process from the instructions -- they need to go to the returns portal. No tool call needed."
        }
      ]
    }
  ]
}
```

**Good explanation:**

> **Turn 1** (tr_001, 1.8s): The user opened the conversation in Slack DM with "Hi, I need help with an order." The agent recognized this as a greeting with order-related intent and responded by asking for the order number. No tools were needed.
>
> **Turn 2** (tr_002, 3.2s): The user provided order #4521. The agent called `lookupOrder` to retrieve the order details (completed in 0.9s). The lookup succeeded and the agent relayed the order information to the user.
>
> **Turn 3** (tr_003, 4.1s): The user asked to cancel the order. The agent called `cancelOrder`, which failed with "Cannot cancel shipped order" -- the order had already shipped. The agent's reasoning shows it recognized the failure and decided to suggest a return as an alternative. The turn is marked as `error` because of the tool failure, but the agent handled it gracefully.
>
> **Turn 4** (tr_004, 2.0s): The user asked how to start a return. The agent answered from its instructions without needing any tool calls, directing the user to the returns portal. The conversation ended successfully.
>
> **Overall:** The conversation followed a natural support flow -- greeting, order lookup, failed cancellation handled with a fallback suggestion, and resolution. The `cancelOrder` error is expected behavior for a shipped order, not a bug.

---

## Picking Which Conversation to Analyze

When the developer doesn't specify a conversation ID, help them find the right one.

### Step 1: List conversations

```bash
adk conversations --format json
```

### Step 2: Narrow down

Use the list output to identify the conversation. Key signals:

| Signal                    | How to Use                                                                      |
| ------------------------- | ------------------------------------------------------------------------------- |
| `lastSeen`                | Most recent conversation is usually the one they're asking about                |
| `hasErrors`               | If they're debugging a failure, look for `hasErrors: true`                      |
| `integration` / `channel` | If they mention "the Slack conversation" or "the webchat issue", match on these |
| `traceCount`              | High turn counts may indicate stuck loops or long interactions                  |

### Step 3: Show the conversation

```bash
adk conversations show <conversation-id> --format json
```

If the developer needs more detail, add `--include-llm`.

---

## Correlating with Trace Data

Each turn in the conversation has a `traceId`. This is the bridge between conversation-level and trace-level analysis.

**When to drill into a trace:**

- A turn has `status: "error"` and you need the full span tree to understand why
- A tool call failed and you need the stack trace or detailed error
- The LLM reasoning (from `llmContent`) is surprising and you want to see the full `think` spans
- You need to see the exact inputs/outputs of a tool call

**How to drill down:**

```bash
# Get the full trace for a specific turn
adk traces trace=<trace-id> --include-llm --format json
```

Then use the trace-reading techniques from `trace-summarization.md` to analyze the individual trace.

**Flow:**

```
adk conversations list          →  find the conversation
adk conversations show <id>     →  see the timeline
adk traces trace=<trace-id>     →  drill into a specific turn
```

---

## Common Patterns to Highlight

When analyzing conversations, watch for these patterns and call them out.

### Long conversations

A conversation with many turns (10+) for what should be a simple task.

**What to say:** Flag the turn count, identify where the conversation got stuck or went off track, and suggest whether the issue is in the agent's instructions, tool design, or workflow logic.

### Error recovery

The agent encounters an error but recovers in a subsequent turn.

**What to say:** Note that the agent handled the error gracefully, explain the recovery path, and confirm whether the behavior is correct or accidental.

### Tool call chains

Multiple tools called in sequence within a single turn, or across turns, to accomplish a multi-step task.

**What to say:** Describe the chain, note whether each step depended on the previous one's output, and flag any unnecessary calls.

### Stuck loops

The agent calls the same tool repeatedly across multiple turns or within a single turn.

**What to say:** Identify the repeating pattern, explain why the agent is stuck (from `llmContent` if available), and suggest fixes (improve tool output, add `onBeforeTool` guard, set `maxIterations`). See `llm-debugging.md` for more on looping.

### Silent failures

A turn completes with `status: "ok"` but the agent didn't actually accomplish the task (e.g., returned a generic response without calling a tool).

**What to say:** Flag the gap between expected and actual behavior, and suggest investigating the LLM reasoning with `--include-llm`.

### Integration-specific patterns

Different integrations have different conversation patterns -- Slack threads vs webchat sessions vs API calls.

**What to say:** Note the integration and channel, and flag anything unusual for that context (e.g., a webchat conversation with 50 turns might indicate the user is stuck in a loop, while a Slack thread with 50 turns might be a busy channel).

---

## Patterns

✅ **Summarize first, explain on request**

```
Developer: "What happened in conv_abc123?"
→ Start with a summary (no --include-llm needed)
→ Only drill into explanation if they ask for more detail
```

✅ **Use the conversation timeline as a map**

```
Good: "The conversation had 4 turns. Turn 3 is where the error occurred. Let me drill into that trace."
Bad: Immediately fetching all traces for all turns and dumping everything.
```

✅ **Name the integration and channel**

```
Good: "A 4-turn Slack DM conversation..."
Bad: "A conversation with 4 turns..."
```

✅ **Connect turns to each other**

```
Good: "The user asked about the order in turn 2, then tried to cancel it in turn 3 -- the cancellation failed because the lookup in turn 2 showed the order was already shipped."
Bad: "Turn 2: lookupOrder called. Turn 3: cancelOrder failed."
```

✅ **Suggest drill-down when appropriate**

```
Good: "Turn 3 failed with a cancelOrder error. To see the full stack trace, run: adk traces trace=tr_003 --include-llm --format json"
Bad: Automatically fetching and dumping the full trace without being asked.
```

❌ **Don't dump raw JSON in the analysis**

The developer already has the JSON. Your job is to synthesize it into understanding.

❌ **Don't speculate about what the user said**

The conversation timeline shows what the agent did, not the exact user messages. Use `trigger` and `llmContent` to infer context, but be clear when you're inferring vs. when you have direct evidence.

❌ **Don't re-explain tool behavior the developer already knows**

If the developer built the tools, they know what `lookupOrder` does. Focus on _what happened_ and _why_, not what the tool is for.

❌ **Don't ignore the overall arc**

Even in a detailed explanation, start and end with the big picture. A list of turns without a conclusion is incomplete.
