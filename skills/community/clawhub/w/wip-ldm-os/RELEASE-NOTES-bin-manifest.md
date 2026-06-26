# Bin ownership manifest + install-time self-heal + prepublish gate

## What changed

`~/.ldm/bin/` now has an explicit ownership model. Two declarers contribute entries:

- **LDM CLI** declares its own files in `package.json` under `wipLdmOs.binFiles`. Five files this release: `process-monitor.sh`, `ldm-backup.sh`, `ldm-restore.sh`, `ldm-summary.sh`, `backfill-summaries.sh`.
- **Extensions** declare in their `openclaw.plugin.json` under `binFiles`. None populated yet; Memory Crystal's follow-up PR adds `crystal-capture.sh`.

`lib/bin-manifest.mjs` aggregates at runtime. Three integration points consume it:

1. **`ldm install`** ... aggregation runs after the registry pass (`autoDetectExtensions`, `migrateRegistry`) and **before** `seedLocalCatalog`, `deployBridge`, `deployScripts`, and the heal walk. If two declarers claim the same name, install aborts before any of those side-effecting calls run. After deploy, the manifest is walked and any missing or non-executable file is restored from its declared `source`. The 2026-04-28 outage's failure class is now self-healing at install time.
2. **`ldm doctor`** ... section 3c (the cron-target health check from the previous release) replaces its hard-coded `knownSources` map with a manifest-driven lookup. Same diagnostics; broader coverage.
3. **`prepublishOnly`** ... `scripts/validate-bin-manifest.mjs` runs before `wip-release` can publish. Each declared `source` must exist in the package, no internal duplicates, `name` must be a basename. A broken declaration cannot reach npm.

## Why

The 2026-04-28 capture outage exposed `crystal-capture.sh` going missing while cron kept firing. The manifest design was decided in PR #717. This is the implementation: layers 1 and 3 of the release-blocker plan (per-package validator + runtime enforcement). Layer 2 (cross-package CI gate against published manifests) lands as a follow-up workflow.

## What this does NOT do

- **Memory Crystal `binFiles` declaration.** That's a follow-up PR on `memory-crystal-private` that adds `binFiles` to `openclaw.plugin.json` and resolves the `ldm-backup.sh` ownership decision (LDM CLI keeps it, MC stops shipping its copy).
- **Cross-package CI gate (layer 2).** Requires a known-extensions registry to fetch from. Filed separately.
- **`imsg` binary ownership.** Stays a known foreigner until owner is identified.

## Tests

- `npm run test:bin-manifest` ... 35 assertions across 8 suites covering aggregator, healer, validator, integration heal, and pre-write conflict abort.
- `npm run test:doctor-cron-target` ... updated to seed declared extension and exercise manifest-driven lookup.
- `npm run test:ldm-install-bin-shim` ... unchanged; foreigners still untouched.
- `npm run validate:bin-manifest` ... validates this repo's own declarations.

## Real-world note

Running this against the actual install during development surfaced a real missing target: `~/.ldm/bin/process-monitor.sh` was absent. With LDM CLI's `wipLdmOs.binFiles` now declaring it, `ldm install` (or `ldm doctor --fix`) will restore it from `bin/process-monitor.sh` automatically. The outage class that started this thread is now closed for both extension-owned and LDM-owned files.
