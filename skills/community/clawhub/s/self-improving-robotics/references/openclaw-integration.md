# OpenClaw Integration

Complete setup and usage guide for integrating the `self-improving-robotics` skill with OpenClaw.

## Overview

OpenClaw uses workspace-based prompt injection combined with event-driven hooks. Context is injected from workspace files at session start, and hooks can trigger on lifecycle events.

## Workspace Structure

```
~/.openclaw/
├── workspace/                   # Working directory
│   ├── AGENTS.md               # Multi-agent coordination patterns
│   ├── SOUL.md                 # Behavioral guidelines and personality
│   ├── TOOLS.md                # Tool capabilities and gotchas
│   ├── MEMORY.md               # Long-term memory (main session only)
│   └── memory/                 # Daily memory files
│       └── YYYY-MM-DD.md
├── skills/                      # Installed skills
│   └── self-improving-robotics/
│       └── SKILL.md
└── hooks/                       # Custom hooks
    └── self-improving-robotics/
        ├── HOOK.md
        └── handler.ts
```

## Quick Setup

### 1. Install the Skill

```bash
clawdhub install self-improving-robotics
```

Or clone manually:

```bash
git clone https://github.com/jose-compu/self-improving-robotics.git ~/.openclaw/skills/self-improving-robotics
```

### 2. Install the Hook (Optional)

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-robotics
openclaw hooks enable self-improving-robotics
```

### 3. Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then initialize:
- `LEARNINGS.md` - domain learnings and patterns
- `ROBOTICS_ISSUES.md` - concrete failures/incidents
- `FEATURE_REQUESTS.md` - tooling and capability requests

## Promotion Targets (Robotics-Specific)

When robotics learnings prove broadly applicable, promote them to durable docs:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Safety-critical failure patterns | Safety checklist | "Always verify estop state transitions before motion enable" |
| Calibration and sync workflows | Calibration playbook | "Camera-lidar extrinsic and timestamp validation sequence" |
| Stable tuning procedures | Tuning runbook | "PID retuning order under payload change" |
| Multi-agent operations workflow | `AGENTS.md` | "Split sim validation and field validation across agents" |
| Behavioral guardrails | `SOUL.md` | "Never bypass safety interlocks for rapid testing" |
| Tool and telemetry integration | `TOOLS.md` | "Always export synchronized clocks for replay analysis" |

### Promotion Decision Tree

```
Is it safety-critical or risk-reducing?
├── Yes -> Promote to safety checklist first
└── No -> Is it calibration or synchronization process?
    ├── Yes -> Promote to calibration playbook
    └── No -> Is it controller/planner tuning guidance?
        ├── Yes -> Promote to tuning runbook
        └── No -> Is it an agent workflow/tool rule?
            ├── Yes -> Promote to AGENTS.md / TOOLS.md / SOUL.md
            └── No -> Keep in .learnings until recurrence confirms
```

## Robotics Detection Triggers

| Trigger | Action | Target |
|---------|--------|--------|
| Robot fails to localize in dynamic environment | Log issue | ROBOTICS_ISSUES.md |
| Planner fails in narrow passage / obstacle-rich scene | Log issue | ROBOTICS_ISSUES.md |
| Oscillatory control behavior / unstable PID tuning | Log issue | ROBOTICS_ISSUES.md |
| Sensor desync (camera-lidar-imu mismatch) | Log issue | ROBOTICS_ISSUES.md |
| Driver drops packets / CAN timeout / serial disconnect | Log issue | ROBOTICS_ISSUES.md |
| Safety stop or emergency brake unexpectedly triggered | Log issue | ROBOTICS_ISSUES.md |
| Simulation success but real robot failure | Log learning | LEARNINGS.md (`sim_to_real_gap`) |
| Thermal throttling, battery sag, or power brownout | Log learning | LEARNINGS.md (`power_thermal_constraint`) |

## Inter-Agent Communication

OpenClaw provides tools for cross-session communication. Use only when cross-session sharing is explicitly needed.

### sessions_send

Share a robotics incident finding with another session:
```
sessions_send(sessionKey="session-id", message="Planner failed in narrow corridor at 0.35 m clearance; fallback behavior avoided collision; add to runbook.")
```

### sessions_spawn

Spawn a background agent to analyze recurring robotics patterns:
```
sessions_spawn(task="Review .learnings/ROBOTICS_ISSUES.md for recurring localization_drift patterns and propose promotion candidates", label="robotics-pattern-review")
```

## Available Hook Events

| Event | When It Fires |
|-------|---------------|
| `agent:bootstrap` | Before workspace files inject |
| `command:new` | When `/new` command issued |
| `command:reset` | When `/reset` command issued |
| `command:stop` | When `/stop` command issued |
| `gateway:startup` | When gateway starts |

## Verification

```bash
openclaw hooks list        # Check hook is registered
openclaw status            # Check skill is loaded
```

## Troubleshooting

### Hook not firing
1. Ensure hooks are enabled in config
2. Restart gateway after config changes
3. Check gateway logs for errors

### Learnings not persisting
1. Verify `.learnings/` directory exists
2. Check file permissions
3. Ensure workspace path is configured correctly

### Skill not loading
1. Check skill is in skills directory
2. Verify `SKILL.md` has valid frontmatter
3. Run `openclaw status` to see loaded skills
