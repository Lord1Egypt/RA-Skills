# vibo-selfdeed

**One product, two stages: GRILL (front door) + MISSION (engine) — powered by [ViBo Memory](https://wwwvibo.com).** Built-in DEMO memory (100 facts) works right after install, no ViBo CLI required — feel the convenience, then upgrade.

The agent receives ONE concrete multi-step task and executes it as an autonomous mission: restore context from ViBo memory → scan for problems → propose fixes (safe, with confirmation) → apply with backups → iterate via paths A/B/C → **save the lesson back into ViBo** → report with numbers.

> The more it works — the more it remembers — the better it does next time.

## Install

```bash
npm install vibo-selfdeed
# or from ClawHub:
# openclaw skills install @vnbochkarev-netizen/vibo-selfdeed
```

Requires Python 3.11 (ViBo core `.so`) and a ViBo CLI (`vibo_use.py`, from the ViBo skill package or https://wwwvibo.com). Set `VIBO_CLI=/path/to/vibo_use.py` if it is not next to the skill.

## Quick start

```bash
./run_mission.sh init --task "find and fix bugs in src/" --target 90
./run_mission.sh checkpoint START ok "context restored from ViBo"
# agent: SCAN → PROPOSE → FIX (backups + confirmation) → LEARN → REPORT
./run_mission.sh finish
```

Optional Telegram controls: `notify` (stage updates), `ask` (✅/❌ buttons), `report` — set `TELEGRAM_MISSION_TOKEN` + `TELEGRAM_MISSION_CHAT`.

## Files

- `SKILL.md` — one product: GRILL pre-flight (G1-G5) + mission instructions (stages, safety, stop matrix)
- `run_mission.sh` — wrapper: init / checkpoint / progress / switch / rollback / finish
- `lib_vibo.py` — thin client to the ViBo CLI (add / find / usage / link / stats)
- `safety.py` — backups, rollback, attempt/timeout limits, L3 masking
- `telegram_mission.py` — Telegram stage + ✅/❌ controls

## Try it immediately (DEMO mode)

No ViBo CLI installed? The skill still works with a built-in DEMO memory (100 facts, word search):
`vibo find "context"` · `vibo add "fact" "value"` — and every command shows where to get the full engine:
**free tier: 500 facts forever** · 2-day trial: https://wwwvibo.com/download/trial.

## Security notes

- Runs ONLY inside the mission workdir; backups in `.selfdeed_backup/`.
- No network by default. Telegram stage updates (`notify`/`ask`/`report`) are opt-in and print a warning before sending.
- `--auto` applies changes without per-fix confirmation — use only in a scoped workspace.
- This package does NOT include any social posting; if you need the optional comment generator it lives in a separate package.

## License

See [EULA.md](EULA.md) — the ViBo license applies (free tier: 500 facts forever; upgrade: $5/mo, $30/yr, $60 lifetime).

© ViBo by Viacheslav Bochkarev — https://wwwvibo.com
