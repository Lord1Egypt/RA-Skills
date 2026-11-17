## Description:

VPick Video Creator helps agents produce AI videos on a visual canvas by generating images, video clips, voiceover, music, lip sync, edits, and final exports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to direct an agent through end-to-end AI video production with VPick, including asset generation, audio, lip sync, canvas organization, and export. It is suited for video, short film, storyboard, narration, music, and media-compositing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP URL contains an embedded token that can trigger VPick generation actions.

Mitigation: Treat the MCP URL as a secret, avoid sharing it publicly, and regenerate it in VPick settings if exposure is suspected.

Risk: Prompts and uploaded media are processed by VPick and routed to third-party model providers.

Mitigation: Avoid submitting sensitive or private media unless the user accepts VPick and provider processing for the workflow.

Risk: Video, image, audio, and lip-sync generations consume VPick credits.

Mitigation: Check available credits and generation cost expectations before running large or repeated jobs.

## Reference(s):

- [VPick MCP connection guide](https://vpick-doc.10xboost.org/guide/mcp-connection.html)
- [VPick app](https://vpick.10xboost.org)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/vpick-ai-video-creator)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with inline tool-call and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in cloud-generated media files, generated media URLs, and paid VPick credit usage.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
