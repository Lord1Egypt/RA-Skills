# PMA-Go Delivery

## Lint And Static Checks

- use `.golangci.yml` for shared lint rules
- keep the enabled set reviewable and non-redundant
- fail on real issues, not style noise

## Testing

- default to table-driven tests
- keep tests close to the package they verify
- add integration tests for DB or HTTP behavior when unit tests alone are insufficient
- use coverage as a signal, not as a substitute for meaningful assertions

## Task Runner

Prefer `Taskfile.yml` for:

- lint
- test
- build
- generate
- migrate

Keep task names predictable and aligned with CI.

## Security Patterns

Review:

- input validation
- SSRF risk on outbound HTTP
- constant-time secret comparison
- auth and permission boundaries
- secret redaction in logs

## Pre-Commit Security Checklist

- no hardcoded secrets
- all user input validated
- no unsafe outbound HTTP behavior
- no sensitive error leakage
- no auth regression on changed endpoints

## CI Pipeline

Typical stages:

- format
- lint
- vet and static checks
- test
- build
- security review

## Git Conventions

- use English remote-visible metadata
- use conventional commits
- keep PR summaries and test plans explicit

## Review Focus

Prioritize:

- correctness
- regression risk
- context propagation
- cancellation and resource lifetime
- missing tests around changed behavior
