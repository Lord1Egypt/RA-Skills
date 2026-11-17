## Description:

Edits talking-head videos by transcribing speech, planning cuts for approval, rendering captions and chapters, and optionally publishing after confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT

## Use Case:

Creators, educators, podcasters, and social media teams use this skill to prepare a talking-head edit with captions and chapters, then optionally publish the approved video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured API keys can cause recordings to be uploaded automatically for cloud transcription.

Mitigation: For private recordings, explicitly choose local transcription or provide an existing transcript; select a cloud provider deliberately before sending audio.

Risk: The fallback WoopSocial connection method puts a publishing credential in a URL.

Mitigation: Connect through OAuth and avoid API keys in URLs.

Risk: An edit could remove footage that should be protected, including material near the ending.

Mitigation: Review the cut list and rendered footage, including protected sections and the ending, before approving publication.

## Reference(s):

- [Editing rules](references/editing-rules.md)
- [WoopSocial setup and publishing guide](references/woopsocial.md)
- [WoopSocial documentation index](https://docs.woopsocial.com/llms.txt)
- [WoopSocial MCP tools reference](https://docs.woopsocial.com/mcp/tools-reference)

## Skill Output:

**Output Type(s):** [Video files, Subtitle files, Text, Markdown, JSON]

**Output Format:** [Edited MP4 video, SRT captions, chapter text, Markdown edit report, and JSON manifest]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an edit plan for review before rendering; publishing requires user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
