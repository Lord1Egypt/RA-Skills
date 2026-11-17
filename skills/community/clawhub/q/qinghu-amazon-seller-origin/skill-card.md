## Description:

Analyzes the distribution of Amazon sellers by country or region within a selected product category, including product counts and sales shares.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and market analysts use this skill to compare sellers' countries of origin in a selected marketplace and category, including whether Chinese or local sellers dominate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs local installation and execution of third-party qhkit, including potentially unpinned upgrades.

Mitigation: Use a trusted, preinstalled or platform-managed qhkit where possible; review the package and approve local installation or upgrades before execution.

Risk: Seller-origin queries and category lookups may consume paid Qinghu credits.

Mitigation: Confirm the marketplace and category, check estimated credits, and obtain user approval before paid calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-seller-origin)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise written analysis, with a table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports marketplace, period, sample size and credits consumed when applicable.]

## Skill Version(s):

0.1.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
