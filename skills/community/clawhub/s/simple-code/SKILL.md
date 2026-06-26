---
name: simple-code
description: "Plan and build small, readable coding projects in three reliable modes: start, continue, and review. Think first, make a short plan, then delegate implementation/review/testing/bug-fixing/documentation/step-tracking to a coding sub-agent. Prefer the model openai-codex/gpt-5.3-codex by default. Use when the user asks for simple code, a small project, a self-contained utility, straightforward feature work, or a practical code review that should stay easy to read and easy to manage."
---

# Simple Code

## Overview

Use this skill for small coding work where readability, simplicity, and reliable progress matter more than cleverness.

This skill supports three explicit modes:

- `start` — create a minimal new project and get the first working version running
- `continue` — continue an existing project with new functionality, changed behavior, fixes, or focused improvements
- `review` — review the current codebase, a current commit, or current changes, then optionally make targeted follow-up improvements

For all three modes, the default expectation is the same:

- think first
- make a short plan
- do the real work in the project folder
- test and verify what is feasible
- add or update minimal documentation when needed
- record the work in `.steps/`
- report clearly what changed and what was verified

## Reliable Triggering

When the user wants to invoke this skill explicitly, they should be able to do it reliably by appending a mode option and a concrete request.

Preferred explicit trigger patterns:

- `simple-code start: <request>`
- `simple-code continue: <request>`
- `simple-code review: <request>`

Also accept slash-command style requests with appended options/details, for example:

- `/simple-code start build a tiny local markdown preview tool`
- `/simple-code continue add CSV export and improve error handling`
- `/simple-code review review current project and fix obvious structural issues`
- `/simple-code review current commit only`
- `/simple-code review working tree changes and patch if needed`

When the mode is explicit, follow it.

When the mode is not explicit, infer it from the task:

- new project / bootstrap / create / build from scratch → `start`
- add / change / improve / extend / continue existing project → `continue`
- review / inspect / audit / check current code / check current diff → `review`

If the user includes extra scope details, use them. For example:

- target project path
- desired feature
- constraints
- files/modules to focus on
- whether to patch after review
- whether to limit review to current commit or working tree

If the request is still ambiguous after that, ask one short clarifying question.

## Common Workflow

1. Read the request carefully and determine whether the mode is `start`, `continue`, or `review`.
2. If the task is project-like, work inside `agent_code/<project-name>` unless the user explicitly points to another project path.
3. Ensure the project has a `.steps/` folder.
4. Initialize or update `.gitignore` if needed so `.steps/` and everything under it are ignored.
5. Think through the task before coding.
6. Make a short plan and state the chosen approach briefly.
7. Spawn a coding sub-agent and prefer the model `openai-codex/gpt-5.3-codex` by default unless the user asks for something else.
8. Do the execution work inside the project folder: implementation, review, testing, bug-fixing, documentation, and `.steps/` tracking.
9. Keep changes simple, readable, and proportionate to the request.
10. Before finishing, verify what you reasonably can, document what changed, and state any remaining limitations honestly.

## Mode: Start

Use `start` when creating a new project or bootstrap implementation.

Goals:

- create the project cleanly
- get to a minimal working version quickly
- avoid overbuilding architecture before the first useful version exists

Workflow for `start`:

1. Create a properly named project folder under `agent_code/<project-name>`.
2. Create `.steps/` inside it.
3. Add `.gitignore` early and ignore `.steps/` from the start.
4. Set up the smallest sensible project structure.
5. Build the first working vertical slice.
6. Add the most important tests that validate the initial core behavior.
7. Add minimal documentation so the project can be understood and run.
8. Verify that the initial version works as far as feasible.

## Mode: Continue

Use `continue` when extending or improving an existing project.

Goals:

- preserve project continuity
- add or change behavior cleanly
- avoid unnecessary rewrites

Workflow for `continue`:

1. Read the relevant existing project before changing it.
2. Understand the current structure, conventions, and behavior.
3. Add the requested functionality or behavior change with the smallest practical edit set.
4. Prefer focused refactors only when they directly support the requested change or clearly improve readability/maintainability.
5. Update tests to cover the changed behavior.
6. Update minimal documentation when behavior, usage, or setup changed.
7. Verify that the changed behavior works as far as feasible.

## Mode: Review

Use `review` when the task is to inspect, critique, validate, or audit code, commits, or changes.

Possible review scopes include:

- the whole current project
- a specific module or file set
- the latest commit
- the current branch diff
- the working tree / uncommitted changes

If the user specifies a scope, use it.
If not, choose the most sensible current scope and state it clearly.

Goals:

- identify meaningful issues or improvement opportunities
- keep findings practical and concrete
- optionally make targeted follow-up changes when they are clearly useful and within scope

Workflow for `review`:

1. Read the review target completely enough to understand the relevant structure and behavior.
2. Identify issues in readability, structure, naming, logic, behavior, safety, maintainability, or test coverage.
3. Summarize the most important findings concretely.
4. If the user asked for fixes, or if small targeted improvements are obviously beneficial and within scope, apply those changes.
5. Verify any changes you made as far as feasible.
6. Update minimal documentation if the resulting behavior or usage changed.

## Verification Rules

For any mode, before finishing:

1. Run the relevant test, build, lint, or smoke-check commands if they are available and reasonable.
2. Verify the main requested behavior as directly as feasible.
3. If something cannot be verified, say exactly what was blocked and why.
4. Do not pretend a project works if it was not actually checked.

## Documentation Rules

- Add or update documentation proportionate to the size of the change.
- For very small projects or changes, a short README or usage note is enough.
- Do not create bloated docs for tiny utilities.
- If behavior, setup, or constraints changed, reflect that in documentation.

## Coding Rules

- Prefer clear names over compact tricks.
- Prefer fewer files and a smaller API when possible.
- Prefer standard tools for the language ecosystem.
- Avoid unnecessary dependencies.
- Handle invalid input and obvious failure cases clearly.
- Keep the implementation easy to read and easy to modify.
- Do not leave the code unverified if a local check is available.

## Project Layout Rules

For project-like requests, create or use this structure by default:

- `agent_code/<project-name>/`
- `agent_code/<project-name>/.steps/`
- source files in that folder root unless there is a good reason to add subdirectories
- tests in the same folder if the project is very small
- add a simple build file when appropriate, such as `CMakeLists.txt` for C++
- add or update `.gitignore` early so `.steps/` is ignored before commits start

## .steps Notes

Use `.steps/` to leave concise tracking notes.

When work results in a commit, create a note named:

- `.steps/<YYYYMMDD-HHMM>-<abbr>-<commit-hash>.md`

When work ends without a commit, create a note named:

- `.steps/<YYYYMMDD-HHMM>-<abbr>.md`

Each `.steps` note should stay short and include only:

- request summary
- short plan
- execution outcome

For review tasks, mention the review scope in the outcome.

## Git Rules

- Use git inside the project folder, not at the whole-workspace level, unless the user explicitly wants workspace-level git.
- Initialize git in the project folder if needed.
- Add `.steps/` to `.gitignore` before the first commit in a new project when possible.
- Commit meaningful milestones after verification.
- If the workspace root has temporary bootstrap git history and the user asks to remove it, remove only that root-level history.
- Do not rewrite git history unless the user explicitly asks.

## Response Style

When reporting back after work completion:

- start with a short ping that the code or review is ready
- state which mode was used: `start`, `continue`, or `review`
- briefly state what was built, changed, or reviewed
- include where it lives
- mention verification status honestly
- mention whether documentation was updated
- include the latest relevant commit hash if git was used
- for review tasks, include the review scope and whether follow-up patches were applied
