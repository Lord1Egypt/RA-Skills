# Symphony SPEC.md Map

Use this file to align implementation work with the upstream contract:
- Upstream source: https://github.com/openai/symphony/blob/main/SPEC.md
- Treat upstream sections as authoritative when behavior is ambiguous.

## Priority Sections to Read First

1. Problem statement and goals (`1`, `2`)
2. Core domain model (`4`)
3. Workflow contract (`5`)
4. Orchestration state machine (`7`)
5. Polling, retries, and reconciliation (`8`)
6. Workspace safety (`9`)
7. Agent runner protocol (`10`)
8. Security and operational safety (`15`)

## Conformance Checklist

- Workflow loader parses YAML front matter + markdown prompt body.
- Strict prompt rendering fails on unknown variables.
- Per-issue workspace keys are deterministic and sanitized.
- Orchestrator keeps one in-memory authoritative state.
- Retry queue uses exponential backoff with bounded maximum delay.
- Active runs stop when issues enter terminal states.
- Startup performs terminal workspace cleanup.
- Logs and status output expose run state, errors, and key metrics.

## Practical Rule

When local behavior conflicts with upstream spec intent, update local implementation to match the spec unless the user explicitly requests a deliberate divergence.
