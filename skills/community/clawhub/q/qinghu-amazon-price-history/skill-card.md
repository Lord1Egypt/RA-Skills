## Description:

Guides an agent in retrieving and interpreting historical Amazon product metrics for a single ASIN, including prices, BSR, reviews, seller counts, Buy Box, and FBA fees, but not sales volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and analysts use this skill to examine a single product's historical pricing, rank, customer feedback, and seller competition for research and monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to install an unpinned npm package and make persistent Node, PATH, or API-token configuration changes without clear approval boundaries.

Mitigation: Require explicit approval for installation and persistent setup, pin the qhkit version where possible, and review credential configuration before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-amazon-price-history)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise narrative with supporting metrics; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports marketplace, period, sample size, and credits consumed when applicable; does not provide sales volume.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
