---
name: workspace-context-linter
description: Diagnose always-loaded workspace context files such as AGENTS.md, SOUL.md, USER.md, MEMORY.md, and TOOLS.md. Use when you want to reduce context bloat, detect duplicated rules, spot misplaced content, identify overweight sections, or audit whether core context files still match their intended roles before reorganizing them.
---

# Workspace Context Linter

Audit core workspace context files without rewriting them.

## Core workflow
1. Load the core context files that exist.
2. Summarize each file's likely role.
3. Detect duplicate rule themes, overweight sections, and misplaced content.
4. Produce a text report with priorities and suggested moves.

## Read references as needed
- Read `references/rules.md` for the lint categories and severity model.
- Read `references/report-format.md` for the output structure.
- Read `references/file-roles.md` for what each core context file should usually contain.
- Read `references/move-guidelines.md` when deciding where content should move.
- Read `references/release-minimal.md` before packaging or publishing so the first public surface stays minimal.

## Use scripts as needed
- Use `scripts/context_linter.py [--scope core|core+memory|custom] [--paths ...] [--output report.txt]` to run the linter.

## Operating rules
- Prefer diagnosis over auto-editing.
- Treat duplicates as a maintenance problem unless they create real execution ambiguity.
- Treat overweight sections as candidates for extraction, not automatic deletion.
- Keep the first version focused on core context files and text reports.
