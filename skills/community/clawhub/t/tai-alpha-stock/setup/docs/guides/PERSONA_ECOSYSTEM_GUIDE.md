# Persona ecosystem guide

## Overview

Personas apply **overlays** on top of the shared dimension score (`score_engine` + `setup/config/score_dimensions.yaml`). They do not replace the core pipeline; they tune conviction and signals per investment style.

## Registry

- Index: [`setup/config/personas/PERSONA_REGISTRY.yaml`](../../config/personas/PERSONA_REGISTRY.yaml)
- One file per persona (e.g. `value_seeker.yaml`) with `overlay` weights and optional `signal_cap_max`.

## CLI

```bash
python scripts/analyze.py AAPL --persona value_seeker
python scripts/analyze.py 0700.HK --market hk --persona momentum_rider --lang zh-CN
python scripts/analyze.py MSFT --persona-all --lang zh-HK
```

## Ensemble

`--persona-all` runs all enabled personas and aggregates with configured `ensemble_weight` (weighted average conviction, unified signal from the blended score).

## Data routing

US/HK/CN symbols are normalized for Yahoo Finance before fetch; see `tai_alpha/market_router.py` in [MODULE_STRUCTURE.md](../../../MODULE_STRUCTURE.md). Adapter metadata is stored under `adapter_meta` in `collect_json`.

## Related

- [CHINESE_AUDIENCE_GUIDE.md](CHINESE_AUDIENCE_GUIDE.md)
- [../core/AGENT_GUIDE.md](../core/AGENT_GUIDE.md)
