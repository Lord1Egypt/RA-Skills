# Workflow Patterns

Use this reference when the skill needs a reusable multi-step process.

## Default workflow shape
1. Classify the task.
2. Gather the required facts.
3. Produce the first concrete artifact.
4. Branch only when a named condition is true.
5. Validate the artifact.
6. Stop when the artifact or decision exists.

## Good workflow properties
- One action per step.
- Explicit branch rules.
- Explicit output or stop condition.
- Cheap navigation to references.
- Deterministic validation near the end.

## Avoid
- Long narrative before the first action.
- Repeated rules in multiple sections.
- Hidden dependencies between far-apart sections.
- Branches that require guessing.
