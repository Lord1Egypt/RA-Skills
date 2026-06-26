# Learnings Bridge — Wiring to Self-Improving Agent

The learnings bridge connects the **self-improving-agent** skill to the **subconscious** skill. They are two separate skills that work together.

## Architecture

```
self-improving-agent skill
    └── writes lessons → {workspace}/.learnings/LEARNINGS.md
                                    ↓ (read by)
subconscious skill
    └── learnings_bridge.py → pending.jsonl → live.json → bias injection
```

## Requirements

The self-improving-agent skill must be installed at:
```
{workspace}/skills/self-improving-agent/
```

And it must produce learnings at:
```
{workspace}/.learnings/LEARNINGS.md
```

## What the Bridge Reads

The bridge (`learnings_bridge.py`) scans these files every tick:
- `{workspace}/.learnings/LEARNINGS.md` — main learnings log
- `{workspace}/.learnings/ERRORS.md` — error patterns
- `{workspace}/.learnings/FEATURES.md` — feature flags / system notes

## What Gets Queued

Each new entry in LEARNINGS.md becomes a `candidate_queued` item in `pending.jsonl` with:
- `kind=ITEM` (general item)
- `confidence=0.7` (default)
- `freshness=1.0` (new)
- `source=self-improving-agent`

## Installing the Self-Improving Agent

If you don't already have it:

```bash
# It's at the standard OpenClaw skill location
ls ~/.openclaw/workspace-alfred/skills/self-improving-agent/

# If missing, install from clawhub:
openclaw skills add self-improving-agent
```

## How They Connect

1. **Self-improving agent** (self-improving-agent skill) writes notable lessons, errors, and behavioral observations to `.learnings/LEARNINGS.md`
2. **Learnings bridge** (subconscious skill, runs every tick) scans for new entries since last run, queues them to `pending.jsonl`
3. **Tick** (subconscious skill) reinforces pending items over time
4. **Rotate** (subconscious skill, hourly with `--enable-promotion`) promotes eligible items to `live.json`
5. **Bias injection** (subconscious skill) makes promoted items available to session prompts

## Verifying the Connection

```bash
# Check learnings exist
cat ~/.openclaw/workspace-alfred/.learnings/LEARNINGS.md | tail -5

# Check bridge tracker
cat ~/.openclaw/workspace-alfred/memory/subconscious/learnings_bridge_last_seen.json

# Check pending queue (should grow from learnings)
python3 ~/.openclaw/skills/subconscious/scripts/subconscious_cli.py pending
```

## If the Bridge Isn't Running

```bash
# Run a manual tick to trigger bridge scan
python3 ~/.openclaw/skills/subconscious/scripts/subconscious_metabolism.py tick

# Check logs
tail -f ~/.openclaw/workspace-alfred/logs/subconscious_tick.log
```
