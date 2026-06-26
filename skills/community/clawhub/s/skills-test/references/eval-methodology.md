# Evaluation Methodology

Use this reference when designing or running skill evaluations.

## Core Principle

Move from "it feels better" to "proof": run the skill, record what happened, grade it with a small set of checks. Every tweak becomes easier to confirm, and every regression becomes clear.

## Skill Categories and Testing Focus

### Capability Uplift Skills

Help the model do something it cannot do consistently on its own. Examples: document generation, code migration, specialized analysis.

Testing focus:
- Does the skill improve output quality compared to the base model alone?
- As models improve, does the skill remain necessary?
- Run periodic A/B comparisons: skill-loaded vs skill-absent.

### Encoded Preference Skills

Sequence steps according to a team's workflow. The model can do each piece but the skill enforces order and conventions. Examples: NDA review, weekly updates, release checklists.

Testing focus:
- Does the skill faithfully reproduce the intended workflow?
- Are all required steps executed in the correct order?
- Do outputs follow the team's conventions, not just generic best practices?

## Five Evaluation Dimensions

The dimensions below describe the full evaluation methodology, including checks that require actually running the skill. The built-in static analyzer (`eval_skill.py`) covers a subset: trigger accuracy, structural integrity, content quality, baseline platform compatibility, and testability. The runtime dimensions (outcome correctness, process fidelity, style compliance, efficiency) apply when you run the skill end-to-end with deterministic graders or LLM rubrics.

### 1. Trigger Accuracy (25%)

Test whether the skill activates at the right time.

Prompt categories:
- **Explicit invocation**: names the skill directly. Must always trigger.
- **Implicit invocation**: describes the task without naming the skill. Tests `name` and `description` quality.
- **Contextual invocation**: adds domain noise but still needs the skill. Tests robustness.
- **Negative control**: adjacent but different tasks. Must NOT trigger.

Minimum coverage: at least 1 prompt per category. Recommended: 3-5 per category for mature skills.

### 2. Outcome Correctness (30%)

Verify concrete, deterministic results.

Check types:
- File existence: expected files and directories created
- File content: key strings, patterns, or structures present
- Command execution: required commands ran in the right order
- Build success: `npm run build`, `pytest`, or equivalent passes
- Runtime smoke: dev server starts, health endpoint responds

### 3. Process Fidelity (15%)

Verify the skill followed its declared workflow.

Check types:
- Step ordering: prerequisite commands before dependent ones
- No skipped steps: all mandatory steps executed
- Tool usage: correct tools invoked (not arbitrary alternatives)
- No unauthorized side effects: no files modified outside scope

### 4. Style Compliance (15%)

Verify outputs follow declared conventions. Best evaluated with LLM rubric grading.

Check types:
- Naming conventions: files, variables, components follow declared patterns
- Formatting: indentation, imports, module structure as specified
- Technology choices: uses declared stack (Tailwind, not CSS modules)
- No forbidden patterns: no CSS modules when Tailwind required, no class components when functional required

### 5. Efficiency (15%)

Verify the skill completes without thrashing.

Check types:
- Command count: not excessive for the task complexity
- No retry loops: commands do not repeat due to errors
- Token usage: `input_tokens` and `output_tokens` within reasonable bounds
- Wall-clock time: completes within timeout

## Evaluation Tiers

| Tier | Trials | Use case |
|------|--------|----------|
| Smoke | 3-5 | Quick capability check during development |
| Standard | 10-15 | Reliable pass rate estimate before release |
| Regression | 25-30 | High-confidence regression detection in CI |

## Scoring

Each grader returns a score from 0.0 to 1.0. The final score is:

```
dimension_score = Σ (grader_score × weight) / Σ weight
overall_score = Σ (dimension_score × dimension_weight) / Σ dimension_weight
```

Thresholds:
- 90-100: Ship-ready
- 75-89: Acceptable, minor issues
- 50-74: Needs work, significant gaps
- Below 50: Not ready, fundamental problems

## Regression Detection

Compare current scores against a baseline (previous version or previous model).

Flag as regression if:
- Any dimension drops more than 10 points
- Overall score drops more than 5 points
- A previously passing deterministic check now fails
- A previously correct trigger now misfires

## Best Practices

- Grade outcomes, not steps. Check that the file was fixed, not that the agent ran a specific command.
- Instructions must name output files. If the grader checks for `output.html`, the instruction must say to save as `output.html`.
- Validate graders first. Use reference solutions before running real evals.
- Start small. 3-5 well-designed tasks beat 50 noisy ones.
- Let real failures drive coverage. Every manual fix is a signal — turn it into a test case.
- Run evals after model updates. A capability uplift skill may become unnecessary.
