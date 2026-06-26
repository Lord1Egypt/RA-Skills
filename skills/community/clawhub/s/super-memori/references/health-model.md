# super_memori v4 — Health Model

## Core health checks
These determine `OK/WARN/FAIL`.
1. canonical files readable
2. lexical DB openable
3. FTS query works
4. semantic backend reachable
5. local embedding model readiness
6. queue backlog within threshold
7. lexical freshness age acceptable
8. integrity audit state acceptable for the current host profile

## Quality checks
These are important, but do not alone define system health.
9. orphaned metadata/chunks below threshold
10. duplicate growth under control
11. pending review load acceptable
12. semantic-unbuilt vs stale-vectors vs orphan-vectors state differentiated correctly

## Health statuses
- `OK` — current host profile is healthy for the capabilities it can truthfully activate
- `WARN` — degraded but usable, or semantic-ready features remain unavailable on this host
- `FAIL` — reliable lexical retrieval is not available
- `EQUIPPED` — host snapshot matches the local MAX PROFILE threshold; this is a truth surface, not a health status

## Freshness policy
- lexical stale: canonical files changed after last lexical index time
- semantic stale: canonical files changed after last semantic index time
- warning threshold: 24 hours stale
- critical threshold: 7 days stale
- stale results should be returned with warnings rather than silently hidden

## Freshness fields
- lexical freshness
- semantic freshness
- queue backlog age
- last successful full build
- last successful incremental update

## Rule
If users or agents are likely to make wrong decisions because memory is stale, degraded, semantically unbuilt, structurally drifted, or running on a lower-than-target host profile, health must say so explicitly. Do not collapse semantic-unbuilt host state into fake corruption, do not collapse real orphan drift into a harmless degraded warning, and do not confuse `standard` host shaping with `max` host shaping.
