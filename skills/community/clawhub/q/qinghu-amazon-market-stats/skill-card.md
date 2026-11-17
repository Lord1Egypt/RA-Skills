## Description:

Analyzes an Amazon category node's market size, competitive concentration, new-product performance, and price and sales gaps using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and market researchers use this skill to assess whether an identified category is worth entering, how concentrated its leading listings are, and whether new products gain traction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating the required command-line package may change local tooling or account configuration.

Mitigation: Preinstall a vetted qhkit version and review any installation or configuration changes before use.

Risk: API credentials are required, and paid queries can consume Qinghu credits, especially for large results.

Mitigation: Provide credentials through a secure secret flow; check the current estimate and obtain approval before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-amazon-market-stats)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown analysis; a tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the marketplace, period, sample size, and credits spent; results depend on the selected category node.]

## Skill Version(s):

0.1.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
