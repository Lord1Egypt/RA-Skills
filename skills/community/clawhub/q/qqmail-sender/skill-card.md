## Description:

Email Sender helps OpenClaw AI Agents send and receive QQ Mail messages over SMTP/POP3, including text or HTML bodies, attachments, and CC/BCC recipients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feastfuyan](https://clawhub.ai/user/feastfuyan)

### License/Terms of Use:

MIT License

## Use Case:

Developers and teams using OpenClaw AI Agents can use this skill to automate email-based notifications, report delivery, file transfer, and multi-agent collaboration through a dedicated QQ Mail account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox credentials or authorization codes may give an agent broad access to send or receive email.

Mitigation: Use a dedicated least-privilege mailbox or app authorization code and avoid sharing primary account credentials.

Risk: Automated sending, auto-replies, or attachments can disclose sensitive information or reach unintended recipients.

Mitigation: Review recipients, attachment contents, and auto-reply rules before sending, and do not attach secrets or regulated data.

Risk: Dependency installation commands can affect the runtime environment.

Mitigation: Prefer pinned or isolated dependency installs before using the skill in a production agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feastfuyan/skills/qqmail-sender)
- [Publisher profile](https://clawhub.ai/user/feastfuyan)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and shell code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides QQ Mail SMTP/POP3 configuration guidance and example email automation snippets.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
