# OpenClaw Integration (Domotics)

Complete setup for `self-improving-domotics` in OpenClaw.

## Install

```bash
clawdhub install self-improving-domotics
```

Manual alternative:

```bash
git clone https://github.com/jose-compu/self-improving-domotics.git ~/.openclaw/skills/self-improving-domotics
```

## Optional Hook

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-domotics
openclaw hooks enable self-improving-domotics
```

## Workspace Files

Ensure:

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Required files:
- `LEARNINGS.md`
- `DOMOTICS_ISSUES.md`
- `FEATURE_REQUESTS.md`

## Promotion Targets

- Home automation playbooks
- Device compatibility matrix
- Automation rule library
- Safety automations

## Detection Focus

- Rule conflict and automation loops
- Sensor drift and stale occupancy
- Device offline / unreachable behavior
- Integration/webhook/API regressions
- Latency and schedule miss patterns
- Energy optimization opportunities
- Safety rule gaps for high-impact routines

## Safety Boundary

This integration captures reminders and documentation only.
It does not execute direct physical actuator actions.
Human confirmation is required for lock/alarm/gas/water/heater high-impact routines.
