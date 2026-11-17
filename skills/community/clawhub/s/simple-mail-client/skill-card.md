## Description:

Simple Mail Client lets agents send, receive, and manage email through SMTP and IMAP/POP3 account integrations with multi-account support, attachments, and message status controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wallinex](https://clawhub.ai/user/wallinex)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to connect an agent to configured mailboxes for sending messages, listing and reading mail, retrieving attachment metadata, and updating IMAP read or folder state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send, read, and modify email, which could expose mailbox data or perform unwanted mailbox actions if installed without review.

Mitigation: Review before installing, use a dedicated mailbox or app-specific password, and restrict which recipients and folders the agent may use.

Risk: Security evidence flags risky dependency and transport settings before trusting the skill with real mail.

Mitigation: Require TLS for SMTP and IMAP, regenerate the lockfile from an HTTPS registry, and update or audit the mail and YAML dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wallinex/skills/simple-mail-client)
- [Skill documentation](artifact/SKILL.md)
- [Configuration example](artifact/config.example.yaml)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [JSON-style handler responses with message summaries, message content, attachment metadata, and send or update status.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires host-side YAML account configuration and mailbox credentials; can send email and modify IMAP message state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
