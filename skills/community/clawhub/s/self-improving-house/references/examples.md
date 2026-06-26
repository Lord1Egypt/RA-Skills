# Domotics Entry Examples

Concrete examples for `LRN`, `DOM`, and `FEAT` entries.

## Example 1: Conflicting Automations (Lighting)

```markdown
## [DOM-20260413-001] hallway_light_conflict

**Logged**: 2026-04-13T19:10:00Z
**Priority**: high
**Status**: pending
**Area**: lighting

### Summary
Night motion routine turns hallway lights on while sleep routine turns them off every 20 seconds.

### Incident Timeline
| Time | Event |
|------|-------|
| T+0m | Motion trigger fires after 23:00 |
| T+1m | Sleep routine "all-off" executes |
| T+2m | Motion retriggers and loop starts |

### Root Cause
Overlapping conditions without precedence or cooldown.

### Prevention
Add precedence: sleep mode dominates. Add 120s cooldown.

---
```

## Example 2: Occupancy False Positive

```markdown
## [LRN-20260413-001] occupancy_mismatch

**Logged**: 2026-04-13T19:30:00Z
**Priority**: high
**Status**: pending
**Area**: sensors

### Summary
Home marked occupied due to stale BLE beacon, preventing alarm arming.

### Details
Presence remained true for 9 hours after all residents left.

### Safe Operating Notes
- High-impact actuator involved: yes
- Human confirmation required: yes
- Fallback on uncertainty: notify-only

### Metadata
- Pattern-Key: occupancy.stale_ble_presence

---
```

## Example 3: HVAC Overshoot

```markdown
## [LRN-20260413-002] latency_jitter

**Logged**: 2026-04-13T20:00:00Z
**Priority**: medium
**Status**: pending
**Area**: climate

### Summary
HVAC overshoots target by 2.3C due to delayed temperature updates and aggressive rule.

### Suggested Action
Use moving average from two sensors + minimum runtime and cooldown.

---
```

## Example 4: Lock Automation Safety Guard

```markdown
## [LRN-20260413-003] safety_rule_gap

**Logged**: 2026-04-13T20:15:00Z
**Priority**: critical
**Status**: pending
**Area**: access_control

### Summary
Auto-unlock at arrival can trigger from low-confidence geofence event.

### Safe Operating Notes
- High-impact actuator involved: yes
- Human confirmation required: yes
- Fallback on uncertainty: no action

### Suggested Action
Require dual signal (geofence + BLE) and explicit user confirmation after 22:00.

---
```

## Example 5: Integration API Change

```markdown
## [DOM-20260413-002] weather_api_schema_break

**Logged**: 2026-04-13T21:00:00Z
**Priority**: high
**Status**: pending
**Area**: integrations

### Summary
Weather provider changed `temp_c` to `temperature.celsius`, breaking climate preheat routine.

### Root Cause
Integration parser had hard-coded field names and no schema version checks.

### Prevention
Add schema validation, feature flags, and fallback parser.

---
```

## Example 6: Energy Optimization Pattern

```markdown
## [LRN-20260413-004] energy_optimization

**Logged**: 2026-04-13T21:20:00Z
**Priority**: medium
**Status**: pending
**Area**: energy

### Summary
Shifting water heater preheat outside peak tariff reduced daily usage cost by 14%.

### Details
Preheat moved from 18:00 to 16:30 with occupancy gate retained.

---
```

## Example 7: Promoted Playbook

```markdown
## [LRN-20260401-006] device_unreachable

**Logged**: 2026-04-01T10:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: home automation playbook
**Area**: network

### Summary
Systematic recovery sequence for Zigbee mesh partitions after power outages.

### Metadata
- Pattern-Key: connectivity.zigbee_mesh_recovery
- Recurrence-Count: 5

---
```

## Example 8: Promoted Skill

```markdown
## [LRN-20260405-004] automation_conflict

**Logged**: 2026-04-05T12:40:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/night-occupancy-lock-guard
**Area**: security

### Summary
Reusable guard pattern to prevent lock/alarm state changes on uncertain occupancy.

### Metadata
- Pattern-Key: safety.lock_guard_uncertain_occupancy
- See Also: DOM-20260413-001, LRN-20260413-001

---
```
