## Description:

Helps agents read, search, draft, and manage Gmail, Outlook, and IMAP/SMTP mail using the Surface CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vishalj99](https://clawhub.ai/user/vishalj99)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents managing Gmail, Outlook, or IMAP mail use this skill to find and read messages, monitor threads, prepare replies, and perform requested mailbox actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive mailbox contents and attachments.

Mitigation: Use only for mail the user has authorized the agent to access, and read only messages needed for the task.

Risk: Sending or changing mail can have unintended effects.

Mitigation: Respect local write-safety settings, prefer drafts, and use configured test recipients for live send tests.

Risk: Direct password flags can expose mailbox credentials.

Mitigation: Avoid direct password flags; use supported environment, file, or command-based password options.

Risk: An external summarizer may receive email content when enabled.

Mitigation: Confirm the privacy tradeoff with the user before enabling or changing an external summarizer.

## Reference(s):

- [Surface CLI project homepage (listed in skill metadata)](https://github.com/VishalJ99/surface-cli)
- [Surface CLI ClawHub release](https://clawhub.ai/vishalj99/skills/surface-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Surface CLI returns JSON for mailbox operations.]

## Skill Version(s):

0.4.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
