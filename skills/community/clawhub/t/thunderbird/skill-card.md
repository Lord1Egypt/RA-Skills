## Description: <br>
Read and search local Mozilla Thunderbird mail storage on disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KomelT](https://clawhub.ai/user/KomelT) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect local Thunderbird profiles, search mailboxes by account, folder, sender, recipient, subject, body, unread state, dates, and attachments, and answer mailbox questions from locally cached mail. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local mailbox searches can expose sensitive email content. <br>
Mitigation: Use narrow profile, account, folder, date, and limit filters, and request full-body output only when necessary. <br>
Risk: Saved or opened attachments may contain untrusted content. <br>
Mitigation: Save attachments only to deliberate locations and open them only when the sender and file type are trusted. <br>
Risk: IMAP cache results may be incomplete or stale compared with the server mailbox. <br>
Mitigation: Treat results as local-cache evidence and tell the user when a missing message may not have synced locally. <br>


## Reference(s): <br>
- [Thunderbird storage layout](references/storage-layout.md) <br>
- [ClawHub release page](https://clawhub.ai/KomelT/clawhub-thunderbird-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands; script output as table-like text or JSON; optional saved attachment files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write matching attachments to user-selected paths when attachment saving is explicitly requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
