## Description: <br>
Upload videos and Shorts to YouTube with titles, descriptions, tags, thumbnails, and captions through Boring's MCP connector. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have an agent prepare and publish videos or Shorts to a connected YouTube channel with metadata, thumbnails, and captions. It is intended for workflows where the user trusts the Boring MCP connector with publishing access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector URL contains an embedded credential that grants publishing access to the connected YouTube channel and other connected social accounts. <br>
Mitigation: Treat the connector URL like a password, store it only in trusted agent configuration, and revoke or regenerate it if exposed. <br>
Risk: The security summary notes that the skill can publish publicly through a third-party credential without a required final confirmation step. <br>
Mitigation: Require the agent to show the exact channel, media file, title, description, thumbnail or captions, and visibility for user approval before publishing. <br>


## Reference(s): <br>
- [Boring MCP connector documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [ClawHub skill listing](https://clawhub.ai/snoopyrain/youtube-video-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown guidance with MCP tool-call parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Boring MCP connector URL with embedded authentication; uploaded videos use the visibility behavior documented by the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
