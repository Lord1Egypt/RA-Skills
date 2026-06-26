---
name: skill-creator
description: Create, edit, improve, or audit AgentSkills. Use when creating a new skill from scratch, restructuring an existing skill, auditing skill quality, or making a skill easier for weaker AI models and agent runtimes to follow.
---

# Skill Creator

Use this skill to author or improve real AgentSkills.
Keep `SKILL.md` executable.
Move heavy explanation into `references/`.
Move repeated deterministic work into `scripts/`.

## Execution

### Definitions
- `<skill-dir>` = the directory that contains the target `SKILL.md`.
- `<output-dir>` = the parent directory where a new skill folder should be created.
- `<tool-scripts>` = the `scripts/` folder inside the `skill-creator` tool directory.
- `<review-artifact>` = the patched `SKILL.md` text or the short self-check written during Step 6, emitted in the current output channel for the environment.

### Step 0 — Choose the path
1. Classify the request using this table, then set the path.

| If the request contains | Then path is |
|-------------------------|--------------|
| `create a new skill`, `new skill called`, `build a skill named` | `new-skill` |
| `restructure`, `reorganize`, `split into references`, `major rewrite` | `major-rewrite` |
| `audit`, `review this skill`, `check skill quality` | `audit` |
| otherwise | continue to step 2 |

2. For edits to existing files, set the path to `small-local-edit` only if all are true:
   - only `SKILL.md` changes
   - no `scripts/`, `references/`, or `assets/` files are added or removed
   - the total change is 15 lines or fewer
   - no step order or branch condition changes
3. If all conditions in 0.2 are met, skip to Step 5. Otherwise continue to Step 1.
Stop when one path is chosen.

### Step 1 — Understand the real task
1. Collect the trigger phrases the user would actually say and write them into the task note.
2. Collect the main success path, add it to the task note, and output that section.
3. Collect the edge cases or failure modes that matter, add them to the task note, and output that section.
4. State the before/after behavior in one sentence, add it to the task note, and output that sentence.
5. Ask exactly one short question only if both are true, then output that question:
   - a required input is missing for the next safe step
   - that input cannot be reasonably defaulted
6. Otherwise continue and output the task note.
Output: a short task note containing triggers, success path, edge cases, and before/after behavior.
Stop when the task note exists.

### Step 2 — Design the skill structure
1. Decide what belongs in `SKILL.md`.
2. Decide what belongs in `scripts/`.
3. Decide what belongs in `references/`.
4. Decide what belongs in `assets/`.
5. Put each recurring item in exactly one home, record that mapping, and output the mapping.
6. If the same code would be rewritten repeatedly, move that code to `scripts/` and record the destination.
7. If the same explanation would be re-written repeatedly, move that explanation to `references/` and record the destination.
8. If the same output starter files would be recreated repeatedly, move those files to `assets/` and record the destination.
Output: a short bulleted list mapping each target file or folder to its single purpose.
Stop when every recurring item has exactly one home.

### Step 3 — Initialize or normalize the skill folder
1. For a new skill, run `python3 <tool-scripts>/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets] [--examples]` and create the starting skill folder.
2. For an existing skill, normalize the folder name, remove placeholder files, and remove stray docs that do not belong in a skill package, then output the normalized folder state.
3. Keep only files that directly help the skill do its job, then stop when the folder is normalized.
Output: a normalized skill folder.
Stop when the skill folder contains only the files the skill actually needs.

### Step 4 — Author or revise the skill
0. Locate the structure plan from Step 2 and use it as the authoring input, then continue authoring.
1. If the structure plan does not exist or is incomplete, stop and return to Step 2.
2. Write frontmatter with `name` and `description`.
3. In `description`, say what the skill does and when to use it.
4. Write the body in imperative form.
5. Put the fastest useful action near the top of the file, then output the reordered section.
6. Use one action per sentence in execution sections, then output the rewritten execution block.
7. Add explicit branch rules when the next step depends on conditions, then output the patched branch.
8. Add explicit outputs or stop conditions when order matters, then output the patched step.
9. Add navigation cues for extra material, then output the revised section list.
10. Create or update supporting files in `scripts/`, `references/`, and `assets/` when the plan requires them, then output the drafted files.
Read `references/authoring-guide.md` when you need authoring principles or folder-design rules. Purpose: guide structure.
Read `references/progressive-disclosure.md` when `SKILL.md` is getting long or supports multiple variants. Purpose: split content.
Read `references/workflows.md` when the task needs a reusable multi-step pattern. Purpose: choose workflow.
Read `references/output-patterns.md` when the skill must emit a specific artifact or report. Purpose: shape output.
Output: the drafted or revised skill files.
Stop when the skill files match the structure plan.

### Step 5 — Run the weak-model authoring pass
1. Check every execution block for one action per sentence and report any violation.
2. Check every execution block for explicit branch rules and patch missing ones.
3. Check every ordered step for an output, a stop condition, or both, then patch any missing case.
4. Replace ambiguous pronouns when the reference chain could break, then output the clarified wording.
5. Replace vague judgment calls with decision rules when possible, then output the revised rule.
6. Add `Read ... when ... Purpose: ...` navigation cues for any reference file that a weaker model must load deliberately.
7. If the draft still needs fallback behavior for ambiguous downstream skills, add or update that fallback behavior explicitly.
Read `references/weak-model-fallbacks.md` when the skill being authored contains `if appropriate`, `as needed`, `when necessary`, or any step whose outcome depends on model judgment without a clear decision rule. Purpose: replace ambiguity with explicit fallback instructions.
Output: the hardened draft plus a 3-line compliance note formatted exactly as:
- Checked: [2 fragile rules that are now explicit]
- Navigations: [new `Read ... when ... Purpose: ...` cues added, or `none`]
- Assumption: [one sentence or `None`]
Stop when the draft and the compliance note exist.

### Step 6 — Choose the review path
If all are true, skip deep review and write a 3-line self-check:
- Step 0 chose `small-local-edit`
- only `SKILL.md` was edited
- no step order or branch condition was added, removed, or changed
Otherwise run full `dual-thinking` review.
Runtime note: this path requires the `dual-thinking` skill to be installed and available in the user's environment.
1. If `dual-thinking` is unavailable, emit exactly: `REVIEW BLOCKED: dual-thinking skill not found. Run: clawhub install dual-thinking. If installation is not possible, ask the user whether to continue without deep review.` Then stop the skill execution.
2. If reviewing, use the real `SKILL.md` text.
3. If reviewing, surface the top remaining failure mode and patch it.
4. If the user declared a larger review round plan before Step 6 began, keep reviewing until that declared plan is complete unless validation blocks further honest review, then output the remaining round target.
5. Otherwise continue only while a concrete remaining failure mode still exists. Stop once the active consultant and you both agree that further improvement would only add churn, then output the review result.
6. If skipping, write exactly: what changed, what could break, and why deep review is safe to skip.
Output: `<review-artifact>`.
Stop when `<review-artifact>` exists.

### Step 7 — Validate
1. Run `python3 <tool-scripts>/quick_validate.py <skill-dir>`.
2. Run `python3 <tool-scripts>/validate_weak_models.py <skill-dir>`.
3. Fix every validation error, then re-run validation and output the new validator state.
4. Review warnings and either fix them or record why the warning is acceptable, then output that warning decision.
5. Re-run both validators after each fix cycle and output the latest results.
6. If either validator fails twice consecutively, output the raw error log, mark validation as blocked, and stop the entire skill execution. Do not proceed to Step 8. Do not loop indefinitely.
Output: validation results for both scripts.
Stop when both validators succeed, the remaining warnings are explicitly accepted, or the 2-cycle retry limit is hit.

### Step 8 — Package
1. Read `PACKAGING_CHECKLIST.md` when packaging or publishing is in scope. Purpose: verify release gate.
2. Run `python3 <tool-scripts>/package_skill.py <skill-dir>`.
3. Optionally pass an explicit output directory if the task needs one.
4. Confirm that the `.skill` archive was created.
5. Confirm that the package contents and hygiene checks required by `PACKAGING_CHECKLIST.md` are satisfied, then output that confirmation.
Output: a packaged `.skill` archive plus the checklist confirmation.
Stop when the package file exists and the checklist confirmation exists.

### Step 9 — Publish if needed
1. Publish only if the user asked for distribution; otherwise stop with a no-publish decision.
2. Publish only after validation, packaging, and the checklist confirmation from Step 8 succeed; otherwise stop before publishing.
3. Ensure `.clawhubignore` exists before publishing. If it is missing, create it with this baseline: `.clawhub/`, `__pycache__/`, `.git/`, `.env*`, `*.skill`, `temp/`, `node_modules/`, `coverage/`, `.diagnostics/`, `.sessions/`, `.profile/`, `.daemon-ws-endpoint`. If it already exists, update it to include any missing baseline line. Output the final file.
4. Determine the release metadata before publishing. Set the publish command inputs for `--slug`, `--name`, `--version`, and `--changelog`, then output those values.
5. Run `clawhub skill publish <skill-dir> --slug <slug> --name "<name>" --version <semver> --changelog "<1-sentence summary>"`, then output the exact command and the raw CLI result.
Output: a published release or a deliberate no-publish decision.
Stop when publication is complete or intentionally skipped.

### Step 10 — Iterate from real usage
1. Run this step only if the user explicitly provides post-deployment feedback, failure logs, or concrete runtime evidence; otherwise stop immediately.
2. Decide whether the fix belongs in `SKILL.md`, `scripts/`, `references/`, or `assets/`, then record that decision.
3. Apply the fix in the correct home, then output the changed artifact.
4. Repeat Steps 5 through 9 only for the user-supplied feedback in scope, then output the updated result.
Output: an improved next version of the skill.
Stop after applying the user-supplied feedback, or immediately if no feedback was provided.

## Quick checks
- Keep `SKILL.md` lean enough that navigation is cheap.
- Prefer `references/` for deep explanations, schemas, and long examples.
- Prefer `scripts/` for deterministic repeated operations.
- Prefer `assets/` for files used in the final output.
- Do not add decorative files like `README.md`, `INSTALLATION_GUIDE.md`, or `CHANGELOG.md` unless the real environment explicitly requires them.

## Completion standard
A skill is ready only when all are true:
- the trigger description is clear
- the structure matches the real task
- recurring code and references live in the right place
- the weak-model pass is complete
- the required review path is complete
- validation passes
- packaging succeeds

If any item above is false, the skill is still in draft.
