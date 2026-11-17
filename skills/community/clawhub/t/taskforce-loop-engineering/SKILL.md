---
name: "taskforce-loop-engineering"
description: "Durable explicit task/project loops with verification, revisions, live progress, and governed completion."
---

# Taskforce Loop Engineering

Use this skill only when the user explicitly invokes Loop Engineering, says `走 loop`, `loop engineering`, `丢进 Ironman loop`, `loop Ironman`, `task-runner`, names a loop queue, or asks to operate an existing loop.

Do not route ordinary chat, research, explanations, or simple direct tasks into a loop unless the user explicitly invokes it.

## Distribution and CLI Installation

A skill installation may provide only this `SKILL.md`; it does **not** prove that the Loop Engineering CLI or an OpenClaw/Hermes integration is installed. Before running loop commands, check the deployment explicitly:

```bash
command -v loop-engineering
loop-engineering --help
```

Official distribution:

- npm package: `taskforce-loop-engineering`
- GitHub repository: `https://github.com/ambitioncn/taskforce-loop-engineering`
- ClawHub skill: `https://clawhub.ai/ambitioncn/skills/taskforce-loop-engineering`
- license: Apache-2.0
- runtime requirement: Node.js 22 or newer

Install the CLI globally from npm:

```bash
node --version
npm install -g taskforce-loop-engineering
loop-engineering --help
```

For a temporary read-only invocation without a global install:

```bash
npx -p taskforce-loop-engineering loop-engineering --help
```

For source-based development, clone the official repository and install its dependencies:

```bash
git clone https://github.com/ambitioncn/taskforce-loop-engineering.git
cd taskforce-loop-engineering
npm install
npm run check
node bin/loop-engineering.mjs --help
```

Do not guess a workspace source path. Use `node packages/loop-engineering/bin/loop-engineering.mjs ...` only after confirming that exact path exists in the current workspace.

### Verify the effective implementation

A skill update does not upgrade the CLI or generated integration. Before relying on scope inference, task-gate reconciliation or isolated verification, inspect the installed package and wrapper imports against the exact implementation that provides the feature. A candidate may share a version label with an older published package. Keep PR source, merged source, published packages, installed CLI and live integration as separate states; do not infer deployment from a green CI run.

### OpenClaw Integration

Installing the npm package exposes the CLI, but it does not automatically route conversations, select a worker agent, or create queue wrappers. First generate a read-only installation plan:

```bash
loop-engineering-openclaw-install \
  --root /path/to/openclaw/workspace \
  --queue agent-tasks
```

Review the installation confirmation summary before proceeding. It must show the target platform, absolute platform CLI path, workspace, queue, scheduler, notification routing, and `writes enabled: no (plan only)`. If any field identifies the wrong platform or destination, stop. Then install with an existing worker-agent id:

```bash
loop-engineering-openclaw-install \
  --root /path/to/openclaw/workspace \
  --queue agent-tasks \
  --worker-agent main \
  --confirm-install
```

The confirmed install also creates `loop-engineering-dashboard.service` on port `4174` and couples it to `openclaw-gateway.service`. Dashboard listening defaults to local-only `127.0.0.1`. To permit Tailnet clients, pass `--dashboard-listen tailscale`; the installer resolves `tailscale ip -4`, binds only that `100.x` address, and fails closed rather than binding all interfaces. Tailnet mode relies on Tailscale ACLs/Grants and does not add application-level login. The plan must declare the selected mode before writes, and the doctor must verify the Dashboard service and gateway drop-in. Use `loop-engineering-dashboard-autostart-install --listen localhost|tailscale` only for standalone install or repair.

The installer never creates the worker agent. After installation, verify wiring before using a real task:

```bash
loop-engineering-openclaw-doctor \
  --root /path/to/openclaw/workspace \
  --queue agent-tasks \
  --worker-agent main

loop-engineering-openclaw-smoke \
  --root /path/to/openclaw/workspace \
  --queue agent-tasks \
  --worker-agent main
```

If the CLI or integration is missing and the user requested installation or repair, install it within the authorized host/workspace scope, then run doctor and the disposable smoke. If the user only asked what is missing, report the exact package, repository, commands, and current deployment state without mutating the system.

### Multi-IM Diagnostic Acceptance

Before OpenClaw doctor/smoke, follow [the multi-IM diagnostic procedure](references/openclaw-diagnostics.md): select the correct CLI/profile, check installed capabilities, and discover actual channels/accounts rather than assuming Feishu. Doctor probes all matching accounts; smoke exercises one selected source per run. For multi-channel acceptance, explicitly test each required channel/account pair and record the coverage.

Notification probes are dry-run only, not evidence of real delivery or authenticated inbound approval support. Smoke still executes a real worker in a disposable queue. Updating this skill alone does not upgrade the installed CLI; the discovery/selection behavior requires package version 0.16.2 or newer; 0.16.1 does not include it.

### Hermes Agent Integration

The core CLI is platform-neutral, but Hermes conversation routing requires its own dispatcher and notifier. Generate a plan and verify its installation confirmation summary identifies Hermes, the absolute Hermes CLI path, intended workspace and queue, systemd scheduler, source-bound notification routing, and `writes enabled: no (plan only)`. If any field identifies the wrong platform or destination, stop. Confirm installation only after that review, then run the read-only doctor and disposable smoke:

```bash
loop-engineering-hermes-install \
  --root /path/to/hermes/workspace \
  --queue agent-tasks

loop-engineering-hermes-install \
  --root /path/to/hermes/workspace \
  --queue agent-tasks \
  --confirm-install

loop-engineering-hermes-doctor \
  --root /path/to/hermes/workspace \
  --queue agent-tasks

loop-engineering-hermes-smoke \
  --root /path/to/hermes/workspace \
  --queue agent-tasks
```

The confirmed Hermes install creates the same Dashboard service and couples it to `hermes-gateway.service`. It accepts `--dashboard-listen localhost|tailscale` with the same default-local, Tailnet-only binding, fail-closed resolution, and ACL/Grant boundary as OpenClaw. The plan and doctor must expose and verify this coupling.

The generated worker uses `hermes -z` (`--oneshot`); the notifier uses `hermes send` without
an LLM call. Preserve source metadata and pass `--source-target` in Hermes
`platform:chat_id[:thread_id]` format. The managed systemd scheduler owns wakeups
so durable queue continuity does not depend on resuming a Hermes Cron session.

## Cross-interface Human Gates

Dashboard and chat approvals use one Gate Command core and one authoritative gate artifact. Cards must show project/task, Gate ID, action, reason, impact, risk, cost/budget, evidence, Dashboard URL, expiry and generation; processed cards are refreshed disabled. Only card buttons or exact card-bound `/approve gate_<id>@<generation>`, `/reject gate_<id>@<generation>` and `/request_revision gate_<id>@<generation> <reason>` replies may mutate a gate. Ordinary chat, quotes, forwards, screenshots and ordinal phrases fail closed as `ignored_untrusted_chat`; `/show_gate gate_<id>` is display-only.

The OpenClaw installer generates `scripts/loops/openclaw-loop-gate.mjs`. A trusted Feishu callback/plugin transport must verify the official signature or encrypted-event envelope, timestamp/nonce and secret before invoking it with `LOOP_GATE_CHANNEL=feishu` and `LOOP_FEISHU_SIGNATURE_VERIFIED=1`; missing verification fails with `feishu_signature_unverified`. The bridge itself performs no delivery. Other channel transports pass normalized, source-bound events. Dashboard and chat commands share actor/source binding, generation fencing, idempotency receipts, confirmation escalation and synchronized card state.

After installation, run `loop-engineering-openclaw-doctor` and `loop-engineering-openclaw-smoke`. Doctor syntax-checks and locally self-tests the Gate bridge; smoke remains disposable and uses dry-run notifications. Neither command sends an online test message.

## Conversation Contract

Interpret explicit loop language as follows:

- `走 loop：<task>`: enqueue and immediately execute one runner tick with notification.
- `走 loop 并立刻执行`: synonym for the default above.
- `走 loop，只入队`, `只排队`, `暂不执行`, or `不立即执行`: enqueue without starting a tick.
- `继续当前 loop，补充要求：…`: amend the active task in place. Preserve the task id and worker session, write a versioned amendment, update the task contract/dev plan/acceptance plan, and require the worker to reread the latest amendment before checkpoints and completion.
- A new explicit `走 loop` request while another task is active is a correction/replacement, not ordinary backlog. Supersede the active task at a safe boundary, retain its evidence and lineage, then start the replacement after the lock is released.
- Status, progress, evidence, or failure questions are read-only and must not start another tick unless the user explicitly asks to continue/run.
- For status questions, read the latest checkpoint, verification result and worker liveness, then reply before doing further work. A failed check is a result to report, not authorization to edit files, rebuild images or rerun tests in the chat session. Send authorized follow-up execution to the task's independent worker session; never adopt its implementation into the conversation session.
- Conversation routing starts a background worker and returns a launch receipt; it must not await the full worker tick. A receipt proves process launch only, not lock acquisition, task execution, or acceptance. The background entry waits for a confirmed queue-lock conflict for up to five minutes by default; only exit code 2 with JSON status=locked and processed=false is retried. Read the launch log and queue state after timeout; do not start a duplicate worker from the chat. Keep scheduler/manual `run-once` execution synchronous and inspect its final artifacts separately.

Do not infer a queue or dispatcher from this skill. Use the integration installed in the current workspace. For OpenClaw, inspect the generated queue configuration under `configs/loops/queues/` and use the managed wrapper when present. A default installation uses queue `agent-tasks` and the generic wrapper below; an operator may choose another queue or worker during installation.

```bash
node scripts/loops/openclaw-loop.mjs route --message "<original user message>" [source options]
node scripts/loops/openclaw-loop.mjs run-once
loop-engineering queue-status --queue <installed-queue> --root . --json
loop-engineering queue-peek --queue <installed-queue> --root . --json
```

If the managed wrapper or queue configuration is absent, stop and run the platform installer/doctor workflow above. Product names, personal agent names, and host-specific dispatchers belong in local workspace instructions, never in this distributed skill.

Pass the original request faithfully. Preserve source channel, target, account, message id, and reply-to metadata so progress, human gates, and terminal results return to the originating conversation. Missing delivery routing must fail closed.

## Context Budget and Durable Handoff

For OpenClaw workers, follow `references/context-budget.md` before long-running work or recovery. Keep one bounded objective per turn, read bounded file ranges, and save checkpoints instead of replaying transcripts. Resolve paths against the resume manifest's workspace root; preserve authority, amendments, and action receipts across session rotation. A handoff is incomplete work, not acceptance. Verify the installed dispatcher and queue policy before claiming these protections are active.

## Task vs Project Classification

Classify scope before enqueueing. For scope inference, task-level gate reconciliation and effective acceptance reviews, follow [scope and task acceptance](references/scope-task-acceptance.md). Verify the generated contract against the original request; inference is heuristic, not authority.

### Scoped task

A bounded change, diagnosis, review, or deliverable with a clear local acceptance target can use one task contract.

### Project-level objective

Treat a request as project-level when the user asks to build/develop/finish a complete product or system, achieve an overall outcome, or otherwise describes a multi-milestone terminal goal.

For a project-level objective:

1. Run project intake and create a project spec.
2. Write an explicit terminal-state/completion contract.
3. Build a complete backlog covering every requirement and known acceptance dimension.
4. Link queue tasks to the project backlog and terminal contract.
5. Continue through implementation, verification, revisions, and the next actionable backlog item within the authorized safety boundary.
6. Stop only when total project acceptance passes, or a genuine human authorization/product decision/external-state blocker prevents meaningful progress.

For project continuations (explicit or inferred scope), preserve worker-authored plans and reread durable plans after dispatch. Progress means a committed milestone newly passes acceptance, including repairing an existing failed milestone; extra checkpoint files or re-emitting accepted milestones do not count. Accepted progress must match durable checkpoint/milestone identity even for a single planned milestone; changing only the plan ID cannot transfer old acceptance to new work. A no-progress continuation stops for revision instead of requeueing. Acceptance refresh re-evaluates changed plans and rebuilds legacy judgements missing coverage once.

Never silently narrow a complete-project request into “first milestone” and call that the Loop complete. A single queue task or milestone may be complete while the project remains active.

Recommended commands:

```bash
loop-engineering project-intake --root <workspace> --name <project> --brief "<full brief>" --type auto
loop-engineering project-plan --root <workspace> --project <project>
loop-engineering project-status --root <workspace> --project <project>
```

The project completion contract must contain:

- terminal user-visible outcome;
- in-scope and explicitly out-of-scope capabilities;
- complete requirement/backlog mapping;
- acceptance checks and evidence locations;
- operational/security/data/deployment requirements when relevant;
- unresolved decisions and required authority;
- a rule that milestone completion cannot satisfy project completion;
- final acceptance status with unmet items and blockers.

If implementation reveals missing work, amend the project backlog/contract before continuing. Do not redefine the terminal goal downward to fit completed work.

## Completion Semantics

Use precise language:

- `阶段完成` or `任务完成`: one task/milestone passed its own acceptance checks.
- `项目完成` or `Loop 跑完`: only when the project completion contract is fully accepted and no required work remains.
- `blocked`: only for a concrete blocker requiring human authority/input or an external state change, with evidence and a specific unblock request.
- `needs_revision`: acceptance found actionable gaps; create a changed-strategy revision rather than claiming completion.
- `superseded`: a newer explicit loop request replaced the task; preserve lineage and evidence.

Final reporting for project work must always state both task/milestone status and total-project status.

## Safety and Authority

Loop invocation authorizes the requested workflow, not unlimited external action.

Require separate explicit confirmation for:

- external messages, publication, social posting, or outreach;
- destructive deletion or difficult-to-recover changes;
- production configuration/deployment changes not already clearly requested;
- credential creation/change/exposure;
- paid model/API usage beyond an established budget;
- memory deletion or migration;
- device/process instrumentation such as `frida`, `tcpdump`, `adb`, `mitmproxy`, hooks, attach/spawn, decrypt, `su`, `kill`, or `pkill`.

Human permission prompts and missing authorization are stop conditions, not retryable failures. `INSTALL_FAILED_USER_RESTRICTED`, device unauthorized, permission denied, and equivalent states require a concrete human-action gate.

Timeouts must terminate the spawned process group. After instrumentation timeouts, verify that no child instrumentation/proxy process remains.

## Operating Flow

1. Read existing project docs, loop configs, queue state, and relevant dirty worktree state.
2. Classify task vs project and define the correct contract before execution.
3. Use `route-message` or the installed conversation wrapper to preserve source metadata and apply immediate/queue-only/amend/supersede semantics.
4. Run preflight before mutable work.
5. Execute one bounded tick or the project’s next actionable backlog item.
6. Emit ordered progress: planning, preflight, worker start, checkpoints, verification, acceptance, final judgement.
7. Inspect run artifacts; never infer success only from dispatcher exit code.
8. If acceptance fails, write a revision request with changed diagnosis/tactic/evidence/verification.
9. Run `doctor` after configuration or queue changes.
10. For projects, re-read project status and completion contract, then automatically advance to the next safe actionable item.
11. Report terminal status with evidence, unmet items, blockers, and next action.

Do not add cron/timers until one manual tick passes.

## Core CLI

Prefer the installed CLI:

```bash
loop-engineering verify --root <workspace>
loop-engineering doctor --root <workspace> [--json]
loop-engineering summarize --root <workspace> --limit 20
loop-engineering route-message --root <workspace> --message "<message>" --queue <queue> --route --confirm-execute [--supersede-active | --amend-active] [source options]
loop-engineering queue-status --root <workspace> --queue <queue>
loop-engineering queue-peek --root <workspace> --queue <queue>
loop-engineering run-queue --root <workspace> --config configs/loops/queues/<queue>.json
loop-engineering queue-revision-next --root <workspace> --queue <queue> --task-id <id>
loop-engineering queue-lineage --root <workspace> --queue <queue> --task-id <id>
loop-engineering queue-lineage-bundle --root <workspace> --queue <queue> --task-id <id>
loop-engineering queue-human-decision --root <workspace> --queue <queue> --task-id <id> --decision approve|request_changes|reject
loop-engineering queue-human-input-resolve --root <workspace> --queue <queue> --gate-id <task:checkpoint> --input "<response>" [--secret-input|--non-secret-input]
loop-engineering queue-terminal-notify --root <workspace> --queue <queue> (--notify-command "<command>" | --dry-run)
loop-engineering queue-human-input-notify --root <workspace> --queue <queue> (--notify-command "<command>" | --dry-run)
```

If the package is available only in the workspace:

```bash
node packages/loop-engineering/bin/loop-engineering.mjs <command>
```

Use `run-queue-drain` only when batch draining is explicitly intended. Conversation routing normally runs one task/tick and uses supersede/amend behavior.

## Revision Discipline

A dispatcher-successful run is not automatically accepted. Inspect `final_judgement.json`, acceptance reviews, checkpoints, and verification evidence.

When acceptance needs changes:

- mark `needs_revision`;
- retain the failed source task;
- use `queue-revision-next`;
- require a changed diagnosis, implementation tactic, evidence source, or verification step;
- inspect lineage before forcing repeated attempts.

Default revision policy may stop after three rounds, two repeated goal signatures, or repeated unchanged strategy. `--force` requires an explicit human override after lineage review.

## Code Work

For L2 code-changing tasks, prefer isolated worktrees. The runner prepares reviewable local changes and verification evidence; it does not implicitly commit, push, publish, deploy, merge, or delete branches.

Before enabling or diagnosing this backend, follow [frozen-input verification](references/frozen-input-verification.md) for prerequisites, receipt checks and compatibility boundaries.

For Linux code queues whose verification must not read the shared project tree, use the opt-in `worktree.isolatedVerification` backend described in [isolated verification](../../docs/isolated-verification.md). Declare the exact project inputs and any user-local runtime files before running the gate. Frozen project files preserve permission bits, which are included in input identity; mode-only changes invalidate stability. Failed undeclared file accesses remain failures from nested working directories even if the command swallows the error. Treat missing/failed receipts, undeclared reads (including probes through symlinks the command creates), changed input digests between commands, or unsupported host isolation as `verify_failed`; a zero command exit alone is not acceptance evidence. The sandbox holds no capabilities (under a root supervisor bwrap gets `--cap-drop ALL` and root-only `/etc` secrets are masked; prefer a non-root supervisor for full separation); read the failure `reason` in the verification artifact before retrying. This generic backend does not cover browser profiles, Docker/Git replay, networked checks, or undeclared dynamic dependencies. Keep those on a separately reviewed project-specific gate until explicitly enrolled and proven; do not silently fall back to ordinary `verifyCommands`.

Safe review flow:

```bash
loop-engineering code-task-status --root <workspace> --queue <queue>
loop-engineering code-worktree-inspect --root <workspace> --queue <queue> --task-id <id>
loop-engineering code-worktree-diff --root <workspace> --queue <queue> --task-id <id>
loop-engineering code-task-autoflow --root <workspace> --queue <queue> --task-id <id> --until closeout
loop-engineering code-patch-apply-plan --root <workspace> --patch <patch> --json
```

Applying a patch and cleaning a worktree require their explicit confirmation flags. Preserve unrelated user changes and never treat a dirty worktree as disposable.

## Observability and Artifacts

Use read-only diagnostics before mutation:

```bash
loop-engineering doctor --root <workspace> --json
loop-engineering summarize --root <workspace> --queue <queue> --limit 20
loop-engineering project-status --root <workspace> --project <project>
```

Task artifacts live under:

```text
runtime/loops/<queue>/tasks/<task_id>/
runtime/loops/<queue>/runs/
runtime/loops/<queue>/{inbox,active,done,failed,canceled}/
```

Expected evidence includes `task_contract.json`, `acceptance_plan.json`, `dev_plan.json`, checkpoints, acceptance reviews, `final_judgement.json`, revision requests, amendments, supersede markers, progress notifications, and lineage bundles.

Project artifacts live under:

```text
configs/loops/projects/<project>.json
runtime/loops/projects/<project>/
```

Summaries must cite the latest run/task/project evidence, verification performed, unmet checks, and blocker reason. Keep raw noisy logs in runtime artifacts; durable memory receives only distilled decisions, recurring failures, accepted safety rules, and verified completion facts.

## Scheduler Policy

Use scheduler ticks only after manual verification. Adaptive schedules may speed up with successful queued work and back off on empty queues, failures, long runs, or human gates.

`queue-scheduler-tick` is adaptive cadence logic, not a resident daemon. A cron, systemd timer, or equivalent external scheduler must wake it regularly. For project queues that promise automatic continuation, set `scheduler.required=true` and a bounded `scheduler.heartbeatMaxAge`; `doctor` must fail with `scheduler_missing` whenever queued work exists without a fresh scheduler heartbeat.

Progress notification must be scoped and idempotent. Report failures, human gates, status changes, and terminal completion promptly; throttle routine progress and idle updates.

## Final Checklist

Before saying a loop is finished, verify:

- Was this a scoped task or project-level objective?
- Is the correct contract present and current?
- Were all amendments applied?
- Did verification and acceptance pass?
- Is `final_judgement.json` acceptable?
- For a project, are all completion-contract items accepted and the backlog terminal?
- Are there any unmet requirements, pending revisions, gates, or external-write confirmations?
- Does the report distinguish milestone status from total-project status?
- Are evidence paths and next actions included?

If any project requirement remains, report a phase/task result and continue with the next authorized item; do not claim the project or Loop is complete.

### Invalid checkpoint baseline repair

Pre-dispatch review treats malformed JSON and non-object checkpoint roots as explicit invalid evidence, not empty accepted coverage. A bounded worker may repair the local record, but an unknown dispatch baseline is persisted as `invalid_checkpoint_baseline` and prevents automatic acceptance/continuation, including after acceptance refresh. Repair success is not proof of new milestone progress: use an explicit revision from validated history. Unrepaired invalid evidence cannot be superseded by a terminal snapshot. Human blockers take precedence; gate reconciliation leaves all gates unchanged while any checkpoint is invalid. Filesystem/permission failures are not classified as repairable JSON corruption. This conservative path may require an additional explicit revision even after a successful repair; it must not replay automatically.

### Normal context handoff versus runtime recovery

A valid successful handoff with nonempty, previously unseen checkpoint verification rotates the session without consuming or resetting runtimeRecoveryCount. Repeated verification (even with renamed checkpoints/new run IDs), empty verification and invalid handoffs stop, and consecutive handoffs stop at `retry.maxContextHandoffs` (default 10, reset when a milestone is accepted); unresolved authority or external outcomes remain human blockers and are copied into the final judgement and terminal notification. Exception recovery remains capped independently. Verification fingerprints are cooperative progress evidence, not independent semantic proof: final task acceptance is still required. Keep checkpoint verification concrete and tied to the completed unit. When hotfixing an installed runner under explicit authority, stage/test the narrow patch separately, back up originals, and note existing processes retain already imported modules.


### Explicit closure of unordered phase checkpoints

New checkpoints must carry stable `task_id`/`milestone_id`, a monotonic `sequence` and checkpoint-owned `created_at`; do not invent clocks for historical records. `revises_checkpoint_id` is lineage only, not proof that every older snapshot is resolved. A final accepted checkpoint can close unordered, status-only `in_progress` records with `revision_coverage`: one entry per old record containing `checkpoint_id`, SHA-256 of the exact checkpoint bytes in `checkpoint_sha256`, a concrete `resolution`, and nonempty `verification` strings also present in the final checkpoint's verification array. Same-task and same-planned-milestone identity must match. Preserve historical files.

Coverage cannot close real failed checks, missing evidence, corruption, duplicate identities, human blockers or deferred gates. A phase that itself declares revision coverage is not a plain status-only target: its invalid declaration cannot be laundered away by a later coverage edge. Invalid coverage remains a revision failure even if clocks otherwise order the records. Uncovered unordered history remains effective. Different explicit milestone identities never supersede each other by time alone; legacy unlabelled single-plan chronology remains supported. Evidence references are cooperative claims, not independent proof of test execution: review the actual artifacts before emitting final coverage.
