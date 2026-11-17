# Acceptance, observation and recovery retention

## Compare the correct state

Capture baseline and final semantic state from the authoritative owners: config/includes, actual service/process/runtime, plugin install/effective state, routes, provider readiness, memory/Wiki and SQLite-backed automation definitions/enabled flags. JSON equality alone does not prove task behavior is unchanged.

Classify differences:
- required/approved migrations and official template changes with preserved user settings;
- expected system-managed compatibility decisions, disclosed with their consequences;
- pre-existing degraded optional paths, separated from newly broken critical paths;
- unaccepted critical workflow loss, which blocks acceptance and cleanup.

For example, a new eligibility rule may disable an already-failing system-owned review job while its prior error and the rest of the automation definitions remain unchanged. Do not re-enable it to bypass the runtime contract, but do not call all schedules unchanged either. A newly disabled business automation needs its own impact/authority decision.

Keep database integrity and meaningful retained-data counts separate from derived index size. Migration can change physical layout. Do not infer data loss from file size alone or claim preservation from schema markers alone.

## Exercise the intended path

Critical plugins need an actual runtime-load or message-path probe supported by current help. Cold discovery is not load evidence. For host-bound official plugins, inspect every relevant convergence outcome, not only the core updater status.

A permitted minimal model request must record effective provider/model, rerouting and tool/delivery effects. Do not use a fallback success to certify an unavailable primary. Do not send external test messages, invoke every provider or trigger outward-delivering automations without the relevant authority/budget.

An aggregate auth/readiness command can fail because of an unused fallback while the selected primary works. Preserve the warning, verify the affected scope and report partial readiness honestly. Do not reset credentials, delete fallback entries or suppress errors to get a zero exit.

A live Gateway can be cold-starting beyond a CLI default. Refresh version, process/progress and logs; make bounded read-only probes inside the planned budget. A read-only Wiki RPC may support a different deadline from its wrapper CLI; discover the same method and semantics before adapting. Never retry an unknown mutating outcome as though it were a read.

For memory chunk/index notices, observe the documented automatic maintenance, verify search and final index identity, and avoid force-rebuilding or clearing caches as a first response. If a critical path remains unverified, report installed-but-acceptance-incomplete.

## Observe the whole agreed interval

Persist required duration, cadence, start, phase identity and a monotonic elapsed-time basis where available. Preserve every failure or lossless cumulative counters, version/build/process/path changes, fatal events and termination/update signals. A tail of recent successful samples cannot erase earlier failures.

Finish only after the full agreed interval and critical gates pass. Do not silently reset the start after a bad sample or shorten a user-selected window to a built-in default. Rehearsal, startup grace and post-activation stability are distinct intervals; report them separately.

Transient noncritical CPU/index warmup is not automatically a fatal event. Retain the evidence and distinguish availability/readiness failures from load notices; apply the accepted policy, not a blanket ignore rule.

## Cleanup only within authorized retention

Before deleting anything, confirm the user authorized the cleanup and retention policy. Prior authorization carries forward; do not ask again for the same proved-safe scope.

After acceptance and the full observation window:
1. Identify the exact recovery set to retain and verify its complete inventory, hashes/read-back and any promised independent restore test.
2. Prove it remains usable without candidate/rehearsal directories, including old program/plugin payloads and required archives/native state.
3. List exact paths owned by this run, why each is redundant, and exclusions. Check live process, service, plugin and recovery-manifest references before removal.
4. Retain historical, protected and unknown-origin materials. Do not infer ownership from a broad name glob.
5. Remove only the authorized, proved-redundant objects; record the manifest and scope.
6. Recheck ordinary CLI/runtime and Gateway health after cleanup.

If official cleanup cannot select this run's scope, do not apply global cleanup merely with --yes. This is especially important where it retires official rollback originals. A user's request to keep one complete set does not authorize deleting excluded protected/history artifacts.

If acceptance fails, a required backup is missing, a live reference exists or recovery is unresolved, preserve material and report the exact remaining gate. The user's failure policy takes precedence over cleanup convenience.

## Evidence and privacy

Keep configs, credentials and private diagnostics local. Reports should link bounded evidence without embedding tokens, credentials or private transcripts. Record from/target/actual versions, native/external case and phase IDs, maintenance timestamps, tested/untested workflows, compatibility differences, retained recovery material and exact cleanup result.
