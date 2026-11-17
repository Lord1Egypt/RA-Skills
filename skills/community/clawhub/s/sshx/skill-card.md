## Description:

Guides agents using sshx to inspect remote hosts, triage logs, run SSH commands, transfer and edit files, manage credentials, and perform guarded database changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamiesun](https://clawhub.ai/user/jamiesun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to guide agents through remote server inspection, command execution, file changes, and guarded SQL operations with sshx.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent access to remote hosts and databases can cause unintended or destructive changes.

Mitigation: Restrict access to trusted workspaces and task-scoped hosts; review dry-run plans and bind plans before mutations.

Risk: Safety bypasses and secret retrieval or discovery can expose credentials or remove operational safeguards.

Mitigation: Keep audits enabled and require explicit human approval before using safety bypasses, password retrieval, or env-file credential discovery.

## Reference(s):

- [sshx on ClawHub](https://clawhub.ai/jamiesun/skills/sshx)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and JSON response guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can return structured JSON or JSONL for agent interpretation.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
