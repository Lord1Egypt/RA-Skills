## Description:

Helps users upscale and interpolate short product videos through Qinghu AI while preserving audio synchronization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and merchants use this skill to enhance blurry, low-bitrate product videos with upscaling and frame interpolation. It guides quoting, submitting, and retrieving the processed video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing and running the qhkit npm CLI introduces a third-party software dependency.

Mitigation: Review the package before installation; pin its version or use an isolated environment for tighter supply-chain control.

Risk: The workflow requires an API token and uploads selected video to the Qinghu service.

Mitigation: Provide the token only through the intended configuration and upload only videos you are authorized to share and process.

Risk: Cloud processing can consume paid Qinghu credits, and estimated or reserved credits may differ from final charges.

Mitigation: Review the estimate and obtain user confirmation before submission; report actual credits after completion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-video-upscale-hd)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Text with commands, a processed-video link, and final credit usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video input is limited to 60 seconds; completion and charges depend on the cloud workflow.]

## Skill Version(s):

0.1.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
