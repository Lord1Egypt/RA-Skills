# Workflow Pattern Details

> Load this when you need in-depth comparison of the 5 workflow patterns.

## Pattern 1: Prompt Chaining

```
Step A → [checkpoint] → Step B → [checkpoint] → Step C
```

- **When**: Task decomposes into sequential steps, each processing the previous output
- **Strengths**: Programmatic checks between steps; easy to debug; predictable
- **Weaknesses**: Not suitable for branching logic
- **Most common pattern** — fits most content generation tasks

## Pattern 2: Routing

```
Input → [classify] → Route A / Route B / Route C
```

- **When**: Input has clear types; different types need different processing flows
- **Strengths**: Clean separation of concerns; easy to add new routes
- **Weaknesses**: Classification must be accurate; route logic duplication possible
- **Example**: Article type → corresponding template and rules

## Pattern 3: Parallelization

```
Input → [split] → Subtask A + Subtask B + Subtask C → [merge]
```

- **When**: Subtasks are independent and can run in parallel for speed
- **Strengths**: Significantly faster than sequential; good for batch processing
- **Weaknesses**: Merge logic can be complex; need to handle partial failures
- **Example**: Core article → simultaneously generate blog, social, newsletter versions

## Pattern 4: Orchestrator-Workers

```
Central LLM → [dynamic dispatch] → Worker1 + Worker2 + ... → [merge]
```

- **When**: Subtasks cannot be predefined; need dynamic planning
- **Strengths**: Maximum flexibility; handles unexpected inputs well
- **Weaknesses**: High complexity; hard to debug; expensive
- **Use sparingly** — only when other patterns clearly don't fit

## Pattern 5: Evaluator-Optimizer

```
Generate → Evaluate → Feedback → Regenerate → ... until pass
```

- **When**: Clear evaluation criteria exist; iteration brings measurable improvement
- **Strengths**: Self-correcting; output quality improves with each iteration
- **Weaknesses**: Can be slow (multiple LLM calls); needs good evaluation criteria
- **Example**: Content review, code review, security audit

## Decision Flow

```
Is task decomposable into fixed steps?
├─ Yes → Steps independent?
│        ├─ Yes → Pattern 3 (Parallelization)
│        └─ No  → Pattern 1 (Prompt Chaining)
└─ No → Input types predictable?
         ├─ Yes → Pattern 2 (Routing)
         └─ No → Need iteration?
                  ├─ Yes → Pattern 5 (Evaluator-Optimizer)
                  └─ No  → Pattern 4 (Orchestrator-Workers)
```
