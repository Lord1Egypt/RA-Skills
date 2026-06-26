# graph-task CLI surface

> Legacy prototype note: this CLI currently operates on `graph.json` runs.
> In the md-first direction, treat its outputs as legacy behavior, migration help, or derived snapshots/exports — not canonical markdown state.

Use the bundled CLI with:

```bash
python3 scripts/graph_task.py <command> ...
```

All commands accept either:
- a run directory (the CLI will use `graph.json` inside it), or
- a direct path to `graph.json`

## Shared status vocabulary

Use the same minimal status set everywhere:
- `pending`
- `active`
- `done`
- `blocked`
- `cancelled`

## Commands

### init
Create a new run directory with `graph.json` and `summary.md`.

```bash
python3 scripts/graph_task.py init ./runs/demo \
  --id demo-project \
  --title "Demo project" \
  --description "Test graph" \
  --goal "Reach a validated state"
```

To initialize inside a git-backed vault/work repo, point `path` at the desired local checkout directory and pass a repo URL. The CLI will clone or refresh the checkout, then create the run under `<checkout>/<project-id-slug>/`.

```bash
python3 scripts/graph_task.py init ./tmp/company-vault \
  --repo-url https://github.company.com/ORG/obsidian-vault.git \
  --repo-branch main \
  --id graph-task-demo \
  --title "Graph task demo" \
  --description "Repo-backed run" \
  --goal "Write into a project-specific folder"
```

### show
Render the current graph as a summary or raw JSON.

```bash
python3 scripts/graph_task.py show ./runs/demo
python3 scripts/graph_task.py show ./runs/demo --format json
```

### add-step
Add a Project-level Step.

```bash
python3 scripts/graph_task.py add-step ./runs/demo \
  --id step-1 \
  --step-type implementation \
  --description "Implement state handling"
```

### add-step-edge
Connect two Steps.

```bash
python3 scripts/graph_task.py add-step-edge ./runs/demo \
  --id step-edge-1 \
  --from-step step-1 \
  --to-step step-2
```

### add-phase
Add a Step-level Phase and automatically create its root node.

```bash
python3 scripts/graph_task.py add-phase ./runs/demo \
  --step-id step-1 \
  --id phase-diverge-1 \
  --phase-type diverge \
  --description "Explore implementation options"
```

### add-phase-edge
Connect two Phases inside a Step.

```bash
python3 scripts/graph_task.py add-phase-edge ./runs/demo \
  --step-id step-1 \
  --id phase-edge-1 \
  --from-phase phase-diverge-1 \
  --to-phase phase-verify-1
```

### add-node
Add a work node to a Phase.

```bash
python3 scripts/graph_task.py add-node ./runs/demo \
  --phase-id phase-diverge-1 \
  --id node-1 \
  --title "Compare libraries" \
  --description "Check Zustand and Redux"
```

### add-edge
Connect two Nodes inside a Phase.

```bash
python3 scripts/graph_task.py add-edge ./runs/demo \
  --phase-id phase-diverge-1 \
  --id edge-1 \
  --from-node phase-diverge-1-root \
  --to-node node-1 \
  --edge-type flow
```

### set-status
Set the status on a Project, Step, Phase, or Node.

```bash
python3 scripts/graph_task.py set-status ./runs/demo \
  --entity-type node \
  --entity-id node-1 \
  --status active
```

### write-result
Append an expected-vs-actual record to a work node.

```bash
python3 scripts/graph_task.py write-result ./runs/demo \
  --node-id node-1 \
  --expected "Choose a candidate state library" \
  --actual "Selected Zustand after comparing complexity" \
  --status done \
  --notes "Simple enough for current scope"
```

### validate
Validate the graph against the current high-level rules.

```bash
python3 scripts/graph_task.py validate ./runs/demo
```

### summary
Regenerate and print `summary.md`.

```bash
python3 scripts/graph_task.py summary ./runs/demo
```

### export-obsidian
Export the current legacy JSON run into an Obsidian-friendly markdown projection.

This export is **non-canonical**. It is a derived view from `graph.json`, not the md-first source of truth.

```bash
python3 scripts/graph_task.py export-obsidian ./runs/demo ./tmp/demo-vault
python3 scripts/graph_task.py export-obsidian ./runs/demo ./tmp/demo-vault --force
```

### git-status
Show git sync state for a repo-backed run.

```bash
python3 scripts/graph_task.py git-status ./tmp/company-vault/graph-task-demo
```

### git-pull
Fast-forward pull the backing repo for a repo-backed run. This fails if the repo has uncommitted changes.

```bash
python3 scripts/graph_task.py git-pull ./tmp/company-vault/graph-task-demo
```

### git-push
Push the backing repo. If `--message` is provided, stage and commit all pending repo changes first.

```bash
python3 scripts/graph_task.py git-push ./tmp/company-vault/graph-task-demo \
  --message "Update graph-task project"
```

### git-sync
Pull first, then optionally commit all pending changes, then push. This is the main manual sync command for repo-backed runs.

```bash
python3 scripts/graph_task.py git-sync ./tmp/company-vault/graph-task-demo \
  --message "Sync graph-task project updates"
```

## Repo-backed run notes

- `--repo-url` on `init` records repo metadata into `project.repo`.
- Repo sync commands only work for runs initialized that way.
- The sync commands operate on the whole backing repo, not only one project folder.
- `git-pull` / `git-sync` intentionally use `pull --ff-only` to avoid hidden merge commits.
- If the repo is dirty, pull fails on purpose; resolve or commit local changes first.

## Current simplifications

For md-first work, prefer editing/validating canonical markdown directly rather than extending this JSON-first CLI unless the task is explicitly about legacy compatibility.


The current CLI intentionally does **not** have:
- a separate mutation engine
- hidden transition logic
- branch/retry/replan commands

If the structure changes, append new Steps / Phases / Nodes / Edges directly and preserve history in the graph.
