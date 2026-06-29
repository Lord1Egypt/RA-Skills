## Description: <br>
Slack API integration with managed OAuth for sending messages, managing channels, searching conversations, retrieving user information, handling files and reactions, and automating Slack workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent work with Slack through Maton-managed OAuth, including message, channel, user, file, search, reaction, pin, star, and bookmark workflows. It is appropriate when the user intends to connect a Slack workspace and approve any write or destructive actions before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents through Slack write or destructive operations such as posting, updating, deleting, archiving, inviting, kicking, uploading, pinning, and bookmark changes. <br>
Mitigation: Require explicit user approval before any create, update, delete, moderation, or workspace-changing Slack request, and confirm the target channel, user, message, file, or connection before execution. <br>
Risk: Requests act through the connected Slack workspace and Maton API key, so an incorrect or unintended connection could affect the wrong account or workspace. <br>
Mitigation: Verify the active Maton authentication state and specify the intended Slack connection when multiple connections exist. <br>
Risk: The skill requires outbound network access and a MATON_API_KEY credential. <br>
Mitigation: Use the skill only in environments where network access is intended, keep the API key secret, and avoid exposing it in logs, prompts, shell history, or shared outputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/skills/slack-api) <br>
- [Publisher Profile](https://clawhub.ai/user/byungkyu) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Slack API Methods](https://api.slack.com/methods) <br>
- [Slack Web API Reference](https://api.slack.com/web) <br>
- [Slack Block Kit Reference](https://api.slack.com/reference/block-kit) <br>
- [Slack Message Formatting](https://api.slack.com/reference/surfaces/formatting) <br>
- [Slack Rate Limits](https://api.slack.com/docs/rate-limits) <br>
- [Maton CLI Manual](https://cli.maton.ai/manual) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell, Python, JavaScript, JSON, and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, a valid MATON_API_KEY, and an active Slack OAuth connection through Maton.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release evidence; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
