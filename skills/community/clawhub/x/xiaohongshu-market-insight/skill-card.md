## Description:

Analyzes public Xiaohongshu posts, creator activity, and comments to surface category trends, market opportunities, and risks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, brand and operations teams, and market analysts use this skill to search public Xiaohongshu notes, review creator activity and comments, and identify content and category trends for research and planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and links are sent to the GUAIKEI third-party service.

Mitigation: Use public data only and avoid sending sensitive search terms or links; review the provider's terms before use.

Risk: The security scan had partial coverage and its tool-misuse analyzer was degraded, leaving some behavior unverified.

Mitigation: Review the source before deployment when fuller assurance is needed, and avoid using the skill with sensitive workflows.

## Reference(s):

- [GUAIKEI service](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/xiaohongshu-market-insight)
- [Command and output contract](references/contract.md)
- [Command options](references/options.md)
- [Natural language routing guide](references/routing.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelopes containing public note, creator, and comment data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One result stream per command; an agent can summarize trends from the returned data.]

## Skill Version(s):

1.2.2 (source: frontmatter, package.json, changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
