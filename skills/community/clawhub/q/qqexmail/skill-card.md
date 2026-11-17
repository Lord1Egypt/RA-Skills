## Description:

Sends, lists, and retrieves Tencent Exmail messages over IMAP/SMTP using credentials supplied through environment variables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunger09](https://clawhub.ai/user/hunger09)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators with Tencent Exmail mailboxes use this skill to send mail, list recent inbox messages, and fetch a full message body by UID from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The email-sending script disables TLS certificate verification, which could expose mailbox credentials or sent mail on a compromised network.

Mitigation: Do not use the sending script with a real mailbox until TLS certificate verification is restored and tested.

Risk: The skill can read mailbox content and print message summaries or full bodies to the console.

Mitigation: Use a dedicated Tencent Exmail authorization code, keep credentials in environment variables, and avoid shared terminals or persistent logs for sensitive mail.

Risk: Runtime dependencies handle mailbox credentials and message content.

Mitigation: Install from the included lockfile after dependency review, and keep dependencies pinned and updated through normal security review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hunger09/skills/qqexmail)
- [Source skill instructions](artifact/SKILL.md)
- [Publisher profile](https://clawhub.ai/user/hunger09)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and console text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses EXMAIL_ACCOUNT and EXMAIL_AUTH_CODE environment variables; mailbox content may be printed to stdout.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
