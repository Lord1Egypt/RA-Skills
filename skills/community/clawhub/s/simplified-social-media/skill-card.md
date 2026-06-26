## Description: <br>
Manage your entire social media from AI, including posting, scheduling, and analytics across Facebook, Instagram, TikTok, YouTube, LinkedIn, Pinterest, Threads, Bluesky, and Google Business. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jacksimplified](https://clawhub.ai/user/jacksimplified) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Social media managers, marketers, and developers use this skill to discover connected social accounts, compose draft or scheduled posts, queue campaigns, and retrieve account or post analytics through Simplified. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can queue, schedule, or publish content to connected social media accounts. <br>
Mitigation: Manually confirm the target accounts, content, media, action type, and timing before any post, schedule, or queue action. <br>
Risk: The skill depends on an API key that can operate connected social accounts. <br>
Mitigation: Use the least-privileged Simplified API key and account scope available, and install the skill only when the publisher and remote MCP service are trusted. <br>
Risk: Ambiguous posting requests may result in unintended public content or timing. <br>
Mitigation: Prefer drafts for unclear requests and ask for confirmation before direct publishing or scheduling. <br>


## Reference(s): <br>
- [Simplified](https://simplified.com) <br>
- [Simplified Social Media MCP Server](https://mcp.simplified.com/social-media/mcp) <br>
- [Simplified API Keys](https://app.simplified.com/settings/api-keys) <br>
- [Analytics Reference Guide](references/ANALYTICS_GUIDE.md) <br>
- [Platform Reference Guide](references/PLATFORM_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration instructions, API calls, Markdown] <br>
**Output Format:** [Markdown with JSON examples and tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces account-selection, post-composition, scheduling, queueing, drafting, and analytics guidance for a remote MCP social media service.] <br>

## Skill Version(s): <br>
1.2.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
