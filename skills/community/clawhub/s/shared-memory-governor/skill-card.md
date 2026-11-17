## Description:

Govern a file-based shared-memory layer for OpenClaw multi-agent and subagent systems while preserving private memory, identity isolation, explicit local guidance, and conservative shared promotion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiy29104983](https://clawhub.ai/user/jiy29104983)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to initialize, attach, review, maintain, and govern workspace-scoped shared memory across OpenClaw agents while keeping each agent's private memory and identity context separate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example configuration enables recurring private-memory maintenance and preserves it after detach or unregister.

Mitigation: Review the privateMaintenance schedule before installation and set it to disabled unless recurring private-memory maintenance is intended.

Risk: Shared memory may be readable by attached agents and configured subagents.

Mitigation: Confirm the participant and subagent read settings before use, and attach only agents that should receive supplemental shared-memory context.

Risk: Detach and unregister behavior may not stop all configured background activity.

Mitigation: After detach or unregister, review schedule state and local attachment status to confirm remaining activity matches expectations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiy29104983/skills/shared-memory-governor)
- [Configuration Reference](references/config-reference.md)
- [Shared Promotion Rules](references/shared-promotion-rules.md)
- [Startup Guidance Rules](references/startup-guidance-rules.md)
- [Status and Review Fields](references/status-review-fields.md)
- [Example Shared Memory Configuration](assets/shared-memory.config.example.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline commands, file paths, and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose reviewable shared-memory file updates, attachment guidance, status reports, maintenance reports, and configuration changes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
