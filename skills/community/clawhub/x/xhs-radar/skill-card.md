## Description:

This read-only skill retrieves public Xiaohongshu notes, note details, comments, and creator posts as structured JSON for topic research, competitor monitoring, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, social media operators, brands, and creator agencies use it to research public Xiaohongshu notes and comments, find content topics, monitor competitors, and assess creator engagement from returned data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Keywords and Xiaohongshu links sent to the third-party API may disclose research interests or other sensitive context.

Mitigation: Avoid sending sensitive keywords or links, and review the provider's privacy terms before use.

Risk: Request payloads shared with support may expose query or link details.

Mitigation: Remove tokens and sensitive query or link details before sharing request payloads with support.

Risk: The security review is incomplete and does not establish that the skill is safe.

Mitigation: Review the package and its data handling before installation; treat the security assessment as limited evidence.

## Reference(s):

- [Options and parameters](references/options.md)
- [Request routing guide](references/routing.md)
- [Output contract](references/contract.md)
- [Errors and limits](references/errors.md)
- [Troubleshooting](references/troubleshooting.md)
- [Guaikei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON envelope containing note search results, note details, comments, creator posts, or creator engagement metrics.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The envelope distinguishes successful results, empty results, and errors.]

## Skill Version(s):

1.2.3 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
