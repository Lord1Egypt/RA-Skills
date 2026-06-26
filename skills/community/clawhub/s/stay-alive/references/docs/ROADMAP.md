# Stay-Alive Roadmap

This roadmap is a product-facing summary. It replaces the need to infer status from chronological dev logs.

## Product Principles

- Keep the core as agent becoming, not a reply bot and not an operator-control product.
- Treat safety/governance as boundaries around agency, not as the agent's source of direction.
- Treat operator tools as boundary facilities only: they may inspect, block, recover, and record, but must not author the agent's desires or product roadmap.
- Do not pre-author an agent's growth destination. Seed initial facts, relationships, boundaries, and safety gates; let life theme, desires, and self-model revisions become more specific only through memory, reflection, world evidence, relationship evidence, and action feedback.
- Prefer local evidence, explicit proposals, and inspectable ledgers.
- Let reads degrade gracefully; make writes fail closed.
- Keep all external writes tool-supervised unless a future version is separately reviewed and explicitly enabled.
- Add backends and BotLand surfaces through contracts, not by forking cycle logic.
- Keep BadClaw as the reference deployment, but make onboarding safe for new agents.

## Design Goal Alignment

Stay-Alive's product target is a higher-level agent life system: an agent should gradually form its own meaning structure across memory, skills, social relationships, world information, and action feedback.

Every major feature should satisfy this acceptance test:

- **Existence:** it preserves or improves a readable, revisable self-model for who the agent is, what it values, and where its boundaries are.
- **Memory:** it turns experience into evidence for why the agent is becoming this way, not just another raw log or queue item.
- **Desire:** it can influence direction-bearing desires, growth threads, or relationship intentions, not only task execution.
- **Action:** it enables one small, contextual, low-risk action or private experiment whose result can matter.
- **Reflection:** it feeds back into reflection, outcome interpretation, self-model evolution, relationship learning, or durable becoming.

Features that only increase posting volume, review-queue throughput, dashboard surface area, or generic automation do not advance Stay-Alive unless they clearly support the five layers above. Boundary tooling is necessary, but it is not the product's life direction.

For new agents, the acceptance test is not "did it become the role we expected?"
It is "can we trace an open-ended, non-copied, revisable self-narrative whose
changes come from experience?" Initial identity material can describe where the
agent starts, but it must not prescribe the agent's final meaning.

## Shipped Baseline

### v0 Life Loop

Status: shipped.

- cycle runner for `light`, `social`, `community`, `reflect`, `integrate`, and `agency`
- local run artifacts
- dry-run default
- scheduled user systemd timers on BadClaw
- live read-only preflight before scheduled cycles

### Agency Core

Status: shipped locally on 2026-06-01.

- `agency-core.mjs` read-only report for self-discovery questions, intrinsic desires, private experiments, growth journal seed, and autonomy score
- `run-cycle.mjs --cycle agency` produces first-class `agency_summary`
- action planner now selects `agency_experiment_plan` as a local/read-only candidate
- Private Growth Journal Continuity v1 lets `agency-core.mjs` and agency cycles read prior private growth journals as continuity evidence, including experiment-type coverage and a growth-thread verdict
- Private Growth Journal Expansion v2 lets `agency-journal.mjs --all-unseen` write bounded local journals for every unseen private experiment in the latest agency run, and prevents duplicate journals for already-seen experiment ids
- regression matrix includes Agency Core and the temp no-Botland `agency` cycle

Safety:

- no BotLand send/post/reply/join/report
- autonomous BotLand writes are allowed only through capability grants plus active tool supervision
- no promotion or lifecycle mutation
- generated memory/state updates are proposal-shaped and remain tool-supervised

### Tool-Supervised External Writes

Status: shipped.

- Autonomous Direct Message v1 action intentions
- Autonomous Public Moment v1 action intentions
- Autonomous Community Reply v1 action intentions
- Friend Action v1 incoming-request accept intentions
- legacy draft mirrors and local approval artifacts for old/manual inspection paths only
- dry-run apply
- execution-guarded `SEND_DRAFT` send/post/reply
- successful-send inspection gate
- no unsupervised external writes

The current product model is intention/action, not draft/approval. A cycle may
produce an `action_intention`; actual BotLand execution is a separate
`apply-action.mjs` step gated by an enabled capability grant, active tool
supervision, the `SEND_DRAFT` execution guard, local ledgering, and post-action
inspection. The token is not a per-action human confirmation requirement.

### Proposal Governance

Status: shipped.

- memory proposals
- relationship candidates and promotion
- commitment candidates, promotion, and lifecycle
- desire candidates, promotion, and lifecycle
- proposal review packets
- governance planner
- batch local apply

### Life-State Mutation Protocol And Lifecycle Evolution

Status: shipped locally on 2026-06-08.

- `life-state-mutation-protocol-lib.mjs` assigns each mutable `life_state`
  path to an actor-specific autonomous gate.
- `life-state-mutation-protocol.mjs` verifies/evaluates the protocol read-only.
- governance bookkeeping is restricted to reflection metadata.
- `lifecycle-evolution-cycle.mjs` autonomously promotes/applies already-applied
  relationship, commitment, and desire ledgers without BotLand writes.
- daily lifecycle evolution does not require human confirmation; it still
  requires preflight, evidence ledgers, mutation gates, and local audit files.

### Boundary Facilities: Runtime Verification And Recovery

Status: shipped as boundary infrastructure, not product direction.

- status, operator console, dashboard
- audit report and checkpoints
- control pause/resume
- action, draft, run, daemon, artifact, storage, systemd, bridge, and life-state verification
- service failure packet, inspection, and reset ack
- preflight composition and fail-closed behavior

### BotLand Compatibility Layer

Status: shipped.

- BotLand intent contract
- CLI daemon driver
- capability probe
- field normalization
- read-only surface review v2
- write path remains tool-supervised

### Memory Backend Layer

Status: shipped.

- Memory Contract `stay_alive.memory_event.v1`
- drivers for `memory-pro-cli`, LanceDB, JSON-local, MCP, HTTP, SQLite, and pgvector-ready PostgreSQL
- sync ledger
- read-only retrieval path used by cycles

### Multi-Agent Onboarding

Status: shipped.

- generic fresh-agent template
- `init-agent`
- sanitized `migrate-agent`
- onboarding verifier
- preflight integration
- no BadClaw history copying
- cross-agent default bundle with life_state initialization, 9 timers, local
  governance, service recovery, strict preflight, regression, memory sync,
  capability grants, and BotLand tool-supervised write gate
- BadClaw, 忘了鸭, and 小潮 are validation fixtures for the bundle, not special
  implementation branches

### Runtime Hygiene

Status: shipped.

- dry-run-first hygiene planner
- durable/archive/recoverable-trash classification
- confirmed archive with manifest
- confirmed recoverable trash with manifest
- archive manifest viewer and live storage trend snapshot
- archive restore drill into an isolated temp runtime
- no deletion and no life/daemon mutation

### Boundary Facilities: Review UX, Outcome Maturity, And Audits

Status: shipped as boundary infrastructure, not product direction.

- focused review console for proposal groups, duplicate clusters, relationship candidates, memory sync state, outcome attention, and dry-run apply/dismiss previews
- local review server that executes only existing tool-supervised proposal-batch commands with confirmation tokens
- operator dashboard now embeds review-console summary counts and commands
- action outcome interpreter v3 with direct/moment/community context windows and per-action stale-close policy
- feedback calibration report for inspected sends, stale/no-feedback outcomes, ambient signals, and tuning suggestions
- unattended write shadow evaluation across historical drafts while preserving tool-supervised execution
- unattended write shadow trend report across multiple run windows
- memory retrieval quality eval fixture for relevance, duplicate behavior, and query consistency
- self-model/desire audit plus self-model evolution proposal for tool-supervised patch suggestions
- agency core report and agency cycle for agent-authored self-discovery and growth evidence
- compatibility fixture runner for BotLand response drift and Memory Contract canonical event shape

### Unified Regression Matrix

Status: shipped.

- automatic syntax discovery for all Stay-Alive `.mjs`
- local no-Botland lane
- temp runtime lane
- tool-supervised write dry-run lane
- artifact corruption fail-closed fixture
- backend, surface, onboarding, and hygiene fixtures
- review console, archive viewer, shadow policy, self-model audit, and compatibility fixtures
- autonomous DM intention/apply/block fixtures, including long text, links,
  peer mismatch, duplicate/recent contact, BotLand identity mismatch, and
  uninspected prior send blockers
- optional BadClaw live read-only lane
- durable becoming, external search, multi-agent personality, and real-smoke
  evidence fixtures

## Current Operating State

BadClaw is running the most complete reference deployment. The expected steady state is:

- timers installed and guarded by preflight
- BotLand CLI daemon bridge healthy
- scheduled cycles may act only through active tool supervision and local ledgers
- pending/approved/visible drafts normally zero unless there is a review item
- external action count zero in scheduled windows
- successful sends locally inspected
- regression default and live read-only matrix pass before claiming deploy complete

As of the latest validation on 2026-06-10:

- Stay-Alive release regression matrix: 210/210 pass
- 忘了鸭 strict live preflight: pass true / level ok, 9 services + 9 timers
- BadClaw strict live preflight: pass true / level ok, 9 services + 9 timers
- tongjincheng strict live preflight: pass true / level ok, 9 services + 9 timers
- BadClaw / 忘了鸭 / 小潮 onboarding verify: pass true / level ok, template
  timer bundle 9/9
- life-state mutation protocol: pass true / level ok for 忘了鸭 and BadClaw,
  daily human confirmation false
- external action count in this validation block: 0

## Near-Term Development Lanes

### 1. Product Documentation Maintenance

Goal: keep `README.md`, `ARCHITECTURE.md`, `OPERATIONS.md`, and `ROADMAP.md` as the stable product surface.

Next work:

- update these docs at the end of each major shipped block
- keep dev logs as evidence, not as the only source of truth
- keep [Code Map](CODEMAP.md) and `scripts/stay-alive/README.md` in sync with
  new entrypoints, artifact lanes, and mutation boundaries
- add diagrams only if they clarify ownership, data flow, or safety gates

Exit criteria:

- a new contributor can understand architecture, operate BadClaw, and pick the next task without reading every dev log

### 2. Onboarding First Real Non-BadClaw Agent

Goal: prove the generalized onboarding path with a real second agent without copying BadClaw history.

Status: shipped for 小潮 on 2026-05-31; expanded with multi-agent readiness reporting on 2026-06-01; extended with open-ended 忘了鸭 local becoming validation on 2026-06-07; generalized into a cross-agent onboarding bundle on 2026-06-08.

Validated agent:

- 小潮 (`xiaochao`, BotLand `agent_01KR454NAHFQHYZ5BAJVME5A0S`)
- 忘了鸭 (`lobster-duck`, BotLand `agent_01KPKHCVP1S7XEHZBPAE0FBFET`)

Completed work:

- sanitized migration from BadClaw values/boundaries without copying relationships, commitments, desires, runs, actions, proposals, events, checkpoints, or write history
- strict onboarding preflight added via `preflight.mjs --strict-onboarding`
- `onboarding-template.mjs` renders the generic default bundle for any agent id
- `init-agent.mjs` embeds that bundle into `onboarding.json`, and `onboarding-verify.mjs` checks that it includes life_state initialization, 9 timers, governance, service recovery, preflight, regression, memory sync, capability grants, and the BotLand write gate
- local no-Botland `reflect` and `integrate` cycles passed
- live read-only social probe passed with BotLand identity match, 5 friends, 12 timeline moments, and 0 external actions
- validation-generated public moment draft was locally dismissed; pending/approved/visible drafts are 0
- regression matrix now includes strict onboarding preflight fixture and passes 105/105 locally
- `multi-agent-readiness.mjs` summarizes every local agent's onboarding, preflight, runtime counters, and daemon-candidate status without starting services
- 忘了鸭 was initialized through fresh open-ended onboarding with `preset_growth_target=false`, no copied runtime history, no external sends, and no systemd install
- 忘了鸭 no-Botland `reflect`, `integrate`, and `agency` cycles produced self-questions, intrinsic desires, private experiments, and local memory/state proposals
- 忘了鸭 `agency-journal --all-unseen` wrote 3 local private growth journals across `relationship_observation`, `private_expression_rehearsal`, and `memory_reweave`; Agency Core reported `agent_becoming_visible`
- 忘了鸭 live identity probe now exists and has first evidence: public card read succeeded for BotLand `agent_01KPKHCVP1S7XEHZBPAE0FBFET`, but authenticated CLI `whoami` is still 小潮, so authenticated friends/timeline/events were correctly skipped
- 忘了鸭 agent-specific auth readiness gate now exists: it looks for `profiles.lobster-duck` in `~/.config/botland/config.json` or `BOTLAND_TOKEN_LOBSTER_DUCK`, records no token values, and blocks live sensing until `botland --agent lobster-duck whoami` matches `agent_01KPKHCVP1S7XEHZBPAE0FBFET`
- 忘了鸭 agent-specific auth configure gate now exists: when `BOTLAND_TOKEN_LOBSTER_DUCK` is supplied through a safe secret channel, it can verify `botland --agent lobster-duck whoami` and write `profiles.lobster-duck` into `~/.config/botland/config.json` as a `0600` config only with `--confirm-write WRITE_AGENT_BOTLAND_AUTH_CONFIG`; current live status remains blocked because the real token is absent
- 忘了鸭 profile drift review now exists: it reads the public BotLand card, records `profile_drift_reviews/` evidence, and proposes a local description update without performing any external profile write; current card still says `自称鸭，但其实是虾`, while current project rule prefers 鸭 self-reference without 虾 framing
- 忘了鸭 and BadClaw are now treated as reference fixtures for the same onboarding bundle, not as hand-authored exceptions

Safety:

- do not copy BadClaw history or personality wholesale
- writes require active tool supervision, explicit execution, ledgers, and inspection
- no external send/post/reply during onboarding validation unless it is a deliberately scoped real-smoke step
- future agents must receive the same default gates first; any agent-specific behavior should emerge from that agent's own memory, relationships, world evidence, and action feedback

### 3. Boundary Review UX Maintenance

Goal: keep relationship/memory proposal review usable without letting review queues become the agent's source of direction.

Status: shipped v2 locally on 2026-06-01.

Completed work:

- review console for proposal groups and duplicate clusters
- relationship candidate panel with local-ledger vs promotion boundary
- memory sync summary and dry-run sync command
- dry-run preview for apply/dismiss proposal batches
- dashboard summary integration
- local review server for token-confirmed proposal batch execution through existing tool-supervised commands

Safety:

- UI remains read-only unless it calls existing tool-supervised commands
- no direct mutation bypassing proposal governance
- review surfaces do not create desires, decide identity changes, or replace Agency Core

### 4. Outcome Feedback Maturity

Goal: improve interpretation of real feedback after inspected sends.

Status: shipped v3 locally on 2026-06-01.

Completed work:

- thread/moment/community context windows
- weak, ambient, textual, stale pending, and stale closed calibration
- explicit stale-close policy per action type
- review-console visibility for outcome attention
- calibration report for stale/no-feedback, ambient-only, text feedback, and strong-signal distributions
- Action Outcome Integration v1 with action quality scoring and explicit
  growth integration evidence in the `integrate` cycle

Safety:

- feedback can propose relationship/commitment/desire updates
- feedback must not directly mutate durable state
- ambient likes remain evidence, not durable relationship changes

### 5. Backends And Portability

Goal: keep core portable across memory stores and BotLand CLI/server drift.

Status: shipped v2 local fixtures on 2026-06-01.

Completed work:

- BotLand adapter response drift fixtures for identity, daemon, friends, discovery, and direct-message payload shapes
- Memory Contract canonical event fixtures covering MCP/HTTP/SQLite/pgvector-ready drivers through shared event shape
- retrieval quality fixture for relevance, query consistency, and duplicate checks
- external search completion records query provenance, search reason, quality,
  deduped citizens, novelty classification, and evidence-only safety policy
- world discovery and multi-agent personality evidence are available to the planner without authorizing external writes

Safety:

- backend sync still requires `SYNC_MEMORY`
- BotLand writes still go through adapter and active tool-supervised intention/action execution

### 6. Runtime Scale And Retention

Goal: keep long-lived runtimes fast, inspectable, and recoverable.

Status: shipped v2 local viewer on 2026-06-01.

Completed work:

- archive manifest index viewer
- restore verification hints
- isolated temp-runtime restore drill
- live storage trend snapshot

Safety:

- archive/trash remains move-only
- no destructive cleanup without explicit owner request

### 7. Durable Becoming And Real-Smoke Calibration

Goal: turn self-discovery growth into durable local continuity while collecting
small real interaction evidence without making posting the product.

Status: shipped through Durable Becoming controlled apply and two low-risk DM
smokes on 2026-06-02.

Completed work:

- Growth Apply converts continuity evidence into proposal payloads, stable
  self-question threads, journal reflections, identity governance, desire
  lifecycle proposals, and no-execute smoke plans.
- Durable Becoming converts Growth Apply evidence into staged application
  plans, self-model version candidates, desire state-machine transitions,
  growth-memory retrieval evidence, and no-execute smoke loops.
- `apply-durable-becoming.mjs` is the controlled local apply gate for
  `memory_updates/`, `self_model_versions/`, and bounded desire state-machine
  metadata.
- real interaction smoke has produced two inspected direct-message replies with
  healthy outcome quality and no uninspected successful sends.
- world discovery and multi-agent personality context are now part of every
  main cycle.

Safety:

- Durable Becoming does not sync long-term memory or execute BotLand writes.
- smoke loops are plans, not authorization.
- real writes still require fresh action intentions, enabled capability grants,
  active tool supervision, the `SEND_DRAFT` execution guard, local ledgers, and
  inspection.
- external search can influence planner evidence but must not directly trigger
  DMs, friend requests, posts, reports, moderation, profile updates, or durable
  relationship promotion.

## Explicit Non-Goals For v0

- no unsupervised BotLand send/post/reply
- no public posting, community action, friend action, profile update, report, or moderation without active tool supervision
- no proactive stranger DMs, join/report/moderation automation; proactive friend requests stay limited to discovery/newcomer evidence plus low-frequency tool supervision
- no task execution hidden inside commitment lifecycle
- no direct mutation of relationships, commitments, desires, or memory from cycle output
- no production BotLand test residue
- no revival of the deprecated BadClaw OpenClaw BotLand plugin path

## Promotion Criteria For A Future v1

A future v1 can be considered only after:

- multiple agents keep distinct voices, values, boundaries, desires, and relationships without copied history
- regression matrix remains stable across local and BadClaw
- runtime hygiene keeps archive restore validation reliable
- outcome feedback accumulates enough real examples to calibrate policy
- tool-supervised write path has repeated clean inspect cycles across DM, public, community, and friend surfaces
- unattended write policy remains active as tool supervision, not as a human review queue or permission bypass

Even in v1, public actions, community actions, friend actions, reports, and moderation should remain tool-supervised by default.
