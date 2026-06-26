## Description: <br>
Slack API integration with smart AI features: send messages, read channels, search conversations, and manage workspaces with Claude-powered summarization and drafting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evolinkai](https://clawhub.ai/user/evolinkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, employees, and workspace operators use this skill to let an agent inspect Slack activity, draft replies, post messages, search conversations, and manage channels from terminal-driven workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post messages, upload files, invite users, react, and archive channels when granted broad Slack scopes. <br>
Mitigation: Use a dedicated least-privilege Slack app and require explicit human confirmation before write, upload, invite, reaction, or archive actions. <br>
Risk: Optional AI commands can send Slack message content, sender names, and channel information to EvoLink. <br>
Mitigation: Enable AI features only with informed consent, avoid sensitive channels, and keep EVOLINK_API_KEY unset when third-party processing is not acceptable. <br>
Risk: Security evidence reports unsafe handling of Slack or user text in executable Python snippets. <br>
Mitigation: Avoid AI commands on untrusted or highly sensitive Slack channels until the interpolation issue is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/evolinkai/slack-assistant) <br>
- [Slack API Reference](https://api.slack.com/methods) <br>
- [EvoLink API documentation](https://docs.evolink.ai/en/api-manual/language-series/claude/claude-messages-api?utm_source=clawhub&utm_medium=skill&utm_campaign=slack) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text and Markdown with inline bash commands; Slack and AI responses may include structured summaries or reply drafts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Slack OAuth credentials for core operations; optional AI features require EVOLINK_API_KEY and may transmit Slack content to api.evolink.ai.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
