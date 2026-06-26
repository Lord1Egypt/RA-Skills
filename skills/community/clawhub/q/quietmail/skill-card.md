## Description: <br>
Provides AI agents with no-verification email sending and mailbox management through a REST API backed by mailcow infrastructure. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[co1onnese](https://clawhub.ai/user/co1onnese) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to create agent email identities, send outbound email, and inspect sent or received mailbox data through a simple API. It is intended for agents that need operational email for notifications, reports, account signups, or similar automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables an agent to control an external email account and send broad outbound email. <br>
Mitigation: Restrict approved recipients and sending volume, and require human approval before outbound mail is sent. <br>
Risk: The release includes live-looking SMTP credentials and test scripts that can exercise real mail infrastructure. <br>
Mitigation: Rotate or remove bundled SMTP credentials before use and avoid running live SMTP test scripts unless explicitly authorized. <br>
Risk: quiet-mail API keys and mailbox passwords grant access to agent mailboxes. <br>
Mitigation: Treat API keys and mailbox passwords as secrets, store them outside source code, and revoke or rotate them after exposure. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/co1onnese/quietmail) <br>
- [API documentation](API.md) <br>
- [README](README.md) <br>
- [quiet-mail homepage](https://quiet-mail.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl, Python, Node.js, shell examples, and JSON API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for creating agent mailboxes, sending email, listing messages, and handling API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
