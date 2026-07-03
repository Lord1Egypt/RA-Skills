## Description: <br>
YouTube Channel Management uploads File Manager videos, updates video metadata, privacy, localizations, thumbnails, captions, playlists, playlist items, channel sections, channel branding, watermarks, and discovers YouTube categories and capabilities through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to manage a connected YouTube channel through AgentPMT remote tool calls, including uploads, metadata updates, playlists, captions, thumbnails, branding, watermarks, and capability discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish, schedule, update, or delete YouTube content, so incorrect parameters could affect public channel content. <br>
Mitigation: Require explicit confirmation of resource IDs and intended privacy, publish, notification, and deletion settings before executing high-impact actions. <br>
Risk: Upload, thumbnail, caption, and watermark actions depend on File Manager file IDs and the connected YouTube account. <br>
Mitigation: Verify the intended file IDs, account, and channel before invoking upload-related actions. <br>
Risk: Some YouTube Studio-only surfaces are not available through the public API. <br>
Mitigation: Check live schema or capabilities before production use and avoid promising unsupported changes such as cards, end screens, or custom in-video linked-video elements. <br>


## Reference(s): <br>
- [YouTube Channel Management Schema](artifact/schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/youtube-channel-management) <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/youtube-api) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, API Calls, Configuration] <br>
**Output Format:** [Markdown instructions with JSON tool-call examples and schema tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT tool calls require connected account setup and File Manager file IDs for upload-related actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
