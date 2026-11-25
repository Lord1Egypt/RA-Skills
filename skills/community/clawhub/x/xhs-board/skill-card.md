## Description:

Provides read-only access to public Xiaohongshu notes, comments, creator posts, and engagement data, returning structured JSON for ranking and analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

External creators, marketers, and content analysts use this skill to search and compare public Xiaohongshu notes, review comments, and examine creator activity and engagement. It returns structured data for ranking, competitor research, and audience analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and links are sent to a third-party API, as noted in the security guidance.

Mitigation: Use public, non-sensitive search terms and links; do not send private account information.

Risk: The security assessment reports medium confidence because parts of the code were only partially inspected and the declared tool scope could not be confirmed.

Mitigation: Review the skill and its requested access before installation or execution.

## Reference(s):

- [ClawHub release](https://clawhub.ai/guaikei/skills/xhs-board)
- [Publisher profile](https://clawhub.ai/user/guaikei)
- [Guaikei API service](https://www.guaikei.com)
- [Changelog](references/changelog.md)
- [Output envelope schema](assets/output_envelope.schema.json)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public note, comment, and creator data; results and request limits depend on the API plan.]

## Skill Version(s):

1.2.3 (source: SKILL.md frontmatter, package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
