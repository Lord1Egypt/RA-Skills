# Compact SOP Style

Authoring guide for compressing spex skill markdown (`SKILL.md`,
`commands/*.md`) into terse, execution-oriented SOPs.

Use when rewriting or reviewing those files. Do **not** use this to
rewrite existing `references/*.md` content (e.g. `apply-review-loop.md`,
`SKILLS-SPEC.md`) unless a separate change explicitly says so.

Compliance baseline: `references/SKILLS-SPEC.md` (front-matter,
progressive disclosure, imperative form). This guide adds compression
rules; it does not relax SKILLS-SPEC.

## Goals

- Cut verbosity / context size.
- Keep **exact** execution semantics: triggers, inputs, preconditions,
  step order, branches, CMDs, side effects, validation, failure
  handling, safety.
- Machine-friendly + human-scannable.

## Allowed Shorthand

| Token | Meaning |
|-------|---------|
| `->` | then / next / leads to |
| `=>` | produces / returns / results in |
| `IF` / `ELSE` / `END` | branch |
| `REQ` | required |
| `OPT` | optional |
| `OK` | success |
| `FAIL` | failure |
| `CHECK` | validation |
| `CMD` | command / tool invocation |
| `ON_FAIL` | failure handling |
| `TIMEOUT` | timeout behavior |
| `ROLLBACK` | rollback / recovery |

Style rules:

- Terse, note-like; fragments OK if unambiguous.
- Prefer arrows, keywords, short lines.
- One action or decision per line.
- Start lines with verbs or keywords when possible.
- Drop background, motivation, examples, filler unless required for
  correct execution.
- Prefer imperative / infinitive (SKILLS-SPEC), not second person.

## Must Preserve

1. Skill / command trigger conditions.
2. REQ and OPT inputs.
3. Preconditions and permissions.
4. Exact step order.
5. Branching logic.
6. Tool names, commands, parameters, env vars, file paths.
7. Side effects (writes, network, state, external actions).
8. Success criteria and validation checks.
9. Failure handling, retries, timeouts, rollback.
10. Safety, security, compliance constraints.
11. YAML front-matter fields and values (`name`, `description`,
    `version`, `disable-model-invocation`, `arguments`, …).
12. Supported Commands table rows (command / aliases / meaning).
13. Command Routing table rows (match → `commands/<file>.md` path).
14. Phase titles and numbers (`### Phase N: ...`).
15. Explicit shared loads:
    `Load and follow references/<file>.md exactly`.

## Do Not

- Remove steps that affect behavior.
- Merge dependent steps unless explicitly safe.
- Infer missing behavior.
- Add new capabilities.
- Change tool names, command syntax, or parameter meaning.
- Weaken validation or safety checks.
- Compress or delete YAML front-matter fields/values.
- Delete or rewrite routing table aliases / paths.
- Inline-expand or drop `Load and follow references/...` pointers.
- Turn executable logic into vague prose.
- Delete steps only to shrink line counts.
- Append trailers or HTML comments to skill/command files.

## File-Type Skeletons

### Router — `SKILL.md`

```markdown
---
# YAML front-matter: keep field names + values unchanged
---

# Spex — Spec-Driven Development

## Usage
- IF no args -> show Supported Commands table -> STOP
- IF recognized command -> load commands/<file>.md -> follow SOP
- IF free-form -> infer intent (see below)

## Supported Commands
| Command | Aliases | Description |
| ... unchanged rows ... |

## Command Routing
| Match | Command file |
| ... unchanged rows ... |

### Routing Discipline
- Role: router, not assistant
- NEVER act on user prompt directly
- NEVER skip / shortcut command SOP
- ALWAYS load full command markdown; follow every Phase

### Free-form Intent Inference
| Heuristic | Suggest |
| ... unchanged mapping ... |
- IF confidence >= 90% -> route with `$prompt`
- ELSE IF ambiguous -> ask user to confirm
- ELSE too vague -> show Supported Commands -> STOP
```

Rules:

- Front-matter: byte-stable preferred; whitespace-only normalize OK;
  never change field values or semantics.
- Keep both tables complete (no dropped rows / renamed paths / changed
  aliases). Surrounding prose may tighten.
- Body: terse Usage branches, Routing Discipline, Intent Inference.

### Command SOP — `commands/*.md`

````markdown
# spex <cmd>

## Usage

    /spex <cmd> [args]

## Inputs

- REQ: ...
- OPT: ...

## Preconditions

- REQ: ...
- permissions / env if any

## Execution

### Phase 1: Name

- CMD: `$spex_skill_dir/scripts/spex ...`
- IF ... -> ...
- ELSE -> ...
- CHECK ... -> OK / FAIL
- ON_FAIL: ...

### Phase N: Name

- ...

## Failure Handling

- ON_FAIL: ...
- TIMEOUT: ... (if any)
- ROLLBACK: ... (if any)

## STOP / Outputs

- returns / writes / side effects
- hard STOP rules (e.g. PLAN only, one-step only)
````

Rules:

- Keep Phase titles + numbers (docs/agents cite them).
- Prefer `CMD:` lines + fenced bash blocks with **identical** CLI
  syntax, flags, heredocs, variable names (`$spex_skill_dir`,
  `$spec_name`, `$commit_sha`, …).
- Shared orchestration stays external:
  `Load and follow references/<file>.md exactly` — do not paste the
  referenced file into the command.

### High-risk zones (never “optimize away”)

- apply / apply-one-step: resume gate, Phase 5 persist `commit_title`
  before `completed_at`, Phase 6 review-loop load, abnormal STOP vs
  round-3 major fix-in-loop.
- create: PLAN-only scope, Phase 9 hard STOP (no app code).
- merge / archive: side-effect boundaries.
- SKILLS-SPEC: third-person `description` triggers; verb-first body;
  referenced files must exist.

## Measurement

Before / after each batch:

1. Record line count and word count for each touched file
   (e.g. `wc -l` / `wc -w`).
2. Confirm reduction comes from removing redundancy, **not** from
   dropping behavioral steps.
3. Semantic diff vs previous version: every CMD, branch, path, Phase
   gate, ON_FAIL still present and equivalent.
4. Run `make check` (Python/version/root-markdown gate). Separately
   lint rewrite targets only (exclude `templates/`):

   ```bash
   npx markdownlint-cli2 \
     "skills/spex/SKILL.md" \
     "skills/spex/commands/*.md" \
     "skills/spex/references/*.md"
   ```

   `make check` does **not** cover these paths. Proceed only when both
   OK.

Target: scannable one-action lines; never trade correctness for size.

## Rewrite Order (spex batch)

1. Land this file (`compact-sop-style.md`).
2. Rewrite `SKILL.md` (router).
3. Short commands: `init.md` -> `archive.md` -> `merge.md`.
4. Medium: `create.md` -> `modify.md`.
5. Long: `apply.md` -> `apply-one-step.md` (keep Phase 6 load of
   `apply-review-loop.md` + STOP semantics aligned).

Out of scope for the compact-skill-markdown effort unless separately
specified: existing reference rewrites, templates, auto-compressor
tools, Python behavior changes.
