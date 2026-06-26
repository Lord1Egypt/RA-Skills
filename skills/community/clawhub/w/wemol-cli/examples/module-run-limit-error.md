# Module Run Limit Error Example

Use this example when `job submit` is rejected before job creation with a module-level run-limit error.

## Why This Example Matters

This is a distinct failure mode from:
- invalid payload fields
- authentication failure
- missing output keys
- empty result data after a successful run

In this case, the backend rejects submission immediately because the module cannot start another run for the current user.

## Verified Error Pattern

When submitting a module with a valid-looking payload, the CLI returned a run-limit error containing `JobModuleTaskMaxNumLimit` (prefix formatting may vary by version):

```text
JobModuleTaskMaxNumLimit: 作业模块任务最大数限制
... {"Limit.RunMaxNum":0,"Module.Id":<module_id>,"User.RunNum":1}
```

This error was reproduced again in a separate retry, not only during an earlier period when multiple unrelated jobs had been submitted.

## Interpretation

The best-supported interpretation is:
- this is a module-level run-capacity or permission limit
- the submission is blocked before a new job is created
- repeated retries with the same payload are unlikely to help

What this does **not** prove with certainty:
- whether the limit is caused by a currently running hidden task
- whether it is a user quota, module policy, or backend occupancy rule

## Agent Rules From This Example

- Do not keep retrying the same `job submit` call when `JobModuleTaskMaxNumLimit` appears.
- Do not rewrite the payload unless there is separate evidence that the payload is invalid.
- Treat this as a backend availability or quota problem for that module, not as a normal parameter-format error.
- Check whether earlier jobs from the same module can be found with `job search` or `job list`, but do not assume visible history is complete.
- Report the limit clearly to the user and suggest waiting, freeing capacity if possible, or choosing another module.

## Recommended Response Pattern

When this error appears:

1. Confirm that the payload was already structurally valid.
2. State that the module rejected the submission due to run-limit constraints.
3. Avoid blind retries.
4. If useful, look for prior jobs or suggest an alternative module.
