## Description:

Guides agents in generating an ordered set of e-commerce product-detail images from a reference product image using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Merchants and designers use this skill to make product-detail image sets for e-commerce listings from a reference photo, with optional promotional copy and color theme.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the qhkit npm package executes third-party code locally.

Mitigation: Review package provenance and pin a version when reproducibility matters.

Risk: Product images are uploaded to Qinghu and the configured API token could be exposed.

Mitigation: Confirm images may be shared with the service, and store the token in a secure environment variable or protected local configuration.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-detail-page)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with commands and ordered links to generated images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a reference product image and Qinghu API token; generated detail images cannot be edited in place.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
