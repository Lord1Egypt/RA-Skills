# CrashLoopBackOff Runbook

## Use this when

- A pod is repeatedly restarting
- The service is unhealthy after a rollout
- You need a fast first-pass diagnosis before deeper debugging

## Triage

1. Identify the latest warnings:
   - `kubectl get events -n production --sort-by='.lastTimestamp' | tail -20`
2. Check pod restart counts and recent logs:
   - `kubectl logs <pod> -n production --previous`
3. Classify the failure:
   - OOM or memory pressure
   - missing image or pull error
   - config or secret error
   - failing startup probe

## Remediation

1. If the failure started with the last rollout, prefer rollback over prolonged
   speculative debugging.
2. If the failure is a repeat pattern, reuse the previously successful fix.
3. Record the service owner, ETA, and operator command path in the incident
   channel.
