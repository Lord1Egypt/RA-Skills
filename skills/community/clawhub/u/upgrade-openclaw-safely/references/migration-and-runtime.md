# Storage migrations, private runtimes and legacy drivers

Read this reference when discovery identifies schema migration, physical stores outside the configured Agent list, case aliases, runtime replacement or an installed-driver limitation. The steps below are conditional; a small same-schema update does not require all of them.

## Recovery coverage before production mutation

Create a source inventory before selecting backup commands. For each required source record owner, logical role, physical path/identity, backup method, recovery destination, verification and explicit exclusions.

Inventory configured agents AND discovered stores. Include shared state, affected Agent SQLite, unregistered historical/placeholder stores, native plugin databases and sidecars, referenced legacy session archives, credential/config includes, service definitions/environment/wrappers, and recoverable old core/plugin payloads. Use plugin backup-resource declarations to distinguish required from regenerable state. Unchanged workspaces can be excluded by a documented policy; that does not exclude migration sources living beside agent directories.

Compare the inventory to the verified manifest before the gate passes. File count, a successful native command and a config-only archive do not prove coverage. Native backup refusal for an unregistered ID is a coverage limitation; use an equivalent approved consistent backup instead of registering the Agent.

For live SQLite, use the supported online snapshot or a documented quiesced procedure including committed WAL data. Validate integrity and relevant counts with a reader compatible with the schema/extensions. A single incompatible cold-reader failure is not proof of corruption. Explain any cross-store consistency boundary; if a migration requires coordinated quiescence, take the final snapshot after verified writers stop.

Back up regular archive files consistently and read hashes back. Do not assume an archive directory is regenerable because the SQLite store is already populated. Restore tests target independent scratch locations and never overwrite production.

Independent recovery objects must survive deletion of candidate/rehearsal directories. Refresh the final cutover snapshot after preparatory runtime/path changes when needed. If coverage is discovered incomplete after mutation, preserve originals and all recovery material; do not call the set complete or clean it until the missing data's recovery relationship is proven.

## Physical identity and case aliases

Compare realpath and device/inode or the platform's file identity. Two strings differing only in case can be one file on a case-insensitive volume; similar strings can also be distinct stores. Do not deduplicate by lowercasing names.

Detect configuration aliases and database-registry aliases separately. Report the exact paths/rows and why they conflict before requesting any genuinely missing authority. A path normalization, source-directory rename and registry-row removal are different operations. Do not turn an approved one-row repair into a reusable automatic SQL deletion recipe.

If such a repair is authorized, preserve the pre-repair snapshot, constrain the exact target, verify the affected count and final integrity/registration, and leave Agent content, model and route identity intact.

## Private Node preparation

Discover target runtime requirements and the installation's supported private-runtime discovery locations. Verify official source/checksum and architecture. Do not hardcode one historical Node version or change system Node/shell profiles when a private runtime was selected.

Record both shell CLI and actual service/Gateway executable. A launcher can retry into a private Node while launchd still holds cached old arguments. Reading a changed plist or running CLI --version alone does not prove the service switched.

For an authorized multi-stage plan:
1. Install the verified private runtime and change only reviewed runtime/service fields.
2. Drain active work and apply the supported lifecycle operation; verify the old OpenClaw under the new Node from the actual process and workflow baseline.
3. Refresh the final recovery set, then perform the core activation under one owner.
4. Verify ordinary CLI reuse and live process identity after activation.

Prefer restart/reload when sufficient. If evidence proves it only kickstarted cached arguments, select the supported controlled re-registration/reload within the approved phase; do not repeat the ineffective action. Service reconstruction or broader definition changes need their own authority.

Managed wrappers can receive a new official template. Compare argument semantics, environment values, ports and heap limits separately from formatting or wrapper-byte changes. Retain before/after evidence and disclose template changes; do not blindly restore an obsolete wrapper merely to match its hash.

## Documented external package fallback

Use only when the installed driver cannot safely complete the reviewed operation and current official documentation explicitly supports an external procedure. Preconditions:

- Verified installation ownership/profile/state identity and exact target, with compatible runtime.
- Complete independent recovery coverage and any warranted isolated migration rehearsal.
- Genuine execution outside the target Gateway and a plan covering service stops, migration/convergence, activation and failure limits.
- No active or ambiguous updater competing for the same installation; no denied authority being bypassed.
- No unresolved migration/lease failure being treated as a package-manager problem.

Follow the current package manager's documented exact-version procedure in the existing prefix, one successful step at a time. Preserve registry semantics rather than leaving a permanent dependency on a temporary tarball path. Never silently replace npm/git/Brew ownership, install another moving channel or run parallel lifecycle repair.

Record one logical core replacement, actual installed version even on nonzero exit, and all later phases. If the core reaches target, any supported official same-version convergence is a maintenance phase with its own admission/result evidence. Recheck exact-selector safety immediately before that phase. Do not rerun a package replacement to finish plugin migration.

On failure follow the user's preservation policy. Database restore and agent-initiated downgrade remain separately authorized; never assume package rollback can undo newer schemas.

## Budgets and rehearsal boundaries

Inspect the installed driver's hard ceiling, per-step timeout, Gateway cold-start budget, read-only RPC timeout and user stability window separately. Larger --timeout values do not override an independent hard cap.

Rehearse copies with real channels, outward-delivering automations and unintended external access disabled. Verify production paths cannot be written; rebinding just the config filename is insufficient. Do not present a canary snapshot as the independent rollback set.

Use rehearsal timings to plan, while allowing for production-only session/history/index checks. Record real maintenance boundaries; a later already-current native run can legitimately report zero native downtime while earlier manual preparation stopped service.

Historical example, not defaults: an upgrade from 2026.9.4 to 2026.9.36 had a 300-second installed-driver ceiling, a 384-second canary Doctor, and a roughly 112-second canary startup. These facts motivated a documented external path on that host. Future upgrades must rediscover versions, limits and supported commands.
