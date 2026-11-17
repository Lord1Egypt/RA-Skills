# Issue Ledger

## Why the ledger exists

Use the schema v2 ledger to avoid rediscovering routes, repeating questions, losing evidence, mixing environments or artifacts, and claiming completion from stale success. The ledger is an execution record, not a replacement for tests, browser evidence, authorization, or the user-facing report.

## Stable recovery location

Use one explicit absolute run directory:

- Prefer a repository-defined untracked QA-artifact directory.
- Otherwise use `<configured-agent-home>/qa-runs/<stable-project-key>/<timestamp-task-slug>`. Derive the project key consistently from the canonical project root; before creating a run, inspect that project-key directory for a recent active ledger.
- Do not place it in tracked source or reuse an unrelated nonempty directory.
- Preserve it for the entire run and report its absolute path at every handoff.

The run directory is the stable recovery path. An anonymous OS temporary directory is not sufficiently discoverable after a task interruption. The helper writes the ledger and its own transient lock/temp files in the selected run directory; evidence may live in an established artifact location and be referenced by sanitized path. Never store secrets or raw personal data.

## Schema v2 invariants

The ledger enforces planning, identity, and state separately:

- Declare browser scenarios before execution with `declare-scenario`; use the returned `SCN-*` identity for every coverage result. Its initial `in` disposition is immutable, and every later exclusion is replayed from a continuous reasoned/evidenced history.
- Declare automated/operational checks before execution with `declare-check`; use the returned `PLN-*` identity for every check result. Mark each plan required or optional. `out` and `baseline-debt` dispositions use the same continuous history and cannot be introduced by directly editing current fields.
- Declare each environment with `declare-target`. A `TGT-*` record carries its environment, URL, production flag, and authorization source; it is not authorization by itself.
- Configure a release around one target, one intended immutable artifact, rollback readiness, rollback plan, and separate rollback-execution authority. The configuration is idempotent before the first attempt and immutable afterward; a different target, artifact, or policy starts a new run.
- After release configuration and no later than the first release result, create an `ATT-*` deployment attempt. It may be created from `BASELINE` through `RELEASE_GATE`. Release check and coverage results must bind to the current release `TGT-*`, intended artifact, and `ATT-*`; non-release results do not invent artifact/attempt bindings.
- Record the observed artifact for the attempt. It must reconcile with the intended artifact before a release can succeed.
- Advance run state only with `advance`. `update RUN` may update current target/URL, notes, or next action but cannot bypass the state machine.
- Record a passing `release-gate` only after every applicable required A/B scenario has an evidenced bound baseline/post-fix pass, every in-scope issue is verified when repair is authorized (otherwise every P0/P1 is verified), every in-scope required non-post-deploy plan passes, a required pre-deploy plan exists, at least one required post-deploy health plan exists, and rollback is ready. After deployment, every in-scope health plan must have an evidenced bound pass. `DEPLOY` re-evaluates both check and browser-coverage snapshots; a new declaration, result, or disposition requires a new gate.
- A newer failure, block, partial result, or unknown state cannot be masked by an older pass. Every historical browser failure remains linked to its confirmed issue and reproduction evidence. Issue severity and scope are replayed from an immutable creation-time classification plus the complete reasoned/evidenced change history, so direct edits cannot silently downgrade or exclude an issue. Linked R0/R1 declarations must each have a current evidenced pass after the issue was fixed.

Treat scenario/check declaration, target/artifact/attempt binding, state advance, and release gate as mandatory correctness boundaries rather than optional documentation.

## Command examples

Resolve `scripts/qa_ledger.py` relative to `SKILL.md`. Run top-level and subcommand `--help` before use; it is authoritative for exact arguments and enum values. The examples below show the v2 shape without inventing project-specific identities.

Initialize a release that may deploy but may not repair source:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> init --name "checkout release" --mode release --repair-authorized false --depth release-regression --scope "checkout" --project <project>
```

Declare the target, planned coverage, and a required check. Capture the generated IDs from command output:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> declare-target --name <target-name> --environment <environment> --url <url> --immutable-id <provider-account-project-environment-region-id> --production --authorization-source "current task: provider/account/project/environment/region"
python scripts/qa_ledger.py --run-dir <absolute-run-dir> declare-scenario --flow "checkout" --name "valid order" --risk-class A --target <TGT-id> --route "/checkout" --regression-level R4
python scripts/qa_ledger.py --run-dir <absolute-run-dir> declare-check --name "frontend build" --kind build --phase pre-deploy --environment <environment> --target <TGT-id> --required --regression-level R3
python scripts/qa_ledger.py --run-dir <absolute-run-dir> declare-check --name "readiness" --kind health --phase post-deploy --environment <environment> --target <TGT-id> --required --regression-level R4
```

Omit `--production` for non-production. Production still requires current-task authorization outside the ledger; `--authorization-source` records that evidence but does not create it.

Record a confirmed issue and typed evidence, then record a repair attempt through `update`:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add --title "Submit remains disabled" --area "checkout" --kind functional --severity P1 --step "Open checkout" --step "Complete required fields" --expected "Submit enables" --actual "Submit remains disabled" --before-evidence <sanitized-evidence-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> update <QA-id> --status investigating
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add-evidence <QA-id> --kind diagnosis --ref <sanitized-evidence-ref> --note "Validity omits address state"
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add-evidence <QA-id> --kind repair --ref <sanitized-diff-or-commit-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> update <QA-id> --status fixed --root-cause "Derived validity omitted address state" --approach extend --reused "existing form reducer" --resolution "Include address validity in the derived selector" --advance-iteration
```

The diagnosis command runs in `TRIAGE`; repair evidence and the transition to `fixed` run in `REPAIR`. Each transition to `investigating` starts a new repair cycle. In `LOCAL_VERIFY`, record current-cycle `after` evidence and a fresh evidenced result for every linked post-fix R0/R1 declaration before changing `fixed` to `verified`. To repair a verified issue again, first reopen it as `investigating`; old repair/after evidence cannot validate the new cycle.

Reclassify an issue only in `TRIAGE`, with reason and evidence; history remains visible:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> update <QA-id> --severity P2 --note <reason> --classification-evidence <sanitized-evidence-ref>
```

An issue can move out of scope only before repair evidence exists. Once source repair is recorded, it remains in the verification closure; do not use scope reclassification to discard an unverified change.

Record a scenario exclusion or a proven pre-existing baseline debt without changing its observed result:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> set-disposition <SCN-id> --status out --reason <why-not-applicable> --evidence <sanitized-evidence-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> set-disposition <baseline-PLN-id> --status baseline-debt --reason <why-pre-existing-and-unrelated> --evidence <sanitized-evidence-ref>
```

An `out` scenario/plan needs evidence that it is genuinely not applicable. `baseline-debt` is accepted only for a baseline plan with a current evidenced failure. Prefer broad baseline discovery plans as optional and reserve `required` for known acceptance/release gates.

For release, configure the immutable artifact and rollback policy, then create the attempt before the first bound release result. Create it as early as `BASELINE` when baseline results belong to the attempt, or by `LOCAL_VERIFY` when no earlier bound result exists. Pass the gate before advancing to deployment:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> configure-release --target <TGT-id> --intended-artifact <immutable-artifact-id> --rollback-readiness ready --rollback-plan <documented-plan> --rollback-recovery-artifact <immutable-known-good-artifact-id> --rollback-execution-authorized false
python scripts/qa_ledger.py --run-dir <absolute-run-dir> declare-attempt
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add-coverage --scenario <required-A-or-B-SCN-id> --phase baseline --result pass --target <TGT-id> --artifact <immutable-artifact-id> --attempt <ATT-id> --evidence <sanitized-browser-evidence-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add-check --plan <PLN-id> --result pass --target <TGT-id> --artifact <immutable-artifact-id> --attempt <ATT-id> --details <sanitized-result> --evidence <sanitized-report-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> advance RELEASE_GATE --next-action "Evaluate the bound release gate"
python scripts/qa_ledger.py --run-dir <absolute-run-dir> release-gate --attempt <ATT-id>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> advance DEPLOY --next-action "Deploy the gated artifact"
python scripts/qa_ledger.py --run-dir <absolute-run-dir> record-deployment --attempt <ATT-id> --result pass --observed-artifact <immutable-artifact-id> --evidence <provider-deployment-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> advance REMOTE_VERIFY
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add-check --plan <health-PLN-id> --result pass --target <TGT-id> --artifact <immutable-artifact-id> --attempt <ATT-id> --evidence <health-result-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> add-coverage --scenario <SCN-id> --phase post-deploy --result pass --target <TGT-id> --artifact <immutable-artifact-id> --attempt <ATT-id> --details <sanitized-result> --evidence <sanitized-browser-evidence-ref>
```

If rollback execution is already authorized, pass `--rollback-execution-authorized true` together with `--rollback-authorization-source <current-task-authority>`; readiness alone is never execution authority. For conditional authority, add each exact `--rollback-trigger`; `record-rollback` must later supply the matching `--trigger` and `--trigger-evidence`.

For one confirmed transient deployment retry, first record the observed non-passing outcome. An `unknown` or partial outcome cannot retry: reconcile provider and target state, then record `failed-unchanged` on the same attempt with new details/evidence. Only then advance `DEPLOY → LOCAL_VERIFY`, declare the single allowed retry attempt, and rerun all bound baseline/post-fix/pre-deploy results before a new gate. A second failed attempt is reported instead of retried. For an authorized rollback discovered during `REMOTE_VERIFY`, record the reconciled recovery state:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> record-rollback --attempt <ATT-id> --result rolled-back --observed-artifact <recovery-artifact-id> --health-result pass --details <sanitized-result> --evidence <provider-or-target-state-ref>
```

Result phases are chronological gates: baseline results are recorded during baseline/exploration/triage (and may be refreshed before a release gate), post-fix results only in `LOCAL_VERIFY`, pre-deploy results in `LOCAL_VERIFY` or `RELEASE_GATE`, and post-deploy results only in `REMOTE_VERIFY`.

Use `advance <STATE>` at every legal phase boundary rather than editing state through `update`. At pause or handoff:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> update RUN --current-target <TGT-id> --current-url <url> --next-action <durable-next-action>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> validate
python scripts/qa_ledger.py --run-dir <absolute-run-dir> summary --format markdown
```

At settlement, run:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> advance REPORT --settlement succeeded --next-action "Deliver the final report"
python scripts/qa_ledger.py --run-dir <absolute-run-dir> validate --strict
```

## Recording discipline

- Add an issue only after confirmation; keep uncertain observations in a scenario result or note until confirmed.
- Keep titles symptom-based and concise.
- Store evidence as sanitized references, not embedded secret-bearing payloads.
- Use typed evidence: `before`, `reproduction`, `diagnosis`, `repair`, and `after`.
- Set `run.next_action` whenever work pauses, crosses agents, or leaves a target in an uncertain state.
- Advance the issue iteration for each materially different repair attempt.
- Bind R0/R1 evidence to every repaired issue and declare higher regression levels when impact requires them.
- Every pass or fail used for a gate or closure carries a sanitized evidence reference; a bare status string is not proof.
- Record checks for tests, lint, typecheck, build, health, browser, deploy, and other operational gates through declared plans.
- Record browser passes, failures, blocks, and skips through declared scenarios, with reasons and issue links.
- Every browser `fail` references a confirmed `QA-*` issue and has details plus reproduction evidence; an in-scope linked failure prevents repair/release success until the issue is closed and the current result passes. Always record a verified issue's recurrence first so the evidence is durable. The ledger marks it as regressed and blocks repair/release success even if a later browser pass is added. In local work, reopen it as `investigating` and complete a new repair cycle; during remote verification, apply the authorized rollback or failed-settlement path instead of attempting an undeclared production hot fix.
- Record externally visible action counts, notification sink status, synthetic-data cleanup/leftovers, and release/rollback outcomes without sensitive payloads.
- Before an optional `DELIVER` action, use `plan-delivery` in `REPORT` for each separately authorized action. Enter `DELIVER`, perform or reconcile the action, then use `record-delivery`. If interrupted while planned or unknown, inspect external state before any replay. Delivery outcome history is chronological and replayed; succeeded, failed, and blocked are terminal, so a terminal action cannot be reset to unknown and executed again.

Example delivery handoff:

```text
python scripts/qa_ledger.py --run-dir <absolute-run-dir> plan-delivery --action report-send --target <exact-recipient-or-destination> --authorization-source <current-task-authority> --idempotency-key <stable-key> --details <planned-effect>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> advance DELIVER
python scripts/qa_ledger.py --run-dir <absolute-run-dir> record-delivery --delivery <DLV-id> --result succeeded --external-id <provider-or-git-id> --details <reconciled-outcome> --evidence <sanitized-provider-or-git-ref>
python scripts/qa_ledger.py --run-dir <absolute-run-dir> validate --strict
```

## Status and settlement meaning

Issue status and run settlement answer different questions:

- `open`: confirmed and not assigned a repair state.
- `investigating`: root-cause work is active.
- `fixed`: a change exists but required evidence is incomplete.
- `verified`: the repair and required local/remote evidence pass.
- `blocked`: unavailable authority, environment, data, or external change prevents progress.
- `wont-fix`: consciously closed without repair, with reason and impact.

`verified`, `blocked`, and `wont-fix` are closure states, but an issue may be explicitly reopened as `investigating`. Reopening invalidates its fixed/verified timestamps and requires a fresh repair and verification cycle. `blocked` and `wont-fix` do not mean the product behavior passed.

An audit may settle successfully after every declared item is accounted for, at least one applicable browser scenario was actually executed, no required/high-risk scenario or required check is blocked or skipped, and every browser/check failure is linked to a confirmed evidenced issue in the findings report; issues may remain open. A repair or repair-authorized release cannot settle as successful while any confirmed in-scope issue remains unverified. A release without repair authority must still verify every in-scope P0/P1 and cannot leave any repaired issue unverified. In repair/release runs, applicable class A/B failures or blocks also prevent success. Evidenced `out` and `baseline-debt` dispositions remain reported rather than being rewritten as passes. Such a run can still be fully reported and settled as failed or blocked.

## Resume protocol

When `qa-ledger.json` exists:

1. run `validate` without `--strict` to detect corruption, schema mismatch, invalid bindings, or illegal transitions;
2. run `summary --format markdown`;
3. inspect next action, current state, current target/URL, declaration dispositions and evidence, latest required-plan results, open in-scope issues, failed/blocked A/B coverage, release gate, latest attempt outcome/history, and any planned or unknown delivery;
4. compare the recorded target and intended/observed artifact with the actual environment;
5. if a browser mutation or deployment has an unknown/partial outcome, reconcile actual state before any replay or retry;
6. resume from the earliest incomplete legal gate.

Do not discard or reinitialize an existing run. A schema v1 ledger cannot satisfy v2 gates; follow the helper's migration/new-run guidance rather than editing JSON by hand or treating v1 strict validation as release proof.

## Completion validation

Use `validate --strict` at handoff. It checks mode-aware state completion, declaration dispositions/results, repair cycles, issue evidence, applicable issue-closure rules, class A/B gates, release/attempt/retry/rollback structure, target/artifact binding, deployment evidence, gate freshness, optional delivery authority/outcome, and cleanup settlement. Pending cleanup blocks success; residual cleanup must name the leftovers. A nonzero result means the run is not eligible for a success claim: continue safely or report the exact failed/blocked condition.

Strict validation makes the accounting conservative; it does not prove exhaustive testing or guarantee a defect-free product. The user-facing report must distinguish product defects, environmental blocks, baseline debt, deployment outcome, cleanup leftovers, and untested scope.
