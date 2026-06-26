## Description: <br>
Sends plain text or HTML email with optional local file attachments through a configured SMTP account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xlbbb-cn](https://clawhub.ai/user/xlbbb-cn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to send email from automation workflows through an existing SMTP account, including optional HTML content and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected local files outside the machine as email attachments. <br>
Mitigation: Review every recipient, subject, body source, and attachment path before execution. <br>
Risk: SMTP credentials can authorize outbound email from the configured account. <br>
Mitigation: Use a dedicated low-privilege SMTP credential, enable TLS where possible, and restrict permissions on smtp-config.json. <br>
Risk: Documented retry, logging, and markdown-conversion behavior is not reliable in the provided implementation. <br>
Mitigation: Do not depend on those advertised features unless the implementation is updated and re-reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xlbbb-cn/smtp-sender) <br>
- [Publisher profile](https://clawhub.ai/user/xlbbb-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Text] <br>
**Output Format:** [Command-line email send operation using JSON SMTP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can send message body text or file content and can attach local files selected by the agent or user.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
