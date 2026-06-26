## Description: <br>
Socialcannon helps agents publish, schedule, analyze, and manage social media content across Twitter/X, Facebook, Instagram, LinkedIn, TikTok, and YouTube through the SocialCannon API and optional MCP integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[miprinia](https://clawhub.ai/user/miprinia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to authenticate with SocialCannon, connect social accounts, create and schedule posts, upload media, inspect calendars and analytics, manage engagement replies, run A/B tests, repurpose content, and generate tracked links. <br>

### Deployment Geography for Use: <br>
Global, subject to SocialCannon availability and the user's connected social-platform accounts, tier limits, and platform policies. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform live public-facing actions, including publishing, replying, deleting posts, disconnecting accounts, repurposing content in post mode, running immediate A/B tests, and uploading media when credentials are available. <br>
Mitigation: Preview content, verify account and post IDs, confirm destructive or public actions before execution, and prefer scheduled or preview modes when available. <br>
Risk: The skill requires sensitive SocialCannon client credentials and OAuth-connected social accounts. <br>
Mitigation: Store credentials in environment variables, restrict access to the agent runtime, and rotate or revoke credentials if exposure is suspected. <br>
Risk: Uploaded media can become publicly accessible and platform-specific requirements can cause failed or unintended posts. <br>
Mitigation: Upload only media intended for public use and verify platform requirements such as TikTok privacy levels and Instagram or TikTok media requirements before posting. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/miprinia/socialcannon) <br>
- [SocialCannon homepage](https://socialcannon.app) <br>
- [SocialCannon MCP package](https://www.npmjs.com/package/@socialcannon/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with curl examples, JSON request and response shapes, and MCP configuration snippets.] <br>
**Output Parameters:** [SOCIALCANNON_CLIENT_ID, SOCIALCANNON_CLIENT_SECRET, Bearer token, account IDs, post IDs, media URLs, content, dates, platform options, and endpoint-specific fields.] <br>
**Other Properties Related to Output:** [Requires curl for REST examples and SocialCannon credentials; generated actions can publish, schedule, delete, reply, upload media, and manage connected accounts.] <br>

## Skill Version(s): <br>
1.8.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
