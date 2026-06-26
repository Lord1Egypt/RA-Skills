# Checkpoints

One file per workflow: `<workflow-id>.md`
Each file defines what to verify at each checkpoint for that workflow.

## Format

```markdown
# Checkpoints: <workflow-id>

## CP-001 — After step N
- Verify: [what to check]
- How: [how to verify — inspect output / confirm field exists / run command / etc.]
- Pass condition: [what constitutes a pass]
- Failure type: hard | soft
- On fail: [what to do]
```
