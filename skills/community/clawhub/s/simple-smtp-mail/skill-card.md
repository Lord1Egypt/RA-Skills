## Description: <br>
Send emails via SMTP using the msmtp command-line tool configured with local SMTP account settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[HITYGX](https://clawhub.ai/user/HITYGX) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure msmtp and send SMTP email messages from a local account. It supports common provider settings, installation commands, test commands, and examples for plain text and HTML email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send email from a user's SMTP account, creating external side effects if recipients, sender, subject, or body are wrong. <br>
Mitigation: Require the agent to show the exact recipient, sender, subject, and body for user confirmation before any email is sent. <br>
Risk: SMTP credentials may be stored in local configuration and exposed if plaintext files are handled carelessly. <br>
Mitigation: Use app-specific or least-privilege SMTP credentials and prefer msmtp passwordeval or a system keychain instead of plaintext passwords when possible. <br>
Risk: The artifact contains an example command with a hard-coded user-specific msmtp config path. <br>
Mitigation: Replace hard-coded paths with the user's intended config path, such as ~/.msmtp/config, before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/HITYGX/simple-smtp-mail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell command examples and SMTP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires msmtp and a configured SMTP account; generated send commands can transmit email externally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
