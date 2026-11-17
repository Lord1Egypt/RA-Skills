## Description:

Safe shutdown/reboot workflow for local or remote machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jvy](https://clawhub.ai/user/jvy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to safely prepare, confirm, schedule, cancel, or execute shutdown and reboot commands for a local or remote machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shutdown or reboot commands can terminate work or disconnect active sessions if run against the wrong target or at the wrong time.

Mitigation: Require explicit confirmation of the target machine, action, timing, exact command, expected impact, and cancellation path before execution.

Risk: Remote shutdown or reboot may disconnect the operator from the host before follow-up checks can run.

Mitigation: Warn about remote session loss before confirmation and recommend post-reboot reachability, service, process, port, and listener checks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jvy/skills/shutdown)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Confirmation-gated command recommendations with platform-specific safety checks.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
