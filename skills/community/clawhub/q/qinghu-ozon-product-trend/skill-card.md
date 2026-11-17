## Description:

Retrieves Ozon product sales trend snapshots by product ID across seven-day, 28-day, monthly, quarterly, and yearly periods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ozon sellers and analysts use this skill to look up a product's sales snapshots by ID and assess changes across reporting periods.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing unpinned external tooling can make persistent changes to the user's environment.

Mitigation: Get explicit confirmation before installing software; prefer a sandbox or a preinstalled, pinned qhkit version.

Risk: The service uses a user-provided API token and paid credits; charges can vary with result size.

Mitigation: Use the token only with a trusted qhkit package, estimate charges first, and obtain explicit confirmation before credit-spending calls.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/autoagc/skills/qinghu-ozon-product-trend)
- [qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise sales-trend summary with optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the reporting period, sample size, and credits spent when a paid query is made.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
