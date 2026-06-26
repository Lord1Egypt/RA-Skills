# RSS-Brew Ops Runbook (V1)

## Status
This runbook covers the **V1 app wrapper** state.

Operationally, RSS-Brew can now be run through the new CLI while still delegating to the legacy runtime scripts.

---

## Environment
Project root:
- `/root/.openclaw/workspace/skills/rss-brew`

Default data root:
- `/root/workplace/2 Areas/rss-brew-data`

Recommended runtime environment:
```bash
cd /root/.openclaw/workspace/skills/rss-brew
export PYTHONPATH=app/src
```

Test environment (Phase 3):
```bash
# one-time (inside skill venv)
./venv/bin/python -m pip install -r requirements.txt

# run app tests
cd app
../venv/bin/python -m pytest -q
```

Optional conservative runtime controls:
```bash
export RSS_BREW_PHASE_A_LIMIT=5
export RSS_BREW_ENV=dev
```

Phase-A direct DeepSeek API env knobs:
```bash
export DEEPSEEK_API_KEY='...'
export DEEPSEEK_BASE_URL='https://api.deepseek.com/v1'   # optional override
export DEEPSEEK_MODEL='deepseek-reasoner'                # optional override
export DEEPSEEK_TIMEOUT_SECONDS=60                        # optional override
export DEEPSEEK_RETRY_COUNT=2                             # optional override
```

---

## Primary commands

### Show CLI help
```bash
python3 -m rss_brew.cli --help
```

### Inspect latest run
```bash
python3 -m rss_brew.cli inspect latest --data-root '/root/workplace/2 Areas/rss-brew-data'
```

### Dry run
```bash
python3 -m rss_brew.cli dry-run --data-root '/root/workplace/2 Areas/rss-brew-data' --debug
```

### Real small-run
```bash
python3 -m rss_brew.cli run --data-root '/root/workplace/2 Areas/rss-brew-data' --debug
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

---

## What to check after a run

### 1) Latest manifest pointer
```bash
python3 -m rss_brew.cli inspect latest --data-root '/root/workplace/2 Areas/rss-brew-data'
```

### 2) CURRENT pointer
Check:
```bash
/root/workplace/2 Areas/rss-brew-data/daily/YYYY-MM-DD/CURRENT
```

### 3) Published output exists
Check:
```bash
/root/workplace/2 Areas/rss-brew-data/daily/YYYY-MM-DD/<run_id>/
```

### 4) Delivery status
Check manifest field:
- `delivery_status`

---

## Known V1 behavior

### CLI delegates to legacy scripts
This is expected in V1. The app wrapper is operational, but runtime semantics still live in `scripts/`.

### Preferred interpreter is the skill venv
The CLI is configured to prefer:
```bash
/root/.openclaw/workspace/skills/rss-brew/venv/bin/python
```
This is required for real execution because system Python may not have RSS-Brew dependencies.

---

## Known failure modes

### Failure: missing dependency (e.g. `pydantic`)
Cause:
- legacy scripts ran under system Python instead of the skill venv

Expected fix in V1:
- CLI should use the skill venv interpreter by default

### Failure: path to legacy scripts incorrect
Cause:
- wrong `SKILL_ROOT` / `LEGACY_SCRIPTS_ROOT` resolution in `paths.py`

### Failure: path to sub-scripts incorrect inside legacy orchestrator
Cause:
- wrong `SCRIPT_DIR` logic in `scripts/run_pipeline_v2.py`

---

## Validated milestone
A successful V1 small real run was confirmed with:
- new CLI entrypoint
- skill venv interpreter
- real data root
- committed final state
- updated CURRENT pointer

Reference run:
- `run_id = 20260309T172911Z-1092041`
- `status = committed`
- `new_articles = 32`
- `deep_set_count = 1`
- `elapsed ≈ 2m46.72s`

---

## What not to do yet
- do not remove legacy `scripts/`
- do not switch everything to compat modules yet
- do not redesign delivery in V1
- do not rewrite orchestrator semantics before tests are stronger
