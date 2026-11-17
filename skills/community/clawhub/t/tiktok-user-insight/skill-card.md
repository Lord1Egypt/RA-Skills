## Description:

Retrieves public TikTok search results, creator posts, and video comments as structured data for audience, trend, and product opportunity analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing and growth teams, market researchers, and product teams can retrieve public TikTok searches, creator posts, and comments, then analyze trends, audience needs, and product opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The service token is required for API access, and requests may incur charges.

Mitigation: Keep GUAIKEI_API_TOKEN private and check the service's pricing before making requests.

Risk: Optional local logs can retain search queries and public profile or comment data.

Mitigation: Keep logging disabled unless needed; restrict access to saved logs and remove them when no longer needed.

Risk: The provider's billing, retention, and data-sourcing claims have not been independently verified.

Mitigation: Review the provider's terms and data handling before sending queries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/why20261/skills/tiktok-user-insight)
- [Guaikei service and token access](https://www.guaikei.com)
- [Command options](references/options.md)
- [Release changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis]

**Output Format:** [Structured JSON containing search results, creator posts, or video comments; the agent can use these data for concise findings or reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public TikTok data; result counts depend on available data and the service plan.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
