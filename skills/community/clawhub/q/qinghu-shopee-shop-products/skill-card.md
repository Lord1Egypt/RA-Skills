## Description:

Retrieves a Shopee shop's popular products by shop ID and sorts them by sales, revenue, listing date, price, or lifetime sales.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market analysts use this skill to identify a shop's best-selling or newly listed products across supported Shopee sites and compare product rankings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Host setup may install or upgrade unpinned Node and qhkit tooling.

Mitigation: Review host changes and prefer a preinstalled, pinned qhkit version.

Risk: Credential setup may change the host's Qinghu API token or environment settings.

Mitigation: Provide credentials through normal secret management and review configuration changes before applying them.

Risk: Product lookups can consume paid Qinghu credits.

Mitigation: Check the current estimate and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-products)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary with product rankings; table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Shopee site, reporting period, sample size, and credits charged for paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
