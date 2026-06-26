#!/bin/bash
# Domotics Self-Improvement Activator Hook
# Reminder-only output; no direct physical actions.

set -e

cat << 'EOF'
<domotics-self-improvement-reminder>
After completing this smart-home task, evaluate if extractable knowledge emerged:
- Automation conflict or loop? -> DOMOTICS_ISSUES.md (automation_conflict)
- Sensor drift/stale readings? -> LEARNINGS.md (sensor_drift)
- Device unreachable/offline/timeout? -> DOMOTICS_ISSUES.md (device_unreachable)
- Integration schema/auth/webhook break? -> DOMOTICS_ISSUES.md (integration_break)
- Occupancy false positive/negative? -> LEARNINGS.md (occupancy_mismatch)
- Latency or schedule miss? -> DOMOTICS_ISSUES.md (latency_jitter)
- Energy optimization opportunity? -> LEARNINGS.md (energy_optimization)
- Safety routine missing guard? -> LEARNINGS.md (safety_rule_gap)

For high-impact routines (locks, alarms, gas/water shutoff, heaters): require human confirmation.
This workflow is documentation/reminder only and does not actuate devices directly.
</domotics-self-improvement-reminder>
EOF
