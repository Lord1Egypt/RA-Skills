## Description: <br>
so-me.studio is a multi-platform social-media scheduler that helps agents schedule posts, manage drafts, reply to inbox messages and comments, generate AI content, query analytics, manage media and biolinks, and react to webhooks across major social platforms. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yasin047](https://clawhub.ai/user/yasin047) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Social media operators, marketers, and support teams use this skill to let an agent schedule and draft social posts, triage inbox conversations, generate content, collect analytics, and manage connected workspace resources through the so-me.studio CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent operate connected social accounts and workspace settings with broad posting, inbox, webhook, account, and team-management capabilities. <br>
Mitigation: Use the least-privileged so-me.studio credential available and require explicit human approval before posting, replying, deleting content, changing team roles, modifying webhooks, disconnecting accounts, or deleting or leaving workspaces. <br>
Risk: An API key or saved login gives the agent access to sensitive social-media and workspace actions. <br>
Mitigation: Keep SOMESTUDIO_API_KEY out of logs and chat output, rotate credentials when access changes, and avoid admin credentials for routine scheduling or analytics work. <br>


## Reference(s): <br>
- [so-me.studio documentation](https://docs.so-me.studio) <br>
- [so-me.studio CLI package](https://www.npmjs.com/package/@so-me/cli) <br>
- [so-me.studio website](https://so-me.studio) <br>
- [so-me.studio app](https://app.so-me.studio) <br>
- [Webhook payloads](https://docs.so-me.studio/webhooks/payloads) <br>
- [MCP server overview](https://docs.so-me.studio/mcp/overview) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON-aware workflow examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid SOMESTUDIO_API_KEY or browser OAuth session for so-me.studio CLI access.] <br>

## Skill Version(s): <br>
0.1.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
