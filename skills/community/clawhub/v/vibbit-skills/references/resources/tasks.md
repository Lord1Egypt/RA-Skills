# Tasks

Use [task query](../runtime/task-lifecycle.md) for a known task ID. There is no public full-history listing command or cross-account task search. Resume from this task's context and redacted journal; do not search unrelated accounts.

Inspect the actual state and result before deciding to retry. Preserve completed parts, report terminal errors, and stop when a required capability or authorization is unavailable. See [task lifecycle](../runtime/task-lifecycle.md).
