---
name: "openclaw-verified-upgrade"
description: "Assess OpenClaw releases, upgrade an installation, or recover a failed update using verified backups, official durable handoff and runtime evidence."
license: "MIT-0"
metadata:
  version: "2.0.0"
---

# OpenClaw Verified Upgrade

Treat an upgrade as an evidence-backed state transition. The selected package, running Gateway, plugin contracts, configuration, critical workflows and agreed stability window must all be verified.

## 1. Record intent and authority

- Upgrade intent authorizes discovery, verified local backup, reviewed standard migrations/plugin convergence, managed activation and verification. Carry existing approval forward; do not add a duplicate confirmation for the same scope.
- Assessment is read-only. Skill maintenance authorizes skill changes and offline validation, never a host update/restart as a test.
- Record the exact target, requested channel/persistence, runtime changes, allowed tests, interruption plan, stability window, backup retention and failure/recovery policy. A one-time upgrade does not authorize auto-update/cron policy changes or coordinator installation.
- Ask only for genuinely new scope: an actual downgrade, widened plugin capabilities, unresolved high-impact migration, an unaccepted degraded baseline, service reconstruction, credentials, destructive cleanup or unsafe rollback. Explicit stop/preserve instructions override automatic recovery.
- Respect current owner/auth/exec policy. Never invent requester identity, reset approval records or use another transport to bypass a denied action.

## 2. Discover the actual installation and baseline

Read installed help before version-sensitive commands. Record CLI realpath/version, package manager/root, config/profile/state identity, service definition, live Gateway build/PID/path, actual Node executable, plugins and install intent, channels, agents/routes/providers, active work, free space and update settings.

Read durable active/last runs; unknown history is not empty history. Follow the original active run rather than competing. Resolve shell/service/process identity mismatches before mutation. Do not silently change npm/git/Nix/Brew ownership.

Record pre-existing failures and authoritative state outside JSON configuration, including SQLite-backed automation definitions and enabled status. Identify configured agents separately from physical stores and plugin-owned native state.

Read [native-updater.md](references/native-updater.md) for transport and result semantics. For SQLite migrations, private runtimes or legacy drivers, also read [migration-and-runtime.md](references/migration-and-runtime.md).

## 3. Resolve an exact target and review impact

Use authoritative releases, installed/target documentation and current selectors. Preserve explicit versions; do not substitute moving latest. Honor requested extended-stable semantics and recheck the selector immediately before admission. Persist a channel only when authorized.

Review runtime, schema, config, service, plugin, channel, provider/auth and feature changes. Unknown high-impact migration or a critical incompatibility blocks activation. Distinguish installed-driver limitations from candidate capabilities.

Check plugin origin, integrity/trust, pins, declared compatibility and capability changes. Let the official updater apply its documented host-bound release-cohort rules, including eligible old official pins. Preserve independently versioned/third-party contracts and explicit user pin constraints; numeric order alone proves neither compatibility nor failure.

If package/runtime/plugins already agree and are healthy, report already-current. Same-version official plugin/config maintenance is distinct from another core package replacement. Prove its target and effects before invoking it.

Preview execution only when supported and useful; a dry-run can write history and does not validate migration, providers or restart survival.

## 4. Verify complete recovery coverage before mutation

Build a required-source inventory and map every migration-relevant item to a verified recovery object: actual config/includes, credentials, shared and discovered affected Agent databases, unregistered historical stores, plugin-native state, associated archives, service/runtime metadata and recoverable old core/plugin payloads. State workspace exclusions explicitly.

Use supported WAL-aware SQLite snapshots, not ordinary copies of live database files. Equivalent consistent backups are allowed within the approved scope when the native command cannot cover a store; do not register historical agents just to back them up.

Verify scope coverage, manifests/hashes and read-back, not merely command success or file count. A rehearsal copy is not the independent recovery set. If restore validation is required, use a separate destination; verification never authorizes overwriting production.

No core mutation until all required coverage passes. Keep private material local. If a new gap is discovered later, preserve originals and backups, disclose the gap and freeze cleanup until recovery coverage is independently proven.

## 5. Choose one lifecycle owner and execute approved phases

Announce the concrete target, risks, backup, interruption stages, checks and recovery limits, then proceed within existing authority.

Prefer the official durable updater able to enforce the reviewed target. Use a documented managed handoff or an execution context genuinely outside the target Gateway. Do not invent unsupported version parameters, requester identity or restart-survival guarantees.

The official updater normally owns staging, migration, convergence and activation. Do not add a parallel restart or replacement command. Use a documented external package-manager fallback only under the conditions in migration-and-runtime.md; never as an improvised retry of an active or ambiguous update.

When approved runtime preparation is needed, record it as a separate phase, verify the old host under the new private runtime, refresh the final backup and then activate the core. Budget necessary service actions per approved phase, not one arbitrary action for the whole upgrade. Never clear counters, locks or run history to obtain another attempt.

Submit one logical core replacement attempt. A lost response is not permission to repeat it. Record case/run identifiers, exact target, installation identity, phase/action results and real maintenance timestamps. Map external phases to native run IDs when available; never fabricate a native ID.

Do not default to --no-restart; use it only when an approved phase/lifecycle owner will complete activation. --yes can accept downgrades; --accept-capabilities widens trust. Neither substitutes for the relevant authority. Never install or repair a coordinator implicitly.

## 6. Resume and verify the same operation

Read the original run ID and phase after interruption. A newer unrelated lastRun is not evidence for this task. Observe within recorded phase budgets without silently resetting deadlines or issuing another mutation.

Verify fresh evidence:

- CLI/package and live Gateway build/path equal the reviewed target; actual Node/process, service, port, RPC and application readiness agree.
- Configuration and required databases pass validation/integrity checks; compare meaningful data counts where migration warrants it.
- Plugin install/effective versions satisfy their contracts, and critical plugins actually load at runtime.
- Channels, routes, provider/auth and essential memory/Wiki/automation configuration remain available relative to the accepted baseline.
- Permitted minimal E2E checks exercise the intended route. Record effective provider/model and rerouting; a successful fallback cannot conceal a broken primary.
- Compare semantic changes in all authoritative stores. Explain expected system-managed changes; unaccepted critical workflow loss blocks acceptance even when the updater exits zero.

A live process after a short start-command timeout may still be starting. Refresh progress and use bounded read-only probes; do not repeatedly restart. Aggregate readiness/auth exit codes require diagnosis against the affected route and baseline, not credential resets to make everything green. For memory maintenance notices, observe supported automatic convergence and recheck the final index identity before considering a manual rebuild.

Keep paid/external effects within authorization. Do not send channel messages or run outward-delivering automations merely to test an upgrade. Mark critical E2E evidence missing when it could not be obtained.

## 7. Observe the agreed window and retain evidence

Use the user's agreed duration and cadence. If unspecified, three real readiness samples spanning at least 120 seconds are a starting policy, not a universal duration. A longer agreed window must be completed in full.

Preserve start/end, stable process/build/path identity, all readiness failures, fatal errors and unexplained termination/update activity over the whole window. Keep full samples or lossless cumulative summaries; a rolling tail must not discard earlier failures or replace the original start time. A new observation phase requires an explicit recorded reason and must respect the failure policy.

Record the actual maintenance interval separately from a native run's reported downtime, especially for external runtime/core preparation or an already-current maintenance run.

Before cleanup or final acceptance, read [verification-and-retention.md](references/verification-and-retention.md).

## 8. Route failures and report accurately

Refresh installed/runtime versions, original run state and bounded logs before recovery. Adapt a command mismatch once only when no mutation was admitted. Back off bounded read-only/network probes within the original budget. Unknown ownership, active migration locks, partial migrations or exhausted budgets freeze mutation; do not remove locks or invent a new run.

Target installed plus later failure means post-update recovery, not another core install. Inspect plugin compatibility, convergence, integrity and capability consent before blaming Node/cache/OAuth. update repair can mutate Doctor/config/plugin state; it is not a status command.

Never automatically restore databases/config, force-install services, reset credentials, disable plugins or purge state as a recovery shortcut. Review official compatibility-checked package recovery against the user's policy before admission and report its actual outcome.

Report success / already-current / installed-but-unverified / rolled-back / blocked / failed, from -> target -> actual runtime, native or external case/run IDs, backups, semantic differences, critical checks, observation evidence, cleanup and remaining action. Terminal updater success alone is insufficient.

Validate skill changes using [offline acceptance scenarios](examples/acceptance-scenarios.md), never a live upgrade.
