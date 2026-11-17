# Delivery and recovery

Use before an authorized publication, deployment, infrastructure change or incident response.

## Make the action reviewable

Confirm the account, environment, artifact/commit, version and affected users. Check that the user's existing authorization covers this action; do not request it again for the same scope. Prepare the exact change and verification before asking for a missing decision. Follow required project checks and approvals without inventing additional gates.

Inspect staged and unstaged changes before preparing the artifact, and preserve unrelated work; a failed check does not authorize discarding edits. Update affected commands, defaults and contracts with the implementation. [Version control](version-control-and-review.md) covers hooks and shared history, and [documentation](documentation.md) covers exercising changed commands.

Inspect a deployment plan for unexpected deletes, replacements, permission changes or data movement. Use the tested artifact rather than rebuilding different contents for production. Preserve unrelated configuration and the previous artifact when needed for recovery.

## Match recovery to the effect

For a reversible publication, verify the published version and how to withdraw it. For a production service, identify the health signal, stop condition and rollback/forward-fix path. Use a staged rollout when impact or uncertainty warrants it, not for every documentation update. The optional [change note](../templates/change-note.md) records the target, recovery and stop condition when reviewers need them.

A code rollback is safe only if it still understands the current data/configuration. Rehearse a material recovery path in a suitable environment and state any part not exercised. Compare a canary with its control; aggregate service metrics can hide a severe problem affecting a small rollout.

After the action, check user-visible behavior and the expected version. A successful upload, accepted request or access-control page does not prove publication, application health or delivery. Distinguish queued checks from a live result. If an external check fails, retain its status and artifact; do not create repeated releases merely to evade it.

## Service lifecycle

When changing health checks or shutdown, separate serving readiness from process liveness. A shared dependency outage should not make every instance fail liveness and restart. Gate slow startup separately when supported. Stop accepting new work before draining in-flight requests/jobs within a bounded shutdown deadline; verify what happens to unfinished work.

## During an incident

Reduce ongoing impact first using the authorized, least disruptive intervention. Verify the affected environment and available evidence; do not assume rolling back is safe after a data change. Escalate a missing consequential decision while continuing read-only diagnosis.

After mitigation, confirm recovery and investigate the cause ([debugging](debugging.md)). Add a regression check, alert or procedure correction that addresses the demonstrated failure. A formal [incident review](../templates/incident-review.md) belongs where the impact or team process requires it; routine tasks do not need a retrospective document.

## Sources

- [Kubernetes probe semantics](https://kubernetes.io/docs/concepts/workloads/pods/probes/)
- [Google SRE: canarying releases](https://sre.google/workbook/canarying-releases/)
- [Google SRE: managing incidents](https://sre.google/sre-book/managing-incidents/)
- [Google SRE: postmortem culture](https://sre.google/sre-book/postmortem-culture/)
