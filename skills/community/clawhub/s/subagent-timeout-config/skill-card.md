## Description:

Configures OpenClaw subagent timeout fields atomically with preset or custom profiles, TTL constraint validation, automatic backup, dry-run preview, and optional gateway restart.

This skill is ready for commercial/non-commercial use.

## Publisher:

[songhonglei](https://clawhub.ai/user/songhonglei)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect, preview, and update OpenClaw timeout settings for subagents that need longer task budgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change OpenClaw timeout settings and restart the gateway.

Mitigation: Use --dry-run first and prefer --no-restart when a gateway interruption would be disruptive.

Risk: Configuration writes may need stronger permission preservation on multi-user systems.

Mitigation: Review file permissions after applying changes and harden the writer before use in shared environments.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/songhonglei/skills/subagent-timeout-config)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dry-run, status, profile, custom-value, config-path, and restart-control CLI invocations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
