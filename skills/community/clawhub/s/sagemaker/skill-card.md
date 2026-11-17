## Description:

SageMaker gives agents a unified memory-and-growth operating system for layered memory, self-model calibration, preflight and retro loops, and gate-based recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenured-master-chef-607](https://clawhub.ai/user/tenured-master-chef-607)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use SageMaker to equip an agent with a consistent memory workflow that captures short-term evidence, promotes reusable conclusions, calibrates a self-model, and gates daily or weekly memory updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can affect later tasks if inaccurate or unreviewed guidance is promoted.

Mitigation: Review memory changes before promotion and keep memory scoped per project or user.

Risk: Repository text, documents, web content, and tool output can become standing behavioral rules if treated as trusted memory.

Mitigation: Treat external content and tool output as untrusted evidence unless approved before promotion into persistent memory.

Risk: Mandatory memory updates and broad future influence require review before installation.

Mitigation: Install only when persistent memory behavior is desired and review the skill's memory-update workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tenured-master-chef-607/skills/sagemaker)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with file paths, JSON examples, and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can direct creation or update of persistent memory files and gate state.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
