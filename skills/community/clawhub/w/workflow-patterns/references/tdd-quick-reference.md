# TDD Quick Reference

## The Cycle

```
RED → GREEN → REFACTOR → COMMIT
```

1. **RED:** Write a failing test that defines desired behavior
2. **GREEN:** Write minimum code to make it pass
3. **REFACTOR:** Improve code while keeping tests green
4. **COMMIT:** Record the change with task reference

## Per-Task Checklist

```
[ ] Mark task as [~] (in progress)
[ ] Write failing tests (RED)
[ ] Implement minimum code (GREEN)
[ ] Refactor for clarity
[ ] Verify 80%+ coverage
[ ] Commit with task reference
[ ] Mark task as [x] with SHA
[ ] Commit plan update
```

## Phase Completion Checklist

```
[ ] All tasks in phase complete
[ ] All tests passing
[ ] Coverage at 80%+
[ ] Generate verification steps
[ ] Present to user for approval
[ ] WAIT for explicit approval
[ ] Create checkpoint commit
[ ] Record SHA in plan
```

## Commit Message Template

```
<type>(<scope>): <subject>

- Change 1
- Change 2
- Change 3

Task: <id>
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Writing implementation first | Always start with failing test |
| Making tests pass "too well" | Write minimum code only |
| Skipping refactor | Refactor is where quality happens |
| Ignoring coverage | Add tests until 80%+ |
| Proceeding without approval | Wait for explicit "approved" |

## Task Status Quick Reference

```
[ ] pending
[~] in progress
[x] complete (include SHA)
[-] skipped (include reason)
[!] blocked (include blocker)
```
