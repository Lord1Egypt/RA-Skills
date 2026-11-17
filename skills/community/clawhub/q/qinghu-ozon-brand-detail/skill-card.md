## Description:

Queries Qinghu's Ozon brand sales data for up to 10 brand names at a time and helps compare the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to look up and compare Ozon brand sales details by brand name through Qinghu's paid data service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid data calls can consume more Qinghu credits as result counts grow, including on some failed requests.

Mitigation: Check the current estimate, explain variable charges, and obtain user approval before the first paid call; avoid repeated trial-and-error requests.

Risk: The skill may install or update local Node/npm tooling and requires a Qinghu API token.

Mitigation: Use a pinned or preinstalled qhkit version in controlled environments and handle the token as a secret.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-brand-detail)
- [Qinghu qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration guidance]

**Output Format:** [Concise Markdown analysis with optional tabular export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries up to 10 brands at a time; results should identify the Ozon site, period, and sample size.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
