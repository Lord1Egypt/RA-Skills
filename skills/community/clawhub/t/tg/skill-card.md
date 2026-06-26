## Description: <br>
Telegram CLI helps agents read, search, and send Telegram messages, and look up contacts, groups, members, and admins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent check Telegram inboxes, search chats, read messages, and send or reply to messages through the tg command-line interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing and using this skill can give an agent access to private Telegram content. <br>
Mitigation: Authenticate only the Telegram account intended for agent use, and avoid broad search or sync commands for sensitive chats unless local copies are acceptable. <br>
Risk: The skill can send or reply to Telegram messages as the authenticated user. <br>
Mitigation: Confirm the recipient, chat, and message text before executing send or reply commands. <br>
Risk: The skill depends on the @cyberdrk/tg package. <br>
Mitigation: Install only if the package is trusted or its source has been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arein/tg) <br>
- [Telegram API application settings](https://my.telegram.org/apps) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; Telegram CLI results may be plain text, Markdown, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Telegram API credentials and an authenticated tg session before message access or sending.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
