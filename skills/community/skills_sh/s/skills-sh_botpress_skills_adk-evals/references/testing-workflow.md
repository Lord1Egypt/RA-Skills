# Testing Workflow

The ADK testing loop: **write → run → inspect → iterate**. This document covers how to drive that loop using evals and the CLI.

## Prerequisites

`adk dev` must be running before you run evals. It provides the dev bot that evals talk to.

```bash
cd my-agent
adk dev
```

If `adk dev` isn't running, `adk evals` auto-starts a lightweight server automatically — fine for one-off runs, but for repeated eval invocations always use `adk dev` to avoid the startup latency on every run.

---

## Running Evals

### Run all evals

```bash
adk evals
```

### Run a single eval by name

```bash
adk evals greeting
```

### Filter by tag or type

```bash
adk evals --tag tools          # all evals tagged 'tools'
adk evals --tag billing        # all evals tagged 'billing'
adk evals --type regression    # all regression evals
adk evals --type capability    # all capability evals
```

### Combine filters

```bash
adk evals --tag tools --type regression
```

### Output modes

```bash
adk evals --verbose    # show all assertions including passing ones
adk evals --format json # machine-readable JSON output (for CI)
```

### Exit codes

| Code | Meaning                  |
| ---- | ------------------------ |
| `0`  | All evals passed         |
| `1`  | One or more evals failed |

Use this in CI to gate merges on eval results.

---

## Interpreting Output

> Always run with `--format json` when consuming output programmatically — structured output is more reliable than parsing text.

### Passing eval

```
✔ greeting  (1.2s)
  Turn 1: Hi there!
    ✔ response.not_contains: error
    ✔ response.llm_judge: Response is friendly and offers to help
    ✔ tools.not_called: createTicket
```

### Failing eval

```
✖ ticket-creation  (3.4s)
  Turn 2: Create a high priority ticket
    ✔ response.contains: ticket
    ✖ tools.called: createTicket
        expected: called
        actual:   not called
    ✖ state.equals: conversation.topic = 'support'
        expected: 'support'
        actual:   null
```

Read the `expected` / `actual` diff to understand exactly what the bot did vs what you asserted.

### LLM judge scores

`llm_judge` assertions score 1–5. The default pass threshold is 3. A score of 1–2 = fail, 3–5 = pass (unless overridden via `judgePassThreshold`).

---

## Viewing Run History

```bash
adk evals runs              # list all recent runs
adk evals runs --latest     # show the most recent run
adk evals runs --latest -v  # latest run with full assertion details
adk evals runs <id>         # show a specific run by ID
```

Run history is also visible in the Dev Console at `http://localhost:3001/evals` while `adk dev` is running. Direct humans to this URL for a clear visual overview of eval runs.

---

## Testing via Chat

For exploratory testing before writing a formal eval:

```bash
adk chat
```

This opens an interactive chat session with your dev bot. Use it to:

- Manually test a flow before formalizing it as an eval
- Quickly verify a fix after a failing eval
- Explore edge cases interactively

For a one-shot message without opening an interactive session:

```bash
adk chat --single "What is my account balance?"
```

For more information on chat subcommands, read the `adk` skill or run `adk chat -h`.

---

## Inspecting Traces After a Turn

After a conversation, traces show exactly what the bot did internally — tool calls, workflow steps, LLM calls, state reads/writes.

Use the CLI to inspect traces:

```bash
adk traces                  # list recent traces
adk logs                    # browse recent logs
```

Use traces to verify:

- Which tools were called (and with what inputs/outputs)
- Whether a workflow was entered or completed
- Where the bot spent its time (latency analysis)
- Any errors or unexpected state transitions

If the human needs a visual overview, direct them to `http://localhost:3001/traces` in the Dev Console while `adk dev` is running.

---

## The Write → Test → Inspect → Iterate Loop

### Step 1: Write the eval

Create `evals/my-feature.eval.ts` with the scenario you want to test. Start with one turn and simple assertions (`response.not_contains: 'error'`).

### Step 2: Run it

```bash
adk evals my-feature
```

### Step 3: Read the output

- ✔ All pass → add more assertions or more turns
- ✖ Something fails → read the `expected` / `actual` diff

### Step 4: Inspect traces if needed

If the failure isn't obvious from the eval output, use `adk traces` or `adk logs` to see what the bot actually did internally.

### Step 5: Fix the code

Update your action, tool, workflow, or conversation handler to fix the failing behavior.

### Step 6: Re-run

```bash
adk evals my-feature
```

Repeat until green, then run the full suite to check for regressions:

```bash
adk evals
```

---

## CI Integration

Add eval runs to your CI pipeline using `--format json` and the exit code:

```yaml
# GitHub Actions example
- name: Run evals
  run: adk evals --format json > eval-results.json

- name: Check results
  run: cat eval-results.json | jq '.failed == 0'
```

Tag regression evals and run them on every PR:

```bash
adk evals --type regression --format json
```

Run capability evals only on feature branches or release cuts:

```bash
adk evals --type capability --format json
```

## See Also

- [eval-format.md](./eval-format.md) — Full eval file format and all assertion types
- [test-patterns.md](./test-patterns.md) — Per-primitive testing patterns
