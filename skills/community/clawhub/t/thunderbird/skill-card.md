## Description:

Read and search local Mozilla Thunderbird mail storage on disk. Use when working with Thunderbird profiles, extracting emails from local folders or IMAP cache, locating messages by sender/recipient/subject/body, checking which account a mailbox belongs to, or answering inbox questions for a specific Thunderbird account such as "do I have unread mail today?" or "search mail for user@example.com".

This skill is ready for commercial/non-commercial use.

## Publisher:

[komelt](https://clawhub.ai/user/komelt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect local Thunderbird profiles, find messages by account, folder, sender, recipient, subject, body, unread state, date range, or attachment, and summarize or export matching local mail artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive local email content and metadata.

Mitigation: Use the narrowest profile, account, folder, query, and date filters possible, and avoid placing full bodies or JSON output in shared logs.

Risk: Saving or opening email attachments can introduce normal email-attachment malware risk.

Mitigation: Save attachments only to an intended location and open unknown attachments only when the user accepts that risk.

Risk: IMAP results may omit messages that are not present in Thunderbird's local cache.

Mitigation: Tell users when results come from local cache and may not represent the full server mailbox.

## Reference(s):

- [Thunderbird storage layout](references/storage-layout.md)
- [ClawHub skill page](https://clawhub.ai/komelt/skills/thunderbird)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands; CLI results as table-like text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write saved attachment files when the user explicitly requests attachment export.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
