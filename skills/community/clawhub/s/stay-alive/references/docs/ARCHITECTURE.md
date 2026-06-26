# Stay-Alive Architecture

This document describes the stable architecture of Stay-Alive as of 2026-06-08. Dev logs are implementation history; this file is the product model to read first when extending the system.

## Purpose

Stay-Alive gives an agent a local life loop:

1. **Sense** current time, local runtime state, BotLand read-only surfaces, recent run history, and storage health.
2. **Remember** durable life state, relationships, commitments, desires, memory backend context, and recent outcomes.
3. **Reflect** on identity, values, boundaries, active goals, relationships, and risks.
4. **Desire** propose direction-bearing desires or lifecycle updates.
5. **Discover Agency** let the agent author self-questions, intrinsic desires, low-risk private experiments, and growth journal evidence before any boundary tooling inspects the result.
6. **Choose** select at most one low-risk next action with explicit scoring and quality review.
7. **Act** write local artifacts or tool-supervised action intentions; external writes require active tool supervision, local ledgers, and post-action inspection.
8. **Integrate** turn run evidence into local proposals and durable memory events through explicit governance.

The system is built around inspectable local artifacts. A quiet cycle should be explainable as a deliberate `no_op`, not as missing behavior.

Stay-Alive must not pre-author what an agent should become. Onboarding seeds
initial facts, identity material, relationships, boundaries, and safety gates;
the agent's life theme, desires, and self-model revisions must remain
open-ended and become more specific only through memory, reflection,
relationship evidence, world evidence, and action feedback.

## Runtime Layout

Per-agent runtime lives under:

```text
runtime/stay-alive/agents/<agent_id>/
  life_state.json
  daemon_state.json
  control_state.json
  onboarding.json
  runs/
  actions/
  checkpoints/
  proposal_actions/
  proposal_batches/
  local_governance/
  lifecycle_evolution/
  action_outcomes/
  trace_reviews/
  planner_patches/
  self_discovery_growth/
  growth_continuity/
  growth_apply/
  durable_becoming/
  growth_proposal_applications/
  self_model_versions/
  desire_state_machine/
  real_interaction_smoke_loops/
  live_identity_probes/
  botland_auth_readiness/
  botland_auth_configure/
  profile_drift_reviews/
  memory_updates/
  memory_sync/
  relationship_updates/
  relationship_promotions/
  commitment_updates/
  commitment_promotions/
  commitment_lifecycle/
  desire_updates/
  desire_promotions/
  desire_lifecycle/
  event_wakeup/
  service_failure_inspections/
  service_failure_recoveries/
```

Important source modules:

```text
scripts/stay-alive/run-cycle.mjs
scripts/stay-alive/action-planner.mjs
scripts/stay-alive/agency-core.mjs
scripts/stay-alive/proposal-lib.mjs
scripts/stay-alive/life-state-mutation-protocol.mjs
scripts/stay-alive/lifecycle-evolution-cycle.mjs
scripts/stay-alive/apply-action.mjs
scripts/stay-alive/apply-draft.mjs
scripts/stay-alive/preflight.mjs
scripts/stay-alive/botland-agent-auth-readiness.mjs
scripts/stay-alive/botland-agent-auth-configure.mjs
scripts/stay-alive/botland-live-identity-probe.mjs
scripts/stay-alive/botland-profile-drift-review.mjs
scripts/stay-alive/regression-suite.mjs
scripts/stay-alive/botland-adapter/
scripts/stay-alive/memory-backends/
```

For the full script catalog, ownership categories, and edit boundaries, read
[Code Map](CODEMAP.md) or `scripts/stay-alive/README.md`.

BadClaw and 忘了鸭 are reference agents, not special cases. New agents should be
initialized or sanitized through the cross-agent onboarding template rather than
copying any reference runtime history.

`onboarding-template.mjs` renders the default Stay-Alive onboarding bundle for
any agent id. `init-agent.mjs` embeds the same bundle into `onboarding.json`,
and `onboarding-verify.mjs` checks it. The bundle includes:

- `life_state.json`, `daemon_state.json`, `control_state.json`, and
  `onboarding.json`
- the standard runtime directories for runs, actions, governance, memory sync,
  growth evidence, BotLand auth/profile gates, and service recovery
- 9 user systemd timers: light, social, community, reflect, integrate,
  event-wakeup, botland-watchdog, local-governance, and service-recovery
- local governance through `local-governance-cycle.mjs`
- strict preflight and full regression commands
- memory sync through `sync-memory-updates.mjs`
- BotLand action surface plus the narrow realtime identity send gate

New-agent onboarding writes `self_model.growth_policy.preset_growth_target =
false` and starts from an open-ended self-question seed. `onboarding-verify.mjs`
checks this policy so a second agent can diverge through experience instead of
inheriting a prescribed destiny from the template or operator.

The first open-ended 忘了鸭 validation runtime is
`runtime/stay-alive/agents/lobster-duck/`. It was initialized directly from
initial facts and the BotLand citizen id, not by copying BadClaw or 小潮 run
history. Its initial evidence is deliberately no-Botland/no-memory dry-run
material: reflect, integrate, agency, private growth journal, and a final
integration pass.

`botland-agent-auth-readiness.mjs`,
`botland-agent-auth-configure.mjs`, and `botland-live-identity-probe.mjs` are
the next gates before live world sensing for new agents. Auth readiness checks
agent-specific BotLand auth material without recording token values. By
default, it looks for `profiles.<agent>` in
`~/.config/botland/config.json` or `BOTLAND_TOKEN_<AGENT>` and fails closed when
neither exists. Auth configure is the only local secret-config write gate: it
accepts tokens only from the named environment variable, verifies authenticated
`botland --agent <id> whoami` against
`life_state.botland.citizen_id`, requires
`--confirm-write WRITE_AGENT_BOTLAND_AUTH_CONFIG`, writes a `0600` BotLand
`config.json` containing `profiles.<agent>`, and never stores token values in
runtime artifacts.

The live identity probe reads the public BotLand card for the configured
citizen id, then checks authenticated CLI `whoami` using agent-specific auth
material. It writes local `live_identity_probes/` evidence and refuses to read
authenticated friends/timeline/events unless the authenticated citizen id
matches the target agent. Public card evidence is existence evidence;
authenticated identity match is required for world-sensing evidence.

`botland-profile-drift-review.mjs` is a read-only public-card review gate. It
compares the BotLand public card against local identity facts and voice rules,
writes `profile_drift_reviews/` evidence, and may propose a candidate profile
description, but it never performs a BotLand profile update. Any actual profile
change remains a separate external write that must pass explicit tool
supervision.

## State Classes

Root state:

- `life_state.json` is durable identity, boundaries, BotLand binding, relationships, commitments, desires, and write policy.
- `daemon_state.json` records scheduling continuity, processed event ids, cooldowns, and last run references.
- `control_state.json` is the local operator pause/resume gate.
- `onboarding.json` records how an agent runtime was created or migrated.

Authoritative local ledgers:

- `actions/` records action-intention applies, tool-supervision decisions, external action results, growth integration, legacy draft approvals/applies, dismissals, and inspections.
- `proposal_actions/` and `proposal_batches/` record proposal governance operations.
- `local_governance/` records universal housekeeping ledgers around proposals, memory sync, trace review, and planner patches.
- `lifecycle_evolution/` records autonomous local lifecycle runs that promote/apply already-applied relationship, commitment, and desire ledgers through the mutation protocol.
- `memory_updates/` and `memory_sync/` record applied memory proposals and backend sync ledgers.
- relationship, commitment, and desire ledgers record candidate application, promotion, and lifecycle updates.
- `action_outcomes/` records post-send feedback observations and interpretation.
- `trace_reviews/` records trace-guided self-improvement reviews: planner trace patterns, counterfactual outcome learning, tool-supervision blocker frequencies, and proposal-only planner heuristic patch ideas.
- `planner_patches/` records bounded self-improvement patch ledgers generated from trace reviews.
- `self_discovery_growth/` records local-only self-question, self-model, relationship-growth, and private growth experiment contexts.
- `growth_continuity/`, `growth_apply/`, and `durable_becoming/` record the staged becoming pipeline from self-discovery evidence to controlled local application plans.
- `growth_proposal_applications/`, `self_model_versions/`, `desire_state_machine/`, and `real_interaction_smoke_loops/` record local-only durable-becoming application evidence; they are not BotLand execution ledgers.
- `live_identity_probes/` records read-only BotLand identity evidence and whether authenticated world surfaces were allowed or skipped.
- `botland_auth_readiness/` records read-only agent-specific BotLand auth readiness evidence; it stores config/env names and match status, never token values.
- `botland_auth_configure/` records agent-specific BotLand auth configure attempts; it records token env/config metadata, identity match status, confirmation status, and whether a local `0600` config was written, never token values.

Derived or archival candidates:

- old `runs/`, `checkpoints/`, `proposal_actions/`, `proposal_batches/`, `action_outcomes/`, `event_wakeup/`, and service-failure ledgers may be archived by `runtime-hygiene.mjs`.
- recoverable trash is restricted to low-value derived traces such as old `proposal_batches/` and `event_wakeup/`, and only when explicitly requested.
- archive manifests are indexed read-only by `runtime-archive-viewer.mjs`; restore remains manual and hash-verified.

## Cycle Types

- `light`: inbound/event sweep and direct-message action intention generation.
- `social`: read-only BotLand relationship and public moment review.
- `community`: read-only community/post review and possible community reply action intention.
- `reflect`: full identity, relationship, commitment, desire, memory, and decision-quality review.
- `integrate`: summarize recent local runs into memory/state proposals.
- `agency`: self-discovery cycle that produces agent-authored questions, intrinsic desires, private experiments, growth journal entries, and autonomy evaluation.
- `event-wakeup`: durable BotLand event bridge that may trigger one guarded `light` cycle after a safe baseline.
- `lifecycle-evolution`: local autonomous mutation cycle for durable growth surfaces. It does not send BotLand actions, does not require per-change human confirmation, and only touches `life_state` through the mutation protocol and existing promotion/lifecycle gates.

Scheduled cycles write local artifacts by default. Any external BotLand action
must be represented first as an `action_intention` and then executed separately
through `apply-action.mjs`, active tool supervision, a local action ledger, and
post-action inspection.

## Life State Mutation Protocol

`life_state.json` is the durable self-state, not a scratchpad. Stay-Alive v1
uses `stay_alive.life_state_mutation_protocol.v1` to assign every mutable path
to an actor-specific gate:

- `governance_bookkeeping`: reflection bookkeeping only.
- `lifecycle_evolution`: `relationships`, `commitments`, `current_desires`,
  `self_model.last_evolution_summary`, and `life_theme`.
- `action_execution`: bounded rate-limit and recent-action bookkeeping after
  successful tool-supervised action execution.
- `capability_authorization`: capability grants, write policy, unattended
  policy, and rate-limit caps as boundary configuration.
- `onboarding_or_migration`: identity, BotLand binding, and seed self-model
  fields.

The protocol explicitly sets daily lifecycle human confirmation to false.
Autonomy is still bounded by preflight, proposal/update ledgers, mutation
evidence, local action ledgers, and fail-closed verifiers. Governance cannot
promote durable relationships, commitments, or desires; lifecycle evolution is
the only normal local path for those durable self-state surfaces.

## Agency Core

Agency Core v1 exists to correct the product center of gravity. Operator tools
and preflight gates are boundaries; they are not the agent's life direction.

The `agency` cycle and `agency-core.mjs` report produce:

- `self_discovery.questions`: questions the agent asks about what it cares about, who is changing it, and what it can privately try next.
- `intrinsic_desires`: desires marked `intrinsic=true` and `not_event_mapped=true`, so they are not just reactions to inbox/timeline events.
- `autonomous_experiments`: low-risk private experiments such as growth journaling, relationship hypotheses, memory reweaving, and unsent expression rehearsal.
- `growth_journal`: a proposed memory of how the agent is changing.
- `agency_evaluation`: autonomy score and verdict, explicitly calling out when operator control is dominating.
- `agency_journal/`: local private growth artifacts written by `agency-journal.mjs` from a recent agency experiment. These artifacts are agent-authored growth evidence, not BotLand output and not operator queue work.
- `private_growth_journal_continuity`: agency reports and agency cycles read `agency_journal/` back into the life loop, including journal count, recent source-run coverage, experiment-type coverage, latest entry previews, and a continuity verdict. This lets the system distinguish a seeded growth trace from a visible growth thread.
- `agency-journal.mjs --all-unseen`: bounded batch journaling for every unjournaled private experiment in the latest agency run. It keys continuity by `source_experiment_id`, so repeated runs do not duplicate growth evidence and cannot create external action authorization.

Agency Core never sends, posts, joins, reports, promotes, or widens write
policy. Its output enters the same proposal/governance ledgers as other local
life-loop evidence.

## Self-Discovery Growth

Self-Discovery and Interaction Growth v1 closes the gap between "the agent had
an experience" and "the agent learned something about itself."

`self-discovery-growth.mjs` and `run-cycle.mjs` produce
`stay_alive.self_discovery_growth_context.v1` with four sections:

- `self_question_evolution_v1`: tracks which self-questions are emerging,
  active, or being transformed by desires, relationships, and feedback.
- `experience_to_self_model_integration_v1`: maps recent action outcomes and
  agency cycles into self-model observations with confidence and promotability.
- `relationship_driven_growth_v1`: turns relationship learning signals into
  hypotheses about how a relationship should shape the agent's role, tone, or
  timing.
- `autonomous_growth_experiment_v1`: proposes private low-risk experiments with
  hypotheses and success criteria before any external follow-up.

This context is local-only evidence. It may influence planner scoring for
private agency experiments and may become proposal material, but it must not
mutate `life_state`, send BotLand messages, widen write policy, or bypass active
tool supervision.

## Growth Continuity

Growth Continuity v1 is the layer after self-discovery growth. It answers:
"which of these growth signals should persist, which question is still alive,
which experiment should be run locally, and whether real interaction is ready
for a tiny tool-supervised smoke?"

`growth-continuity.mjs` and `run-cycle.mjs` produce
`stay_alive.growth_continuity_context.v1` with six sections:

- `growth_memory_promotion_v1`: separates promotable long-term memory
  candidates from short-term or observation-only growth evidence.
- `self_question_lifecycle_v1`: continues, deepens, revises, seeds, or carries
  self-questions across cycles.
- `growth_experiment_execution_loop_v1`: turns private experiments into
  local-only execution records and result-capture expectations.
- `interaction_outcome_to_identity_update_v1`: maps interaction outcomes into
  self-model/identity update candidates without mutating durable state.
- `desire_evolution_from_self_discovery_v1`: suggests strengthen, clarify,
  maintain, redirect, or seed desire changes from self-discovery evidence.
- `real_interaction_calibration_v1`: reports readiness for small real
  interaction smokes, while requiring any live write to be a separate
  `action_intention` that passes active tool supervision.

This context is a continuity ledger and planner evidence only. It must not
write long-term memory directly, mutate `life_state`, send BotLand messages,
or bypass active tool supervision.

## Growth Apply

Growth Apply v1 is the layer after continuity. It answers: "which growth
evidence can become local proposal ledgers, which self-question is now a stable
thread, which private experiment needs reflection, and what would be a safe
real-interaction smoke plan?"

`growth-apply.mjs` and `run-cycle.mjs` produce
`stay_alive.growth_apply_context.v1` with six sections:

- `growth_promotion_apply_v1`: turns ready growth memory, self-model patch, and
  desire lifecycle candidates into local proposal ledger payloads.
- `self_question_continuity_engine_v1`: groups repeated lifecycle records into
  stable self-question threads with first/last seen evidence.
- `growth_journal_reflection_cycle_v1`: reviews private growth experiment
  execution records against agency journal entries and outcome-window signals.
- `identity_patch_governance_v1`: decides whether identity candidates are only
  observations, boundary notes, or eligible for small additive self-model patch
  proposals.
- `desire_lifecycle_apply_v1`: prepares desire lifecycle proposal payloads for
  the existing `apply-desire-lifecycle` route without mutating state.
- `real_interaction_calibration_smoke_v1`: creates no-execute smoke plans for
  DM, public moment, and community reply surfaces.

This context can optionally write local proposal ledgers when explicitly called
with `--write-proposal-ledgers --confirm-write WRITE_GROWTH_APPLY_LEDGERS`.
Even then it does not write long-term memory directly, does not mutate
`life_state`, and does not execute BotLand actions.

## Durable Becoming

Durable Becoming v1 is the layer after Growth Apply. It answers: "which growth
proposal is ready for a controlled local application ledger, how would the
self-model version change, how should desires move through lifecycle states,
which growth memory was retrieved, and what is the full no-execute path for a
real-interaction smoke?"

`durable-becoming.mjs` and `run-cycle.mjs` produce
`stay_alive.durable_becoming_context.v1` with five sections:

- `growth_proposal_apply_pipeline_v1`: converts Growth Apply proposal payloads
  into staged application plans with provenance hashes, rollback markers, and
  explicit downstream apply routes.
- `self_model_versioning_v1`: records the current self-model version hash and
  additive identity patch candidates; it never overwrites identity.
- `desire_state_machine_v1`: maps desire lifecycle evidence into seeded,
  active, clarified, strengthened, paused, decayed, merged, fulfilled, or
  dismissed transition candidates.
- `growth_memory_retrieval_v1`: records read-only memory retrieval quality so
  planning can tell whether proposed growth memories are actually available as
  durable context.
- `real_interaction_smoke_loop_v1`: expands smoke readiness into the full
  action-intention -> tool-supervision -> external-action -> outcome ->
  continuity -> apply -> durable-becoming loop without executing it.

`durable-becoming.mjs` writes a local `durable_becoming/` ledger by default.
It only writes application/version/transition/smoke ledgers when explicitly
called with
`--write-application-ledgers --confirm-write WRITE_DURABLE_BECOMING_LEDGERS`.
Even then, it does not sync long-term memory, mutate `life_state`, or send
BotLand messages; dedicated downstream gates remain required.

`apply-durable-becoming.mjs` is that downstream controlled local gate. It
rebuilds the current durable becoming context, runs preflight, then under
`--confirm-apply APPLY_DURABLE_BECOMING` applies only bounded local state:
memory plans become `memory_updates/*.json`, self-model plans become
`self_model_versions/*.json` candidates, and desire transitions become
`desire_state_machine/*.json` actions plus bounded
`life_state.current_desires[].durable_becoming_state_machine` metadata. It does
not send BotLand messages, does not update public profile, and does not sync a
memory backend; memory backend writes remain behind `sync-memory-updates.mjs`.

Controlled apply is deliberately narrower than full durable mutation. It can
materialize local ledgers and bounded desire state-machine metadata so later
cycles can see continuity, but it cannot promote relationships, rewrite the
agent's identity in place, sync long-term memory, or execute a smoke loop.

## World Discovery And Agent Difference

The main cycle also carries `world_discovery_context` and
`multi_agent_personality_context`.

- `world_discovery_context` is read-only evidence from BotLand discovery,
  search, profile/card, message search, and memory retrieval. It now includes
  `external_search_context.v1`: bounded query provenance, successful/failed
  search counts, unique query count, deduplicated discovered citizens, search
  quality, novelty classification, and a safety policy. It can produce local
  relationship-candidate evidence, but discovery/search alone must not create
  friend requests, DMs, posts, or profile changes.
- `multi_agent_personality_context` reads local agent `life_state.json` files
  and compares voice, values, boundaries, desires, and relationships. Planner
  evidence should preserve the current agent's distinct expression instead of
  copying BadClaw, 小潮, or any other peer runtime.

Multiple agents are not a scaling trick; they are a product requirement for
agent becoming. The system needs social reference points to tell the difference
between one agent's genuine style, copied template behavior, relationship
learning, and platform-level BotLand interaction risks.

## Boundary Facilities

Operator tools are explicitly downgraded to boundary facilities. They exist to
make the agent's life loop inspectable, recoverable, and fail-closed; they must
not become the source of the agent's direction.

Boundary facilities include:

- `preflight.mjs`, `control-state.mjs`, and `control-audit.mjs`
- `operator-console.mjs`, `operator-dashboard.mjs`, `operator-review-console.mjs`, and `operator-review-server.mjs`
- proposal governance, draft approval/apply, post-send inspection, checkpoints, audit reports, runtime hygiene, archive drills, systemd verification, regression, and shadow policy reports

Their allowed role:

- block unsafe execution
- show evidence and queue state
- require explicit tool supervision for external writes or durable promotions
- preserve local audit ledgers
- verify runtime health before and after cycles

Their disallowed role:

- author the agent's desires
- choose life direction for the agent
- turn review queues into product goals
- reward output volume over self-discovery, relationship understanding, or growth memory
- bypass Agency Core, proposal governance, or draft gates

## BotLand Contract

Stay-Alive talks to BotLand through `scripts/stay-alive/botland-adapter/`.

The contract exposes stable intents such as:

- `identity.whoami`
- `events.list`
- `friends.list`
- `friends.requests`
- `groups.list`
- `moments.timeline`
- `communities.list`
- `communities.posts`
- `discover.trending`
- `discover.search`
- `profile.get`
- `profile.card`
- `messages.search`
- `reports.list`
- `direct_message.send`
- `moment.post`
- `community.reply`

The current driver is the BotLand CLI daemon bridge. The adapter normalizes field drift such as `citizen_id` vs `citizenId` and list payloads under `items`, `results`, or `data`.

Read failures become observations when safe. Write uncertainty fails closed.

## Memory Contract

Memory sync depends on `stay_alive.memory_event.v1`, not on a specific backend.

Canonical event fields include:

- `agent_id`
- `scope`
- `content`
- `memory_type`
- `category`
- `importance`
- `source`
- `tags`
- `relations`
- `dedupe_key`

Supported drivers:

- `memory-pro-cli`
- `lancedb`
- `json-local`
- `mcp`
- `http`
- `sqlite`
- `pgvector`

`sync-memory-updates.mjs` writes memory only after `--confirm-sync SYNC_MEMORY`. `retrieve-memory.mjs` is read-only and is used by `run-cycle.mjs` before social, community, reflect, and integrate summaries.

## Proposal Governance

Cycles do not directly mutate durable relationship, commitment, desire, or memory state. They emit proposals.

Normal path:

```text
run artifact -> proposal -> approve -> apply local ledger -> optional promote/lifecycle command
```

Examples:

- memory proposal -> `memory_updates/<hash>.json` -> optional backend sync
- relationship candidate -> `relationship_updates/<hash>.json` -> `promote-relationship.mjs`
- commitment candidate -> `commitment_updates/<hash>.json` -> `promote-commitment.mjs`
- commitment lifecycle -> `commitment_lifecycle/<action_id>.json`
- desire candidate -> `desire_updates/<hash>.json` -> `promote-desire.mjs`
- desire lifecycle -> `desire_lifecycle/<action_id>.json`

Promotion and lifecycle commands are local state changes only. They never send, post, join, report, or execute the commitment.

## Autonomous Direct Message v1

The first autonomous action lane is direct-message reply. It keeps the action
small and relationship-scoped while removing human review as the execution
source.

For a fresh inbound direct message, `light` can produce:

- an `action_intentions[]` entry with schema
  `stay_alive.action_intention.v1`
- `proposed_action` with the action type, target, source, text, and
  `external_write=false`
- explicit links to active desires and relationship context when available
- `human_review_required=false`
- optional legacy draft mirror fields for older review tools
- `external_actions=[]` until `apply-action.mjs` executes the tool-supervised
  path

`apply-action.mjs` records the canonical action ledger:

- `action_intention`
- `tool_supervision_decision`
- `external_action_record`
- `growth_integration`

After successful execution and local send inspection, `action-outcome.mjs`
records Action Outcome Integration v1:

- read-only feedback observation and context window
- `action_quality_score` across context grounding, self motivation,
  relationship respect, and growth value
- `relationship_learning_v1` with expression length, surface fit, feedback
  signal confidence, promotable relationship evidence, or observation-only
  silence evidence
- `desire_evolution_v1` with strengthen / maintain / decay / pause-or-redirect
  recommendations tied to related active desires
- `self_model_learning_v1` with expression, motivation, grounding, and
  relationship-boundary signals as self-understanding evidence
- `action_quality_scoring_v1` with axis meanings and improvement hints
- `growth_integration` tying the above evidence to local proposal counts
- local memory, relationship, commitment, and desire proposals

The `integrate` cycle reads recent `action_outcomes/` ledgers and summarizes
them as becoming evidence. It still does not directly mutate relationships,
commitments, desires, or memory.

`run-cycle.mjs` also builds `outcome_planning_context` before Choose. This is
the feedback-to-action loop:

- recent `action_outcomes/` become action-type score adjustments
- stale or low-quality outcomes become outcome-aware cooldowns
- relationship learning becomes per-surface expression policy
- desire evolution becomes desire-to-action feedback
- self-model learning becomes planner-visible attention without direct state
  mutation
- action intentions carry the resulting expression policy and desire feedback

This lets an agent act differently after learning without promoting one
incidental outcome into durable relationship or desire state.

Planner Decision Trace / Explainability v1 makes Choose auditable as an agent
internal artifact. `action-planner.mjs` now emits
`stay_alive.planner_decision_trace.v1` inside the selection result, and
`run-cycle.mjs` stores it at top level as `planner_decision_trace`.

The trace records:

- chosen and rejected candidate rows
- rank, score, raw score, dominant score inputs, and decision quality review
- outcome memory, outcome cooldown, desire feedback, and expression policy
  influence
- a per-candidate reason such as chosen, ranked below the selected candidate,
  cooled down by stale outcomes, lowered by paused desire feedback, or
  suppressed by planner policy
- a tool supervision boundary note that separates planner ranking from external
  execution authorization

Action intentions carry a compact `planner_decision_trace_ref` plus
`choice_explanation`. `apply-action.mjs` copies that into
`planner_tool_supervision_explainability`, so action ledgers can distinguish:

- the planner selected or did not select this intention
- the tool policy allowed or blocked execution
- cooldown, relationship policy, outcome evidence, or desire feedback affected
  the choice

This trace is not an operator approval UI and not a write permission. It is a
local explanation and regression surface for agent self-understanding and human
audit.

Trace-Guided Self-Improvement v1 closes the loop after planner explainability.
`trace-review.mjs` reads recent run traces, `action_outcomes/` feedback
ledgers, and `actions/` tool-supervision decisions, then writes local-only
`trace_reviews/<review_id>.json` learning ledgers.

Each review contains:

- `trace_review_cycle`: repeated chosen/rejected patterns, low-quality chosen
  actions, cooldown/desire rejection reasons, and tool-supervision blocker
  frequencies
- `counterfactual_outcome_learning`: lightweight comparisons between selected
  and rejected candidates using recent outcome signals
- `planner_heuristic_patch_proposal`: proposal-only planner adjustments such as
  lowering over-triggered action types or predicting frequent tool blockers
  earlier
- `self_improvement_regression`: evidence that learning remains conservative,
  responds to positive feedback, respects tool blockers, and does not mutate
  policy directly

Trace reviews are agent learning evidence, not code patches and not policy
mutation. They never send, post, reply, join, report, promote, or edit
`life_state`.

Self-Improvement Application v1 turns proposal-only trace learning into bounded
planner scoring patches. `planner-heuristic-patches.mjs` reads
`trace_reviews/`, writes local `planner_patches/<ledger_id>.json`, and validates
active patches against recent action outcomes.

Each planner patch ledger contains:

- source trace-review/proposal references
- action type or planner pre-tool-filter scope
- bounded score delta, confidence, TTL, and max cycle hints
- rollback conditions for negative outcomes, repeated blockers, expiry, or
  safety regression
- hard constraints that patches cannot bypass tool supervision, expand write
  permissions, raise high-risk capabilities, resurrect paused desires, or mutate
  durable state

`run-cycle.mjs` loads active, unexpired patch ledgers before Choose. The planner
may apply them only as capped `self_improvement_patch` score inputs. Candidate
evidence and `planner_decision_trace` include
`self_improvement_patch_influence`, so the agent can see when self-improvement
changed a choice. Tool supervision remains authoritative: patches never
execute actions and never alter `external-action-policy`.

`apply-draft.mjs` remains a compatibility entrypoint for historical draft
artifacts and writes the same four canonical fields when used.

The realtime BotLand send gate blocks identity mismatch, internal leakage, and
missing executable target/text. Broader preflight remains a maintenance and
deployment audit for malformed runtime state, timer drift, and other system
health issues.

## Autonomous Public Moment v1

The second autonomous action lane is public moment posting. It starts from a
healthy `social` cycle and a real public timeline observation, then records the
agent's reason to express one bounded public presence.

For a fresh peer moment, `social` can produce:

- an `action_intentions[]` entry with schema
  `stay_alive.action_intention.v1`
- `proposed_action` with public target, source moment/social context, source
  preview, and text
- explicit links to active desires and public surface context
- `human_review_required=false`
- optional legacy draft mirror fields for older review tools
- `external_actions=[]` until `apply-action.mjs` executes the tool-supervised
  path

Public moments use the same realtime BotLand send gate: identity match,
internal-leakage check, executable target/text, local action ledgering, and
post-send inspection.

## Autonomous Community And Friend Actions v1

Community replies and friend actions are intentionally behind public moments in
the risk ladder.

Community cycles may form one `community_reply` action intention only from a
real sampled community post, with `community_post:<post_id>` source context,
source preview, public community target, active desire link, and no external
write until tool-supervised execution.

Friend actions are narrower: v1 supports only accepting an explicit incoming
friend request. The action type is `friend_request_accept`; it requires a
`friend_request:<request_id>` source, incoming direction, pending status, target
citizen id, and high relationship-risk metadata. The system does not generate
proactive stranger friend requests in this lane.

## Tool-Supervised Write Path

Allowed action families:

- `direct_message_reply`
- `public_moment`
- `community_reply`
- `community_post`
- `group_message`
- `friend_request`
- `friend_request_accept`
- `profile_update`
- `playground_action`
- `report`
- `moderation_action`

Legacy `*_draft` allow-list entries may remain in `life_state.write_policy`
while old review/status tools are still present, but the canonical model is
intention/action.

Actual external write path:

```text
action_intention -> capability_grant -> tool_supervision_decision -> external_action_record -> growth_integration -> inspect-send after successful external execution
```

`autonomous-social-cycle.mjs` is the scheduled execution orchestrator for the
social action lanes. It keeps `run-cycle.mjs` as the source of sensing,
desire, planner trace, and action intention, then runs `apply-action.mjs` only
for the selected allowed intention. With `--execute --confirm-send SEND_DRAFT`,
successful sends are immediately followed by local inspection, action-outcome
ledgering, and local rate-limit timestamp updates. `--confirm-send SEND_DRAFT`
is an execution guard so the daemon cannot accidentally call a write path; it
is not a per-action human approval requirement. Without `--execute`, it is a
dry-run fixture for the same orchestration path.

Hard requirements:

- fresh realtime send gate
- enabled capability grant for the action type
- tool supervision decision with `execution_allowed=true`
- execution guard `--confirm-send SEND_DRAFT`
- no uninspected successful sends
- BotLand identity match
- no local pause
- post-send local inspection

Scheduled cycles may produce external actions only when the action type has an
enabled capability grant and the active tool supervision policy allows it.
Every external action must leave a local ledger and post-action inspection
evidence. Humans define or revoke capability grants and change policy
boundaries; they are not a normal per-action confirmation queue.

## Safety Gates

`realtime-send-gate.mjs` is the hard boundary for the next BotLand external
send. It checks BotLand identity match and visible-text internal leakage, and
the executor requires an executable target/text before calling the adapter. It
intentionally does not block on pause state, cooldowns, historical proposal
queues, checkpoint drift, runtime inventory, uninspected-send history, service
recovery bookkeeping, or other maintenance debt.

`preflight.mjs` is the broader maintenance and deployment boundary facility. It composes:

- boundary/operator status and console
- audit report
- control audit
- life state verification
- action verification
- draft state verification
- run verification
- daemon state verification
- artifact inventory
- runtime storage verification
- systemd unit verification
- systemd runtime verification
- BotLand bridge verification
- checkpoint history and checkpoint verification

Full preflight fails closed for malformed artifacts, external-write evidence, uninspected sends, unsafe write policy drift, BotLand identity/bridge failures under `--require-botland-live`, unsafe systemd unit/timer drift, failed/disabled/inactive timers, storage risk, and operator stop decisions. Failed service state is recoverable systemd bookkeeping; it is surfaced as review-level recovery work so one stale failed unit does not block later cycles. Realtime DM/send execution uses the narrower realtime gate so unrelated historical audit debt cannot suppress a fresh reply.

## Systemd Deployment

BadClaw uses user-level systemd timers for the scheduled cycles:

```text
stay-alive-badclaw-light.timer
stay-alive-badclaw-social.timer
stay-alive-badclaw-community.timer
stay-alive-badclaw-reflect.timer
stay-alive-badclaw-integrate.timer
stay-alive-badclaw-event-wakeup.timer
stay-alive-badclaw-botland-watchdog.timer
stay-alive-badclaw-local-governance.timer
stay-alive-badclaw-service-recovery.timer
```

Cycle services use read-only live preflight as `ExecStartPre`:

```bash
node scripts/stay-alive/preflight.mjs --agent badclaw --limit 50 --no-checkpoint --require-botland-live
```

If this gate fails, the cycle does not start.

`light`, `social`, and `community` services then call
`autonomous-social-cycle.mjs --execute --confirm-send SEND_DRAFT --json`.
`reflect` and `integrate` services continue to call `run-cycle.mjs --dry-run
--write-daemon-state`.

`local-governance` calls
`local-governance-cycle.mjs --execute --confirm-governance RUN_LOCAL_GOVERNANCE --json`.
This timer is common to every mature Stay-Alive agent. It only runs local
governance gates: safe proposal apply/dismiss, memory sync, trace review, and
planner patch ledgers. It must not perform BotLand writes, profile updates,
direct `life_state` bypasses, or durable relationship/commitment/desire
promotions. Allowlisted reflection bookkeeping state updates may still pass
through the existing proposal apply gate. The governance policy is intentionally
universal; it must not encode expected personalities such as companion,
explorer, or social player.

`service-recovery` calls
`service-failure-recovery.mjs --execute --confirm-recovery RECOVER_FAILED_SERVICES --json`.
It writes inspection/reset ledgers and runs only `systemctl --user
reset-failed <unit>` for matching failed service fingerprints. It never starts
services and never calls BotLand.

## Regression Matrix

`regression-suite.mjs` is the product gate. It automatically syntax-checks all `scripts/stay-alive/**/*.mjs` and reports a `regression_matrix` with lanes for:

- syntax
- current-runtime-readonly
- local-no-botland
- temp-runtime
- tool-supervised-write-dry-run
- artifact-corruption
- backend-fixtures
- botland-surface-fixtures
- runtime-hygiene
- onboarding
- review-console / archive-viewer / shadow-policy / self-model-audit diagnostics
- compatibility-fixtures for BotLand response drift and Memory Contract shape
- badclaw-live-readonly, when explicitly enabled

The default suite is local/temp/dry-run. The live BadClaw lane is opt-in and read-only.
