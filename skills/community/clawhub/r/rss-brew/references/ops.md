# RSS-Brew Operations Reference

This file captures practical operational checks for the current in-place app-ified RSS-Brew state.

## Environment
Project root:
```bash
/root/.openclaw/workspace/skills/rss-brew
```

Recommended shell setup:
```bash
cd /root/.openclaw/workspace/skills/rss-brew
export PYTHONPATH=app/src
```

Optional conservative runtime settings:
```bash
export RSS_BREW_PHASE_A_LIMIT=5
export RSS_BREW_ENV=dev
```

## Primary runtime paths

### App entrypoint
```bash
app/src/rss_brew/cli.py
```

### Legacy runtime source of truth
```bash
scripts/
```

### Data root
```bash
/root/workplace/2 Areas/rss-brew-data
```

### Scoring V2 shadow path (internal)
Use the additive shadow script (keeps production V1 cron path unchanged):
```bash
/root/.openclaw/scripts/rss-brew-scoring-v2-shadow.sh
```

Defaults:
- Shadow data root: `/root/workplace/2 Areas/rss-brew-data-shadow-v2`
- Runs with: `--scoring-v2`
- No user-visible delivery by default

Optional (for separate cron/manual dry-run):
```bash
RSS_BREW_V2_SHADOW_DRY_RUN=1 /root/.openclaw/scripts/rss-brew-scoring-v2-shadow.sh
```

## After-run checks

### 1. Inspect latest
```bash
python3 -m rss_brew.cli inspect latest \
  --data-root '/root/workplace/2 Areas/rss-brew-data'
```

### 2. Check CURRENT pointer
```bash
/root/workplace/2 Areas/rss-brew-data/daily/YYYY-MM-DD/CURRENT
```

### 3. Check published output exists
```bash
/root/workplace/2 Areas/rss-brew-data/daily/YYYY-MM-DD/<run_id>/
```

### 4. Check delivery status
Read manifest field:
- `delivery_status`

## Operational facts in current phase
- CLI now prefers the skill venv interpreter
- dry-run through new CLI has been validated
- small real run through new CLI has been validated
- legacy scripts still remain the authoritative runtime layer

## Common failure classes

### 1. Wrong interpreter / missing dependency
Example symptom:
- `ModuleNotFoundError: No module named 'pydantic'`

Meaning:
- delegated scripts ran under system Python instead of the skill venv

### 2. Wrong path resolution
Meaning:
- `SKILL_ROOT`, `LEGACY_SCRIPTS_ROOT`, or local script path assumptions are wrong

### 3. Legacy script health issue
Meaning:
- syntax/path issue in `scripts/run_pipeline_v2.py` or sibling scripts

## Immediate response checklist
If a run fails unexpectedly:
- inspect latest manifest
- confirm CLI is using the venv-backed delegate path
- confirm `scripts/*.py` still compile
- confirm staging/published paths were created as expected
- compare against known good V1 run behavior documented in `app/docs/migration-v1.md`

## Current migration posture
This is still a transitional state.

Do:
- use the app CLI for new execution/testing
- keep legacy scripts intact
- document fixes during migration

Do not yet:
- remove legacy scripts
- rewrite orchestrator semantics during simple ops work
- redesign delivery as part of operational cleanup
