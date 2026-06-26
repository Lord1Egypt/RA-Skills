---
name: adk-debugger
description: Systematic debugging for ADK agents — trace reading, log analysis, common failure diagnosis, and the debug loop.
license: MIT
---

# ADK Debugger Skill

## What is ADK Debugging?

Every ADK agent records its behavior as traces and logs — every conversation turn, tool call, LLM reasoning step, and error. These are the source of truth for understanding what your agent did and why.

The ADK CLI provides the tools you need to debug. Most diagnostic commands support `--format json`; use it for programmatic output. The exception is `adk dev`, which has no `--format` flag and uses `adk dev --non-interactive` for structured NDJSON output.

## When to Use This Skill

Use this skill when the developer asks about:

- **Bot not working** — not responding, wrong responses, unexpected behavior
- **Tool issues** — wrong tool called, tool errors, hallucinated parameters
- **Workflow problems** — stuck workflows, steps not executing, state issues
- **Reading traces/logs** — how to query, filter, and interpret debug output
- **LLM misbehavior** — hallucinations, refusals, looping, poor extraction
- **Build/deploy failures** — validation errors, schema mismatches
- **Config issues** — agent.json vs agent.local.json, integration setup
- **Post-fix verification** — confirming a fix worked, writing regression evals

**Trigger questions:**

- "My bot isn't responding"
- "The wrong tool was called"
- "My workflow is stuck"
- "How do I read traces?"
- "How do I check logs?"
- "The LLM is hallucinating"
- "Something broke after my last change"
- "My deploy failed"
- "`adk check` found errors"
- "Summarize this trace"
- "What happened in trace X?"
- "Give me an overview of this conversation turn"
- "Why did the bot do X in this trace?"
- "Walk me through what happened"
- "How do I debug this?"
- "Summarize this conversation"
- "Explain what happened in conversation X"
- "Why did the bot respond that way?"
- "Walk me through this conversation"
- "What went wrong in this conversation?"

## Available Documentation

| File                                  | Contents                                                                                                                                     |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `references/traces-and-logs.md`       | CLI debugging tools, log querying, trace structure, span types, `onTrace` hooks, reproduction with `adk chat`                                |
| `references/common-failures.md`       | Runtime failure patterns — validation, bot not responding, tool errors, workflow stuck, integration failures, build errors, config confusion |
| `references/llm-debugging.md`         | LLM behavior issues — wrong tool, hallucinated params, refusals, token limits, looping, reading model reasoning                              |
| `references/debug-workflow.md`        | The systematic 8-step debug loop: validate → reproduce → logs → traces → classify → fix → verify → prevent                                   |
| `references/trace-summarization.md`   | How to fetch, walk, and summarize traces as free-form natural-language narratives — adapting depth to context                                |
| `references/conversation-analysis.md` | How to summarize and explain full conversations — listing conversations, timeline analysis, correlating with traces, common patterns         |

## How to Answer

1. **"How do I read traces/logs?"** → Read `traces-and-logs.md` for CLI commands and trace structure
2. **Something is broken, known pattern** → Read `common-failures.md` for the matching failure pattern
3. **LLM is misbehaving** → Read `llm-debugging.md` for the matching behavior issue
4. **Systematic investigation needed** → Read `debug-workflow.md` and follow the 8-step loop
5. **"Summarize this trace" / "What happened?"** → Read `trace-summarization.md` for how to fetch, walk, and narrate traces
6. **"Summarize this conversation" / "Explain what happened"** → Read `conversation-analysis.md` for multi-turn conversation summaries and explanations
7. **After fixing, need to prevent regression** → Point to the `adk-evals` skill for writing evals

---

## Quick Reference

### The Debug Loop

```
symptom → validate (adk check) → reproduce (adk chat) → logs (adk logs) → traces (adk traces) → root cause → fix → verify
```

### CLI Commands (prefer structured output)

```bash
adk check --format json                         # offline validation
adk logs error --format json                     # recent errors
adk logs --follow --format json                  # stream live
adk traces --format json                         # recent traces
adk traces conversation=<id> --format json       # specific conversation
adk chat --single "msg" --format json            # test message
adk dev --non-interactive                        # structured NDJSON dev output (no TUI)
adk conversations --format json                  # list recent conversations
adk conversations show <id> --format json        # conversation timeline
adk conversations show <id> --include-llm --format json  # timeline with LLM reasoning
```

### Span Types

| Type                       | What It Shows                                        |
| -------------------------- | ---------------------------------------------------- |
| `think`                    | LLM reasoning — why it chose an action               |
| `tool_call`                | Tool invocation — name, input, output, success/error |
| `code_execution_exception` | Runtime error — message and stack trace              |
| `end`                      | Conversation turn completed                          |

---

## Prerequisites Check

Before debugging, verify:

- [ ] **Project valid?** Run `adk check --format json` — fix any reported issues first
- [ ] **Dev server running?** `adk dev` (or `adk dev --non-interactive` for structured NDJSON output)
- [ ] **Bot linked?** `agent.json` exists with `botId` and `workspaceId` (created by `adk link`)
- [ ] **Dev bot created?** `agent.local.json` has `devId` (set automatically by the first `adk dev` run)
- [ ] **Integration configured?** Check Dev Console at localhost:3001 for unconfigured integrations

---

## Critical Patterns

✅ **Run `adk check` before debugging runtime issues**

```bash
# CORRECT — catch config/schema problems offline first
adk check --format json
# Then debug runtime issues
```

❌ **Skipping offline validation**

```bash
# WRONG — jumping straight to runtime debugging wastes time on config issues
adk traces --format json  # might be chasing a config problem
```

---

✅ **Use `--format json` on all CLI commands**

```bash
# CORRECT — structured output for reliable parsing
adk logs error --format json
adk traces --format json
adk chat --single "test" --format json
```

❌ **Parsing human-readable output**

```bash
# WRONG — human-readable format is for display, not parsing
adk logs error
adk traces
```

---

✅ **Use `adk logs error` to filter errors**

```bash
# CORRECT — focused error scan
adk logs error --format json
adk logs warning since=1h --format json
```

❌ **Scrolling through all output**

```bash
# WRONG — too much noise, easy to miss the actual error
adk logs --format json  # 50 entries of everything
```

---

✅ **Use `onTrace` hooks for programmatic monitoring**

```typescript
// CORRECT — structured, automated trace analysis
hooks: {
  onTrace: ({ trace }) => {
    if (trace.type === 'tool_call' && !trace.success) {
      console.error(`[TOOL ERROR] ${trace.tool_name}`, trace.error)
    }
  }
}
```

❌ **Only checking console output**

```typescript
// WRONG — console.log in handlers misses the structured trace data
handler: async (input) => {
  console.log('tool called') // not useful for debugging
}
```

---

✅ **Write a regression eval after fixing**

```typescript
// CORRECT — prevents the bug from coming back
export default new Eval({
  name: 'fix-order-lookup',
  type: 'regression',
  conversation: [{ user: 'Look up order 123', assert: { tools: [{ called: 'lookupOrder' }] } }],
})
```

❌ **Fixing and moving on**

```
// WRONG — the same bug will return and you'll debug it again
```

---

## Example Questions

**Basic:**

- "My bot isn't responding — how do I figure out why?"
- "How do I check for errors in my ADK project?"
- "What's the difference between agent.json and agent.local.json?"

**Intermediate:**

- "The bot called createTicket instead of lookupTicket — how do I fix this?"
- "My workflow starts but the second step never runs"
- "How do I see what the LLM was thinking when it made a decision?"
- "Integration actions are failing with auth errors"

**Advanced:**

- "How do I set up onTrace hooks for automated error detection?"
- "The model loops on the same tool call — how do I add a guardrail?"
- "How do I monitor tool call performance with timing metrics?"
- "How do I systematically debug a multi-step workflow failure?"

---

## Response Format

**Match depth to the question.**

### Simple questions ("how do I check logs?", "what are trace spans?")

Answer directly — one sentence + the CLI command or concept. Don't run the full debug loop for informational questions.

### Active debugging ("my bot is broken", "X isn't working")

Follow the full loop:

1. **Check prerequisites** — verify dev server, config files, project validation
2. **Start with `adk check --format json`** — rule out offline issues
3. **Reproduce** — use `adk chat --single "msg" --format json` to create a clean reproduction
4. **Read the evidence** — `adk logs error --format json` for quick scan, `adk traces --format json` for details
5. **Identify the root cause** — point to the specific span, log entry, or config issue
6. **Suggest a targeted fix** — reference the appropriate failure pattern doc
7. **Verify** — re-run the reproduction, confirm clean output
8. **Write a regression eval** — load the `adk-evals` skill and generate the eval file automatically
