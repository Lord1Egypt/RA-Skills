#!/bin/bash
# Robotics Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect robotics/autonomy failures in command output
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "localization"
    "localisation"
    "drift"
    "odom"
    "odometry"
    "imu"
    "lidar"
    "camera timeout"
    "timestamp mismatch"
    "desync"
    "sync lost"
    "planner failed"
    "planning failed"
    "no valid path"
    "trajectory infeasible"
    "collision"
    "collision imminent"
    "safety stop"
    "emergency stop"
    "emergency brake"
    "watchdog"
    "watchdog timeout"
    "CAN timeout"
    "can timeout"
    "serial disconnect"
    "packet drop"
    "dropped packets"
    "motor overcurrent"
    "overcurrent"
    "thermal"
    "throttle"
    "throttling"
    "brownout"
    "battery sag"
    "low voltage"
    "power rail"
    "segfault"
    "Segmentation fault"
    "panic"
    "assertion failed"
    "ERROR"
    "error:"
    "FATAL"
)

contains_error=false
for pattern in "${ERROR_PATTERNS[@]}"; do
    if [[ "$OUTPUT" == *"$pattern"* ]]; then
        contains_error=true
        break
    fi
done

if [ "$contains_error" = true ]; then
    cat << 'EOF'
<robotics-error-detected>
A robotics/autonomy issue term was detected in command output. Consider logging to .learnings/ if:
- Operational failure with repro context → ROBOTICS_ISSUES.md [ROB-YYYYMMDD-XXX]
- Root-cause learning about autonomy stack behavior → LEARNINGS.md [LRN-YYYYMMDD-XXX]
- Tooling or capability gap discovered → FEATURE_REQUESTS.md [FEAT-YYYYMMDD-XXX]

Capture subsystem area, synchronized timestamps, telemetry summary, and safety impact.
</robotics-error-detected>
EOF
fi
