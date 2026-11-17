## Description:

Queries up to 30 days of daily Shopee keyword sales, revenue, and search-interest trends by keyword ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce sellers and analysts use this skill to review daily Shopee keyword trends and assess recent demand in supported marketplaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Qinghu API calls may incur credits, including on some failed requests.

Mitigation: Check the estimated charge and obtain approval before paid calls; report the actual credits used.

Risk: The skill may install or upgrade Node.js and qhkit or change local PATH settings.

Mitigation: Prefer a preinstalled, reviewed qhkit version; require explicit approval before installations, automatic upgrades, or profile and PATH changes.

Risk: A Qinghu access token may be stored locally during configuration.

Mitigation: Ask before configuring a token, keep it out of responses, and use only trusted local credential storage.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-keyword-trend)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Narrative trend summary with optional table file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Daily metrics for up to 30 days; results depend on a valid keyword ID, selected Shopee site, and available Qinghu data.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
