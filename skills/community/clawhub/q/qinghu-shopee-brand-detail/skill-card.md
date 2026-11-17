## Description:

Queries Shopee brand details for up to 10 brands at a time, including product counts, sales, revenue, and shop counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts compare brand performance across supported marketplaces for a selected date, using product, sales, revenue, and shop statistics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or update Node and qhkit on the local machine.

Mitigation: Review the installation steps and preinstall a reviewed, pinned qhkit version when possible.

Risk: Configuring qhkit may persist an API token with account access.

Mitigation: Use only an account you intend the agent to access, and review local token storage before configuring it.

Risk: Brand-data queries can consume paid credits, including when a service-side call fails.

Mitigation: Check the current estimate and obtain user approval before paid calls; avoid repeated trial-and-error requests.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Brief summaries and tables or exported files for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results identify the marketplace, date, and credits charged.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
