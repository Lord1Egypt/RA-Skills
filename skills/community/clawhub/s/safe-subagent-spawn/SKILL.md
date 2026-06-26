---
name: safe-subagent-spawn
description: |
  Safely create and manage subagents through a strict wrapper instead of calling sessions_spawn directly. Use whenever a task needs a subagent, detached helper, or delegated worker. Mandatory for all models when creating a subagent. Supports multi-round continuity via shared context files with full-text history.
---

# Safe Subagent Spawn

Use this skill whenever you need to create a subagent. Do **not** call `sessions_spawn` directly.

## Hard Rules

1. **Never call `sessions_spawn` directly.** Always use `scripts/safe_subagent_spawn.py` to generate the payload.
2. Enforced invariants (built into the script):
   - `runtime`: "subagent"
   - `mode`: "run"
   - `thread`: false
   - `cleanup`: "keep" (preserve sessions to expose subagent issues)
   - `streamTo`: never included
3. **NEVER confuse `agentId` with `model`.** `agentId` must be a real agent id from `agents.list[].id` — never a model alias or `provider/model` string.
   - `agentId` is optional and rarely needed. Omit it unless the user explicitly names a target agent that exists in `agents.list[].id`.
   - To select a model, use the `model` field.
   - ✗ `agentId: "google/gemini-2.5-pro"` — **WRONG!!** this is a model string
   - ✓ `agentId: "main"` — correct, a real agent id
   - ✓ omit `agentId` entirely — correct default
4. The parent agent must **never read** a context file after creating it. Use `scripts/append_to_context.py` for all appends. The parent tracks each context file by its task slug (visible in the file's Metadata section and filename) and file path.
5. No summary mechanism. Every child output is preserved verbatim.
6. Context files are permanent and must not be deleted.
7. **Multi-round tasks are strictly sequential.** The parent must wait for the child to return (Step 4) before appending a new directive and spawning the next round (Step 5). Never spawn round N+1 before receiving round N's output, unless the wait times out.
8. **No automatic retry on timeout.** If a subagent times out, the parent must stop the task and report the timeout to the user. Do not silently retry or spawn a replacement subagent.
9. **Task slugs must use only `a-z`, `0-9`, and `-`** (lowercase ASCII letters, digits, and hyphens). Must start and end with an alphanumeric character. Maximum 48 characters. The script validates this and rejects invalid names — no silent transformation.

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/create_context.py` | Create a new context file (initial metadata + background + first directive) |
| `scripts/safe_subagent_spawn.py` | Generate a spawn payload from an existing context file |
| `scripts/append_to_context.py` | Append a directive, child output, or external message to a context file |

> All `scripts/` paths are relative to this skill's installation directory.

## Context File Reuse — Same Task vs New Task

When spawning a subagent, the parent must decide whether to **reuse an existing context file** or **create a new one**.

**Reuse the existing context file** when:
- The new subagent is a continuation of the same logical task.
- The new subagent needs the output of a prior subagent to proceed.
- The user's request is a follow-up or iteration on a previous delegation.

**Create a new context file** when:
- The task is unrelated to any prior subagent delegation.
- The task requires a clean context with no prior history.
- A different user request introduces a separate objective.

When in doubt, create a new file. Unnecessary context is worse than missing context.

## Workflow

### 1. New task — create context file

```bash
scripts/create_context.py \
  --task "descriptive-task-slug" \
  --background "the user's original request or relevant background" \
  --directive "clear instructions for the child agent"
```

`--directive` is optional. Omit it to create a context file with only metadata and background — useful when you need to collect information (via External Messages) before formulating the first directive. A context file without a directive cannot be spawned until a directive is appended (the spawn script enforces this).

Output (stdout): the absolute path to the newly created context file.

### 1b. (Optional) Deferred directive — collect information first

If the context file was created without `--directive`, append External Messages to supply information before defining the task:

```bash
scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role external-message \
  --content "information gathered from an external source"
```

When ready, append the first directive:

```bash
scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role directive \
  --content "instructions for the child agent, informed by the external messages above"
```

Then proceed to Step 2 to generate the spawn payload.

### 2. Generate spawn payload

The context file must contain at least one Directive section. The script validates this and rejects files that have no directive.

```bash
scripts/safe_subagent_spawn.py \
  --context-file "<context_path>" \
  --timeout-seconds 300
```

Optional parameters:
- `--child-model "provider/model-name"` — Override the child agent's model. Maps to the `model` field (string, optional) of `sessions_spawn`, overriding the parent's default model.
- `--agent-id "agent-name"` — Target a specific agent id (must come from `agents.list[].id`). Rarely needed — omit unless the user explicitly names an existing agent.

`--timeout-seconds` should be determined by the parent agent based on task complexity. Default is 300 seconds. Use a shorter value for simple tasks and a longer value for complex ones.

Output (JSON): the spawn payload. Use it directly when calling `sessions_spawn`. Do not modify or add fields.

### 3. Spawn the subagent

Pass the JSON output from Step 2 directly to `sessions_spawn` as the complete argument:

```
sessions_spawn(<complete JSON payload from Step 2>)
```

Do not manually decompose or reassemble fields. The script output is the ready-to-use payload.

### 4. After child returns — record output

Append the child's **full verbatim output** to the context file:

```bash
scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role child-output <<'CHILD_EOF'
<full verbatim child output>
CHILD_EOF
```

For very long output, use a temp file instead:

```bash
# Write output to temp file first, then append
scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role child-output \
  --content-file /tmp/child_output.txt
```

### 5. (Optional) Append external messages

External messages can be appended in two positions:

- **Before the first directive** — when the context file was created without `--directive`, to supply information before formulating the first task (see Step 1b).
- **Between a Child Output and the next Directive** — to feed incremental information into subsequent rounds.

If the parent has incrementally obtained information (e.g., streaming results, user replies, external API responses), append it as external messages **before** appending the next directive:

```bash
scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role external-message \
  --content "first piece of information"

scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role external-message \
  --content "second piece of information, appended to the same section"
```

External messages have no round numbers and no timestamps. Multiple consecutive appends are merged into a single `## External Message` section — no new header is created until the next directive starts a new round.

External messages can only appear (1) after Background and before the first Directive, or (2) between a Child Output and the next Directive. The script enforces this ordering.

### 6. Continue task — append directive and spawn next child

If the task requires another round, append a new directive and spawn:

```bash
# Append new directive
scripts/append_to_context.py \
  --context-file "<context_path>" \
  --role directive \
  --content "new instructions for the next round"

# Generate spawn payload (same as Step 2)
scripts/safe_subagent_spawn.py \
  --context-file "<context_path>" \
  --timeout-seconds 300
```

Then spawn using the output payload (same as Step 3).

The next child reads the entire context file — including all prior directives and child outputs — and executes the **latest** directive.

## Append Format

`scripts/append_to_context.py` auto-detects round numbers and appends structured entries:

```md
---

## Directive — Round 2 — 2026-04-02T12:00:00+00:00

<parent's instructions for this round>

---

## Child Output — Round 2 — 2026-04-02T12:05:00+00:00

<full verbatim output from child agent>
```

For external messages (no round number, no timestamp; consecutive appends merge into one section):

```md
---

## External Message

<first piece of information>

<second piece of information, appended without a new header>
```

Content can be provided via:
- `--content "inline text"` — for short directives
- `--content-file /path/to/file` — for long content stored in a file
- stdin (heredoc) — for piping content directly

**Deduplication:** If the content being appended is identical to the latest existing entry of the same role, the script silently discards the duplicate and exits successfully (exit code 0).

## Context File Format

All context files are stored by default under `sub-agents/` in default workspace folder, named `{timestamp}-{task-slug}.md`.

When `--directive` is omitted during creation, the file initially contains only Metadata, Standing Instructions, and Background. External Messages and the first Directive are appended later via `append_to_context.py`.

```md
# Subagent Context: {task-slug}

## Metadata
- Created: {ISO-8601 timestamp}
- Task: {task-slug}
- Context File: {absolute path}

## Standing Instructions
- Do not self-append or modify this file. It is read-only context provided by the parent.
- Do not spawn additional subagents inside this subagent. All delegation must come from the parent.

## Background
{user's original request or relevant background information}

---

## Directive — Round 1 — {ISO-8601 timestamp}

{clear instructions for the child agent}

---

## Child Output — Round 1 — {ISO-8601 timestamp}

{full verbatim output from child agent}

---

## Directive — Round 2 — {ISO-8601 timestamp}

{new instructions for the next round}

---

## Child Output — Round 2 — {ISO-8601 timestamp}

{full verbatim output from child agent}

---

## External Message

{incrementally appended information from parent, before next directive}

---

## Directive — Round 3 — {ISO-8601 timestamp}

{instructions that can reference the external messages above}
```

When the context file is created without a directive (deferred directive pattern), the initial portion looks like:

```md
# Subagent Context: {task-slug}

## Metadata
- Created: {ISO-8601 timestamp}
- Task: {task-slug}
- Context File: {absolute path}

## Standing Instructions
- Do not self-append or modify this file. It is read-only context provided by the parent.
- Do not spawn additional subagents inside this subagent. All delegation must come from the parent.

## Background
{user's original request or relevant background information}

---

## External Message

{information collected before the first directive}

---

## Directive — Round 1 — {ISO-8601 timestamp}

{instructions informed by the external messages above}
```

## Design Principles

- **Full-text append, no summaries.** Every child output is preserved verbatim. The parent never compresses or summarizes. Subsequent children read the complete history.
- **Parent never reads back.** The parent writes the initial file and appends entries via helper scripts. It never reads the file into its own context window. Helper scripts may read the file internally (e.g., to auto-detect round numbers), but this is transparent to the parent.
- **One file per logical task.** Multi-round tasks share a single context file. Unrelated tasks get separate files.
- **Permanent retention.** Context files are never deleted. They serve as a permanent audit trail.
- **Session compaction is safe.** Because context files are the persistent store for all subagent interactions, the parent's session can be compacted using the platform's default rules without losing information. Context files ensure continuity across compacted sessions.

## Error Handling

If any step in the workflow fails — script error, subagent timeout, or wrapper unavailable:

1. **Stop immediately.** Do not retry, work around, or guess at a fix.
2. **Report to the user in detail**: include the failed command, exit code, and full error output.
3. **Do not fall back** to calling `sessions_spawn` directly.
