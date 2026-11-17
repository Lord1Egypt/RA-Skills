## Description:

Roadrunner helps agents use the rr CLI to operate Beeper Desktop chats, messages, contacts, connect info, websocket events, search, and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johntheyoung](https://clawhub.ai/user/johntheyoung)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to inspect and operate local Beeper Desktop data through the rr command-line tool, including chat lookup, message search, status checks, reminders, and explicitly requested message actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private Beeper chats and contacts through local CLI reads.

Mitigation: Use read-only agent defaults for exploratory work and summarize only the minimum private data needed for the user's request.

Risk: Explicitly requested mutations can send messages, upload files, create chats, archive chats, or set reminders.

Mitigation: Require clear user intent, recipient identifiers, and message content before mutating, and prefer dry-run validation where available.

Risk: Authentication tokens for Beeper Desktop are sensitive local secrets.

Mitigation: Keep tokens configured locally and never paste, request, or store raw tokens in chat.

## Reference(s):

- [ClawHub Roadrunner Skill](https://clawhub.ai/johntheyoung/skills/roadrunner)
- [Roadrunner Project Homepage](https://github.com/johntheyoung/roadrunner)
- [Go install module for rr](https://pkg.go.dev/github.com/johntheyoung/roadrunner/cmd/rr)
- [Homebrew formula path](johntheyoung/tap/roadrunner)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON-oriented command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents toward structured JSON or JSON Lines CLI output, read-only and dry-run modes, and careful summarization of private chat data.]

## Skill Version(s):

0.17.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
