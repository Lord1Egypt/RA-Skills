---
name: self-improving-domotics
description: "Captures smart-home automation conflicts, sensor drift, device connectivity failures, integration regressions, safety rule gaps, and energy optimization opportunities for continuous domotics improvement. Use when: (1) Automations conflict, loop, or misfire, (2) Sensors become stale or inaccurate, (3) Devices are unreachable or intermittently offline, (4) Cloud or local integrations break, (5) Occupancy detection is inconsistent with reality, (6) Latency causes delayed or jittery automations, (7) Energy usage patterns are inefficient, (8) Safety automations need stronger guardrails."
---

# Self-Improving Domotics Skill

Log domotics-specific learnings, issues, and feature requests to markdown files for continuous improvement of smart home systems.

This skill is documentation and reminder guidance only. It does not execute physical actuator actions directly.

Always prefer safe defaults and human confirmation for high-impact routines involving door locks, alarms, gas or water shutoff, and heaters.

## First-Use Initialisation

Before logging anything, ensure `.learnings/` exists in the project or workspace root and contains the required files:

```bash
mkdir -p .learnings
[ -f .learnings/LEARNINGS.md ] || printf "# Domotics Learnings\n\nSensor reliability lessons, automation quality findings, integration regressions, safety gaps, and energy optimization observations.\n\n**Categories**: automation_conflict | sensor_drift | device_unreachable | integration_break | energy_optimization | safety_rule_gap | occupancy_mismatch | latency_jitter\n**Areas**: lighting | climate | security | access_control | energy | sensors | routines | voice_assistants | integrations | network\n\n---\n" > .learnings/LEARNINGS.md
[ -f .learnings/DOMOTICS_ISSUES.md ] || printf "# Domotics Issues Log\n\nRecurring smart-home failures, rule conflicts, unreliable sensors, unreachable devices, and safety-relevant incidents.\n\n---\n" > .learnings/DOMOTICS_ISSUES.md
[ -f .learnings/FEATURE_REQUESTS.md ] || printf "# Domotics Feature Requests\n\nAutomation, observability, reliability, and safety capability requests.\n\n---\n" > .learnings/FEATURE_REQUESTS.md
```

Never overwrite existing files. The commands are no-op when already initialised.

Do not log secrets, access tokens, lock PINs, alarm codes, network credentials, or personal household schedules in plain text.

If automatic reminders are needed, enable hook integration (opt-in) in [Hook Integration](#hook-integration).

## Quick Reference

| Situation | Action |
|-----------|--------|
| Two automations fire opposite commands | Log in `.learnings/DOMOTICS_ISSUES.md` as `automation_conflict` |
| Zigbee/Z-Wave devices intermittently disappear | Log issue as `device_unreachable` with radio and topology details |
| Occupancy says "home" while house is empty | Log learning as `occupancy_mismatch` and add confidence notes |
| HVAC oscillates around target temperature | Log learning as `latency_jitter` or `sensor_drift` |
| Integration API response schema changed | Log issue as `integration_break` and link vendor release notes |
| Rule repeatedly misses schedule window | Log issue as `latency_jitter` with timeline and queue delay |
| Energy spike after automation rollout | Log learning as `energy_optimization` with before/after kWh |
| Safety routine lacks confirmation step | Log learning as `safety_rule_gap` and escalate priority |
| Pattern appears 3+ times | Add `See Also`, raise priority, and consider promotion |
| Reusable approach discovered | Promote to playbook, compatibility matrix, rule library, or safety automation standard |

## OpenClaw Setup (Recommended)

OpenClaw is the primary platform for this skill. It supports workspace injection and optional hooks for proactive reminders.

### Installation

**Via ClawdHub (recommended):**
```bash
clawdhub install self-improving-domotics
```

**Manual clone:**
```bash
git clone https://github.com/jose-compu/self-improving-domotics.git ~/.openclaw/skills/self-improving-domotics
```

### Workspace Structure

OpenClaw injects workspace files at session start:

```
~/.openclaw/workspace/
├── AGENTS.md / SOUL.md / TOOLS.md / MEMORY.md
├── memory/YYYY-MM-DD.md
└── .learnings/{LEARNINGS.md, DOMOTICS_ISSUES.md, FEATURE_REQUESTS.md}
```

### Create Learning Files

```bash
mkdir -p ~/.openclaw/workspace/.learnings
```

Then create (or copy from `assets/`) the domotics logs:
- `LEARNINGS.md` - reliability and optimization learnings
- `DOMOTICS_ISSUES.md` - concrete failures and incident-style timelines
- `FEATURE_REQUESTS.md` - automation and observability capability requests

### Promotion Targets

Promote proven learnings to durable assets:

| Learning Type | Promote To | Example |
|---------------|------------|---------|
| Reproducible automation fix | Home automation playbook | "Night routine fails when motion timeout overlaps lock delay" |
| Device reliability pattern | Device compatibility matrix | "Battery sensors on firmware X drift after 30 days" |
| Rule-quality pattern | Automation rule library | "Debounce + cooldown template for occupancy-triggered lighting" |
| Human-safety safeguard | Safety automations | "Two-step confirmation for door unlock at night" |
| Communication and caution patterns | `SOUL.md` | "Ask explicit confirmation for high-impact routines" |
| Cross-agent routine design | `AGENTS.md` | "Split analysis of integrations vs radio reliability" |
| Integration constraints | `TOOLS.md` | "Webhook retry backoff and schema validation rules" |

### Optional: Enable Hook

For reminder injection during session bootstrap:

```bash
cp -r hooks/openclaw ~/.openclaw/hooks/self-improving-domotics
openclaw hooks enable self-improving-domotics
```

See `references/openclaw-integration.md` for details.

---

## Generic Setup (Other Agents)

For Claude Code, Codex, Copilot, or other agents:

```bash
mkdir -p .learnings
```

Create the three files with the headers shown in First-Use Initialisation.

### Add reference to agent instruction files

Add to `AGENTS.md`, `CLAUDE.md`, or `.github/copilot-instructions.md`:

#### Self-Improving Domotics Workflow

When smart-home issues or patterns are discovered:
1. Log to `.learnings/DOMOTICS_ISSUES.md`, `.learnings/LEARNINGS.md`, or `.learnings/FEATURE_REQUESTS.md`
2. Promote verified recurring patterns to:
   - Home automation playbooks
   - Device compatibility matrix
   - Automation rule library
   - Safety automations

## Logging Format

### Learning Entry [LRN-YYYYMMDD-XXX]

Append to `.learnings/LEARNINGS.md`:

```markdown
## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending
**Area**: lighting | climate | security | access_control | energy | sensors | routines | voice_assistants | integrations | network

### Summary
One-line domotics learning

### Details
What happened, why behavior was suboptimal, what rule/device/integration assumptions failed,
and what robust approach should be preferred.

### Safe Operating Notes
- High-impact actuator involved: yes | no
- Human confirmation required: yes | no
- Fallback on uncertainty: no action | notify-only | safe mode

### Suggested Action
Specific design, rule, configuration, or documentation change

### Metadata
- Source: automation_event | incident_review | user_report | monitoring_alert | simplify-and-harden
- Category: automation_conflict | sensor_drift | device_unreachable | integration_break | energy_optimization | safety_rule_gap | occupancy_mismatch | latency_jitter
- Related Devices: thermostat-v2, zigbee-motion-3
- Related Integrations: home-assistant | mqtt | matter | zigbee2mqtt | alexa
- Related Entries: DOM-20260413-001
- Tags: tag1, tag2
- See Also: LRN-20260410-002
- Pattern-Key: occupancy.false_positive_night | integration.schema_change (optional)
- Recurrence-Count: 1 (optional)
- First-Seen: 2026-04-13 (optional)
- Last-Seen: 2026-04-13 (optional)

---
```

### Domotics Issue Entry [DOM-YYYYMMDD-XXX]

Append to `.learnings/DOMOTICS_ISSUES.md`:

```markdown
## [DOM-YYYYMMDD-XXX] issue_name

**Logged**: ISO-8601 timestamp
**Priority**: medium | high | critical
**Status**: pending
**Area**: lighting | climate | security | access_control | energy | sensors | routines | voice_assistants | integrations | network

### Summary
Brief issue statement

### Incident Timeline
| Time | Event |
|------|-------|
| T+0m | Trigger observed |
| T+Xm | Detection or alert |
| T+Xm | Mitigation applied |
| T+Xm | Verified stable or still failing |

### Root Cause
Underlying reason (rule conflict, stale sensor, network partition, vendor API change, etc.)

### Correct Approach
How system design or operating procedure should handle this scenario

### Home Impact
- User Impact: none | minor | significant
- Safety Impact: none | potential | high
- Security Impact: none | potential | high
- Energy Impact: neutral | increased | reduced
- Manual Intervention: none | required

### Prevention
Guardrails, retries, validation, fallback policy, notification policy, or routine redesign

### Context
- Trigger: monitoring_alert | user_report | regression | integration_update | schedule_miss
- Topology: local_only | cloud_assisted | hybrid
- Network Layer: wifi | zigbee | zwave | thread | ethernet | mixed

### Metadata
- Related Devices: lock-front-door, motion-hallway
- Related Files: automations/night-routine.yaml
- Related Entries: LRN-20260413-001
- See Also: DOM-20260410-002

---
```

### Feature Request Entry [FEAT-YYYYMMDD-XXX]

Append to `.learnings/FEATURE_REQUESTS.md`:

```markdown
## [FEAT-YYYYMMDD-XXX] capability_name

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high
**Status**: pending
**Area**: lighting | climate | security | access_control | energy | sensors | routines | voice_assistants | integrations | network

### Requested Capability
What automation or reliability capability is needed

### User Context
Why this matters, what failure pattern it prevents, what experience it improves

### Complexity Estimate
simple | medium | complex

### Suggested Implementation
Specific architecture, tooling, API contracts, and rollout safety controls

### Metadata
- Frequency: first_time | recurring
- Related Features: feature_name_or_component

---
```

## Entry Types and Categories

### Entry Types

| Type | Meaning | File |
|------|---------|------|
| `LRN` | Learning from behavior, reliability, safety, or optimization | `.learnings/LEARNINGS.md` |
| `DOM` | Domotics issue or incident requiring corrective handling | `.learnings/DOMOTICS_ISSUES.md` |
| `FEAT` | Feature request for tooling, automation, observability, or policy | `.learnings/FEATURE_REQUESTS.md` |

### Categories

| Category | Use When |
|----------|----------|
| `automation_conflict` | Two or more rules produce contradictory actuator commands |
| `sensor_drift` | Sensor readings diverge from reality over time or conditions |
| `device_unreachable` | Device becomes offline, intermittently available, or non-responsive |
| `integration_break` | Integration API/auth/schema changes break automations |
| `energy_optimization` | Opportunity to reduce kWh peaks or unnecessary runtime |
| `safety_rule_gap` | Automation lacks safeguards for high-impact physical actions |
| `occupancy_mismatch` | Occupancy inference does not match actual presence |
| `latency_jitter` | Timing inconsistency causes delayed, oscillatory, or missed actions |

## ID Generation

Format: `TYPE-YYYYMMDD-XXX`
- TYPE: `LRN` | `DOM` | `FEAT`
- YYYYMMDD: current date
- XXX: sequential or random 3-char suffix (`001`, `A9K`)

Examples:
- `LRN-20260413-001`
- `DOM-20260413-A7B`
- `FEAT-20260413-002`

## Resolving Entries

When addressed, update:
1. `**Status**: pending` -> `**Status**: resolved`
2. Add resolution section:

```markdown
### Resolution
- **Resolved**: 2026-04-13T18:20:00Z
- **Action Taken**: Added cooldown and guard condition to occupancy-lighting routine
- **Notes**: Added manual confirmation before lock and alarm state transitions at night
```

Other valid statuses:
- `in_progress` - actively investigated
- `wont_fix` - accepted as non-actionable (include reason)
- `promoted` - promoted to permanent target
- `promoted_to_skill` - extracted to reusable skill

## Detection Triggers

Automatically log when these domotics signals appear.

### Automation Conflict Triggers (-> `DOM` or `LRN`)
- Rapid repeated toggles, opposing commands, or circular rule loops
- Overlapping conditions without explicit precedence

### Device Reachability Triggers (-> `DOM`)
- Offline/unreachable warnings, repeated timeouts, missing acknowledgments
- Zigbee/Z-Wave mesh drops or MQTT entity unavailable states

### Integration Break Triggers (-> `DOM` or `LRN`)
- Webhook/API auth/schema/endpoint changes causing parser or action failures
- Voice-assistant intent mapping regressions after platform updates

### Occupancy and Sensor Triggers (-> `LRN`)
- Occupancy confidence mismatches observed reality
- Stale/impossible sensor values beyond threshold windows

### Timing and Schedule Triggers (-> `DOM`)
- Missed schedules, delayed execution, or jitter-induced duplicate actions
- Timezone/sunrise-sunset offset errors affecting routines

### Safety Triggers (-> `LRN` high/critical)
- High-impact routines executing without human confirmation
- Lock/alarm/gas/water/heater actions under uncertain confidence

## Priority Guidelines

| Priority | When to Use | Domotics Examples |
|----------|-------------|------------------|
| `critical` | Potential physical harm, security exposure, or hazardous state | Heater stuck on with failed thermostat feedback; lock opens on false occupancy; gas shutoff rule triggers incorrectly |
| `high` | Significant reliability/security degradation or repeated unreachable devices | Repeated front-door lock offline; alarm routine disabled by integration break; occupancy loop causing night disruptions |
| `medium` | Operational nuisance, moderate inefficiency, isolated integration mismatch | HVAC overshoot after schedule changes; webhook retries fail for one integration |
| `low` | Documentation improvement, minor optimization, edge-case tuning | Non-critical light scene delay under unusual network load |

## Area Tags

| Area | Scope |
|------|-------|
| `lighting` | Scene control, occupancy-based lights, dimming and schedule logic |
| `climate` | HVAC, thermostat feedback loops, humidity controls |
| `security` | Alarm states, intrusion sensors, siren and notification policies |
| `access_control` | Smart locks, garage doors, entry routines, authentication checks |
| `energy` | Consumption scheduling, peak shaving, tariff-aware automations |
| `sensors` | Motion, contact, temperature, humidity, air quality, leak sensors |
| `routines` | Cross-device orchestrations and multi-step automation flows |
| `voice_assistants` | Voice intent mapping, command ambiguity, assistant integrations |
| `integrations` | Cloud/local APIs, webhooks, middleware platforms |
| `network` | Wi-Fi, Zigbee, Z-Wave, Thread, MQTT broker, latency behavior |

## Promoting to Permanent Domotics Standards

Promote only when learning is verified, repeatable, and broadly useful.

### Promotion Targets

| Target | What Belongs There |
|--------|-------------------|
| Home automation playbooks | Incident-tested troubleshooting and recovery procedures |
| Device compatibility matrix | Firmware/model interoperability, known limits, workaround notes |
| Automation rule library | Reusable rule templates with guards, debounce, and precedence |
| Safety automations | High-impact routines with confirmations, rollback, and audit trails |
| `SOUL.md` | Behavioral safety defaults and communication constraints |
| `AGENTS.md` | Multi-agent decomposition for diagnostics and remediation planning |
| `TOOLS.md` | Integration constraints, retry policies, and validation requirements |

### When to Promote

- Pattern recurs 3+ times within a month
- Root cause and corrective pattern are validated
- Applies across multiple homes/devices/integrations
- Includes explicit safety boundary for high-impact actuations

### How to Promote

1. Distill the learning into concise, reusable rule language
2. Add it to the best promotion target
3. Update original entry:
   - `**Status**: promoted`
   - `**Promoted**: home automation playbook` (or matrix/library/safety automation)

## Recurring Pattern Detection

If an event resembles existing entries:

1. Search first: `rg "keyword|Pattern-Key" .learnings/`
2. Add `See Also` links to related IDs
3. Increase priority if recurrence grows
4. Move from one-off mitigation to systemic pattern fix

## Simplify & Harden Feed

Ingest strong candidates from simplify-and-harden reviews:

1. Use `Pattern-Key` as dedupe key
2. Search existing records: `rg "Pattern-Key: <key>" .learnings/LEARNINGS.md`
3. If found:
   - increment `Recurrence-Count`
   - update `Last-Seen`
   - add cross-links in `See Also`
4. If not found:
   - create new `LRN` entry with `Source: simplify-and-harden`

Promotion threshold:
- `Recurrence-Count >= 3`
- observed across 2+ areas or integration paths
- validated over at least 14 days

## Periodic Review

Review `.learnings/` at natural checkpoints.

### When to Review

- Before major automation rollout
- After firmware updates
- After integration API changes
- Weekly reliability retrospective
- After safety-relevant incidents

### Quick Status Check

```bash
rg "Status\*\*: pending" .learnings/*.md | wc -l
rg -n "Priority\*\*: critical|Priority\*\*: high" .learnings/DOMOTICS_ISSUES.md
rg -n "safety_rule_gap|device_unreachable|integration_break" .learnings/*.md
rg -n "energy_optimization|occupancy_mismatch" .learnings/LEARNINGS.md
```

### Review Actions

- Resolve fixed entries with evidence
- Promote repeated patterns to permanent targets
- Tune thresholds and rule precedence
- Ensure confirmation steps exist for high-impact routines

## Safety Posture and Operational Boundaries

This skill does not directly control physical devices. It captures and structures learnings so humans can implement changes safely.

### Mandatory Safe Defaults

- Prefer notify-only mode when confidence is low
- Require explicit human confirmation for:
  - door lock or unlock routines
  - alarm arm/disarm transitions
  - gas or water shutoff actions
  - heater on/off changes with high thermal impact
- Keep conservative fallback state on sensor ambiguity
- Separate detection logic from actuator execution logic

## Hook Integration

Hooks are optional and reminder-only. They must not perform direct actuator actions.

### Quick Setup (Claude Code / Codex)

Create `.claude/settings.json` (or equivalent):

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-domotics/scripts/activator.sh"
      }]
    }]
  }
}
```

### Advanced Setup (With Output Detection)

```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-domotics/scripts/activator.sh"
      }]
    }],
    "PostToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./skills/self-improving-domotics/scripts/error-detector.sh"
      }]
    }]
  }
}
```

Enable `PostToolUse` only if signal detection on tool output is desired.

### Available Hook Scripts

| Script | Hook Type | Purpose |
|--------|-----------|---------|
| `scripts/activator.sh` | UserPromptSubmit | Reminds to evaluate domotics learnings after each task |
| `scripts/error-detector.sh` | PostToolUse (Bash) | Detects high-signal domotics issue phrases and prints reminder-only guidance |

See `references/hooks-setup.md` for troubleshooting.

## Automatic Skill Extraction

When a domotics learning is stable and reusable, extract it into a standalone skill.

### Skill Extraction Criteria

| Criterion | Description |
|-----------|-------------|
| **Recurring** | Same pattern appears 3+ times |
| **Verified** | Entry status is `resolved` with proof |
| **Safety-aware** | Includes safe defaults and confirmation strategy for high-impact routines |
| **Non-obvious** | Insight required investigation, not trivial documentation |
| **Broadly applicable** | Works across homes, devices, or integration stacks |
| **User-flagged** | User requests extraction explicitly |

### Extraction Workflow

1. Identify a candidate that meets criteria
2. Run helper:
   ```bash
   ./skills/self-improving-domotics/scripts/extract-skill.sh skill-name --dry-run
   ./skills/self-improving-domotics/scripts/extract-skill.sh skill-name
   ```
3. Fill generated `SKILL.md` TODO placeholders
4. Update source entry:
   - `**Status**: promoted_to_skill`
   - `**Skill-Path**: skills/skill-name`
5. Validate in a fresh session

### Extraction Detection Triggers

- Conversation signals: "keeps happening", "save as skill", "reusable safety pattern"
- Entry signals: multiple `See Also`, high/critical resolved status, repeated `Pattern-Key`

## Multi-Agent Support

| Agent | Activation | Detection |
|-------|-----------|-----------|
| Claude Code | Hooks + manual review | `error-detector.sh` + periodic review |
| Codex CLI | Hooks + manual review | same scripts and workflow |
| GitHub Copilot | Instruction-file guidance | manual logging and periodic review |
| OpenClaw | Workspace injection + hook integration | bootstrap reminder and optional detection |

## Best Practices

1. Prefer deterministic automations over hidden side effects
2. Add debounce, cooldown, and guard conditions for noisy sensors
3. Separate occupancy estimation from high-impact actuations
4. Design explicit rule precedence to avoid conflicts
5. Treat integration contracts as versioned dependencies
6. Capture before/after energy metrics for optimization claims
7. Keep manual override paths available for security and climate routines
8. Document safe fallback behavior for every critical routine

## Gitignore Options

**Keep learnings local**:
```gitignore
.learnings/
```

**Track learnings in repo**:
Do not add `.learnings/` to `.gitignore`.

**Hybrid**:
```gitignore
.learnings/*.md
!.learnings/.gitkeep
```

## Reference Links
- Skill repository: `https://github.com/jose-compu/self-improving-domotics.git`
- Hook setup walkthrough: `references/hooks-setup.md`
Use this skill to improve reliability, safety, and efficiency through better documentation and review loops. Keep workflows reminder-only, and require human confirmation for high-impact routines.

## Stackability Contract (Standalone + Multi-Skill)

This skill is standalone-compatible and stackable with other self-improving skills.

### Namespaced Logging (recommended for 2+ skills)
- Namespace for this skill: `.learnings/domotics/`
- Keep current standalone behavior if you prefer flat files.
- Optional shared index for all skills: `.learnings/INDEX.md`

### Required Metadata
Every new entry must include:

```markdown
**Skill**: domotics
```

### Hook Arbitration (when 2+ skills are enabled)
- Use one dispatcher hook as the single entrypoint.
- Dispatcher responsibilities: route by matcher, dedupe repeated events, and rate-limit reminders.
- Suggested defaults: dedupe key = `event + matcher + file + 5m_window`; max 1 reminder per skill every 5 minutes.

### Narrow Matcher Scope (domotics)
Only trigger this skill automatically for domotics signals such as:
- `sensor|actuator|automation|iot|home assistant`
- `energy profile|false trigger|device offline|scene failure`
- explicit domotics intent in user prompt

### Cross-Skill Precedence
When guidance conflicts, apply:
1. `security`
2. `engineering`
3. `coding`
4. `ai`
5. user-explicit domain skill
6. `meta` as tie-breaker

### Ownership Rules
- This skill writes only to `.learnings/domotics/` in stackable mode.
- It may read other skill folders for cross-linking, but should not rewrite their entries.
