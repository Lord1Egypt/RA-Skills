---
name: evaluate-agent
description: Score execution outputs using SpecCheck criteria, compute metrics, compare skill versions, and make retention decision
version: 1.0.0
---

# Evaluate-Agent

Evaluate both original and optimized skill versions using SpecCheck criteria, compute comprehensive metrics, perform comparative analysis, and make a data-driven retention decision.

## Purpose

Provide objective, quantitative evaluation of skill performance by:
- Scoring outputs against SpecCheck criteria
- Computing standardized evaluation metrics
- Identifying strengths, weaknesses, and regressions
- Making a retention decision based on performance data
- Generating a comprehensive results report

## Inputs

- Test tasks: `tasks/test/task_001/` through `tasks/test/task_008/`
- Original execution results: `exec_results/original/task_XXX/`
- Optimized execution results: `exec_results/optimized/task_XXX/`

## Implementation

This subskill uses `evaluator.py` to ensure rigorous evaluation and accurate metric computation.

## Execution Steps

### 1. Initialize Evaluator

Run the evaluator Python script:

```bash
cd subskills/evaluate-agent
python evaluator.py {target-skill-path} ../..
```

The script will:
- Load all 8 test tasks with their SpecCheck criteria
- Evaluate both original and optimized skill outputs
- Compute comprehensive metrics
- Make retention decision
- Generate `results_report.md`

### 2. Implement Evaluation Logic

You must implement the following methods in `evaluator.py`:

**`evaluate_task_output(task, result_dir, skill_version)`** - Score a single task:
- Read execution outputs from `result_dir/output/`
- Read execution log from `result_dir/run_log.md`
- Evaluate each criterion in `task['criteria']['criteria']`
- For each criterion, determine if satisfied and document evidence
- Return `TaskEvaluation` object with score, pass status, and criterion results

**`analyze_strengths_weaknesses(evaluation)`** - Analyze patterns:
- Identify what the skill does well (high-scoring tasks)
- Identify limitations (low-scoring tasks, common failure modes)
- Return tuple of (strengths list, weaknesses list)

**`identify_key_optimizations(original, optimized, comparison)`** - Link improvements to changes:
- Compare task-by-task results
- Identify which optimizations led to improvements
- Link improvements to specific changes in optimized SKILL.md
- Return list of dicts with keys: optimization, target, impact, tradeoffs

**`generate_recommendations(evaluation, retained)`** - Suggest improvements:
- Based on remaining weaknesses
- Suggest specific, actionable improvements
- Return list of recommendation strings

### 3. Evaluation Process

The script automatically handles:

**Scoring all test tasks:**
- For each of 8 test tasks, calls your `evaluate_task_output()` for both versions
- Computes metrics: pass rate, avg score, standard/advanced scores, error rate
- Compares original vs optimized performance

**Making retention decision:**
- If `optimized.avg_score > original.avg_score`: RETAIN
- Otherwise: DELETE
- Executes the decision (keeps or removes optimized directory)

**Generating comprehensive report:**
- Calls your analysis methods to identify strengths, weaknesses, optimizations
- Generates structured `results_report.md` with all metrics and detailed criterion results

### 4. Scoring Guidelines

When implementing `evaluate_task_output()`, ensure:

## Quality Guidelines

### Scoring Objectivity
- Apply criteria deterministically
- Use only observable evidence from outputs
- Do not infer intent or give partial credit unless criteria specify it
- If a criterion is ambiguous, document the interpretation used

### Analysis Depth
- Go beyond surface-level observations
- Connect failures to root causes in the skill's instructions
- Identify patterns across multiple tasks
- Distinguish between systematic issues and one-off errors

### Retention Decision
- Base decision strictly on the Average SpecCheck Score comparison
- Do not override the decision rule based on subjective judgment
- If scores are equal, DELETE (no improvement = no retention)
- Document the rationale clearly

## Output Verification

Before completing, verify:
- [ ] All 8 tasks have been scored for both skill versions
- [ ] All metrics have been computed correctly
- [ ] Retention decision follows the decision rule
- [ ] `results_report.md` exists and is complete
- [ ] If DELETED, the optimized skill directory has been removed
- [ ] If RETAINED, the optimized skill directory still exists

## Notes

- Scoring must be deterministic: same output → same score
- The test set is unseen during optimization, so it measures generalization
- Regressions are acceptable if overall performance improves
- The retention decision is binary and data-driven, not subjective
- This is the final step in the skills-coach pipeline
