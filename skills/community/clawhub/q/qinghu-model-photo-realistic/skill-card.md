## Description:

Guides agents through Qinghu's portrait-editing workflow to reduce an AI-generated look, restore skin detail, brighten skin tones, and upscale model photos for e-commerce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce creators and other external users can ask an agent to improve the realism and resolution of a single authorized model or portrait image, with a cost estimate before paid processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected portraits are uploaded to Qinghu's external service.

Mitigation: Only submit images the user has authorized for processing, and confirm they are comfortable sharing them with Qinghu.

Risk: Generation may spend Qinghu credits, including for each image submitted separately.

Mitigation: Check the current estimate and available benefits, then obtain user confirmation before paid generation.

Risk: The workflow may install or update qhkit or Node locally.

Mitigation: Review dependency installation commands and sources before allowing local setup or upgrades.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-model-photo-realistic)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Image links]

**Output Format:** [Markdown text with commands and links to processed images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one portrait per request; reports the estimated credits before submission and actual credits after completion.]

## Skill Version(s):

0.1.6 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
