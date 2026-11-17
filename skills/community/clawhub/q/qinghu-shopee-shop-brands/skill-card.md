## Description:

Analyzes brands sold by a Shopee shop, including product counts, sales volume, and revenue for a selected date and marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and market analysts use this skill to examine a shop's brand mix by product count, sales volume, and revenue across supported marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrade of unpinned qhkit or Node.js can alter host tooling beyond the scope of a shop query.

Mitigation: Review and preinstall a pinned qhkit version; require approval before installing or upgrading host tools.

Risk: Paid queries may consume credits, including when a service call fails.

Mitigation: Confirm paid calls with the user before execution and report actual credits charged.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-brands)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written analysis; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports marketplace, date, sample size, and credits spent when applicable.]

## Skill Version(s):

0.1.1 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
