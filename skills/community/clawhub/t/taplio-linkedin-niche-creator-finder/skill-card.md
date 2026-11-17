## Description:

Identify the top LinkedIn creators in a given niche, with their angle, format mix, posting frequency, and what makes their content work. Returns a ranked list with concrete observations the user can steal. Requires the Taplio MCP, which grounds the list in real high-performing posts pulled from the live LinkedIn inspiration index and the user's own niche and keywords. Use when the user is starting on LinkedIn, exploring a new niche, or looking for inspiration to model their content on.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover LinkedIn creators relevant to a niche and target audience. It summarizes creator angles, content formats, estimated cadence, and practical ideas to adapt, using Taplio inspiration results when the Taplio MCP is connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User profile settings and niche keywords are sent to Taplio to inform searches, so confidential search terms may be exposed to the connected service.

Mitigation: Avoid including confidential or sensitive information in profile settings and search terms.

Risk: Creator cadence, follower tier, and profile URLs may be estimated or unavailable from search results.

Mitigation: Treat estimated statistics and unresolved profile details as unverified, and confirm them in Taplio before relying on them.

## Reference(s):

- [Taplio MCP server](https://mcp.taplio.com)
- [Taplio Claude connector setup](https://claude.ai/customize/connectors/id/taplio)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown ranked list with creator observations and usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Typically lists 8–10 creators; may label unverified profile details and estimated statistics for verification.]

## Skill Version(s):

1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
