# Tool Surface — parameter detail & status() field reference

The full tool list with parameter shapes and batch limits, plus the
`status()` return fields SKILL.md's Quick Reference and Session check don't
spell out. **The live tool schema always wins over this file** — it is a
convenience index, not the contract; if a schema and this page disagree,
follow the schema.

## Contents

1. [Memory](#memory)
2. [Outputs — the Wiki](#outputs--the-wiki)
3. [Instructions](#instructions)
4. [Recurring cycle](#recurring-cycle)
5. [One-off task drain](#one-off-task-drain)
6. [Shared Memories](#shared-memories)
7. [Remote Actions](#remote-actions)
8. [status() — non-safety fields](#status--non-safety-fields)

---

## Memory

- `memory_search()` — keyword/semantic search; supports `last_n`, `recency_days`, `include_remote`. `include_remote=true` requires the once-per-conversation user ask — see [shared memories](shared-memories.md).
- `memory_get()` — retrieve memory details by ID; `id` for one, `ids=[…]` for a batch.
- `memory_save()` — store new memories; `content` for one, `items=[…]` (up to 25) for a batch, auto-categorized. `preview=true` to preview before writing.
- `memory_update()` — change one memory's content by ID. **Single `id` only** — there is no batch form; update several by calling it once per memory.
- `memory_delete()` — remove by ID; `id` for one, `ids=[…]` (up to 25) for a batch.
- `memory_move(id, target_type)` — move a memory to another category; pass `ids=[…]` (up to 25) to move several to the same target in one call. Each item gets a new ID; Emm rewrites inline **canonical** references (`work:40`, wiki links, app URLs) across memories, outputs and instructions, and the response carries the old → new ID mapping. The response also lists documents that mention a moved ID in **free text** (e.g. "memory 40"), which the rewriter cannot safely touch — fix those by hand. Write cross-references as canonical tokens (`memory_work:40`) from the start so future moves keep them in sync.
- `memory_types()`, `memory_create_type()`, `memory_delete_type()` — manage categories.
- `how_to_use()` — personalized guide. Heavy; call it on first interaction, not every session.

## Outputs — the Wiki

- `output_search(query, category?, limit?)` — hybrid semantic + keyword search across categories. Excludes `log` — use `output_list(category="log", recency_days=N)` instead.
- `output_list(category)` — list items in a category.
- `output_get(id="<category>:<id>")` — fetch one item with full body.
- `output_create(category, slug, title, content, short_description, ...)` — create.
- `output_update(id="<category>:<id>", ...)` — modify. Pass the `updated_at` you read as `if_match` and a write that lost the race is refused with `revision_conflict` (carrying the current revision) instead of clobbering the other edit.
- `output_move(id="<category>:<id>", folder?, slug?, target_category?)` — relocate a document **without sending its body**. Use this, not `output_update`, whenever the body is not changing: `output_update` requires the full content, so re-foldering a set would pull every body through the conversation twice and a write cut short by a context limit stores a truncated document. Pass `ids=[…]` (up to 25) to send several to the same destination; `slug` and `if_match` name a single document and are refused alongside `ids`. Pass `folder` and `slug` together to re-folder and rename in one call; if the slug itself carries a folder, an explicit `folder` wins. A folder or slug change **within the document's own category** keeps its ID, so `output:<category>/<id>` links keep resolving; `target_category=…` mints a new ID — every entry in `moves[]` says which happened via `id_preserved`. Either way it rewrites links in **other** documents' bodies that named the old path, to the canonical `output:<category>/<id>` form, so the next relocation has nothing to repair; free-text mentions it cannot safely touch come back in `prose_candidates` to fix by hand, and links written with a name that matches more than one document come back separately in `ambiguous_links` — those are left alone deliberately, because guessing which document was meant would silently repoint the others.
- `output_delete(id="<category>:<id>")` — remove (rarely; prefer update). Pass `ids=[…]` (up to 25) to delete several at once; per-item failures are isolated, so one not-found doesn't abort the rest. Optionally pass the `updated_at` you read as `if_match` to have the delete refused (`revision_conflict`) rather than remove an item someone else has since edited — **single `id` only**, since a revision token describes one item; combining it with `ids=[…]` is rejected.
- `output_dashboard()` — fetch or ensure-create the singleton actions dashboard.
- `output_categories()` — list the categories that currently exist (defaults + any custom ones). Call before minting a new category to avoid near-duplicates.

## Instructions

- `instruction_list()` — list installed instructions, incl. `maintained_by` (`emm`/`user`) and `update_available`.
- `instruction_load(name)` — load one by short name (`agents`, `tasks`, `default_tasks`, `personal`, `style`).
- `instruction_merge_preview(name)` — preview the 3-way merge for a doc with a pending update (or a self-diff if none). Call before saving an update.
- `instruction_save(name, content, ...)` — write a standing instruction. Pass `applied_update: true` when incorporating a reviewed update, or `apply_clean_merge: true` to accept a clean merge without re-sending the body.
- `instruction_delete(name)` — remove a standing instruction.

## Recurring cycle

- `agent_run()` — full cycle entry point. Returns instructions + dashboard state in-band; execute immediately.
- `agent_run_complete(run_id=...)` — call once the cycle finishes to clear the in-progress marker.

## One-off task drain

- `work_on_task()` — get one context-prepared ad-hoc task; `list_only=true` to peek; `mark_done=true, task_id=ID` to close.

## Shared Memories

- `memory_search(include_remote=true)`, `list_connections()` — see who shares what.
- Ask the user once per conversation before searching remote memories. Remember the answer for the rest of that conversation; ask again next session. Attribute matches: *"Alice mentioned …"*

See [shared memories](shared-memories.md) for patterns.

## Remote Actions

- `list_connections()`, `describe_method()`, `execute_method()`.
- Confirm with the user before executing unfamiliar methods.

See [remote actions](remote-actions.md) for patterns.

---

## status() — non-safety fields

The run-lifecycle fields (`runs`, `mode`, `suggested_actions`, `unlock_window`)
are safety-relevant and stay documented in SKILL.md's Session check — read
them there. The remaining fields:

- `limits.memory_max_kb` — per-memory body cap (defaults around 400 KB). Check before attempting a large `memory_save`.
- `limits.outputs_per_category` — per-category soft cap (defaults around 500). The `log` category has a lower cap — `limits.outputs_per_category_log` (defaults around 100). Beyond either, suggest the user prune.
- `links.help_page` — absolute URL to the user's in-app help page (the user-facing companion to this skill's content). Give it to the user when they ask where to read more in the web app; don't try to fetch it yourself.
- `links.app_home` — absolute URL to the user's web app root. Use when the user asks to "open Emm" without a specific destination.
- `tools_recommended` — names of the Emm tools this skill assumes will be available. Treat it as an informational contract from the server, not a prescription to drive your MCP loader. If a name on the list isn't in your live tool list, your host will surface it when you actually need it (deferred-loading clients) or it really is unavailable; don't try to second-guess your platform's loading mechanism.
- `your_client_has_only_used_reads` — server observed your client only making read calls. If `true`, mention it to the user once: "I'm only seeing reads on this connection — if you intended writes, your MCP client may need permission adjustments."

`status().conventions` — display rules, link forms, attribution cap, search freshness — mirrors SKILL.md's Display Rules table live; see SKILL.md for the full table with examples.
