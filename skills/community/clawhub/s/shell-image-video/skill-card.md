## Description:

RunningHub AI workflow integration for image face swap, Wan2.2 motion transfer, advanced motion transfer, HD dance video, digital human, comparison, and lip-sync workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lygjoey](https://clawhub.ai/user/lygjoey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to select and run RunningHub image and video generation workflows for face swap, motion transfer, dance video generation, digital-human narration, media comparison, and lip-sync tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact includes a plaintext RunningHub API key.

Mitigation: Treat the key as compromised, remove it from the skill, rotate it, and require users to supply RUNNINGHUB_API_KEY from their own environment.

Risk: Face, voice, image, video, and audio inputs may be sent to RunningHub workflows.

Mitigation: Avoid private or sensitive media unless the user has consent and accepts the external processing risk.

Risk: The skill tells agents to run local Node scripts that are not bundled in the submitted artifact.

Mitigation: Review the scripts, dependencies, and target workspace before execution, and run only in an appropriate sandbox.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lygjoey/skills/shell-image-video)
- [ClawHub publisher profile](https://clawhub.ai/user/lygjoey)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents toward RunningHub workflow calls that may return JSON, image URLs, GIFs, or videos through the referenced local scripts.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
