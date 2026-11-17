# Changelog

All notable changes to the **Working with Emm AI** skill (ClawHub slug: `working-with-emm`; previously published under `managing-actingweb-memory`).

## [2.5.0] — 2026-08-21

### Added

- **`output_move` — relocating a wiki document without sending its body.**
  `output_update` requires the full content, so re-foldering a set of
  documents meant reading every body out and writing it back: a large job did
  not fit, and a write cut short by a context limit stored a truncated
  document rather than failing. `output_move` carries path metadata only, in
  both directions, one document or up to 25 per call. The ID guarantee is
  stated per branch — a folder or slug change **within** the document's own
  category keeps the ID, `target_category` mints a new one, and every entry in
  `moves[]` says which happened via `id_preserved`. Links in *other*
  documents' bodies that named the old path are repaired to the canonical
  `output:<category>/<id>` form, so the next relocation has nothing left to
  repair; free-text mentions the rewriter cannot safely touch come back in
  `prose_candidates`.

- **`batch_too_large` (`-32091`) in the error-code table.** Every batch tool
  (`memory_save`, `memory_delete`, `memory_move`, `output_move`,
  `output_delete`) now enforces a 25-item cap server-side, rejecting the whole call before any
  item is written — previously the declared limit was advertising only, and an
  oversized batch simply ran. The new row states the cap, that nothing was
  applied, and that recovery is to split and re-send *every* item rather than
  assume a prefix went through.

### Fixed

- **The documented outer-code range was stale.** Three places said errors run
  `-32099` through `-32092`; `batch_too_large` sits at `-32091`, so an agent
  hitting it would not have found it in the table.
- **`revision_conflict` is no longer described as outputs-only.** It can now
  arrive as a per-item result inside a `memory_delete` batch when that memory
  changed between the batch's read and its delete. The row explains the memory
  case separately and warns that this is *not* `not_found` — the item still
  exists, so searching for a replacement is the wrong move.
- **`memory_save`'s batch limit is now stated.** It was the only batch tool
  whose entry gave no cap, while `memory_delete`, `memory_move` and
  `output_delete` all said "up to 25".

## [2.4.0] — 2026-08-17

### Added

- **A troubleshooting section.** New "When Emm isn't responding" section with
  a direct answer for missing tools, structured tool errors, and the
  Claude.ai client-side approval-gate denial — previously reachable only by
  chance, from a deep link inside another section.
- **`references/tool-surface.md`** — the full per-tool parameter reference
  and `status()`'s non-safety field reference, split out so the always-loaded
  part of the skill stays a behavioural guide, not a schema dump.
- **`license: MIT-0`** and **`compatibility:`** frontmatter fields, matching
  how this skill is actually distributed (open on ClawHub, requires the Emm
  AI MCP connector).

### Fixed

- **The `instructions_locked` error row now points at
  `instruction_request_update_window()`** — the old wording told the agent
  to ask in chat, which never notified the account owner.
- **The `run_not_open` error row no longer tells the agent to start a fresh
  cycle.** The correct recovery is to re-issue the same write without
  `run_id` — starting a new cycle to recover from one surplus argument was
  needlessly expensive.
- **The `log` category's soft cap was misreported as 500** (same as every
  other category); it's actually 100. `status()` and this skill now agree.
- **`instruction_merge_preview`'s conflict response now warns against
  blind-saving the auto-draft** — the data-loss rule was previously only in
  this skill, not in the tool response itself.
- **`if_match` now sits next to the re-read rule it enforces.** "Re-read
  immediately before you update" named the habit but not the mechanism,
  which was documented only in the session-check block an agent may never
  revisit mid-run. The tool-surface reference also gained `if_match` on
  `output_update` and `output_delete` — including that `output_delete`
  accepts it with a single `id` only, never alongside `ids=[…]`.
- **`agent_run_complete`'s `last_open` parameter no longer contradicts its
  own tool description.** It claimed the refusal depended on which MCP
  session started the run; it actually fires whenever more than one run is
  open account-wide, whoever started them.
- **The error-envelope code range** quoted in the References table and in §1
  said `-32099` / `-32098` / `-32097`; the table it points at runs through
  `-32092`.
- **The tool reference promised a batch `memory_update` that doesn't exist.**
  Condensing two tools into one line extended `memory_delete`'s `ids=[…]` form
  to `memory_update`, which takes a single required `id` — so following the
  reference produced a call the server rejects. The two now have separate
  entries, and `memory_update` says single-`id`-only outright.
- **The link-form table was missing both memory forms.** Linking to a memory
  from an output body, or from an MCP response, was documented only in
  Display Rules as a worked example — so the table you'd actually consult to
  answer "what form do I use here?" had four of the six answers. It now has
  all six, and its Form column is consistently placeholder notation (the
  bare row reads `<category>:<id>` rather than `category:id`) with the worked
  example beside it.

### Changed

- **`Available Tools` is now a compact per-pillar table**; parameter detail
  moved to the new tool-surface reference.
- Trimmed internal repetition (the reinstall nudge, the `full_id`
  convention, the shared-memory consent rule) down to one canonical
  statement each, adding a dedicated Critical Rules row for shared-memory
  consent so it isn't lost in the process.
- **This CHANGELOG is now trimmed to the current version plus the last few**
  — full history moved to the ActingWeb repository (`docs/CHANGELOG-skill-archive.md`),
  out of the distributed bundle.
- **SKILL.md now has a size budget, enforced in CI.** This is the first
  release in the skill's recorded history that removes more than it adds.
  A ratchet in the ActingWeb repository's test suite caps SKILL.md just
  above its current size, so future growth has to clear the bar
  deliberately rather than accumulating unnoticed — which is what happened
  over the twelve preceding releases.

## [2.3.0] — 2026-08-03

### Fixed

- **`agent_run` returns its bundle again.** Tools now declare whether their
  answer is prose or structured data, instead of the server guessing. Some
  clients discard every text block whenever a response carries structured
  fields, so `agent_run` — whose entire payload is the standing-orders bundle —
  had been answering with nothing but a run id since the field was added.
  A plain `work_on_task()` retrieve was losing its task brief the same way.

### Changed

- **Where to read each answer.** `agent_run` and a plain `work_on_task()`
  retrieve are **prose**: read the response text; they carry no structured
  fields. `agent_run_complete`, `work_on_task(list_only=true)`,
  `work_on_task(mark_done=true)`, `status`, and every memory / output /
  instruction tool are **structured**: read `result.structuredContent`. Note
  the nesting is preserved as it always shipped —
  `result.structuredContent.output.id` for `output_create`, not
  `.structuredContent.id`.
- The `run_id` for `agent_run_complete` comes from the `agent_run` response
  **text** — the `**Run ID:**` preamble line, or the
  `agent_run_complete(run_id="…")` reminder at the end.

### Added

- **`instruction_save` reports two signals as fields**, not only in prose:
  `window_closed` (Instructions-Update Mode was turned off by this save) and
  `server_merged` (a clean 3-way merge was applied server-side). Both are
  always present, so a `false` is distinguishable from a missing field.

## [2.2.0] — 2026-07-30

### Changed — breaking

- **`status().runs.open` is now a list**, not a single object or `null`, and is
  accompanied by `runs.open_count`. Several runs can be open at the same time,
  so "the open run" no longer names one thing. Skills reading
  `runs.open.started_by_client_id` will get `undefined` rather than a wrong
  answer — reinstall to pick up the new shape.
- **The coordination rule is inverted.** Previous versions said *"don't start a
  competing run; talk to the user before forcing close."* Overlapping runs are
  now supported and expected: a scheduled Autopilot run and an interactive one
  can both be open. Proceed with your own run, expect shared surfaces (the
  dashboard, the wiki, the task queue) to change under you, and close only the
  run you started.
- **`agent_run_complete(last_open=true)` acts only when exactly one run is open
  account-wide.** If anything else is open it refuses with
  `-32095 explicit_run_id_required` and names the candidates — even when one of
  them looks like yours. The server cannot always tell two clients apart, and
  it will not guess with a live cycle at stake. Pass the `run_id` from your own
  `agent_run()` response: the by-id close is exact and never depends on caller
  identity. Treat `last_open` as a convenience for the single-run case.

### Added

- **`if_match` on `output_update` / `output_delete`.** Pass the `updated_at` you
  read and a concurrent edit is refused with `-32093 revision_conflict` —
  carrying the item's current revision — instead of being silently clobbered.
  Worth using on the dashboard, which more than one run may rewrite per cycle.
- **`run_id` on output writes and `work_on_task`.** Optional; a write carrying a
  run that has been closed or has expired is refused with `-32092
  run_not_open`. `agent_run` now returns `run_id` as a top-level field, so it
  need not be re-read out of the bundle — record it, because it is the reliable
  way to close your own run when several are open.
- **Tasks are leased on hand-out** (60 minutes). Two runs draining the queue get
  different tasks. `list_only` marks a claimed task `claimed: true` while still
  reporting it `ready`; `has_ready_task` counts only unclaimed ones. The server
  applies this on every hand-out, though it is a read-then-write check, so it
  narrows the duplicate window rather than sealing it.

### Fixed

- A matching `started_by_client_id` is **not** proof a run is yours: two
  sessions of one registered client share it and the server cannot tell them
  apart. Unless you hold the `run_id` from your own `agent_run()`, treat a
  same-client run as someone else's.
- Closing an already-abandoned run no longer flips it back to `done`.
- A run left open is swept to `abandoned` after a 3-hour deadline — there *is*
  now a server-side path that closes a run on its own, contrary to what earlier
  versions of this skill stated.
- The end-of-cycle order is stated consistently everywhere: run log, close,
  then dashboard and memory.

## [2.1.6] — 2026-07-06

Native self-improvement lifecycle. The self-review → standing-instruction
loop is now something the AI can complete on its own, at parity with the web
app — no more hand-holding through every step of applying a proposal.

The old "user-owned" vs "system-owned" framing is gone. Every instruction is
yours to edit; the only distinction left is **who ships baseline updates**,
surfaced as `maintained_by` (`emm` or `user`) on `instruction_list()` and
`instruction_load()`. `emm`-maintained docs (like `agents`, now on that
channel) show an "update available" flag and merge your edits in on apply —
they're never silently overwritten.

### Added

- **`instruction_merge_preview(name)`** — see the 3-way diff between your
  current version, your edits, and a pending baseline update before you touch
  anything. Returns a rendered diff plus the structured strategy
  (`clean` / `conflict`) and per-hunk conflicts.
- **One-call clean applies.** When a pending update merges cleanly,
  `instruction_save(name=..., apply_clean_merge: true)` applies it without
  re-emitting the body. On a conflict, resolve each hunk yourself and save with
  `applied_update: true` — the skill's new **Improvement lifecycle** section
  walks the find → route → apply → retire loop, and guards refuse a no-op or a
  blind conflict apply so you can't clear "update available" without actually
  merging.
- **`status()` improvement playbook.** In Instructions-Update Mode, `status()`
  now returns an ordered, tool-named checklist (review self-reviews → apply
  pending updates → rationalize tasks) plus an `unlock_window` block telling you
  how long the window has left and which writes are paused.
- **Deterministic custom tasks.** The `tasks` doc gained a real
  checklist → numbered-definition wiring for your own recurring tasks, matching
  how default tasks already work — tick a task on, and its procedure ships in
  the cycle bundle.
- **Instruction change history (web app).** Each instruction now records who
  changed it and how, with created/updated timestamps and a read-only view of
  the previous body — so "why did this change?" has an answer.

### Changed

- **Clearer update & reset UX (web app).** Emm-maintained and "Yours" badges,
  a non-destructive "a newer default is available — your version is untouched"
  framing, and an always-available per-doc "Reset to default" (confirm-gated),
  so you never have to reach for a reset-everything button to fix one file.
- **Skill-update reinstall nudge is channel-neutral** — it points you to
  reinstall however you originally added the skill (bundle, plugin, or
  registry) rather than naming one source.

## [2.1.4] — 2026-06-12

Added a rule to re-read each output or memory immediately before
updating it. A cycle can run for many minutes, and if you edit a
document in the web app partway through, the agent could otherwise
write back the older copy it loaded at the start and wipe your change.
The agent now re-fetches the current version right before saving and
merges its update onto your latest text — so concurrent edits no
longer collide. Matters most for the action list and rolling trackers.

Also made the "skill out of date" nudge channel-neutral: it no longer
tells you to reinstall "from ClawHub" specifically (that's only one of
several install paths — re-uploading the bundle, reinstalling the
plugin, or pulling from a skill registry all apply depending on how
you added it).

Full history before 2.1.4 lives in `docs/CHANGELOG-skill-archive.md` in the
ActingWeb repository — not shipped in this bundle.
