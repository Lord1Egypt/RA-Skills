## Description:

Helps agents look up a brand's best-selling Shopee products by site and daily, weekly, or monthly ranking period.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to identify a brand's popular Shopee products for a chosen market and ranking period.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or run unpinned Node and qhkit packages.

Mitigation: Review the installation instructions and install a trusted, pinned qhkit version yourself before use.

Risk: The skill may change qhkit authentication or site configuration.

Mitigation: Provide credentials through normal platform controls and review configuration changes before allowing them.

Risk: Product lookups can consume Qinghu credits.

Mitigation: Check the estimated credit cost and approve paid calls before execution.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-brand-products)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown findings, with a table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes site, ranking period, sample size, and credits spent; source data is not real time.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
