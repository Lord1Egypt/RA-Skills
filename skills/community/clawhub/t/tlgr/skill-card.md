## Description:

Guides agents in reading and managing a personal Telegram account through the tlgr command-line tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erfnzdeh](https://clawhub.ai/user/erfnzdeh)

### License/Terms of Use:

MIT-0

## Use Case:

People using an agent with a personal Telegram account can check messages, search chats, send replies, and manage conversations and account features through tlgr.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting the CLI grants access to sensitive personal Telegram content and account actions.

Mitigation: Install only with the account owner's consent and restrict commands to the tasks needed.

Risk: Sending messages or changing chats and account settings can have unintended effects.

Mitigation: Require explicit confirmation before sending to new contacts, deleting, blocking, leaving chats, or changing account settings.

Risk: Credentials shared in chat or command arguments may be exposed.

Mitigation: Use environment-variable, standard-input, or file-based secret options instead of sharing passwords in chat.

## Reference(s):

- [tlgr on ClawHub](https://clawhub.ai/erfnzdeh/skills/tlgr)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suggested tlgr commands return JSON and use exit codes to indicate outcomes.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
