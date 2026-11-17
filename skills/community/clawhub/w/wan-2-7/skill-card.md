## Description:

Generate text-to-video with Wan 2.7 on RunComfy, including guidance for multi-reference conditioning, audio-driven lip-sync, prompt expansion, duration, resolution, aspect ratio, and routing to related video models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate short Wan 2.7 text-to-video clips through RunComfy, including lip-synced videos from supplied audio and prompt-controlled commercial video variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run an unpinned global RunComfy CLI that handles account tokens and media prompts.

Mitigation: Review the CLI before installing, prefer a pinned or local install, and use a scoped token that can be rotated.

Risk: Prompts, private media URLs, and generated outputs are processed by the RunComfy service.

Mitigation: Avoid sending sensitive prompts, private media URLs, or long-lived credentials unless the service and package provenance are trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/wan-2-7)
- [RunComfy](https://www.runcomfy.com)
- [RunComfy CLI documentation](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-2-7)
- [Wan 2.7 text-to-video model page](https://www.runcomfy.com/models/wan-ai/wan-2-7/text-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-2-7)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-2-7)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and JSON input examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to call the RunComfy CLI and save generated video files to a user-selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
