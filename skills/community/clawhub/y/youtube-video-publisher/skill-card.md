## Description:

Upload videos and Shorts to YouTube. Use when the user says 'upload to YouTube', 'publish YouTube video', 'post a YouTube Short', 'upload video with thumbnail', or wants to upload videos with titles, descriptions, tags, thumbnails, and captions to their YouTube channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and channel operators use this skill to publish YouTube videos or Shorts through a Boring MCP Connector with titles, descriptions, tags, thumbnails, and captions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP Connector URL contains an embedded credential with publishing access to connected social accounts.

Mitigation: Treat the connector URL like a password, revoke or regenerate it if exposed, and connect only accounts intended for agent-mediated publishing.

Risk: Publishing actions can create public uploads or use the wrong channel, metadata, staged media URL, or visibility.

Mitigation: Confirm the YouTube account, video file, title, description, tags, thumbnail, captions, staged media URLs, and visibility before asking an agent to publish.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/youtube-video-publisher)
- [Boring MCP connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [Text, Guidance, Configuration, API calls]

**Output Format:** [Markdown guidance with tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Boring MCP Connector URL with embedded auth token and a connected YouTube account.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
