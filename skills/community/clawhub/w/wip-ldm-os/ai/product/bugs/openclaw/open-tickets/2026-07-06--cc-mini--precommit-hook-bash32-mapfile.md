# OpenClaw pre-commit hook assumes bash 4 (mapfile); macOS ships bash 3.2

- **Date:** 2026-07-06
- **Author:** cc-mini (Claude Code, Fable 5)
- **Status:** open (thin ticket; filed per Codex third review so this stops living as a bullet)
- **Severity:** P2 (workflow friction; caused a coder session to stall 2026-07-03)
- **Umbrella:** `2026-07-04--cc-mini--lesa-noreply-loop-recovery-and-upgrade-plan.md` (section 7 owed items)

## Problem

OpenClaw's pre-commit hook uses bash 4 features (`mapfile`), but macOS ships bash 3.2 at `/bin/bash`. On this machine the hook fails, which on 2026-07-03 stalled the oc-update-fixes-coder session into considering `--no-verify` (corre