## Description:

Memory Manager helps OpenClaw agents organize shared memory files, archive project memory, check agent memory paths, and log memory-management operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wcwudi](https://clawhub.ai/user/wcwudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to coordinate memory sharing between a main agent and sub-agents, archive memory files, inspect memory-system health, and keep operation logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross-agent memory access can expose another agent's memory path beyond intended sharing.

Mitigation: Disable or narrow the default writing-assistant memory path unless that access is explicitly required, and keep agent access read-only unless writes are deliberately approved.

Risk: PowerShell guidance includes ExecutionPolicy Bypass and Force deletion or move examples.

Mitigation: Review scripts before running them, avoid ExecutionPolicy Bypass, preview file operations, back up affected files, and require explicit confirmation before destructive changes.

Risk: Release security evidence marks the skill verdict as suspicious.

Mitigation: Review before installing and treat file-management commands as proposals until the target paths, permissions, and intended files are verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wcwudi/skills/wcwudi-memory-manager)
- [README](artifact/README.md)
- [Quick Start](artifact/docs/QUICK_START.md)
- [Architecture](artifact/docs/ARCHITECTURE.md)
- [Default Configuration](artifact/config/default.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and JSON configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory-management instructions, file-operation workflows, and configuration guidance for an agent; it does not itself guarantee safe execution of file operations.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact config)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
