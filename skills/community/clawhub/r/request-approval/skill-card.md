## Description:

Use Preloop's request_approval tool to get human approval before risky operations like deletions, production changes, or external modifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yconst](https://clawhub.ai/user/yconst)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to add human approval checkpoints before destructive, production, security, financial, or externally modifying actions. It helps agents gather impact details, request approval through Preloop, and stop when approval is denied or unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup documentation includes an unpinned MCP server command, which can make installations harder to audit.

Mitigation: Prefer direct HTTPS/SSE configuration or a pinned, purpose-specific Preloop MCP client before deploying the skill.

Risk: Approval requirements may be weakened outside production, even though destructive or externally modifying actions can still cause harm in development or staging.

Mitigation: Keep approval required for destructive or externally modifying actions unless an organization has an explicit policy exception.

Risk: Preloop API tokens or authorization headers may be needed for authenticated instances.

Mitigation: Store API tokens as secrets, avoid committing them to configuration files, and review MCP setup before installation.

## Reference(s):

- [Setup & Configuration](references/SETUP.md)
- [Detailed Examples](references/EXAMPLES.md)
- [Troubleshooting](references/TROUBLESHOOTING.md)
- [Preloop Documentation](https://docs.preloop.ai)
- [Agent Skills Specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Guidance, Text, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline tool-call parameters, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Preloop MCP server and approval policy.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
