---
name: self-improving-robotics
description: "Captures robotics autonomy failures, operational incidents, and engineering learnings to enable continuous improvement across perception, localization, planning, control, simulation, safety, and hardware integration. Use when: (1) Robot fails to localize in dynamic environment, (2) Planner fails in narrow passage or obstacle-rich scene, (3) Oscillatory control behavior or unstable PID tuning appears, (4) Sensor desync occurs (camera-lidar-imu timestamp mismatch), (5) Hardware driver drops packets or CAN timeout occurs, (6) Safety stop or emergency brake triggers unexpectedly, (7) Simulation succeeds but real robot fails, (8) Thermal throttling, battery sag, or power brownout appears."
---

# Self-Improving Robotics Skill

Log robotics-specific learnings, incidents, and feature requests to markdown files for continuous improvement. This skill captures localization drift, planning failures, control instability, sensor fusion issues, hardware interface faults, safety boundary violations, sim-to-real gaps, and power/thermal constraints.

Important learnings get promoted to durable operational artifacts:
- Safety checklists
- Calibration playbooks
- Tuning runbooks
- Robotics sections in `SOUL.md`, `AGENTS.md`, and `TOOLS.md`

## First-Use Initialisation

Before logging anything, ensure the `.learnings/` directory and files exist in the project or workspace root. If any are missing, create them:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Robotics Learnings\n\nLocalization drift events, planning failures, control instabilities, sensor fusion errors, hardware interface issues, safety boundary violations, sim-to-real gaps, and power/thermal constraints captured during robotics engineering work.\n\n**Categories**: localization_drift | planning_failure | control_instability | sensor_fusion_error | hardware_interface_issue | safety_boundary_violation | sim_to_real_gap | power_thermal_constraint\n**Areas**: perception | localization | mapping | planning | control | manipulation | navigation | safety | simulation | hardware_integration\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/ROBOTICS_ISSUES.md ] || printf "# Robotics Issues Log\n\nRecurring robotics failures, autonomy incidents, and subsystem-level defects.\n\n---\n" > .learnings/ROBOTICS_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Feature Requests\n\nRobotics tooling, automation, and autonomy capability requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. This is a no-op if `.learnings/` is already initialised.

Do not log secrets, private keys, or sensitive infrastructure endpoints. Prefer redacted excerpts for logs, telemetry, and stack traces.

If you want automatic reminders, use the opt-in hook workflow described in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Robot fails to localize in dynamic environment | Log issue to `.learnings/ROBOTICS_ISSUES.md` and learning to `.learnings/LEARNINGS.md` with `localization_drift` |
| Planner fails in narrow passage / obstacle-rich scene | Log to `.learnings/ROBOTICS_ISSUES.md` with reproducible scene metadata |
| Oscillatory control behavior / unstable PID tuning | Log to `.learnings/ROBOTICS_ISSUES.md` with control loop telemetry and frequency |
| Sensor desync (camera-lidar-imu timestamp mismatch) | Log to `.learnings/ROBOTICS_ISSUES.md` and tag `sensor_fusion_error` |
| Driver drops packets / CAN timeout / serial disconnect | Log to `.learnings/ROBOTICS_ISSUES.md` with bus and firmware details |
| Safety stop or emergency brake unexpectedly triggered | Log to `.learnings/ROBOTICS_ISSUES.md` with safety state transitions |
| Simulation success but real robot failure | Log to `.learnings/LEARNINGS.md` with category `sim_to_real_gap` |
| Thermal throttling / battery sag / brownout | Log to `.learnings/LEARNINGS.md` with category `power_thermal_constraint` |
| New capability needed for robotics workflow | Log to `.learnings/FEATURE_REQUESTS.md` |
| Recurring issue (3+ occurrences) | Link entries, increase priority, and promote to runbook/checklist |
| Broadly applicable autonomy pattern | Promote to safety checklist, calibration playbook, tuning runbook, or core prompt docs |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It uses workspace-based prompt injection with automatic skill loading.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-robotics
```

**Manual clone:**
```bash
git clone https://github.com/jose-compu/self-improving-robotics.git ~/.openclaw/skills/self-improving-robotics
```

### Workspace Structure

OpenClaw injects these files into every session:

```
~/.openclaw/workspace/
├── AGENTS.md          # Multi-agent workflows and delegation
├── SOUL.md            # Behavioral and safety guardrails
├── TOOLS.md           # Tooling usage and integration notes
├── MEMORY.md          # Long-term memory (main session only)
├── memory/            # Daily memory files
│   └── YYYY-MM-DD.md
└── .learnings/        # This skill's log files
    ├── LEARNINGS.md
    ├── ROBOTICS_ISSUES.md
    └── FEATURE_REQUESTS.md
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create the log files (or copy from `assets/`):
- `LEARNINGS.md` - category-based learnings
- `ROBOTICS_ISSUES.md` - concrete incidents and failures
- `FEATURE_REQUESTS.md` - tooling and capability requests

### Promotion Targets

When robotics learnings prove broadly applicable, promote them:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Safety-critical incident patterns | Safety checklist | "Require sensor freshness checks before enabling autonomous motion" |
| Calibration/sync workflows | Calibration playbook | "Camera-lidar-imu time sync verification sequence" |
| Stable tuning methods | Tuning runbook | "PID retune order under payload changes" |
| Robotics behavior principles | `SOUL.md` | "Never bypass safety interlocks for speed" |
| Multi-agent robotics workflow | `AGENTS.md` | "Separate sim, HIL, and field validation owners" |
| Tooling integration standards | `TOOLS.md` | "Always record synchronized telemetry bundles" |
| Reusable failure mitigations | New reusable skill | "narrow-passage-planning-resilience" |

### Optional: Enable Hook

For automatic reminders at session start:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-robotics
openclaw hooks enable self-improving-robotics
```

See `references/openclaw-integration.md` for complete details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents, create `.learnings/` in project or workspace root:

```bash
mkdir -p .learnings
```

Create files using the headers shown in this skill.

## Logging Format

Use entry types:
- `LRN` = learning
- `ROB` = robotics issue
- `FEAT` = feature request

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: perception | localization | mapping | planning | control | manipulation | navigation | safety | simulation | hardware_integration

### Summary
One-line description of the learning

### Details
Full context: what was observed, why it happened, what constraints mattered,
and how the mitigation should be applied. Include specific telemetry indicators.

### Suggested Action
Concrete process or config update to apply

### Metadata
- Source: telemetry_alert | simulation_failure | hil_test | field_test | safety_event | hardware_diagnostics | code_review | postmortem
- Platform: robot_model_or_stack (optional)
- Related Files: path/to/config_or_code
- Tags: tag1, tag2
- See Also: LRN-20250110-001 (if related)
- Pattern-Key: localization_drift.dynamic_scene (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2025-01-15 (optional)
- Last-Seen: 2025-01-15 (optional)

---
```

**Categories for learnings:**

| Category | Use When |
|----------|----------|
| `localization_drift` | Pose confidence degrades over time or in dynamic scenes |
| `planning_failure` | Planner repeatedly cannot find safe/feasible path |
| `control_instability` | Oscillation, overshoot, divergence, or instability appears |
| `sensor_fusion_error` | Multi-sensor alignment/timing inconsistency corrupts estimate |
| `hardware_interface_issue` | Driver, bus, transport, or actuator interface defects |
| `safety_boundary_violation` | Safety envelope trigger or near-violation occurs |
| `sim_to_real_gap` | Simulation passes but field behavior fails |
| `power_thermal_constraint` | Thermal, voltage, or energy limits degrade behavior |

### Robotics Issue Entry [ROB-YYYYMMDD-XXX]

Append to `.learnings/ROBOTICS_ISSUES.md`:

```markdown
## [ROB-YYYYMMDD-XXX] issue_name

**Logged**: ISO-8601 timestamp
**Priority**: high
**Status**: pending
**Area**: perception | localization | mapping | planning | control | manipulation | navigation | safety | simulation | hardware_integration

### Summary
Brief description of the robotics issue

### Error Output
```
Command output, safety alerts, diagnostics, or stack traces (redacted/summarized)
```

### Root Cause
What subsystem or integration issue caused the failure.

### Fix
Specific mitigations, parameter adjustments, code updates, or operational changes.

### Prevention
How to avoid recurrence (checklist guardrail, test, monitor, fallback behavior).

### Context
- Trigger: telemetry_alert | simulation_failure | hil_test | field_test | safety_event | hardware_diagnostics
- Environment: sim | lab | warehouse | outdoors | unknown
- Run ID or mission segment

### Metadata
- Reproducible: yes | no | unknown
- Related Files: path/to/config_or_code
- See Also: ROB-20250110-001 (if recurring)

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: medium
**Status**: pending
**Area**: perception | localization | mapping | planning | control | manipulation | navigation | safety | simulation | hardware_integration

### Requested Capability
What robotics capability, tool, or automation is needed

### User Context
Why it is needed and what workflow it improves

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
How this could be built (tooling, pipeline, monitor, playbook, simulation harness)

### Metadata
- Frequency: first_time | recurring
- Related Features: existing_tool_or_feature

---
```

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` (learning), `ROB` (robotics issue), `FEAT` (feature request)
- YYYYMMDD: current date
- XXX: sequential number or random 3 chars (example: `001`, `A7B`)

Examples: `LRN-20250415-001`, `ROB-20250415-A3F`, `FEAT-20250415-002`

## Resolving Entries

When an issue is fixed, update the entry:

1. Change `**Status**: pending` to `**Status**: resolved`
2. Add a resolution block after Metadata:

```markdown
### Resolution
- **Resolved**: 2025-01-16T09:00:00Z
- **Commit/PR**: abc123 or #42
- **Validation**: simulation + HIL + controlled field test
- **Notes**: Parameter retuned, watchdog threshold adjusted, and safety test added
```

Other status values:
- `in_progress` - actively being diagnosed or fixed
- `wont_fix` - intentionally not addressed (add reason in Resolution notes)
- `promoted` - elevated to checklist, playbook, runbook, or core docs
- `promoted_to_skill` - extracted as reusable skill

## Detection Triggers

Automatically log when you encounter:

**Localization degradation** (issue + learning):
- Robot fails to localize in dynamic environment
- Covariance growth or pose jump after sensor occlusion
- Repeated relocalization events in stable map zones
- Odom drift divergence against fused pose estimate

**Planning failures** (issue + learning):
- Planner fails in narrow passage
- No valid path in obstacle-rich scenes
- Recovery loops exceed threshold
- Frequent oscillation between alternative paths

**Control instability** (issue + learning):
- Oscillatory control behavior appears
- Unstable PID tuning under payload changes
- Command saturation and watchdog warnings
- Tracking error diverges during low-speed maneuvers

**Sensor fusion anomalies** (issue + learning):
- Camera-lidar-imu timestamp mismatch
- Out-of-order sensor packets
- Frame transform inconsistencies
- Fusion jumps due to delayed sensor stream

**Hardware interface faults** (issue + learning):
- Driver drops packets
- CAN timeout bursts
- Serial disconnects
- Motor driver overcurrent faults

**Safety incidents** (issue + learning):
- Safety stop unexpectedly triggered
- Emergency brake event without true obstacle
- Boundary monitor false positives
- Interlock state transitions out of sequence

**Sim-to-real mismatches** (learning):
- Simulation success but real robot failure
- Sensor noise or latency assumptions differ from field
- Domain randomization lacks critical disturbances
- Control policy brittle under real-world traction or dynamics

**Power and thermal limits** (learning):
- Thermal throttling under sustained workload
- Battery sag causes degraded control rate
- Brownout events during high actuator demand
- Compute frequency throttling impacts planner timing

## Priority Guidelines

| Priority | When to Use | Robotics Examples |
|----------|-------------|-------------------|
| `critical` | Safety risk, collision potential, emergency stop instability, hardware damage risk | Emergency stop false negatives, repeated collision near-miss, motor overcurrent damage risk |
| `high` | Recurring failure that blocks autonomy missions | Planner fails in narrow corridor, localization drift in common dynamic scenes |
| `medium` | Significant but recoverable issue with available fallback | Sensor desync occasional spikes, moderate control oscillation with fallback enabled |
| `low` | Minor tuning or observability improvement | Dashboard labeling mismatch, non-critical telemetry naming cleanup |

## Area Tags

Use area tags to filter and route issues:

| Area | Scope |
|------|-------|
| `perception` | Object detection, feature extraction, sensor preprocessing |
| `localization` | Pose estimation, drift correction, relocalization strategies |
| `mapping` | Map quality, occupancy updates, semantic map consistency |
| `planning` | Global/local planning, feasibility, obstacle avoidance |
| `control` | PID/MPC/controller behavior, stability, actuator command tracking |
| `manipulation` | Grasp planning, arm trajectories, end-effector behavior |
| `navigation` | End-to-end mission routing and navigation state transitions |
| `safety` | Safety monitors, interlocks, emergency stop logic, boundaries |
| `simulation` | Simulator fidelity, scenario generation, domain randomization |
| `hardware_integration` | Drivers, buses, firmware, power systems, interfaces |

## Promoting to Permanent Robotics Standards

When a learning is broadly applicable (not a one-off fix), promote it to permanent project standards.

### When to Promote

- Same failure pattern appears in 2+ missions or sites
- Mitigation proves stable across sim and real robot
- Safety impact warrants mandatory guardrail
- Reproducible diagnostics workflow saves repeated debugging time

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Safety checklist | Mandatory pre-run and post-incident safety checks |
| Calibration playbook | Repeatable calibration/time-sync procedures |
| Tuning runbook | Stable controller/planner tuning workflow and limits |
| `SOUL.md` | Robotics behavior principles and non-negotiable guardrails |
| `AGENTS.md` | Multi-agent validation workflows and decision steps |
| `TOOLS.md` | Telemetry, replay, simulation, and diagnostics tooling guidance |
| Simulation test suite docs | Scenario matrices and acceptance thresholds |

### How to Promote

1. **Distill** the learning into concise operational rule or checklist item
2. **Place** it in the right target document
3. **Update** original entry:
   - Change `**Status**: pending` to `**Status**: promoted`
   - Add `**Promoted**: safety checklist` (or calibration playbook, tuning runbook, `SOUL.md`, `AGENTS.md`, `TOOLS.md`)

## Recurring Pattern Detection

If logging something similar to an existing entry:

1. **Search first**: `rg "keyword" .learnings/`
2. **Link entries**: add `**See Also**: ROB-20250110-001` in Metadata
3. **Bump priority** if recurrence grows and fallback weakens
4. **Escalate systemic fix** when recurrence suggests process or tooling gaps.

### Pattern Keys and Recurrence

Use `Pattern-Key` for dedupe, such as:
- `localization_drift.dynamic_aisle`
- `planning_failure.narrow_passage_clearance`
- `control_instability.low_speed_heading`
- `sensor_fusion_error.timestamp_skew`

When recurrence is tracked:
- Increment `Recurrence-Count`
- Update `Last-Seen`
- Add `See Also` links between related `LRN` and `ROB` entries

## Periodic Review Cadence

Review `.learnings/` at natural robotics development milestones:

### When to Review
- Before new field deployment
- After each incident postmortem
- At end of each tuning cycle
- Weekly during active autonomy development
- Before releasing updated safety or calibration docs

### Quick Status Check

```bash
# Count pending robotics entries
rg "Status\\*\\*: pending" .learnings/*.md | wc -l

# List high-priority unresolved robotics issues
rg -n "Priority\\*\\*: high|Priority\\*\\*: critical" .learnings/ROBOTICS_ISSUES.md

# Find all localization learnings
rg -n "localization_drift|Area\\*\\*: localization" .learnings/*.md

# Find unresolved safety incidents
rg -n "Area\\*\\*: safety" .learnings/ROBOTICS_ISSUES.md
```

### Review Actions

- Resolve fixed incidents and add validation evidence
- Promote recurring patterns to checklist/playbook/runbook
- Link related entries across learnings and issues
- Archive stale low-priority items if explicitly `wont_fix`
- Convert strong patterns into reusable skills

## Best Practices

1. **Safety first** - if there is risk to people, environment, or hardware, log and escalate immediately
2. **Capture synchronized telemetry** - include timestamps and subsystem context, not isolated log snippets
3. **Record reproducibility conditions** - include robot model, firmware, map, payload, and environment
4. **Use staged validation** - simulation -> HIL -> controlled field before declaring resolved
5. **Separate symptom from root cause** - emergency stop is symptom; stale safety mask may be cause
6. **Preserve fallback behavior context** - note which fallback mitigated risk and where it failed
7. **Track sim-to-real assumptions** - list what simulator omitted or simplified
8. **Treat power and thermal as first-class constraints** - degraded compute can mimic software defects
9. **Prefer minimal, actionable entries** - concise and precise entries are easier to promote
10. **Promote aggressively when recurrence appears** - repeated failures should become standards, not isolated notes

## Resolution Workflow

Follow this workflow for each `ROB` or `LRN` item:

1. **Triage**
   - classify severity and safety impact
   - assign area and category
2. **Reproduce**
   - replicate in closest safe environment
   - capture deterministic evidence when possible
3. **Diagnose**
   - isolate subsystem boundaries
   - verify whether failure is data, model, control, hardware, or integration
4. **Mitigate**
   - apply smallest safe change first
   - add guardrail if risk remains
5. **Validate**
   - run simulation/HIL/field checks per severity
   - verify no regression in adjacent subsystem
6. **Document**
   - update status and resolution block
   - link related entries and promotion target if warranted

## Hook Integration

Enable automatic reminders through agent hooks. This is opt-in.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` in your project:

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-robotics/scripts/activator.sh"
      }]
    }]
  }
}
```

This injects a robotics-focused reminder after each prompt (~50-100 tokens overhead).

### Advanced Setup (With Error Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-robotics/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-robotics/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` when you want automatic scan of command output for robotics/autonomy failure patterns.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate robotics learnings |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Detects common robotics/autonomy error terms in output |

See `references/hooks-setup.md` for complete setup and troubleshooting.

## Automatic Skill Extraction

When a robotics learning is valuable enough to become reusable, extract it.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same failure mode appears in 2+ subsystems, robots, or deployments |
| **Verified** | Status is `resolved` with validated mitigation |
| **Non-obvious** | Required meaningful diagnosis beyond trivial config typo |
| **Broadly applicable** | Useful across projects or autonomy stacks |
| **Safety/ops value** | Prevents incidents or reduces operational risk |
| **User-flagged** | User says "save this as a skill" or equivalent |

### Extraction Workflow

1. **Identify candidate**: learning meets extraction criteria
2. **Run helper** (or create manually):
   ```bash
   ./skills/self-improving-robotics/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-robotics/scripts/extract-skill.sh skill-name
   ```
3. **Customize SKILL.md**: fill template with telemetry-backed robotics content
4. **Update learning**: set status to `promoted_to_skill`, add `Skill-Path`
5. **Verify**: ensure extracted skill is clear and safe to apply

### Extraction Detection Triggers

**In conversation**:
- "This keeps happening in field tests"
- "Document this as a reusable robotics workflow"
- "Save this mitigation as a skill"
- "We keep seeing this planner/localization/control failure"

**In entries**:
- Multiple `See Also` links
- High/critical resolved issues with strong validations
- Repeated `Pattern-Key` across environments
- Similar `ROB` and `LRN` entries over multiple dates

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks (UserPromptSubmit, PostToolUse) | Automatic via `error-detector.sh` |
| Codex CLI | Hooks (same pattern) | Automatic via hook scripts |
| GitHub Copilot | Manual (`.github/copilot-instructions.md`) | Manual review |
| OpenClaw | Workspace injection + inter-agent messaging | Via sessions and shared `.learnings/` |

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/robotics/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: robotics
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (robotics)
Only trigger this skill automatically for robotics signals such as:
- `planner|localization|slam|trajectory|control loop`
- `sensor fusion|actuator fault|sim2real|safety stop`
- explicit robotics intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/robotics/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
