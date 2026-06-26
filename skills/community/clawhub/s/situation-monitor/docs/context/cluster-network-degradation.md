# Cluster Network Degradation Runbook

## Use this when

- GCP or your cloud status page reports packet loss, latency, or control-plane network trouble
- Services across more than one namespace show timeouts at the same time
- Ingress, service-to-service traffic, or node-to-node communication degrades together

## Triage

1. Confirm whether the incident is regional, zonal, or global:
   - check the cloud provider status page
   - note the impacted region and timestamps
2. Check whether multiple services are failing with the same network symptoms:
   - elevated `503`
   - connection timeout
   - DNS or service discovery failures
3. Inspect cluster health quickly:
   - `kubectl get nodes`
   - `kubectl get pods -A | grep -E 'CrashLoop|Pending|Error'`
4. Check ingress and service events:
   - `kubectl get events -A --sort-by='.lastTimestamp' | tail -40`
5. Confirm whether the issue aligns with a rollout. If not, treat it as shared infrastructure until proven otherwise.

## Remediation

1. Freeze non-essential deploys while network symptoms are active.
2. Shift traffic away from the affected region or zone if you have failover available.
3. Prefer keeping existing healthy replicas in service over risky restart churn.
4. If ingress is affected, move to a known-good traffic path before debugging individual workloads.
5. Record the blast radius, impacted region, and the provider incident link in the incident channel.

## Escalate when

- More than one critical service is degraded
- Checkout, auth, or user-facing APIs are timing out
- The cloud provider status page confirms an active network or control-plane event
- Regional failover is unavailable or incomplete
