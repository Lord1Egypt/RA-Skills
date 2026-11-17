## Description:

VoooAI lets agents relay creative media requests to a backend that generates, executes, monitors, and downloads image, video, music, and multimedia workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkljjkl](https://clawhub.ai/user/hkljjkl)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, designers, studios, businesses, game developers, and educators use this skill to create or edit images, videos, music, storyboards, digital humans, and multi-step creative workflows through VoooAI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose the VOOOAI_ACCESS_KEY or user data if pointed at an untrusted base URL or used with files the user did not intend to share.

Mitigation: Use only a VOOOAI_ACCESS_KEY intended for media-generation work, leave VOOOAI_BASE_URL unset or set it only to a trusted VoooAI HTTPS origin, and upload only user-selected files.

Risk: Direct result downloads from untrusted URLs can pull unwanted or unsafe content into the local workspace.

Mitigation: Prefer downloads from completed VoooAI executions and avoid direct --urls downloads unless the URL source is trusted.

Risk: Generated workflows may consume VoooAI points or credits.

Mitigation: Show estimated points or cost information to the user and wait for confirmation before executing a points-consuming workflow.

Risk: Multimedia generation can be misused for non-consensual impersonation, deepfakes, or political disinformation.

Mitigation: Decline requests for non-consensual facial or voice mimicry, impersonation without consent, and election interference or political disinformation content.

## Reference(s):

- [VoooAI homepage](https://voooai.com)
- [ClawHub skill page](https://clawhub.ai/hkljjkl/skills/voooai)
- [ClawHub publisher profile](https://clawhub.ai/user/hkljjkl)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON responses, downloaded media files, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload user-selected reference files and download generated image, video, or audio results; workflow execution may consume VoooAI points.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
