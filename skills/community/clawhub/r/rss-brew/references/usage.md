# RSS-Brew Usage Reference

This file explains how to use RSS-Brew in its current **Phase 2 wrap-up / Phase 3 start** state.

## Current operational model

RSS-Brew now has two layers:

1. **App wrapper** under `app/`
2. **Legacy runtime scripts** under `scripts/`

Current reality:
- the recommended entrypoint for new operations is the app CLI
- runtime semantics still live in the legacy scripts
- the CLI currently delegates to the legacy scripts intentionally

## Recommended working directory
```bash
cd /root/.openclaw/workspace/skills/rss-brew
export PYTHONPATH=app/src
```

## Recommended real data root
```bash
/root/workplace/2 Areas/rss-brew-data
```

## Main commands

### Show CLI help
```bash
python3 -m rss_brew.cli --help
```

### Inspect latest run
```bash
python3 -m rss_brew.cli inspect latest \
  --data-root '/root/workplace/2 Areas/rss-brew-data'
```

### Dry run
```bash
python3 -m rss_brew.cli dry-run \
  --data-root '/root/workplace/2 Areas/rss-brew-data' \
  --debug
```

### Real small run
Recommended conservative settings:
```bash
export RSS_BREW_PHASE_A_LIMIT=5
export RSS_BREW_ENV=dev
python3 -m rss_brew.cli run \
  --data-root '/root/workplace/2 Areas/rss-brew-data' \
  --debug
```

### Update delivery status
```bash
python3 -m rss_brew.cli delivery update \
  --data-root '/root/workplace/2 Areas/rss-brew-data' \
  --status sent
```

or

```bash
python3 -m rss_brew.cli delivery update \
  --data-root '/root/workplace/2 Areas/rss-brew-data' \
  --status failed \
  --message 'delivery failed details here'
```

## Current recommendation

### For daily operations
Use the app CLI:
```bash
python3 -m rss_brew.cli ...
```

### For debugging migration issues
Inspect both:
- `app/src/rss_brew/cli.py`
- `scripts/run_pipeline_v2.py`

## Current known good validation
A confirmed successful small real run through the new CLI exists:
- `run_id = 20260309T172911Z-1092041`
- `status = committed`
- `new_articles = 32`
- `deep_set_count = 1`
- `elapsed ≈ 2m46.72s`

## What is still transitional
- tests are not fully complete yet
- legacy scripts are still the runtime source of truth
- compat copies exist but are not yet the primary execution layer
