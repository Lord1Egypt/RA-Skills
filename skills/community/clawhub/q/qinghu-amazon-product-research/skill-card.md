## Description:

Filters Amazon products by marketplace, keyword, category, price, sales, rank, ratings, profit margin, and other commercial criteria using Qinghu AI data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and product researchers use this skill to shortlist products and assess opportunities across supported marketplaces using commercial filters and Qinghu AI product data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating unpinned tools may introduce unreviewed code.

Mitigation: Use a controlled setup with reviewed, preinstalled versions of Node and qhkit; avoid automatic npx or latest upgrades.

Risk: The external data service requires an API token that may be persisted in local configuration.

Mitigation: Decide how to store the token before use and limit access to the configuration or environment where it is kept.

Risk: Queries use a paid external service and can consume credits.

Mitigation: Check the current estimate and obtain user consent before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-product-research)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Files]

**Output Format:** [Concise written findings with supporting product data and a table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings identify the marketplace, time period, sample size, and credits charged when applicable.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
