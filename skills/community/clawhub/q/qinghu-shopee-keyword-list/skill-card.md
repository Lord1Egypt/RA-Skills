## Description:

Filters Shopee trending keywords by marketplace, category, product location, recent sales, and recommended bid using Qinghu's T+1 keyword data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee merchants and analysts use this skill to find and compare trending search terms across supported marketplaces, filtering by category, 30-day sales, and bid range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install Node and qhkit or change the local PATH and configuration.

Mitigation: Review installation steps first; prefer a pinned, preinstalled qhkit in an isolated environment.

Risk: Authentication setup may change stored tokens or environment configuration.

Mitigation: Supply credentials through a trusted secret flow and confirm the intended account and site before changing configuration.

Risk: Keyword queries and related tool calls may spend Qinghu credits.

Mitigation: Check the current estimate, obtain user approval before paid calls, and report actual charges.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-keyword-list)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise keyword findings with optional tabular export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports marketplace, date, sample size, and actual credits charged; source data updates T+1.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
