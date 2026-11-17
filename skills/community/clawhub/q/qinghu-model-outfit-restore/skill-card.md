## Description:

Guides virtual outfit replacement on a model photo while aiming to preserve pose, lighting, and clothing details for ecommerce imagery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce creators and other users provide an authorized model image and garment image to generate a single virtual try-on image with consistent pose and lighting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model and garment images are uploaded to an external service.

Mitigation: Use only images authorized for upload and obtain consent for any identifiable likeness.

Risk: Generation can incur charges or require a subscription.

Mitigation: Show the live credit estimate and confirm with the user before submitting a generation.

Risk: Installing the CLI or changing Node and shell settings modifies the user's environment.

Mitigation: Ask for approval before installing packages or modifying shell profiles; safeguard the API token.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-model-outfit-restore)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Image links]

**Output Format:** [Markdown with command snippets and links to generated images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One outfit per generation; a Qinghu API token and approved credit estimate are required before submission.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
