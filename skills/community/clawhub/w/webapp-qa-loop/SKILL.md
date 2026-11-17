---
name: webapp-qa-loop
description: Drive an existing runnable web application through a real browser to find and evidence functional, interaction, and UI defects and, only when requested, repair them, validate changes, deploy to an authorized environment, and run post-deployment regression. Use for click-through QA, browser smoke or regression testing, deployed-version verification, release verification, and browser-based test-and-fix work. Do not use for static code review, API-, unit-, or automated-E2E-only testing, greenfield UI creation, screenshot-only critique, an explicitly pure UX or visual audit, native apps, dedicated security or load testing, or deployment without browser QA.
license: MIT-0
metadata:
  short-description: Browser QA, repair, deploy, and regression loop
  openclaw:
    homepage: https://github.com/liubai00/webapp-qa-loop
    requires:
      anyBins:
        - python
        - python3
---

# Webapp QA Loop

Run a browser-centered quality loop with explicit authority, durable evidence, bounded retries, and proportionate regression. Reduce interruptions by discovering facts, never by guessing permissions or external targets.

Use the user's language for progress updates, blocking questions, evidence summaries, and the final report unless the user requests another language. Keep ledger enum values, identifiers, command names, and command arguments unchanged.

## Read the relevant guidance

Resolve every path relative to this `SKILL.md`.

- Always read `references/scope-and-selection.md`, `references/browser-playbook.md`, and `references/issue-ledger.md`.
- In `repair` mode, read `references/repair-and-reuse.md` before editing.
- In `release` mode, always read `references/release-and-rollback.md`; if `repair_authorized=true`, also read `references/repair-and-reuse.md` before entering `REPAIR`.
- When creating or changing automated tests, also read `references/automation-promotion.md`.

Do not load guidance for a phase the task cannot enter.

## Establish authority and depth

Infer the least permissive mode that satisfies the request:

| User intent | Mode | Authorized work |
| --- | --- | --- |
| “测试一下”“检查页面”“找问题”; verify an already-deployed build/version | `audit` | Browse, exercise safe flows, capture evidence, and report. Do not edit source, commit, push, open a PR, or deploy. Deployed-version verification normally uses `release-regression` depth but remains an audit. |
| “测试并修复”“发现问题直接改” | `repair` | Everything in `audit`, plus edit source and tests and run local verification. Do not commit, push, open a PR, merge, or deploy unless separately authorized. |
| “部署/发布并回归” | `release` | Execute the explicitly authorized deployment path and post-deploy verification. Set `repair_authorized=true` only when the user also requested source repair; deployment alone does not authorize edits. |

Only initiating a deployment makes a run `release`. Testing a deployment someone else already performed is `audit` plus `release-regression`.

Treat commit, push, PR creation/update, merge, report upload/send, deployment, and rollback execution as distinct permissions. `DELIVER` is an optional externally visible handoff state for an explicitly authorized Git or report-delivery action; it is not implied by any mode and is not deployment.

Resolve depth in this order:

1. An explicit user depth or coverage request wins.
2. An actual release, deployed-version verification, or change with shared auth, navigation, state, schema, tokens, or infrastructure impact uses `release-regression`.
3. A named defect, page, journey, or recent change uses `targeted` unless a higher rule applies.
4. A vague broad request such as “smoke test it” uses `smoke`.

“End to end” for one named workflow means that workflow from entry through durable outcome; it does not imply whole-site or release regression. State the inferred mode, `repair_authorized` when relevant, depth, target, and exclusions in one short update.

## Non-negotiable authority boundary

Never infer authorization for:

- a production target or production access;
- real payment, purchase, refund, transfer, or irreversible deletion;
- sending real email, SMS, chat, push, invitations, or other notifications;
- changing real users, permissions, credentials, billing, subscriptions, or security settings;
- writing, migrating, rolling back, or cleaning production data or schema;
- bypassing MFA, CAPTCHA, authorization, rate limits, or platform safeguards;
- reading or exposing passwords, cookies, tokens, local storage, session stores, secrets, or unrelated personal data.

“全自动执行”, “别问”, “你决定”, and similar autonomy language authorizes uninterrupted work only inside permissions already granted. It does not supply a missing production target, Git, delivery, deployment, rollback, or high-side-effect permission.

Exact authorization identifies the environment and immutable target, action, affected object/account/recipient, amount or maximum count, expected external effect, cleanup or recovery plan, and one-run boundary. For production, the current task must explicitly name provider, account, project, environment, and region, even when only one target is configured, selected, or visible. Do not reuse a default, repository value, prior-task approval, or open browser as production authorization. When all applicable details are already explicit, do not ask again unless a material detail changes.

Synthetic writes and cleanup may proceed without another prompt only in a verified isolated non-production tenant, with bounded data created by this run, no real delivery or billing, and a reliable cleanup path. Production and shared environments are read-only by default. See `references/browser-playbook.md` for notification, OTP, MFA, and cleanup boundaries.

## Minimize questions through discovery

Before asking the user anything:

1. Read applicable `AGENTS.md` and repository instructions.
2. Inspect README files, manifests, task scripts, routes, tests, environment examples, compose files, and CI/deployment definitions.
3. Detect an already running local app and available browser session.
4. Infer critical journeys from routes, navigation, tests, domain names, and recent changes.
5. Reuse established start, test, build, and, in release mode only, deployment commands.

Ask one grouped set of blocking questions only when a material fact remains unavailable:

- no runnable URL or start path can be found;
- authentication requires user action, MFA, CAPTCHA, or unavailable credentials;
- plausible expected behaviors would lead to different fixes;
- a production target lacks current-task identity, or a release target remains ambiguous;
- a high-side-effect action is essential to the requested scope;
- a release or optional delivery needs ungranted authority.

An audit never asks for a release path or rollback authority. Continue independent work while waiting, and do not ask for preferences derivable from the design system, repository conventions, or objective accessibility rules.

## Select supporting capabilities deliberately

- Use browser control for real interaction and evidence. Prefer an existing browser only when its authorized authenticated state is required; otherwise use an isolated browser for public or local pages.
- For nontrivial cross-file repairs, use the repository-engineering workflow if available.
- For a hard or repeated defect, use a disciplined diagnosis workflow if available.
- Use a dedicated product-design audit only when the user explicitly requests UX/design critique.
- Keep one agent responsible for browser state and ledger transitions. Delegate only independent scans, tests, or root-cause investigations with non-overlapping write ownership.

## Create or resume a durable run

Use `scripts/qa_ledger.py` with an explicit `--run-dir` outside tracked source for every `repair` or `release` run and every nontrivial audit. An audit is nontrivial when it covers multiple routes or journeys, authenticated or state-changing behavior, `release-regression`, meaningful P0/P1 risk, or work that may pause, resume, or cross agents. A narrow read-only check of one public route can remain lightweight. Prefer a repository-defined untracked artifact location; otherwise use a discoverable project-keyed directory under the configured agent or skill-runtime home, not an anonymous OS temporary directory.

Treat the run directory as the stable recovery path and report its absolute location. At the start:

1. Before initializing, inspect the project-keyed QA-run location for an active ledger. If `qa-ledger.json` exists, run `validate`, then `summary`; reconcile the recorded target/build with reality and resume from the recorded state and next action.
2. Otherwise initialize schema v2 with mode, `repair_authorized`, depth, scope, and project, then declare each known target separately.
3. Declare each planned scenario and required check before recording its result. Bind results to the declaration so a late pass cannot hide an undeclared or newer failure.
4. For release, declare an immutable target and authorization source, configure the intended artifact and rollback readiness, then treat that target/artifact/policy as immutable for the run. Create the active attempt before its first release result, and bind every check, coverage result, and artifact observation to that same target/artifact/attempt.
5. Advance run state only with the ledger's state-transition command. Record a passing release gate before entering `DEPLOY`; the ledger rechecks its prerequisites and exact result snapshot at the deployment boundary.

Record issues, sanitized evidence references, root causes, repair attempts, checks, coverage, external effects, cleanup, release outcomes, and next actions as work progresses. Never store secrets or raw personal data. The ledger records facts; it does not execute commands, browse, deploy, or grant authority. See `references/issue-ledger.md` for the v2 contract and command examples.

## Follow the mode-aware paths

Use the applicable path; do not silently skip gates:

- `audit`: `INTAKE → DISCOVER → BASELINE → EXPLORE → TRIAGE → REPORT [→ DELIVER]`
- `repair`: `INTAKE → DISCOVER → BASELINE → EXPLORE → TRIAGE ↔ REPAIR ↔ LOCAL_VERIFY → REPORT [→ DELIVER]`
- `release`, `repair_authorized=true`: `INTAKE → DISCOVER → BASELINE → EXPLORE → TRIAGE ↔ REPAIR ↔ LOCAL_VERIFY → RELEASE_GATE → DEPLOY → REMOTE_VERIFY → REPORT [→ DELIVER]`
- `release`, `repair_authorized=false`: `INTAKE → DISCOVER → BASELINE → EXPLORE → TRIAGE → LOCAL_VERIFY → RELEASE_GATE → DEPLOY → REMOTE_VERIFY → REPORT [→ DELIVER]`
- One reconciled transient retry: after provider/target evidence changes an `unknown` outcome to `failed-unchanged`, use `DEPLOY → LOCAL_VERIFY → RELEASE_GATE → DEPLOY`; create exactly one retry attempt and rerun every bound result. Never retry an unknown/partial outcome or jump directly from a failed attempt to a new gate.

`DELIVER` is optional and requires its own authorization. Do not restart the entire tour after each small repair; loop only through the affected diagnosis, repair, and verification work.

### INTAKE and DISCOVER

Define the target, role, viewport, scope, exclusions, critical journeys, and automation. Define the release target, artifact, Git/delivery path, and rollback readiness only for a release run. Build one route/journey/impact map and reuse it.

### BASELINE

Run the cheapest relevant existing checks first: focused tests, lint, type checks, build, health checks, and browser smoke. Mark broad discovery suites optional; mark only known acceptance and release gates required. Separate pre-existing failures from run-introduced failures. If a required baseline is proven unrelated and pre-existing, record an evidenced `baseline-debt` disposition instead of changing the result or fixing unrelated code. A failing baseline is evidence, not permission to fix unrelated code.

### EXPLORE

Exercise declared journeys with semantic interactions and observable waits. Cover applicable scenario classes proportionately:

- A: critical happy paths and state-changing actions;
- B: likely validation, empty, error, permission, navigation, and refresh variants;
- C: lower-risk cosmetic or rare combinations.

Use pairwise coverage for cross-cutting role, viewport, locale, data, and network variables. Record passes, failures, blocks, and skips against declared scenario IDs. When evidence proves a declared scenario is not applicable to the tested role, flag, or target, use an evidenced `out` disposition; never turn an exclusion into a fake pass.

Every recorded browser `fail` must reference at least one confirmed issue and carry reproduction details/evidence. In repair/release runs, a failure linked to an in-scope issue prevents success even if an older pass exists. Record a verified issue's recurrence before taking further action: reopen and close it through a new local repair cycle, or during remote verification apply the authorized rollback/failed-settlement path. A later pass alone cannot erase the recurrence.

### TRIAGE

Confirm defects, remove environmental noise, group symptoms by probable root cause, and assign severity:

- `P0`: security, data loss/corruption, outage, or destructive uncontrolled behavior;
- `P1`: critical journey blocked or materially wrong with no reasonable workaround;
- `P2`: important defect with a workaround, significant accessibility problem, or recurring interaction failure;
- `P3`: minor behavior, visual consistency, or low-impact polish issue.

Prefer two reproductions or one reproduction plus deterministic console, network, DOM, or automated evidence. Record a P0 immediately and stop the unsafe mutation.

Severity and scope changes occur only in `TRIAGE` and require a reason plus evidence. Preserve the classification history; never silently downgrade or exclude a P0/P1 to pass a completion gate.

Once repair work has been recorded for an issue, its scope cannot be changed to `out`: the source change must be verified, or explicitly reverted and the run reported as failed/blocked before starting a clean run. Never use a late exclusion to hide unverified code.

### REPAIR

Fix root causes, not screenshots or symptoms. Search existing components, hooks, services, utilities, patterns, and tests before creating abstractions. Record `reuse`, `configure`, `extend`, `extract`, or `new` and the evidence for that choice. Do not add a dependency or shared pattern without concrete lifecycle or repeated-variation need.

### LOCAL_VERIFY

Use impact-based regression:

- R0: exact reproduction and acceptance condition;
- R1: immediate component, route, upstream input, and downstream result;
- R2: consumers of changed shared code and semantic variants;
- R3: critical journeys when auth, router, global state, schema, tokens, or infrastructure changed;
- R4: deployed identity, health, critical smoke, and closed-defect verification.

Run R0 and R1 for every repair. Add R2/R3 only when impact analysis requires them. A release with `repair_authorized=false` still runs the declared local or artifact-level pre-deploy checks before its release gate.

Record passing post-fix closure evidence only after the issue reaches `fixed`; a failing post-fix observation may be recorded against an active or completed repair cycle so failure is never lost. Each transition to `investigating` starts a new repair cycle whose repair/after evidence cannot be borrowed from an older cycle. If a verified issue needs another code change, reopen it as `investigating`. Every in-scope issue that received repair work, regardless of severity, must reach `verified`; a release re-runs every linked R0 and R1 declaration against the deployed target.

### RELEASE_GATE, DEPLOY, and REMOTE_VERIFY

These states occur only when this run executes a deployment. Follow `references/release-and-rollback.md`. The release gate requires evidenced bound local/artifact passes for every applicable required A/B scenario, passing required non-post-deploy checks, at least one required post-deploy health plan, and rollback readiness. It rejects every unresolved in-scope issue when repair is authorized; otherwise it rejects unresolved in-scope P0/P1. Deploy once per coherent verified batch. Verify target and artifact identity, every in-scope health plan, safe critical smoke, and every defect repaired by this run against the deployed environment. Any non-passing health result on the attempt blocks a successful release even if a later result passes. A timeout, unknown result, or partial deploy is reconciled against actual target state before any retry. Record an authorized remote rollback and restored artifact/health with `record-rollback` before reporting failure.

### REPORT and optional DELIVER

Lead with the outcome and include:

- mode, depth, environment, immutable target/build identity, and covered journeys;
- defects fixed, open, blocked, or excluded by severity;
- files and tests changed in repair/release mode;
- declared checks and browser scenarios with results;
- deployment outcome, external effects, cleanup status, and rollback readiness/execution when applicable;
- residual risks and precise untested scope;
- ledger path, settlement status, and next action.

Perform an optional authorized `DELIVER` action only after the report is ready. In `REPORT`, use `plan-delivery` to record each separately authorized action, authorization source, exact target, and idempotency key; only then enter `DELIVER`. After execution or reconciliation, use `record-delivery` to store outcome, external identifier, details, and evidence. On resume from a planned or unknown delivery, inspect external state before replaying it. `validate --strict` in `DELIVER` succeeds only when every planned action has a reconciled successful result. Never claim the whole application is defect-free, flawless, perfect, or exhaustively proven.

## Retry and stop rules

- If the same symptom survives two repairs without new evidence, stop patching and return to diagnosis.
- If three materially different hypotheses fail, settle the run as blocked and report the missing evidence or authority.
- Retry a confirmed transient deployment failure at most once per target/artifact. For timeout, unknown, or partial outcomes, record reconciliation on the same attempt; retry only after the current outcome is evidenced as `failed-unchanged`. A second failed attempt is reported, not retried.
- On production health degradation, unexpected mutation, auth anomaly, or rollback trigger, stop related production mutations and deploys. Continue safe local or read-only diagnosis. Execute rollback only under separate current or pre-granted conditional authorization; never automate data/schema rollback.

## Completion and settlement

Keep two outcomes distinct:

- **Run settlement:** the planned test work has been accounted for and reported as `succeeded`, `failed`, or `blocked`.
- **Product issue closure:** an individual issue is `verified`, `blocked`, or `wont-fix`; a terminal issue status does not by itself make the run successful.

An audit can settle successfully by delivering a complete evidence-backed findings report even when confirmed issues remain open. A repair or release can claim success only when all applicable conditions hold:

- every declared scenario and check has a current result tied to its declaration and target context;
- at least one applicable browser scenario was actually executed; excluding every browser path can never produce a successful browser-QA run;
- in `repair` and repair-authorized `release` runs, every confirmed in-scope issue is verified closed; in release-only runs, every in-scope P0/P1 is verified closed;
- in `repair`/`release`, all applicable class A and B scenarios pass; in `audit`, required and class A/B scenarios are actually executed as pass/fail and every failure is confirmed and evidenced; an evidenced `out` disposition remains visible but is not applicable;
- in repair/release, required tests/builds pass; in audit, required checks are actually executed as pass/fail and each failure is linked to a confirmed evidenced issue; blocked or skipped required checks prevent a successful audit settlement; an evidenced pre-existing `baseline-debt` disposition remains visible without invalidating the artifact;
- no new relevant console or network errors remain in covered flows;
- every repaired defect, including P2/P3, has current-cycle before/repair/after evidence and a fresh evidenced pass for every linked R0/R1 declaration; audit findings have reproducible before evidence;
- release evidence comes from the gated attempt for one authorized target and intended artifact, including identity, health, smoke, and rollback readiness;
- exclusions, cleanup leftovers, residual risks, and untested combinations are named.

If a required condition cannot be met, the run may be fully accounted for and reported, but its settlement is `blocked` or `failed`, not successful. Completeness means declared coverage is evidenced; it is never a promise of absolute quality.
