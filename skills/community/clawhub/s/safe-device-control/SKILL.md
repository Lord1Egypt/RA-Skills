---
name: safe-device-control
version: 1.0.0
description: "Physical-device control safety gate — never blindly toggle cloud devices; check state, surface risk, require explicit go-ahead before risky actions."
allowed-tools: [exec, read, edit]
---

# Safe Device Control

## Core Rule
**Never execute risky control actions on physical devices without explicit go-ahead from Hobo.** Risky = anything that could lock a device offline, change persistent settings, require physical intervention to reverse, or trigger firmware/account-level locks.

## Pre-Action Checklist (Before Any Risky Control Command)
1. **Read current state first** — get full device state via the sensor endpoint
2. **Classify the action** into one of the risk tiers below
3. **Surface the risk** — tell Hobo what could go wrong
4. **Get explicit go-ahead** for write-risky and write-irreversible actions
5. **Verify after** — read state again, confirm intended change actually happened

## Risk Tiers

### Read-Only — no gate needed
- Get current state, list devices, read sensors, query API

### Write-Low-Risk — execute, but verify state after
- Toggle Tapo plug on/off (state-verifiable via /plug/<name>)
- Set fan_speed (queued, reversible, doesn't lock device)
- Set mode to a known preset (Auto/Strong/Sleep — reversible)
- Send learned IR code (reversible)

### Write-Risky — require explicit go-ahead from Hobo
- **Power toggle action** on any cloud-controlled device (can trigger deep standby — see FP10 incident below)
- Factory reset, firmware update, account linking/unlinking
- Wipe learned IR codes, change device passwords
- First-time control of a device that hasn't been end-to-end-tested before
- Any action where the API returns `code: 0` but device state didn't actually change (treat as suspicious)

### Write-Irreversible — requires typed approval from Hobo
- Anything in AGENTS.md red lines (deleting files, configs, cron jobs)
- Anything destructive flagged in HEARTBEAT.md or LISTS.md
- Network/firewall changes, auth key rotations

## Mistakes to Avoid (Lessons from FP10 Incident, 2026-07-17)
1. **Don't blindly toggle power on a cloud-controlled device.** The Dreame FP10 toggle action (`siid=2, aiid=3`) put the device into deep standby — went from `online: True` (with stale reads) to `online: False` (no reads at all). Required physical button press on the unit to recover.
2. **`code: 0` from cloud APIs is not confirmation.** The Dreame cloud returned success for `set_properties` on power (`siid=2, piid=1`) when the device silently rejected it. The action toggle returned success and then bricked the connection. Cloud acceptance ≠ device execution.
3. **Don't run untested control code on a real device.** Test with `dry_run=true`, against a known-good baseline, or against a non-critical device first.
4. **Don't assume state.** Always read current state before controlling. If state is ambiguous (e.g., device shows online but power state is stuck, or returns stale values like `fan_speed=8/10` while reporting `power=2`), **stop and ask**.
5. **Don't chain control commands without per-step verification.** Set one thing, verify it actually took effect, then proceed.
6. **The "soft off" model matters.** Some devices (Dreame FP10 included) have a *soft-off* state (e.g., Sleep mode + fan_speed=1) that keeps cloud alive, vs a *deep standby* (physical button press) that disconnects. Confirming which state we're in should be the first read before any control action.

## Concrete API Guards (Already Implemented)
- `POST /dreame/<name>/on` requires `{"force": true}` in body — refuses without it (HTTP 403 with reason). Hobo must explicitly type the confirmation.
- `POST /dreame/<name>/off` — soft-off only (Sleep + fan_speed=1). No deep standby path.
- `POST /dreame/<name>/fan_speed` — value is clamped 1-10 (FP10 supports 10 manual speeds). No gate, since it's reversible.
- Future risky endpoints should follow the same `force=true` pattern.

## Recovery Procedures
- **Dreame FP10 deep standby:** physical power button press on the unit (~3s hold). After wake, fan_speed queued value should be honored.
- **Tapo plug offline:** unplug 10s, replug, wait for DHCP lease + WiFi reconnect.
- **Broadlink RM4 Mini timeout:** power cycle the unit (unplug/replug).
- **Anything else:** check the device's official app first to confirm cloud-side state before re-trying from our API.

## When to Use This Skill
Use this skill BEFORE any device control action that is:
- A new control path (first time we're sending this command to this device)
- Anything in the Write-Risky tier
- An action that has previously failed or behaved unexpectedly
- Part of a chained sequence where one link failed

Routine actions already validated end-to-end (e.g., turning the plant-light on/off, sending a learned IR button) don't need to re-trigger this skill every time — they're pre-approved by their existing log of successful runs.

## Sources
- Original incident: `memory/2026-07-17.md` (21:11–21:49 SGT)
- MiOT spec verified from: https://github.com/CodyJon/dreame-ap10-integration
- Force-guard implementation: `scripts/smart-home/app.py` (`dreame_on` endpoint)
- HEARTBEAT.md: "Device Control — Safety Gate" section (loaded at every wake)
