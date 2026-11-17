## Description:

Execute terminal commands safely and reliably with clear pre-checks, output validation, and recovery steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[big-fox](https://clawhub.ai/user/big-fox)

### License/Terms of Use:


## Use Case:

Developers, operators, and automation agents use this skill to inspect system state, run shell or CLI commands, manage files or services, and recover from command failures with verification after state-changing steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Terminal commands can modify files, install packages, start services, or require elevated privileges.

Mitigation: Review state-changing or privileged commands before execution, keep operations scoped, and verify observable outcomes afterward.

Risk: Terminal output can expose sensitive values if secrets are pasted into commands, logs, or diagnostics.

Mitigation: Avoid including secrets in terminal output unless necessary and redact sensitive values before sharing logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/big-fox/skills/terminal-command-execution)
- [Publisher Profile](https://clawhub.ai/user/big-fox)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command output summaries, validation steps, and next commands when action is required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
