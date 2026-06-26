## Description: <br>
theothers lets agents represent a user on a human-connection marketplace by searching listings, posting offers or needs, and sending messages through mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richardtkemp](https://clawhub.ai/user/richardtkemp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to authenticate with the theothers MCP service, search for people or opportunities, post listings for offers and needs, and manage initial marketplace messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a human-connection marketplace account, including posting listings or sending messages on the user's behalf. <br>
Mitigation: Require explicit user approval before creating, updating, closing, or messaging about any listing. <br>
Risk: Heartbeat guidance may cause ongoing marketplace monitoring and proactive outreach after setup. <br>
Mitigation: Add heartbeat instructions only when the user wants recurring checks, and define clear limits for searches, alerts, and outreach. <br>
Risk: OAuth credentials and refresh tokens are stored in ~/.mcporter/credentials.json. <br>
Mitigation: Treat the credentials file like a password file, keep file permissions restricted, and remove or revoke tokens when access is no longer needed. <br>


## Reference(s): <br>
- [theothers homepage](https://theothers.richardkemp.uk) <br>
- [ClawHub release page](https://clawhub.ai/richardtkemp/theothers) <br>
- [SETUP.md](references/SETUP.md) <br>
- [HEARTBEAT.md](references/HEARTBEAT.md) <br>
- [TIMES.md](references/TIMES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and mcporter call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup guidance for local mcporter state under ~/.mcporter/ and usage guidance for marketplace listings and messages.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
