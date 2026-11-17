## Description:

Interact with Threads (by Meta) via the yarn-threads-cli to read feeds and posts, inspect profiles, search users, and post, reply, or quote on Threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeizzon](https://clawhub.ai/user/jeizzon)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to let an agent operate yarn-threads-cli for authenticated Threads browsing, profile lookup, search, and posting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent sensitive Threads account access, including private feeds, saved content, account cookies, and public posting ability.

Mitigation: Install only reviewed, pinned versions in an isolated environment and require explicit user approval before reading private account data or posting publicly.

Risk: Manual session and CSRF tokens can be exposed if pasted into chat, logs, or shell history.

Mitigation: Prefer Chrome or Firefox profile authentication and avoid pasting session or CSRF tokens into chat or command history.

## Reference(s):

- [yarn-threads-cli documentation](https://github.com/jeizzon/yarn-threads-cli)
- [yarn-threads Command Reference](references/commands.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and CLI output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct use of JSON or plain-text CLI flags for parseable Threads data.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
