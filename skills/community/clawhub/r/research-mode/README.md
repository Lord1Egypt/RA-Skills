# Research Mode

[English](#english) | [Русский](#русский)

[![CI](https://img.shields.io/github/actions/workflow/status/VKambulov/research-mode/ci.yml?branch=main&label=CI)](https://github.com/VKambulov/research-mode/actions/workflows/ci.yml)
[![Latest release](https://img.shields.io/github/v/release/VKambulov/research-mode?label=release)](https://github.com/VKambulov/research-mode/releases)
[![License: Apache-2.0](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
![OpenClaw skill](https://img.shields.io/badge/OpenClaw-skill-2f6fed)
![Review gated](https://img.shields.io/badge/review-gated-0f766e)

`research-mode` is an OpenClaw cron-based skill for durable background research:
bounded isolated iterations, persistent task state, review-gated finalization, and
inspectable artifacts.

It is not a standalone Python package yet. The helper scripts can be run directly,
but the product model assumes OpenClaw cron architecture for scheduled worker turns,
owner-channel updates, pause/resume/stop control, and review handoff.

This project was originally created for a personal OpenClaw workflow and is
published for people who want to study, adapt, or run a similar setup. It is
provided as-is, without any warranty or promise that it will fit every OpenClaw
installation without local adjustment.

> **Development status:** Research Mode is still under active development.
> The current top priority is making research runs stable, observable, and
> recoverable. Long-running research tasks may hit lifecycle, scheduling,
> delivery, or environment issues. If a task appears stuck or produces an
> unexpected state, ask your OpenClaw agent to diagnose the task, inspect
> `summary` / `health`, and run the appropriate recovery flow before restarting
> the research from scratch.

## At A Glance

Research Mode is for questions that are too large for one chat response and too
important to leave as an unreviewed draft. It gives an OpenClaw agent a durable,
local-first research loop: scheduled worker turns collect evidence, write
artifacts, verify adequacy, and stop at a human review gate before anything is
treated as final.

New tasks start with a preflight gate by default. The preflight worker records
`preflight.decision` as `go`, `go_with_warnings`, `needs_setup`, or `blocked`,
and writes `workspace/preflight/research-preflight.md`. Operators may use
`--skip-preflight` as an escape hatch; that path is recorded visibly as
`preflight.decision="skipped"`. Research Mode-specific standing rules can live
in a user-owned `RULES.md` in this skill directory; this repository ships
`RULES.example.md` as a template and does not create or overwrite the real file.

It is built for operators and agent builders who care about auditability:
sources, findings, iterations, state transitions, and final deliverables remain
inspectable on disk. The repository includes public examples with sanitized
research traces so reviewers can see how real tasks move from request to
review-ready package.

```mermaid
flowchart LR
    Request[Chat research request] --> Schedule[OpenClaw cron schedule]
    Schedule --> Iterations[Bounded worker iterations]
    Iterations --> Evidence[Sources, findings, notes]
    Evidence --> Adequacy[Research adequacy gate]
    Adequacy --> Package[Review-ready package]
    Package --> Review[Human review]
    Review --> Delivery[Approved delivery]
```

### Why It Stands Out

- Durable task state instead of one long fragile session.
- Bounded cron iterations instead of unbounded background work.
- Local artifact trail for sources, findings, runs, and final reports.
- Review-gated finalization so raw workspace output is not mistaken for the
  user-facing result.
- Public examples that include sanitized `research-trace/` directories.

### Showcase

- `examples/web-capture-evaluation/` demonstrates safe web-to-Markdown capture
  as a reviewable research package.
- `examples/rag-eval-tooling-matrix/` demonstrates a source-backed RAG
  evaluation tooling matrix with Markdown reports, validation notes, and an XLSX
  workbook.

See `examples/README.md` for a guided tour of the outputs and traces.

Note: ClawHub skill installs are text-only. The GitHub repository and GitHub
releases include binary presentation/example files such as
`assets/social-preview.png` and
`examples/rag-eval-tooling-matrix/rag-eval-tooling-matrix.xlsx`; those binary
files are not included when installing through `clawhub install`.

For project status and contribution paths, see `ROADMAP.md`,
`CONTRIBUTING.md`, `SECURITY.md`, and the issue templates under
`.github/ISSUE_TEMPLATE/`.

## English

### What this is

Use Research Mode when a question is too large for a single answer and should be
handled as a durable task:

- background research over hours or days;
- accumulating sources, findings, iteration notes, and final reports on disk;
- bounded cron iterations instead of one long live session;
- explicit review before user-facing delivery;
- linked follow-up research after an approved result.

Do not use it for one-shot lookups, quick summaries, ordinary coding tasks, or
anything that does not need durable state and scheduled continuation.

### Installation

Quick install from ClawHub:

```bash
clawhub install research-mode
openclaw skills check
```

Install it as an OpenClaw skill by cloning this repository directly into your
OpenClaw skills directory. The workspace folder name is installation-specific;
set `OPENCLAW_SKILLS_DIR` to the directory where your OpenClaw installation
loads skills from.

```bash
export OPENCLAW_SKILLS_DIR="/path/to/your/openclaw/skills"
git clone https://github.com/VKambulov/research-mode.git "$OPENCLAW_SKILLS_DIR/research-mode"
openclaw skills check
```

Some OpenClaw installations reject symlinks that resolve outside the configured
skills root. If that applies to your setup, keep the repository physically
inside the skills directory, as shown above.

For local development when the skill already exists inside a larger OpenClaw
workspace, turn that directory into the standalone repository source of truth:

```bash
cd /path/to/your/openclaw/skills/research-mode
git init
git add .
git status
```

### User Guide

#### What Research Mode Does

Research Mode turns a broad research request into a durable OpenClaw task. The
task can continue through scheduled bounded iterations, keep sources and
findings on disk, produce inspectable artifacts, and stop for review before the
result is delivered.

It is useful when the work needs continuity:

- a landscape review that should gather and compare sources over time;
- an evidence audit where claims, source quality, and open questions matter;
- a local corpus review over notes, PDFs, screenshots, or datasets;
- a decision memo that should survive restarts and be revised before delivery;
- a follow-up investigation based on an already approved result.

It is not the right tool for a quick lookup, a one-turn summary, a small coding
change, or a question that does not need scheduled continuation and saved state.

#### How A Task Is Started

For normal use, a person asks an OpenClaw agent to start Research Mode from
chat. The agent maps that request to the helper commands, attaches any supplied
materials, schedules worker turns, and reports meaningful milestones.

Good request shape:

```text
Start a Research Mode task.
Goal: compare local AI search approaches for a small private knowledge base.
Deliverable: short recommendation memo with trade-offs.
Depth: L.
Corpus: hybrid; use the attached notes and current public docs.
Constraints: prefer primary sources, identify weak evidence, avoid vendor-only claims.
Updates: send milestones, blockers, and the final review candidate only.
```

The request does not need to mention Python scripts. The scripts are an
operator and maintainer interface behind the chat workflow.

#### Launch Parameters

Research Mode works best when the initial request provides the following
fields.

- **Goal**: the research question, comparison, decision, or investigation target.
- **Title**: optional short label for the task.
- **Deliverable**: expected output shape, such as a brief, memo, table, source
  list, report, implementation plan, or evidence matrix.
- **Depth**: `S`, `M`, `L`, or `XL`. Larger depth allows more iterations,
  broader source collection, and a slower path to completion.
- **Phase**: `search`, `analyze`, or `synthesize`. This is useful when the task
  should start from discovery, evaluation, or final composition.
- **Corpus mode**: `web`, `local`, or `hybrid`. Use `local` for provided files,
  `web` for external discovery, and `hybrid` when both are needed.
- **Constraints**: hard requirements such as excluded source types, required
  source quality, privacy limits, language, geography, or deadline assumptions.
- **Instructions**: softer preferences for method, comparison criteria, report
  structure, update cadence, or review expectations.
- **Open questions**: known unknowns that should remain visible across
  iterations.
- **Input materials**: URLs, PDFs, screenshots, notes, datasets, or workspace
  files that should be attached before the first worker turn.
- **Limits**: maximum iterations, runtime, source count, or update frequency when
  the task should remain tightly bounded.

#### Depth Selection

Depth is a planning hint, not a guarantee of quality.

- `S`: a small durable task; useful for a narrow source set or a short memo.
- `M`: normal background research with a few focused iterations.
- `L`: broader comparison, multiple source families, or careful synthesis.
- `XL`: large investigation where the result may need several review and
  rework cycles.

For uncertain tasks, `M` or `L` is usually a better starting point than `XL`.
The operator can add constraints, extend the task, or create linked follow-up
research later.

#### During The Task

The agent or operator can inspect and steer the task without editing state files:

- show a compact status or summary;
- pause, resume, stop, or unschedule the task;
- add a research angle, instruction, constraint, or deliverable;
- attach more files, notes, URLs, or PDFs;
- ask for changes after review;
- approve the review candidate;
- mark the result as delivered;
- create linked follow-up research from an approved result.

Useful user-level requests:

```text
Show the current Research Mode summary.
Pause this research task.
Add a constraint: do not use forum comments as evidence.
Attach this PDF to the current research task.
Request changes: the final memo needs a clearer risk section.
Approve the result.
Create a linked follow-up research task for the next open question.
```

#### Review And Delivery

Research Mode deliberately separates review from delivery.

- `awaiting_review` means a candidate result is ready for human review.
- `approve` means the candidate is accepted.
- `request-changes` sends the task back for revision with feedback.
- `mark-delivered` records that a deliverable is ready or has been delivered
  through the chosen channel.

This separation prevents an unchecked draft, raw workspace artifact, or partial
recovery note from being treated as the final user-facing result.

#### Owner Binding And Delivery Intents

When a chat or operator launch should receive milestone and review updates, bind
the task owner at creation time with `--channel` and `--chat-id`. Use
`--thread-id` or `--topic-id` when the messaging surface needs a thread or topic
target. Use `--no-owner` only when notification delivery is intentionally
disabled; this records an explicit disabled reason instead of looking like a
forgotten owner target.

Research Mode itself emits a serializable `delivery_intent`. Platform-specific
wrappers should send the pending intent through their messaging surface, include
`primary_file` and `attachments` when supported, and then call
`record-notification --status sent` or `--status failed`. When a provider rejects
the target shape, wrappers can pass
`--error-code delivery_channel_addressing_failed`; Research Mode records only a
sanitized target shape, such as whether chat/thread/topic ids were present, not
the private ids themselves.

#### Research Adequacy Gate

Before finalization, Research Mode runs a research adequacy gate. This checks
whether the accumulated sources, findings, constraints, open questions, and
requested deliverable actually satisfy the user's goal.

The gate uses `phase=verify` and the structured `result.adequacy` field. If the
research is incomplete, lifecycle code routes the task back to `search`,
`analyze`, or `synthesize` with an explicit `operator_next_action`. If adequacy
passes, the task can move to `finalize`, where the system creates and validates
the human-reviewable candidate.

#### What The Task Produces

A Research Mode task can produce several kinds of artifacts:

- `state.json`: task status, working memory, review state, delivery state, and
  transition history;
- `sources.jsonl`: source records and source metadata;
- `findings.jsonl`: accumulated findings and evidence notes;
- `adequacy`: state and result fields that record whether the research is
  sufficient before finalization;
- `iterations/`: per-run notes and intermediate work;
- `workspace/`: task-local scripts, datasets, screenshots, exports, and
  analysis outputs;
- `task-playbook.md`: operator-facing view of current state and next action;
- `runs.tsv`: execution trail;
- `recovery-log.jsonl`: explicit repair/recovery events;
- `final-report.md`: synthesized candidate or approved report when available.

Human review should focus on the final candidate and operator surfaces, not on
raw internal workspace files.

#### Common Work Patterns

Source-backed brief:

```text
Goal: explain whether a new database feature is mature enough for production.
Deliverable: two-page brief with recommendation, risks, and source links.
Depth: M.
Corpus: web.
Constraints: prefer official docs, changelogs, and issue discussions.
```

Local corpus review:

```text
Goal: summarize the attached project notes and extract unresolved decisions.
Deliverable: decision log with open questions.
Depth: S.
Corpus: local.
Constraints: do not infer facts that are not present in the files.
```

Hybrid investigation:

```text
Goal: compare the attached internal requirements with current public options.
Deliverable: comparison table plus recommendation memo.
Depth: L.
Corpus: hybrid.
Constraints: separate verified facts from assumptions.
```

Follow-up after approval:

```text
Create linked follow-up research from the approved result.
Goal: investigate the highest-risk option in more detail.
Deliverable: implementation plan with blockers.
```

### Operations

#### Roles

Research Mode has three practical roles.

- **User**: asks for research and reviews the result through chat.
- **Operator**: inspects task state, steers work, handles review, and repairs
  normal operational issues through helper commands.
- **Maintainer**: changes code, documentation, tests, and release packaging.

One person or agent can hold several roles, but the documentation keeps them
separate because the safe actions differ.

#### Launch Mode 1: Chat-First Start

This is the normal product path. The user describes the task in chat and the
OpenClaw agent creates or starts the task. The agent may use the CLI internally,
but the user does not need to run commands from the repository.

The agent should collect or infer:

- goal;
- deliverable;
- depth;
- corpus mode;
- constraints and instructions;
- attached input material;
- update cadence;
- review expectations.

#### Launch Mode 2: Create And Schedule In One Step

`start` creates the task and schedules worker turns unless `--no-schedule` is
used.

```bash
python3 scripts/research_mode.py start \
  --goal "Compare local AI search approaches" \
  --deliverable "short recommendation memo" \
  --depth L \
  --corpus-mode hybrid \
  --constraint "prefer primary sources" \
  --instruction "separate facts from assumptions" \
  --every 5m
```

Useful `start` options include:

- `--id`, `--title`, `--goal`;
- `--depth`, `--phase`, `--corpus-mode`;
- `--initial-angle`, `--open-question`, `--constraint`, `--instruction`;
- `--deliverable`;
- `--max-iterations`, `--max-runtime-min`, `--max-sources`;
- `--tick-every-min`, `--stale-timeout-min`, `--milestone-every`,
  `--failure-threshold`;
- `--every`, `--timeout-seconds`, `--thinking`, `--agent`, `--model`, `--name`;
- `--light-context`, `--dry-run`, `--no-schedule`.

#### Launch Mode 3: Create, Attach, Then Schedule

Use this path when the task needs local material before the first worker turn.

```bash
python3 scripts/research_mode.py create \
  --goal "Review the supplied notes and produce an evidence map" \
  --deliverable "evidence matrix" \
  --corpus-mode local

python3 scripts/research_mode.py attach-input --file ./notes.md
python3 scripts/research_mode.py attach-pdf --file ./paper.pdf
python3 scripts/research_mode.py attach-note --title "Operator note" --text "Focus on unresolved claims."

python3 scripts/research_mode.py schedule --every 5m
```

When exactly one active non-final task exists, user-facing commands may omit
`--id`. If several tasks are active, specify `--id` or `--path`.

#### Launch Mode 4: Manual Worker Iteration

Manual iteration is for diagnostics, smoke tests, or recovery. It is not the
normal user entrypoint.

```bash
python3 scripts/research_mode.py begin --id <research-id>
```

The worker performs one bounded step, writes a result JSON file, then commits it:

```bash
python3 scripts/research_mode.py finish \
  --id <research-id> \
  --run-id <run-id> \
  --result-file ./result.json
```

If the leased iteration fails:

```bash
python3 scripts/research_mode.py fail \
  --id <research-id> \
  --run-id <run-id> \
  --error "what failed"
```

If a worker wrote `.tmp/result-<run-id>.json` but crashed before `finish`,
recover the pending result instead of starting another worker over it:

```bash
python3 scripts/research_mode.py recover \
  --id <research-id> \
  --apply-pending-result
```

If only derived operator files are missing, regenerate them without changing
`state.json`:

```bash
python3 scripts/research_mode.py recover \
  --id <research-id> \
  --refresh-derived
```

Do not keep working indefinitely inside one lease. The system is designed around
bounded iterations.

For multiple reviewable deliverables, use
`working_memory.output_contract.outputs[]` and produce matching
`finalization.candidate_artifacts` / `delivery.outputs` entries. MIME values are
open strings supplied by the contract or worker; Research Mode does not keep a
file-extension or MIME registry and does not infer role or provenance from file
names, text, or list order. Use `source_for` and `derived_from` id references
when an artifact is the declared source for another artifact or was generated
from another artifact.

Finalization records `output_decision` for structured outputs.
`deliverable_decision`, `working_memory.output_contract.kind`, and
`finalization.primary_deliverable_kind` remain legacy single-output
compatibility fields.

#### Launch Mode 5: Scheduling Existing Tasks

Use `schedule` when a task already exists and should receive recurring isolated
worker turns.

```bash
python3 scripts/research_mode.py schedule --id <research-id> --every 5m
```

Use `bind-job` only when an existing cron job must be attached to task state:

```bash
python3 scripts/research_mode.py bind-job \
  --id <research-id> \
  --job-id <cron-job-id> \
  --mode isolated \
  --every 5m
```

Use `unschedule` to remove the currently bound cron job from the task:

```bash
python3 scripts/research_mode.py unschedule --id <research-id>
```

#### Targeting Tasks

Most operator commands accept:

- `--root`: research root directory;
- `--id`: task id under the root;
- `--path`: explicit task path constrained to the selected root.

Task ids must be safe single path segments. Paths outside the selected root,
path traversal, and delivery paths that escape the task directory are rejected.

#### Lifecycle States

Important states:

- `idle`: task can be picked up by a worker;
- `running`: a worker lease is active;
- `finalize`: completion was attempted, but finalization requires rework;
- `awaiting_review`: a candidate is ready for review and normal worker turns
  should stop;
- `paused`: task is intentionally paused;
- `complete`: task has been approved or marked complete;
- `cancelled`: task was stopped;
- `failed`: task failed after an error path or threshold.

Terminal or review-gated states should not be forced forward with `begin`.

Semantic phases are separate from lifecycle states: `search`, `analyze`,
`synthesize`, `verify`, and `finalize`. `verify` is the research adequacy phase;
it decides whether to return to research work or continue to finalization.

#### Operator Surfaces

Use these instead of reading raw JSON first:

```bash
python3 scripts/research_mode.py list --format text
python3 scripts/research_mode.py status --id <research-id> --format text
python3 scripts/research_mode.py summary --id <research-id> --format text
python3 scripts/research_mode.py preflight --id <research-id> --format text
python3 scripts/research_mode.py health --id <research-id> --format text
python3 scripts/research_mode.py reconcile --id <research-id> --format text
python3 scripts/research_mode.py queue-status --root <research-root>
python3 scripts/research_mode.py draft-report --id <research-id> --format markdown
python3 scripts/research_mode.py render-prompt --id <research-id>
```

`queue-status` also returns read-only findings when queue state disagrees with
task state, such as a missing holder task, a holder/task lock mismatch, a stale
waiter, or a terminal task still listed as waiting. Task-specific queue findings
are included in `health`.

For automated monitors, `summary --format json` includes
`operator_attention.status`, `conditions`, and `recommended_actions`. Treat any
status other than `ok` as a reason to alert or follow the recommended lifecycle
command instead of silently reporting that a task is still running.

Task-local files also matter:

- `task-playbook.md`: current operator guidance and next action;
- `runs.tsv`: execution trail;
- `recovery-log.jsonl`: explicit repair/recovery events;
- `state.json`: source of truth when deeper diagnosis is needed.

#### Steering Commands

Use helper commands instead of editing `state.json`.

```bash
python3 scripts/research_mode.py add-angle "compare with the alternative approach"
python3 scripts/research_mode.py add-constraint "exclude low-quality reposts"
python3 scripts/research_mode.py add-instruction "show uncertainty explicitly"
python3 scripts/research_mode.py set-deliverable "short comparative memo"
```

For detailed updates:

```bash
python3 scripts/research_mode.py mutate-working-memory \
  --id <research-id> \
  --append-angle "check deployment cost" \
  --add-open-question "which option has the weakest evidence?" \
  --add-constraint "avoid unsourced claims" \
  --set-deliverable "risk-focused recommendation memo"
```

#### Corpus Commands

Corpus helpers attach material to the task and record provenance.

```bash
python3 scripts/research_mode.py attach-input --id <research-id> --file ./notes.md
python3 scripts/research_mode.py attach-input --id <research-id> --dir ./corpus
python3 scripts/research_mode.py attach-input --id <research-id> --glob './docs/**/*.md'
python3 scripts/research_mode.py attach-note --id <research-id> --title "Local context" --text "..."
python3 scripts/research_mode.py attach-url-as-md --id <research-id> --url "https://example.com/article"
python3 scripts/research_mode.py attach-pdf --id <research-id> --file ./paper.pdf
```

Images attached through `attach-input` are marked with `content_hint=image` so
future worker turns can treat them as visual inputs.
`attach-url-as-md` accepts only `http://` and `https://` URLs and blocks local
or private network hosts, including redirect targets.

#### Runtime Preparation

Use `prepare-runtime` when a task needs local code, structured analysis, or
exports.

```bash
python3 scripts/research_mode.py prepare-runtime --id <research-id>
python3 scripts/research_mode.py prepare-runtime --id <research-id> --package pandas --package openpyxl
```

The expected task-local layout is:

```text
workspace/
  analysis/
  tools/
  data/
  outputs/
  outputs/screenshots/
  outputs/vision/
  tmp/
  data/analysis.sqlite
  analysis/schema.sql
  analysis/queries/
```

Task-local Python packages are currently allowed through `--package`. Operators
should check unusual or risky packages before installation and record the reason
when a package materially affects the result.

Retrieved pages, PDFs, prompts, or task artifacts must not decide package
installation on their own; package installation is a controlled
operator/runtime capability. `prepare-runtime` may create a task-local virtual
environment and run Python tooling through subprocesses. Interpreter paths and
venv paths are useful local diagnostics, but public/package-facing summaries
should prefer task-relative or redacted paths when an absolute path is not
needed.

A stricter package allowlist or lock policy is a future layer, not part of the
current baseline.

#### Review And Delivery Commands

Review commands:

```bash
python3 scripts/research_mode.py approve --id <research-id>
python3 scripts/research_mode.py approve --id <research-id> --approved-artifact final-report.md
python3 scripts/research_mode.py request-changes --id <research-id> "what must change"
python3 scripts/research_mode.py reopen --id <research-id> --feedback "why it is reopened"
```

Delivery commands:

```bash
python3 scripts/research_mode.py format-delivery --id <research-id> --channel file

python3 scripts/research_mode.py mark-delivered \
  --id <research-id> \
  --primary-file final-report.md \
  --summary-text "Final report is ready." \
  --channel-strategy attach \
  --ready
```

`awaiting_review` is not delivery-ready by itself. `delivery.ready=true` is set
only after approval or explicit delivery marking.

#### Linked Research

Use linked research when an approved result opens a new bounded investigation.

```bash
python3 scripts/research_mode.py create-linked-research \
  --id <research-id> \
  --goal "Investigate the highest-risk option in detail" \
  --relation follow-up \
  --carry-summary \
  --carry-open-questions \
  --carry-constraints
```

Useful carry options:

- `--carry-summary`;
- `--carry-open-questions`;
- `--carry-constraints`;
- `--carry-deliverable`;
- `--carry-approved-artifact`.

#### Quality Gates

Documentation-only check:

```bash
python3 scripts/check_research_mode_docs.py
```

Release and behavior gate:

```bash
scripts/check_research_mode.sh
```

If the skill was installed from ClawHub and the shell script is not executable
in your environment, run the same gate explicitly through `bash`:

```bash
bash scripts/check_research_mode.sh
```

The full gate runs compile checks, linting, documentation smoke, release smoke,
type checks, the selftest runner, and pytest-compatible tests.

GitHub Actions runs the same release gate and a Bandit security smoke scan on
pushes to `main` and on pull requests. CodeQL is not enabled in the baseline
workflow today; the lightweight security baseline is the release gate plus the
Bandit smoke scan.

### Architecture

Research Mode is designed around OpenClaw cron architecture:

1. A task directory under a research root stores `state.json` and artifacts.
2. OpenClaw cron starts isolated worker turns.
3. Each worker turn calls `begin`, does one bounded iteration, writes a result
   JSON file, and calls `finish`.
4. Worker execution is serialized per research root by the global iteration
   queue. Multiple tasks may be scheduled together; a skipped tick with
   `deferred:global-research-lock` is normal waiting, not failure.
5. `awaiting_review` stops further worker acquisition until the operator uses
   `approve`, `request-changes`, `reopen`, or `stop`.

The helper scripts are deterministic control-plane tools. The autonomous research
behavior comes from OpenClaw workers using those tools on a schedule.

Full architecture reference with diagrams:
- `ARCHITECTURE.md`

### Documentation Map

Start with the guide that matches the work:

- `README.md` — project overview, installation, chat-first usage, launch parameters, operations, review, delivery, scheduling, runtime preparation, and quality gates.
- `TROUBLESHOOTING.md` — diagnosis order, common failure modes, and safe repair paths.
- `ARCHITECTURE.md` — system model, data model, lifecycle, finalization, and design principles.
- `docs/CLI.md` — stable operator CLI surface and more volatile/internal helpers.
- `docs/STATE_VERSIONING.md` — `version` compatibility policy and migration expectations.
- `schemas/` — JSON contract slices for task state, worker results, adequacy, finalization, and delivery intents.
- `ROADMAP.md` — public project direction and current support boundary.
- `CONTRIBUTING.md` — development setup, pull request expectations, and privacy rules for public contributions.
- `examples/` — reviewed example output packages generated by Research Mode tasks.
- `RELEASING.md` — release procedure, package boundary, and public repository contents for maintainers.
- `SECURITY.md` — security model and reporting guidance.
- `AGENTS.md` — repository maintenance notes for coding agents.

### Maintainer Smoke Check

From the repository root:

```bash
python3 scripts/release_smoke.py
```

### Operator surfaces

Use these instead of manually stitching state files:

- `summary`
- `status`
- `health`
- `reconcile`
- `preflight`
- `queue-status`
- `draft-report`
- `task-playbook.md`
- `runs.tsv`

Finalization surfaces expose `operator_next_action` so the operator can distinguish
review-ready candidates from worker rework and human-intervention states.

### Safety invariants

- `research_id` must be a safe single path segment.
- `--path` must stay under the selected research root.
- Approval and delivery artifacts must stay inside the task directory.
- Research completion must pass `result.adequacy` before finalization.
- `awaiting_review` means review-ready, not delivery-ready.
- Worker-initiated completion requires `result.finalization.status="passed"`.
- Raw workspace artifacts must not be exposed as final user deliverables.
- Successful `finish` records `transactions.finish.status=committed`.

### Release gate

Run from the repository or package root before tagging a release or after
meaningful helper changes:

```bash
scripts/check_research_mode.sh
```

The gate runs `compileall`, `ruff`, docs smoke, release smoke, `pyright`,
selftests, and pytest-compatible tests.

Maintainer release procedure:
- `RELEASING.md`

Architecture and release notes:
- `ARCHITECTURE.md`
- `RELEASE_NOTES.md`

Repository maintenance:
- `SECURITY.md`
- `AGENTS.md` for coding-agent maintenance notes

License: Apache License, Version 2.0. See `LICENSE`.

## Русский

### Что это

Проект изначально создавался для личного сценария работы в OpenClaw и
публикуется для тех, кто хочет изучить, адаптировать или запустить похожую
схему. Он поставляется как есть, без гарантий и без обещания, что подойдёт к
любой установке OpenClaw без локальной настройки.

`research-mode` — это OpenClaw skill для длительного фонового исследования:
ограниченные запуски через cron, состояние задачи на диске, проверка результата
перед выдачей пользователю и артефакты, которые можно посмотреть.

> **Статус разработки:** Research Mode всё ещё активно развивается.
> Сейчас главный приоритет проекта — стабильное, наблюдаемое и восстанавливаемое
> проведение исследований. В долгих исследованиях могут возникать проблемы с
> жизненным циклом, расписанием, доставкой результата или окружением. Если
> задача зависла или перешла в неожиданное состояние, попросите OpenClaw-агента
> провести диагностику задачи, проверить `summary` / `health` и выполнить
> подходящее восстановление, прежде чем начинать исследование заново.

Важно: установка через ClawHub содержит только текстовые файлы. Бинарные
файлы витрины и примеров, например `assets/social-preview.png` и
`examples/rag-eval-tooling-matrix/rag-eval-tooling-matrix.xlsx`, доступны в
GitHub-репозитории и GitHub releases, но не попадают в `clawhub install`.

Статус проекта и правила участия описаны в `ROADMAP.md`, `CONTRIBUTING.md`,
`SECURITY.md` и issue templates в `.github/ISSUE_TEMPLATE/`.

Research Mode подходит для задач, которые должны жить дольше одного ответа:

- исследование в фоне несколько часов или дней;
- постепенное накопление источников и выводов;
- управление `pause` / `resume` / `stop`;
- итоговый отчёт или набор материалов, которые проходят проверку перед выдачей;
- последующее исследование на базе утверждённого результата.

Новые задачи по умолчанию начинаются с preflight gate. Worker записывает
`preflight.decision` как `go`, `go_with_warnings`, `needs_setup` или `blocked`
и пишет `workspace/preflight/research-preflight.md`. Оператор может использовать
`--skip-preflight` как escape hatch; такой путь явно фиксируется как
`preflight.decision="skipped"`. Постоянные правила именно для Research Mode
можно хранить в пользовательском `RULES.md` в директории этого скилла;
репозиторий поставляет только шаблон `RULES.example.md` и не создаёт и не
перезаписывает реальный файл.

Research Mode не подходит для быстрых одноразовых вопросов, обычных задач по
коду и задач, которым не нужны сохранённое состояние, cron-итерации и проверка
результата.

### Установка

Быстрая установка из ClawHub:

```bash
clawhub install research-mode
openclaw skills check
```

Установка выполняется как OpenClaw skill: репозиторий клонируется прямо в
директорию skills. Название рабочей папки зависит от конкретной установки;
`OPENCLAW_SKILLS_DIR` должен указывать на директорию, из которой OpenClaw
загружает skills.

```bash
export OPENCLAW_SKILLS_DIR="/path/to/your/openclaw/skills"
git clone https://github.com/VKambulov/research-mode.git "$OPENCLAW_SKILLS_DIR/research-mode"
openclaw skills check
```

Некоторые установки OpenClaw не принимают символические ссылки, если они
указывают наружу из разрешённой директории skills. В таком случае репозиторий
должен физически находиться внутри директории skills, как в примере выше.

Для локальной разработки, когда skill уже лежит внутри большой рабочей области
OpenClaw, эту директорию можно превратить в самостоятельный git-репозиторий:

```bash
cd /path/to/your/openclaw/skills/research-mode
git init
git add .
git status
```

### Руководство пользователя

#### Что делает Research Mode

Research Mode превращает широкий исследовательский запрос в долговечную задачу
OpenClaw. Задача может продолжаться через ограниченные итерации по расписанию,
сохранять источники и выводы на диске, формировать проверяемые артефакты и
останавливаться на ревью перед выдачей результата.

Он полезен, когда работе нужна непрерывность:

- обзор рынка или технологий с накоплением источников;
- проверка доказательств, качества источников и открытых вопросов;
- разбор локального корпуса заметок, PDF, скриншотов или данных;
- записка для решения, которую нужно пережить рестарты и доработать перед
  выдачей;
- последующее исследование на базе уже утверждённого результата.

Он не нужен для быстрого поиска, одноразовой сводки, небольшой задачи по коду
или вопроса, которому не нужны расписание и сохранённое состояние.

#### Как запускается задача

В обычном сценарии человек просит агента OpenClaw запустить Research Mode из
чата. Агент преобразует запрос во вспомогательные команды, прикрепляет
переданные материалы, ставит рабочие итерации в расписание и сообщает только о
значимых вехах.

Хорошая форма запроса:

```text
Запустить Research Mode.
Цель: сравнить подходы к локальному AI-поиску для небольшой частной базы знаний.
Форма результата: краткая рекомендация с плюсами, минусами и компромиссами.
Глубина: L.
Корпус: hybrid; использовать приложенные заметки и актуальную публичную документацию.
Ограничения: предпочитать первичные источники, отмечать слабые доказательства,
не опираться только на заявления продавцов.
Обновления: только вехи, блокеры и финальный кандидат на ревью.
```

В пользовательском запросе не требуется упоминать Python-скрипты. Скрипты
остаются интерфейсом оператора и сопровождающего за обычным чатовым сценарием.

#### Параметры запуска

Research Mode работает лучше, когда стартовый запрос содержит следующие поля.

- **Цель**: исследовательский вопрос, сравнение, решение или объект проверки.
- **Название**: короткая метка задачи, если она нужна.
- **Форма результата**: краткая записка, отчёт, таблица, список источников,
  план внедрения, матрица доказательств или другой формат.
- **Глубина**: `S`, `M`, `L` или `XL`. Большая глубина разрешает больше
  итераций, шире сбор источников и более медленное завершение.
- **Фаза**: `search`, `analyze` или `synthesize`, если задачу нужно начать с
  поиска, анализа или сборки результата.
- **Режим корпуса**: `web`, `local` или `hybrid`. `local` подходит для
  переданных файлов, `web` — для внешнего поиска, `hybrid` — для обоих типов.
- **Ограничения**: жёсткие требования: исключённые типы источников, качество
  источников, приватность, язык, география или сроки.
- **Инструкции**: предпочтения по методу, критериям сравнения, структуре
  отчёта, частоте обновлений или ревью.
- **Открытые вопросы**: известные неизвестные, которые должны оставаться
  видимыми между итерациями.
- **Входные материалы**: URL, PDF, скриншоты, заметки, датасеты или файлы из
  рабочей области, которые нужно прикрепить до первой итерации.
- **Лимиты**: максимальное число итераций, время выполнения, число источников
  или частота обновлений, если задача должна быть жёстко ограничена.

#### Выбор глубины

Глубина — это планировочная подсказка, а не гарантия качества.

- `S`: небольшая долговечная задача, короткая записка или узкий набор источников.
- `M`: обычное фоновое исследование на несколько сфокусированных итераций.
- `L`: более широкое сравнение, несколько семейств источников или аккуратный
  синтез.
- `XL`: крупное исследование с возможными циклами ревью и доработки.

Для неопределённых задач обычно лучше начинать с `M` или `L`, а не с `XL`.
Оператор может добавить ограничения, продлить задачу или создать связанное
последующее исследование позже.

#### Работа во время задачи

Агент или оператор может управлять задачей без ручного редактирования файлов
состояния:

- показать статус или сводку;
- поставить задачу на паузу, продолжить, остановить или снять с расписания;
- добавить угол исследования, инструкцию, ограничение или форму результата;
- прикрепить дополнительные файлы, заметки, URL или PDF;
- запросить доработки после ревью;
- утвердить кандидат на результат;
- отметить результат как доставленный;
- создать связанное последующее исследование от утверждённого результата.

Полезные пользовательские запросы:

```text
Показать текущую сводку Research Mode.
Поставить эту исследовательскую задачу на паузу.
Добавить ограничение: не использовать комментарии форумов как доказательства.
Прикрепить этот PDF к текущей исследовательской задаче.
Запросить доработки: в итоговой записке нужен более ясный раздел рисков.
Утвердить результат.
Создать связанное исследование по следующему открытому вопросу.
```

#### Ревью и доставка

Research Mode намеренно разделяет ревью и доставку.

- `awaiting_review` означает, что кандидат готов к проверке человеком.
- `approve` означает, что кандидат принят.
- `request-changes` возвращает задачу на доработку с обратной связью.
- `mark-delivered` фиксирует, что результат готов к выдаче или уже выдан через
  выбранный канал.

Это разделение не даёт непроверенному черновику, сырому артефакту рабочей
области или заметке восстановления стать финальным пользовательским результатом.

Для внешней отправки Research Mode создаёт сериализуемый `delivery_intent`.
Адаптер канала отправляет текст и поддерживаемые файлы, затем вызывает
`record-notification --status sent` или `--status failed`. Если провайдер
отклоняет форму цели, адаптер может передать
`--error-code delivery_channel_addressing_failed`; в состоянии сохраняется
только безопасная форма цели, например наличие chat/thread/topic id, но не сами
приватные id.

#### Проверка достаточности исследования

Перед финальной проверкой Research Mode выполняет gate достаточности
исследования. Он проверяет, действительно ли накопленные источники, выводы,
ограничения, открытые вопросы и требуемая форма результата закрывают цель
пользователя.

Для этого используется `phase=verify` и структурированное поле
`result.adequacy`. Если исследование неполное, lifecycle-код возвращает задачу в
`search`, `analyze` или `synthesize` и показывает явный `operator_next_action`.
Если достаточность пройдена, задача переходит в `finalize`, где формируется и
проверяется кандидат для ревью человеком.

#### Что создаёт задача

Research Mode может создавать несколько типов артефактов:

- `state.json`: статус задачи, рабочая память, ревью, доставка и история
  переходов;
- `sources.jsonl`: источники и их метаданные;
- `findings.jsonl`: накопленные выводы и заметки по доказательствам;
- `adequacy`: поля состояния и результата, фиксирующие достаточность
  исследования перед финальной проверкой;
- `iterations/`: заметки отдельных итераций и промежуточная работа;
- `workspace/`: локальные скрипты, данные, скриншоты, экспорты и результаты
  анализа;
- `task-playbook.md`: операторское представление состояния и следующего шага;
- `runs.tsv`: след запусков;
- `recovery-log.jsonl`: явные события repair/recovery;
- `final-report.md`: синтезированный кандидат или утверждённый отчёт, если он
  уже создан.

Ревью должно опираться на финальный кандидат и операторские представления, а не
на сырые внутренние файлы рабочей области.

#### Частые рабочие сценарии

Записка на базе источников:

```text
Цель: понять, достаточно ли зрелая новая функция базы данных для production.
Форма результата: записка на две страницы с рекомендацией, рисками и ссылками.
Глубина: M.
Корпус: web.
Ограничения: предпочитать официальные docs, changelog и обсуждения issues.
```

Разбор локального корпуса:

```text
Цель: обобщить приложенные проектные заметки и извлечь нерешённые решения.
Форма результата: decision log с открытыми вопросами.
Глубина: S.
Корпус: local.
Ограничения: не выводить факты, которых нет в файлах.
```

Смешанное исследование:

```text
Цель: сравнить приложенные внутренние требования с актуальными публичными вариантами.
Форма результата: сравнительная таблица и рекомендация.
Глубина: L.
Корпус: hybrid.
Ограничения: отделять проверенные факты от предположений.
```

Продолжение после утверждения:

```text
Создать связанное исследование от утверждённого результата.
Цель: подробнее проверить самый рискованный вариант.
Форма результата: план внедрения с блокерами.
```

### Операции

#### Роли

У Research Mode есть три практические роли.

- **Пользователь**: просит провести исследование и проверяет результат через чат.
- **Оператор**: смотрит состояние задачи, управляет работой, проводит ревью и
  исправляет штатные эксплуатационные проблемы через вспомогательные команды.
- **Сопровождающий**: меняет код, документацию, тесты и релизную упаковку.

Один человек или агент может совмещать роли, но документация разделяет их,
потому что безопасные действия отличаются.

#### Вариант запуска 1: через чат

Это штатный продуктовый путь. Пользователь описывает задачу в чате, а агент
OpenClaw создаёт или запускает задачу. Агент может использовать CLI внутри
процесса, но пользователь не обязан запускать команды из репозитория.

Агент должен собрать или вывести из запроса:

- цель;
- форму результата;
- глубину;
- режим корпуса;
- ограничения и инструкции;
- входные материалы;
- частоту обновлений;
- ожидания от ревью.

#### Вариант запуска 2: создать и запланировать одной командой

`start` создаёт задачу и ставит рабочие итерации в расписание, если не указан
`--no-schedule`.

```bash
python3 scripts/research_mode.py start \
  --goal "Сравнить подходы к локальному AI-поиску" \
  --deliverable "краткая рекомендация" \
  --depth L \
  --corpus-mode hybrid \
  --constraint "предпочитать первичные источники" \
  --instruction "отделять факты от предположений" \
  --every 5m
```

Полезные параметры `start`:

- `--id`, `--title`, `--goal`;
- `--depth`, `--phase`, `--corpus-mode`;
- `--initial-angle`, `--open-question`, `--constraint`, `--instruction`;
- `--deliverable`;
- `--max-iterations`, `--max-runtime-min`, `--max-sources`;
- `--tick-every-min`, `--stale-timeout-min`, `--milestone-every`,
  `--failure-threshold`;
- `--every`, `--timeout-seconds`, `--thinking`, `--agent`, `--model`, `--name`;
- `--light-context`, `--dry-run`, `--no-schedule`.

#### Вариант запуска 3: создать, прикрепить материалы, затем запланировать

Этот путь подходит, когда задаче нужны локальные материалы до первой рабочей
итерации.

```bash
python3 scripts/research_mode.py create \
  --goal "Разобрать переданные заметки и сделать карту доказательств" \
  --deliverable "матрица доказательств" \
  --corpus-mode local

python3 scripts/research_mode.py attach-input --file ./notes.md
python3 scripts/research_mode.py attach-pdf --file ./paper.pdf
python3 scripts/research_mode.py attach-note --title "Operator note" --text "Focus on unresolved claims."

python3 scripts/research_mode.py schedule --every 5m
```

Если активная незавершённая задача ровно одна, пользовательские команды могут
не указывать `--id`. Если активных задач несколько, нужен явный `--id` или
`--path`.

#### Вариант запуска 4: ручная рабочая итерация

Ручная итерация нужна для диагностики, smoke-тестов или восстановления. Это не
обычная пользовательская точка входа.

```bash
python3 scripts/research_mode.py begin --id <research-id>
```

Исполнитель делает один ограниченный шаг, пишет JSON-результат и фиксирует его:

```bash
python3 scripts/research_mode.py finish \
  --id <research-id> \
  --run-id <run-id> \
  --result-file ./result.json
```

Если итерация с блокировкой завершилась ошибкой:

```bash
python3 scripts/research_mode.py fail \
  --id <research-id> \
  --run-id <run-id> \
  --error "что сломалось"
```

Одна блокировка не должна превращаться в бесконечную работу. Система
спроектирована вокруг ограниченных итераций.

#### Вариант запуска 5: расписание для существующей задачи

`schedule` используется, когда задача уже есть и ей нужны повторяющиеся
изолированные итерации.

```bash
python3 scripts/research_mode.py schedule --id <research-id> --every 5m
```

`bind-job` нужен только тогда, когда существующий cron job нужно привязать к
состоянию задачи:

```bash
python3 scripts/research_mode.py bind-job \
  --id <research-id> \
  --job-id <cron-job-id> \
  --mode isolated \
  --every 5m
```

`unschedule` удаляет текущий привязанный cron job из задачи:

```bash
python3 scripts/research_mode.py unschedule --id <research-id>
```

#### Выбор задачи для команды

Большинство операторских команд принимает:

- `--root`: корень исследований;
- `--id`: id задачи внутри корня;
- `--path`: явный путь к задаче, ограниченный выбранным корнем.

Id задачи должен быть безопасным одиночным сегментом пути. Выход за пределы
корня, path traversal и delivery-пути наружу из директории задачи отклоняются.

#### Состояния жизненного цикла

Важные состояния:

- `idle`: задачу может взять рабочая итерация;
- `running`: активна рабочая блокировка;
- `finalize`: завершение было запрошено, но финальная проверка требует доработки;
- `awaiting_review`: кандидат готов к ревью, обычные рабочие итерации должны
  остановиться;
- `paused`: задача намеренно поставлена на паузу;
- `complete`: задача утверждена или помечена завершённой;
- `cancelled`: задача остановлена;
- `failed`: задача завершилась ошибкой или порогом ошибок.

Terminal- и review-gated-состояния нельзя продвигать командой `begin` вслепую.

Смысловые фазы отделены от lifecycle-состояний: `search`, `analyze`,
`synthesize`, `verify` и `finalize`. `verify` — фаза проверки достаточности
исследования; она решает, вернуться ли к исследовательской работе или перейти к
финальной проверке.

#### Представления оператора

Сначала используются эти команды, а не ручное чтение JSON:

```bash
python3 scripts/research_mode.py list --format text
python3 scripts/research_mode.py status --id <research-id> --format text
python3 scripts/research_mode.py summary --id <research-id> --format text
python3 scripts/research_mode.py preflight --id <research-id> --format text
python3 scripts/research_mode.py health --id <research-id> --format text
python3 scripts/research_mode.py reconcile --id <research-id> --format text
python3 scripts/research_mode.py queue-status --root <research-root>
python3 scripts/research_mode.py draft-report --id <research-id> --format markdown
python3 scripts/research_mode.py render-prompt --id <research-id>
```

`queue-status` также возвращает read-only findings, если состояние очереди не
сходится с состоянием задач: missing holder task, holder/task lock mismatch,
stale waiter или terminal task, которая всё ещё числится waiting. Findings,
относящиеся к конкретной задаче, попадают и в `health`.

Для автоматических наблюдателей `summary --format json` содержит
`operator_attention.status`, `conditions` и `recommended_actions`. Любой статус
кроме `ok` нужно считать поводом уведомить оператора или выполнить
рекомендованную lifecycle-команду, а не молча считать задачу всё ещё рабочей.

Внутри задачи также важны:

- `task-playbook.md`: текущее операторское руководство и следующий шаг;
- `runs.tsv`: след запусков;
- `recovery-log.jsonl`: явные события repair/recovery;
- `state.json`: источник истины для глубокой диагностики.

#### Управление направлением исследования

Вместо ручного редактирования `state.json` используются helper-команды.

```bash
python3 scripts/research_mode.py add-angle "сравнить с альтернативным подходом"
python3 scripts/research_mode.py add-constraint "исключить низкокачественные пересказы"
python3 scripts/research_mode.py add-instruction "явно показывать неопределённость"
python3 scripts/research_mode.py set-deliverable "краткая сравнительная записка"
```

Для более подробного обновления:

```bash
python3 scripts/research_mode.py mutate-working-memory \
  --id <research-id> \
  --append-angle "проверить стоимость внедрения" \
  --add-open-question "у какого варианта самые слабые доказательства?" \
  --add-constraint "избегать неподтверждённых утверждений" \
  --set-deliverable "рекомендация с фокусом на риски"
```

#### Команды корпуса

Команды корпуса прикрепляют материалы к задаче и фиксируют происхождение.

```bash
python3 scripts/research_mode.py attach-input --id <research-id> --file ./notes.md
python3 scripts/research_mode.py attach-input --id <research-id> --dir ./corpus
python3 scripts/research_mode.py attach-input --id <research-id> --glob './docs/**/*.md'
python3 scripts/research_mode.py attach-note --id <research-id> --title "Local context" --text "..."
python3 scripts/research_mode.py attach-url-as-md --id <research-id> --url "https://example.com/article"
python3 scripts/research_mode.py attach-pdf --id <research-id> --file ./paper.pdf
```

Изображения, прикреплённые через `attach-input`, помечаются как
`content_hint=image`, чтобы будущие итерации могли воспринимать их как
визуальные входные материалы.
`attach-url-as-md` принимает только URL с `http://` и `https://` и блокирует
локальные или приватные сетевые хосты, включая redirect targets.

#### Подготовка локального окружения

`prepare-runtime` используется, когда задаче нужны локальный код,
структурированный анализ или экспорты.

```bash
python3 scripts/research_mode.py prepare-runtime --id <research-id>
python3 scripts/research_mode.py prepare-runtime --id <research-id> --package pandas --package openpyxl
```

Ожидаемая структура внутри задачи:

```text
workspace/
  analysis/
  tools/
  data/
  outputs/
  outputs/screenshots/
  outputs/vision/
  tmp/
  data/analysis.sqlite
  analysis/schema.sql
  analysis/queries/
```

Task-local Python-пакеты сейчас разрешены через `--package`. Необычные или
рискованные пакеты нужно проверять перед установкой и фиксировать причину,
если пакет существенно влияет на результат.

Полученные страницы, PDFs, prompts или task artifacts не должны сами принимать
решение об установке package; package installation — controlled
operator/runtime capability. `prepare-runtime` может создавать task-local
virtual environment и запускать Python tooling через subprocesses. Пути
interpreter и venv полезны для локальной диагностики, но public/package-facing
summaries должны предпочитать task-relative или redacted paths, если абсолютный
путь не нужен.

Более строгая package allowlist или lock policy — future layer, а не часть
текущего baseline.

#### Команды ревью и доставки

Команды ревью:

```bash
python3 scripts/research_mode.py approve --id <research-id>
python3 scripts/research_mode.py approve --id <research-id> --approved-artifact final-report.md
python3 scripts/research_mode.py request-changes --id <research-id> "что нужно изменить"
python3 scripts/research_mode.py reopen --id <research-id> --feedback "почему задача открыта снова"
```

Команды доставки:

```bash
python3 scripts/research_mode.py format-delivery --id <research-id> --channel file

python3 scripts/research_mode.py mark-delivered \
  --id <research-id> \
  --primary-file final-report.md \
  --summary-text "Итоговый отчёт готов." \
  --channel-strategy attach \
  --ready
```

`awaiting_review` само по себе не означает готовность к доставке.
`delivery.ready=true` появляется после утверждения или явной отметки доставки.

Для нескольких reviewable deliverables используется
`working_memory.output_contract.outputs[]`, а фактические файлы указываются в
`finalization.candidate_artifacts` / `delivery.outputs`. MIME values — открытые
строки из контракта или worker result; Research Mode не держит registry
extension/MIME и не выводит роль или provenance из имени файла, текста или
порядка в списке. Для provenance используются id-ссылки `source_for` и
`derived_from`.

Finalization записывает `output_decision` для structured outputs.
`deliverable_decision`, `working_memory.output_contract.kind` и
`finalization.primary_deliverable_kind` остаются legacy compatibility для
single-output модели.

#### Связанное исследование

Связанное исследование используется, когда утверждённый результат открывает
новую ограниченную исследовательскую задачу.

```bash
python3 scripts/research_mode.py create-linked-research \
  --id <research-id> \
  --goal "Подробно проверить самый рискованный вариант" \
  --relation follow-up \
  --carry-summary \
  --carry-open-questions \
  --carry-constraints
```

Полезные параметры переноса:

- `--carry-summary`;
- `--carry-open-questions`;
- `--carry-constraints`;
- `--carry-deliverable`;
- `--carry-approved-artifact`.

#### Проверки качества

Проверка только документации:

```bash
python3 scripts/check_research_mode_docs.py
```

Полная проверка релиза и поведения:

```bash
scripts/check_research_mode.sh
```

Если skill установлен из ClawHub и shell script в вашей среде не исполняемый,
запустите тот же gate явно через `bash`:

```bash
bash scripts/check_research_mode.sh
```

Полная проверка запускает compile checks, linting, docs smoke, release smoke,
type checks, selftest-runner и pytest-compatible tests.

GitHub Actions запускает ту же полную проверку и Bandit security smoke scan
при push в `main` и в pull requests. CodeQL сейчас не включён в baseline
workflow; лёгкий security baseline — это release gate плюс Bandit smoke scan.

### Архитектура

Проект завязан на архитектуру OpenClaw cron:

1. У задачи есть директория с `state.json` и артефактами.
2. OpenClaw cron запускает изолированные рабочие итерации.
3. Каждая итерация делает один ограниченный цикл: `begin` → работа → JSON-результат → `finish`.
4. Рабочие итерации сериализуются на уровне research root через global iteration queue.
   Несколько задач можно планировать одновременно; пропущенный тик с
   `deferred:global-research-lock` означает ожидание очереди, а не сбой.
5. `awaiting_review` останавливает новые рабочие блокировки, пока оператор не выполнит
   `approve`, `request-changes`, `reopen` или `stop`.

Скрипты можно запускать руками, но штатная модель — именно OpenClaw cron, а не
самостоятельный Python-демон.

Полное описание архитектуры со схемами:
- `ARCHITECTURE.md`

### Карта документации

Начинать лучше с руководства, которое соответствует задаче:

- `README.md` — обзор проекта, установка, использование из чата, параметры запуска, операции, ревью, доставка, расписание, локальное окружение и проверки качества.
- `TROUBLESHOOTING.md` — порядок диагностики, частые сбои и безопасные способы исправления.
- `ARCHITECTURE.md` — модель системы, данные, жизненный цикл, финальная проверка и принципы дизайна.
- `docs/CLI.md` — стабильная операторская CLI-поверхность и более изменчивые/internal helpers.
- `docs/STATE_VERSIONING.md` — политика совместимости `version` и ожидания по миграциям.
- `schemas/` — JSON-срезы контрактов для task state, worker results, adequacy, finalization и delivery intents.
- `ROADMAP.md` — публичное направление проекта и текущая граница поддержки.
- `CONTRIBUTING.md` — среда разработки, ожидания к pull request и правила приватности для публичных изменений.
- `examples/` — проверенные примеры итоговых пакетов, созданных задачами Research Mode.
- `RELEASING.md` — процедура релиза, граница пакета и состав публичного репозитория для сопровождающих.
- `SECURITY.md` — модель безопасности и правила сообщения о проблемах.
- `AGENTS.md` — заметки по сопровождению репозитория для агентов-разработчиков.

### Smoke-проверка для сопровождающих

Из корня репозитория:

```bash
python3 scripts/release_smoke.py
```

### Представления для оператора

Для проверки используются:

- `summary`
- `status`
- `health`
- `reconcile`
- `preflight`
- `queue-status`
- `draft-report`
- `task-playbook.md`
- `runs.tsv`

Поверхность финальной проверки показывает `operator_next_action`: проверить
кандидат на результат, отправить задачу на доработку, вмешаться оператору,
проверить состояние ревью или продолжить исследование.

### Инварианты безопасности

- `research_id` не может содержать path traversal или разделители пути.
- `--path` должен указывать на задачу внутри выбранного `--root`.
- Артефакты для утверждения и выдачи должны лежать внутри директории задачи.
- Завершение исследования должно пройти `result.adequacy` перед финальной
  проверкой.
- `awaiting_review` означает готовность к ревью, а не доставку пользователю.
- Финальная проверка от рабочей итерации требует `result.finalization.status="passed"`.
- Сырые артефакты рабочей области не должны становиться финальным результатом.
- Успешный `finish` пишет `transactions.finish.status=committed`.

### Проверка качества

Из корня репозитория перед тегом релиза или значимыми изменениями:

```bash
scripts/check_research_mode.sh
```

Проверка запускает `compileall`, `ruff`, проверку документации, релизный
smoke-тест, `pyright`, selftest-runner и pytest-совместимый прогон.

Процедура релиза для сопровождающих:
- `RELEASING.md`

Архитектура и заметки о релизе:
- `ARCHITECTURE.md`
- `RELEASE_NOTES.md`

Сопровождение репозитория:
- `SECURITY.md`
- `AGENTS.md` — заметки для агентов-разработчиков и сопровождающих

Лицензия: Apache License, Version 2.0. См. `LICENSE`.

Документационный контракт проверяется через `scripts/check_research_mode_docs.py`
и входит в общий `check_research_mode.sh`. Он проверяет обязательные docs-файлы,
ключевые инварианты, описанные CLI-команды и примеры `bash` относительно
`argparse`.
