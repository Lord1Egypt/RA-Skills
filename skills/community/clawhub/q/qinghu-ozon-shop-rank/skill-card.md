## Description:

Helps users find top-selling Ozon shops by period, category, shop type, sales, ratings, and other filters using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and market analysts use this skill to identify leading Ozon shops and compare competitors across categories and sales ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic installation or upgrade of unpinned Node/npm tooling can change the local environment.

Mitigation: Preinstall a reviewed, pinned qhkit version and approve tooling changes before execution.

Risk: Configuring or using an API token can expose credentials if handled insecurely.

Mitigation: Supply the token through a secure secret mechanism and avoid sharing it in chat or logs.

Risk: Paid data calls can consume Qinghu credits, especially for large result sets.

Mitigation: Estimate charges and obtain user consent before paid calls or large downloads.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ozon-shop-rank)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written findings; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results should state the platform, period, sample size, and credits spent.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
