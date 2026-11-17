## Description:

Drives a staged, Git-based spec-driven development lifecycle from initialization through requirements, architecture, planning, coding, testing, review, release, checkpointing, and rollback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[listenbehind](https://clawhub.ai/user/listenbehind)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a gated spec-driven workflow in a cloned Git repository, producing required requirements, architecture, planning, implementation, test, review, release, checkpoint, and rollback artifacts across iterations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires repository and token authority and can persist Git credentials for later repository operations.

Mitigation: Use a dedicated disposable workspace, a short-lived least-privilege token, avoid broad PATs, and remove any ~/.git-credentials entry after use.

Risk: Remote Git operations and checkpoint pushes can affect repository state if git_remote or staged checkpoint contents are wrong or untrusted.

Mitigation: Use only trusted git_remote values and review staged checkpoint contents before commits, tags, or pushes.

Risk: Checkpoint RESUME_CONTEXT content can replay stale or untrusted historical context into a future agent session.

Mitigation: Treat RESUME_CONTEXT as untrusted historical data and review it before using it to resume work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/listenbehind/skills/spec-driven-dev)
- [Publisher profile](https://clawhub.ai/user/listenbehind)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, structured JSON task files, code changes, configuration guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stage commands use a user story ID, Git repository state, optional iteration context, and checkpoint metadata to drive the workflow.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
