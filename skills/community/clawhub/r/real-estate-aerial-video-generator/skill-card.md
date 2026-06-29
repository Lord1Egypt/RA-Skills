## Description: <br>
Creates or retrieves cinematic aerial real-estate videos from street addresses through AgentPMT-hosted remote tool calls and returns downloadable MP4 links when footage is ready. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and real-estate professionals use this skill to request or fetch aerial property videos for listings, vacation rentals, neighborhood previews, destination marketing, and location-based client presentations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Property addresses are sent to AgentPMT when generating or fetching aerial videos. <br>
Mitigation: Submit only addresses the user is authorized to use and keep inputs scoped to the minimum needed for the request. <br>
Risk: Generating a new aerial video is documented as a 25-credit action, while fetching existing videos is free. <br>
Mitigation: Confirm user intent before requesting new generation and prefer fetching an existing video when an address or video ID is available. <br>
Risk: Returned MP4 download links expire after 7 days and new footage may take 24 to 48 hours. <br>
Mitigation: Preserve the video ID for follow-up checks and tell users when a video is queued, processing, unavailable, or ready. <br>


## Reference(s): <br>
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/real-estate-aerial-video-generator) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/real-estate-aerial-video-generator) <br>
- [Real Estate Aerial Video Generator Schema](schema.md) <br>
- [AgentPMT Account MCP/REST Setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [What AgentPMT Is](https://clawhub.ai/agentpmt/what-is-agentpmt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON tool-call shapes, status-handling notes, setup links, and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote AgentPMT tool use; completed download links expire after 7 days, new video generation can take 24 to 48 hours, and some addresses may lack aerial coverage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
