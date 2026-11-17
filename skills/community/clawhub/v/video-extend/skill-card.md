## Description:

Extend or continue an existing video clip on RunComfy via the runcomfy CLI by routing to Google Veo 3-1 extend-video endpoints with a source video and continuation prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, and developers use this skill to extend short video clips or build chained narrative shots with RunComfy's CLI and Google Veo 3-1 video-extension endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing or invoking the RunComfy CLI, and server security guidance notes caution around unpinned npm or npx commands.

Mitigation: Verify the @runcomfy/cli package source before installation and pin a reviewed version where operational policy requires reproducibility.

Risk: The skill uses a RunComfy access token through RUNCOMFY_TOKEN or local CLI login configuration.

Mitigation: Use a token with only the access needed for the task, keep it out of prompts and logs, and store it through the CLI or environment rather than embedding it in commands.

Risk: Video URLs are externally supplied inputs and may contain content that causes the generated continuation to diverge from the user prompt.

Mitigation: Only extend video URLs intentionally provided for the task and review generated clips for unexpected motion, identity drift, or prompt divergence.

## Reference(s):

- [RunComfy](https://www.runcomfy.com)
- [Veo 3-1 Extend Video](https://www.runcomfy.com/models/google-deepmind/veo-3-1/extend-video?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend)
- [Veo 3-1 Fast Extend Video](https://www.runcomfy.com/models/google-deepmind/veo-3-1/fast/extend-video?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend)
- [Veo 3 Collection](https://www.runcomfy.com/models/collections/veo-3?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend)
- [RunComfy CLI Introduction](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend)
- [RunComfy CLI Troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=video-extend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON CLI input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to select a RunComfy Veo 3-1 extend endpoint, prepare prompt and video URL inputs, run the CLI, and interpret common exit codes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
