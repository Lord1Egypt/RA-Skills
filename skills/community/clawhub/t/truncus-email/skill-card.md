## Description:

Send transactional emails (alerts, reports, receipts, notifications) via the Truncus API. Use when a workflow needs to deliver email to a recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codevanmoose](https://clawhub.ai/user/codevanmoose)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to send transactional email for alerts, reports, receipts, notifications, and other workflow-driven delivery through Truncus.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email contents, recipient data, metadata, and attachments may be sent to Truncus.

Mitigation: Use a scoped API key and avoid sending secrets or regulated data unless the use case has been approved.

Risk: Local development mode may print email payload details into transcripts or logs.

Mitigation: Avoid sensitive payloads during simulated sends and review logs or transcripts before sharing them.

Risk: Open and click tracking may collect engagement signals when enabled.

Mitigation: Disable open and click tracking when tracking is not needed or not approved.

Risk: The skill can send real email when explicitly invoked with a configured API key.

Mitigation: Confirm recipients and intent before sending, use a unique idempotency key for each send, and report failures or simulated sends honestly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codevanmoose/skills/truncus-email)
- [Metadata homepage](https://github.com/codevanmoose/truncus-openclaw-skill)
- [README](artifact/README.md)
- [Send a basic email](artifact/send_basic_email.md)
- [Send an HTML report](artifact/send_html_report.md)
- [Send a monitoring alert](artifact/send_alert.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Truncus API request payloads, response summaries, and delivery status guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
