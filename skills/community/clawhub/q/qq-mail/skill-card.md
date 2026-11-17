## Description:

Summarizes visible QQ Mail mailbox lists, unread counts, labels, and public share pages without automating login, sending, receiving, or permission bypass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codenova58](https://clawhub.ai/user/codenova58)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to summarize non-sensitive QQ Mail metadata from visible mailbox pages or public share links, including subjects, senders, timestamps, unread status, labels, titles, and public attachment names.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose visible QQ Mail metadata such as subjects, senders, timestamps, labels, and unread status to the agent session.

Mitigation: Use it only with mailboxes and public share links whose metadata may be shared with the agent, and avoid storing or outputting sensitive private details.

Risk: Mailbox pages may require login and human verification.

Mitigation: Keep interaction human-controlled; the skill should not automate login, send mail, receive mail, or bypass account security controls.

## Reference(s):

- [QQ Mail](https://mail.qq.com/)
- [ClawHub Skill Page](https://clawhub.ai/codenova58/skills/qq-mail)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text summaries and reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not produce executable code, persistent storage, credential automation, or email send/receive actions.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
