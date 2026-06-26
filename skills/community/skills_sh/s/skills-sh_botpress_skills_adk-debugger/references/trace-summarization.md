# Trace Summarization

How to fetch a trace, walk its span tree, and produce a free-form natural-language summary of what happened. The goal is a synthesized narrative, not a raw dump of span data.

---

## Fetching Trace Data

Use the `adk traces` CLI with filters to get the raw data.

```bash
# Full trace with LLM reasoning included
adk traces trace=<trace-id> --include-llm --format json

# All traces for a conversation
adk traces conversation=<id> --include-llm --format json

# Recent traces (start here if you don't have an ID)
adk traces --include-llm --format json
```

**Always pass `--include-llm`** when summarizing. Without it, `think` spans are omitted and you lose the model's reasoning, which is essential for explaining _why_ the agent did what it did.

**Always pass `--format json`** for structured, parseable output.

---

## Reading the Span Tree

Traces contain a flat list of spans, but spans form a parent-child hierarchy via `parentSpanId`. To summarize effectively, reconstruct the tree.

### Span hierarchy (typical)

```
handler.conversation (or handler.workflow, handler.action)
  └─ autonomous.execution
       └─ autonomous.iteration (one per LLM turn)
            ├─ cognitive.request (the LLM call)
            ├─ think (model reasoning)
            ├─ tool_call (tool invocation)
            │    └─ autonomous.tool (tool execution detail)
            ├─ tool_call (another tool)
            ├─ code_execution_exception (if something broke)
            └─ end (turn complete)
```

### How to walk it

1. **Find the root span** -- the span with no `parentSpanId`, or the handler span (`handler.conversation`, `handler.workflow`, `handler.action`). This tells you what triggered the trace.
2. **Walk children in chronological order** by `startTime`. Each child span is a step in the agent's behavior.
3. **Group by iteration** -- `autonomous.iteration` spans each represent one LLM turn. Within each iteration, look for the `think` -> `tool_call` -> `end` sequence.
4. **Follow errors upward** -- if a `code_execution_exception` or failed `tool_call` appears, check its parent iteration and the subsequent iteration to see how the agent recovered (or didn't).

### Key fields per span type

| Span Type                  | Fields to Read                                                        | What They Tell You                                 |
| -------------------------- | --------------------------------------------------------------------- | -------------------------------------------------- |
| `handler.conversation`     | `context.conversationId`, `context.userId`                            | What triggered the trace (incoming message)        |
| `handler.workflow`         | `name`, `context`                                                     | Which workflow was invoked                         |
| `handler.action`           | `name`, `context`                                                     | Which action was called                            |
| `autonomous.iteration`     | `data.iterationIndex`                                                 | Which LLM turn this is (0-indexed)                 |
| `cognitive.request`        | `data.model`, `data.tokens`                                           | Which model was used, token counts                 |
| `think`                    | `data.content`                                                        | The LLM's reasoning -- why it chose an action      |
| `tool_call`                | `data.tool_name`, `data.input`, `data.output`, `status`, `data.error` | What tool was called, with what, and what happened |
| `code_execution_exception` | `data.message`, `data.stackTrace`                                     | Runtime error in the LLMz sandbox                  |
| `end`                      | `data.response`                                                       | What the agent said back to the user               |

---

## Producing a Summary

Do **not** use a fixed template. Write a natural-language narrative that reads like a concise incident report or activity log. Cover these aspects in whatever order makes the most sense for the specific trace:

### What to cover

1. **The trigger** -- What started this trace? An incoming user message? A workflow invocation? A scheduled trigger? Extract this from the root span type and context.

2. **The LLM's plan** -- What did the model decide to do and why? Synthesize from `think` spans. Don't quote them verbatim unless a specific phrase is important -- paraphrase the reasoning.

3. **Tool calls and their outcomes** -- Which tools were called, with what key inputs, and what happened? For successful calls, note what was returned if relevant. For failures, state the error clearly.

4. **Errors and recovery** -- Were there exceptions? Did the agent retry or give up? What was the error message? If the agent recovered, explain how.

5. **The outcome** -- What was the final result? What did the agent respond with? Did the conversation turn succeed or fail?

6. **Performance** -- Only mention if relevant (e.g., unusually slow, many iterations, high token usage). Don't include timing details for normal traces.

### Adapting depth to context

The summary depth should match what the developer is asking:

| Developer Question                                  | Summary Depth                                                                                                          |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| "What happened?" / "Summarize this trace"           | **Brief** -- 3-5 sentences covering trigger, actions taken, outcome                                                    |
| "Why did it do X?" / "Why did the bot call tool Y?" | **Focused** -- Zoom into the relevant `think` span and the tool call, explain the reasoning chain                      |
| "What went wrong?" / "Why did this fail?"           | **Diagnostic** -- Focus on the error path: what led to the failure, what the error was, whether recovery was attempted |
| "Walk me through the whole trace"                   | **Detailed** -- Full chronological narrative covering every iteration and tool call                                    |

---

## Examples

### Sample trace data (abbreviated)

```json
{
  "traceId": "tr_01J5EXAMPLE",
  "spans": [
    {
      "spanId": "sp_001",
      "name": "handler.conversation",
      "startTime": "2026-04-21T14:00:00.000Z",
      "endTime": "2026-04-21T14:00:03.200Z",
      "status": "ok",
      "context": {
        "conversationId": "conv_abc123",
        "userId": "user_xyz"
      }
    },
    {
      "spanId": "sp_002",
      "parentSpanId": "sp_001",
      "name": "autonomous.execution",
      "startTime": "2026-04-21T14:00:00.050Z",
      "endTime": "2026-04-21T14:00:03.100Z",
      "status": "ok"
    },
    {
      "spanId": "sp_003",
      "parentSpanId": "sp_002",
      "name": "autonomous.iteration",
      "startTime": "2026-04-21T14:00:00.100Z",
      "endTime": "2026-04-21T14:00:02.800Z",
      "status": "ok",
      "data": { "iterationIndex": 0 }
    },
    {
      "spanId": "sp_004",
      "parentSpanId": "sp_003",
      "name": "think",
      "startTime": "2026-04-21T14:00:00.200Z",
      "data": {
        "content": "The user is asking for the status of order #4521. I should look this up using the lookupOrder tool with the order ID."
      }
    },
    {
      "spanId": "sp_005",
      "parentSpanId": "sp_003",
      "name": "tool_call",
      "startTime": "2026-04-21T14:00:00.500Z",
      "endTime": "2026-04-21T14:00:01.200Z",
      "status": "ok",
      "data": {
        "tool_name": "lookupOrder",
        "input": { "orderId": "4521" },
        "output": { "status": "shipped", "trackingNumber": "1Z999AA10123456784", "estimatedDelivery": "2026-04-23" }
      }
    },
    {
      "spanId": "sp_006",
      "parentSpanId": "sp_003",
      "name": "end",
      "startTime": "2026-04-21T14:00:02.800Z",
      "data": {
        "response": "Your order #4521 has been shipped! Tracking number: 1Z999AA10123456784. Estimated delivery: April 23rd."
      }
    }
  ]
}
```

### Brief summary ("What happened?")

> The user asked about order #4521. The agent looked it up with `lookupOrder`, found it was shipped with tracking number 1Z999AA10123456784 and an estimated delivery of April 23rd, and relayed that information to the user. Completed in one iteration, ~3 seconds.

### Sample trace with an error (abbreviated)

```json
{
  "traceId": "tr_01J5FAILURE",
  "spans": [
    {
      "spanId": "sp_010",
      "name": "handler.conversation",
      "startTime": "2026-04-21T15:00:00.000Z",
      "endTime": "2026-04-21T15:00:08.500Z",
      "status": "error",
      "context": {
        "conversationId": "conv_def456",
        "userId": "user_xyz"
      }
    },
    {
      "spanId": "sp_011",
      "parentSpanId": "sp_010",
      "name": "autonomous.execution",
      "startTime": "2026-04-21T15:00:00.050Z",
      "endTime": "2026-04-21T15:00:08.400Z",
      "status": "error"
    },
    {
      "spanId": "sp_012",
      "parentSpanId": "sp_011",
      "name": "autonomous.iteration",
      "startTime": "2026-04-21T15:00:00.100Z",
      "endTime": "2026-04-21T15:00:04.000Z",
      "status": "error",
      "data": { "iterationIndex": 0 }
    },
    {
      "spanId": "sp_013",
      "parentSpanId": "sp_012",
      "name": "think",
      "startTime": "2026-04-21T15:00:00.200Z",
      "data": {
        "content": "The user wants to cancel order #7890. I'll use the cancelOrder tool."
      }
    },
    {
      "spanId": "sp_014",
      "parentSpanId": "sp_012",
      "name": "tool_call",
      "startTime": "2026-04-21T15:00:00.500Z",
      "endTime": "2026-04-21T15:00:02.000Z",
      "status": "error",
      "data": {
        "tool_name": "cancelOrder",
        "input": { "orderId": "7890" },
        "error": "OrderService: Cannot cancel order in 'shipped' status"
      }
    },
    {
      "spanId": "sp_015",
      "parentSpanId": "sp_011",
      "name": "autonomous.iteration",
      "startTime": "2026-04-21T15:00:04.100Z",
      "endTime": "2026-04-21T15:00:08.000Z",
      "status": "ok",
      "data": { "iterationIndex": 1 }
    },
    {
      "spanId": "sp_016",
      "parentSpanId": "sp_015",
      "name": "think",
      "startTime": "2026-04-21T15:00:04.200Z",
      "data": {
        "content": "The cancelOrder tool failed because the order is already shipped. I should inform the user that shipped orders cannot be cancelled and suggest they initiate a return instead."
      }
    },
    {
      "spanId": "sp_017",
      "parentSpanId": "sp_015",
      "name": "end",
      "startTime": "2026-04-21T15:00:07.900Z",
      "data": {
        "response": "I wasn't able to cancel order #7890 because it has already shipped. You can initiate a return once it arrives — would you like me to help with that?"
      }
    }
  ]
}
```

### Diagnostic summary ("What went wrong?")

> The user asked to cancel order #7890. The agent called `cancelOrder` but it failed with "Cannot cancel order in 'shipped' status" -- the order was already shipped. In the second iteration, the agent recognized the failure, informed the user that shipped orders can't be cancelled, and suggested initiating a return instead. The agent handled the error gracefully; this is expected behavior for an already-shipped order, not a bug.

### Focused summary ("Why did it suggest a return?")

> After `cancelOrder` failed with a "shipped" status error, the agent's reasoning (iteration 1 `think` span) explicitly noted that shipped orders can't be cancelled and decided to suggest a return as an alternative. This came from the model's own reasoning, not from the tool output or instructions -- it inferred the next-best action based on the error context.

---

## Patterns

✅ **Synthesize, don't transcribe**

```
Good: "The agent looked up the order, found it was shipped, and told the user."
Bad:  "Span sp_004 is a think span with content 'The user is asking...' then span sp_005 is a tool_call to lookupOrder with input orderId=4521..."
```

✅ **Name tools and key values**

```
Good: "Called `lookupOrder` with orderId '4521', got status 'shipped'."
Bad:  "A tool was called and it returned some data."
```

✅ **Explain causation, not just sequence**

```
Good: "The cancelOrder call failed because the order was already shipped, so the agent suggested a return instead."
Bad:  "cancelOrder failed. Then the agent said to try a return."
```

✅ **Flag what matters for the developer's question**

```
Good (for "why did it fail?"): "The root cause is that cancelOrder doesn't handle shipped orders -- it throws instead of returning an error object."
Bad:  Giving a full trace walkthrough when the developer only asked about the failure.
```

❌ **Don't dump raw JSON or span IDs in the summary**

Span IDs and raw field values are debugging artifacts. The summary is for understanding, not for grep. Reference tool names, error messages, and key data values instead.

❌ **Don't speculate beyond the trace data**

If the trace doesn't show why something happened, say so. Don't invent explanations.

❌ **Don't include timing unless it's notable**

A 3-second conversation turn is normal. A 45-second turn with 12 iterations is worth calling out.
