---
name: adk-evals
description: Complete reference for writing, running, and iterating on evals (automated conversation tests) for ADK agents. Covers eval file format, all assertion types, CLI usage, and per-primitive testing patterns.
license: MIT
---

# ADK Evals Skill

## What are Evals?

Evals are automated conversation tests for ADK agents. Each eval defines a scenario — a sequence of user messages or events — and asserts on what the bot should do: what it says, which tools it calls, how state changes, which workflows run, and more.

Evals run against a live dev bot (`adk dev`), so they test the full stack — not mocks.

## When to Use This Skill

Use this skill when the developer asks about:

- **Writing evals** — file format, assertions, turn types, setup
- **Running evals** — CLI commands, filtering, output interpretation
- **Testing specific primitives** — how to test actions, tools, workflows, conversations, state
- **The testing loop** — write → run → inspect traces → iterate
- **CI integration** — exit codes, `--format json` flag, tagging strategies
- **Eval configuration** — idleTimeout, judgePassThreshold, judgeModel

Or when you are developing an ADK bot and need to write the equivalent of unit/end-to-end tests.

**Trigger questions:**

- "How do I write an eval?"
- "How do I test my workflow?"
- "How do I assert that a tool was called with specific params?"
- "My eval is failing, how do I debug it?"
- "How do I test that the bot stays silent?"
- "How do I run evals in CI?"
- "How do I seed state before an eval?"
- "How do I trigger a workflow in an eval?"

## Available Documentation

| File                             | Contents                                                                                                      |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `references/eval-format.md`      | Complete file format — all fields, turn types, assertion categories, match operators, setup, outcome, options |
| `references/testing-workflow.md` | Running evals, interpreting output, using traces, the write → test → iterate loop, CI integration             |
| `references/test-patterns.md`    | Per-primitive patterns for actions, tools, workflows, conversations, and state                                |

## How to Answer

1. **Writing an eval** → Read `eval-format.md` for structure and assertions
2. **Running evals** → Read `testing-workflow.md` for CLI commands and output
3. **Testing a specific primitive** → Read `test-patterns.md` for the relevant section
4. **Debugging a failure** → Combine `testing-workflow.md` (inspect traces) + `eval-format.md` (check assertion syntax)

---

## Quick Reference

### Eval file structure

```typescript
import { Eval } from '@botpress/evals'

export default new Eval({
  name: 'greeting',
  type: 'regression',
  tags: ['basic'],

  setup: {
    state: { bot: { welcomeSent: false } },
    workflow: { trigger: 'onboarding', input: { userId: 'test-1' } },
  },

  conversation: [
    {
      user: 'Hi!',
      assert: {
        response: [{ not_contains: 'error' }, { llm_judge: 'Response is friendly and offers to help' }],
        tools: [{ not_called: 'createTicket' }],
        state: [{ path: 'conversation.greeted', equals: true }],
      },
    },
  ],

  outcome: {
    state: [{ path: 'conversation.greeted', equals: true }],
  },

  options: {
    idleTimeout: 60000,
    judgePassThreshold: 4,
  },
})
```

### Turn types

| Turn                  | When to use                                    |
| --------------------- | ---------------------------------------------- |
| `user: 'message'`     | Standard user message                          |
| `event: { payload }`  | Push a custom event (arrives as `chat:custom`) |
| `expectSilence: true` | Assert bot does NOT respond                    |

### Assertion categories

| Category   | What it checks                                              |
| ---------- | ----------------------------------------------------------- |
| `response` | Bot reply text (contains, not_contains, matches, llm_judge) |
| `tools`    | Tool calls (called, not_called, call_order, params)         |
| `state`    | Bot/user/conversation state (equals, changed)               |
| `workflow` | Workflow execution (entered, completed)                     |
| `timing`   | Response time in ms (lte, gte)                              |

### CLI commands

```bash
adk evals                        # run all evals
adk evals <name>                 # run one eval
adk evals --tag <tag>            # filter by tag
adk evals --type regression      # filter by type
adk evals --verbose              # show all assertions
adk evals --format json          # JSON output for CI

adk evals runs                   # list recent runs
adk evals runs --latest          # most recent run
adk evals runs --latest -v       # with full details
```

---

## Critical Patterns

✅ **Every turn needs `user` or `event`**

```typescript
// CORRECT
{ user: 'hello', expectSilence: true }
{ event: { payload: { kind: 'payment.failed' } }, expectSilence: true }
```

❌ **`expectSilence` alone is not a valid turn**

```typescript
// WRONG — missing user or event
{
  expectSilence: true
}
```

---

✅ **Assert tool params to verify correct extraction**

```typescript
// CORRECT — verifies the LLM extracted the right values
{ called: 'createTicket', params: { priority: { equals: 'high' } } }
```

❌ **Only asserting the tool was called**

```typescript
// INCOMPLETE — doesn't verify params were correct
{
  called: 'createTicket'
}
```

---

✅ **Use `outcome` for post-conversation state and workflow assertions**

```typescript
// CORRECT — final state checked once after all turns
outcome: {
  state: [{ path: 'conversation.resolved', equals: true }],
  workflow: [{ name: 'ticketFlow', completed: true }],
}
```

---

✅ **Seed state to test conditional behavior without running setup turns**

```typescript
// CORRECT — start in a known state
setup: {
  state: {
    user: { plan: 'pro' },
    conversation: { phase: 'support' },
  },
}
```

❌ **Using conversation turns to set up state (slow and fragile)**

```typescript
// WRONG — depends on the bot correctly processing setup turns
conversation: [
  { user: 'I am on the pro plan' }, // hoping bot sets user.plan
  { user: 'I need help with billing' }, // actual test turn
]
```

---

## Example Questions

**Writing evals:**

- "Write an eval that tests my createTicket tool is called with the right priority"
- "How do I assert that the bot stays silent after an internal event?"
- "How do I test a multi-turn conversation where context is retained?"

**Running evals:**

- "How do I run only regression evals?"
- "How do I see which assertions failed and why?"
- "How do I integrate evals into GitHub Actions?"

**Debugging:**

- "My eval says the tool wasn't called but I think it was — how do I check?"
- "How do I inspect what the bot actually did during an eval?"

**Per-primitive:**

- "How do I test a workflow that uses step.sleep()?"
- "How do I test that state changed from the seeded value?"

---

## Response Format

**Match depth to the question.**

### Simple questions ("what assertions are available?", "how do I run evals?")

Answer directly — show the relevant table or CLI command. Don't generate a full eval file for an informational question.

### Writing an eval

1. Show the complete `new Eval({})` call with realistic field values
2. Include imports (`import { Eval } from '@botpress/evals'`)
3. Briefly explain non-obvious assertions — skip if the assertion is self-explanatory
4. Suggest the CLI command to run it: `adk evals <name>`

### Debugging a failing eval

1. Ask for or show the failing assertion (`expected` / `actual` diff)
2. Suggest opening traces in the Dev Console to see what the bot did
3. Identify whether the issue is in the eval assertion or the bot's behavior
