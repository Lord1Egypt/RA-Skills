# SkillForge — Agent Skill Audit & Optimization

A quality bench for skill authors: it splits a SKILL.md into six checkable dimensions and returns a weighted scorecard, itemized fixes, and a drop-in rewrite. On a whole library it returns a repair queue ranked by impact.

## What This Is

- Solves one problem: skills that look correct but never trigger, stall mid-workflow, cannot be verified, bloat the context window, or leak absolute paths and secrets.
- Produces three artifacts: a human-readable report (`<slug>.audit.md`), a machine-readable scorecard (`<slug>.audit.json`), and a rewrite either as a full replacement or as a per-hunk diff.
- Different from asking a general model: every score is anchored to a fixed rubric, so two audits of the same file should land within 5 points of each other. Ad-hoc chat reviews drift, cannot be compared across a team, and cannot be re-run as a regression.
- Scope: a single SKILL.md, a skill directory with `references/` and `scripts/`, or an entire skill library.
- Ships one deterministic tool: `scripts/skill_audit.py` counts what can be counted (lines, sections, frontmatter fields, filler phrases, risks) using the standard library only.

## When to Use

- I am about to publish a paid skill and need to know whether it is ready and where buyers will complain.
- My skill works sometimes and fails other times; I need to know whether the trigger or the workflow is at fault.
- I suspect the skill eats the context window and want its size quantified before deciding whether to split it.
- I want to turn a working personal skill into something a team can reuse.
- I have dozens of skills and no idea which to fix first; I need a repair queue ranked by impact.
- I need acceptance criteria so the agent can self-check after every run.
- I want a pre-delivery sweep for absolute paths, secrets, and internal addresses.
- I want to compare two competing skills for the same job and keep one.

## When NOT to Use

- Only a description, no original SKILL.md: findings would be unreliable.
- Requests to guarantee approval: structure and executability only.
- Undocumented internal APIs or private protocols: clarity only, no verification.
- Wording-only edits: the rubric will expose structural problems you are unwilling to fix.

## Quick Reference

| Situation | Use |
|---|---|
| Score a skill | `references/audit-rubric.md` + `scripts/skill_audit.py` |
| Known issue, unclear fix | `references/rewrite-patterns.md` |
| Worried the rewrite is too long | `references/token-budget.md` |
| Audit a batch | `references/batch-audit.md` |

## Inputs and Outputs

| Field | Required | Description |
| --- | --- | --- |
| `skill_path` | yes | Path to a single SKILL.md or to a skill directory; the library root when auditing in batch |
| `mode` | no | `single` (default) for one skill; `batch` to walk a library and emit a repair queue |
| `profile` | no | `house` (default, validates the full frontmatter field set) or `generic` (validates `name` and `description` only) |
| `rewrite` | no | `full` (default, whole replacement) / `patch` (per-hunk diff only) / `none` (score only) |
| `target_readers` | no | Who the skill serves: the author's own agent, paying buyers, or a team. Sets how strict boundaries and acceptance must be |
| `fail_under` | no | Exit code `1` when the total score falls below this value |

Three artifacts are mandatory; missing any one means the job is not delivered:

- `<slug>.audit.md`: the report with scorecard, issue list (each with a location), rewrite or diff, and acceptance checklist. 800-1,500 words.
- `<slug>.audit.json`: the machine-readable scorecard. Every number in the report must appear here under the same name.
- `audit-queue.md`: batch mode only. Repair queue with priority, skill, total score, top issue, and repair cost.

## Workflow


### 1. Read and parse

- **Do**: run `python scripts/skill_audit.py <skill_dir>` for the countable metrics, then read the body for frontmatter fields, heading tree, size (lines and characters), code blocks, list items, and any dependency the text claims.
- **Pass if**: you can answer four questions. Does a parseable frontmatter exist? Which baseline sections are missing (`house` expects ten, `generic` expects a positioning, workflow, acceptance, and boundary block)? Which size band does the file fall into? Do the `references/` and `scripts/` files the text cites actually exist?
- **If it fails**: never guess a missing or broken frontmatter; log it as P0 and ask the author. For non-UTF-8 input, transcode first; if transcoding fails, audit size and keywords only and stamp the report "structure score unavailable".

### 2. Score six dimensions

- **Do**: score each dimension 0-5 as an integer against `references/audit-rubric.md`, record the evidence location, then apply the weights.
- **Pass if**: every point maps to one place in the source (line or heading). A score you cannot evidence must drop to 3 or below.
- **If it fails**: when two passages contradict each other (the body says required, the table says optional), score the weaker side and file a separate consistency defect.

### 3. Locate the defects

- **Do**: turn each deduction into one issue with a fixed shape: location (section, line, or quoted sentence), consequence (which failure it causes), fix (an executable action).
- **Pass if**: one issue belongs to exactly one dimension, and its consequence matches an observable failure (no trigger, stalls halfway, unverifiable, over budget, information leak).
- **If it fails**: if all you can write is "unclear", you have not located the sentence. Find the phrase or drop the issue; never pad the list.

### 4. Rewrite

- **Do**: apply `references/rewrite-patterns.md` to every P0 and P1 issue. `rewrite=full` emits a whole replacement; `rewrite=patch` emits per-hunk diffs.
- **Pass if**: the replacement has the same level-2 heading count as the original, adds no fact, dependency, or link that the original did not contain, and raises the re-run score.
- **If it fails**: when the rewrite would break the size ceiling, move detail into `references/` first. When meaning cannot survive the rewrite, keep it as advice and downgrade the item to P2.

### 5. Emit scorecard and diff

- **Do**: write `<slug>.audit.md` and `<slug>.audit.json` with identical totals. Diffs go in a `diff` block where `-` is the original line and `+` is the replacement.
- **Pass if**: every number in the report resolves to a field in the JSON, and large rewrites carry at most three bullet points of change summary.
- **If it fails**: when the report and the JSON disagree, the script wins. Re-run it, explain the delta in a footnote, and never hand-edit a number.

### 6. Batch audit and prioritize

- **Do**: run `python scripts/skill_audit.py --scan <root>` for a first pass, compute priorities with the formula in `references/batch-audit.md`, manually spot-check at least 20 percent, then write `audit-queue.md`.
- **Pass if**: every priority in the queue reproduces from the formula, and at least three spot-checked items can be traced to a real sentence.
- **If it fails**: above 60 skills, split into two passes (triage P0/P1 first, deep-audit the survivors). If a scan is interrupted, resume per directory and never rescan a finished one.

## Output Format

```
Scorecard: six dimensions x 0/3/5 + total + band
Issue list: location | evidence | impact | fix
Rewrite: full replacement (default) or diff (patch mode)
Acceptance checklist: tickable items after rewrite
```

## Quality Gate

- [ ] Each of the six dimensions carries one integer score from 0 to 5 plus an evidence location
- [ ] The scorecard has 6 dimension rows and 1 total row; the weight column sums to 100
- [ ] Total equals the sum of (dimension score / 5 x weight), reproducing with zero error
- [ ] Every issue has location, consequence, and fix; a missing part fails the gate
- [ ] Every consequence maps to an observable failure (no trigger, stall, unverifiable, over budget, leak)
- [ ] The rewrite has the same level-2 heading count as the original
- [ ] The rewrite introduces no fact, dependency, or link absent from the original
- [ ] The report contains no absolute paths, secrets, internal addresses, or real personal data
- [ ] The script's JSON and the report agree number for number
- [ ] The report body is 800-1,500 words and the issue list holds at most 15 entries
- [ ] Three randomly sampled issues can be located in the source text
- [ ] In batch mode, every queue priority reproduces from the formula

## Boundaries

- No runtime proof. The audit is static: it can show that the text is executable in principle, not that the skill succeeds on a live tool chain. Run one end-to-end pass when that guarantee matters.
- No business or pricing judgement. It scores structure, executability, size, and risk, not whether the skill deserves to be sold.
- No edits to your files. It emits a rewrite and a diff; writing them down needs your confirmation.
- No cross-language polish. The English version aligns structure and compliance only; it is not a literary rewrite.
- Unparseable input (broken frontmatter, binary attachments, encrypted files) is marked `unparsed`, that segment is skipped, and nothing is inferred.
- For undocumented third-party APIs or private protocols, it scores only what the text evidences and does not extrapolate feasibility.

## Common Traps

- **Static checks sold as runtime validation**: run the critical path at least once.
- **Wording changes without workflow changes**: each edit must map to an executable action.
- **Thin trigger coverage**: cover synonyms and colloquial phrasing.
- **No regression after rewrite**: run the acceptance checklist every time.

## Example Delivery

Input:

```
skill_path = skills/report-writer/SKILL.md
profile = house        rewrite = full
```

Output skeleton (values illustrative; real numbers come from the audit):

````markdown
# report-writer audit

## Scorecard

| Dimension | Weight | Score | Weighted |
| --- | --- | --- | --- |
| Trigger accuracy | 20 | 2 | 8.0 |
| Boundary clarity | 15 | 3 | 9.0 |
| Workflow executability | 25 | 2 | 10.0 |
| Acceptance testability | 20 | 2 | 8.0 |
| Token economy | 10 | 3 | 6.0 |
| Safety and compliance | 10 | 5 | 10.0 |
| **Total** | 100 | - | **51.0 (grade C)** |

## Issues

1. [P0] Triggers reduce to "write a report", with no controlled vocabulary and no counter-triggers (location: frontmatter `trigger_keywords`).
   Consequence: it competes with every general writing skill, so hit rate is unpredictable.
   Fix: replace with 8-12 controlled triggers plus three "do not trigger when" clauses.
2. [P1] Workflow step 3 says only "generate the report", with no criterion and no failure branch (location: workflow step 3).
   Consequence: missing data gets invented and the deliverable cannot be verified.
   Fix: see the diff below.

## Rewrite (excerpt)

```diff
- 3. Generate the report
+ 3. Generate the report skeleton in four parts: context, data, conclusion, recommendation. Hard cap 800 words.
+    Criterion: all four parts present, each backed by at least one checkable source.
+    If it fails: mark a part "pending" and never fill in numbers.
```

## Acceptance Checklist

- [ ] Re-run the script; total rises from 51.0 to at least 75.0
- [ ] Triggers map one-to-one onto the five scenarios
````

## Related Skills

- **Skill Audit Manager (free)**: single-skill six-dimension check-up first.
- **PolicyForge (paid)**: calibrate content standards when auditing policy skills.

## Reference Files

- `references/audit-rubric.md`: the six-dimension rubric, 0/3/5 anchors, and common misjudgements. Read it before scoring.
- `references/rewrite-patterns.md`: ten recurring defects with sourced sentence and rewrite pattern.
- `references/token-budget.md`: character-to-token estimation, size bands, and the split decision rule.
- `references/batch-audit.md`: batch procedure, priority formula, repair queue, and report template.
- `scripts/skill_audit.py`: deterministic metric collection and first-pass scoring, JSON output, standard library only.
