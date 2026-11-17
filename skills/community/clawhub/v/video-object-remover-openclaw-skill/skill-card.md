## Description:

Remove an unwanted person, object, logo, or distraction from a video with Video Object Remover.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luffy2023100](https://clawhub.ai/user/luffy2023100)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users use this skill to remove one unwanted visual element from a video they own or are authorized to edit. The workflow submits the video to Video Object Remover, presents the selected mask for review, and proceeds with erasing only after explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos are uploaded to the Video Object Remover service.

Mitigation: Install and use the skill only after confirming the service is trusted for the intended video content.

Risk: The API key can use account credits and access processed jobs.

Mitigation: Keep VIDEO_OBJECT_REMOVER_API_KEY private and avoid printing it, writing it to logs, or including it in URLs.

Risk: Object removal can alter the meaning or rights context of a video.

Mitigation: Use the skill only for videos the user owns or is authorized to edit, and require mask review plus explicit confirmation before final erasing.

## Reference(s):

- [Server-resolved source repository](https://github.com/luffy2023100/video-object-remover-openclaw-skill)
- [Video Object Remover OpenClaw setup guide](https://videoobjectremover.com/blog/remove-objects-from-video-with-openclaw)
- [Video Object Remover website](https://videoobjectremover.com)
- [ClawHub skill page](https://clawhub.ai/luffy2023100/skills/video-object-remover-openclaw-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline shell commands and API request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VIDEO_OBJECT_REMOVER_API_KEY and explicit user confirmation before final erase.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
