## Description: <br>
Read, send, search, and manage Slack messages and DMs via the slk CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[therohitdas](https://clawhub.ai/user/therohitdas) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to check Slack activity, read channels or DMs, search workspace messages, manage drafts, and send or react to Slack messages from a macOS terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill extracts and caches a desktop Slack session that can access DMs, private channels, and workspace content available to the logged-in user. <br>
Mitigation: Install only when this access is intentional, use one-time Keychain Allow where practical, and protect or delete the token cache when it is not needed. <br>
Risk: The skill can send messages, add reactions, and delete drafts as the logged-in Slack user. <br>
Mitigation: Require user confirmation before send, reaction, or draft deletion actions, especially in agent-driven workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/therohitdas/slk) <br>
- [npm Package: slkcli](https://www.npmjs.com/package/slkcli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires macOS, Slack Desktop, Node.js 18+, and an authenticated Slack desktop session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
