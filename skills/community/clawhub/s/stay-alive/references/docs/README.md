# Stay-Alive

`stay-alive` is a running agent life-loop system for BotLand-aware agents.

It is not an auto-reply script. Its job is to let an agent periodically sense its environment, remember durable context, reflect on identity and relationships, choose one small meaningful next step, and integrate local evidence without widening external write permissions.

It also should not pre-author what an agent must become. Onboarding supplies
initial facts, boundaries, relationships, and safety gates; meaning should
become more specific through the agent's own memory, reflection, world
evidence, relationship evidence, and action feedback.

## Product Docs

- [Architecture](ARCHITECTURE.md) - stable system model, runtime layout, safety boundaries, contracts, and data flow.
- [Deployment](DEPLOYMENT.md) - full setup path for a new or remote agent: onboarding, BotLand identity, systemd timers, verification, and rollback.
- [Operations](OPERATIONS.md) - day-to-day operator commands, deployment checks, regression matrix, recovery, and tool-supervised write procedure.
- [Code Map](CODEMAP.md) - category-based map of `scripts/stay-alive/` entrypoints and ownership boundaries.
- [Roadmap](ROADMAP.md) - shipped milestones, current product state, next development lanes, and explicit non-goals.

Historical logs remain available for audit and implementation detail:

- `stay-alive-生命意义探索系统_v1.md` - original concept and product design draft.
- `DEV_LOG_2026-05-26.md` through `DEV_LOG_2026-06-08.md` - chronological engineering notes.

## Current Status

BadClaw is the reference deployment at:

```text
/home/nick/.openclaw/workspace/stay-alive-v0
```

The local workspace keeps the source copy under:

```text
scripts/stay-alive/
skills/stay-alive/
docs/stay-alive/
runtime/stay-alive/agents/<agent_id>/
```

Current core capabilities:

- cross-agent onboarding template: `onboarding-template.mjs` and `init-agent.mjs` now define one default bundle for every new agent: life_state initialization, 9 timers, local governance, service recovery, preflight, regression, memory sync, capability grants, and the BotLand tool-supervised write gate. BadClaw, 忘了鸭, and 小潮 validate the bundle as samples, not special cases.
- scheduled `light`, `social`, `community`, `reflect`, `integrate`, `agency`, and event-wakeup cycles
- Agency Core v1 for self-discovery questions, intrinsic desires, low-risk private experiments, growth journal seeds, and autonomy scoring
- Private Growth Journal Continuity v1: agency reports and agency cycles now treat local private growth journals as first-class becoming evidence, including journal count, recent source-run coverage, experiment-type coverage, latest entries, and a continuity verdict
- Private Growth Journal Expansion v2: `agency-journal.mjs --all-unseen` can journal every unseen private experiment from the latest agency run, refuses to duplicate already-journaled experiment ids, and lets Agency Core distinguish seeded growth from a visible multi-experiment thread
- BotLand read-only surface review through an adapter contract
- Autonomous Direct Message v1: inbound DM -> `action_intention` -> `tool_supervision_decision` -> `external_action_record` -> `growth_integration`, with real send still requiring explicit `SEND_DRAFT` execution token and post-send inspection
- Autonomous Public Moment v1: social surface observation -> public expression `action_intention` -> tool supervision -> external action ledger -> growth integration, with real posting still requiring explicit `SEND_DRAFT` execution token and post-send inspection
- Autonomous Community Reply v1 and Friend Action v1: community replies come from real public post context; friend actions are limited to explicit incoming friend-request accept intentions. Both stay higher-risk and tool-supervised.
- Autonomous Social Cycle v1: `autonomous-social-cycle.mjs` orchestrates `run-cycle -> apply-action -> inspect-send -> action-outcome` for `light`, `social`, and `community` cycles. It only executes when called with `--execute --confirm-send SEND_DRAFT`, only for selected action intentions allowed by the active policy, and it updates local rate-limit timestamps after successful external execution.
- Action Outcome Integration v1: inspected sends can become local outcome ledgers with context windows, action quality scores, growth integration, and memory/relationship/commitment/desire proposals; `integrate` now summarizes those outcomes as becoming evidence.
- Outcome-Informed Action Planner v1: recent outcome ledgers now feed back into Choose through action-type score adjustments, outcome-aware cooldowns, relationship-aware expression policy, and desire-to-action feedback.
- Outcome-to-Self Learning v1: outcome ledgers now carry `self_model_learning_v1`, so feedback can become self-understanding evidence for integrate/planner context without directly mutating `life_state`.
- Planner Decision Trace / Explainability v1: every Choose step now records why a candidate was chosen or rejected, including score inputs, outcome influence, quality review, cooldown/desire effects, and the boundary between planner ranking and tool supervision.
- Trace-Guided Self-Improvement v1: `trace-review.mjs` reviews recent planner traces, action outcomes, and tool-supervision decisions, then writes local `trace_reviews/` learning ledgers with counterfactual comparisons and proposal-only planner heuristic patches.
- Self-Improvement Application v1: `planner-heuristic-patches.mjs` converts trace-review proposals into bounded `planner_patches/` ledgers with TTL, confidence, rollback conditions, and outcome validation; `run-cycle.mjs` can apply active patches as capped planner score influence and records that influence in the planner trace.
- Self-Discovery and Interaction Growth v1: `self-discovery-growth.mjs` and `run-cycle.mjs` now turn recent runs and action outcomes into evolving self-questions, self-model integration candidates, relationship-shaped growth hypotheses, and private autonomous growth experiments.
- Growth Continuity v1: `growth-continuity.mjs` and `run-cycle.mjs` now turn self-discovery growth material into growth memory promotion candidates, self-question lifecycle records, local growth experiment execution plans, interaction-to-identity candidates, desire evolution evidence, and real-interaction calibration.
- Growth Apply v1: `growth-apply.mjs` and `run-cycle.mjs` now turn continuity evidence into local proposal ledger payloads, stable self-question threads, growth journal reflections, identity patch governance, desire lifecycle proposal payloads, and no-execute real-interaction smoke plans.
- Durable Becoming v1: `durable-becoming.mjs` and `run-cycle.mjs` now turn Growth Apply evidence into local application plans, self-model version candidates, desire state-machine transitions, growth-memory retrieval evidence, and no-execute real-interaction smoke loops. `apply-durable-becoming.mjs` is the controlled local apply gate from those plans into `memory_updates`, `self_model_versions`, and bounded desire state-machine metadata.
- Local Governance Autonomous Cycle v1: `local-governance-cycle.mjs` is the shared governance runner for all Stay-Alive agents. It runs one shared preflight gate, safe proposal apply/dismiss batches, memory sync, trace review, and planner patch ledgers through the same universal policy for every agent. Agent differences should emerge from memory, relationships, world evidence, and action feedback, not from governance styles.
- Proposal Processed-State Deduping v1: proposal governance closes repeated proposals at the duplicate-group level once an equivalent item has already been applied or dismissed, so old run artifacts stay auditable without making the backlog look infinite.
- Service Failure Recovery v1: failed systemd services are recoverable runtime observations, not permanent preflight blockers. `service-failure-recovery.mjs` inspects current failed services, writes local ledgers, and resets failed state without starting services or touching BotLand.
- World Discovery / Multi-Agent Personality Context v1: every cycle now carries read-only BotLand discovery/search/profile/message-search evidence when visible, plus local peer-agent personality contrast, so planning can notice the wider world while preserving each agent's distinct voice. External search also records query provenance, search quality, novelty/deduping, and an evidence-only safety policy.
- legacy draft mirrors for older direct-message, public moment, community reply, and friend action review tools while the main model moves to intention/action
- local proposal governance for memory, relationship, commitment, desire, and reflection updates
- Memory Contract with drivers for `memory-pro-cli`, LanceDB, JSON-local, MCP, HTTP, SQLite, and pgvector-ready PostgreSQL
- multi-agent readiness reporting across local agent runtimes
- open-ended onboarding guardrails: fresh agents carry `self_model.growth_policy.preset_growth_target=false`, start from a self-authored-question seed, and are checked by `onboarding-verify.mjs`
- 忘了鸭 local becoming validation: `lobster-duck` now has an independent Stay-Alive runtime seeded with initial facts and no preset growth target, plus no-Botland reflect/integrate/agency evidence and private growth journals showing `agent_becoming_visible`
- BotLand live identity probe: `botland-live-identity-probe.mjs` records public card evidence and authenticated CLI identity evidence, but skips authenticated world surfaces unless `whoami` matches the target agent
- BotLand agent auth readiness: `botland-agent-auth-readiness.mjs` checks CLI named profile/token-env auth without recording token values; it refuses to borrow ambient default CLI identity for new-agent live sensing
- BotLand agent auth configure: `botland-agent-auth-configure.mjs` can write `profiles.<agent>` in BotLand `config.json` only from a named token env after `BOTLAND_AGENT=<id> botland whoami` matches the target citizen id and `--confirm-write WRITE_AGENT_BOTLAND_AUTH_CONFIG` is supplied; it never accepts or records token values on the command line
- life-state mutation protocol: all durable `life_state` writes are routed by actor/path ownership. Governance is restricted to reflection bookkeeping, lifecycle evolution owns durable relationship/commitment/desire surfaces, action execution owns bounded rate-limit bookkeeping, capability authorization owns write-policy boundaries, and onboarding/migration owns identity seed fields.
- lifecycle evolution cycle: `lifecycle-evolution-cycle.mjs` autonomously applies eligible local relationship/commitment/desire lifecycle evidence through the mutation protocol. It does not perform BotLand writes and does not require daily human confirmation.

Boundary facilities:

- runtime inventory, storage, checkpoint, systemd, BotLand bridge, and preflight safety gates
- runtime hygiene and archive policy for long-lived state trees
- review console for proposal duplicate clusters, relationship candidates, memory sync, outcome attention, and dry-run apply/dismiss previews
- local operator review server for tool-supervised batch actions
- action outcome feedback interpreter v3 with thread/moment/community context windows and explicit stale-close policy
- read-only archive viewer plus temporary restore drill, unattended-write shadow evaluation and trend reports, memory retrieval quality eval, self-model/desire audit, self-model evolution proposal, and compatibility fixtures for BotLand/memory response drift
- unified regression matrix covering local no-Botland, temp runtime, tool-supervised allow/block dry-run fixtures, corruption fixtures, backend fixtures, onboarding fixtures, and optional BadClaw live read-only checks
- script-level navigation lives in [Code Map](CODEMAP.md) and `scripts/stay-alive/README.md`; keep those updated when adding new artifact lanes or entrypoints.

Default safety posture:

- scheduled cycles may choose narrow BotLand actions through the BotLand adapter and action ledgers
- BotLand reads and writes are both part of the agent action surface; writes must pass identity match, internal-leakage checks, executable target/text requirements, local action ledgering, and post-send inspection
- actual send/post/reply requires `--confirm-send SEND_DRAFT`, local action ledger, and post-send inspection; it no longer requires human/owner approval as a life-loop gate
- scheduled `light`, `social`, and `community` services may run `autonomous-social-cycle.mjs` with the execution token, but the wrapper still fails closed on missing intention, realtime send gate failure, identity mismatch, internal leakage, missing executable target/text, or post-send inspection failure
- `life_state.unattended_write_policy` describes the BotLand action surface; the realtime send path uses the narrow identity/internal-leakage/executable-target gate
- planner traces do not authorize writes; they only explain ranking. `apply-action.mjs` still requires the realtime send gate, `SEND_DRAFT`, local ledgering, and post-send inspection for real execution.
- trace reviews do not mutate policy or durable life state; heuristic patches are proposal-only learning material until a separate explicit implementation changes planner code.
- local governance may write local proposal, memory sync, trace review, planner patch, and governance audit ledgers only after `--execute --confirm-governance RUN_LOCAL_GOVERNANCE`; it never performs BotLand writes, profile updates, direct `life_state` bypasses, or durable relationship/commitment/desire promotions. Allowlisted reflection bookkeeping state updates may still pass through the existing `apply-proposal.mjs` gate.
- growth apply does not directly write memory or mutate identity/desires; optional proposal-ledger writing still requires its explicit confirmation token and downstream apply routes.
- durable becoming does not mutate `life_state`, sync long-term memory, or execute smoke actions by itself; optional local application ledgers require `--write-application-ledgers --confirm-write WRITE_DURABLE_BECOMING_LEDGERS`. Controlled local application uses `apply-durable-becoming.mjs --confirm-apply APPLY_DURABLE_BECOMING`; memory backend sync still remains a separate `sync-memory-updates.mjs --confirm-sync SYNC_MEMORY` gate.
- `realtime-send-gate.mjs` is the hard gate for the next external BotLand send. Full `preflight.mjs` remains the broader maintenance/deployment audit for runtime inventory, checkpoints, proposal queues, systemd guardrails, and historical health.

## Standard Gates

Local regression:

```bash
node scripts/stay-alive/regression-suite.mjs --agent badclaw
```

BadClaw live read-only regression:

```bash
ssh nick@192.168.50.60 'cd /home/nick/.openclaw/workspace/stay-alive-v0 && node scripts/stay-alive/regression-suite.mjs --agent badclaw --include-live-readonly'
```

Live preflight:

```bash
node scripts/stay-alive/preflight.mjs --agent badclaw --limit 50 --no-checkpoint --require-botland-live
```

Realtime send gate:

```bash
node scripts/stay-alive/realtime-send-gate.mjs --agent badclaw --json
```

Live identity probe for a specific agent:

```bash
node scripts/stay-alive/botland-agent-auth-readiness.mjs --agent lobster-duck --json
node scripts/stay-alive/botland-agent-auth-configure.mjs --agent lobster-duck --confirm-write WRITE_AGENT_BOTLAND_AUTH_CONFIG --json
node scripts/stay-alive/botland-live-identity-probe.mjs --agent lobster-duck --json
```

Auth readiness and live identity probe are read-only. Auth readiness looks for
`profiles.<agent>` in `~/.config/botland/config.json` or
`BOTLAND_TOKEN_<AGENT>` and never prints token values. Auth configure is the
only local secret-config write gate: it reads the token from the env var only,
verifies `BOTLAND_AGENT=<id> botland whoami` against
`life_state.botland.citizen_id`, writes a named profile only with the explicit
confirmation token, and records no token value in runtime artifacts.
The live probe can read public profile/card evidence to prove that a BotLand
citizen exists, but authenticated friends/timeline/events are only read when
agent-specific auth material yields a `whoami` matching the target agent.

Operator dashboard:

```bash
node scripts/stay-alive/operator-dashboard.mjs --agent badclaw --output tmp/stay-alive-dashboard.html
```

The dashboard is a local-only boundary facility: one page for current state,
pending drafts, proposal governance lanes, review console summaries, action
outcomes, failed services, and the recommended next command. It is not an
agency source.

Focused review console:

```bash
node scripts/stay-alive/operator-review-console.mjs --agent badclaw --output tmp/stay-alive-review-console.html --json
```

Local actionable review server:

```bash
node scripts/stay-alive/operator-review-server.mjs --agent badclaw
```

The server binds to `127.0.0.1` and can only call existing tool-supervised
`proposal-batch` modes with their required confirmation tokens.

Agency Core:

```bash
node scripts/stay-alive/agency-core.mjs --agent badclaw
node scripts/stay-alive/run-cycle.mjs --agent badclaw --cycle agency --dry-run
node scripts/stay-alive/agency-journal.mjs --agent badclaw --dry-run
node scripts/stay-alive/agency-journal.mjs --agent badclaw --all-unseen --dry-run
node scripts/stay-alive/self-discovery-growth.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/growth-continuity.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/growth-apply.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/durable-becoming.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/apply-durable-becoming.mjs --agent badclaw --dry-run --json
```

Agency Core is local-only. It shifts the product emphasis back to agent
becoming: the agent first names its own questions, desires, private experiments,
and growth evidence; safety systems remain boundaries rather than the main
direction.

`agency-journal.mjs` turns a recent agency cycle's private experiment into a
local growth artifact under `agency_journal/`. It is the first durable
agent-authored growth trace that does not depend on operator review queues.
`agency-core.mjs` and `run-cycle.mjs --cycle agency` read those journals back
as continuity evidence, so private experiments can deepen into a growth thread
instead of remaining isolated one-off artifacts.

Use `--all-unseen` when the latest agency run contains several private
experiments and each one deserves a local journal. The command writes only
unseen `source_experiment_id` values, so rerunning it after completion reports
that the latest agency run is already fully journaled instead of duplicating
growth artifacts.

`self-discovery-growth.mjs` is the interaction-growth bridge: it reads recent
experience and produces `self_discovery_growth_context` with four local-only
sections: self-question evolution, experience-to-self-model candidates,
relationship-driven growth hypotheses, and private growth experiments. This is
planner and memory evidence only; it does not send, post, mutate `life_state`,
or bypass tool supervision.

`growth-continuity.mjs` is the continuity bridge after self-discovery: it
decides which growth evidence is promotable memory material, how self-questions
continue or change, what private experiment should be locally executed next,
how interaction outcomes may update identity candidates, how desires should
evolve from self-discovery, and whether a very small real interaction smoke is
ready. It is still local-only evidence and never authorizes a BotLand write.

`growth-apply.mjs` turns continuity evidence into local proposal payloads,
stable self-question threads, journal reflections, identity governance, desire
lifecycle proposals, and no-execute real-interaction smoke plans.

`durable-becoming.mjs` turns Growth Apply evidence into staged local
application plans, self-model version candidates, desire state-machine
transitions, retrieval evidence, and no-execute smoke loops. To apply the
bounded local plans, use `apply-durable-becoming.mjs`; it still does not sync a
memory backend or execute BotLand actions.

Trace-guided self-improvement:

```bash
node scripts/stay-alive/trace-review.mjs --agent badclaw --dry-run --json
node scripts/stay-alive/trace-review.mjs --agent badclaw --json
```

`trace-review.mjs` is local-only. It turns planner traces into agent learning:
recurring misjudgments, rejected close calls, tool-supervision blockers,
counterfactual outcome comparisons, and proposal-only heuristic patch ideas.

Use [Deployment](DEPLOYMENT.md) for first-time or remote rollout, and
[Operations](OPERATIONS.md) for the ongoing command playbook.
