---
name: workspace-smoke-test
description: Run quick health checks on the workspace: skill loadability, evolver version/status, git state, and a summary of failures. Use when you need a fast system health snapshot or before running evolver cycles.
---

# Workspace Smoke Test

Run lightweight checks to verify the workspace is in a sane state.

## Usage

```bash
node skills/workspace-smoke-test/scripts/smoke.js
node skills/workspace-smoke-test/index.js   # programmatic
```

## Checks

- **Skill loadability**: verifies each `skills/<name>/index.js` exists and requires without error
- **Evolver status**: checks `evolver --version` responds
- **Git state**: counts dirty files in the workspace

## Output

JSON object with counts, failures, and tool status.
