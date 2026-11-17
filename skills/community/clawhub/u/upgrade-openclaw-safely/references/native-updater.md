# Native updater evidence and transport

Use the installed package's documentation and help first. Inspect docs/cli/update.md, its handoff/history references, docs/install/updating.md, and current backup/doctor/lifecycle commands. Rediscover command and schema support on each host.

## Select transport by actual capability

1. Prefer the official Gateway action for same-Gateway requests when exposed, authorized and able to enforce the reviewed target. Preserve trusted requester/session continuation.
2. Inspect the live schema. An observed update action may support requester, continuation and git target but no exact npm version. Do not fabricate a version/tag field.
3. If it cannot enforce the target, use documented managed CLI handoff with verified service identity, or a genuinely external operator context. background=true, nohup, a child agent or an exec-session ID does not prove survival.
4. Generic RPC is not a workaround for a denied action. Read-only RPC success proves access, not update authority.
5. If no supported restart-surviving transport exists, stop before mutation and identify the missing external execution step. Do not install a custom coordinator to satisfy an ordinary upgrade.

A ready, compatible coordinator that is already installed may be the sole owner when explicitly selected. Do not mix its ledger/lifecycle with native or manual mutation paths.

## Installed versus target behavior

A staged candidate cannot repair every limitation in the installed driver before package replacement. Inspect admission checks, hard validation ceilings, runtime requirements and schema fencing in the installed version as well as the target.

If a documented external fallback is necessary, read migration-and-runtime.md. Do not keep raising --timeout when the installed implementation has an independent hard ceiling.

## Exact target, channel and plugin intent

--tag can select a one-off package target; --channel persists policy. Effective extended-stable may reject a tag override. Use the discovered exact-selector contract, and stop if a moving selector can no longer enforce the reviewed version.

Already-current core maintenance can still converge plugins/config and repair eligible old official release pins. This is not permission to submit another core replacement. Verify that the maintenance mode/selector cannot admit a different core.

Official host-bound plugins can track the exact core or a documented base release cohort. Eligible old official pins can resume their default intent under the current contract. Preserve independent pins, custom registries and third-party ranges. User instructions to keep a particular pin take precedence; explain conflicts before changing it.

Do not use blanket plugin updates, numeric-version assumptions or --accept-capabilities to bypass review. A core success can coexist with individual plugin failures: inspect every relevant outcome and the effective runtime load.

## Durable result semantics

- accepted/skipped/managed-service-handoff-started means accepted, not completed.
- restart-health-pending remains pending. Handoff unavailable/failed is not success.
- Follow activeRun or the exact original run ID. runStatusError is unknown history.
- Where supported, update.runs.list/get or equivalent native status/report reads identify the original operation. A newer unrelated lastRun cannot close this task.
- A transport timeout, SIGTERM or exit 143 can be handoff. Inspect the original run before acting.
- Dry-run can write a skipped history record; it is not migration or restart evidence.
- Official package recovery is compatibility-checked and does not reverse database migration. Review its authority and report actual rollback, not target success.

Keep stdout attached where it carries handoff evidence. Do not chain shell commands that depend on surviving the Gateway shutdown. Construct argv/structured JSON safely and keep credentials out of logs and command arguments.

## Mutation and legacy boundaries

update repair may run Doctor/config/plugin mutations. update cleanup permanently gives up recovery originals. Neither is a read-only inspection action. --yes may approve a downgrade; do not use it as blanket authority.

Bundled upgrade-transaction.mjs and the old transaction/recovery contracts are retained for compatibility with historical records only. They are not the current execution protocol. Do not use their fixed lifecycle counters or rolling observation tail for a new upgrade, and do not edit old ledgers to lift restrictions.

Official documentation references:
- https://docs.openclaw.ai/cli/update
- https://docs.openclaw.ai/install/updating
- https://docs.openclaw.ai/cli/backup
