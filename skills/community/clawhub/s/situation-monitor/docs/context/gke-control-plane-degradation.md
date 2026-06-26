# GKE Control Plane Degradation Runbook

## Use this when

- Google Kubernetes Engine reports cluster control-plane issues
- `kubectl` commands become slow, fail, or return intermittent API errors
- Scheduling, rollouts, or autoscaling stop behaving normally

## Triage

1. Confirm the scope from the provider incident:
   - control plane only
   - node creation / autoscaling
   - cluster upgrades / API availability
2. Check whether the existing workloads are still serving traffic:
   - do not assume a control-plane issue means the data plane is fully down
3. Validate current node and workload state:
   - `kubectl get nodes`
   - `kubectl get deploy -n production`
   - `kubectl get pods -n production`
4. Check whether recent changes depend on new scheduling or rollout activity.
5. If the API server is flaky, avoid repeated write operations that can worsen operator confusion.

## Remediation

1. Freeze deploys, upgrades, and manual scaling while the control plane is degraded.
2. Keep healthy existing replicas running; avoid unnecessary pod churn.
3. Use regional failover or a standby cluster if the workload cannot tolerate control-plane instability.
4. Delay non-essential reconciliations until the provider marks the control plane healthy.
5. Capture the provider incident URL, impacted cluster name, and the last successful operator action.

## Escalate when

- Critical production changes are blocked by control-plane availability
- Autoscaling or recovery depends on new pod scheduling
- API-server instability affects more than one cluster
- The provider incident remains unresolved beyond the agreed response window
