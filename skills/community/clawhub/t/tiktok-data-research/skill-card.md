## Description:

Retrieves public TikTok search results, creator posts, and video comments as structured data for content research, competitor monitoring, and audience analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

TikTok creators, marketing teams, and researchers use the skill to retrieve public videos, creator posts, and comments for topic research, competitor reviews, and audience analysis. An agent can summarize the returned data for the user's requested research task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some components were only partially inspected, so scan coverage is incomplete.

Mitigation: Review the partially inspected components before installing, since the scan does not establish their safety.

Risk: Search keywords and TikTok links are sent to guaikei.com to retrieve data.

Mitigation: Use public TikTok queries and confirm that sending the requested information to this service is acceptable.

## Reference(s):

- [Official service and support](https://www.guaikei.com)
- [Command options](artifact/references/options.md)
- [Release notes](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis]

**Output Format:** [Structured JSON results with agent-written summaries when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the public TikTok data available for the requested keywords, accounts, or videos.]

## Skill Version(s):

1.1.2 (source: SKILL.md frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
