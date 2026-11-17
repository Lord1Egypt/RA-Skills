# Prompt Evolution: Self-Improving Prompts for AI Agents

## Overview

Prompt evolution is the systematic process of improving the instructions, templates, and behavioral patterns that govern an AI agent's actions. Just as genetic algorithms evolve solutions through selection, mutation, and fitness evaluation, prompt evolution applies these principles to the text-based instructions that define agent behavior. This document describes how an AI agent can automatically improve its own prompts, skills, and procedural instructions through iterative refinement driven by performance feedback.

## The Prompt Evolution Loop

The core evolution cycle follows a generate → evaluate → select → mutate pattern:

```
┌─────────────────────────────────────────────────────────┐
│                  PROMPT EVOLUTION LOOP                    │
│                                                           │
│   ┌──────────┐    ┌──────────┐    ┌──────────┐         │
│   │ Generate │───→│ Evaluate │───→│  Select  │         │
│   │Variants  │    │ Fitness  │    │ Survivors│         │
│   └──────────┘    └──────────┘    └────┬─────┘         │
│        ↑                               │                 │
│        │          ┌──────────┐         │                 │
│        └──────────┤  Mutate  │←────────┘                 │
│                   │& Recombine│                           │
│                   └──────────┘                           │
│                                                           │
│   ┌─────────────────────────────────────────────┐       │
│   │         PROMPT VERSION STORE                 │       │
│   │  v1.0 → v1.1 → v1.2 → ... → v_current      │       │
│   │  (with fitness scores and lineage)           │       │
│   └─────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────┘
```

## Prompt Version Control

### Version Naming Convention
```
Format: {skill-name}-v{major}.{minor}
Example: debugging-checklist-v2.3

Major version: Significant structural change (new steps, removed sections)
Minor version: Incremental improvement (wording, ordering, emphasis)
```

### Version Metadata
Each prompt version stores:
- **Version ID**: Unique identifier
- **Parent version**: What this version was derived from
- **Mutation description**: What changed and why
- **Fitness score**: Performance metric at time of evaluation
- **Sample size**: Number of tasks evaluated against
- **Creation date**: When this version was created
- **Status**: active | deprecated | experimental | rolled-back

### Version Store Structure
```
skills/
└── {skill-name}/
    ├── SKILL.md              # Current active version (symlink or copy)
    ├── versions/
    │   ├── v1.0.md           # Original version
    │   ├── v1.1.md           # First improvement
    │   ├── v1.2.md           # Second improvement
    │   └── ...
    ├── changelog.md          # History of all changes
    ├── fitness-log.md        # Performance scores per version
    └── rollback-pointer      # Points to last known-good version
```

## Mutation Strategies

Mutations are the mechanism for generating prompt variants. Different mutation types serve different improvement goals.

### 1. Precision Mutation
**What:** Make instructions more specific and unambiguous.
**When:** Agent frequently misinterprets the prompt.
**Example:**
```
Before: "Check if the website is working"
After:  "Open the website URL in browser tool, take a screenshot, 
         verify HTTP 200 status, and confirm the main content 
         area renders without error messages"
```

### 2. Generalization Mutation
**What:** Make instructions more flexible to handle edge cases.
**When:** Prompt works for happy path but fails on variations.
**Example:**
```
Before: "If the error is a 404, check if the container is running"
After:  "If the error indicates a missing resource (404, not found, 
         does not exist), systematically check: container status, 
         routing configuration, file existence, and permissions"
```

### 3. Ordering Mutation
**What:** Reorder steps to improve efficiency or success rate.
**When:** Analysis shows early steps frequently fail or waste time.
**Example:**
```
Before: 1. Read docs → 2. Try implementation → 3. Test → 4. Debug
After:  1. Quick test to understand current state → 2. Read relevant docs 
        → 3. Implement → 4. Test → 5. Debug
```

### 4. Deletion Mutation
**What:** Remove unnecessary or harmful instructions.
**When:** Steps that don't contribute to outcomes are identified.
**Example:**
```
Before: "First, greet the user. Then, check the database. Then, process..."
After:  "Check the database. Process..."
(Removed unnecessary greeting step that added tokens without value)
```

### 5. Addition Mutation
**What:** Add missing steps or safeguards.
**When:** Failures reveal gaps in the procedure.
**Example:**
```
Before: "Deploy the container and verify it's running"
After:  "Deploy the container, wait 10 seconds for startup, 
         verify health endpoint returns 200, check logs for 
         errors, then verify from external network"
```

### 6. Emphasis Mutation
**What:** Change the relative emphasis/priority of instructions.
**When:** Agent follows instructions but prioritizes incorrectly.
**Example:**
```
Before: "Complete the task efficiently and accurately"
After:  "CRITICAL: Accuracy over speed. Verify every step before 
         proceeding. Do NOT sacrifice correctness for efficiency."
```

### 7. Cross-Pollination Mutation
**What:** Combine elements from two different prompt versions.
**When:** Two variants each have strengths in different areas.
**Example:**
```
Version A has great error handling but slow execution
Version B has fast execution but poor error handling
Cross-pollinated version: Fast path for common cases + 
                          robust error handling for edge cases
```

## Fitness Evaluation

### Fitness Metrics for Prompts
| Metric | Description | Weight |
|--------|-------------|--------|
| Success rate | % of tasks completed successfully | 40% |
| Efficiency | Tokens used per successful task | 20% |
| First-attempt rate | % success without rework | 20% |
| Error rate | Frequency of errors during execution | 15% |
| User satisfaction | Explicit/implicit feedback quality | 5% |

### Fitness Function
```
Fitness = (0.40 × SuccessRate) + 
          (0.20 × EfficiencyScore) + 
          (0.20 × FirstAttemptRate) + 
          (0.15 × (1 - ErrorRate)) + 
          (0.05 × SatisfactionScore)

Where all component scores are normalized to [0, 1]
```

### Evaluation Protocol
```
1. Select evaluation task set (representative sample of target tasks)
2. Execute each task with the prompt variant
3. Record outcomes (success/failure, tokens used, errors, time)
4. Compute fitness score
5. Compare against current active version's fitness
6. If new variant fitness > current fitness × 1.05 (5% improvement threshold)
   → promote to active
7. Otherwise, archive variant with results
```

### Evaluation Sample Size
- Minimum 5 tasks per variant for statistical significance
- For high-variance tasks, increase to 10+
- Track confidence interval: if CI overlaps with current, result is inconclusive

## A/B Testing Prompts

### Controlled Experiment Design
When comparing two prompt versions, use A/B testing methodology:

```
1. HYPOTHESIS: "Version B will improve success rate by >5%"
2. TASK SET: Select N similar tasks (same type, similar difficulty)
3. RANDOMIZATION: Randomly assign tasks to Group A (current) or Group B (new)
4. EXECUTION: Run all tasks, record outcomes
5. ANALYSIS: Compare success rates using statistical test
6. DECISION: If p < 0.05 AND improvement > 5%, adopt Version B
```

### Practical Constraints
- In production, we can't truly randomize (each task is unique)
- Instead, use matched pairs: compare performance on similar task types before/after
- Use rolling evaluation: track metrics continuously, detect improvement over time
- Minimum observation period: 1 week of normal operation

### A/B Testing in the 2 AM Cycle
```
During daily reflection:
1. Identify prompts that were used today
2. Compare today's metrics against baseline (pre-change) metrics
3. If prompt was recently changed:
   - Is performance improving, stable, or declining?
   - Has the change been in effect long enough to evaluate?
4. If performance declining → flag for rollback
5. If performance improving → continue monitoring
6. If stable for 7+ days → confirm change, update baseline
```

## Rollback Mechanisms

### Automatic Rollback Triggers
1. **Performance regression**: Fitness score drops >10% from baseline
2. **Critical failure**: Prompt causes task that previously succeeded to fail
3. **User complaint**: Explicit negative feedback about agent behavior
4. **Safety violation**: Prompt leads to behavior outside safety boundaries

### Rollback Process
```
1. DETECT: Rollback trigger fires
2. IDENTIFY: Find last known-good version from rollback-pointer
3. REVERT: Replace current SKILL.md with last known-good version
4. LOG: Record rollback reason, affected version, and evidence
5. NOTIFY: Flag for review during next reflection cycle
6. QUARANTINE: Move failed version to versions/ with "rolled-back" status
7. ANALYZE: During reflection, determine why the variant failed
```

### Graduated Rollback
Not all regressions require full rollback:
- **Minor regression** (< 5% fitness drop): Monitor for 3 days, auto-recover if improves
- **Moderate regression** (5-10% drop): Rollback to previous version, analyze
- **Major regression** (> 10% drop): Immediate rollback, quarantine variant, alert

## Evolutionary Algorithms for Prompts

### Genetic Algorithm Approach
```
Population: Set of prompt variants (10-20 variants)
Generation: One cycle of evaluation + selection + mutation

Algorithm:
1. INITIALIZE: Start with current prompt + N random mutations
2. EVALUATE: Score each variant on fitness function
3. SELECT: Keep top-K variants (elitism)
4. CROSSOVER: Combine pairs of high-fitness variants
5. MUTATE: Apply random mutations to offspring
6. REPLACE: New generation = elites + offspring
7. REPEAT: Until fitness converges or max generations reached
```

### Population Diversity Management
- Maintain at least 3 fundamentally different approaches in the population
- If population converges (all variants similar), inject random variants
- Track "fitness landscape" — if stuck at local optimum, increase mutation rate

### Multi-Objective Optimization
Prompts often need to optimize for competing objectives:
- Speed vs. thoroughness
- Brevity vs. completeness
- Flexibility vs. precision
- Autonomy vs. safety

Use Pareto optimization: maintain a set of prompts that represent different tradeoffs, select based on current task requirements.

## Prompt Fitness Scoring in Practice

### Daily Scoring (Automated)
```python
# Pseudocode for daily fitness computation
def compute_daily_fitness(prompt_id, date):
    tasks = get_tasks_using_prompt(prompt_id, date)
    
    success_rate = count(tasks, success=True) / len(tasks)
    avg_tokens = mean(task.tokens_used for task in tasks)
    efficiency = 1.0 / (1.0 + avg_tokens / 10000)  # Normalize
    first_attempt = count(tasks, rework=False) / len(tasks)
    error_rate = count(tasks, errors=True) / len(tasks)
    
    fitness = (0.40 * success_rate + 
               0.20 * efficiency + 
               0.20 * first_attempt + 
               0.15 * (1 - error_rate) + 
               0.05 * user_satisfaction)
    
    return fitness
```

### Trend Analysis
Track fitness over time to detect:
- **Improving trend**: Prompt evolution is working
- **Plateau**: May need different mutation strategies
- **Declining trend**: Task distribution may have shifted, need new approach
- **Sudden drop**: Environmental change, regression, or data quality issue

## Integration with Skill Workshop

The Skill Workshop system provides the infrastructure for managing prompt evolution:
- **Create**: New prompt variants are proposals in the workshop
- **Update**: Successful variants update the live skill
- **Revise**: Underperforming variants are revised before re-evaluation
- **Rollback**: Failed variants are rejected, reverting to previous version

## Conclusion

Prompt evolution transforms the agent's instructions from static documents into living, adapting systems. By applying evolutionary principles — variation, selection, and inheritance — to prompt design, the agent can systematically improve its own behavioral instructions without human intervention. The key is rigorous fitness evaluation, safe rollback mechanisms, and maintaining enough diversity to avoid local optima. Combined with the memory and evaluation systems described in companion documents, prompt evolution provides the mechanism by which self-improvement insights are actually encoded into agent behavior.
