## Description:

Translate raw LinkedIn analytics (impressions, engagement rate, profile visits, follower growth, top posts) into a clear diagnosis : what is working, what is not, and 3 specific actions to take next month. Use when the user has numbers but does not know what they mean or what to do about them. Requires the Taplio MCP, which pulls the user's real analytics and per-post data directly instead of asking them to paste numbers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

External LinkedIn creators and professionals use this skill to understand their Taplio analytics, identify patterns in top- and lower-performing posts, and choose three goal-aligned actions for the next month.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Taplio access can include publishing capabilities beyond the analytics-only workflow, and the skill retrieves profile context, analytics, and post text.

Mitigation: Review Taplio connector permissions and grant only the access appropriate for the user's intended use.

Risk: Analytics recommendations may be misleading if metrics are missing or rough engagement benchmarks are treated as universal targets.

Mitigation: State when metrics are unavailable, frame benchmarks as approximate, and relate conclusions to the user's stated goal and reporting period.

## Reference(s):

- [Taplio MCP](https://mcp.taplio.com)
- [Taplio connector for Claude](https://claude.ai/customize/connectors/id/taplio)
- [ClawHub skill release](https://clawhub.ai/porenes/skills/taplio-linkedin-analytics-interpreter)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown analytics diagnosis with observations and three prioritized actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in retrieved analytics and post data; reports unavailable metrics rather than inventing them.]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
