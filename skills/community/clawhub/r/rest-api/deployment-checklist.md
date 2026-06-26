# Deployment Checklist - REST API

Use this checklist before each production release.

## Contract and Compatibility

- [ ] OpenAPI spec updated and validated.
- [ ] Breaking changes documented with migration path.
- [ ] Deprecations include timeline and communication plan.

## Security

- [ ] Auth and authorization checks verified on critical endpoints.
- [ ] Secrets loaded from secure source, not hardcoded.
- [ ] Rate limits and payload limits configured.

## Data and Migrations

- [ ] Migration plan reviewed (expand, migrate, contract).
- [ ] Rollback path tested.
- [ ] Data integrity checks prepared.

## Quality

- [ ] Integration and end-to-end tests passing.
- [ ] Performance smoke test completed.
- [ ] Error responses and logs verified.

## Operations

- [ ] Dashboards include latency, error rate, and saturation.
- [ ] Alerts enabled with owner and on-call route.
- [ ] Incident runbook linked and current.

## Release

- [ ] Staged rollout or canary plan defined.
- [ ] Post-deploy verification commands prepared.
- [ ] Explicit go/no-go decision recorded.
