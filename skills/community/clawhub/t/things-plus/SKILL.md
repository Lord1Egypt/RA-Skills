---
name: things-plus
description: Personal task manager powered by Things 3. Trigger when the user asks to add, capture, review, organize, reprioritize, search, or manage tasks in Things. Also trigger when the user expresses a concrete personal future action or commitment, including natural planning phrases like "tomorrow I need to…", "I still need to…", "I should…", "remind me to…", "I've got to…", "don't let me forget…", or "help me note this down" — even when Things is not mentioned explicitly. Also trigger when the user asks for an end-of-day summary, work log, daily report, or asks to summarize what was done today and put it into Things.

Do NOT trigger for: hypothetical examples, quoted text, brainstorming about someone else's tasks, or vague general discussion without clear personal action intent.

Execution default: attempt writes directly; escalate to environment or auth checks only when a write actually fails.

metadata:
  openclaw:
    requires:
      bins:
        - things
    primaryEnv: THINGS_AUTH_TOKEN
---

# Things Plus

Use the `things` CLI to read from and write to the local Things 3 database.

**Credential policy:** `THINGS_AUTH_TOKEN` may be required for some operations in some environments (for example, certain update paths). Verify token presence via `things auth`; do not ask the user to paste it into chat.

## Setup

- Install: `brew install ossianhempel/tap/things3-cli`
- Ensure the install directory is on `PATH`.
- `THINGS_AUTH_TOKEN` must be set in the environment visible to the execution context (prefer `~/.zshenv` over `~/.zshrc` for background/agent use).
- Grant **Full Disk Access** to the calling app only if database reads fail or direct DB access is needed.

## Pre-flight

Run full pre-flight only on: explicit setup intent, or execution failures that suggest environment/auth/CLI issues. Do not block ordinary task capture on pre-flight.

```bash
mdfind 'kMDItemCFBundleIdentifier == "com.culturedcode.ThingsMac"' | head -5
which things && things --version
things auth
things today --json
```

Decision flow:
1. App missing → stop; ask user to install Things.app
2. CLI missing or broken → stop; reinstall via Homebrew
3. `things auth` fails → do not block ordinary add/read flows that still work directly; only pause token-gated operations and guide token setup if the requested action actually depends on token/auth (Things 3 → Settings → General → Things URLs). Verify presence with `things auth` in the same execution context before continuing
4. Auth present → proceed; do not treat `things auth` alone as proof writes work — verify with a real add/delete on a disposable item if write reliability is in question

**Token setup:** identify the active shell/context first (`echo $SHELL`), then give one exact command for the appropriate environment file. Prefer replacing an existing entry over appending a duplicate. Before asking the user about setup/auth/environment problems, first inspect the current execution context and try the smallest safe command that can confirm the actual behavior.

## Interface layer

Use the `things` CLI as the execution interface.

Most common reads:
- `things today --json`
- `things upcoming --json`
- `things search "query" --json`
- `things show --id <UUID> --json`

Most common writes:
- `things add "Title" --when tomorrow`
- `things update --id <UUID> ...`
- `things delete --id <UUID> --confirm <UUID>`

Use the smallest command that can safely confirm the current state.
Before risky mutations, prefer `search` and `show` to identify the exact item.
Verify every write by read-back instead of trusting exit status alone.

### Execution rules

- `add`: execute directly; no dry-run required
- `update`: use `--dry-run` first when the change is broad or risky
- `delete`: for clearly identified single-item deletions, execute directly (recoverable via trash) and verify by read-back; for ambiguous or broad deletions, clarify first
- Prefer UUID for mutations whenever available; do not rely on title-only matching when an exact UUID can be obtained
- Never claim success from exit code alone — verify every write with a read

### Duplicate prevention

Before `add`, do a quick duplicate check when the task title is generic or was mentioned earlier in the session:

```bash
things search "key phrase" --json
things createdtoday --json
```

If an open match exists, prefer updating by UUID. If intent is ambiguous, ask one brief clarifying question.

## Strategy layer

- Treat concrete personal planning phrases as capture intent; add directly without asking for confirmation
- For ambiguous intent (hypotheticals, someone else's plans, general discussion) — do not capture
- When the user mentions multiple distinct future actions in one message, split them into separate tasks unless they clearly belong to a single bundled action
- Use Things' native **Today / Upcoming / Anytime / Someday** views; do not invent extra taxonomy
- Only proactively surface **Today + nearest Upcoming** by default
- Rewrite titles for executability by default; preserve exact wording only when the user asks, the title is already action-ready, or verbatim capture is the point.
- When plans change, suggest re-prioritization; ask before moving anything to tomorrow

## Field policy

### `--when`
Use for any concrete or fuzzy time reference.
- Exact time → `--when "YYYY-MM-DD HH:MM:SS"`
- Fuzzy → morning `08:30` · noon `12:00` · afternoon `15:00` · evening `20:00` · before bed `23:00`
- Date only → `--when DATE`
- States → `today` · `tomorrow` · `evening` · `anytime` · `someday`

### `--deadline`
Use for latest acceptable completion date ("by Friday", "due Monday"). Not a substitute for `--when`. Set both when both apply.

### `--tags`
Add only when tags clearly improve retrieval. Default: 0–2 tags. Reuse existing tags; do not invent new ones.

### `--checklist-item`
Add only when the task has 2+ concrete sub-steps executed as a bundle. Max 5 items.

### `--repeat`
Use for recurring personal tasks in Things (weekly reviews, habit reminders, etc.). Use cron for background/system automation. Do not infer recurrence unless the user asks.

## Default workflow

For new task capture, always follow this order:
1. infer intent
2. rewrite the title into an executable action
3. decide the correct view or schedule
4. add the task
5. verify by read-back

Do not add first and rewrite later unless the user explicitly asks to preserve exact wording.

### 1. Rewrite vague titles into executable actions
Before creating a task, rewrite vague, exploratory, or topic-like titles into the next visible executable action whenever possible. Do not preserve the user's original wording if it is too vague to act on directly.

Treat titles as needing rewrite if they are mainly about:
- learning something broadly
- understanding a topic without a concrete output
- looking into, exploring, or checking something without a defined action or decision
- reviewing a resource without a clear next step
- naming a topic area rather than an action

If the title still reads like a topic, intention, or area of study rather than an action, rewrite it again before adding.

Examples:
- `buy groceries` → `make grocery list and place order`
- `work on presentation` → `draft first 5 slides`
- `email John` → `reply to John with requested details`
- `learn harness engineering` → `outline the basic concepts of harness engineering`
- `check the Datawhale tutorial` → `decide whether the Datawhale tutorial is worth following`
- `read the Claude skill guide` → `read the Claude skill guide and extract key points`

### 2. Rewrite learning and research tasks toward a concrete next action
For learning, research, review, or exploration requests, convert broad titles into a concrete next action.

Prefer titles that describe:
- reading or reviewing a specific resource
- extracting key points
- writing notes or a short summary
- comparing whether a resource is worth following
- outlining the basic concepts or framework

### 3. Route to the correct view
- Today → clearly for today
- Upcoming → has a date/deadline/near-term commitment
- Anytime → important but unscheduled
- Someday → ideas, reading lists, later-maybe

### 4. Apply metadata deliberately
Only set `--when`, `--deadline`, `--tags`, or `--checklist-item` when the user's input actually warrants it. Default is a clean, simple task.

### 5. Daily report / logbook capture
When the user asks for a daily summary, work log, end-of-day report, or asks to summarize what was done today and put it into Things:
- default to one completed todo with a concise title for the day or theme, plus a short checklist of the main outcomes
- use multiple completed todos only when the day clearly contains several unrelated threads
- summarize from available session context or memory instead of asking the user to restate the whole day unless key details are missing
- treat the day as a small number of themes, not a raw transcript
- preserve outcomes, decisions, validations, and deliverables; skip micro-steps
- if writing after midnight, warn the user it will land in the current day's Logbook

## Error handling

Start with: `things today --json`

- If output is empty or fails to parse:
- run `things tasks --json --limit=3`
- if that is still broken, report CLI/database trouble

- If `things auth` is empty:
- enter token setup flow only for operations that actually depend on token/auth
- do not block ordinary add/read flows that still work directly

- If a UUID is not found:
- re-run `things search` to relocate the exact item

- If a write appears to succeed but the data is unchanged:
- trust the read-back, not the exit status
- check in this order:
1. token/auth requirement for that specific operation
2. shell/environment visibility
3. Things URL permission

- If delete reports success but the item still appears:
- retry after a short pause
- suspect AppleScript instability before assuming auth failure

**Recovery:** never create a replacement task because an update failed. Fix auth/UUID first, then retry the original operation.

## Tone
- Direct and calm
- Collaborative triage, not productivity doctrine
- Explain before postponing; ask before moving to tomorrow