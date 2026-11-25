## Description:

Provides read-only access to public Xiaohongshu notes, comments, creator posts, and engagement data, returning structured JSON for topic research, competitor monitoring, creator screening, and sentiment analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and analysts use this skill to research public Xiaohongshu posts, review comment sentiment, monitor competitors, and screen creators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is incomplete, and the skill's tool scope and data disclosures remain unclear.

Mitigation: Clarify the requested tool permissions and what query data is sent to the service, and have the partially inspected executable files fully reviewed before installation.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/guaikei/skills/xhs-engine)
- [Guaikei Xiaohongshu data API](https://www.guaikei.com)
- [Routing guide](references/routing.md)
- [Output contract](references/contract.md)
- [Setup and data handling FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands]

**Output Format:** [Structured JSON in a consistent response envelope]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may be arrays or objects; per-call limits and fees depend on the service plan.]

## Skill Version(s):

1.2.3 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
