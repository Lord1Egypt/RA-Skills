# Per-Primitive Testing Patterns

How to write evals for each ADK primitive type. Each section shows the recommended pattern, what to assert, and common pitfalls.

---

## Actions

Actions are strongly-typed functions callable from conversations, workflows, other actions, or exposed as AI-callable tools. Test them by triggering a conversation that invokes the action and asserting on the response.

```typescript
import { Eval } from '@botpress/evals'

export default new Eval({
  name: 'lookup-order-action',
  tags: ['actions'],

  conversation: [
    {
      user: 'What is the status of order ORD-123?',
      assert: {
        response: [{ contains: 'ORD-123' }, { llm_judge: 'Response includes order status information' }],
        tools: [{ called: 'lookupOrder', params: { orderId: { equals: 'ORD-123' } } }],
      },
    },
  ],
})
```

**What to assert:**

- `tools.called` with expected params — verify the action was invoked correctly
- `response.contains` — verify the bot surfaced the action's result
- `state` — if the action writes to state, verify the write

---

## Tools

Tools are LLM-callable functions. Focus on asserting which tools were called, with what params, and in what order.

```typescript
export default new Eval({
  name: 'ticket-creation-tool',
  tags: ['tools'],

  conversation: [
    {
      user: 'I need help with a billing issue',
      assert: {
        tools: [{ not_called: 'createTicket' }], // not yet
      },
    },
    {
      user: 'Yes, please create a ticket for this',
      assert: {
        tools: [
          {
            called: 'createTicket',
            params: {
              category: { equals: 'billing' },
              priority: { in: ['normal', 'high'] },
            },
          },
        ],
        response: [{ contains: 'ticket' }],
      },
    },
  ],
})
```

**What to assert:**

- `tools.called` with `params` — verify inputs are correctly extracted from the conversation
- `tools.not_called` — verify tools are NOT called prematurely or inappropriately
- `tools.call_order` — verify the correct sequence when multiple tools are involved

### Tool call order pattern

```typescript
assert: {
  tools: [
    { call_order: ['lookupUser', 'fetchAccountBalance', 'formatResponse'] },
  ],
}
```

---

## Workflows

Workflows are long-running resumable processes. Use `setup.workflow` to trigger one before the conversation and assert on its execution.

```typescript
export default new Eval({
  name: 'onboarding-workflow',
  tags: ['workflows'],

  setup: {
    workflow: {
      trigger: 'onboarding',
      input: { userId: 'test-user-1', plan: 'pro' },
    },
  },

  conversation: [
    {
      user: 'What happens next?',
      assert: {
        workflow: [{ name: 'onboarding', entered: true }],
        response: [{ llm_judge: 'Response explains the onboarding next steps' }],
      },
    },
  ],

  outcome: {
    workflow: [{ name: 'onboarding', completed: true }],
    state: [{ path: 'user.onboardingComplete', equals: true }],
  },
})
```

### Testing time-based workflows (`step.sleep()`)

Server-side scheduling cannot be fast-forwarded. Workaround: make the sleep duration configurable in the workflow by reading from bot state.

**In your workflow:**

```typescript
const state = await client.getState({ type: 'bot', id: botId, name: 'botState' })
const sleepMs = (state.state.payload?.value as any)?.sleepDurationMs ?? 10 * 60 * 1000
await step.sleep('wait', sleepMs)
```

**In your eval:**

```typescript
setup: {
  state: {
    bot: { sleepDurationMs: 3000 }, // 3 seconds instead of 10 minutes
  },
  workflow: {
    trigger: 'reminderFlow',
    input: { userId: 'test-user-1' },
  },
}
```

**What to assert:**

- `workflow.entered` — workflow was triggered
- `workflow.completed` — workflow ran to completion (use in `outcome`)
- `state` — final state after the workflow completes
- `tools` — any tools the workflow invoked

---

## Conversations

Conversations are channel-specific message handlers. Test multi-turn flows and context retention across turns.

```typescript
export default new Eval({
  name: 'multi-turn-context',
  tags: ['conversations'],

  conversation: [
    {
      user: 'My name is Alice',
      assert: {
        response: [{ llm_judge: 'Bot acknowledges the name' }],
      },
    },
    {
      user: 'What is my name?',
      assert: {
        response: [{ contains: 'Alice' }], // bot retained context
      },
    },
  ],
})
```

### Testing event-driven conversations

```typescript
export default new Eval({
  name: 'payment-failed-event',
  tags: ['conversations', 'events'],

  conversation: [
    {
      event: {
        payload: { amount: 99.99, currency: 'USD', customerId: 'cust-001' },
      },
      assert: {
        response: [{ llm_judge: 'Bot notifies about the failed payment and offers help' }],
        tools: [{ called: 'lookupCustomer' }],
      },
    },
  ],
})
```

### Testing that events produce no response

```typescript
export default new Eval({
  name: 'internal-event-silence',
  tags: ['conversations', 'events'],

  conversation: [
    {
      event: { payload: { kind: 'heartbeat' } },
      expectSilence: true, // bot should not respond to heartbeat payloads
    },
  ],
})
```

---

## State

State is bot/user/conversation-scoped storage. Use `setup.state` to seed values and assert on state changes.

### Asserting state was set

```typescript
export default new Eval({
  name: 'state-write',
  tags: ['state'],

  conversation: [
    {
      user: 'I prefer to be contacted by email',
      assert: {
        state: [{ path: 'user.contactPreference', equals: 'email' }],
      },
    },
  ],
})
```

### Asserting state changed from seeded value

```typescript
export default new Eval({
  name: 'state-transition',
  tags: ['state'],

  setup: {
    state: {
      conversation: { phase: 'greeting' },
    },
  },

  conversation: [
    {
      user: 'I need help with billing',
      assert: {
        state: [
          { path: 'conversation.phase', equals: 'support' },
          { path: 'conversation.phase', changed: true }, // changed from 'greeting'
        ],
      },
    },
  ],
})
```

### Asserting state did NOT change

```typescript
outcome: {
  state: [
    { path: 'bot.version', changed: false }, // seeded value, should be unchanged
  ],
}
```

---

## Quick Reference: What to Assert Per Primitive

| Primitive     | Primary assertions                   | Secondary assertions |
| ------------- | ------------------------------------ | -------------------- |
| Actions       | `tools.called` + params              | `response`, `state`  |
| Tools         | `tools.called/not_called/call_order` | `response`           |
| Workflows     | `workflow.entered/completed`         | `state`, `outcome`   |
| Conversations | `response` (multi-turn)              | `tools`, `state`     |
| State         | `state.equals/changed`               | `outcome.state`      |

---

## Pattern: Negative Testing

Always test what the bot should NOT do, not just what it should do.

```typescript
conversation: [
  {
    user: 'Show me all users in the system', // unauthorized request
    assert: {
      tools: [{ not_called: 'listAllUsers' }], // should not call admin tool
      response: [
        { not_contains: 'user@example.com' }, // should not leak data
        { llm_judge: 'Response politely declines the request' },
      ],
    },
  },
]
```

## Pattern: Happy Path + Edge Case

```typescript
export const happyPath = new Eval({
  name: 'create-ticket-success',
  type: 'regression',
  conversation: [{ user: 'Create a ticket', assert: { tools: [{ called: 'createTicket' }] } }],
})

export const missingInfo = new Eval({
  name: 'create-ticket-missing-info',
  type: 'capability',
  conversation: [
    {
      user: 'Create a ticket', // no details provided
      assert: {
        tools: [{ not_called: 'createTicket' }], // should ask for more info first
        response: [{ llm_judge: 'Bot asks for more information before creating a ticket' }],
      },
    },
  ],
})
```

## See Also

- [eval-format.md](./eval-format.md) — Full eval file format and all assertion types
- [testing-workflow.md](./testing-workflow.md) — Running evals and the write → test → iterate loop
