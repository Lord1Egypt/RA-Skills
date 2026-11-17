## Description:

Local-first email skill for agents that guides IMAP sync into maildir and SQLite FTS5, then supports CLI search, read, thread, contact, attachment, inbox, and OpenAI-assisted mail questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cirne](https://clawhub.ai/user/cirne)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure zmail and query a user's mailbox through local-first CLI workflows. It is suited to email search, message reading, thread review, attachment extraction, contact lookup, and synthesized answers over indexed mail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned npm or npx installation can execute a newer package version than the reviewed release while handling mailbox credentials and email content.

Mitigation: Review and pin @cirne/zmail to version 0.1.2 before installation or execution, and avoid sudo.

Risk: IMAP credentials, OpenAI API keys, and email-derived content are sensitive and may be exposed through command lines, chat transcripts, local files, or provider calls.

Mitigation: Provide secrets through the user's shell environment or protected config, avoid pasting secrets into chats or command arguments, and use the skill only when the mailbox owner accepts local caching and OpenAI or enrichment-provider processing.

Risk: zmail stores a local mailbox cache, SQLite index, maildir data, and credentials under ZMAIL_HOME by default.

Mitigation: Treat ZMAIL_HOME and its .env file as sensitive local data, apply appropriate file permissions and backup controls, and use documented local wipe behavior when removing cached data.

Risk: Building shell command strings with untrusted email or chat content can create command-injection exposure.

Mitigation: Invoke zmail with argument arrays or careful quoting, and do not interpolate untrusted message text into sh -c command strings.

## Reference(s):

- [ClawHub zmail skill page](https://clawhub.ai/cirne/skills/zmail)
- [zmail project homepage](https://github.com/cirne/zmail)
- [zmail repository](https://github.com/cirne/zmail)
- [Canonical docs and agent discovery](references/CANONICAL-DOCS.md)
- [OpenClaw creating skills](https://docs.openclaw.ai/tools/creating-skills)
- [Agent Skills specification](https://agentskills.io/specification.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node 20+, npm, zmail on PATH after install, IMAP credentials, and an OpenAI API key for setup, ask, and inbox workflows.]

## Skill Version(s):

0.1.2 (source: server evidence, artifact metadata, and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
