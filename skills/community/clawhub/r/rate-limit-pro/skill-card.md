## Description:

Advanced rate limiting with tiered controls and quota management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add configurable per-user rate limiting, tiered request quotas, usage resets, and request statistics to agent-integrated JavaScript workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Exposed or long-running services can accumulate tracked identities and stale request history in memory.

Mitigation: Add TTL cleanup and a maximum number of tracked identities before relying on the helper in production.

Risk: Unvalidated user identifiers can create unbounded key growth or unexpected rate-limit buckets.

Mitigation: Validate the source and length of userId values before calling the rate limiter.

## Reference(s):

- [Rate Limit Pro on ClawHub](https://clawhub.ai/raghulpasupathi/skills/rate-limit-pro)
- [raghulpasupathi publisher profile](https://clawhub.ai/user/raghulpasupathi)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Markdown with JavaScript and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a JavaScript RateLimiter helper with tier configuration examples and usage guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
