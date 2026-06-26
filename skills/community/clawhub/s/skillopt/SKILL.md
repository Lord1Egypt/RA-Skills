---
name: skillopt
description: Train, evaluate, and improve Agent skill files as reusable external capabilities. Use when a user wants to optimize SKILL.md, prompt procedures, OpenClaw/Hermes/Codex/Claude Code skills, agent workflows, skill factories, benchmark-driven skill iteration, rollout analysis, validation gates, best_skill.md export, or controlled self-evolving skills inspired by Microsoft SkillOpt.
---

# SkillOpt

## Operating Idea

Treat a skill document as trainable external state. Keep the target model, tools, and runtime fixed; optimize only the skill text through measured task rollouts, failure reflection, small edits, validation gating, and versioned export.

Default output is a deployable `best_skill.md` plus a short optimization report. Training may use many traces and candidate files; deployment should require only the final skill file.

## Invariants

- Preserve the original skill before editing.
- Separate train and validation tasks. Never accept an edit based only on the examples used to propose it.
- Prefer small, reviewable edits over full rewrites. Keep the skill's public contract stable unless the task suite proves the contract is wrong.
- Score behavior, not eloquence. A prettier skill that does not improve validation is rejected.
- Record rejected edits and the reason, then consult that buffer before proposing another edit.
- Do not add model-specific hacks unless the target deployment is explicitly model-specific.
- Do not leak validation answers into the skill. Validation data may guide accept/reject decisions, not become memorized instructions.

## Run Directory

Create a run directory near the skill being optimized unless the user specifies another path:

```text
skillopt_runs/<target-skill-slug>/
  source_skill.md
  candidates/
    candidate_000.md
    candidate_001.md
  tasks/
    train.jsonl
    val.jsonl
  rollouts/
    train/
    val/
  rejected_edits.md
  best_skill.md
  report.md
```

Use `scripts/skillopt.py` for deterministic run setup, JSONL validation, simple command-backed rollouts, score aggregation, validation gates, and report generation. Read `references/evaluation.md` when defining task schemas or scorers.

## Workflow

### 1. Define the Optimization Contract

Identify:

- target skill path and deployment agents
- target model/runtime/tool constraints to keep fixed during evaluation
- success metric and acceptance threshold
- task distribution the skill should serve
- allowed edit budget, such as max 3 sections or max 25% changed lines per round

If no task suite exists, create a small proxy suite first, label it as proxy data, and tell the user that real production traces are needed for stronger conclusions.

### 2. Build Train and Validation Sets

Represent each task as JSONL with an id, prompt, optional inputs, and a scorer. Keep validation examples independent and representative.

Minimum split:

- `train.jsonl`: failure discovery and edit proposal
- `val.jsonl`: accept/reject gate

For fragile or high-stakes skills, add a hidden or holdout split outside the optimization loop and use it only for final reporting.

### 3. Run Baseline Rollouts

Evaluate the unmodified skill on train and validation tasks using the same target agent that will later deploy it.

Examples:

```bash
python3 scripts/skillopt.py init --skill path/to/SKILL.md --out skillopt_runs/my-skill
python3 scripts/skillopt.py validate-tasks skillopt_runs/my-skill/tasks/train.jsonl
python3 scripts/skillopt.py run --tasks skillopt_runs/my-skill/tasks/val.jsonl --skill skillopt_runs/my-skill/source_skill.md --out skillopt_runs/my-skill/rollouts/val_baseline --agent-command "hermes -s {skill_path} -z {prompt}"
```

For OpenClaw or any other agent, replace `--agent-command` with a command template that accepts `{skill_path}`, `{prompt}`, `{task_id}`, and optionally `{output_path}`.

### 4. Reflect on Traces

Analyze successful and failed rollouts separately.

For each failure, classify the root cause:

- missing procedure
- wrong tool order
- weak verification
- ambiguous output contract
- missing edge case
- over-broad instruction
- environment assumption
- scoring mismatch

Extract patterns across failures before editing. Do not chase one-off errors unless they reveal a generalizable instruction.

### 5. Propose a Controlled Edit

Generate one candidate skill with a concise edit rationale:

- add: missing guardrail, checklist, or workflow step
- delete: harmful or distracting instruction
- replace: ambiguous wording with operational criteria
- reorder: move high-leverage instructions earlier

Keep the candidate deployable as a normal skill. Avoid embedding run logs, benchmark answers, private traces, or optimizer notes in the final skill text.

### 6. Gate on Validation

Run the same validation set on the candidate. Accept only when the candidate beats the baseline by the configured threshold and does not introduce unacceptable regressions.

Default acceptance:

- validation average improves by at least `0.02`
- no critical task regresses from pass to fail
- skill remains shorter or only grows for a clear procedural reason
- output format and trigger metadata remain valid

If rejected, append a short note to `rejected_edits.md`:

```text
## candidate_003
Rejected because validation avg +0.00 and task val_docx_04 regressed.
Avoid adding broad "always rewrite" instructions; they caused format drift.
```

### 7. Iterate

Repeat rollout, reflection, candidate edit, and validation gate until:

- validation score plateaus for 2 rounds
- edit budget is exhausted
- regressions become persistent
- the skill is good enough for the user's target use

Track the best candidate, not merely the latest candidate.

### 8. Export

Copy the best accepted candidate to `best_skill.md`. If the user wants installation, replace or install the deployed skill only after showing the report summary.

The final report should include:

- baseline train/validation scores
- best candidate train/validation scores
- accepted edits
- rejected edit patterns
- known overfitting risks
- deployment instructions for OpenClaw, Hermes, or the current agent

## Cross-Agent Notes

- For Codex-style skills, keep required YAML frontmatter to `name` and `description`.
- For Hermes, prefer standard `SKILL.md` folders and invoke with `hermes -s <skill-or-path>` when testing locally.
- For OpenClaw, keep the same folder portable and install from the local directory when needed.
- For unknown agents, use the skill as plain Markdown instructions plus any bundled scripts. The only required contract is: load the candidate skill, run the task prompt, capture output, score it, and compare against the baseline.

## Quality Bar

A good SkillOpt run feels like engineering, not vibes:

- claims are backed by recorded rollouts
- edits are small enough to review
- validation decides acceptance
- rejected edits teach the next round
- final deployment is one clean skill file
