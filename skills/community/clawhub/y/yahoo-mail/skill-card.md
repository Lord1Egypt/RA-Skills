## Description:

Yahoo Mail integration over IMAP and SMTP with an app-specific password.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maton](https://clawhub.ai/user/maton)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to read, search, organize, draft, send, and manage Yahoo Mail, and to set up user-approved email automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting grants the service access to the selected Yahoo mailbox.

Mitigation: Use a separate app-specific password, select the intended connection, and revoke access when the work is complete.

Risk: Sending mail or deleting messages, drafts, folders, or connections can have lasting effects.

Mitigation: Review the exact target and proposed change, use dry-run where available, and obtain user approval before each consequential action.

Risk: Automations can run mail actions later or deliver events to configured destinations.

Mitigation: Review the function code, trigger destination, and duration before enabling an automation; remove it and revoke access when finished.

## Reference(s):

- [Yahoo Mail skill on ClawHub](https://clawhub.ai/maton/skills/yahoo-mail)
- [Yahoo: generate and manage app passwords](https://help.yahoo.com/kb/SLN15241.html)
- [Yahoo: IMAP server settings](https://help.yahoo.com/kb/SLN4075.html)
- [RFC 3501: IMAP4rev1](https://www.rfc-editor.org/rfc/rfc3501)
- [RFC 8474: IMAP extension for object identifiers](https://www.rfc-editor.org/rfc/rfc8474)
- [RFC 5321: SMTP](https://www.rfc-editor.org/rfc/rfc5321)
- [Maton Docs](https://docs.maton.ai)
- [Maton CLI Manual](https://cli.maton.ai/manual)
- [Time trigger reference](references/time/triggers.md)
- [Calendly trigger reference](references/calendly/triggers.md)
- [GitHub trigger reference](references/github/triggers.md)
- [Google Mail trigger reference](references/google-mail/triggers.md)
- [HubSpot trigger reference](references/hubspot/triggers.md)
- [Linear trigger reference](references/linear/triggers.md)
- [Notion trigger reference](references/notion/triggers.md)
- [Slack trigger reference](references/slack/triggers.md)
- [Stripe trigger reference](references/stripe/triggers.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Code, Configuration instructions, Guidance]

**Output Format:** [Markdown instructions and responses with shell commands, optional code examples, and structured mail results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox content or changes and optional automation code or configuration; consequential actions require user approval.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
