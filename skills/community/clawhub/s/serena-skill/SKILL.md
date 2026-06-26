---
name: serena
description: Use Serena-backed semantic code navigation and editing when working in existing software projects with non-trivial structure, especially multi-file repos where symbol-aware lookup and targeted edits are more reliable and token-efficient than brute-force file reading. Use when the environment exposes Serena tools such as project activation, symbol lookup, reference search, semantic search, file reads, directory listing, file finding, or symbol-scoped edits.
---

# Serena

Use Serena as the first choice for understanding and editing **existing** codebases when the necessary tools are available.

## What this skill is for

Use this skill when another agent needs to integrate Serena into its normal coding workflow instead of treating the repo as a pile of text files.

Aim for this behavior:

- activate the project once
- inspect structure semantically before reading large files
- trace references before editing
- prefer symbol-scoped edits when possible
- fall back to normal file tools only when Serena is missing a capability or fails

For extra examples and trigger patterns, read `references/integration-patterns.md`.

## Core workflow

1. Resolve the target project path.
2. Call `serena_activate_project`.
3. Start with structure discovery:
   - `serena_project_overview`
   - `serena_find_symbol`
   - `serena_list_dir`
   - `serena_find_file`
   - `serena_session_status` when you need to inspect active Serena sessions
4. Narrow scope with:
   - `serena_find_references`
   - `serena_search_pattern`
   - `serena_read_symbol`
   - `serena_read_file`
5. Prefer semantic edits when changing existing code:
   - `serena_replace_symbol_body`
   - `serena_insert_before_symbol`
   - `serena_insert_after_symbol`
   - `serena_rename_symbol`
6. Use broader edit tools only when symbol-scoped tools are not a good fit:
   - `serena_replace_content`
   - `serena_create_text_file`
7. Use `serena_execute_shell_command` only as an advanced escape hatch when project-context shell execution is genuinely the right tool.
8. Use `serena_call_tool` only when the normalized surface does not cover the needed Serena capability.
9. Fall back to ordinary file tools only when Serena cannot answer safely or reliably.

## When Serena is worth the overhead

Prefer Serena when:

- the project spans multiple files
- the user asks about references, call chains, or symbol relationships
- the user wants a precise edit to an existing class, function, method, or module
- reading whole files would be noisy or wasteful
- the repo already has real structure and semantic lookup is available

Skip or delay Serena when:

- the task is a tiny one-file change and the target location is already obvious
- you are creating a brand-new file with little dependency on existing code
- Serena is unavailable or failing and direct file tools are simpler
- the user already provided the exact file region and semantic lookup adds no value

## Tool preference order

For existing codebases, prefer this order:

1. `serena_activate_project`
2. `serena_project_overview` / `serena_find_symbol` / `serena_find_file`
3. `serena_find_references` / `serena_search_pattern`
4. `serena_read_symbol` / `serena_read_file`
5. symbol-scoped edit tools
6. broader Serena edit tools
7. `serena_session_status` for session inspection/debugging
8. `serena_execute_shell_command` only when semantic tools are not the right mechanism
9. fallback to `read`, `edit`, and `exec` only when needed

## Integration guidance for agent authors

When you want another agent to use Serena well, instruct it to:

- activate the project before semantic reads or edits
- inspect symbols and references before modifying code
- use normalized Serena tools first
- keep edits narrow and structured
- avoid whole-file rewrites when a symbol-scoped edit is possible
- treat passthrough as an escape hatch, not the default workflow

A good instruction pattern is:

> Use Serena on the repo. Start with `serena_activate_project`, then narrow scope with `serena_find_symbol`, `serena_find_references`, and `serena_read_symbol` before editing.

## Practical usage patterns

### Understand a repo area

Use this sequence:

1. `serena_activate_project`
2. `serena_find_file` or `serena_list_dir`
3. `serena_project_overview`
4. `serena_find_symbol`
5. `serena_read_symbol`

### Trace impact before changing code

Use this sequence:

1. `serena_find_symbol`
2. `serena_find_references`
3. `serena_search_pattern` if naming or text-level usage matters
4. `serena_read_symbol` for the most relevant callers/callees

### Make a targeted edit

Use this sequence:

1. locate the exact symbol
2. read the symbol body
3. inspect references if behavior changes could ripple outward
4. choose the narrowest valid edit tool
5. re-read the changed symbol or nearby references when confidence is low

## Editing rules

- Keep edits as narrow as possible.
- Prefer symbol-targeted edits over text replacement across a whole file.
- Prefer semantic rename over manual multi-file rename logic.
- Re-read the relevant symbol or references after a material edit when confidence is low.
- If semantic identity is ambiguous, do not guess; disambiguate using path or extra lookup.
- In read-only mode, do not attempt mutating Serena tools.

## Safety and fallback behavior

If Serena fails:

1. Explain briefly what failed.
2. Fall back to standard file-based workflow.
3. Keep using the smallest possible read/edit scope.
4. Do not pretend the semantic result was confirmed if it was not.

If a raw Serena passthrough tool is available:

- use it only when the normalized tool surface does not cover the needed capability
- prefer stable normalized tools for repeated workflows
- avoid passthrough for routine actions that already have a clear normalized tool
