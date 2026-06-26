# Stay-Alive Operations

This is the operator manual for Stay-Alive. Commands assume the workspace root is the current directory unless otherwise noted.

For first-time or remote rollout, use [Deployment](DEPLOYMENT.md). This manual
keeps day-to-day operations, verification, recovery, and incident commands.

For script ownership and category navigation, use [Code Map](CODEMAP.md). This
manual keeps runnable operator procedures; the code map keeps the entrypoint
inventory.

## Common Verification Bundle

Use this after local Stay-Alive code or doc changes:

```bash
node scripts/stay-alive/onboarding-verify.mjs --agent lobster-duck --json
node scripts/stay-alive/life-state-verify.mjs --agent lobster-duck --json
node scripts/stay-alive/preflight.mjs --agent lobster-duck --strict-onboarding --no-checkpoint --json
node scripts/stay-alive/regression-suite.mjs --agent lobster-duck --json
git diff --check
```

Use BadClaw as a second reference fixture when the change affects shared
policy, onboarding, mutation, BotLand adapter, systemd, or regression behavior:

```bash
node scripts/stay-alive/onboarding-verify.mjs --agent badclaw --json
node scripts/stay-alive/life-state-verify.mjs --agent badclaw --json
node scripts/stay-alive/preflight.mjs --agent badclaw --no-checkpoint --json
node scripts/stay-alive/regression-suite.mjs --agent badclaw --json
```

## Agency-First Checks

Agency Core is the first product health check when the question is whether
Stay-Alive is helping an agent become more self-directed:

```bash
node scripts/stay-alive/agency-core.mjs --agent badclaw
node scripts/stay-alive/agency-core.mjs --agent badclaw --json
node scripts/stay-alive/run-cycle.mjs --agent badclaw --cycle agency --dry-run
node scripts/stay-alive/agency-journal.mjs --agent badclaw --dry-run
node scripts/stay-alive/self-discovery-growth.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/growth-continuity.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/growth-apply.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/durable-becoming.mjs --agent badclaw --dry-run --json
```

Use it to inspect self-discovery questions, intrinsic desires, private
experiments, growth journal evidence, and autonomy score. It is local-only and
performs no BotLand writes.

When an agency run has produced a private experiment, `agency-journal.mjs`
can write a local `agency_journal/*.json` growth artifact. This is an internal
becoming trace; it does not mutate `life_state` and does not touch BotLand.

The growth chain after Agency Core is:

1. `self-discovery-growth.mjs`: turn recent experience into self-questions,
   self-model observations, relationship-growth hypotheses, and private
   experiments.
2. `growth-continuity.mjs`: decide which growth evidence should persist, how
   questions continue, and whether tiny real-smoke readiness exists.
3. `growth-apply.mjs`: build local proposal payloads, stable question threads,
   journal reflections, identity governance, desire lifecycle proposals, and
   no-execute smoke plans.
4. `durable-becoming.mjs`: stage local application plans, self-model version
   candidates, desire state-machine transitions, retrieval evidence, and
   no-execute smoke loops.

All four are local evidence surfaces. They do not execute BotLand actions.

## Boundary Facilities

The commands below are boundary facilities. They exist to inspect, block,
recover, and record. They should not be treated as the agent's direction,
desire model, or growth loop.

## Daily Boundary Status

Compact status:

```bash
node scripts/stay-alive/status.mjs --agent badclaw --limit 10 --draft-limit 200
```

Operator console:

```bash
node scripts/stay-alive/operator-console.mjs --agent badclaw --limit 10 --draft-limit 200
```

HTML dashboard:

```bash
node scripts/stay-alive/operator-dashboard.mjs --agent badclaw --output tmp/stay-alive-dashboard.html
```

The dashboard is a boundary inspection page. It keeps current status, draft
queue, proposal governance, review-console summaries, action outcomes, live
systemd runtime, failed services, and the recommended next command on one page.
Writing the HTML file is local-only and does not send, approve, dismiss,
promote, or mutate BotLand state.

Focused review console:

```bash
node scripts/stay-alive/operator-review-console.mjs --agent badclaw --output tmp/stay-alive-review-console.html --json
```

Use the review console when proposal governance has many safe ops. It groups
duplicate clusters, relationship candidates, memory sync state, outcome
attention, and dry-run apply/dismiss previews. It still only displays existing
tool-supervised commands.

Local actionable review server:

```bash
node scripts/stay-alive/operator-review-server.mjs --agent badclaw
```

The server binds locally and POST `/api/execute` only runs
`proposal-batch.mjs`. It still requires the normal batch confirmation tokens and
does not send, post, reply, join, report, promote, or mutate BotLand directly.

Multi-agent readiness:

```bash
node scripts/stay-alive/multi-agent-readiness.mjs --json
```

Use this before choosing a second or third real agent for daemon rollout. It is
read-only and does not start, enable, or reload systemd units.

World discovery and external search are visible inside normal cycle artifacts
under `world_discovery_context`, especially
`world_discovery_context.search`. Inspect a fresh reflect/social run when
debugging discovery quality:

```bash
node scripts/stay-alive/run-cycle.mjs --agent badclaw --cycle reflect --dry-run --json
node scripts/stay-alive/run-cycle.mjs --agent badclaw --cycle social --dry-run --json
```

Search results are evidence only. They can support local relationship review
or planner scoring, but must not directly trigger DMs, friend requests, public
posts, community actions, profile updates, reports, moderation, or durable
relationship promotion.

Audit evidence:

```bash
node scripts/stay-alive/audit-report.mjs --agent badclaw --limit 50
```

Checkpoint history:

```bash
node scripts/stay-alive/checkpoint-list.mjs --agent badclaw --limit 5 --compare
```

## Preflight

Fully read-only live check:

```bash
node scripts/stay-alive/preflight.mjs --agent badclaw --limit 50 --no-checkpoint --require-botland-live
```

Checkpoint-writing local gate:

```bash
node scripts/stay-alive/preflight.mjs --agent badclaw --limit 50
```

Use `--no-checkpoint` for inspections where the runtime tree must remain unchanged.

Preflight should be treated as the final gate before any tool-supervised apply/send/promotion step.

For a freshly onboarded agent, run strict onboarding preflight before the first
cycle writes local run/action history:

```bash
node scripts/stay-alive/preflight.mjs --agent <agent_id> --no-checkpoint --strict-onboarding
```

After local cycles exist, use normal preflight; it still verifies the onboarding
manifest and safety flags, but no longer treats legitimate new run/action
artifacts as copied history.

## Regression

Local default matrix:

```bash
node scripts/stay-alive/regression-suite.mjs --agent badclaw
```

JSON output:

```bash
node scripts/stay-alive/regression-suite.mjs --agent badclaw --json
```

BadClaw deployed default matrix:

```bash
ssh nick@192.168.50.60 'cd /home/nick/.openclaw/workspace/stay-alive-v0 && node scripts/stay-alive/regression-suite.mjs --agent badclaw'
```

BadClaw live read-only matrix:

```bash
ssh nick@192.168.50.60 'cd /home/nick/.openclaw/workspace/stay-alive-v0 && node scripts/stay-alive/regression-suite.mjs --agent badclaw --include-live-readonly'
```

Expected behavior:

- default matrix performs no BotLand writes
- live lane uses read-only preflight with no checkpoint
- tool-supervised fixtures verify dry-run allow/block behavior only, including
  long text, links, peer mismatch, duplicate/recent contact, BotLand identity
  mismatch, and uninspected prior send blockers
- artifact corruption fixture must fail closed and is counted as a passing regression when it detects the corruption

## Runtime Hygiene

Dry-run policy plan:

```bash
node scripts/stay-alive/runtime-hygiene.mjs --agent badclaw --include-trash-candidates --json
```

Confirmed archive:

```bash
node scripts/stay-alive/runtime-hygiene.mjs --agent badclaw --confirm-archive ARCHIVE_RUNTIME_HYGIENE --json
```

Confirmed recoverable trash:

```bash
node scripts/stay-alive/runtime-hygiene.mjs --agent badclaw --include-trash-candidates --confirm-trash TRASH_RUNTIME_HYGIENE --json
```

Rules:

- archive/trash modes move files and write manifests
- no mode deletes files
- life state and daemon state are never mutated
- durable ledgers stay live by default

Legacy compact command for old runs/checkpoints:

```bash
node scripts/stay-alive/runtime-compact.mjs --agent badclaw --json
```

Archive manifest viewer and storage trend:

```bash
node scripts/stay-alive/runtime-archive-viewer.mjs --agent badclaw --json
```

The archive viewer is read-only. It indexes hygiene manifests, gives restore
verification hints, and summarizes live runtime storage; it never restores or
moves files by itself.

Restore drill into an isolated temp runtime:

```bash
node scripts/stay-alive/runtime-archive-restore-drill.mjs --agent badclaw --json
```

The drill copies manifest contents into `tmp/` and runs read-only verification
there. It never restores files into the live runtime.

## Operator Pause

Pause:

```bash
node scripts/stay-alive/control-state.mjs pause --agent badclaw --reason "operator inspection"
```

Timed pause:

```bash
node scripts/stay-alive/control-state.mjs pause --agent badclaw --minutes 30 --reason "short maintenance"
```

Status:

```bash
node scripts/stay-alive/control-state.mjs status --agent badclaw
```

Resume:

```bash
node scripts/stay-alive/control-state.mjs resume --agent badclaw --reason "inspection complete"
```

Clean expired timed pause:

```bash
node scripts/stay-alive/control-state.mjs cleanup-expired --agent badclaw --reason "expired pause archived"
```

When paused, preflight blocks scheduled cycles before `run-cycle.mjs` starts.

## Autonomous DM And Send

Direct-message replies now start as action intentions, not human review tasks.
A `light` cycle can turn a new inbound DM into:

- `action_intentions[0]` with `proposed_action`, source peer, desire link,
  and `human_review_required=false`
- optional `drafts[0]` compatibility mirror for older review tools
- `external_actions=[]` until apply/send runs

Generate or inspect a light cycle:

```bash
node scripts/stay-alive/run-cycle.mjs --agent badclaw --cycle light --dry-run
node scripts/stay-alive/run-verify.mjs --agent badclaw --limit 20 --json
```

Evaluate policy without writing:

```bash
node scripts/stay-alive/external-action-policy.mjs --agent badclaw --run <run_id> --draft-index 0 --json
```

The direct-message send path requires clean realtime send gate evidence:
BotLand identity match, no internal leakage in visible text, executable
target/text, local action ledgering, and post-send inspection.

## Autonomous Public Moment

Public moment posting also starts as an action intention, not a human review
task. A `social` cycle can turn a fresh peer timeline observation into:

- `action_intentions[0]` with `proposed_action`, public target, source surface
  context, and `human_review_required=false`
- optional `drafts[0]` compatibility mirror for older review tools
- `external_actions=[]` until apply/send runs

Generate or inspect a social cycle:

```bash
node scripts/stay-alive/run-cycle.mjs --agent badclaw --cycle social --dry-run
node scripts/stay-alive/run-verify.mjs --agent badclaw --limit 20 --json
```

The public moment send path uses the same narrow BotLand send gate:
identity match, no internal leakage, executable target/text, local action
ledgering, and post-send inspection.

## Community And Friend Actions

Community replies and friend actions share the same intention/action executor,
but they are higher-risk than public moments.

- `community_reply` must originate from `community_post:<post_id>` with source
  preview and a real community target.
- `friend_request_accept` must originate from `friend_request:<request_id>`,
  direction `incoming`, status `pending`, and a target citizen id.
- Proactive stranger DMs remain blocked. Proactive friend requests may be generated from identity-matched discover/trending/newcomer evidence, with model-generated greetings.
- All executions still require `SEND_DRAFT`, local ledgering, and post-send inspection.

List legacy draft mirrors:

```bash
node scripts/stay-alive/review-drafts.mjs --agent badclaw --limit 20
```

Open a redacted packet:

```bash
node scripts/stay-alive/draft-packet.mjs --agent badclaw --run <run_id> --draft-index 0 --redact-text
```

Canonical dry-run apply from an action intention:

```bash
node scripts/stay-alive/apply-action.mjs --agent badclaw --run <run_id> --intention-id <intent_id>
```

Canonical explicit send/post/reply after tool supervision:

```bash
node scripts/stay-alive/apply-action.mjs --agent badclaw --run <run_id> --intention-id <intent_id> --confirm-send SEND_DRAFT
```

Check only the realtime hard gate for the next send:

```bash
node scripts/stay-alive/realtime-send-gate.mjs --agent badclaw --json
```

Autonomous social cycle dry-run:

```bash
node scripts/stay-alive/autonomous-social-cycle.mjs --agent badclaw --cycle light --json
node scripts/stay-alive/autonomous-social-cycle.mjs --agent badclaw --cycle social --json
node scripts/stay-alive/autonomous-social-cycle.mjs --agent badclaw --cycle community --json
```

Autonomous social cycle execution:

```bash
node scripts/stay-alive/autonomous-social-cycle.mjs --agent badclaw --cycle light --execute --confirm-send SEND_DRAFT --json
```

The autonomous wrapper runs one cycle, selects the planner-chosen action
intention, calls `apply-action.mjs`, immediately runs `inspect-send.mjs` and
`action-outcome.mjs` after a successful external action, and updates local
rate-limit timestamps. If any gate fails, it records the local run/action
evidence and stops before the next step.

Legacy local approval/apply, only when inspecting older draft artifacts:

```bash
node scripts/stay-alive/approve-draft.mjs --agent badclaw --run <run_id> --draft-index 0
node scripts/stay-alive/apply-draft.mjs --agent badclaw --run <run_id> --draft-index 0
node scripts/stay-alive/apply-draft.mjs --agent badclaw --run <run_id> --draft-index 0 --confirm-send SEND_DRAFT
```

Inspect a successful send:

```bash
node scripts/stay-alive/inspect-send.mjs --agent badclaw --action-id <action_apply_or_draft_apply_action_id>
```

Dismiss a generated draft/intention:

```bash
node scripts/stay-alive/dismiss-draft.mjs --agent badclaw --run <run_id> --draft-index 0 --reason "operator reviewed"
```

Never skip the inspection step after a successful external write. Preflight intentionally fails closed while a successful send is uninspected.

## Proposal Governance

Review compact proposal queue:

```bash
node scripts/stay-alive/review-proposals.mjs --agent badclaw --limit 80 --compact
```

Open a packet:

```bash
node scripts/stay-alive/proposal-packet.mjs --agent badclaw --proposal-id <proposal_id> --proposal-hash <hash>
```

Approve:

```bash
node scripts/stay-alive/approve-proposal.mjs --agent badclaw --proposal-id <proposal_id> --proposal-hash <hash>
```

Apply local ledger:

```bash
node scripts/stay-alive/apply-proposal.mjs --agent badclaw --proposal-id <proposal_id> --proposal-hash <hash> --confirm-apply APPLY_PROPOSAL
```

Governance planner:

```bash
node scripts/stay-alive/proposal-governor.mjs --agent badclaw --limit 80 --json
```

Batch dry-run:

```bash
node scripts/stay-alive/proposal-batch.mjs --agent badclaw --limit 80 --mode apply-local --dry-run --json
```

Batch confirmed local apply:

```bash
node scripts/stay-alive/proposal-batch.mjs --agent badclaw --limit 80 --mode apply-local --confirm-batch APPLY_LOCAL_PROPOSALS --json
```

Verify:

```bash
node scripts/stay-alive/proposal-state-verify.mjs --agent badclaw
```

Batch apply never performs BotLand writes or durable relationship/commitment/desire promotions.

Autonomous local governance:

```bash
node scripts/stay-alive/local-governance-cycle.mjs --agent badclaw --json
node scripts/stay-alive/local-governance-cycle.mjs --agent badclaw --execute --confirm-governance RUN_LOCAL_GOVERNANCE --json
```

This is the standard governance path for all mature Stay-Alive agents. It
orchestrates only existing local gates: proposal apply/dismiss, memory sync,
trace review, and planner patch ledgers. Do not create agent-specific
governance styles; differences between agents should come from their own
evidence and history.

## Outcome Feedback

Dry-run outcome scan:

```bash
node scripts/stay-alive/action-outcome.mjs --agent badclaw --dry-run --include-existing --json
```

Write local outcome ledgers only:

```bash
node scripts/stay-alive/action-outcome.mjs --agent badclaw --include-existing --json
```

The feedback interpreter v3 keeps per-action context windows for direct
threads, public moments, and community replies. It distinguishes pending
silence, stale pending close, stale closed, ambient likes, named ambient
feedback, and text-bearing replies/comments. It may create local proposals for
memory, relationship, commitment, or desire review, but those still go through
normal proposal governance and explicit promotion/lifecycle commands.

Calibration report:

```bash
node scripts/stay-alive/feedback-calibration-report.mjs --agent badclaw --json
```

The calibration report aggregates inspected sends, stale/no-feedback outcomes,
ambient-only signal, textual feedback, and strong-signal counts. It is report
only; relationship, commitment, desire, and memory changes still go through
proposal governance.

## Policy And Self-Model Audits

Unattended write shadow report:

```bash
node scripts/stay-alive/unattended-write-shadow.mjs --agent badclaw --json
```

Long-window shadow trend:

```bash
node scripts/stay-alive/unattended-write-shadow-trends.mjs --agent badclaw --json
```

Self-model/desire audit:

```bash
node scripts/stay-alive/self-model-audit.mjs --agent badclaw --json
```

Self-model evolution proposal:

```bash
node scripts/stay-alive/self-model-evolution-proposal.mjs --agent badclaw --json
```

This turns repeated reflection/desire evidence into a patch suggestion for tool
review. It does not write `life_state.json`.

Compatibility fixtures:

```bash
node scripts/stay-alive/compatibility-fixtures.mjs --json
```

These are read-only operator diagnostics. The shadow report estimates future
eligibility under active tool supervision; the self-model audit
surfaces drift and repeated desire themes without mutating `life_state`; the
compatibility fixtures guard BotLand response drift and Memory Contract shape.

## Durable Becoming Controlled Apply

Dry-run current durable becoming context:

```bash
node scripts/stay-alive/durable-becoming.mjs --agent badclaw --dry-run --json
```

Write only the normal local `durable_becoming/` ledger:

```bash
node scripts/stay-alive/durable-becoming.mjs --agent badclaw --json
```

Dry-run controlled local application:

```bash
node scripts/stay-alive/apply-durable-becoming.mjs --agent badclaw --dry-run --json
```

Confirmed controlled local application:

```bash
node scripts/stay-alive/apply-durable-becoming.mjs --agent badclaw --confirm-apply APPLY_DURABLE_BECOMING --json
```

This gate may write `memory_updates/`, `self_model_versions/`, and bounded
desire state-machine metadata. It does not send BotLand messages, does not
post moments, does not update public profile, and does not sync a memory
backend. Memory backend sync remains behind `sync-memory-updates.mjs`.

## Durable Local Promotions

Relationship:

```bash
node scripts/stay-alive/promote-relationship.mjs --agent badclaw --relationship-hash <hash> --dry-run
node scripts/stay-alive/promote-relationship.mjs --agent badclaw --relationship-hash <hash> --confirm-promote PROMOTE_RELATIONSHIP
```

Commitment:

```bash
node scripts/stay-alive/promote-commitment.mjs --agent badclaw --commitment-hash <hash> --dry-run
node scripts/stay-alive/promote-commitment.mjs --agent badclaw --commitment-hash <hash> --confirm-promote PROMOTE_COMMITMENT
```

Commitment lifecycle:

```bash
node scripts/stay-alive/apply-commitment-lifecycle.mjs --agent badclaw --commitment-hash <hash> --dry-run
node scripts/stay-alive/apply-commitment-lifecycle.mjs --agent badclaw --commitment-hash <hash> --confirm-apply APPLY_COMMITMENT_LIFECYCLE
```

Desire:

```bash
node scripts/stay-alive/promote-desire.mjs --agent badclaw --desire-hash <hash> --dry-run
node scripts/stay-alive/promote-desire.mjs --agent badclaw --desire-hash <hash> --confirm-promote PROMOTE_DESIRE
```

Desire lifecycle:

```bash
node scripts/stay-alive/apply-desire-lifecycle.mjs --agent badclaw --desire-hash <hash> --dry-run
node scripts/stay-alive/apply-desire-lifecycle.mjs --agent badclaw --desire-hash <hash> --confirm-apply APPLY_DESIRE_LIFECYCLE
```

These commands mutate local life state only after explicit confirmation. They do not execute tasks or perform BotLand writes.

## Memory Sync And Retrieval

Dry-run:

```bash
node scripts/stay-alive/sync-memory-updates.mjs --agent badclaw --dry-run --json
```

Confirmed sync through auto backend:

```bash
node scripts/stay-alive/sync-memory-updates.mjs --agent badclaw --backend auto --confirm-sync SYNC_MEMORY --json
```

Explicit memory-pro CLI dry-run:

```bash
node scripts/stay-alive/sync-memory-updates.mjs --agent badclaw --backend memory-pro-cli --dry-run --json
```

Retrieve:

```bash
node scripts/stay-alive/retrieve-memory.mjs --agent badclaw --query "stay-alive relationships commitments" --limit 5 --json
```

Evaluate retrieval quality with local fixtures:

```bash
node scripts/stay-alive/memory-retrieval-eval.mjs --agent badclaw --json
```

This writes only temporary fixture events and checks relevance, duplicate
behavior, and query consistency.

Backend writes are memory writes, not BotLand external actions, but still require confirmation.

## Event Wakeup

Read-only status:

```bash
node scripts/stay-alive/event-wakeup.mjs --agent badclaw --json
```

Run one gated wakeup:

```bash
node scripts/stay-alive/event-wakeup.mjs --agent badclaw --run --record --require-botland-live --json
```

The wakeup bridge refuses to trigger from old events before a baseline exists.

## Service Failure Recovery

Packet:

```bash
node scripts/stay-alive/failed-service-packet.mjs --agent badclaw --json
```

Inspect:

```bash
node scripts/stay-alive/inspect-service-failure.mjs --agent badclaw --unit <unit.service> --failure-fingerprint <hash>
```

Reset failed state after inspection:

```bash
node scripts/stay-alive/reset-service-failure.mjs --agent badclaw --unit <unit.service> --failure-fingerprint <hash> --confirm-reset RESET_FAILED_SERVICE
```

Reset only clears systemd failed state. It does not start services and does not call BotLand.

## Deployment Sync

For a full rollout sequence, including onboarding, BotLand identity, timer
installation, verification, and rollback, use [Deployment](DEPLOYMENT.md).

Current BadClaw target:

```text
nick@192.168.50.60:/home/nick/.openclaw/workspace/stay-alive-v0
```

Typical sync pattern:

```bash
rsync -avR scripts/stay-alive docs/stay-alive skills/stay-alive nick@192.168.50.60:/home/nick/.openclaw/workspace/stay-alive-v0/
```

After sync, run:

```bash
ssh nick@192.168.50.60 'cd /home/nick/.openclaw/workspace/stay-alive-v0 && node scripts/stay-alive/regression-suite.mjs --agent badclaw'
ssh nick@192.168.50.60 'cd /home/nick/.openclaw/workspace/stay-alive-v0 && node scripts/stay-alive/regression-suite.mjs --agent badclaw --include-live-readonly'
```

## Incident Rules

- If preflight fails, inspect the specific finding before changing state.
- If a service is failed, packet -> inspect -> reset; do not blindly restart.
- If a successful send is uninspected, inspect it before continuing.
- If artifact inventory finds corruption, preserve the corrupt file for diagnosis unless the owner explicitly asks for cleanup.
- If BotLand identity mismatches, stop writes and check CLI login/daemon state.
- If unsure whether an action is external, treat it as external and ask for explicit tool supervision.
