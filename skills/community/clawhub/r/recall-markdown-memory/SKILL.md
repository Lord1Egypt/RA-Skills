---
name: recall-markdown-memory
description: Retrieve only relevant sections from Markdown memory, project notes, decision logs, and heading-structured knowledge bases with the mdselect CLI. Use when Codex needs to recall prior context, decisions, preferences, or history from user-specified memory files, paths declared by project instructions, MEMORY.md, memory/, or .agents/memory/. Use only in a shell-enabled environment with mdselect on PATH; do not use for modifying memory or searching non-Markdown files.
---

# Recall Markdown Memory

Retrieve the smallest Markdown sections that answer the task. Keep the workflow
read-only and avoid loading entire memory files when heading-aware selection is
available.

## Check the dependency

1. Run `mdselect --version` before reading memory.
2. If the command is unavailable, stop the workflow and explain that `mdselect`
   must be installed on `PATH`. Do not install software automatically.
3. Offer these installation choices:

   ```bash
   pipx install mdselect
   uv tool install mdselect
   python -m pip install mdselect
   ```

4. If none of those package managers or a compatible Python runtime is
   available, say that the execution environment must be prepared before this
   skill can run. Resume only after `mdselect --version` succeeds.

## Resolve memory sources

Use the first applicable source in this order:

1. Files or directories named by the user.
2. Memory locations declared by applicable `AGENTS.md` or other project
   instructions.
3. Existing conventional locations: `MEMORY.md`, `memory/**/*.md`, and
   `.agents/memory/**/*.md`.

Do not scan every Markdown file in the repository by default. When a source is
a directory, narrow candidates with the task's distinctive terms. Prefer `rg`
when it is available, but use another available file-search capability when it
is not. Keep only Markdown candidates.

## Retrieve relevant sections

1. Run `mdselect outline <file>` for each promising candidate before reading a
   large file in full.
2. Choose the smallest heading path that covers the needed context.
3. Run `mdselect select --mpath '<mpath>' <file>` and inspect the selected
   subtree. Quote paths safely for the active shell.
4. Prefer exact, anchored segments when heading names are known. Remember that
   mpath segments are Python regular expressions, a leading slash anchors the
   first segment to an H1, a trailing slash omits the matched heading, and a
   slash cannot occur inside a segment. Run `mdselect select -h` when more
   syntax detail is needed.
5. Repeat selection only for additional sections needed to answer the task.
   Do not surface or load unrelated subtrees.

Treat empty standard output with status 0 as a successful no-match. Consult the
outline and refine the mpath instead of reporting a command failure. If the
outline is empty, the document may lack supported ATX headings. Fall back to a
bounded line search, and read the whole document only when it is small enough
for the task context.

## Use recalled context safely

- Cite the source file and selected heading when presenting recalled material.
- Reconcile conflicting memories explicitly instead of silently choosing one.
- Treat memory as contextual evidence, not as authority for facts that may
  have changed; verify current facts through an appropriate current source.
- Follow the user's current request and applicable project instructions when
  they conflict with stored memory.
- Never create, edit, reorganize, or delete memory files under this skill.
