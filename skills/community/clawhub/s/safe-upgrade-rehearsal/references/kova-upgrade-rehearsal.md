# Stateful upgrades with Kova and OpenClaw

Use this reference when an upgrade can migrate state, change plugin loading,
or when importing Kova evidence. The skill owns package preflight and evidence
verification. Kova owns scenario execution; OCM owns disposable environments;
OpenClaw is the product under test.

## Verified upstream boundary

Checked against Kova `14589997967d0ce0f1531ea2d030d6ed5b4c975a`:

- [report contract](https://github.com/openclaw/Kova/blob/14589997967d0ce0f1531ea2d030d6ed5b4c975a/docs/REPORT_SCHEMA.md)
- [target identity](https://github.com/openclaw/Kova/blob/14589997967d0ce0f1531ea2d030d6ed5b4c975a/src/target-identity.mjs)
- [upgrade state invariants](https://github.com/openclaw/Kova/blob/14589997967d0ce0f1531ea2d030d6ed5b4c975a/src/evidence/upgrade-existing-user.mjs)

`kova.matrix.run.receipt.v1` points to `kova.report.v1`, a bundle, and its
checksum. Every executed record must agree with the report's
`kova.target.identity.v1`. Exact `npm:<version>` targets can bind the installed
core artifact through npm integrity. Moving selectors and local builds may
have no supported exact identity and remain incomplete in this importer.

An exact core artifact does not attest add-ons, local patches, production
configuration, or copied state. The output marks its scope
`core_npm_artifact_only`; `target_candidate_root` identifies the comparison
target, not proof that its entire composition ran in Kova.

The report's `platform` comes from the Kova process. It cannot prove the target
Node/npm/libc combination. Policies requesting `environment-matched-rehearsal`
remain incomplete until an upstream target-environment contract is supported.
The example policy omits that claim while retaining the existing preflight
environment gate. No canonical preflight gate is waived by importing evidence.

## Plan and import

For an already installed Kova, inspect a JSON plan first:

```bash
kova matrix plan --profile smoke --target npm:<exact-version> --json
```

Choose scenarios from the current inventory for the actual installation.
The bundled example requires `upgrade-existing-user`, `release-runtime-startup`,
`official-plugin-install`, `plugin-lifecycle`, `mcp-runtime-start-stop`, and
`mcp-tool-call`; a smoke profile alone need not contain them all. Missing
scenarios remain incomplete. Read Kova's `kova-operator` and `ocm-operator`
instructions before separately authorized execution. `--execute` is a lab
mutation; durable environments are clone sources only.

Import the saved matrix receipt with the command in SKILL.md. Keep the receipt,
report, tar bundle, and checksum together or preserve their referenced paths.
The importer verifies the outer checksum, indexed members, identical bundled
report, summaries, scenario ledgers, and candidate identity. It writes only
sanitized identifiers, status, and hashes. It never executes Kova.

The importer accepts only execution evidence with every required scenario and
ledger proof passing. `DRY-RUN`, `SKIPPED`, `BLOCKED`, `INCOMPLETE`, and failures
cannot become success. A checksum proves consistency, not an independent
signature of the producer. Use artifacts from the lab you intended to run.

## Method learned from stateful upgrades

1. Close the exact candidate, including plugin provenance and ordered local
   patches. Follow the installation's supported OpenClaw update path. Compare
   it with Kova's actual scenario commands before claiming path parity.
2. Quiesce writers and rehearse on a faithful disposable copy. Include every
   agent database, SQLite WAL/SHM sibling, session tree, scheduled job, and
   declared mutable surface. Kova's bounded state snapshots alone do not
   establish a complete backup. Cloning alone does not establish no-egress;
   verify network isolation before starting a copy with real identities.
3. Run the actual target CLI paths on the copy, including plugin installation
   and first startup. Even a validation command can trigger migration. Compare
   semantic state and schema invariants; permit only explained bookkeeping
   changes. The bundled policy requires preservation invariants, not merely
   the presence of before/after snapshots.
4. Drill each supported restore path on a fresh copy, verify all restored state,
   and measure duration with margin. A backup checksum, snapshot count, or a
   scenario title containing "recovery" is not lossless rollback proof.
5. After separately controlled activation, prove new work is accepted and a
   correlated reply completes. A `ready` log, cron activity, or absence of
   errors before the first agent turn is insufficient. Keep the probe in the
   repository and bind results to the service start being checked.

## Recovery boundary

| Observed boundary | Required disposition |
| --- | --- |
| Runtime files changed; state untouched | Restore the exact declared runtime mutation set. |
| State migrated; no new durable work accepted | Restore only a fresh, verified snapshot covered by the same-window rollback proof. |
| New work accepted or durable scheduled writes occurred | Preserve current state; forward repair or contain. A stale snapshot would discard work. |
| Boundary unknown | Block automatic rollback and determine the state first. |

Record these facts in the existing [phase handoffs](phase-handoffs.md).
Avoid restarting a baseline merely to retry a stale rehearsal: the restart
can itself mutate state and invalidate the proof again. After a repair, repeat
the failed user path. Admission rejected as draining after `ready` is a failure
unless a known restart window is actively in progress.

## OpenClaw installation compatibility

The entrypoint uses the documented `{baseDir}` substitution, standard
`metadata.openclaw.requires.bins`, and normal model/user invocation. Keep Kova
optional so offline package inspection works without it. Follow the current
[OpenClaw skills contract](https://docs.openclaw.ai/tools/skills) and
[update guide](https://docs.openclaw.ai/install/updating) for installation shape
and loading. Reinstall a local/Git skill to refresh it; registry update commands
track ClawHub installs. Capability acceptance remains an explicit operator
decision bound to the reviewed changes.
