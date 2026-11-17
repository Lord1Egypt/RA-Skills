## Description:

Guides agents through uploading and managing videos, captions, playlists, and channel settings on a connected YouTube account through AgentPMT.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Channel managers and developers use this skill to guide an agent in uploading videos and maintaining video metadata, captions, playlists, and channel branding for an AgentPMT-connected YouTube channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public uploads, privacy changes, and subscriber notifications can expose content or alert an audience unintentionally.

Mitigation: Require manual confirmation before public uploads, privacy changes, or subscriber notifications.

Risk: Deleting videos, captions, playlists, or channel sections and changing branding can have high-impact effects without clear rollback guidance.

Mitigation: Require manual confirmation for branding changes and every delete or remove action; review the target before proceeding.

Risk: Unpinned installation examples may retrieve a different skill version.

Mitigation: Prefer OpenClaw installation routes or version-pinned setup commands over floating npx examples.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/agentpmt/skills/youtube-channel-management)
- [AgentPMT YouTube Channel Management marketplace page](https://www.agentpmt.com/marketplace/youtube-api)
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)
- [YouTube Channel Management schema](artifact/schema.md)

## Skill Output:

**Output Type(s):** [Guidance, JSON tool-call arguments]

**Output Format:** [Text with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions require a connected account; media uploads use File Manager file IDs.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
