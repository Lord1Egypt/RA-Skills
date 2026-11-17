# Release and Rollback Gate

## Release boundary

Use `release` mode only when this run will initiate a deployment. Verification of a build/version that someone else already deployed is an `audit` with `release-regression` depth, even when the target is production.

A release can use `repair_authorized=false` to validate and deploy an already prepared artifact. In that path, do not enter `REPAIR` or edit source; still run all declared artifact-level and pre-deploy checks before the gate.

## Target authorization

Production is never inferred. This holds when it is the only configured target, the repository default, the provider's currently selected target, or the environment already open in a signed-in browser. The current task must explicitly name provider, account, project, environment, and region. Record an immutable target identifier and authorization source when the platform provides one. Authorize and gate each target independently.

For non-production, state the resolved provider/account/project/environment/region and whether it is isolated or shared. A discoverable isolated target may be selected when it unambiguously matches the request; a shared target remains read-only unless the deployment and any data effects are explicitly authorized.

“全自动”, “别问”, or “你决定” does not authorize a target, deployment, Git action, rollback, or high-side-effect operation. If exact authorization is already present and the target/action/effect has not changed, do not request it again.

## Release prerequisites

Before recording a passing release gate, confirm all applicable items:

- one immutable target and its deployment authority are explicit;
- the intended artifact identity is recorded and traceable to a commit, version, image digest, or build;
- `repair_authorized` accurately reflects whether source edits were requested;
- the established release mechanism is known, and every required Git or delivery action is separately authorized;
- the working tree is clean or every unrelated change is understood and excluded;
- all applicable required A/B browser scenarios and required focused tests, lint/type checks, and build have evidenced current bound passes;
- when repair is authorized, every confirmed in-scope issue is verified; otherwise no in-scope P0/P1 remains unresolved;
- broad discovery baselines are optional; any required failure proven pre-existing and unrelated has an evidenced `baseline-debt` disposition rather than a rewritten pass;
- no secret, debug bypass, local URL, temporary flag, or sensitive evidence enters the artifact;
- configuration and migrations are compatible with the target;
- at least one required post-deploy health/readiness check is documented; every additional in-scope health plan is also release-gating and must pass;
- rollback readiness is recorded separately from rollback execution authorization;
- the release window and externally visible effects match the one-run authorization.

Bind every release result and the gate to the same release target, intended artifact, and active attempt. Configure that target/artifact/rollback policy once; the exact same pre-attempt command is idempotent, but a changed configuration or any reconfiguration after an attempt requires a new run. The gate consumes the latest evidenced results for all in-scope required non-post-deploy plans, requires at least one required pre-deploy plan, and snapshots the latest bound baseline/post-fix pass for every applicable required A/B scenario. It rejects every unresolved in-scope issue when repair is authorized, and unresolved in-scope P0/P1 otherwise. Its exact check and browser snapshots are rechecked before `DEPLOY`; any new declaration, result, or disposition makes the previous gate stale. A success from another target, artifact, attempt, or an older result cannot satisfy it. If the repository has no safe discoverable deployment or recovery path, stop and ask; do not invent one.

## Git and optional delivery authority

Treat these as separate external operations:

- commit;
- push;
- create or update a PR;
- merge;
- upload or send a report/artifact;
- deploy;
- execute rollback.

Obtain explicit authorization before any commit, push, PR, merge, or delivery action not already granted. An established named workflow may bundle operations only after its externally visible steps are disclosed and the user authorizes that workflow. Explaining an extra Git action is not authorization. In `REPORT`, call `plan-delivery` separately for each Git/report action with its current-task authority source, exact target, and idempotency key; only then enter `DELIVER`. After execution or reconciliation, call `record-delivery` with the outcome, external identifier, details, and evidence. If interrupted while planned or unknown, inspect external state before replay. `validate --strict` rejects an unsettled or failed delivery. This handoff is not deployment evidence.

## Rollback readiness and execution

A known rollback path does not authorize running it. Before deployment, record:

- recovery path and trigger conditions;
- recovery artifact or known-good version;
- whether rollback execution is authorized;
- the current-task authorization source when rollback execution is authorized;
- whether authorization is unconditional or conditional on named health/regression triggers.

The user may grant conditional rollback authorization before deployment. Record each allowed condition with `--rollback-trigger`. When one exact recorded trigger occurs, execute that established application rollback without asking again, then call `record-rollback` with the matching `--trigger` and `--trigger-evidence`, restored artifact identity, and health result. A different or unevidenced trigger is not authorized. Without execution authorization, stop related production mutations/deployments, keep only safe read-only monitoring and diagnosis active, and request confirmation.

Never automatically roll back or forward production data or schema. Those actions always require a documented migration/recovery plan and separate exact authorization at execution time, even when application rollback was pre-authorized.

## Deployment sequence

1. Record the authorized immutable target, intended artifact, rollback readiness, rollback execution authority, and health plan.
2. Create one active deployment attempt bound to that target and artifact before recording its first release result; create it by `BASELINE` when baseline evidence belongs to the attempt.
3. Record evidenced baseline, post-fix, artifact, and pre-deploy checks plus applicable required A/B browser results against that same target/artifact/attempt.
4. Evaluate and record the release gate; immediately before `DEPLOY`, recheck both its prerequisites and exact result snapshot.
5. Deploy one coherent, locally verified batch through the established mechanism.
6. Reconcile the target's observed artifact with the intended artifact using provider or target-state evidence; a command exit code alone is not proof.
7. Run every in-scope evidenced bound health/readiness check. Any non-passing health observation on the active attempt is preserved as a deployment degradation and blocks a successful release settlement; a later pass cannot erase it. Apply the recorded rollback/failed-settlement policy rather than relabeling the attempt successful.
8. Execute R4 critical smoke with safe read-only steps or authorized synthetic data.
9. Re-verify both R0 and R1 for every in-scope issue repaired by this run, regardless of severity, against the deployed artifact.
10. Check relevant runtime errors, logs, and metrics when access is authorized.
11. Record release outcome, checks, coverage, external effects, cleanup, and rollback status against the same target/artifact/attempt.

Do not perform repeated production hot-fix/deploy loops. Return to local diagnosis and verification after an application-behavior failure.

## Failure and retry policy

- A timeout, lost connection, unknown outcome, or partial deployment is not a confirmed transient failure. First reconcile actual target artifact, deployment record, health, and any partial external effect. Record the reconciled observation on the same attempt. `failed-unchanged` requires the observed unchanged artifact/version plus provider or target-state evidence; a verbal “nothing changed” with no identity does not unlock retry. Do not retry while state is unknown or partial.
- Retry a confirmed transient infrastructure failure at most once for the same target/artifact, and only after the active attempt is evidenced as `failed-unchanged`. Then advance `DEPLOY → LOCAL_VERIFY`, declare the one allowed retry attempt, and rerun every bound result before a new gate. A second failed attempt is reported, not retried.
- On build or logic failure, stop deployment work; repair only if authorized, then verify locally before a new gated attempt.
- On health degradation, error spike, unexpected mutation, auth anomaly, or P0/P1 regression, stop related production mutations immediately and apply the recorded rollback policy. In `REMOTE_VERIFY`, use `record-rollback` to persist `rolled-back` or `rollback-failed`, observed recovery artifact, restored-health result, details, and provider/target evidence. Safe local and read-only diagnosis may continue.
- `failed-unchanged`, `rolled-back`, `rollback-failed`, and `blocked` are terminal for that attempt. A successful attempt may proceed only to remote verification or an authorized `record-rollback`; never reuse the same attempt for another deployment observation after a terminal outcome.
- Never let an older successful attempt hide the latest failed, partial, rolled-back, or unknown attempt.

Use the ledger's exact outcome values: `not_deployed`, `succeeded`, `failed-unchanged`, `failed-partial`, `rolled-back`, `rollback-failed`, `blocked`, or `unknown`. A failed, partial, rolled-back, rollback-failed, blocked, or unknown release can be fully reported but cannot be called a successful release.

## Post-deploy evidence

Evidence for a successful release must all bind to the gated deployment attempt and include:

- authorized immutable target identity;
- intended and observed artifact/build identity;
- health/readiness result;
- critical browser smoke and required class A/B results;
- closed-defect verification;
- relevant runtime signals;
- actual externally visible actions and counts;
- notification sink status and synthetic-data cleanup/leftovers;
- rollback readiness and rollback execution outcome as separate fields;
- remaining risk and untested production-only behavior.

The report preserves the complete post-deploy health history for the attempt, not only the latest value.

If the visible app does not expose build identity, use the provider deployment record, immutable image digest, or commit identifier and label any inference. Do not promise a flawless or defect-free production system; report only the bound evidence and declared coverage.
