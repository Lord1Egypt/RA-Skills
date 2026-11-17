## Description:

Audit Git repositories and worktrees, preserve findings, and monitor scheduled audit health without deleting work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to audit authorized Git repositories and worktrees, preserve findings in private state, and monitor scheduled audit health without performing cleanup or deployment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit runs Git subprocesses against configured repositories, which can expose credentials or command execution risk when repository Git configuration is hostile.

Mitigation: Run under a least-privileged account with a minimal environment and use only repositories whose Git configuration is trusted or hardened.

Risk: Scheduled operation and the --fetch, --github, or --persist options increase exposure to credentials, network access, and private state handling.

Mitigation: Delay scheduled or networked operation until credentials and network access are isolated, and keep persisted state outside source repositories, indexed memory, and public artifacts.

## Reference(s):

- [Configuration](references/configuration.md)
- [Findings and reports](references/findings.md)
- [Repository configuration example](references/repositories.example.json)
- [Scheduling](references/scheduling.md)
- [Supervised actions](references/supervised-actions.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown prose with inline shell commands and optional JSON audit or watchdog reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic cleanup; persisted audit state is private JSON when persistence is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
