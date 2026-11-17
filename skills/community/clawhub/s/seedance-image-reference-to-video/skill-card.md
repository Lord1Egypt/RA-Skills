## Description:

Creates Seedance reference-image-to-video generation tasks through AI Hive, uploading reference images, tracking generation status, and downloading completed videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, advertising teams, and e-commerce operators use this skill to turn reference images and prompts into AI-generated videos for ads, product showcases, social content, short drama, and related marketing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary marks the skill for review because its activation scope is overly broad.

Mitigation: Install and invoke it only for intentional Seedance reference-image-to-video tasks that require AI Hive generation.

Risk: The security guidance warns that the skill uploads media to AI Hive and creates remote generation tasks.

Mitigation: Avoid sensitive private media unless the user has deliberately chosen to send that content to AI Hive.

Risk: The security guidance warns that downloaded output filenames are not safely constrained.

Mitigation: Use a low-risk output directory and review downloaded files before opening, moving, or publishing them.

Risk: The skill can submit billable generation tasks and poll for completion.

Mitigation: Confirm task count, routing mode, and estimated cost before large or repeated generation runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/seedance-image-reference-to-video)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API key page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands and JSON task output; downloaded video files when generation completes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AI Hive API key, uploads user-provided media to AI Hive, and saves completed generated media to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
