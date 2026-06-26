# Ingress 502 Errors Runbook

## Use this when

- External traffic starts returning `502`, `503`, or gateway errors
- Load balancer or ingress health checks fail
- The application is up internally but public traffic is degraded

## Triage

1. Confirm whether the failure is at ingress, service, or pod level:
   - `kubectl get ingress -A`
   - `kubectl get svc -n production`
   - `kubectl get endpoints -n production`
2. Check whether healthy backend pods still exist.
3. Review recent ingress or service changes:
   - hostname
   - backend port
   - TLS or certificate changes
4. Check cloud load-balancer or provider health events if the issue is regional.
5. Compare internal service reachability against the public endpoint.

## Remediation

1. Roll back the ingress or service change if the failure started after a deploy.
2. Route traffic to the last known-good backend path.
3. Keep healthy old replicas serving while new backends are investigated.
4. If the provider reports a regional networking issue, shift traffic away from the affected region where possible.
5. Record the failing hostname, affected backend service, and any recent config changes.

## Escalate when

- User-facing traffic is returning gateway errors
- More than one service behind the same ingress path is affected
- The issue overlaps a cloud load-balancer or networking incident
- No healthy fallback path exists
