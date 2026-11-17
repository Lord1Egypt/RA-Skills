## Description:

Guides agents in creating a door-opening outfit-change video from a model photo, up to four clothing images, and optional audio using Qinghu AI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and apparel sellers use this skill to turn authorized model and outfit images into a short outfit-change video for fashion marketing or styling content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Model, clothing, and optional audio files are uploaded to Qinghu's service.

Mitigation: Use only media approved for upload to that service and confirm with the user before submitting.

Risk: Video generation consumes Qinghu credits and may require a paid subscription.

Mitigation: Check the live estimate and entitlements, disclose the cost, and obtain confirmation before generating.

Risk: Commercial use of unlicensed media or a model's likeness may infringe rights.

Mitigation: Use owned or licensed clothing and audio assets and obtain the model's permission.

Risk: Installing the qhkit package or Node adds third-party software to the environment.

Mitigation: Review package provenance when supply-chain pinning matters and avoid permanent PATH changes unless intended.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-door-outfit-change)
- [Qinghu qhkit package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with command examples and generated video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides a cost estimate for confirmation before submission and reports the final credit charge after completion.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
