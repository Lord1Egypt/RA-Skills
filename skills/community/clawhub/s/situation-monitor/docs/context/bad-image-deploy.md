# Bad Image Deploy Runbook

## Use this when

- Pods show `ImagePullBackOff` or `ErrImagePull`
- A rollout hangs after a new image tag is deployed
- Old replicas are still serving while new ones fail

## Triage

1. Confirm the failing image reference:
   - `kubectl describe pod <pod> -n production`
2. Check rollout state:
   - `kubectl rollout status deployment/<service> -n production`
3. Verify whether the image tag exists in the registry.
4. Confirm whether old healthy replicas are still available.

## Remediation

1. Roll back the deployment:
   - `kubectl rollout undo deployment/<service> -n production`
2. If rollback is not possible, patch the deployment to a known-good image tag.
3. Pause merges for the affected service until the image path is corrected.
4. Capture the bad tag and CI job reference for postmortem follow-up.

## Escalate when

- The deployment affects login, user, or checkout paths
- The bad image tag reached multiple regions or environments
