## Description:

Queries Shopee's popular products for a specified trending keyword ID and site using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market researchers use the skill to identify popular products associated with a known trending keyword ID across supported Shopee sites and reporting dates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or upgrading Node and qhkit can make persistent changes to the local environment.

Mitigation: Review installation steps, pin the package version, and use an isolated environment before running the skill.

Risk: A Qinghu API token must be configured locally to access the paid data service.

Mitigation: Store the token securely, avoid including it in shared output, and verify that the configured account and site match the intended service.

Risk: Paid data queries consume credits, and failed service calls may still incur charges.

Mitigation: Check the estimated credit cost and obtain user approval before paid calls; avoid repeated speculative retries.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-keyword-products)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown findings and a tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the site, period, sample size and credits charged; source data is not real time.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
