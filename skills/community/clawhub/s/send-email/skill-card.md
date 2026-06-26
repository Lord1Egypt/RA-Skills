## Description: <br>
Send emails via SMTP. Configure in ~/.openclaw/openclaw.json under skills.entries.send-email.env. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fontStep](https://clawhub.ai/user/fontStep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents use this skill to send plain-text emails, with optional local file attachments, through a user-configured SMTP account. It is intended for workflows where the user has already configured SMTP credentials for OpenClaw runtime injection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email and optional local file attachments through the configured account. <br>
Mitigation: Verify recipients, subject, body, and attachment paths before execution, and install only where this sending authority is acceptable. <br>
Risk: An alternate shell script can use local msmtp or mutt profiles outside the documented OpenClaw environment-variable credential path. <br>
Mitigation: Prefer the documented Python script path and remove or ignore send_email.sh unless the publisher documents the msmtp/.msmtprc behavior clearly. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [Command-line invocation guidance and SMTP send results as terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SMTP credentials supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
