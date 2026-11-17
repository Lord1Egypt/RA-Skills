## Description:

Connects agents to Revdoku mailboxes to read and reply to email, manage attachments, and store or share authorized files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emirn](https://clawhub.ai/user/emirn)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users manage incoming email, attachments, and cloud files in authorized Revdoku mailboxes, including replies, uploads, and approved account or mailbox changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the skill saves a local credential and grants access to selected mail and files.

Mitigation: Install only for intended Revdoku access, authorize the selected mailbox, and keep credentials private.

Risk: Recursive uploads can include private files in a selected folder.

Mitigation: Preview uploads with dry-run and select only files intended for transfer.

Risk: Sending email, configuring webhooks, archiving, or deleting can affect external recipients or stored data.

Mitigation: Review exact recipients and targets before acting; require explicit approval for permanent deletion.

## Reference(s):

- [Revdoku homepage](https://revdoku.com)
- [Revdoku API documentation](https://revdoku.com/api.md)
- [Revdoku first email workflow](https://revdoku.com/docs.md#first-email-workflow)
- [Revdoku ClawHub release](https://clawhub.ai/emirn/skills/revdoku)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown responses, CLI output, and downloaded files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mailbox summaries, file links, and action confirmations.]

## Skill Version(s):

1.0.566 (source: ClawHub release, VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
