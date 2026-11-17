# Agent flavors and Command Center extensions

Status: the initial business-operations flavor and explicit Node selection/collection
CLI are implemented. Base install/upgrade commands do not select flavors. See the
[runbook](../../flavors/business-operations/README.md) for supported operations and limits.

## Decision

Spacesuit owns reusable agent flavors. Command Center owns universal OpenClaw
monitoring and the generic extension host. Flavors compose workspace conventions,
optional domain collectors, panel definitions, translations and workflows; they do
not fork the dashboard or replace the OpenClaw runtime.

Keep the base scaffold generic. Command Center works independently out of the box;
Spacesuit is its highly recommended companion. Spacesuit can scaffold and collect
without Command Center but **has no human-agent interaction UX on its own**. Command
Center provides the dashboard interface. This does not promise a chat composer.

## What belongs here

- Generic flavor definitions such as personal-assistant, engineering, research or
  business-operations. Business operations is shipped; the others remain illustrative categories.
- Reusable domain extensions (first candidates: Intel, Pipeline, Monetization).
- Extension-specific schemas, collectors, fixtures, panel definitions and locales.
- Flavor defaults and workspace workflows that explicitly select extensions.

Real agent names, hostnames, account IDs, customer information, business records,
credentials and local configuration remain in private workspaces. A public flavor
is a reusable capability set, not a copy of someone's workspace. Credentials are
configured outside manifests using the host's credential mechanism.

Generic gateway/host health, sessions/subagents, recent messages, quotas, costs,
cron/jobs monitoring and shared transport/i18n stay in Command Center. Domain
interpretations of those data can be optional flavor panels, but must not take
over core endpoints or make session monitoring dependent on Spacesuit.

## Package ownership and layout

Manifests under `flavors/` and `extensions/` are consumed by the explicit CLI.
Collectors are reviewed shared code under `lib/flavors/`, not executable paths in
manifests. Per-extension tests are consolidated in `tests/flavors.test.js`. The
long-term organization remains:

```text
flavors/
  <flavor-id>/
    manifest.json         # flavor version, selected extension IDs, defaults
    README.md             # purpose, inputs, compatibility, upgrade/rollback
extensions/
  <extension-id>/
    manifest.json         # core contract version, panel IDs, declared data inputs
    collectors/           # reviewed, separately invoked data producers
    locales/              # namespaced translations
    tests/                # synthetic fixtures and domain regression coverage
```

A flavor is composition, not copied extension code. Multiple flavors may select the
same extension. Start with one explicitly selected flavor per profile/agent and
local overrides; defer layered flavor precedence until there is a demonstrated need.

Command Center is the source of truth for the extension contract/schema. Each
Spacesuit extension declares compatibility and its own version; package versions
must be pinned as a compatible pair for upgrades and rollback. The initial host
supports read-only structured cards/tables, not arbitrary executable browser code.

## Per-instance activation and isolation

The explicit CLI offers preview before writing; base installation does not select a flavor. Installation is not
authorization to start collectors, schedule work, enable controls, or deploy changes.

- Select flavor and enabled extension IDs explicitly for the target profile, agent
  and workspace. Do not infer selection from usernames, hostnames or directory names.
- Store selections and private bindings in workspace-local configuration, not the
  Command Center source checkout or a global machine-wide switch.
- Validate contract compatibility, unique namespaced IDs, locale keys, and data roots.
  Reject invalid/incompatible packages with an actionable diagnostic.
- Preserve user overrides outside managed sections and never overwrite custom files.
- Absent or disabled flavors leave the core dashboard functional. Disabling stops
  collection and presentation without deleting artifacts.

Collectors publish bounded structured snapshots separately from dashboard requests.
Snapshots declare observation time and availability; missing data is unavailable,
not zero. Core validates, escapes, redacts and renders them using shared routing,
state and transport. Do not introduce per-panel SSE streams or share caches across
profiles. A malformed or slow extension must not stall the session or cost panels.

A manifest is not a security sandbox. v1 must not execute arbitrary paths, shell
commands, remote scripts or raw HTML from package metadata. Collector installation
and invocation require the normal code-review and runtime-permission boundaries.

## Localization and maintenance

Preserve `data-i18n` attributes and translation keys when migrating panels. Move
extension-specific strings and English/Chinese locales with the extension; do not
copy domain strings back into core. Test language changes while panels are open,
including loading, empty, stale, unavailable and error states.

Keep the generic base/template content synchronized. Flavor-managed sections must
have explicit ownership and never nest or collide with existing `SPACESUIT` markers.
Exact marker naming and merge rules are deferred to the installer implementation.

## Incremental migration and acceptance

1. Record the paired ownership decision; do not alter current installed behavior.
2. Build the generic Command Center host and validate a synthetic read-only extension.
3. Extract Intel, Pipeline and Monetization from Command Center, retaining contributor
   attribution, license notices, parser fixtures and injection regression tests.
4. Implement flavor preview/selection/upgrade/rollback; test fresh and established
   workspaces, missing/incompatible extensions, and preservation of private overrides.
5. Pilot one instance, then another profile with a different flavor; verify shared
   core functionality and data isolation before expanding.
6. Remove legacy built-ins only after compatibility and migration gates pass.

For existing installations, keep legacy panels until the user explicitly migrates
or a documented compatibility policy applies. Do not silently remove data or panels.
Acceptance requires core-only operation, no cross-profile reads, English/Chinese
switching, root/prefixed routing, bounded failed collectors, and reversible upgrades.

The companion [Command Center boundary](https://github.com/jontsai/openclaw-command-center/blob/main/docs/architecture/core-and-flavors.md)
contains the extraction map and host contract proposal. Links resolve after the
companion documentation merges; they do not imply the runtime is implemented.
