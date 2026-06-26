# Symphony Incident Playbook

Use this playbook to triage common runtime failures.

## Fast Triage Matrix

| Symptom | Likely Cause | Immediate Action |
|--------|--------------|------------------|
| No issues dispatch | Wrong `project_slug` or active states | Verify tracker config and state names in `WORKFLOW.md` |
| Repeated retry loop | Hook failure or template render error | Check logs, fix root cause, keep workspace state |
| Agent stops unexpectedly | Missing auth/permissions or timeout | Confirm required secrets and Codex settings |
| Stale workspaces never removed | Terminal states mismatch | Align terminal state names with Linear workflow |
| Workflow reload ignored | File watcher or parse failure | Restart service after validating YAML |

## Recovery Steps

1. Capture the exact issue identifier and current tracker state.
2. Inspect Symphony logs for the first failing event, not only the last one.
3. Validate `WORKFLOW.md` front matter and prompt template variables.
4. Confirm environment variables (`LINEAR_API_KEY`, optional workspace root vars).
5. Re-run one issue with low concurrency to verify the fix.

## Retry Discipline

- Retries should resume in the same workspace for that issue.
- Do not delete workspace contents unless corruption is confirmed.
- Increase backoff for repeated transient failures.
- Escalate to manual intervention after repeated identical failures.

## Cleanup Discipline

- Before removing a workspace, verify the issue is terminal.
- Run `before_remove` hooks only if directory exists.
- Log cleanup outcomes for each issue identifier.

## Post-Incident Notes

After resolution, store in `~/symphony/incidents.md`:
- incident summary
- root cause
- remediation steps
- validation evidence
- prevention change for future runs
