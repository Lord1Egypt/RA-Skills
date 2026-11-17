---
name: code-abstraction-encapsulation
description: Use when converting repeated, messy, or over-specialized code into reusable components, clean interfaces, and engineering rules.
version: 0.1.0
status: preview
language: en
type: compression
models:
  - Codex
  - Claude
---

# Code Abstraction And Encapsulation Skill

## When To Use

Use this skill when code, scripts, or automation flows show repeated patterns that should become reusable modules, helpers, or rules.

Good fit:

- Several functions do almost the same thing.
- A script mixes data processing, printing, rendering, and side effects.
- Bug fixes reveal a reusable defensive pattern.
- One-off code should become a library-quality component.

## Inputs

Collect:

- Source files or code snippets.
- Known behavior that must not change.
- Repeated patterns or pain points.
- Runtime, language, framework, and test constraints.
- Desired target: helper, class, package, hook, API, CLI, or skill rule.

## Workflow

1. Inspect the existing code before proposing abstraction.
2. Identify duplication, unstable boundaries, hardcoded values, and side effects.
3. Preserve behavior with tests or explicit verification steps.
4. Separate computation from presentation:
   - Core logic should return data.
   - UI, logging, printing, and rendering should stay outside core logic.
5. Extract the smallest useful reusable unit.
6. Replace call sites only when the risk is understood.
7. Document the interface, examples, and limits.
8. Record reusable engineering rules for future compression.

## Output Contract

Return:

1. `Observed Pattern`
2. `Abstraction Candidate`
3. `Behavior Preservation Plan`
4. `Proposed Interface`
5. `Implementation Steps`
6. `Tests Or Verification`
7. `Reusable Rule`

## Codex Notes

Codex should make scoped edits, follow repository style, run targeted tests, and avoid broad refactors unless needed. It must not overwrite unrelated user changes.

## Claude Notes

Claude should help reason about abstraction boundaries, naming, tradeoffs, and rule extraction before code changes.

## Boundaries

- Do not abstract only because two snippets look similar.
- Do not change behavior without a test or explicit verification.
- Do not hide important domain differences behind a generic helper.
- Do not combine computation and presentation in the extracted component.

## Example Prompt

```text
Use the Code Abstraction And Encapsulation Skill.

Source: Three scripts parse product review JSON, each with different hardcoded paths and print statements.
Goal: Extract a reusable parser and keep printing in a separate CLI layer.
Output: Interface, implementation plan, tests, and reusable rule.
```
