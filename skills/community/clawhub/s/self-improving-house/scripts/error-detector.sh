#!/bin/bash
# Domotics Self-Improvement Issue Detector Hook
# Scans tool output for high-signal domotics patterns.
# Reminder-only; does not execute physical actions.

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ISSUE_PATTERNS=(
    "device offline"
    "device unavailable"
    "unreachable"
    "timeout"
    "timed out"
    "no response"
    "zigbee"
    "zwave"
    "z-wave"
    "mqtt disconnect"
    "mqtt unavailable"
    "webhook failed"
    "webhook failure"
    "integration error"
    "schema mismatch"
    "api changed"
    "automation loop"
    "rule conflict"
    "conflicting automation"
    "occupancy stale"
    "stale occupancy"
    "sensor unavailable"
    "sensor stale"
    "jitter"
    "latency"
    "schedule missed"
    "missed schedule"
    "alarm"
    "lock"
    "heater"
    "water shutoff"
    "gas shutoff"
)

contains_issue=false
for pattern in "${ISSUE_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_issue=true
        break
    fi
done

if [ "$contains_issue" = true ]; then
    cat << 'EOF'
<domotics-issue-detected>
High-signal domotics issue detected in tool output. Consider logging:
- automation_conflict / latency_jitter / device_unreachable -> DOMOTICS_ISSUES.md [DOM-YYYYMMDD-XXX]
- sensor_drift / occupancy_mismatch / safety_rule_gap / energy_optimization -> LEARNINGS.md [LRN-YYYYMMDD-XXX]
- tooling or platform capability gap -> FEATURE_REQUESTS.md [FEAT-YYYYMMDD-XXX]

Reminder-only workflow: do not execute direct actuator actions from this hook.
For high-impact routines (locks, alarms, gas/water shutoff, heaters), use human confirmation.
</domotics-issue-detected>
EOF
fi
