## Description:

Guides agents through creating e-commerce product videos, promotional clips, and storyboards using the qhkit video tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and marketers use this skill to plan and generate short product videos and advertising clips from prompts or images, then retrieve completed video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the qhkit package introduces third-party software into the agent environment.

Mitigation: Confirm that the npm package and iqinghu service are trusted; use a pinned or reviewed package version where required.

Risk: The qhkit API token could be exposed through shared terminals or logs.

Mitigation: Keep the token private and do not paste it into shared terminals or logs.

Risk: Video generation can consume credits and cannot be cancelled once submitted.

Mitigation: Confirm the duration and estimated credits with the user before submitting a generation task.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/autoagc/skills/qinghu-ecom-video)
- [qhkit npm package](https://www.npmjs.com/package/@iqinghu/qhkit)
- [Qinghu AI API keys](https://www.iqinghu.com/workbench/dashboard/api-keys?urlCode=1788417429126)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Storyboard text, Video links]

**Output Format:** [Markdown with inline commands and video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Video generation is asynchronous; the agent polls for completion before providing the video URL.]

## Skill Version(s):

0.1.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
