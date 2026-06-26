# Eval File Format

Evals are TypeScript files in the `evals/` directory. Each file exports one or more eval definitions using `new Eval`.

## File Location

Evals live in `evals/` at the **project root** (not inside `src/`). Create it if it doesn't exist:

```
my-agent/
├── agent.config.ts
├── src/
│   ├── actions/
│   └── workflows/
└── evals/              ← create this
    ├── greeting.eval.ts
    └── billing.eval.ts
```

- **Naming**: `*.eval.ts` convention (recommended)
- **Auto-discovery**: All files in `evals/` are picked up by `adk evals`

## Full Structure

```typescript
import { Eval } from '@botpress/evals'

export default new Eval({
  name: 'my-eval', // unique identifier (required)
  description: 'What this tests', // optional
  type: 'regression', // 'capability' or 'regression' — optional, for filtering
  tags: ['tools', 'multi-turn'], // optional, for filtering

  setup: {
    // Seed state or trigger a workflow before the conversation (optional)
  },

  conversation: [
    {
      user: 'message from user', // or: event, expectSilence
      assert: {
        /* per-turn assertions */
      },
    },
  ],

  outcome: {
    /* post-conversation assertions (optional) */
  },

  options: {
    /* per-eval overrides (optional) */
  },
})
```

## Types

| Type         | Purpose                                |
| ------------ | -------------------------------------- |
| `capability` | Verify the bot can do something new    |
| `regression` | Verify the bot still does it correctly |

## Multiple Evals Per File

```typescript
export const greeting = new Eval({ name: 'greeting', ... })
export const farewell = new Eval({ name: 'farewell', ... })
```

---

## Conversation Turns

Each entry in `conversation` is one turn. A turn must have either `user` or `event`.

### User Message

```typescript
{
  user: 'What is my account balance?',
  assert: { /* assertions on the bot's response */ },
}
```

### Event Trigger

Push a custom event instead of a user message. The turn carries only a `payload`; the bot receives it as a `chat:custom` event and reads the data at `event.payload.payload`.

```typescript
{
  event: {
    payload: { orderId: 'ORD-001', total: 49.99 },
  },
  assert: {
    workflow: [{ name: 'orderConfirmation', entered: true }],
  },
}
```

### Expect Silence

Assert the bot does **not** respond. Add `expectSilence: true` to any turn.

```typescript
// Silence after a user message
{ user: 'Please ignore this.', expectSilence: true }

// Silence after an event
{ event: { payload: { kind: 'ping' } }, expectSilence: true }
```

> **Note:** `expectSilence` is mutually exclusive with `assert.response`. Every turn must have `user` or `event` — `expectSilence` is a flag on top of that, not a standalone turn type.

---

## Assertion Categories

### Response

What the bot said back.

```typescript
assert: {
  response: [
    { contains: 'ticket' },                    // substring present
    { not_contains: 'error' },                 // substring absent
    { matches: 'TKT-\\d{3}' },               // regex match
    { llm_judge: 'Response confirms the ticket was created' }, // AI judge, scores 1–5
  ],
}
```

### Tools

Which tools the bot called and with what parameters.

```typescript
assert: {
  tools: [
    { called: 'createTicket' },                          // tool was invoked
    { called: 'createTicket', params: {                  // with specific params
        priority: { equals: 'high' },
        department: { contains: 'Engineering' },
    }},
    { not_called: 'deleteTicket' },                      // tool was NOT invoked
    { call_order: ['lookupUser', 'createTicket'] },      // ordered calls
  ],
}
```

### State

Bot, user, or conversation state values after the turn.

```typescript
assert: {
  state: [
    { path: 'conversation.topic', equals: 'support' },  // exact value
    { path: 'conversation.topic', changed: true },       // value changed from before
    { path: 'bot.ticketCount', equals: 3 },
  ],
}
```

### Workflow

Workflow execution (verified via trace spans).

```typescript
assert: {
  workflow: [
    { name: 'onboarding', entered: true },    // workflow was started
    { name: 'onboarding', completed: true },  // workflow finished
  ],
}
```

### Timing

How long the bot took to respond (milliseconds).

```typescript
assert: {
  timing: [
    { response_time: { lte: 5000 } },  // must respond within 5s
    { response_time: { gte: 100 } },   // sanity-check: not suspiciously fast
  ],
}
```

---

## Match Operators

Used in tool params, state values, and workflow params:

| Operator       | Example                      | Description        |
| -------------- | ---------------------------- | ------------------ |
| `equals`       | `{ equals: 'urgent' }`       | Exact match        |
| `contains`     | `{ contains: 'HR' }`         | Substring          |
| `not_contains` | `{ not_contains: 'test' }`   | Excludes substring |
| `matches`      | `{ matches: '\\d+' }`        | Regex              |
| `in`           | `{ in: ['high', 'urgent'] }` | One of             |
| `exists`       | `{ exists: true }`           | Property exists    |

**Numeric-only operators** (for `timing` and numeric state values):

| Operator | Example         | Description           |
| -------- | --------------- | --------------------- |
| `gte`    | `{ gte: 100 }`  | Greater than or equal |
| `lte`    | `{ lte: 5000 }` | Less than or equal    |

---

## Eval Setup

Use `setup` to put the bot in a known state before the conversation starts.

### Seed State

Pre-populate bot, user, or conversation state.

```typescript
setup: {
  state: {
    bot: { welcomeMessageSent: true },
    user: { plan: 'pro' },
    conversation: { topic: 'billing' },
  },
}
```

The seeded state becomes the baseline for `changed` assertions — `{ changed: false }` passes if the value matches the seeded value at the end.

### Trigger a Workflow

Start a workflow before the conversation begins.

```typescript
setup: {
  workflow: {
    trigger: 'onboarding',
    input: { userId: 'test-user-1' },
  },
}
```

Both can be combined:

```typescript
setup: {
  state: {
    bot: { sleepDurationMs: 3000 }, // 3 seconds instead of default 10 minutes
  },
  workflow: {
    trigger: 'reminderFlow',
    input: { userId: 'test-user-1' },
  },
}
```

> **Testing `step.sleep()`:** Server-side scheduling can't be fast-forwarded. Workaround: make the sleep duration configurable by reading it from bot state in the workflow, then seed a short value in ms (e.g. `3000`) in `setup.state.bot`.

---

## Outcome Assertions

Run once after all conversation turns complete. Supports `state` and `workflow` (not `response` or `tools` — those are per-turn only).

```typescript
outcome: {
  state: [
    { path: 'conversation.resolved', equals: true },
  ],
  workflow: [
    { name: 'ticketFlow', completed: true },
  ],
}
```

---

## Options

Override defaults for a specific eval. Cascades: **eval options → agent config → default**.

```typescript
options: {
  idleTimeout: 60000,       // ms to wait for bot response (default: 30000)
  judgePassThreshold: 4,    // llm_judge score required to pass, 1–5 (default: 3)
}
```

Agent-level defaults in `agent.config.ts`:

```typescript
export default defineConfig({
  evals: {
    idleTimeout: 20000,
    judgePassThreshold: 3,
    judgeModel: 'fast', // 'fast', 'best', or a model ref like 'openai:gpt-4o'
  },
})
```

---

## Common Mistakes

❌ **Turn with neither `user` nor `event`**

```typescript
// WRONG — every turn needs a trigger
{
  expectSilence: true
}
```

✅ **Correct**

```typescript
{ user: 'hello', expectSilence: true }
```

---

❌ **`expectSilence` with `assert.response`**

```typescript
// WRONG — mutually exclusive
{ user: 'hello', expectSilence: true, assert: { response: [{ contains: 'hi' }] } }
```

✅ **Correct — pick one**

```typescript
{ user: 'hello', expectSilence: true }
// or
{ user: 'hello', assert: { response: [{ contains: 'hi' }] } }
```

---

❌ **Both `user` and `event` on the same turn**

```typescript
// WRONG — mutually exclusive
{ user: 'hello', event: { payload: { amount: 50 } } }
```

✅ **Correct — use separate turns**

```typescript
{
  event: {
    payload: {
      amount: 50
    }
  }
}
```

## See Also

- [testing-workflow.md](./testing-workflow.md) — Running evals, interpreting output, the write → test → iterate loop
- [test-patterns.md](./test-patterns.md) — Per-primitive testing patterns
