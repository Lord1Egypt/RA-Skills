# Sanitized Demo

Use this file to demonstrate the skill without exposing private workspace details.

## Goal

Show that the architecture is practical, not just conceptual.

This demo intentionally proves four things:
1. corpora are explicit
2. agent access is controlled
3. retrieval has a stable interface
4. maintenance has a selective refresh path

## Demo setup

Assume a workspace with this simplified structure:

```text
workspace/
  AGENTS.md
  SOUL.md
  skills/
  product/
    roadmap.md
    architecture.md
  research/
    notes.md
  specialist/
    data/
    specialist-guide.md
  retrieval/
    config/
    scripts/
    indexes/
```

## Step 1. Bootstrap sanitized config

```bash
python3 skills/workspace-local-retrieval/scripts/bootstrap_workspace_retrieval.py \
  --dest retrieval \
  --workspace-root /ABSOLUTE/PATH/TO/WORKSPACE
```

Expected result:
- `retrieval/config/corpora.json`
- `retrieval/config/agent_corpora.json`
- `retrieval/config/agent_memory.json`

## Step 2. Customize corpora

Example corpus split:
- `workspace-core` → shared workspace docs
- `workspace-product` → product plans and architecture notes
- `workspace-research` → research notes
- `workspace-specialist-private` → specialist-only materials

## Step 3. Define agent access

Example policy:
- `main` can access `workspace-core`, `workspace-product`
- `research-agent` can access `workspace-research`
- `specialist-agent` can access `workspace-specialist-private`

Important check:
- no agent gets broad access “just in case”

## Step 4. Query through one wrapper

Example command:

```bash
node retrieval/scripts/workspace_search.mjs "architecture roadmap" --agent main --json
```

Expected outcome:
- results come only from corpora allowed to `main`
- response shape is machine-friendly and stable

## Step 5. Verify denial path

Try a disallowed query scope:

```bash
node retrieval/scripts/workspace_search.mjs "specialist data" --agent main --corpus workspace-specialist-private --json
```

Expected outcome:
- non-zero exit or clear denial message
- no silent widening of scope

This is a feature, not a failure.

## Step 6. Verify maintenance path

After editing a small number of files, run a refresh helper that:
- reports changed corpora
- reports changed files
- chooses `file-selective-reindex` when appropriate
- falls back to full rebuild only when necessary

What to check:
- the changed set is explainable
- the chosen action is proportionate
- embeddings are refreshed only where needed when supported

## What this demo proves

A good retrieval architecture is not only about finding relevant text.
It should also show:
- explicit boundaries
- explainable access rules
- stable interfaces
- maintainable freshness workflows

That combination is the main point of the skill.
