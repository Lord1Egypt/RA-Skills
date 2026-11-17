## Description:

Looks up 1688 product details by offer ID, including title, price, sales, and supplier information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers, sourcing teams, and developers use this skill to retrieve 1688 product prices, sales, and supplier details from a product ID or link.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install Node/npm tooling and change the host environment.

Mitigation: Review and approve installation first; prefer a platform-managed or pinned qhkit package.

Risk: The skill uses Qinghu account credentials for paid data lookups and may change existing configuration.

Mitigation: Use a scoped token, review configuration changes, and approve the estimated charge before calling the paid tool.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-1688-goods-detail)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Markdown summary with optional tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports credits charged for paid lookups.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
