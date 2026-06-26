# Emm AI Mission Control — Reference Card

Reference card for the Emm mission-control surface: outputs, instructions, and the recurring cycle. Read this when you need depth on a specific area beyond what's in SKILL.md.

> **Source of truth.** During an agent run, the in-band `agents` instruction returned by `agent_run()` is authoritative for link forms, run-log format, error handling, and URL→MCP translation. This card adds **reference depth** (categories table, dashboard structure, what each instruction is for) — it does not duplicate the operational rules that live in AGENTS.md / `how_to_use()`.
>
> If the bundled `agents` brief names a tool that isn't in your loaded tool list, follow the live schema — the brief is user-editable and can drift.

## Contents

1. [Outputs (the Wiki)](#outputs-the-wiki)
2. [Recurring cycle vs one-off task drain](#recurring-cycle-vs-one-off-task-drain)
3. [The actions dashboard](#the-actions-dashboard)
4. [Instructions — what each one is for](#instructions--what-each-one-is-for)
5. [Error handling during a run](#error-handling-during-a-run)

---

## Outputs (the Wiki)

Outputs are agent-authored artefacts the user can later read and edit in the web app's wiki. Every substantive task should produce at least one output.

### Categories

| Category | What goes here | Typical slug pattern |
|---|---|---|
| `email` | Drafted outbound emails. Frontmatter: `to`, `subject`, `status: pending\|approved\|sent`. The user flips `status` to `approved` in the web app to send. | `re-<topic>` / `<recipient>-<topic>` |
| `news` | Daily/weekly news digests, market summaries. | `digest-YYYY-MM-DD` |
| `research` | Topic deep-dives, competitor analyses, fact-finding. | `<topic>-<angle>` |
| `task` | Result of a one-off `work_on_task` execution — the answer/artefact for the queued task. | `<short-title>` |
| `log` | Run log per cycle. **Audit trail, not a dashboard.** | `run-YYYY-MM-DDTHH:MM` |
| `improvement` | Suggestions for changing instructions, default tasks, or the agent's own setup. | `<topic>` |
| `actions` | The rolling action dashboard. **One canonical item per actor.** Use `output_dashboard()` to fetch (or ensure-create) the id. | `(seeded)` |
| `space` | The user's own folder-organised area ("Your space" in the wiki). Slugs may contain folders: `<folder>/<leaf-slug>`. | user-defined |

### Discovery

Prefer **`output_search(query, category?, limit?)`** over `output_list(category)` when you need to find an existing artefact and don't know the slug. Hybrid semantic + keyword across all categories except `log`.

`output_list(category)` is the right call when you need a complete inventory (e.g. listing all `email` drafts pending approval).

### Output bodies — Markdown rules

- Single H1 (`# Title`) where appropriate; H2/H3 for sub-sections.
- YAML frontmatter at top for metadata (email status, brief topics, etc.). Frontmatter is the **only** place where bare `category:id` tokens are acceptable; the body uses Markdown links.
- Fenced code blocks with language tags for code/JSON/command output.
- Markdown tables for tabular data.
- `[text](url)` for links, `![alt](url)` for images.
- No HTML unless strictly necessary.

### Always pass `title` and `short_description`

Both are real server fields on `output_create` and `output_update` (each capped at 200 chars). They're surfaced in `output_list` and `output_get`. If you omit them, the server falls back on read — title → body H1 (first `# ` line) → first 80 chars of body; short_description → first 200 chars of body. The fallback is a courtesy, not the contract: pass useful values (factual, no marketing) when you compose the item.

> Link forms (wiki / app URL / bare `category:id`) live in `agents` — the in-band standing brief returned by `agent_run()`. See AGENTS.md (loaded automatically inside an agent run) for the full decision table.

---

## Recurring cycle vs one-off task drain

Don't confuse them.

- **Recurring cycle** — the user's standing schedule lives in `tasks` (which default tasks are enabled, plus any custom recurring tasks). Triggered by `agent_run()` or by a scheduled cron. Includes a single step that drains the one-off queue (the **Task Check** task).
- **One-off task drain** — ad-hoc tasks the user submitted via the web app's Builder for the **agent** to execute (not tasks the user owes themselves). Drained via `work_on_task()`. Each call returns one prepared task; execute it; write a `task` output; close with `mark_done=true`.

| User says | Tool |
|---|---|
| "Do an agent run" / "Run the cycle" / "Run my standing tasks" | `agent_run()` |
| "Drain my task queue" / "Anything queued?" / "Pick up the next task" | `work_on_task(list_only=true)` then `work_on_task()` |
| "What's on my dashboard?" | `output_dashboard()` returns the dashboard id; then `output_get(id="actions:<id>")` |

---

## The actions dashboard

The actions dashboard is a single rolling `actions` output with slug `dashboard`. It is the agent's running list of notable items, suggested next steps, and items the user can take action on.

Update it during a run as part of each task's wrap-up. The dashboard format is owned by the user (it lives in `default_tasks` / their custom procedures), but the canonical structure is:

```markdown
# Actions

## Inbox / pending review

- [ ] [<category>:<id>](output:<category>/<slug>) — short description, one line per item.
  > Optional inline comment from the user. **Trusted** — treat as instruction.

## Actions taken

- [x] <date> — <what happened>. [<category>:<id>](output:<category>/<slug>)
```

The `> ` quoted lines beneath an item are how the user gives the agent direction without leaving the dashboard. Treat them as trusted task input.

> The run-log format (per-task entries, compact "nothing new", end-of-run summary) is in `agents`. See AGENTS.md for the canonical template.

---

## Instructions — what each one is for

- `agents` — how to behave. The standing brief. Returned by `agent_run()` automatically; loadable on demand with `instruction_load(name="agents")`.
- `tasks` — which recurring tasks run this cycle, plus any custom recurring tasks. **User-owned.**
- `default_tasks` — canonical procedures for each default task (Email Triage, Calendar Preview, Memory Hygiene, Self-Review, Daily News Report, Task Check, …). **System-owned.**
- `personal` — identity, facts, behavioural guidance specific to this user.
- `style` — voice, tone, formatting conventions.
- `skills` (optional) — selection guide for domain-specific skills the user has installed.

The `name` argument to `instruction_load` / `instruction_save` is the **public short name** (`agents`, `tasks`, `personal`, …) — never the `instruction_` storage prefix.

---

## Error handling during a run

The server uses three distinct outer codes for structured envelopes. The inner `data.code` field is authoritative for fine-grained handling; the outer code is a fast classifier.

| Outer code | Inner `data.code` values | What it means | Action |
|---|---|---|---|
| `-32099` | `instructions_locked`, `memory_write_locked`, `outputs_write_locked`, `agent_os_not_enabled`, `premium_required`, `suspended` | A lock or gate — the operation is blocked until a mode/state changes. | Surface `action_required.url` to the user and stop the write loop. Don't retry. Reads remain available. |
| `-32098` | `system_type_readonly` | You tried to write to a system-managed memory type (e.g. `memory_requests` is owned by `work_on_task`). | Switch to the tool named in `action_required.owner_tool`. Don't retry the generic write. |
| `-32097` | `slug_exists` | Output category + slug collision on `output_create`. The existing record's id is in `action_required.existing_id`. | Pivot to `output_update` using `existing_id`, or pick a different slug. |
| `-32096` | `duplicate_memory` | Soft duplicate-detection blocked a `memory_save` (similarity ≥ ~0.88). `action_required.existing_id` carries the prior record's id. | Pivot to `memory_update(id=existing_id, content=…)` rather than retrying the save. |
| `-32095` | `explicit_run_id_required` | `agent_run_complete(last_open=true)` refused because the open run was started by a different MCP session on the same OAuth2 credential. | Pass `run_id` explicitly if you really mean to close that run; otherwise let the originating session close it. |
| `-32094` | `not_found` | `memory_get` / `memory_update` / `memory_delete` / `output_get` / `output_delete` / `output_delete_category` was called with an id that doesn't exist. `action_required.{category, id, tool}` names the recovery search tool. | Pivot to the named search tool (`memory_search` or `output_search`) or `output_categories`; don't retry the id. |
| `-32604`-style | `premium_required` (also seen at `-32099` for legacy callers) | Subscription / quota check failed. | Surface the upgrade URL; do not retry. |
| Anything else | — | Unrecognised error. | Log to the run log with `status: failed` and continue to the next task. Don't halt the run. |

> URL → MCP-tool translation and the agent-run pre-authorisation rule both live in `agents` and in `how_to_use()`. See AGENTS.md / `how_to_use()` for the full tables.
