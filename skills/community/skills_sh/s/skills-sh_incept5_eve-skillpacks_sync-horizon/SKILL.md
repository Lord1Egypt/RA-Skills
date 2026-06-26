---
name: sync-horizon
description: Sync eve-skillpacks with latest eve-horizon changes. Goes deep into plans, code, and commits to understand what shipped — then cascades to skills and reference docs.
---

# Sync Horizon

Synchronize eve-skillpacks with the latest state of the eve-horizon repository.

## Core Insight

System docs often lag behind implementation. Features ship via feat commits with plans marked "Implemented" — but `docs/system/` may not update for weeks. This sync goes to the source: **plans, code changes, and commit messages** tell us what actually shipped. System docs are one signal among many, not the primary driver.

## Prerequisites

- The eve-horizon repo must be at `../eve-horizon` (sibling directory)
- `.sync-state.json` must exist in the repo root (create from template if missing)
- `.sync-map.json` must exist in the repo root

## Architecture: Orchestrator + Parallel Workers

You (the orchestrator) discover what shipped and dispatch focused workers. Each worker handles one update in isolation with its own context budget.

The orchestrator reads **lightweight signals** (commit log, plan headers, file stats, CLI module list). Workers read the **heavy content** (plan bodies, code diffs, source docs, target files).

## Output Standards

- Distill only shipped platform behavior. Plans marked Implemented/Complete describe shipped features.
- Do not carry roadmap content into skillpacks. Ignore plans marked Proposed/Draft and sections like `Planned (Not Implemented)`, `What's next`, or "current vs planned" framing.
- Keep `eve-work/eve-read-eve-docs/SKILL.md` task-first: route by intent, load only the minimal reference files needed.
- Keep reference docs scoped and actionable — curated distillations, not copies.

## Workflow

### Phase 1: Deep Discovery (orchestrator)

Read lightweight signals from multiple dimensions to understand what actually shipped.

#### 1a. Commit log

```bash
cd ../eve-horizon && git log --oneline <last_synced_commit>..HEAD
```

Categorize commits:
- `feat:` — new capabilities (primary interest)
- `fix:` — bugfixes that may affect documented behavior
- `docs:` — documentation changes (check if they describe already-shipped features)
- `chore:` / `refactor:` — usually no skillpack impact, but note removals

#### 1b. Plan intelligence

This is the richest signal. Plans describe what shipped, why, and how.

```bash
cd ../eve-horizon && git diff --stat <last_synced_commit>..HEAD -- docs/plans/
```

For each changed plan, read its **header only** (first 15-20 lines) to extract status:

```bash
cd ../eve-horizon && head -20 docs/plans/<plan-file>.md
```

Categorize:
- **Shipped**: Status contains `Implemented`, `Complete`, or `Done` — these are the primary source of truth for new capabilities
- **In progress**: Status contains `In Progress`, `Partially Implemented` — note for awareness but don't distill unfinished work
- **Proposed/Draft**: Status contains `Proposed`, `Plan`, `Draft`, `Ready to build` — skip entirely
- **Removed**: Plan files deleted in this range — something was deprecated or abandoned

**IMPORTANT**: Do not read full plan bodies. Just headers. Workers will read the plans they need.

#### 1c. Code signal

New CLI commands, DB migrations, and package changes confirm what shipped and reveal capabilities that plans may not fully describe.

```bash
# New/changed/removed CLI commands
cd ../eve-horizon && git diff --stat <last_synced_commit>..HEAD -- packages/cli/src/commands/

# New DB migrations (table/column names reveal capability shape)
cd ../eve-horizon && git diff --stat <last_synced_commit>..HEAD -- packages/db/migrations/

# Key package changes (new modules, removed modules)
cd ../eve-horizon && git diff --stat <last_synced_commit>..HEAD -- packages/shared/src/ packages/api/src/ packages/worker/src/ packages/gateway/src/ --stat-name-width=120 | head -50
```

#### 1d. System doc changes

Still a useful signal — especially for removals and corrections.

```bash
cd ../eve-horizon && git diff --stat <last_synced_commit>..HEAD -- docs/system/ AGENTS.md
```

#### 1e. Current CLI surface

Snapshot the current CLI command modules. This is the ground truth for what agents can invoke.

```bash
cd ../eve-horizon && ls packages/cli/src/commands/*.ts
```

### Phase 2: Capability Synthesis (orchestrator)

**STOP and think.** This is the critical step. Cross-reference all signals to build a capability map.

For each **shipped plan** (Implemented/Complete), create a capability entry:

```
Capability: <name>
  Plan: docs/plans/<file>.md (status: Implemented)
  Feat commits: <matching commit hashes>
  Code signal: <new CLI commands, new migrations, new/removed modules>
  System doc: <updated/created/unchanged>
  Scope: <which platform areas this touches>
  One-line summary: <what this capability does, from the plan header>
```

Also create entries for capabilities evidenced by feat commits that have **no corresponding plan** — these are smaller features or fixes that shipped directly.

Also note **removals**: plans deleted, CLI commands removed, modules deleted. These need to be cleaned from our skills too.

### Phase 3: Cascade Analysis (orchestrator)

For each capability in the map, determine its impact on `eve-read-eve-docs`:

#### 3a. Reference doc impact

For each capability, ask:
1. Does an existing reference already cover this area? → Worker updates it
2. Is this a new primitive that needs its own reference? → Worker creates it
3. Was something removed? → Worker cleans stale content from affected references

Cross-reference against the current reference index in `eve-work/eve-read-eve-docs/SKILL.md` and the `reference_docs` section of `.sync-map.json`.

#### 3b. SKILL.md routing impact

Check if `eve-work/eve-read-eve-docs/SKILL.md` needs:
- New entries in the Task Router
- New entries in the Index
- New rows in the Intent Coverage Matrix
- New trigger keywords in the frontmatter
- Removal of stale entries for deprecated capabilities

#### 3c. Other skill impact

Check `.sync-map.json` `skill_triggers` and `composite_triggers` for other skills affected. Also consider:
- `eve-se/eve-manifest-authoring` — if manifest shape changed
- `eve-se/eve-deploy-debugging` — if deploy/infra behavior changed
- `eve-se/eve-auth-and-secrets` — if auth model changed
- `eve-work/eve-agent-memory` — if storage primitives changed
- `eve-design/eve-fullstack-app-design` — if app patterns changed

### Phase 4: Plan Work Items (orchestrator)

For each update identified in Phase 3, create a work item:

- **Title**: `Update <target-file>: <capability name>`
- **Description** — everything a worker needs to operate independently:
  - The eve-horizon repo path (`../eve-horizon`)
  - The commit range: `<last_synced_commit>..HEAD`
  - Which plan(s) to read (the shipped plans relevant to this update)
  - Which source files to diff or read (code, system docs)
  - The target file path to update or create
  - Whether this is a reference doc update, skill update, new reference, or removal
  - The appropriate worker instructions from below

Add a final work item: `Update sync state and produce report` — blocked until all updates finish.

If any work item touches `eve-work/eve-read-eve-docs`, also add:
- `Run state-today compliance scan for eve-read-eve-docs`
- `Validate progressive-access routing in eve-read-eve-docs/SKILL.md`
- `Update .sync-map.json with any new reference doc mappings`

### Phase 5: Dispatch Workers (parallel)

Spawn one background worker per work item. Launch them all at once.

**Each worker prompt must be self-contained.** The worker has no access to the orchestrator's conversation. Include:

1. The plan file(s) to read — these are the primary source of truth
2. The git diff command for relevant code/doc changes
3. The target file to read and modify
4. The capability summary from Phase 2
5. The appropriate worker instructions from below

#### Worker Instructions: Reference Doc Update

> Your primary sources are **shipped plans** (marked Implemented/Complete) and **code changes**.
> System docs are secondary — they may lag behind or be absent.
>
> 1. Read the plan(s) listed in your task — understand what shipped and why.
> 2. Read the current reference doc you're updating.
> 3. Run the git diff for relevant source files (code, system docs).
> 4. If the plan references specific CLI commands or APIs, verify they exist:
>    ```bash
>    cd ../eve-horizon && ls packages/cli/src/commands/<name>.ts
>    ```
> 5. Distill the shipped capability into the reference doc:
>    - What it does (from plan + code)
>    - How to use it (CLI commands, manifest config, API calls)
>    - Key constraints or requirements
> 6. Exclude roadmap content. Only document what is implemented.
> 7. Edit the existing file; do not rewrite from scratch.
> 8. Preserve existing structure, voice, and formatting.

#### Worker Instructions: New Reference Doc

> 1. Read the plan(s) that describe this capability.
> 2. Check for any system doc coverage: `cd ../eve-horizon && cat docs/system/<name>.md` (may not exist).
> 3. Read the CLI command source if relevant: `cd ../eve-horizon && cat packages/cli/src/commands/<name>.ts`
> 4. Create a reference doc that follows the conventions of existing references in `eve-work/eve-read-eve-docs/references/`.
> 5. Include: purpose, CLI commands/flags, manifest config if relevant, key behaviors, constraints.
> 6. Keep it concise and agent-actionable. These are distillations, not documentation copies.
> 7. State-today only — no planned/roadmap content.

#### Worker Instructions: Skill Update

> Your primary sources are **shipped plans** and **code changes**.
>
> 1. Read the plan(s) listed in your task.
> 2. Read the current SKILL.md you're updating.
> 3. Update with new commands, changed workflows, or new capabilities.
> 4. Remove stale content that references deprecated features.
> 5. Keep state-today only. Ensure progressive disclosure.
> 6. Maintain imperative voice and conciseness.
> 7. Edit the existing file; do not rewrite from scratch.

#### Worker Instructions: SKILL.md Routing Update

> This worker updates the eve-read-eve-docs SKILL.md routing, index, and coverage matrix.
>
> 1. Read the current `eve-work/eve-read-eve-docs/SKILL.md`.
> 2. For each new reference doc created by other workers, add:
>    - A Task Router entry describing when to load it
>    - An Index entry with the file path and one-line description
>    - An Intent Coverage Matrix row if it serves a distinct user intent
> 3. For each removed capability, clean up stale routing entries.
> 4. Add any new trigger keywords to the YAML frontmatter.
> 5. Maintain alphabetical or logical ordering within sections.

#### Worker Instructions: Staleness Check

> This is a cross-cutting skill that spans multiple platform primitives.
> Your job is to validate that the skill's claims match current platform reality.
>
> 1. Read the SKILL.md and all files in its `references/` directory.
> 2. Read the shipped plan(s) listed in your task for context on what changed.
> 3. List current CLI command modules:
>    ```bash
>    cd ../eve-horizon && ls packages/cli/src/commands/*.ts
>    ```
> 4. Scan the skill for stale claims:
>    - "No dedicated X" / "X not available" / "not yet supported" — check if X now exists.
>    - "Current Gaps" or "Workarounds" sections — verify each gap is still a gap.
>    - Decision tables or comparison matrices — check for missing rows.
>    - References to removed features (e.g., inference/ollama/managed-models).
> 5. If stale claims are found, update the skill. Add new primitives. Remove false gaps.
> 6. Keep state-today only. Maintain imperative voice and conciseness.
> 7. Edit existing files; do not rewrite from scratch.
>
> Report what was stale and what you corrected.

#### Worker Instructions: Sync Map Update

> Update `.sync-map.json` to reflect new mappings discovered during this sync.
>
> 1. Read the current `.sync-map.json`.
> 2. For each new reference doc created, add a `reference_docs` entry mapping the source files to the target.
> 3. For each new skill trigger relationship discovered, add a `skill_triggers` entry.
> 4. For removed source docs, clean up stale mappings.
> 5. Ensure `watch_paths` covers any new directories that should be monitored.

#### Example Worker Prompt

```
You are updating a reference doc in the eve-skillpacks repository.

## Your Task
Update the file: eve-work/eve-read-eve-docs/references/agents-teams.md
Add coverage for agent aliases (short names for chat addressing).

## Capability Summary
Agent aliases let users declare short names for agents instead of using full
project-slug-agent-name. Declared in manifest under `agents[].alias`. Resolved
at chat dispatch time. Status: Implemented.

## Primary Source
Read the plan: cd ../eve-horizon && cat docs/plans/agent-aliases-plan.md

## Code Confirmation
The agents CLI was updated: cd ../eve-horizon && git diff <commit>..HEAD -- packages/cli/src/commands/agents.ts
New migration: packages/db/migrations/00076_add_agent_alias.sql

## Target
Read and edit: eve-work/eve-read-eve-docs/references/agents-teams.md

## Rules
- Distill only shipped behavior from the plan and code
- Edit the existing file; do not rewrite from scratch
- These are curated distillations for agents, not copies
- Keep it concise and actionable
```

### Phase 6: Collect Results and Finalize (orchestrator)

Wait for all workers to complete.

Once all update work items are done:

1. Get current HEAD:
   ```bash
   cd ../eve-horizon && git rev-parse HEAD
   ```
2. Run state-today and progressive-access checks:
   ```bash
   ./private-skills/sync-horizon/scripts/check-state-today.sh
   ```
3. Update `.sync-state.json`:
   - Set `last_synced_commit` to the HEAD hash
   - Set `last_synced_at` to current ISO timestamp
   - Append to `sync_log` (keep last 10 entries)

### Phase 7: Report (orchestrator)

```
## Sync Report: <old_commit_short>..<new_commit_short>

### Commits
- <count> commits synced (<feat count> features, <fix count> fixes)

### Shipped Capabilities (from plans)
- <capability>: <one-line summary> (plan status, feat commits)

### Capability Cascade
For each shipped capability:
- <capability> → updated <reference/skill>, because <reason>

### Removals
- <what was removed/deprecated and cleaned from skills>

### Updated Reference Docs
- <file>: <what changed and why>

### New Reference Docs
- <file>: <what it covers>

### Updated Skills
- <skill>: <what changed>

### SKILL.md Routing Changes
- <new routes, index entries, or coverage matrix rows>

### Sync Map Changes
- <new mappings added>

### State-Today Compliance
- <pass/fail + scan results>

### Coverage Gaps
- <shipped capabilities with no reference doc yet>
- <plan files with no sync-map entry>
- <CLI commands with no documentation coverage>

### Next Steps
- <manual follow-up needed>
```

## Key Constraints

- **Plans are the primary source of truth** for understanding what shipped. System docs are secondary. Code changes are confirmation.
- **Orchestrator reads lightweight signals only**: commit log, plan headers (first 15-20 lines), file stats, CLI module list. Never full plans, full diffs, or source docs.
- **Workers read the heavy content**: full plans, code diffs, source docs, target files.
- **Worker independence**: Each worker prompt must be fully self-contained with plan paths, code paths, target path, capability summary, and update rules.
- **Parallelism**: All workers launch simultaneously. No worker depends on another worker's output (except the routing update worker, which should launch after reference doc workers finish).
- **Edit, don't rewrite**: Workers modify existing files incrementally.
- **State-today fidelity**: Only document shipped, implemented behavior.
- **Progressive access**: Preserve task-first routing in entry skills and keep deep detail in references.
