---
name: grap-skill
description: Skill Graph for Analogical Reasoning. Build a graph over SKILL.md skills, choose one primary skill, and retrieve complementary support instead of naively attaching top similar skills.
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---

# Skill Graph for Analogical Reasoning

Use this skill when the user wants to work with a **graph skill** over local `SKILL.md` folders.

This skill is for:

- graph-based skill indexing
- analogical reasoning and transfer
- one primary skill plus complementary support
- avoiding naive "top similar skills" retrieval

The full Python package and CLI for this project are available in the GitHub repository.

## What this skill does

This skill wraps the `grap-skill` capability.

It supports three primary commands:

- `/grap-skill build`
- `/grap-skill query`
- `/grap-skill look`

## Core rule

- `build` is the only command that may scan skill folders and update the graph.
- `query` and `look` are read-only against an existing `graph.json`.
- Do not silently rebuild during `query`.

## Code-backed usage

This skill is allowed to call code.

The `python3 {baseDir}/scripts/run_grap_skill.py ...` commands below are the
stable execution entrypoints intended for the skill runtime and for model-driven
tool use. They let the skill call a controlled wrapper inside the installed
skill bundle instead of relying on ad hoc shell reconstruction.

Preferred execution order:

1. Use the helper script in `{baseDir}/scripts/run_grap_skill.py`.
2. If the Python package is installed in the current interpreter, the wrapper may use `python -m auto_grap_skill`.
3. If neither bundled code nor the local Python package is available, direct the user to the GitHub repository for this project and install the Python package first.

## Primary commands

### `/grap-skill build`

```bash
python3 {baseDir}/scripts/run_grap_skill.py build --source <skills_dir> --output <graph_dir>
```

Example:

```bash
python3 {baseDir}/scripts/run_grap_skill.py build --source ./skills-main --output ./.grap-skill
```

### `/grap-skill query`

```bash
python3 {baseDir}/scripts/run_grap_skill.py query "<task text>" --graph <graph_json_path>
```

Example:

```bash
python3 {baseDir}/scripts/run_grap_skill.py query "edit a docx file with comments" --graph ./.grap-skill/graph.json
```

### `/grap-skill look`

```bash
python3 {baseDir}/scripts/run_grap_skill.py look --graph <graph_json_path> --output <html_path>
```

Example:

```bash
python3 {baseDir}/scripts/run_grap_skill.py look --graph ./.grap-skill/graph.json --output ./.grap-skill/graph-look.html
```

## How to interpret results

- `primary_skill` is the execution center.
- Always treat `primary_skill` as the default lead. Use a `supporting_skill` only if it adds clear missing coverage and does not conflict with or dilute the primary skill. If a suggested supporting skill is not actually helpful for the current task, do not adopt it.
- `supporting_skills` are the only skills that should normally supplement the primary skill in context.
- `fallback_skills` are substitutes for failure paths.
- `similar_skills` are for graph browsing, not default prompt context.

## Why this is different

Most retrieval systems stop at similarity.
This one tries to separate:

- the skill that should lead execution
- the skills that add complementary coverage
- the skills that are merely nearby or redundant

That is the whole analogical-reasoning goal of this project.

## More files in this skill

- `README.md` — human-facing usage and install notes
- `reference.md` — algorithm and result interpretation
- `scripts/run_grap_skill.py` — helper wrapper that calls the actual Python package/CLI

## GitHub version

The GitHub release of this project should also point users back to this skill
bundle for skill-style installation:

- ClawHub/OpenClaw install: `openclaw skills install skill-graph-for-analogical-reasoning`
- GitHub/Python install: use the repository's Python package and local CLI when a full source checkout is preferred
