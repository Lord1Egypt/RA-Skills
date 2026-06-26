---
name: optimize-agent
description: Optimize a target Skill using training-free GRPO to maximize SpecCheck scores across training tasks
version: 1.0.0
---

# Optimize-Agent

Apply Group Relative Policy Optimization (GRPO) to iteratively improve a Skill's SKILL.md prompt/instructions based on performance across training tasks.

## Purpose

Generate an optimized version of the target Skill that:
- Achieves higher SpecCheck scores on training tasks
- Clarifies ambiguous instructions
- Handles edge cases more robustly
- Maintains or improves core functionality

## Inputs

- `target-skill-path`: Path to the original Skill directory
- Training tasks: `tasks/train/task_001/` through `tasks/train/task_012/`

## Implementation

This subskill uses `grpo_optimizer.py` to ensure rigorous GRPO implementation and accurate scoring.

## Execution Steps

### 1. Initialize GRPO Optimizer

Run the optimizer Python script:

```bash
cd subskills/optimize-agent
python grpo_optimizer.py {target-skill-path} ../..
```

The script will:
- Load the original SKILL.md
- Load all 12 training tasks
- Compute baseline performance
- Run GRPO optimization loop (3-10 iterations)
- Save optimized skill and optimization log

### 2. Implement Optimization Logic

You must implement the following methods in `grpo_optimizer.py`:

**`generate_variants(iteration, training_tasks)`** - Generate candidate variants:
- Analyze failures from previous iteration (stored in `self.iterations`)
- Identify patterns in low-scoring tasks
- Generate N=4 targeted mutations to address weaknesses
- Return list of N variant SKILL.md contents (as strings)
- Document what mutations were applied to each variant

**`execute_and_score_task(skill_content, task)`** - Execute and score a variant:
- Create temporary SKILL.md with the variant content
- Execute the skill with the task input from `task['task_content']`
- Evaluate output against criteria in `task['speccheck_content']`
- Return `TaskScore` object with score, total, passed status, and criterion results

### 3. GRPO Optimization Loop

The script automatically handles the optimization loop (3-10 iterations):

**Per Iteration:**

1. **Generate variants**: Calls your `generate_variants()` to create 4 candidate SKILL.md variants
2. **Execute variants**: Runs each variant on all 12 training tasks using your `execute_and_score_task()`
3. **Compute relative rewards**: Applies GRPO formula (normalize scores relative to group mean)
4. **Select best**: Chooses variant with highest absolute score as new baseline
5. **Check convergence**: Stops early if no improvement for 2 consecutive iterations

### 4. Mutation Strategy Guidelines

When implementing `generate_variants()`, apply targeted mutations based on failure analysis:

**Mutation types:**
- **Clarification**: Make ambiguous instructions more explicit
- **Edge case handling**: Add specific guidance for boundary conditions
- **Restructuring**: Reorder steps for better logical flow
- **Constraint refinement**: Add or clarify constraints, output formats
- **Simplification**: Remove redundant or contradictory instructions
- **Error handling**: Add guidance for unexpected inputs or failure modes

**Mutation strategy:**
- Analyze which training tasks failed in previous iteration
- Identify patterns (e.g., all empty input tasks failed)
- Apply mutations that specifically address observed failure modes
- Keep mutations targeted and minimal (avoid wholesale rewrites)

### 5. Output Files

The script automatically generates:
- `{target-skill-name}-optimized/SKILL.md` - Optimized skill
- `optimization_log.md` - Complete iteration history with scores and rationale

## Quality Guidelines

### Mutation Quality
- Each mutation should be hypothesis-driven (based on observed failures)
- Avoid random or unfocused changes
- Maintain the skill's original intent and scope
- Don't add functionality beyond the original specification

### Execution Fidelity
- Execute each variant exactly as the skill would be invoked in production
- Capture all outputs, errors, and side effects
- Ensure consistent execution environment across all variants

### Scoring Accuracy
- Apply SpecCheck criteria deterministically
- Document any ambiguities in scoring
- If a criterion is unclear, interpret conservatively

## Output Verification

Before completing, verify:
- [ ] `{target-skill-name}-optimized/` directory exists
- [ ] Optimized `SKILL.md` is present and well-formed
- [ ] `optimization_log.md` exists and contains complete iteration history
- [ ] Final training score is equal to or better than baseline
- [ ] All mutations are documented with rationale

## Notes

- GRPO is training-free: no gradient computation or backpropagation
- The optimization is prompt-engineering, not model fine-tuning
- Overfitting to training tasks is possible; test set evaluation will reveal this
- If no improvement is found after 10 iterations, return the best variant found (may be the original)
