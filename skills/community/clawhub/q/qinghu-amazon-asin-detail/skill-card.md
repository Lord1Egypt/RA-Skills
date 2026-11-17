## Description:

Looks up an Amazon ASIN's product details, category and sales rank, price, reviews, sellers, variants, and operational indicators through Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and analysts use this skill to retrieve details for a single ASIN in a selected marketplace and assess product listings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install or update Node.js and qhkit on the user's machine.

Mitigation: Prefer managed or preinstalled tooling, and review package and runtime installation before proceeding.

Risk: The skill configures a Qinghu API token locally.

Mitigation: Use a securely managed token and review local credential configuration before setup.

Risk: ASIN lookups can consume paid Qinghu credits.

Mitigation: Check the current estimate and obtain user approval before paid calls, especially for larger requests.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-amazon-asin-detail)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise Markdown findings; a tabular file when results contain 10 or more records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the marketplace and credits spent on paid calls; larger results may be returned as local files.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
