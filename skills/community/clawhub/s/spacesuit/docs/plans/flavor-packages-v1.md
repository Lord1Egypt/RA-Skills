# Flavor packages v1 implementation plan

## Goal and boundary

Command Center runs standalone. Spacesuit is its highly recommended companion for
workspace conventions and optional agent flavors, but has **no human-agent
interaction UX on its own**. Command Center provides the UI; this release does not
implement chat composition or mutate OpenClaw sessions.

## Implemented slice

- Explicit `business-operations` flavor composing three pinned 1.0.0 extensions.
- Reviewed dependency-free Node CLI: preview, apply, collect, core disable, restore.
- Identity-bound workspace selection and snapshots following Command Center v1.
- Atomic per-file publication, bounded reads, nofollow/symlink rejection, safe error
  outputs and a workspace operation lock. No network, shell execution or scheduler.
- Extracted table/parser behavior with MIT attribution and regression coverage.
- Structured bilingual read-only tables and metrics. No raw HTML or manifest code.
- No changes to workspace scaffold templates or managed skill instructions.

## Acceptance and rollout

Run `make test` with Bash 4+ and Node 18+. Validate generated synthetic snapshots
against the paired Command Center host. Check core-only operation, missing data,
profile mismatch, symlink rejection, blank cells and injected HTML strings. Verify
English/Chinese root and prefixed dashboard rendering in the companion PR.

No live selection or collection occurs during this implementation. Existing users
keep legacy panels until explicit migration. Pilot by preview/apply/collect for one
instance, verify all three panels, then test another isolated workspace/profile.
Disabling or restoring must preserve source data and private selection overrides.

## Deliberate limits / follow-up

One selection per workspace; separate profile workspaces are required. Fixed input
conventions only; configurable bindings and multi-flavor precedence are deferred.
Selection backups do not include snapshots or source data. Three snapshot renames
are individually atomic, not one cross-file transaction. Human-agent interaction
controls beyond the existing dashboard are not implied by companion branding.
