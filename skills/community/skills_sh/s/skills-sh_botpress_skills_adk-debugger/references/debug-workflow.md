# Systematic Debug Workflow

A step-by-step process for diagnosing and fixing issues in ADK agents. Follow these steps in order — each step narrows the problem space.

Most diagnostic CLI commands use `--format json` for structured, parseable output. Make sure `adk dev` is running in the background, once the project is validated.

---

## The Debug Loop

```
1. VALIDATE  → adk check --format json
2. REPRODUCE → adk chat --single "msg" --format json
3. LOGS      → adk logs error --format json
4. TRACES    → adk traces --format json
5. CLASSIFY  → Runtime error? LLM behavior? Config issue?
6. FIX       → Apply targeted fix
7. VERIFY    → Re-test with adk chat, confirm clean output
8. PREVENT   → Write a regression eval
```

---

## Step 1: Validate

Before debugging runtime behavior, rule out project-level issues.

```bash
adk check --format json
```

This catches:

- Invalid `agent.config.ts`
- Schema mismatches in actions, tools, workflows
- Invalid entity names
- Missing dependencies
- Import errors

If `adk check` reports errors, fix them first. Many "runtime" issues are actually build/config problems.

---

## Step 2: Reproduce

Create a minimal reproduction with a single message.

```bash
adk chat --single "the message that triggers the bug" --format json
```

**Why minimal?** A single message isolates the problem. Most often, multi-turn conversations add noise — the issue might be in turn 3 but caused by context from turn 1. That being said, some bugs are only reproducible by going through many turns.

**Pushed-event or proactive bug?** `adk chat --single` only sends user text — it can't push a `chat:custom` event. Reproduce with an eval `event` turn (`event: { payload: {...} }`) and run `adk evals`; don't curl the chat webhook.

**Save the conversation ID** from the JSON output — you'll need it for trace queries and follow up conversations.

If the issue requires multi-turn context:

```bash
# First message
adk chat --single "Setup message" --format json
# Note the conversation_id from output

# Trigger the bug
adk chat --single "Bug-triggering message" --conversation-id <id> --format json
```

---

## Step 3: Check Logs

Quick scan for errors and warnings.

```bash
# Errors only
adk logs error --format json

# Errors and warnings from the last hour
adk logs warning since=1h --format json

# Stream live while reproducing
adk logs --follow --format json
```

Logs give you a high-level view. If the error is obvious here (startup failure, integration auth error, missing config), fix it directly.

If logs don't explain the issue, move to traces.

---

## Step 4: Inspect Traces

Traces show everything the agent did during a conversation turn.

```bash
# All recent traces
adk traces --format json

# For a specific conversation
adk traces conversation=<id> --format json
```

**Read spans in order.** Look for:

1. **`think` spans** — Does the model's reasoning make sense? Does it understand the user's intent?
2. **`tool_call` spans** — Was the right tool called? Did it succeed? Are the parameters correct?
3. **`code_execution_exception` spans** — Any runtime errors? Read the stack trace.
4. **`end` span** — Did the turn complete normally?

**Find the divergence point:** Compare what happened vs what should have happened. The first span that doesn't match expectations is usually where the bug is.

---

## Step 5: Classify the Failure

Based on what you found in logs and traces, classify the issue:

### Runtime Error

The code threw an exception or returned an error.

- **Traces show:** `code_execution_exception` or `tool_call` with `success: false`
- **Next:** See `common-failures.md` for specific patterns and fixes

### LLM Behavior

The model made a bad decision — wrong tool, hallucinated values, refusal, or looping.

- **Traces show:** `think` span with incorrect reasoning, or `tool_call` with wrong tool/params
- **Next:** See `llm-debugging.md` for diagnosis and fixes

### Config Issue

Missing or incorrect configuration — integration auth, agent.json, environment.

- **Traces show:** May not have traces at all, or errors mentioning config/auth
- **Logs show:** Startup errors, auth failures, missing config warnings
- **Next:** See `common-failures.md` sections on config, integration failures, and agent.json vs agent.local.json

---

## Step 6: Fix

Apply a targeted fix based on the classification:

| Classification           | Where to Fix                               | Reference                                    |
| ------------------------ | ------------------------------------------ | -------------------------------------------- |
| Runtime error in handler | Action/tool/workflow handler code          | `common-failures.md`                         |
| Schema mismatch          | Input/output schema definitions            | `common-failures.md` § Build Errors          |
| Wrong tool selected      | Tool descriptions, instructions            | `llm-debugging.md` § Wrong Tool              |
| Hallucinated params      | Input schemas, validation                  | `llm-debugging.md` § Hallucinated Parameters |
| Model refusal            | Instructions, tool descriptions            | `llm-debugging.md` § Refusal                 |
| Model looping            | `onBeforeTool` guard, output clarity       | `llm-debugging.md` § Looping                 |
| Integration failure      | Dev Console config, `adk integrations add` | `common-failures.md` § Integration Failures  |
| Config issue             | `agent.json`, `agent.local.json`           | `common-failures.md` § Config Confusion      |

---

## Step 7: Verify

Re-run the exact reproduction from Step 2:

```bash
adk chat --single "the message that triggered the bug" --format json
```

Then confirm:

```bash
# No errors in logs
adk logs error --format json

# Traces show correct behavior
adk traces --format json
```

Check that:

- The bot responds correctly
- The right tools are called with the right parameters
- No error spans in the traces
- No new warnings in logs

---

## Step 8: Prevent with Evals

After fixing, write a regression eval so the bug can't come back. Use the **adk-evals** skill for full guidance.

Quick template:

```typescript
import { Eval } from '@botpress/evals'

export default new Eval({
  name: 'fix-description-here',
  type: 'regression',
  tags: ['bugfix'],

  conversation: [
    {
      user: 'the message that triggered the bug',
      assert: {
        response: [{ not_contains: 'error' }, { llm_judge: 'Response correctly handles the scenario' }],
        tools: [{ called: 'expectedTool' }],
      },
    },
  ],
})
```

Run it:

```bash
adk evals fix-description-here --format json
```

Tag regression evals as `type: 'regression'` so they run in CI and catch future regressions.

---

## When to Escalate

If you've gone through the loop and still can't resolve the issue, gather this information for a bug report:

```bash
# Project validation
adk check --format json > check-output.json

# Recent errors
adk logs error --format json > error-logs.json

# Traces from the failing conversation
adk traces conversation=<id> --format json > traces.json
```

Include:

1. **Reproduction steps** — exact messages/events that trigger the issue
2. **`adk check` output** — project state
3. **Error logs** — relevant error entries
4. **Trace output** — full trace with spans for the failing conversation
5. **Expected vs actual behavior** — what should happen vs what does happen
6. **ADK version** — `adk --version`

Let the human know and suggest reaching out to support with the above information.
