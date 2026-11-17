## Description:

Queries popular products from an Ozon shop by name or ID, with optional category, period, and sales, revenue, or price sorting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and market researchers use this skill to identify popular products in a shop and compare sales, revenue, or prices across categories and reporting periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct the agent to install or upgrade Node.js and qhkit on the host without clear approval.

Mitigation: Confirm host software changes first; prefer a preinstalled, reviewed qhkit version.

Risk: Product-data queries may incur Qinghu credits, with charges varying by result count.

Mitigation: Check estimated credits and shop parameters, then obtain approval before paid calls or large batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-shop-products)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written findings with an optional table file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports shop, site, reporting period, sample size, and credits charged when applicable.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
