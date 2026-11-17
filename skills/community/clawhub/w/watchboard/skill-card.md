## Description:

Query Watchboard intelligence dashboards for structured event data, casualty figures, KPIs, contested claims, and daily digests across trackers covering conflicts, politics, culture, science, and space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[artemiopadilla](https://clawhub.ai/user/artemiopadilla)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve structured Watchboard tracker summaries, KPIs, recent events, search results, RSS fallback data, and briefings when a topic is covered by Watchboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries are sent to watchboard.dev and responses are cached under /tmp/watchboard-cache.

Mitigation: Install only when this data flow is acceptable, avoid elevated privileges, and prefer a private per-user cache with restrictive permissions on shared systems.

Risk: The shared temporary cache creates a local file-safety and cache-poisoning risk.

Mitigation: Review cache handling before deployment and isolate or harden the cache location when multiple users can access the same system.

## Reference(s):

- [Watchboard](https://watchboard.dev)
- [Watchboard API v1](https://watchboard.dev/api/v1/)
- [ClawHub Skill Release](https://clawhub.ai/artemiopadilla/skills/watchboard)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Watchboard API responses and caches fetched data locally for 1 hour.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
