## Description:

Create OmniHuman audio-to-video tasks and helper tasks for human identification and subject-mask detection through RunAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[runapi-ai](https://clawhub.ai/user/runapi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create RunAPI OmniHuman media-generation tasks, including talking-head video generation from image and audio inputs and helper tasks for human identification or subject-mask detection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit paid RunAPI media-generation tasks.

Mitigation: Confirm the user is comfortable using RunAPI for paid media-generation work before submitting tasks.

Risk: Selected image and audio inputs are shared with RunAPI to perform the requested media task.

Mitigation: Use only user-approved input files and avoid submitting sensitive media unless the user has accepted that sharing.

Risk: The skill depends on the disclosed RunAPI CLI and Homebrew tap.

Mitigation: Confirm the installation requirement is acceptable before installing or using the RunAPI CLI.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/runapi-ai/skills/runapi-omnihuman)
- [RunAPI OmniHuman Model Overview](https://runapi.ai/models/omnihuman.md)
- [RunAPI OmniHuman Homepage](https://runapi.ai/models/omnihuman)
- [RunAPI ByteDance Provider Overview](https://runapi.ai/providers/bytedance.md)
- [RunAPI Model Catalog](https://runapi.ai/models.md)
- [RunAPI OmniHuman SDK](https://github.com/runapi-ai/omnihuman-sdk)
- [OmniHuman 1.5](https://runapi.ai/models/omnihuman/1.5.md)
- [OmniHuman 1.5 Human Identification](https://runapi.ai/models/omnihuman/1.5-human-identification.md)
- [OmniHuman 1.5 Subject Detection](https://runapi.ai/models/omnihuman/1.5-subject-detection.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Code, Markdown]

**Output Format:** [Markdown guidance with shell commands, JSON request and response files, and optional integration code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to submit RunAPI tasks, preserve task and result JSON, and verify downloaded video deliverables.]

## Skill Version(s):

0.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
