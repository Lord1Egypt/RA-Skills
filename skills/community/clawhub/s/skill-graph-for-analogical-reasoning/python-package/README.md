# Skill Graph for Analogical Reasoning

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache--2.0-blue.svg)](./LICENSE)

`Skill Graph for Analogical Reasoning` is a graph-powered retrieval engine for AgentSkills-compatible `SKILL.md` folders.

- pick one `primary_skill` as the execution center
- retrieve a small set of `supporting_skills` that add complementary value
- keep `similar_skills` separate from the default prompt context
- use the graph to support transfer, analogy, and non-redundant composition

This project is built for graph skill retrieval, analogical reasoning, and
cross-skill transfer over real skill folders.

## Highlights

- graph-based retrieval over `SKILL.md`
- one `primary_skill` plus complementary support
- not naive `top-k similar skills`
- read-only query over a persisted `graph.json`
- whole-graph HTML visualization with edge explanations
- code-backed ClawHub/OpenClaw skill bundle

## What You Get

- multiple skills say almost the same thing
- context gets wider but not smarter
- execution focus becomes weaker
- the model sees redundancy, not real analogy

- `primary_skill` answers: which skill should lead?
- `supporting_skills` answer: which skills fill what the primary skill does not cover?
- `fallback_skills` answer: which nearby options are substitutes rather than companions?
- `similar_skills` answer: what is graph-nearby, but should not be injected by default?

The graph is designed to separate leadership, support, fallback, and redundancy instead of collapsing everything into similarity.

## Quick Start

### Install

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -e .
```

### Build A Graph

```bash
./.venv/bin/grap-skill build --source ./skills-main --output ./.grap-skill
```

### Query The Graph

```bash
./.venv/bin/grap-skill query "edit a docx file with comments" --graph ./.grap-skill/graph.json
```

### Render The Graph

```bash
./.venv/bin/grap-skill look --graph ./.grap-skill/graph.json --output ./.grap-skill/graph-look.html
```

## Core Commands

### `build`

`build` is the only command allowed to scan skill folders and update the graph.

It currently:

- recursively scans `SKILL.md` and `skill.md`
- parses frontmatter and markdown instructions
- extracts descriptions, triggers, keywords, tool references, code references, and runtime constraints
- constructs a weakly supervised graph from those signals
- persists both a `similarity` view and a `complementarity` view into `graph.json`

`query` and `look` are read-only over the saved graph and do not silently rebuild.

### `query`

`query` selects a structured result instead of dumping a similarity list.

It returns:

- `primary_skill`
- `supporting_skills`
- `fallback_skills`
- `similar_skills`

The important part is how `supporting_skills` are selected.
They are not chosen by raw similarity.

They are scored by a balance of:

- `task_relevance`
- `complementarity`
- `execution_support`
- `redundancy_with_primary`

Current support scoring is:

```text
support_score =
  0.30 * task_relevance
  + 0.30 * complementarity
  + 0.25 * execution_support
  - 0.25 * redundancy_with_primary
```

This is the mechanism that moves retrieval away from nearest-neighbor packing and toward main-skill-plus-support selection.

### `look`

`look` renders the current graph as a standalone HTML view.

The visualization currently supports:

- full-graph browsing
- `Similarity` and `Complementarity` view switching
- edge color mapping from blue (`0`) to red (`1`)
- click-edge explanations with natural-language summaries
- evidence and score breakdowns for why an edge exists

## Graph Signals

At build time, the graph tries to infer relationships from `SKILL.md` itself, including:

- semantic description overlap
- shared keywords and trigger language
- tool and code affinity
- runtime and constraint compatibility

At query time, high-similarity neighbors can still be excluded from `supporting_skills` if they do not add enough non-redundant value.

## Example Output Shape

```json
{
  "primary_skill": "...",
  "supporting_skills": ["..."],
  "fallback_skills": ["..."],
  "similar_skills": ["..."]
}
```

Result interpretation:

- `primary_skill` is the execution center
- `supporting_skills` are the only skills that should usually supplement context
- `fallback_skills` are substitutes for failure paths
- `similar_skills` are for browsing and inspection, not default prompt packing

## Current Status

This repository is already usable as an early MVP.

Working now:

- graph build over `SKILL.md` folders
- read-only query over persisted `graph.json`
- primary-skill selection
- complementary support selection
- whole-graph HTML visualization
- edge explanations with evidence

Still early by design:

- stronger relations such as prerequisite and composition are not inferred yet
- graph quality is still bounded by what can be extracted from `SKILL.md`
- there is no trace-driven self-improvement loop yet

## Repository Layout

- `src/auto_grap_skill/` contains the Python package and CLI
- `skills/grap-skill/` contains the local skill wrapper
- `releases/github/` contains a visible GitHub-facing source snapshot
- `releases/clawhub-skill/` contains the final ClawHub upload bundle
- `releases/gist/` contains the long-form public markdown version

## Python Package And CLI

The installable package name is:

- `skill-graph-for-analogical-reasoning`

The local CLI command is:

- `grap-skill`

The module entrypoint also works:

```bash
./.venv/bin/python -m auto_grap_skill --help
```

## ClawHub Version

A code-backed ClawHub skill bundle is prepared in:

- `releases/clawhub-skill/skill-graph-for-analogical-reasoning`

That bundle is not markdown-only.
It includes:

- `SKILL.md`
- supporting documentation
- `scripts/run_grap_skill.py`
- `python-package/src/auto_grap_skill/`

The ClawHub bundle now carries both the wrapper entrypoint and the packaged Python source used by the project.

## Why The Name

`Skill Graph for Analogical Reasoning` is intentionally explicit.

It says what the project actually is:

- a skill graph
- for analogical reasoning
- over real `SKILL.md` skills
