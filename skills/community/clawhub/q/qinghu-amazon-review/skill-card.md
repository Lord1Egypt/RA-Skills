## Description:

Queries reviews for a specified Amazon ASIN by star rating and review type, returning titles, text, ratings, and review dates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and researchers use this skill to retrieve Amazon product reviews for an ASIN and examine negative feedback and customer concerns by rating and review type.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-led installation can change local tooling and execute unpinned dependencies.

Mitigation: Set up Node and qhkit yourself before use; avoid unpinned npx or @latest execution in sensitive environments.

Risk: Configuring an API token can expose credentials or change local configuration.

Mitigation: Configure the Qinghu token yourself and review local configuration before granting the agent access.

Risk: Review queries consume paid Qinghu credits, with costs varying by result volume.

Mitigation: Check the estimated credit cost and approve paid calls before requesting large batches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-amazon-review)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise review summary with a tabular file for larger result sets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the marketplace, sample size, and credits consumed when applicable.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
