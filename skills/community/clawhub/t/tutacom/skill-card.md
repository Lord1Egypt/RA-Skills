## Description:

Send, read, and manage email through a user's Tuta account using a Python CLI client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aididmyhomework](https://clawhub.ai/user/aididmyhomework)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent log in to a Tuta account, list inbox messages, read decrypted mail, and send non-confidential email to external recipients.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access mailbox contents and send email through the configured Tuta account.

Mitigation: Use a dedicated low-risk account where possible and install only when that mailbox access and sending authority are acceptable.

Risk: Credentials and decrypted mailbox keys may be exposed through command-line password use, plaintext configuration, or reusable session files.

Mitigation: Avoid command-line passwords and plaintext config, store session files in a private user directory instead of /tmp, keep file permissions restricted, and delete session files when work is complete.

Risk: The documented dependency install uses system-level pip behavior that can affect the host Python environment.

Mitigation: Install dependencies in a pinned virtual environment before running the client.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aididmyhomework/skills/tutacom)
- [Tuta REST endpoint referenced by artifact](https://app.tuta.com/rest/)
- [Rust client reference cited by artifact](https://github.com/nenaddi/tutanota_client)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with bash commands; CLI commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tuta credentials and a local session file for reused mailbox access.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
