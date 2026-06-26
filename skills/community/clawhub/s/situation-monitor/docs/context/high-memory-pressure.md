# High Memory Pressure Runbook

## Use this when

- Pods are getting `OOMKilled`
- Deployments enter `CrashLoopBackOff` shortly after a release
- Node memory pressure or eviction warnings appear

## Triage

1. Confirm the failing pod and container:
   - `kubectl get pods -n production`
   - `kubectl describe pod <pod> -n production`
2. Check for `OOMKilled`, `Back-off restarting failed container`, or memory
   pressure events.
3. Compare requests and limits against actual usage:
   - `kubectl top pod <pod> -n production`
4. Inspect the most recent rollout:
   - `kubectl rollout history deployment/<service> -n production`

## Remediation

1. Freeze further deploys for the impacted service.
2. Roll back to the last healthy revision if the spike started immediately after
   a deploy.
3. Increase limits only if the workload is known-good and the problem is bad
   sizing rather than a leak.
4. If a memory leak is suspected, restore the previous image and capture heap or
   profiling artifacts out of band.

## Escalate when

- Checkout or payment traffic is degraded
- More than one service shows the same OOM pattern
- Node memory pressure is affecting unrelated workloads
