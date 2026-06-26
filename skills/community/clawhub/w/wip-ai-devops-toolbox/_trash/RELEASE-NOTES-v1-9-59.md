# Release Notes: wip-ai-devops-toolbox v1.9.59

**Fix three bugs in branch guard destructive command handling.**

## The story

v1.9.56 added destructive command blocking but introduced three bugs because the new code was written differently from the existing guard pattern. The existing guard checks allowed patterns before blocked patterns and works per-command. The new code skipped the allowed check and matched against the entire raw command string, causing false positives on quoted text (blocking `gh issue create` when the body mentioned git commands) and false negatives on compound commands (allowing `rm -f file ; echo done` because `echo` is in the allowed list).

Fix: two helper functions that strip quoted content before matching and check each command segment independently. Same pattern as the existing guard code. Also adds `~/.claude/plans/` to the shared state allowlist so plan files are editable.

## Issues closed

- #232 (branch guard three bugs in v1.9.56)

## How to verify

```bash
# These should now be ALLOWED (were false-positive blocked):
# gh issue create --body "use git checkout -- to fix"
# echo "don't run git commit on main"

# These should now be DENIED (were false-negative allowed):
# rm -f file ; echo done  (on main)

# These should still be DENIED:
# git checkout -- file.txt
# python3 -c "open('f').write('x')"
```
