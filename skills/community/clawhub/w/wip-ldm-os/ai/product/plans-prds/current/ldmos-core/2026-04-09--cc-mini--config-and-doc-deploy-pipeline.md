# Ticket: Config Files and Documentation Deploy Pipeline

**Date:** 2026-04-09
**Author:** cc-mini (with Parker)
**Status:** ticket
**Repo:** wip-ldm-os-private (installer)

## Problem

Five config files live at `~/.ldm/` root. Two are used by code, three are unused. None have documentation about how they get deployed, updated, or automated. The installer deploys some of them but there's no clear pipeline for keeping them current.

## The five files

| File | Used? | Deployed by installer? | Auto-updated? |
|---|---|---|---|
| `config.json` | Yes | Partially (harnesses section) | Harnesses only |
| `catalog.json` | Yes | Yes (seeded from npm package) | On self-update |
| `change-dependencies.json` | No | Yes (from shared/) | Never |
| `config-dependencies.json` | No | Yes (from shared/) | Never |
| `doc-dependencies.json` | No | Yes (from shared/) | Never |

## What needs to happen

### 1. ldm install: deploy documentation to ~/.ldm/library/documentation/

Currently `deployDocs()` in `bin/ldm.js` deploys to `~/wipcomputerinc/library/documentation/` (home docs). It does NOT deploy to `~/.ldm/library/documentation/` (agent docs). Both locations need to receive docs on every install.

**File:** `bin/ldm.js` function `deployDocs()` (~line 486)
**Change:** After deploying to home library, also deploy to `~/.ldm/library/documentation/`

### 2. ldm install: deploy config dependency files

The three dependency files (`change-dependencies.json`, `config-dependencies.json`, `doc-dependencies.json`) are deployed from `shared/` in the npm package. They should be updated in the repo when the dependency maps change.

**Source:** `wip-ldm-os-private/shared/change-dependencies.json` (and others)
**Deployed to:** `~/.ldm/change-dependencies.json`
**Current status:** Working. The installer copies them. But nobody reads them.

### 3. Wire dependency files into wip-release (Step 6 of docs pipeline)

`wip-release` should read `change-dependencies.json` before publishing. If source files changed since the last tag but the mapped docs didn't change, warn.

**File:** `wip-ai-devops-toolbox-private/tools/wip-release/core.mjs`
**See:** `ai/product/plans-prds/current/docs/2026-03-26--cc-mini--docs-pipeline.md` Step 6

### 4. Wire dependency files into ldm doctor

`ldm doctor` should read `config-dependencies.json` and verify all referenced paths exist. If a path was renamed but configs still point to the old path, warn.

**File:** `wip-ldm-os-private/bin/ldm.js` function `cmdDoctor()`

### 5. Wire dependency files into daily audit

The workspace audit should read `doc-dependencies.json` and compare doc timestamps against source timestamps. If a source is newer than its dependent doc, flag it.

**File:** `wip-ai-devops-toolbox-private/tools/ldm-jobs/workspace-audit.sh`

## Related plans and bugs

- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/docs/2026-04-03--cc-mini--doc-architecture-and-update-pipeline.md` ... the full doc pipeline plan (Step 6 is the guard)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/docs/2026-03-26--cc-mini--docs-pipeline.md` ... original docs pipeline (Steps 5b and 6 not started)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/master-plans/2026-04-09--cc-mini--master-plan-004-execution-order.md` ... Step 7 (doc dependency guard)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/plans-prds/current/ldmos-core/2026-04-08--cc-mini--daily-workspace-audit.md` ... daily audit plan (section 6: doc sync check)
- `/Users/lesa/wipcomputerinc/repos/ldm-os/wip-ldm-os-private/ai/product/bugs/installer/2026-04-03--cc-mini--installer-recreates-renamed-folders.md` ... installer deploy path bugs

## How documentation should flow on install

```
wip-ldm-os-private/shared/docs/*.md.tmpl    Source templates (in repo)
    |
    v  ldm install reads templates + config.json
    |
    +---> ~/wipcomputerinc/library/documentation/    Human docs (personalized)
    +---> ~/.ldm/library/documentation/              Agent docs (personalized)

wip-ldm-os-private/shared/change-dependencies.json
wip-ldm-os-private/shared/config-dependencies.json
wip-ldm-os-private/shared/doc-dependencies.json
    |
    v  ldm install copies
    |
    +---> ~/.ldm/change-dependencies.json
    +---> ~/.ldm/config-dependencies.json
    +---> ~/.ldm/doc-dependencies.json
```

## About the ~/.ldm/ repo

`~/.ldm/` is tracked by a personal git repo (`wipcomputer/wipcomputer-ldmos-wipcomputerinc-system-private`). This is NOT a development repo. It exists to track changes to system files for integrity auditing. Development happens here in wip-ldm-os-private.

When `ldm install` deploys files to `~/.ldm/`, those changes show up as uncommitted modifications in the personal repo. An auto-commit hook (planned) will commit them periodically so the audit trail is continuous.
