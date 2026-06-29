---
name: research-mode
description: Run durable long-running research in OpenClaw using isolated cron iterations, persistent state, bounded execution, and milestone updates. Use when the user wants background research that can continue for hours or days, pause/resume/stop cleanly, accumulate sources/findings over time, and produce a final report instead of a single one-shot answer.
---

# Research Mode

Use this skill for **long-running research workflows**, not for ordinary one-shot questions.

Use it for:
- background research that should continue across hours or days;
- gradual source/finding accumulation;
- pause/resume/stop control over a durable task;
- review-gated final reports or deliverables;
- follow-up research based on an approved result.

Do **not** use this skill for:
- quick one-shot summaries;
- a single web/search lookup;
- ordinary coding tasks;
- ad-hoc analysis that fits in one normal turn;
- tasks that do not need durable state, cron iteration, or review-loop.

## Core model

Do **not** treat durable research as one giant prompt or one endless session.
Use:
1. a research task directory under `research/`;
2. `state.json` as the control plane;
3. append-only artifacts (`sources.jsonl`, `findings.jsonl`, `iterations/*.md`);
4. isolated cron scheduling for repeated bounded work.

Main helper:

```bash
python3 scripts/research_mode.py --help
```

Current hardened baseline:
- task ids are safe single path segments;
- explicit task paths are constrained to the selected research root;
- approval and delivery files must live under the task directory;
- research adequacy must pass before finalization;
- `awaiting_review` means review-ready, not delivery-ready;
- helper-code changes must pass `scripts/check_research_mode.sh` from the package root.

## Default workflow

1. **Create or start** a task with the helper.
   - Use `create` when you want to inspect/attach/prepare first.
   - Use `start` when you want create + schedule in one step.
2. **Schedule isolated work** with the helper cron flow.
3. Each worker iteration must do exactly one bounded cycle:
   - `begin`
   - stop immediately on `skipped` / `paused` / final states
   - do one focused iteration
   - write result JSON
   - `finish`
   - `fail` if the leased iteration breaks
4. Use `summary` / `preflight` / `health` / `reconcile` / `draft-report` / `status`
   for operator inspection instead of manually stitching files.
5. Use `pause` / `resume` / `stop` and working-memory mutation helpers instead of hand-editing state.

## Command families that matter

### Task lifecycle
- `create`
- `start`
- `schedule`
- `begin`
- `finish`
- `fail`
- `pause`
- `resume`
- `stop`
- `unschedule`

### Operator/query surfaces
- `list`
- `status`
- `summary`
- `preflight`
- `health`
- `reconcile`
- `queue-status`
- `draft-report`
- `render-prompt`
- `prepare-runtime`

### Recovery handoff
- `recover --apply-pending-result`
- `recover --refresh-derived`

### Review and delivery
- `approve`
- `request-changes`
- `reopen`
- `mark-delivered`
- `format-delivery`

### Steering / working memory
Prefer helper mutation commands over direct `state.json` edits:
- `mutate-working-memory`
- `add-angle`
- `add-constraint`
- `add-instruction`
- `set-deliverable`

If there is exactly one active non-final task, user-facing commands can omit `--id`. If several are active, the helper should fail loudly and require explicit targeting.

## Corpus helpers

Use corpus helpers when the task should carry local/web material across isolated iterations.

Available helpers:
- `attach-input --file ...`
- `attach-input --dir ...`
- `attach-input --glob '.../**/*.md'`
- `attach-note --title ... --text ...`
- `attach-url-as-md --url ...`
- `attach-pdf --file ...`

Image files attached through `attach-input` are preserved in the corpus manifest and marked with `content_hint=image`, so future `begin` work orders can recognize them as visual inputs rather than generic files.

These helpers should remain **lightweight**:
- update manifest/provenance;
- make attached material visible in future `begin` work orders;
- avoid turning `research-mode` into a heavy ingestion platform.

## Runtime / local analysis

If deeper coding or local data work is needed, use `prepare-runtime` and keep generated scripts/exports/datasets under the task-local `workspace/`.
Install extra Python packages only into the task-local runtime, not globally.

Recommended task-local layout after `prepare-runtime`:
- `workspace/analysis/` — one-off analysis scripts and code notebooks-in-files
- `workspace/tools/` — tiny task-specific helpers/utilities
- `workspace/data/` — intermediate structured inputs / normalized datasets
- `workspace/outputs/` — derived tables, JSON, CSV, reports
- `workspace/outputs/screenshots/` — raw screenshots and saved visual captures
- `workspace/outputs/vision/` — derived vision notes / visual interpretations / auxiliary artifacts
- `workspace/tmp/` — disposable scratch artifacts
- `workspace/data/analysis.sqlite` — optional task-local SQLite store for structured analysis
- `workspace/analysis/schema.sql` — SQLite schema used for this task when DB is helpful
- `workspace/analysis/queries/` — saved SQL queries / views / exports

Treat code as a **first-class helper** when it improves accuracy, scale, or reproducibility, especially for:
- parsing / extraction
- structured data cleanup
- deduplication / comparison
- scoring / ranking
- calculations / aggregations
- corpus-wide transforms

Treat SQLite as an equally valid helper when the task becomes structured and query-heavy, especially for:
- repeated filtering / segmentation
- deduplication / entity resolution
- joins across normalized records
- aggregation / ranking / queue generation
- coverage/accounting layers over many observations

Before creating task-specific SQLite tables, the worker should explicitly decide:
1. the 1–3 core entities;
2. their relationships;
3. likely dedup keys;
4. provenance fields (`source_id`, `captured_at`, `note`, `confidence` where relevant).

Keep the schema minimal first. Prefer a small task-fit schema over premature over-modeling.

If code materially influenced the iteration result, the worker should:
1. save the relevant script/output under the task-local workspace;
2. report `code_used=true` in the result payload;
3. list durable artifacts via `analysis_artifacts`;
4. record any important runtime deps in `packages_used`.

If SQLite materially influenced the iteration result, the worker should also:
1. report `database_used=true` in the result payload;
2. list DB/schema/query/export files via `database_artifacts`;
3. summarize DB purpose/tables/row counts via `database_summary`.

Treat vision/image analysis as another first-class helper when the task includes screenshots, maps, charts, dashboards, UI states, photos, or user-provided images.
If visual evidence materially influenced the iteration result, the worker should:
1. report `vision_used=true` in the result payload;
2. list screenshots / visual artifacts via `vision_artifacts`;
3. summarize the visual purpose via `vision_summary`.

Use vision as a helper, not as the sole source of truth when a stronger structured/text path exists.

Do **not** turn a bounded research iteration into open-ended product engineering. Prefer the smallest reproducible code path that answers the question.

Current package policy: `prepare-runtime --package` may install arbitrary task-local pip packages. This is intentional for now. Do not claim strict production package governance until an allowlist/lock policy exists.
Do not install dangerous or suspicious packages without checking their source, necessity, and install-time behavior first. If a package looks unusual or risky, record the decision/risk in the iteration instead of treating the install as routine.

## Search stack defaults

- For **RU / regional / local-business / SERP-harvesting** research, prefer regional/local search or SERP tools before synthesis-first search.
- Use discovery tools to gather candidate sites/resources/lists, then follow direct sources with whatever tools fit the case.
- Use synthesis-first search later for broader context, summarization, or international cross-checking.
- When the task is local and a city/region is known, include it explicitly in the query rather than relying only on abstract intent.
- Write user-facing summaries and final deliverables in the same language as the user's goal/instructions unless the user asks for another language.

## User updates

Send updates only when there is real value:
- task started;
- milestone reached;
- blocker / user input needed;
- final result ready.

Avoid a message on every cron tick.
When helper output returns `notify_user=true`, prefer the returned `update_text` instead of inventing a fresh one.
If the task runs under the default isolated cron setup with internal-only delivery, use `delivery_intent` as the handoff contract: send pending intent text through the available messaging surface, then call `record-notification` with `sent` or `failed`, and reply `NO_REPLY` in the cron run.
For chat-launched tasks, bind the owner at `create` / `start` time with `--channel`, `--chat-id`, and when needed `--thread-id` / `--topic-id`. Use `--no-owner` only when notifications are intentionally disabled; otherwise a missing owner should remain visible as `notification_blocked:missing_owner`.

## Current hardened behavior

### Operator-facing surfaces
`summary`, `runs.tsv`, and `task-playbook.md` are now the primary inspectable operator surfaces.
Prefer them over manual artifact spelunking.
Finalization surfaces include `operator_next_action` so the operator can distinguish
review-ready candidates from worker rework and human-intervention states without
reverse-engineering validation findings.

### Terminal reasons
Statuses stay simple (`idle`, `running`, `paused`, `complete`, `failed`, `cancelled`), but lifecycle output may also expose normalized reasons such as:
- `completed:worker`
- `completed:budget`
- `completed:topic_saturated`
- `stopped:user`
- `failed:blocker`
- `failed:error-threshold`
- `rejected:completion-validation`

### Deliverable-aware completion checks
Completion validation is intentionally lightweight but inspectable. It may reject completion when the requested output shape is clearly not satisfied (for example weak bullet-list/comparative/overview structure).

### Research adequacy gate
Do not treat finalization as the place to discover whether the research itself is incomplete.
Before a task can move to finalization, the worker must pass through `phase=verify` and report `result.adequacy`.

The adequacy check is about the accumulated research, not report polish:
- does the evidence answer the user's goal;
- were explicit constraints and user instructions accounted for;
- is the requested deliverable shape understood;
- are important open questions resolved or intentionally judged nonblocking;
- is the evidence base diverse enough for the task;
- are coverage gaps, evidence risks, and contradictions recorded honestly.

If the research is not sufficient, set `result.adequacy.status` to the appropriate state:
- `needs_research` -> return to `search`;
- `needs_analysis` -> return to `analyze`;
- `needs_synthesis` -> return to `synthesize`;
- `needs_user_input` -> pause for user/operator input;
- `needs_intervention` -> require operator inspection.

Only set `result.adequacy.status="passed"` when the research can responsibly move to `finalize`. Lifecycle code owns attempt counters, routing, and `operator_next_action`; worker-provided adequacy fields are candidate claims, not trusted control decisions.

### Human-ready finalization
Do not treat a task as truly final just because a report file exists.
Before calling a result user-ready, make sure the primary deliverables are human-facing rather than internal-agent scaffolding:
- avoid presenting draft-named artifacts as the final output when the task is marked complete;
- avoid final reports that mainly point to internal workspace paths without giving a human-readable synthesis;
- if needed, produce a polished final report and final-named deliverables before presenting the task as done.
- if the deliverable is a file, do not make the user hunt for it in workspace paths when the platform can attach/send it or when a clear delivery path can be provided.
- if the result is too long for a convenient chat reply, package it deliberately: concise summary in chat + full file/report as attachment or clearly named artifact.

For worker-initiated completion, `result.finalization` is mandatory evidence, not a decorative note. Before setting `should_complete=true`, the worker must record:
- `status="passed"`;
- inferred user need, intended recipient, and primary deliverable kind;
- internal artifacts versus candidate user-facing artifacts;
- blocking and nonblocking defects found during recipient-style review;
- revisions made after self-review;
- validation evidence showing what was actually checked.

If `result.finalization.status` is missing / `not_started`, blocking defects remain, validation evidence is empty, or a raw workspace artifact is exposed as the final result, `finish` must route the task back to `finalize` / rework instead of `awaiting_review`.

Finalization also performs lightweight candidate artifact inspection:
- candidate artifact paths must stay inside the task directory;
- existing candidate artifacts must exist and be regular files;
- generated `final-report.md` can be validated from `final_report_markdown` before the file is committed;
- Markdown candidates are checked for basic readable structure;
- `.xlsx` candidates must be openable as workbook ZIPs with workbook/sheet entries.

These hooks are deliberately lightweight. They prove that the declared deliverable is inspectable, not that every domain-specific quality requirement has been solved.

`summary --format json`, `summary --format text`, and `task-playbook.md` expose the
next operator action for finalization:
- `review_candidate` — inspect the candidate deliverable and use `approve` or `request-changes`;
- `worker_rework` — let the next worker turn repair failed finalization checks;
- `operator_intervention` — inspect repeated or explicit finalization failures before continuing;
- `verify_review_state` — finalization passed, but the task is not in the expected review gate;
- `continue_research` — no passing finalization evidence exists yet.

`summary --format json` also exposes `operator_attention` for execution-health
conditions that should wake an operator or watcher even when lifecycle status is
still `running`, such as a stale active run with or without a pending result.
Treat `operator_attention.status != "ok"` as actionable.

### Review-ready vs delivery-ready
Do not collapse review state and delivery state:
- `delivery.review_ready=true` means there is an artifact ready for review.
- `delivery.ready=true` means the artifact is ready for user delivery.
- Worker finalization to `awaiting_review` sets review readiness, not delivery readiness.
- `approve` or `mark-delivered --ready` is the normal route to delivery readiness.

### Integrity markers
Successful `finish` writes `transactions.finish.status=committed` with the run id and iteration. If a stale worker left `.tmp/result-<run-id>.json` without calling `finish`, use `recover --apply-pending-result`; valid results are applied through the normal finish path and then marked consumed.

## Execution discipline

- One run = one bounded iteration.
- Worker iterations are serialized per research root by the global iteration queue.
- A `begin` response with `status=skipped` and `normalized_reason=deferred:global-research-lock` is normal queue waiting, not a failed worker turn.
- A `begin` response with `status=recovered` means a stale pending result was applied; the next tick may acquire a fresh lease if more work remains.
- Use `queue-status`, `status`, or `summary` to inspect the active holder and waiters before attempting recovery.
- `state.json` remains the source of truth.
- Research task ids must be safe single path segments; never use `/`, `\`, `.`, `..`, or path traversal in ids.
- `--path` must point to a task under the selected `--root`; do not operate on arbitrary filesystem paths.
- Review and delivery artifacts must live under the task directory. If an external file is relevant, attach/copy it into the task workspace first.
- For XLSX deliverables, do not combine a worksheet-level `autoFilter` and an Excel Table over the same range. Use a table filter or a plain worksheet filter, not both; review-ready XLSX candidates are checked with strict OOXML compatibility validation.
- Before changing the helper code, run or update tests first. Before calling code changes complete, run `scripts/check_research_mode.sh` from the package root.
- Do not bypass path containment by symlink or absolute path. The helper validates resolved paths; if it rejects a path, move/copy the artifact into the task workspace.
- Do not rely on chat memory between cron iterations.
- Persist important context explicitly into task artifacts.
- Record no-progress iterations honestly (`meaningful_progress=false`).
- Keep future changes lightweight; do not silently redesign the platform.

## Development / verification gate

For helper-code or skill-contract changes, run:

```bash
scripts/check_research_mode.sh
```

The gate covers:
- `compileall`;
- `ruff`;
- `pyright`;
- auto-discovered selftests;
- pytest-compatible `scripts/selftest/`.

If `pyright` or `pytest` are not installed but `uv` is available, the script runs them through `uvx`.

## Review handoff rules

When a research task reaches `awaiting_review`, the lifecycle enters a **review-gated** state. The following rules are mandatory:

### What happens automatically
- `begin` short-circuits on `awaiting_review` — cron will not acquire a new lease until the operator resolves the review.
- The task status remains `awaiting_review` and surfaces display it explicitly.
- The active cron job is **disabled** while the task waits in `awaiting_review`, so isolated turns stop consuming tokens.
- The job binding is preserved in `history.last_job_binding`, allowing clean resumption after approval or changes request.
- `request-changes` / `reopen` re-enable the bound job when possible; if the task had already been approved and its old job was removed, `reopen` recreates a fresh cron job from the saved schedule template.

### Required operator transitions
To move a task out of `awaiting_review`, use exactly one of:
- **`approve`** — mark the deliverable as accepted and move to `complete`.
- **`request-changes`** — record feedback and return the task to `idle` for runner rework.
- **`reopen`** (from `complete`) — return a completed task to `idle` for further work.
- **`stop`** — cancel the task; also removes the job binding.

Command shape:
```bash
python3 scripts/research_mode.py approve --id <research-id>
python3 scripts/research_mode.py request-changes --id <research-id> "what to change"
python3 scripts/research_mode.py reopen --id <research-id>
```

**Do not** use `pause`/`resume` as a substitute for the review transition. `resume` only restores tasks from `paused` state, not from `awaiting_review`.

For plain `paused` tasks the same execution-layer rule now applies: pausing disables the bound cron job, and `resume` enables it again.

### Forbidden operator actions (hard boundaries)
The following are **never acceptable** without an explicit `manual_override outside research flow` audit marker:
1. Manually editing `final-report.md`, `workspace/*`, `delivery.primary_file`, or other task artifacts after `awaiting_review`.
2. Using side-run sessions or ad-hoc file surgery to mutate deliverables without going through the lifecycle.
3. Telling the user the task is complete when only a runner rework is needed — use `request-changes` instead.
4. Polling `begin` in a tight loop while waiting for user input — the task stays in `awaiting_review` with an inspectable `review_gated` flag.
5. Using `approve` when the user requested changes — always use `request-changes`.

### Manual override semantics
Only when the user **explicitly** requests intervention outside the research flow:
1. Mark the action with an `audit_marker: "manual_override"` in the state history.
2. Record the reason and what was changed.
3. Return to the normal lifecycle as soon as possible.

### Before responding to the user
Verify that:
- Feedback was written to task state via the appropriate transition command.
- The task status reflects the correct transition (`idle`, `complete`, `cancelled`).
- `delivery.review_ready`, `delivery.ready`, `delivery.primary_file`, and `review.status` are consistent with what the user was told.
- Delivery paths are task-local and point to real files when telling the user a file is ready.

## Linked research — universal continuation mechanism

When a completed research task should serve as the basis for a new, related investigation, use `create-linked-research`. This is the generic mechanism for launching a follow-up research task — not a business-specific preset, but a universal linked-task builder.

### When to use it
- After an approved result, to investigate a sub-angle or unresolved question.
- To run a deeper phase of analysis on the same topic.
- To shift focus (e.g., from search to synthesize or compare) while building on prior work.

### Command
```bash
python3 scripts/research_mode.py create-linked-research \
  --id <source-task-id> \
  --goal "Проверить гипотезу о ..." \
  [--title "Фаза 2 — углублённый анализ"] \
  [--relation phase-2] \
  [--instruction "..."] \
  [--constraint "..."] \
  [--open-question "..."] \
  [--carry-summary] \
  [--carry-open-questions] \
  [--carry-constraints] \
  [--carry-deliverable] \
  [--carry-approved-artifact]
```

### Carry-forward policy
By default, the linked task is **clean**: it starts fresh and only carries an explicit reference to the source. Use flags to selectively transfer context:
- `--carry-summary` — copy the source's working summary into the new task's working memory.
- `--carry-open-questions` — forward open questions from the source.
- `--carry-constraints` — forward hard constraints.
- `--carry-deliverable` — inherit the requested deliverable/output shape.
- `--carry-approved-artifact` — record paths to approved artifacts from the source task.

### Constraints on carry-forward
- Carry-forward is **opt-in per flag**. No data is transferred unless explicitly requested.
- The linked task is a **new research task**, not a continuation of the source. It gets a fresh `status`, `progress`, `lock`, and `corpus`.
- The source task remains `complete` and untouched.

### What this is NOT
- This is not a lead/contact enrichment pipeline or a business workflow registry.
- There are no hardcoded task types (`contact-enrichment`, `outreach-prep`, etc.) — those were removed in v1.4.1.
- The mechanism is domain-agnostic: any research topic can be continued as a linked task.
