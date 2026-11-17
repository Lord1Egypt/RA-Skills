## Description:

Queries Shopee shop bestseller and rising-shop rankings by category, marketplace, and daily, weekly, or monthly period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Marketplace researchers and sellers use this skill to compare leading and fast-growing Shopee shops within a category and marketplace over daily, weekly, or monthly periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions can install or update unpinned Node/npm tooling and qhkit.

Mitigation: Review installation steps and prefer a preinstalled, pinned qhkit version before running the skill.

Risk: The skill may store an access token and persistently change qhkit configuration.

Mitigation: Approve credential setup and configuration changes explicitly; avoid sharing the token in responses.

Risk: Ranking queries may spend paid credits, including some failed calls.

Mitigation: Show the intended tool, purpose, and estimated credits, and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-rank)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown with ranking summaries, tables, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranking results depend on the selected marketplace, category, period, and available qhkit data.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
