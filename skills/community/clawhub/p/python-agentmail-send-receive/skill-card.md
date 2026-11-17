## Description:

Provides Python scripts and setup guidance for sending email, downloading unread AgentMail inbox messages, and replying to existing email threads through the AgentMail API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lausser](https://clawhub.ai/user/lausser)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to configure AgentMail API access, send outbound email, download unread messages as local JSON files, and reply in existing threads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AgentMail API key that can send email and read unread mailbox content.

Mitigation: Store the API key securely, restrict access to the .env file, and install only where this mailbox access is acceptable.

Risk: Downloaded MAIL.* files can contain sensitive email content and attachments metadata.

Mitigation: Treat generated mail files as sensitive data and remove or protect them after processing.

Risk: Running the mail check marks downloaded unread messages as read.

Mitigation: Run the script only when changing unread mailbox state is intended.

Risk: Dependencies are installed dynamically from package indexes during setup.

Mitigation: Pin and review dependencies before use in controlled or production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lausser/skills/python-agentmail-send-receive)
- [Project homepage](https://github.com/lausser/python-agentmail-send-receive)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Python and shell command examples; scripts produce JSON mail files and status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloads unread email content to local MAIL.* JSON files and marks downloaded messages as read.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
