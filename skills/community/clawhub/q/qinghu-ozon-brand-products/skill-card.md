## Description:

Queries the last 28 days of Ozon product sales for specified brands, with sorting by sales volume, revenue, or price.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to compare a brand's products by recent sales volume, revenue, or price and identify strong sellers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or update Node.js and qhkit on the user's machine.

Mitigation: Review installation steps first; prefer an externally managed, pinned qhkit version.

Risk: The skill needs a Qinghu API token stored or configured locally.

Mitigation: Obtain the token from the intended Qinghu account and keep it out of chat and logs.

Risk: Data queries are paid and larger responses can cost more credits.

Mitigation: Estimate costs and get consent before paid calls; limit calls and disclose actual credit usage.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-ozon-brand-products)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written findings, with a tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers the latest 28-day sales period; reports actual Qinghu credits used for paid calls.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
