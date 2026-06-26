## Description: <br>
Advanced rate limiting with tiered controls and quota management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raghulpasupathi](https://clawhub.ai/user/raghulpasupathi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers use this skill to add an in-memory JavaScript rate limiter with tier-based request quotas, rolling time windows, user resets, and basic usage statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage counters are stored in memory, so limits do not persist across process restarts and are not coordinated across multiple servers. <br>
Mitigation: Use shared storage and coordination when applying this pattern in production across restarts or multiple server instances. <br>


## Reference(s): <br>
- [Rate Limit Pro on ClawHub](https://clawhub.ai/raghulpasupathi/rate-limit-pro) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Configuration, Guidance] <br>
**Output Format:** [JavaScript and JSON examples in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exports a RateLimiter class with configurable tiers and in-memory request tracking.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
