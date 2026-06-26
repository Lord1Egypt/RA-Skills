---
name: skill-test
description: Evaluate and QA a skill before release on ClawHub, skills.sh, and similar directories. Includes the bundled static evaluator `scripts/eval_skill.py` plus guidance for optional deterministic or LLM-assisted grading. Use when you need to test a skill, write evals, benchmark quality, catch regressions, audit trigger accuracy, compare versions, or decide whether a skill is ready to publish.
metadata: { "openclaw": { "emoji": "🧪", "requires": { "bins": ["python3"] } } }
---

# Skill Test

Test, evaluate, and grade agent skills across platforms. Catch regressions, verify triggers, score outputs, and track quality over time — without depending on any specific agent runtime.

## Quick Start

Choose one of these entry points:

1. `Trial Mode`: test a skill safely before trusting or adopting it.
2. `Publish Evaluation Mode`: evaluate a skill before submitting it to ClawHub or skills.sh.

Always start by reading the target `SKILL.md`, then run:

```sh
python3 {baseDir}/scripts/eval_skill.py <skill-path>
```

## Included Tooling

This package bundles one executable:

- `scripts/eval_skill.py` for static quality, structure, and release-readiness checks

Deterministic graders, runtime smoke tests, and LLM rubric grading are optional workflows you define around the target skill. They are not extra bundled executables inside this package.

## When to Use This Skill

Use this skill when you need evidence that a skill is ready to publish, ship, or compare against a previous version.

Typical use cases:

- Check whether a skill triggers for the right prompts
- Generate or refine an `eval.yaml` suite when regression testing is needed
- Review release blockers before publishing to ClawHub or skills.sh
- Compare two versions of a skill for regressions
- Turn vague quality concerns into a structured scorecard

## Trial Mode

Use Trial Mode when the question is: "Should I trust or adopt this skill at all?"

Trial Mode should focus on:

- Safe first-pass inspection of `SKILL.md`, scripts, and references
- Boundary review: what the skill can and cannot do
- Obvious side effects, credentials, or risky commands
- Whether the skill is coherent enough to justify deeper testing

## Publish Evaluation Mode

Use Publish Evaluation Mode when the question is: "Is this skill ready to publish or update?"

Publish Evaluation Mode should focus on:

- Trigger quality and first-screen clarity
- Structural integrity and portable commands
- Release blockers in documentation or workflow
- Regression checks against a previous version when available

## When Not to Use This Skill

Do not use this skill when the task is primarily listing optimization rather than quality validation.

Use a different workflow when you need to:

- Improve search visibility, naming, slug choice, or listing copy
- Perform a general code review unrelated to skill behavior
- Design a new skill from scratch without evaluating an existing one
- Debug a specific runtime failure in an underlying product or API

## When the Evaluation Is Inconclusive

If the static report cannot prove readiness, say what is still unverified and what test evidence is missing.

Common next steps:

- Add or tighten `eval.yaml` with deterministic checks
- Run comparative evaluation against a known-good baseline
- Add stronger negative trigger tests for boundary cases
- Escalate to manual runtime testing when the skill depends on external systems

## Isolation Principle

Treat third-party or unfamiliar skills as untrusted until reviewed.

When testing a skill:

- Do not load the target skill into the main working context unless necessary
- Prefer disposable sessions, sub-agents, or isolated workspaces for risky skills
- Inspect scripts and references before running commands with side effects
- Be explicit about what was statically inspected versus what was actually executed

## Assistant Responsibilities

When using this skill, the assistant should:

- Read the target skill's `SKILL.md`, scripts, and references before judging quality
- Run the static evaluator first to establish a baseline
- Separate proven failures from unverified concerns
- Recommend the smallest next test that would most reduce uncertainty
- Preserve the target skill's capability boundary while improving testability
- Use isolated evaluation where side effects, credentials, or shell commands make blind execution risky

## Recommended Output Structure

Organize the final evaluation report like this:

1. Overall score and release-readiness summary
2. Highest-severity findings first
3. Per-dimension scores with brief explanations
4. What is verified versus what is still unverified
5. Next actions in priority order

## Notes and Constraints

Keep these limits explicit when reporting results:

- Static analysis is not proof of runtime correctness
- Baseline platform compatibility may be partial or inferred
- The only bundled executable is `scripts/eval_skill.py`; deeper deterministic or LLM grading needs additional user-defined setup
- LLM rubric grading is optional, requires an external model provider, and should be labeled as qualitative
- Regression claims should cite a baseline, not intuition
- If a skill depends on external systems, publish-readiness may still require manual verification
- `eval.yaml` is an optional quality asset, not a universal release requirement
- UI metadata such as `agents/openai.yaml` is optional and should not be treated as a baseline quality gate

## Edge Cases

Call out these cases explicitly when they appear:

- The skill requires credentials or paid APIs
- The skill contains many auxiliary files beyond `SKILL.md`
- The skill shells out to destructive or stateful commands
- The baseline version is missing or not comparable
- Static checks pass, but runtime proof is still absent

## Prerequisites

- Python 3.10+ available as `python3`.
- The target skill must have a `SKILL.md` with valid YAML frontmatter.
- No API key is required for the bundled static evaluator.
- If you choose to run external LLM rubric grading outside this package, configure the provider credentials required by your own grading environment.

## Example Prompts

- `Is this skill ready to publish on skills.sh, or does it still have quality gaps?`
- `Audit this skill before I submit it to ClawHub and show me the release blockers.`
- `Evaluate this skill and tell me if it would trigger correctly for common user prompts.`
- `Write a test suite for my skill that covers trigger, output, and style checks.`
- `Run the skill-test grader against this skill folder and show me the report.`
- `Compare the current version of this skill against the previous version and flag regressions.`
- `Audit this skill's trigger description — does it fire when it should and stay silent when it shouldn't?`
- `Benchmark this skill: run 10 trials and give me pass rates with confidence intervals.`
- `Find trigger gaps, output issues, and release blockers in this skill before publication.`

## Workflow

1. Identify the target skill folder. Read its `SKILL.md` to understand intent and structure.
2. Run the bundled static analyzer to get a baseline quality report:

   ```sh
   python3 {baseDir}/scripts/eval_skill.py <skill-path>
   ```

3. Read [references/eval-methodology.md](references/eval-methodology.md) for the full evaluation framework.
4. Read [references/grader-patterns.md](references/grader-patterns.md) for grader implementation guidance.
5. Read [references/sandbox-testing.md](references/sandbox-testing.md) when the target skill is third-party, risky, or side-effectful.
6. Read [references/comparison-workflow.md](references/comparison-workflow.md) when comparing two versions of a skill.
7. Read [references/publish-evaluation.md](references/publish-evaluation.md) when preparing a skill for ClawHub or skills.sh release.
8. Based on the skill type, apply the appropriate evaluation strategy:
   - **Trigger evaluation**: test whether the skill activates for the right prompts and stays silent for wrong ones.
   - **Deterministic grading**: check concrete outcomes (files created, commands run, structure correct) using target-skill-specific checks you define.
   - **LLM rubric grading**: score qualitative aspects (style compliance, workflow fidelity, convention adherence) only if you intentionally add an external grading environment.
   - **Regression tracking**: compare scores across versions or model updates.
9. Generate or refine an `eval.yaml` test suite for the target skill when repeatable regression testing is needed.
10. Present results as a structured report with scores, findings, and actionable fixes.

## Evaluation Dimensions

The evaluator scores skills across five dimensions:

Dimension | What it measures | Weight
--- | --- | ---
Trigger accuracy | Does the skill fire for correct prompts and stay silent for incorrect ones? | 25%
Structural integrity | Are referenced files, links, and paths valid and portable? | 20%
Content quality | Does SKILL.md document workflow, prerequisites, commands, and completion criteria? | 25%
Baseline platform compatibility | Does the skill meet the minimum structural expectations for OpenClaw-style packaging, with other platforms treated as coarse compatibility checks? | 15%
Testability | Can automated graders verify the skill's outcomes and boundaries? | 15%

## Output Requirements

Produce a structured report containing:

- Overall score (0–100) and per-dimension scores
- Trigger test results: which prompts fired correctly, which misfired or missed
- Deterministic check results: pass/fail for each concrete assertion
- LLM rubric results: per-criterion scores with notes
- Regression flags: any dimension that dropped compared to baseline
- Prioritized action list with `critical`, `high`, `medium`, `low` severity

## Writing Eval Suites

When the user asks you to create tests for a skill, generate an `eval.yaml` in the target skill folder:

```yaml
version: "1"
defaults:
  trials: 5
  timeout: 300
  threshold: 0.8

trigger_tests:
  - id: explicit-invoke
    should_trigger: true
    prompt: "Use the $<skill-name> skill to do X"
  - id: implicit-invoke
    should_trigger: true
    prompt: "Do X with Y for quick Z experiments"
  - id: negative-control
    should_trigger: false
    prompt: "Add Y to my existing X project"

outcome_tests:
  - id: file-structure
    type: deterministic
    checks:
      - file_exists: "package.json"
      - file_exists: "src/index.ts"
      - command_ran: "npm install"
  - id: style-compliance
    type: llm_rubric
    rubric: |
      Structure (0-0.5): Does the output match the declared project layout?
      Conventions (0-0.5): Are naming, formatting, and tooling choices consistent?
```

## Static Analysis Checks

The built-in analyzer verifies without running the skill:

- Frontmatter completeness: `name`, `description`, trigger phrasing, length
- Structural integrity: referenced files exist, commands use `{baseDir}`, no dead links
- Definition of done: a measurable completion criteria section exists
- Example coverage: at least 3 realistic user-facing example prompts
- Boundary clarity: the skill states what it does NOT do
- Baseline platform compatibility: `SKILL.md` validity first, with other platform hints checked only when relevant

## Commands

```sh
# Full evaluation report (text)
python3 {baseDir}/scripts/eval_skill.py /path/to/skill

# JSON output for automation
python3 {baseDir}/scripts/eval_skill.py /path/to/skill --json

# Evaluate with explicit quality keywords
python3 {baseDir}/scripts/eval_skill.py /path/to/skill --keywords "backup,restore,disaster recovery"

# Generate eval.yaml scaffold for a skill
python3 {baseDir}/scripts/eval_skill.py /path/to/skill --scaffold

# Compare two versions of a skill
python3 {baseDir}/scripts/eval_skill.py /path/to/skill-v2 --baseline /path/to/skill-v1
```

## Definition of Done

- The static analyzer has run and produced a baseline report.
- All `critical` and `high` findings have been addressed or explicitly justified.
- Trigger tests cover at least 1 explicit, 1 implicit, and 1 negative prompt.
- Platform readiness shows green for the target platforms.
- If comparing versions, no regression flags remain unexplained.
- The final report has been presented to the user with scores and actionable next steps.

## When Editing a Skill Based on Eval Results

- Fix `critical` and `high` issues first.
- Preserve the existing capability surface unless the user asks to expand it.
- After each fix, re-run the evaluator to confirm improvement and catch new regressions.
- Do not chase a perfect score at the cost of readability or actual utility.

## Resources

- Full evaluation methodology: [references/eval-methodology.md](references/eval-methodology.md)
- Grader patterns and implementation: [references/grader-patterns.md](references/grader-patterns.md)
- Safe testing for third-party skills: [references/sandbox-testing.md](references/sandbox-testing.md)
- Version-to-version comparison workflow: [references/comparison-workflow.md](references/comparison-workflow.md)
- Publish-time evaluation workflow: [references/publish-evaluation.md](references/publish-evaluation.md)
