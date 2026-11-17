## Description:

Creates or retrieves cinematic aerial property videos from street addresses through AgentPMT-hosted tool calls and returns downloadable MP4 links when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and business users use this skill to request, check, and retrieve aerial videos for real estate listings, vacation rentals, neighborhood previews, destination marketing, and property presentations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Property addresses are sent to AgentPMT's authenticated MCP or REST service.

Mitigation: Use the skill only when sharing the address with AgentPMT is acceptable and keep tool inputs limited to the location data needed for the request.

Risk: Setup and live-instruction guidance can depend on mutable remote content or unpinned installers.

Mitigation: Use pinned or reviewed installation sources, refresh schema details before production use, and keep local security and credential-handling rules authoritative.

## Reference(s):

- [Real Estate Aerial Video Generator Schema](artifact/schema.md)
- [AgentPMT Marketplace Page](https://www.agentpmt.com/marketplace/real-estate-aerial-video-generator)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/real-estate-aerial-video-generator)
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with JSON tool-call examples and downloadable MP4 links when videos are ready]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Completed video download links expire after 7 days; new requests can take 24 to 48 hours and may be unavailable for some addresses.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
