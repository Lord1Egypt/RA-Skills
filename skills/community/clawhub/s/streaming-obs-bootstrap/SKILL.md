---
name: streaming-obs-bootstrap
description: Rebuild and validate a reusable OBS streaming scene pack via agentic-obs and mcporter. Use when setting up or migrating streaming scenes (local or remote OBS), wiring browser overlays from workspace over LAN HTTP, running recording smoke tests, and troubleshooting browser-source rendering/emoji issues.
---

# Streaming OBS Bootstrap

Use this skill to quickly stand up a consistent streaming scene set on OBS and verify it with recording walkthroughs.

## Prerequisites

- `mcporter` installed and configured with `obs` MCP server
- OBS WebSocket enabled on target host (default port `4455`)
- Overlay files present in workspace (`streaming/overlays`)

## Workflow

1. Set target OBS host (local or LAN host)
2. Start workspace HTTP server for overlays (LAN reachable)
3. Rebuild baseline scene pack
4. Attach overlay browser sources
5. Apply transition preset and optional audio baseline
6. Run recording smoke walkthrough and optional stream dry-run
7. Share output path and any troubleshooting notes

## Commands

Run from workspace root.

```bash
# 1) Target OBS host
./skills/streaming-obs-bootstrap/scripts/obs_target_switch.sh <obs-host-ip> 4455

# 2) Start/verify overlay host server
./skills/streaming-obs-bootstrap/scripts/start_overlay_server.sh

# 3) Rebuild scenes + attach overlays
./skills/streaming-obs-bootstrap/scripts/rebuild_scenes.sh

# 4) Apply transition preset
./skills/streaming-obs-bootstrap/scripts/apply_transition_preset.sh Fade 300

# 5) Optional audio baseline (set OBS_AUDIO_INPUTS first)
# export OBS_AUDIO_INPUTS="Mic/Aux,Desktop Audio"
./skills/streaming-obs-bootstrap/scripts/apply_audio_baseline.sh

# 6) Run walkthrough recording (default 7s/scene)
./skills/streaming-obs-bootstrap/scripts/smoke_test_walkthrough.sh

# 7) Optional stream dry-run (default 15s)
./skills/streaming-obs-bootstrap/scripts/stream_dry_run.sh 15 "Intro" "Main Live"
```

## Notes

- Never use `/tmp` for persistent overlay assets.
- Prefer `http://<agent-lan-ip>:8787/...` browser source URLs over `file://` for remote OBS.
- Ensure HTML files declare UTF-8 and emoji-capable font stacks.

## Troubleshooting

See:
- `references/troubleshooting.md`
- `references/networking.md`
- `references/scene-map.md`
- `references/v0.2-features.md`
