---
name: rss-brew
description: Run and operate the RSS-Brew digest pipeline, including app CLI usage, dry-runs, latest-run inspection, delivery status updates, and retry/finalize-aware operations.
---

# RSS-Brew Skill

Use this skill when you need to:
- run the RSS-Brew pipeline
- inspect the latest run
- do a dry-run
- update delivery status
- understand the current migration/app-wrapper state
- troubleshoot retry/finalize behavior

## Current recommended entrypoint

Use the app CLI from the skill root:

```bash
cd /root/.openclaw/workspace/skills/rss-brew
export PYTHONPATH=app/src
python3 -m rss_brew.cli --help
```

Common commands:

```bash
python3 -m rss_brew.cli inspect latest --data-root '/root/workplace/2 Areas/rss-brew-data'
python3 -m rss_brew.cli dry-run --data-root '/root/workplace/2 Areas/rss-brew-data' --debug
python3 -m rss_brew.cli run --data-root '/root/workplace/2 Areas/rss-brew-data' --debug
python3 -m rss_brew.cli delivery update --data-root '/root/workplace/2 Areas/rss-brew-data' --status sent
```

## Current architecture reality

RSS-Brew is in an in-place app-ification state:
- `app/` is the new app wrapper/container
- `app/src/rss_brew/cli.py` is the new entrypoint
- `scripts/` still contain the runtime source-of-truth semantics
- the app CLI intentionally delegates to legacy scripts in the current phase

## Read these references as needed

- **Usage / commands:** `references/usage.md`
- **Operational checks / failure modes:** `references/ops.md`
- **Pipeline behavior / outputs:** `references/pipeline-spec.md`
- **Retry / finalize architecture:** `references/retry-architecture.md`
- **Migration / implementation status:** `docs/rss-brew-implementation-plan.md`

## Current default data root

```bash
/root/workplace/2 Areas/rss-brew-data
```

## Important note

This skill is no longer just a loose script bundle. It is now a working app-wrapper around the legacy RSS-Brew runtime. Prefer the app CLI for new operations while keeping legacy scripts intact during migration.
