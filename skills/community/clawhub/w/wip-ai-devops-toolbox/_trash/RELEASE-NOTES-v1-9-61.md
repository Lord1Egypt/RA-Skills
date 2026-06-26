# Release Notes: wip-ai-devops-toolbox v1.9.61

**Add test script for branch guard. Fix node bypass regex.**

## The story

Every guard bug this session (v1.9.56-59) would have been caught by running a test before merging. This release adds test.sh to the guard that pipes test JSON into guard.mjs and verifies allow/deny results. 30 test cases covering destructive commands, quoted strings (Bug 1/3), compound commands (Bug 2), safe commands, and plan files.

Also fixes the node bypass regex: `require('fs').writeFileSync` wasn't caught because the regex looked for `fs.writeFile` literally. Broadened to match `writeFile` after `node -e`.

## Issues closed

- #232 (guard test coverage)

## How to verify

```bash
cd tools/wip-branch-guard && bash test.sh
# Should show: 30 passed, 0 failed, 3 skipped
```
