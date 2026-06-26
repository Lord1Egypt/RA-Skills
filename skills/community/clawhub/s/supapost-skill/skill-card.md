## Description: <br>
Generate AI images and video, build TikTok slideshows, manage AI influencers, and schedule posts to TikTok / Instagram / YouTube / X through the Supapost MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supapost-dev](https://clawhub.ai/user/supapost-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to generate social media assets, manage AI influencer identities, and schedule or publish content through connected Supapost social accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduling, publishing, or account-specific changes can affect connected social media accounts. <br>
Mitigation: Before approval, verify the platform, social account, media, caption or title, timing, and whether the action can be reversed. <br>
Risk: Supapost access requires a sensitive API credential. <br>
Mitigation: Keep SUPAPOST_API_KEY out of logs, files, prompts, and tool arguments; configure it only through the MCP environment or approved client settings. <br>
Risk: Delete actions can remove projects, influencers, scheduled posts, or assets. <br>
Mitigation: Confirm destructive actions with the user and resolve named resources to IDs before calling delete tools. <br>


## Reference(s): <br>
- [ClawHub Supapost Skill](https://clawhub.ai/supapost-dev/supapost-skill) <br>
- [Supapost OpenClaw Developer Docs](https://supapost.so/developers/openclaw) <br>
- [Supapost MCP Documentation](https://supapost.so/developers/mcp) <br>
- [Supapost MCP Endpoint](https://mcp.supapost.so) <br>
- [Supapost API Keys](https://supapost.so/settings/developer) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with command snippets, JSON configuration examples, and MCP tool call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a SUPAPOST_API_KEY credential and the Supapost MCP endpoint; some actions affect connected social accounts.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
