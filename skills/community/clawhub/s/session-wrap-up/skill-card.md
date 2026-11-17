## Description:

Wrap up a conversation session before starting a new one by flushing context to memory files, updating PARA notes, committing changes, and providing a summary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[branexp](https://clawhub.ai/user/branexp)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to preserve end-of-session context, update memory and note files, commit workspace changes, and receive a concise handoff summary before starting a new session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save conversation details into persistent memory and note files.

Mitigation: Review and redact sensitive session details before persisting them in memory, daily logs, or PARA notes.

Risk: The skill can automatically stage broad workspace changes, commit them, and push to a Git remote without a separate confirmation prompt.

Mitigation: Restrict staging to known memory and note paths, show the diff and status, and ask separately before committing or pushing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/branexp/skills/session-wrap-up)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files, guidance]

**Output Format:** [Markdown summary with shell command blocks and workspace file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update memory and note files, then run git add, commit, and push as part of the wrap-up workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
