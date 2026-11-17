## Description:

Video Edit — Pro Pack on RunComfy helps an agent transform existing video clips with RunComfy-hosted models for restyling, background swaps, outfit swaps, motion transfer, color grading, and related edit tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and automation agents use this skill to route an existing video plus an edit instruction to an appropriate RunComfy video-edit endpoint and prepare the matching CLI invocation. It is useful for identity-stable edits such as restyling, background replacement, outfit changes, motion transfer, color grading, and product packaging swaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source video URLs, prompts, and optional reference images are sent to RunComfy for third-party media processing.

Mitigation: Use the skill only with videos and reference assets that are approved for upload to RunComfy.

Risk: RunComfy authentication tokens can grant access to the user's account or processing quota.

Mitigation: Protect RUNCOMFY_TOKEN and prefer a pinned or locally scoped @runcomfy/cli installation where possible.

Risk: The workflow depends on trust in the local RunComfy CLI installation.

Mitigation: Install the CLI from a trusted source, keep it scoped to the intended environment, and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/video-edit-runcomfy)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy)
- [RunComfy video edit models](https://www.runcomfy.com/models?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=video-edit-runcomfy)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with RunComfy CLI commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that upload source video URLs, prompts, and optional reference images to RunComfy for processing.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
