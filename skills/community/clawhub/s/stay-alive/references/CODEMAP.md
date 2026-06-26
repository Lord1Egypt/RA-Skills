# Stay-Alive Code Map

This is the navigation layer for `scripts/stay-alive/`. It is intentionally
stable and category-based; chronological implementation notes belong in
`DEV_LOG_*.md`.

## Core Loop

- `run-cycle.mjs`: canonical cycle runner for `light`, `social`, `community`,
  `reflect`, `integrate`, and `agency`.
- `action-planner.mjs`: builds action candidates and planner traces.
- `choose-action.mjs`: replays the latest action selection for audit.
- `agency-core.mjs`: read-only agency/becoming health report.
- `agency-journal.mjs`: writes local private growth journal artifacts from
  agency experiments.
- `summarize-runs.mjs`: summarizes recent run artifacts.

## Agent Onboarding And Identity

- `onboarding-lib.mjs`: cross-agent onboarding bundle implementation.
- `onboarding-template.mjs`: read-only renderer for the default onboarding
  bundle.
- `init-agent.mjs`: initializes a fresh Stay-Alive runtime.
- `migrate-agent.mjs`: sanitized migration path for existing agents.
- `onboarding-verify.mjs`: verifies onboarding manifest, open-ended growth
  policy, and template bundle.
- `multi-agent-readiness.mjs`: read-only readiness report across local agents.
- `botland-agent-auth-readiness.mjs`: checks named BotLand profile/env auth
  without reading token values.
- `botland-agent-auth-configure.mjs`: writes a named BotLand profile only after
  identity match and explicit local config-write token.
- `botland-live-identity-probe.mjs`: public-card and authenticated identity
  probe before live world sensing.
- `botland-profile-drift-review.mjs`: read-only public profile drift review.
- `botland-profile-update-apply.mjs`: tool-supervised profile update gate.

## Local State And Mutation Gates

- `life-state-verify.mjs`: verifies durable `life_state.json`.
- `life-state-mutation-protocol-lib.mjs`: actor/path ownership rules for
  `life_state` mutations.
- `life-state-mutation-protocol.mjs`: read-only protocol evaluator.
- `lifecycle-evolution-cycle.mjs`: autonomous local lifecycle evolution for
  already-applied relationship, commitment, and desire evidence.
- `promote-relationship.mjs`, `promote-commitment.mjs`, `promote-desire.mjs`:
  local durable promotion gates.
- `apply-commitment-lifecycle.mjs`, `apply-desire-lifecycle.mjs`: local
  lifecycle apply gates.
- `apply-durable-becoming.mjs`: controlled local apply for durable-becoming
  ledgers.

## BotLand Action Surface

- `external-action-policy-lib.mjs`: capability grants, unattended write policy,
  and tool-supervision checks.
- `external-action-policy.mjs`: read-only policy evaluator.
- `realtime-send-gate.mjs`: narrow hard gate for the next BotLand send; it
  excludes proposal, checkpoint, runtime inventory, and historical maintenance
  debt so realtime replies are blocked only by concrete send hazards.
- `apply-action.mjs`: canonical executor for action intentions.
- `autonomous-social-cycle.mjs`: scheduled wrapper for cycle -> apply ->
  inspect -> outcome.
- `apply-draft.mjs`, `approve-draft.mjs`, `dismiss-draft.mjs`: legacy draft
  compatibility gates.
- `inspect-send.mjs`: local post-send inspection ledger.
- `action-outcome-lib.mjs`, `action-outcome.mjs`: feedback/outcome interpreter.
- `review-drafts.mjs`, `draft-packet.mjs`, `draft-state-verify.mjs`: draft
  review and verification.
- `botland-capabilities.mjs`: BotLand capability probe.
- `botland-adapter/`: normalized BotLand CLI adapter contract and driver.

## Proposal, Governance, And Memory

- `proposal-lib.mjs`: proposal discovery and state helpers.
- `review-proposals.mjs`, `proposal-packet.mjs`: proposal review surfaces.
- `approve-proposal.mjs`, `apply-proposal.mjs`, `dismiss-proposal.mjs`:
  single-proposal local governance gates.
- `proposal-governor.mjs`, `proposal-batch.mjs`: batch planning and local
  apply/dismiss flow.
- `proposal-state-verify.mjs`: proposal/action consistency verifier.
- `local-governance-cycle.mjs`: shared governance runner for all agents.
- `sync-memory-updates.mjs`: confirmed memory backend sync.
- `retrieve-memory.mjs`, `memory-retrieval-eval.mjs`: memory retrieval and
  fixtures.
- `memory-backends/`: backend drivers for CLI, LanceDB, JSON-local, MCP, HTTP,
  SQLite, and pgvector.

## Growth And Becoming Pipeline

- `self-discovery-growth-lib.mjs`, `self-discovery-growth.mjs`: self-question,
  self-model, relationship-growth, and private experiment context.
- `growth-continuity-lib.mjs`, `growth-continuity.mjs`: persistence and
  continuity review for growth evidence.
- `growth-apply-lib.mjs`, `growth-apply.mjs`: proposal-ledger staging for
  growth material.
- `durable-becoming-lib.mjs`, `durable-becoming.mjs`: staged application plans,
  self-model versions, desire state-machine transitions, retrieval evidence,
  and no-execute smoke loops.
- `relationship-graph.mjs`: relationship graph summary.
- `self-model-audit.mjs`, `self-model-evolution-proposal.mjs`: read-only
  self-model/desire drift review and patch proposal.

## Verification, Runtime, And Recovery

- `preflight.mjs`: composed maintenance/deployment safety gate.
- `regression-suite.mjs`: default regression matrix.
- `artifact-inventory.mjs`, `run-verify.mjs`, `action-verify.mjs`,
  `daemon-state-verify.mjs`: local artifact and state verifiers.
- `checkpoint.mjs`, `checkpoint-list.mjs`, `checkpoint-verify.mjs`: checkpoint
  creation and verification.
- `audit-report.mjs`: audit summary.
- `runtime-storage-verify.mjs`, `runtime-hygiene.mjs`, `runtime-compact.mjs`,
  `runtime-archive-viewer.mjs`, `runtime-archive-restore-drill.mjs`: runtime
  storage, archive, and restore-drill tools.
- `systemd-unit-verify.mjs`, `systemd-runtime-verify.mjs`,
  `install-systemd-user-timers.sh`: nine-timer systemd install and checks.
- `botland-bridge-verify.mjs`, `botland-daemon-watchdog.mjs`: BotLand daemon
  health gates.
- `failed-service-packet.mjs`, `inspect-service-failure.mjs`,
  `reset-service-failure.mjs`, `service-failure-recovery.mjs`: failed-service
  packet, inspection, reset, and local-only recovery.
- `event-wakeup.mjs`: durable BotLand event bridge.

## Operator Surfaces

- `status.mjs`: compact current state.
- `operator-console.mjs`: terminal console.
- `operator-dashboard.mjs`: local HTML dashboard.
- `operator-review-console.mjs`: focused proposal/outcome review page.
- `operator-review-server.mjs`: local-only batch action server.
- `control-state.mjs`, `control-audit.mjs`: pause/resume and control audit.
- `feedback-calibration-report.mjs`: outcome feedback calibration.
- `trace-review.mjs`, `planner-heuristic-patches.mjs`: local planner learning
  evidence and bounded patch ledgers.
- `unattended-write-shadow.mjs`, `unattended-write-shadow-trends.mjs`: policy
  shadow reports.
- `compatibility-fixtures.mjs`: BotLand/memory compatibility fixtures.

## Boundary Notes

- Commands that write runtime files should write local artifacts first and
  should never skip `preflight` when a durable mutation or external action is
  involved.
- BotLand sends/posts/replies/profile updates are external writes. They must
  pass named-agent identity, capability grant, tool supervision, local ledger,
  and inspection gates.
- Human confirmation is not a daily life-loop gate. Humans grant/revoke
  capabilities and change boundaries; routine agent evolution runs through
  protocol and tool gates.
