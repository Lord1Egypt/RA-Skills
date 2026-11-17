## Description:

Turns long videos into captioned vertical clips and prepares social posts through WoopSocial after the user approves them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT

## Use Case:

Social media creators use the skill to select standalone moments from long videos, render vertical short clips, and prepare posts for their accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API-key fallback can expose a credential when a key is placed in a URL.

Mitigation: Prefer OAuth; keep any API key private and out of shared chats and committed files.

Risk: Uploads may be sent to an unintended destination.

Mitigation: Use the original upload-session response and restrict upload destinations to HTTPS on documented WoopSocial storage hosts.

Risk: Transcribing private recordings through a hosted service sends audio to that service.

Mitigation: Choose local transcription for private recordings.

Risk: A post could be published with the wrong account, content, or schedule.

Mitigation: Review every posting plan and approve it before publishing.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/social-media-skills/skills/video-to-shorts-skill)
- [Clip selection rubric](references/clip-rubric.md)
- [Shorts specifications](references/shorts-specs.md)
- [WoopSocial posting guide](references/woopsocial.md)
- [WoopSocial documentation](https://docs.woopsocial.com/llms.txt)
- [WoopSocial MCP tools reference](https://docs.woopsocial.com/mcp/tools-reference)

## Skill Output:

**Output Type(s):** [Video files, Text, API calls]

**Output Format:** [MP4 clips, JSON manifests, transcripts, titles, and captions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Vertical 9:16 clips with captions; posting requires user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
