## Description:

Queries Shopee category rankings to identify top-selling and fast-growing subcategories across daily, weekly, or monthly periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market analysts use this skill to compare hot-selling or rising subcategories by marketplace, category, and reporting period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or upgrade qhkit and Node tooling on the user's machine.

Mitigation: Review installation before use; prefer a pre-provisioned qhkit installation with a pinned version.

Risk: Configuring Qinghu API credentials may persist secrets locally.

Mitigation: Provide credentials through the platform's secret mechanism when possible and review local configuration before storing tokens.

## Reference(s):

- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-category-rank)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown findings; optional table file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the Shopee marketplace, reporting period, and sample size; paid queries consume Qinghu credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
