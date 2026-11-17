## Description:

Queries monthly, quarterly, or yearly aggregate trends for Shopee products over up to 720 days using Qinghu data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Shopee sellers and analysts use this skill to examine a product's longer-term sales trajectory across monthly, quarterly, or yearly periods at supported sites.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup or upgrades may change local software and environment settings.

Mitigation: Require explicit approval before installing or upgrading tools or changing PATH or profiles; prefer a preinstalled, pinned qhkit version.

Risk: Credential configuration may expose or persist a Qinghu API token.

Mitigation: Require approval before configuring credentials and keep the token out of shared output.

Risk: Qinghu data calls can incur charges.

Mitigation: Explain estimated credits and obtain authorization before paid calls; report actual credits used.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-shopee-product-trend)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Concise trend analysis in Markdown; tabular file for larger results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes the queried site and period, with actual Qinghu credits reported after paid calls.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
