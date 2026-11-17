## Description:

Helps agents save, restore, and switch structured project session context using local markdown files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aptratcn](https://clawhub.ai/user/aptratcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to maintain project continuity by saving active tasks, decisions, file maps, blockers, and environment notes, then restoring that context at the start of a later session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local context notes may contain sensitive project state if users save secrets, credentials, customer data, or raw connection details.

Mitigation: Keep the .context directory out of source control when it may contain sensitive state, review entries before saving or restoring, and never store secrets, tokens, passwords, connection strings, customer data, or credential files in the markdown notes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aptratcn/skills/session-context-bridge)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reviewable session notes and context file structure guidance without requiring external services.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
