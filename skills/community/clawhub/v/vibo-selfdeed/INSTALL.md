# vibo-selfdeed — install

**Self-improving agent mission skill powered by ViBo Memory.**

## Requirements
- Python 3.11 (ViBo core `.so` is built for CPython 3.11; `lib_vibo.py` finds `python3.11` automatically, falls back to `python3`)
- `vibo_use.py` (ViBo CLI) — lib_vibo finds it via: `VIBO_CLI` env → `PATH` → next to the skill → walking up 3 parent levels
- Optional: a ViBo license (`activate.py VIBO-...` or free tier: 500 facts forever)

## Install
1. Copy the `vibo-selfdeed/` folder next to your ViBo skill package (or anywhere).
2. Verify:
   ```bash
   python3 lib_vibo.py stats
   python3 lib_vibo.py find "your project"
   ```
   If the CLI is not auto-found: `export VIBO_CLI=/path/to/vibo_use.py`.

## Quick start (mission)
```bash
./run_mission.sh init --task "find and fix bugs in src/" --target 90
./run_mission.sh checkpoint START ok "context restored"
# ... agent works through SCAN → PROPOSE → FIX → ITERATE ...
./run_mission.sh finish
```

## Files
| File | Purpose |
|---|---|
| `SKILL.md` | agent instructions (stages, safety, stop matrix) |
| `TASK.md` | mission template |
| `run_mission.sh` | mission wrapper (init/checkpoint/progress/switch/rollback/finish) |
| `lib_vibo.py` | thin ViBo client (add/find/usage/link/stats) |
| `safety.py` | backups, rollback, attempt/timeout limits, smart stop matrix |
| `examples/` | 3 usage examples |

## License
ViBo EULA applies (see the ViBo skill package: `EULA.md`, https://wwwvibo.com).
