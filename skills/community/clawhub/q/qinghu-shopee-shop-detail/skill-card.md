## Description:

Queries up to 10 Shopee stores by ID for sales, revenue, product counts, and ratings through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Sellers and analysts use this skill to compare Shopee store sales, revenue, listings, and ratings across supported sites for a specified date, with up to 10 store IDs per query.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may install Node and qhkit or change the user's PATH or profile.

Mitigation: Review before use in sensitive environments; prefer a pre-provisioned, pinned qhkit installation.

Risk: Configuring the Qinghu API token grants access to a credential.

Mitigation: Provide the token only intentionally and avoid exposing it in shared output.

Risk: Store queries can consume paid Qinghu credits.

Mitigation: Check the estimated cost and obtain consent before paid calls.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-shop-detail)
- [@iqinghu/qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Files]

**Output Format:** [Markdown summary; table file for 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the site, date, sample size, and credits charged when applicable.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
