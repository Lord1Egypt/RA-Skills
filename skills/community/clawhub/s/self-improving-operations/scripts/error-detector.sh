#!/bin/bash
# Operations Self-Improvement Error Detector Hook
# Triggers on PostToolUse for Bash to detect operational errors
# Reads CLAUDE_TOOL_OUTPUT environment variable

set -e

OUTPUT="${CLAUDE_TOOL_OUTPUT:-}"

ERROR_PATTERNS=(
    "incident"
    "outage"
    "degraded"
    "alert"
    "threshold"
    "capacity"
    "timeout"
    "retry"
    "rollback"
    "deploy failed"
    "OOM"
    "OOMKilled"
    "disk full"
    "No space left"
    "connection refused"
    "SLA"
    "SLO"
    "error budget"
    "CrashLoopBackOff"
    "ImagePullBackOff"
    "Evicted"
    "NotReady"
    "Unhealthy"
    "FailedScheduling"
    "circuit breaker"
    "rate limit"
    "429"
    "503"
    "502"
    "504"
    "connection pool"
    "deadlock"
    "replication lag"
    "queue depth"
    "backpressure"
    "throttle"
    "terminated"
    "killed"
    "SIGKILL"
    "SIGTERM"
    "health check failed"
    "certificate expired"
    "cert expired"
    "TLS handshake"
    "DNS resolution"
    "unreachable"
    "failed to connect"
    "deployment failed"
    "pipeline failed"
    "build failed"
    "rollback completed"
    "canary failed"
    "error rate"
    "latency spike"
    "memory pressure"
    "cpu throttling"
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
<operations-error-detected>
An operational issue was detected in command output. Consider logging to .learnings/ if:
- Incident or outage requiring response → OPERATIONS_ISSUES.md [OPS-YYYYMMDD-XXX]
- Capacity threshold breached → OPERATIONS_ISSUES.md with capacity_issue category
- Deployment failure or rollback → OPERATIONS_ISSUES.md with change context
- Alert fatigue or noisy monitor → LEARNINGS.md with automation_gap or monitoring area
- Manual remediation that should be automated → LEARNINGS.md with toil_accumulation

Include timeline, impact metrics, and DORA metrics context. Never log secrets or PII.
</operations-error-detected>
EOF
fi
