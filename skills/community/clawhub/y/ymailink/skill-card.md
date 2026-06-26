## Description: <br>
ymailink helps agents guide users through installing, configuring, and using a terminal email client for IMAP/SMTP, Outlook, Gmail, Exchange, attachments, message composition, and AI-assisted email summaries or reply suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2969192546](https://clawhub.ai/user/2969192546) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other terminal users use this skill when they need agent guidance for reading, sending, searching, organizing, and automating email from the command line. It also supports setup and troubleshooting for email credentials, OAuth flows, backend-specific configuration, RFC 822 message composition, attachments, and optional AI-assisted summaries or replies. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide commands that access or change email accounts, including sending, moving, deleting, purging, and flagging messages. <br>
Mitigation: Review commands before execution, use the intended account and folder, and confirm destructive mailbox operations before running them. <br>
Risk: The skill requires sensitive email credentials or OAuth configuration for normal use. <br>
Mitigation: Prefer OAuth, system keyring, or password-manager commands over raw passwords, and restrict permissions on configuration and token files. <br>
Risk: AI features may send selected email content to an external AI service. <br>
Mitigation: Avoid using AI commands on confidential mail unless the user explicitly accepts that external processing. <br>
Risk: The security evidence recommends verifying the upstream package source before installation. <br>
Mitigation: Install only from a trusted source and confirm the package origin before granting access to email accounts. <br>


## Reference(s): <br>
- [ymailink Configuration Reference](references/configuration.md) <br>
- [Message Composition Reference](references/message-composition.md) <br>
- [ymailink upstream homepage](https://github.com/lizhisec/ymailink) <br>
- [ClawHub skill page](https://clawhub.ai/2969192546/ymailink) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands, TOML examples, and procedural guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include command examples, configuration snippets, troubleshooting steps, and cautions for credentials, mailbox changes, and AI email processing.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
