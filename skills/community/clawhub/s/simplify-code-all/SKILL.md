---
slug: simplify-code-all
displayName: "simplify-code"
version: 1.1.1
name: simplify-code
description: Simplify, clean up, or refactor existing code in any language (JS/TS, Python, Java, Go, Rust, C#, C/C++, PHP, SQL, Bash…) while preserving behavior and public APIs. Use whenever the user asks to simplify, tidy, clean up, refactor, de-nest, deduplicate, remove dead code, modernize syntax (const/let, ===, ??, streams, async/await, for..of), rewrite a function more concisely, polish recently written code, fix code smells (god class, feature envy, primitive obsession), or "make this cleaner" — including 简化代码, 精简代码, 重构, 整理代码, 代码整洁, 去除重复代码, 减少嵌套, 代码坏味道, 这段代码太乱了; read-only simplification assessments too. Not for performance tuning, bug fixes, new features, porting between languages, lint config, writing tests, security review, or prose (性能优化、修 bug、新功能、代码翻译、写单测、文章精简).
license: MIT
metadata:
  version: "1.1.1"
---

> This file is longer than one read (~4,000 characters). Keep reading in chunks until the end (Golden rules, Output format, Quick checklist, References) before editing.

# Simplify Code

Make code easier to read and change without changing what it does: the *smallest readable equivalent*, in small steps that are each checked. Non-negotiable (details in Golden rules below): preserve behavior and public APIs; claim only checks you ran; if a command, delete, or tool is denied, report it and leave it — don't route around it with another tool or script.

## Workflow

Run the steps in order. Step labels are for your tracking; the user sees only the Step 7 report.

### Step 0 — Mode and scope
- **Do:** fix the scope (the code the user named; else this session's changes or the working diff); read `AGENTS.md`/`CLAUDE.md`, lint/formatter config, neighbouring code.
- **Output:** mode + in-scope files/functions + language(s) (open that section of `references/languages.md`).
- **Decision:** pasted snippet, no repo → Steps 1–7, verifying by reasoning or a tiny script · read-only assessment → **R-branch**, no edits · repository code → Steps 1–7 in place (`references/assessment.md` if large or tools are limited) · user asked for a risky change (`||`→`??`, `===` everywhere, `Promise.all`) → handle in Step 3.

### Step 1 — Understand the contract
- **Do:** state inputs, outputs, side effects, errors, edge cases; find the public surface (`export`, `pub`, `public`, `__all__`, callers).
- **Output:** a 1–2 sentence contract + public symbols you must not change.
- **Done when:** for every in-scope function you know who calls it and what it promises.

### Step 2 — Baseline and safety net
- **Do:** run existing tests/lint/build/type checker **before any edit**; with no tests, write a throwaway differential check (old vs new on edge inputs) outside the project or delete it afterwards. Edge inputs: `0`, `''`, `false`, null/undefined, NaN, negatives, fractions, empty/duplicate collections, duplicate keys, boxed values (`new String('x')`), sync throws.
- **Output:** baseline record (commands + results, or "not runnable: why") + edge-input list.
- **Done when:** Step 6 has something to compare against.

### Step 3 — Plan by payoff and risk
- **Do:** list candidates: dead code → nesting → redundancy → duplication → naming → conditionals → structure (`references/rules.md` §19–20, language section). Tag each **apply** (private, provably equivalent), **propose** (changes behavior/API) or **skip**. For a risky user request, apply the safe parts and give a concrete input that would change for each unsafe part. If the requested form can't be made exactly equivalent, apply the closest equivalent form instead (e.g. `collect(HashMap::new, (m, u) -> m.put(k, v), Map::putAll)` when `toMap` would reject null values or duplicates) or keep the original — never ship a version with a known differing input, even with a note.
- **Output:** ordered, tagged plan.
- **Decision:** nothing to apply or propose → **Already simple exit** (change nothing, go to Step 7). Else → Step 4.

### Step 4 — Apply one transformation
- **Do:** make exactly one behavior-preserving edit from the plan.
- **Output:** one small edit.
- **Done when:** complete and inside scope → Step 5.

### Step 5 — Check that transformation
- **Do:** run fast checks (affected tests, type checker after any type change); review the lines against `references/behavior-traps.md`: *which input makes old and new differ?*
- **Output:** pass, or the differing input.
- **Decision:** pass → Step 4 for the next item · any known differing input (found by a check *or* by reasoning) = fail → revert only this edit, move it to *propose* with the input · plan done → Step 6.

### Step 6 — Final verification
- **Do:** re-run the Step 2 set and compare with the baseline; unavailable tools = partial verification, said plainly.
- **Output:** each command + result; what wasn't run and why.
- **Decision:** new failure vs baseline → revert the causing step, re-run · otherwise → Step 7.

### Step 7 — Report
- **Do:** write the Output format below in the user's language, then the diff or code. Call out semantics the user might not expect that you **kept** (e.g. "sync throws from `run()` are still caught by `try`/`await`", "`||` kept: `0`/`''` fall back to defaults").
- **Output:** the final message.
- **Done when:** every "verified" matches a command you ran; every *propose* item is under Needs approval with its input; denied commands are listed.

### R-branch — read-only assessment (no step may mutate the checkout; see `references/assessment.md`)
- **R1 Scope:** name sampled files/revision and exclusions. Done when the sample is named; no repo-wide claim from a sample.
- **R2 Evidence:** Step 1 for the sample; inspect test commands/CI without modifying anything. Done when each area has callers/tests or "unknown".
- **R3 Proposals:** Step 3 with every item a proposal (priority, risk, rule, unsafe input). Nothing worth proposing → report already simple.
- **R4 Report:** assessment.md format with Scope and Verification lines stating nothing was edited. Done when every proposal has location, payoff, risk, evidence.

## Golden rules

Rules 1–2 outrank everything else in this skill, including the checklists in `references/`. Users ask for cleanup expecting to merge it without re-testing the world; a silent behavior change betrays that trust.

1. **Preserve behavior.** Keep outputs, side effects and their order, error types and messages, null/empty handling, laziness, resource lifetime, and complexity class. A change to any of these is a bug fix or redesign — propose it separately so the user can judge it on its own.
2. **Preserve public APIs.** Exported names, signatures, public fields, error text, wire/DB/CLI formats, and mutability contracts have callers you can't see. Callback→promise, sync→async, panic→`Result`, `null`→exception, parameter objects, and newtypes are API changes: propose, don't apply.
3. **Follow project conventions.** Read applicable `AGENTS.md` / `CLAUDE.md`, linter/formatter config, and neighbouring code; they beat generic advice here because consistency within a codebase matters more than any one style. Project lint/formatter rules also outrank this skill's stylistic preferences (including no nested ternaries): if de-nesting triggers max-depth or another lint rule, try a cohesive helper; otherwise retain the existing form — don't disable lint or rewrite its config. Let the formatter decide layout; hand-formatting creates diff noise that hides the real changes. Use only syntax the configured runtime/compiler supports; don't add dependencies or change config for cleanup.
4. **Prefer clarity over compression.** Avoid nested ternaries, dense one-liners, and chains that hide side effects; the next reader pays for every clever line. Keep helpful boundaries, intention-revealing names, and comments that explain *why*.
5. **Don't over-engineer.** Add abstractions only when they remove real duplication or complexity now; speculative ones are complexity you must maintain. Prefer deleting complexity to relocating it, and deep modules to many shallow helpers.
6. **Respect scope.** Touch the code the user named; if none, the code changed in this session or the working diff. Unrequested edits elsewhere inflate review cost and may collide with others' work, so list out-of-scope smells as suggestions instead.
7. **Report verification honestly.** Claim only checks you actually ran, with the command and result. If something wasn't run, say "not run" and why. A false "verified" leads the user to merge broken code — worse than admitting uncertainty.
8. **Denied means stop.** If a command, file deletion, or tool call is denied or blocked, don't achieve the same effect another way (e.g. `os.remove` after `rm` is denied). Leave it, and list it in the report so the user can decide.

## Output format

```
Summary: <what was simplified>; behavior/API unchanged | changes needing approval listed below.
Changes:
- <rule/category>: <what and why, one line each>
Not changed: <tempting edits skipped and why (API, semantics, scope)>
Needs approval: <proposed behavior/API changes with the input that would differ>   (omit if none)
Bugs found (not fixed): <file:line, suspected/confirmed, reproduction or reasoning; keep separate from simplifications>   (omit if none)
Scope: <mode, files/modules sampled, revision if known, excluded areas; no repository-wide claim from a sample>
Verification: <each command actually run + result>; <what was not run and why>; <edge inputs checked by reasoning>
```

Then show the diff or the rewritten code. For a no-change result, state why the code is already minimal and stop. Keep it short.

## Quick checklist

Apply freely to private/local code; at public boundaries only propose.

- **Delete:** unused code/imports/params (beware reflection, dynamic registration, exports), commented-out code, journal and "what" comments.
- **De-nest:** guard clauses, early `continue`, inverted conditions; aim for ≤2 levels.
- **Collapse redundancy:** `if c return true else false` → `return c` (when `c` is boolean); merge branches with identical bodies; drop single-use temporaries and pass-through wrappers that add no meaning; replace hand-written stdlib operations only when semantics match exactly (check `toMap`, `Object.keys`, `sort`, `Promise.all` in the traps file).
- **Deduplicate** knowledge that changes together; tolerate look-alike code that changes for different reasons.
- **Name** intent; replace magic values with named constants.
- **Conditionals:** extract complex predicates; avoid double negatives; use lookup tables or polymorphism for repeated type switches (unknown-key behavior must match).
- **Resources/errors:** `with`/`using`/`defer`/RAII/try-with-resources when cleanup order and exceptions stay equivalent; never swallow errors that were previously raised.
- **Equality:** `==` → `===` is not free in JS/TS: `new String('desc') == 'desc'` is true, `=== 'desc'` is false; `null == undefined`; `'1' == 1`. Keep loose equality (or prove the types) and say so.
- **Async/errors:** keep `try { await f() }` loops when `f` may throw synchronously — the sync throw is caught there; `items.map(f)` + `Promise.all` throws it outside the `try`. Note this in the report.
- **Structure:** split god functions/classes along real responsibilities; inline shallow helpers; keep deep modules.

## References

| File | Read when |
|---|---|
| `references/languages.md` → `languages-tier1.md` / `languages-tier2.md` | Always, for the one language being edited (section only). |
| `references/behavior-traps.md` | Steps 5–6, for every rewritten line. |
| `references/rules.md` | Planning non-trivial refactors; §20 for minimum-code decisions; §19 smell → refactoring map. |
| `references/examples.md` | Unsure whether a rewrite is safe; contains safe, propose-only, and reject/leave-alone examples plus report samples. |
| `references/sources.md` | User asks where a rule comes from. |
| `references/assessment.md` | Read-only simplification assessments, large-repository sampling, priority/risk ratings, lint conflicts, unavailable tools, and partial/platform verification. |
