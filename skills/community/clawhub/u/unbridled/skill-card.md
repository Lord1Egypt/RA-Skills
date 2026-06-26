## Description: <br>
Send and read messages on Facebook Messenger, WhatsApp, Instagram, LinkedIn, Twitter/X, Signal, Telegram, Discord and other networks through a Beeper account, using the cloud Matrix bridges, Matrix E2EE, Beeper recovery-key cross-signing, a sync daemon, and a Python wrapper for chat listing, search, send, and history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkobject](https://clawhub.ai/user/jkobject) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to read, search, summarize, and send messages across a user's Beeper-bridged chat networks from a single Matrix-backed interface. It is intended for personal or delegated messaging workflows where every outbound message is handled as a privileged action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can provide broad, durable access to a Beeper account, encrypted chat history, and message sending from linked social accounts. <br>
Mitigation: Install only on a dedicated trusted host, keep disk encryption and strict file permissions enabled, and revoke the Beeper session if the host or files are exposed. <br>
Risk: Recovery keys, access tokens, and local Olm stores can enable account impersonation or private-message disclosure if leaked. <br>
Mitigation: Store secrets outside the repository with restrictive permissions, avoid exposing digest output in shared temporary locations, and reset the recovery key after suspected exposure. <br>
Risk: Automated outbound messaging can send unintended, sensitive, or spam-like messages from the user's accounts. <br>
Mitigation: Require explicit user confirmation before every send, avoid mass-send loops, and maintain an audit trail for outgoing messages. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jkobject/unbridled) <br>
- [Publisher Profile](https://clawhub.ai/user/jkobject) <br>
- [Project Homepage](https://github.com/jkobject/unbridled) <br>
- [Architecture](references/architecture.md) <br>
- [Setup Checklist](references/setup-checklist.md) <br>
- [Beeper Bridge Manager](https://github.com/beeper/bridge-manager) <br>
- [matrix-nio](https://github.com/poljar/matrix-nio) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, Python examples, and command output from messaging actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include private chat metadata or message text when the agent runs the skill against a configured Beeper account.] <br>

## Skill Version(s): <br>
0.2.3 (source: SKILL.md frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
