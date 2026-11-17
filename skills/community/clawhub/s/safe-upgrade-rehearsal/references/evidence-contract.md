# Evidence Contract

The safe-update rehearsal is a read-only package compatibility check. It does not prove live runtime behavior and cannot authorize an update.

## Inputs

- Exact current and target versions for each package.
- Registry metadata containing package name, version, `dist.integrity`, and `dist.shasum`.
- Current and target package archives downloaded without installation.
- Current and target OpenClaw dependency closures resolved with an isolated npm configuration, lifecycle scripts disabled, and exact Node, npm, OS, architecture, and libc identity.
- A customization manifest describing deployment-specific compatibility checks, unless the operator explicitly confirms a vanilla deployment.
- An installation coverage profile declaring the runtime Node version, required surfaces, their customization evidence, and concrete post-upgrade checks.
- An installation contract declaring every capability, component, contract, dependency edge, and separately distributed artifact identity.
- A fresh local installation attestation bound to the current composed candidate root.
- Conservative inputs containing only hash-bound named gate evidence and optional operator escalations. They cannot waive machine findings or set a verdict.

## Outputs

Every JSON output includes `effect: read_only_openclaw_update_rehearsal`, `runtime_effect: none`, `external_effect: npm_registry_read_only`, `external_write_effect: none`, `production_apply_allowed: false`, and `operator_approval: false` where applicable. Package fetches are network egress pinned to `https://registry.npmjs.org`, but they do not write to external systems.

`runtime-truth.json` records exact package coordinates and integrity validation.

`core-candidate-lock.json` records canonical SHA-256 roots for the current and
target resolved OpenClaw core closures. It includes exact transitive, peer, and
optional package identities, integrity values, platform selectors and
selection results, resolver policy, and toolchain/environment identity. Missing
integrity, mutable links, unsupported lockfiles, non-registry resolutions,
truncated closure data, or current/target environment drift fail closed.
Lifecycle scripts are declared and hash-bound by package integrity but are
never executed during resolution.

`installation-candidate-lock.json` composes the core closure with the
canonical installation contract. Its current and target roots bind every
declared component once, including all of its roles, contracts, dependency
edges, exact artifacts, relevant environment, analyzer version, and
composition policy. External plugin, sidecar, add-on, configuration, and
personalization artifacts must use `<name>@<exact-version>#sha256:<digest>`.
Missing, floating, duplicate, or unsupported artifacts fail closed.

`installation-attestation.json` keeps observation, freshness, and completeness
as separate axes. It is generated from an explicit local observation spec and
binds sanitized component names, types, digests, and service config pointers
to the current composed candidate root. Local paths are never emitted.
Configuration and personalization paths are checked structurally without
opening their contents. Content hashing is permitted only for declared
package, add-on, sidecar, and external-asset files. Missing observations,
unexplained residue, undeclared service config pointers, an expired artifact,
or a candidate-root mismatch fail closed.

`conservative-gates.json` applies a stable deterministic policy to the complete,
unbounded authority diff. Unknown closure, stale/incomplete attestation,
lossy input, and unknown optional/native selection block directly. Migration,
lifecycle/download, rollback, environment, SDK, service, permission, protocol,
and channel-crypto changes require named hash-bound evidence. Resolved closure
drift is always conservative. Human-facing member lists may be truncated, but
they never authorize this decision.

`impact-shadow.json` is a non-authoritative attachment. It maps the complete
closed-candidate diff to declared components, capabilities, contracts, and
hypothetical namespaced checks while preserving every unmapped member and
package. Its `would_omit_checks` list is structurally empty. Deleting the
artifact or running with `--disable-impact-shadow` leaves the canonical
decision content, digest, required evidence, and verdict unchanged. It is not
part of `evidence-bundle.json`.

`analysis-cache.json` records a canonical rehearsal-input digest and
content-addressed cache provenance for the `archive`, `contract`, `policy`, and
`shadow` namespaces. The full digest binds composed candidate roots,
installation contract, attestation, conservative inputs, deterministic policy,
analyzer version, semantic options, and deterministic core, package, coverage,
and customization analysis. Cache hits and misses are operational
metadata outside canonical decision content. The cache root is private to the
current user, entries are authenticated with a cache-local integrity key, and
unsafe filesystem ownership, permissions, or symlinks disable reuse. Corrupt,
tampered, partial, stale, or version-mismatched entries are ignored and
recomputed; no worker or external review output is cacheable authority.

`archive-execution.json` is non-authoritative execution telemetry for pure
archive analysis. It records the bounded worker count, configured timeout,
input-ordered unit statuses, and wall-clock durations. A failed or timed-out
unit still blocks through the existing runtime and package evidence. Each unit
runs in a killable subprocess, so a timeout cannot produce a late cache write; worker
count and timing never enter `decision_content`, `decision_digest`, or
`evidence-bundle.json`.

`advisory-input.json`, `advisory-result.json`, and
`advisory-attachment.json` are optional, public-safe, non-authoritative
artifacts produced outside `simulate`. The input verifies the status-bound
evidence bundle, binds the target candidate and exact source artifact digests,
baseline check definitions, bounded structural facts, and fixed output limits.
It excludes raw package prose. Evidence references resolve only against the
digest-bound advisory input content, not arbitrary source paths. A result is
accepted only when its input digest, source references, namespace, shape,
byte size, collection and text limits, and immutable false authority flags
validate. Existing archive inspection already supplies decompressed-byte,
member-count, duplicate-path, parser-time, and nesting limits before these
facts are prepared. A suggested check that
collides with a baseline ID must reproduce the baseline definition and
evidence digests exactly; otherwise it is rejected. Accepted advisory output
has `canonical_status_effect: none`. Missing, malformed, timed-out,
conflicting, or digest-mismatched output cannot change canonical status,
remove evidence, improve a verdict, or enter the analysis cache. Worker
agreement carries no confidence semantics.

`synthetic-update.json` records archive safety, package identity, bounded added, removed, and changed member lists, plus current-to-target changes in Node engines, dependencies, optional and peer dependencies, lifecycle scripts, and executable declarations. Changed lifecycle scripts and incompatible or unproven Node requirements block the rehearsal.

`customization-compatibility.json` records every requested customization check and its result. Missing members, unreadable text, or absent anchors fail closed.

`coverage-report.json` records every declared installation surface and verifies that required surfaces have post-upgrade checks and that referenced customization checks exist and passed.

`post-upgrade-e2e.json` is a generated test plan. Its checks remain `not_run`; generation is not proof of live behavior.

`evidence-bundle.json` binds the evidence artifacts by SHA-256. A downstream gate may translate this bundle to its own schema, but must preserve failures and the no-approval state.

`verdict.json` is the single authoritative preflight status using schema
`openclaw.safe_update.status.v2`. It has only two valid outcomes:

- `blocked`: required evidence or compatibility checks failed.
- `ready_for_operator_plan`: package-level evidence passed; prepare a rollback-aware plan and request separate approval for any live mutation.

Its timestamp-free `decision_content` is bound by `decision_digest`. Volatile
run metadata, evidence paths and hashes, and operator-facing prose do not affect
that digest. The status is always `phase: preflight`,
`post_activation_e2e: not_run`, `production_apply_allowed: false`, and
`operator_approval: false`.
The authoritative status repeats exactly one current and one target composed
candidate root; it does not treat a list of loosely related hashes as the
installation identity.

The embedded, non-authoritative `compatibility_view` preserves the previous
`openclaw.safe_update.verdict.v1` payload for v1.1 consumers. It is derived from
the v2 status and cannot override it. There is no parallel
`upgrade-status.json`.

`summary.md` is a human-readable view and is not authoritative over the JSON artifacts.

`operator-plan.md` binds the target and evidence into a review surface, lists the still-missing operator inputs, and stops before apply.

## Non-Claims

A green rehearsal does not prove:

- Signal or Matrix inbound and outbound behavior;
- read receipts, reactions, attachments, or voice transcription;
- MCP discovery and calls;
- provider authentication or quotas;
- memory, persona, or conversation continuity;
- systemd, container, filesystem ownership, or gateway behavior;
- rollback against live persistent state.

Those surfaces require fresh post-deploy E2E evidence during an approved maintenance window. The coverage profile and generated operator plan must enumerate them explicitly.

## Installation Coverage Profile

Schema: `openclaw.safe_update.coverage.v1`.

The supported 1.1 install shape is `npm_global_linux`. `runtime.node_version` must be an exact version, and `runtime.os`, `runtime.arch`, and `runtime.libc` must explicitly identify the target platform. The declared platform must match the core candidate closure. Every surface requires a unique `id`, a supported `category`, a boolean `required` flag, a list of customization check IDs, and a list of concrete post-update checks. A required surface with no post-update check is blocked.

Supported categories are `channel`, `plugin`, `mcp`, `memory`, `persona`, `provider`, `service`, `attachment`, `voice`, and `other`.

The profile is a declaration of expected behavior, not an automatic discovery claim. The `inventory` command deliberately does not read secrets, configuration values, conversations, or service state.

## Customization Manifest

Schema: `openclaw.safe_update.customizations.v1`.

Each check requires:

- `id`: stable unique identifier;
- `package`: npm package name;
- `kind`: `required_member` or `member_contains`;
- `member`: exact tar member path.

`member_contains` additionally requires a non-empty `needle`. It is restricted to regular text files no larger than 4 MiB.

Archive paths must be relative, must not traverse outside the package root, and must not be links. Unsafe archives are blocked before customization checks run.
