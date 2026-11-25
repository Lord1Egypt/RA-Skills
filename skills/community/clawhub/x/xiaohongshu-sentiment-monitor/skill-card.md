## Description:

Searches public Xiaohongshu posts, comments, and creator profiles by keyword or URL and returns structured data for sentiment, market, and content research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content, brand, and customer support teams use this skill to research public Xiaohongshu posts, review comments, monitor creators, and inform topic, competitor, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and Xiaohongshu links are sent to the third-party Guaikei service when the skill is used.

Mitigation: Use non-sensitive queries and public links, and review the service and the skill’s declared scope before calling it.

Risk: The security scan is incomplete: 13 of 42 components were only partially inspected.

Mitigation: Review the skill’s scope and permissions and complete a fuller scan before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/xiaohongshu-sentiment-monitor)
- [Guaikei service](https://www.guaikei.com)
- [Output contract](artifact/references/contract.md)
- [Command options](artifact/references/options.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [Structured JSON envelope containing Xiaohongshu post, comment, creator, and engagement data; command examples are shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; interaction counts may be returned as strings. An agent can use the JSON to prepare summaries and analysis.]

## Skill Version(s):

1.2.2 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
