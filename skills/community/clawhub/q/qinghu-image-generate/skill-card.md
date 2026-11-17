## Description:

Helps agents generate e-commerce product and promotional images from text prompts or optional reference images using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce creators and marketers use this skill to request product, scene, and promotional images from prompts, with optional reference images for image-to-image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running an external qhkit CLI introduces third-party executable code.

Mitigation: Review the package and prefer a user-scoped, version-reviewed installation over automatic latest-version upgrades in sensitive environments.

Risk: Using the service requires a Qinghu AI API token.

Mitigation: Keep the token private and provide it only through the supported configuration or environment variable.

Risk: Prompts and reference images are sent to Qinghu AI for image generation.

Mitigation: Confirm users are comfortable sharing the provided content with the external service before submitting it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-image-generate)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Text or Markdown with generated image links and credit usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are delivered as links; generation consumes service credits.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
