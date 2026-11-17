## Description:

Trade Qualifier helps agents score and prioritize B2B foreign-trade prospects across six dimensions with A/B/C/D grading.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and sales teams use this skill to qualify customer lists, prioritize high-value B2B prospects, and decide follow-up actions from structured scoring criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Customer lists used for B2B lead qualification may contain sensitive business or personal data.

Mitigation: Review and minimize customer data before use, and avoid including unnecessary personal, credential, or confidential commercial information.

Risk: The release metadata declares a curl requirement even though the written skill instructions do not use it.

Mitigation: Do not grant network, credential, or shell access solely because of the declared curl requirement unless a specific reviewed workflow requires it.

Risk: Qualification scores and follow-up recommendations may be incomplete or inaccurate if source customer data is outdated or biased.

Mitigation: Treat scoring output as decision support and review high-impact outreach decisions against current customer records and applicable compliance requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/trade-qualifier)
- [Publisher Profile](https://clawhub.ai/user/wangm-a3)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown guidance with JSON or table-style scoring results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include six-dimension BOI scores, A/B/C/D grade summaries, recommended follow-up actions, and visual analysis guidance.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
