## Description:

Wan 3.0 Prime Reference to Video helps an agent generate reference-guided video clips on RunComfy from prompts plus approved image, video, and audio reference URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[permew](https://clawhub.ai/user/permew)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route reference-to-video requests to RunComfy's Wan 3.0 Prime endpoint, prepare valid inputs, estimate cost-sensitive settings, and invoke the local RunComfy CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on an unpinned third-party RunComfy CLI with account credentials.

Mitigation: Use a trusted, pinned local CLI version, avoid elevated privileges, and verify authentication is limited to the intended RunComfy account.

Risk: Generated video runs can incur charges, especially for high resolution, long duration, or attached reference videos.

Mitigation: Confirm cost-sensitive settings before submission, draft at lower resolution and shorter duration, and trim reference videos before use.

Risk: Prompts and approved reference media URLs are sent to RunComfy for processing.

Mitigation: Submit only media URLs the user supplied or approved, and avoid sensitive or unauthorized reference content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/permew/skills/wan-3-0-prime-reference-to-video)
- [RunComfy](https://www.runcomfy.com)
- [Wan 3.0 Prime Reference to Video model page](https://www.runcomfy.com/models/wan-ai/wan-3.0-prime/reference-to-video?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-3-0-prime-reference-to-video&utm_content=wan-ai-wan-3.0-prime-reference-to-video)
- [RunComfy CLI introduction](https://docs.runcomfy.com/cli/introduction?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-3-0-prime-reference-to-video&utm_content=cli-docs-introduction)
- [RunComfy CLI troubleshooting](https://docs.runcomfy.com/cli/troubleshooting?utm_source=clawhub&utm_medium=skill&utm_campaign=wan-3-0-prime-reference-to-video&utm_content=cli-docs-troubleshooting)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON input examples and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides RunComfy CLI calls that may download generated video files into a user-selected output directory.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
