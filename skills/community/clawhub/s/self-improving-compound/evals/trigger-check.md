# Trigger Check — Self-Improving Evaluation

## Purpose
Verify that the agent correctly identifies when to log a learning.

## Checklist

- [ ] Did the agent detect an explicit user correction?
- [ ] Did the agent detect a non-obvious failure?
- [ ] Did the agent detect a missing capability request?
- [ ] Did the agent detect a better approach for a recurring task?
- [ ] Did the agent avoid logging routine noise (typos, expected failures)?

## Threshold
Pass if ≥3/5 checks are true.
