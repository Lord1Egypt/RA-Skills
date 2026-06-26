#!/bin/bash
# Robotics Self-Improvement Activator Hook
# Triggers on UserPromptSubmit to remind about robotics-specific learning capture
# Keep output minimal (~50-100 tokens) to minimize overhead

set -e

cat << 'EOF'
<robotics-self-improvement-reminder>
After completing this robotics task, evaluate if extractable knowledge emerged:
- Robot fails to localize in dynamic environment? → ROBOTICS_ISSUES.md
- Planner fails in narrow passage or obstacle-rich scene? → ROBOTICS_ISSUES.md
- Oscillatory control behavior / unstable PID tuning? → ROBOTICS_ISSUES.md
- Sensor desync (camera-lidar-imu timestamp mismatch)? → ROBOTICS_ISSUES.md
- Hardware driver drops packets / CAN timeout / serial disconnect? → ROBOTICS_ISSUES.md
- Safety stop or emergency brake unexpectedly triggered? → ROBOTICS_ISSUES.md
- Simulation success but real robot failure? → LEARNINGS.md (sim_to_real_gap)
- Thermal throttling, battery sag, or power brownout? → LEARNINGS.md (power_thermal_constraint)

If recurring pattern (3+ occurrences): promote to safety checklist, calibration playbook, or tuning runbook.
If broadly applicable: consider skill extraction.
</robotics-self-improvement-reminder>
EOF
